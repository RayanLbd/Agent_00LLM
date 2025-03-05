from typing import Callable, List, Optional, Literal
from langchain_core.language_models.chat_models import BaseChatModel
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from typing_extensions import TypedDict
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from flights_tool import FlightSearchTool
from hotels_tool import HotelSearchTool
from whatsapp_tool import WhatsAppTool
from meteo_tool import WeatherForecastTool
from datetime import date
from langchain.callbacks import StdOutCallbackHandler
from prompts import (
    supervisors_prompt,
    research_team_prompt,
    the_supervisor_prompt,
    trip_planner_prompt,
    accomodation_agent_prompt,
)

today = date.today()

# On instancie les tools:
flights_tool = FlightSearchTool()
hotels_tool = HotelSearchTool()
whatsapp_tool = WhatsAppTool()
weather_forecast_tool = WeatherForecastTool()
tavily_tool = TavilySearchResults(max_results=3)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY", "")

llm = ChatOpenAI(
    model_name="gpt-4o-mini-2024-07-18",
    verbose=True,
    callbacks=[StdOutCallbackHandler()],
)


class State(MessagesState):
    next: str
    instructions: str


def make_supervisor_node(
    llm: BaseChatModel, members, custom_prompt=""
) -> Callable[[State], Command[str]]:
    system_prompt = custom_prompt + supervisors_prompt.format(
        today=today, members=members
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH. If workers needed, give instructions to worker.
        Add a comment to explain your next step. The answer if you have one is to display to the user."""

        next: str
        instructions: Optional[str]
        comment: Optional[str]
        answer: Optional[str]

    def supervisor_node(state: State) -> Command[str]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        # print("Supervisor messages avant llm:", messages)  # Debugging
        response = llm.with_structured_output(Router).invoke(messages)
        # print("Supervisor response après llm:", response)  # Debugging
        goto = response["next"]
        if goto == "FINISH":
            goto = END
        return Command(
            goto=goto,
            update={
                "next": goto,
                "instructions": response["instructions"],
                "messages": response["answer"],
            },
        )

    return supervisor_node


supervisor_custom_prompt = the_supervisor_prompt.format(today=today)
teams_supervisor_node = make_supervisor_node(
    llm,
    {
        "research_team": "Can search on the web and give meteo information",
        "trip_planner": "Can give flight availibilites",
        "accomodation_agent": "Can give accomodation availabilities like hotels",
    },
    supervisor_custom_prompt,
)

# ----------------------------------------------------------------------
# Research team: Websearch and meteo

search_agent = create_react_agent(llm, tools=[tavily_tool])


def search_node(state: State) -> Command[Literal["supervisor"]]:
    result = search_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="search")
            ]
        },
        goto="supervisor",
    )


meteo_agent = create_react_agent(llm, tools=[weather_forecast_tool])


def meteo_node(state: State) -> Command[Literal["supervisor"]]:
    result = meteo_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="meteo")
            ]
        },
        goto="supervisor",
    )


research_custom_prompt = research_team_prompt

research_supervisor_node = make_supervisor_node(
    llm, ["search", "meteo"], research_custom_prompt
)

research_builder = StateGraph(State)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("search", search_node)
research_builder.add_node("meteo", meteo_node)

research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()


def call_research_team(state: State) -> Command[Literal["supervisor"]]:
    content_to_send = state.get("instructions", "").strip()
    if not content_to_send:
        content_to_send = state["messages"][-1].content
    local_state = State(
        messages=[HumanMessage(content=content_to_send, name="research_team")]
    )
    sub_result = research_graph.invoke(local_state)
    last_message = sub_result["messages"][-1]
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_message.content, name="research_team")
            ]
        },
        goto="supervisor",
    )


# ----------------------------------------------------------------
# Trip agent: Flight search

flight_agent = create_react_agent(llm, tools=[flights_tool])


def search_flight_node(state: State) -> Command[Literal["supervisor"]]:
    result = flight_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="flight")
            ]
        },
        goto="supervisor",
    )


flight_custom_prompt = trip_planner_prompt

trip_supervisor_node = make_supervisor_node(llm, ["flight"], flight_custom_prompt)

flight_builder = StateGraph(State)
flight_builder.add_node("supervisor", trip_supervisor_node)
flight_builder.add_node("flight", search_flight_node)
flight_builder.add_edge(START, "supervisor")
flight_graph = flight_builder.compile()


def call_trip_team(state: State) -> Command[Literal["supervisor"]]:
    content_to_send = state.get("instructions", "").strip()
    if not content_to_send:
        content_to_send = state["messages"][-1].content
    local_state = State(
        messages=[HumanMessage(content=content_to_send, name="trip_planner")]
    )
    sub_result = flight_graph.invoke(local_state)
    last_message = sub_result["messages"][-1]
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_message.content, name="trip_planner")
            ]
        },
        goto="supervisor",
    )


# ----------------------------------------------------------------
# Accomodation agent

hotel_agent = create_react_agent(llm, tools=[hotels_tool])


def search_hotel_node(state: State) -> Command[Literal["supervisor"]]:
    result = hotel_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="hotel")
            ]
        },
        goto="supervisor",
    )


acco_custom_prompt = accomodation_agent_prompt

hotel_supervisor_node = make_supervisor_node(llm, ["hotel"], acco_custom_prompt)

hotel_builder = StateGraph(State)
hotel_builder.add_node("supervisor", hotel_supervisor_node)
hotel_builder.add_node("hotel", search_hotel_node)
hotel_builder.add_edge(START, "supervisor")
hotel_graph = hotel_builder.compile()


def call_accomodation_team(state: State) -> Command[Literal["supervisor"]]:
    content_to_send = state.get("instructions", "").strip()
    if not content_to_send:
        content_to_send = state["messages"][-1].content
    local_state = State(
        messages=[HumanMessage(content=content_to_send, name="accomodation_agent")]
    )
    sub_result = hotel_graph.invoke(local_state)
    last_message = sub_result["messages"][-1]
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_message.content, name="accomodation_agent")
            ]
        },
        goto="supervisor",
    )


# ----------------------------------------------------------------
# Define the graph.
super_builder = StateGraph(State)
super_builder.add_node("supervisor", teams_supervisor_node)
super_builder.add_node("research_team", call_research_team)
super_builder.add_node("trip_planner", call_trip_team)
super_builder.add_node("accomodation_agent", call_accomodation_team)
super_builder.add_edge(START, "supervisor")
super_graph = super_builder.compile()

try:
    img_data = super_graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img_data)
    img = mpimg.imread("graph.png")
    plt.imshow(img)

    plt.axis("off")
    plt.show()
except Exception:
    print("You need to install graphviz and mermaid to display the graph")


def stream_graph_updates(user_input: str):
    events = super_graph.stream(
        {"messages": [("user", user_input)]}, config, stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()


config = {"configurable": {"thread_id": "1"}}
state = State(messages=[])

emoji_dict = {
    "supervisor": "🤖",
    "research_team": "🌤️",
    "trip_planner": "🛫",
    "accomodation_agent": "🏨",
}
print("\nCharacters:")
print("🤖: Global Agent")
print("🌤️: Research team")
print("🛫: Trip planner")
print("🏨: Accomodation agent")
print("\n--- Starting the conversation ---\n")
while True:
    try:
        # Récupérer l'entrée utilisateur
        user_input = input("Vous : ")
        if user_input.lower() == "exit":
            print("Au revoir !")
            break

        if not user_input:
            continue

        # Ajouter l'entrée utilisateur dans les messages de l'état
        state["messages"].append(HumanMessage(content=user_input, name="user"))

        # print("\n--- Début de l'exécution du graphe ---\n")

        # Exécuter le graphe principal
        last_output = None
        for output in super_graph.stream(state, {"recursion_limit": 100}):
            last_output = output
            # print("--- Étape du graphe ---")
            for agent_identifier in output.keys():
                if len(output[agent_identifier]["messages"]) > 0:
                    if isinstance(output[agent_identifier]["messages"], list):
                        print(
                            f"\n{emoji_dict[agent_identifier]} : {output[agent_identifier]['messages'][-1].content}"
                        )
                        state["messages"].append(
                            output[agent_identifier]["messages"][-1]
                        )
                    else:
                        print(
                            f"\n{emoji_dict[agent_identifier]} : {output[agent_identifier]['messages']}"
                        )
                        state["messages"].append(
                            HumanMessage(
                                content=output[agent_identifier]["messages"],
                                name=agent_identifier,
                            )
                        )
                if (
                    "instructions" in output[agent_identifier]
                    and len(output[agent_identifier]["instructions"]) > 0
                ):
                    print(
                        f"\n{emoji_dict[agent_identifier]} -> {emoji_dict[output[agent_identifier]['next']]} : {output[agent_identifier]['instructions']}"
                    )

            print("---\n")

    except KeyboardInterrupt:
        print("\nAu revoir !")
        break
    except Exception as e:
        print(f"Erreur : {e}")
