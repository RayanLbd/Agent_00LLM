import getpass
import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from meteo_tool import WeatherForecastTool
from whatsapp_tool import WhatsAppTool
from flights_tool import FlightSearchTool
from hotels_tool import HotelSearchTool
from datetime import date


# from langchain_community import tools
from langchain_core.messages import ToolMessage
import json
from typing import Literal


# Charger les clés d'API depuis un fichier .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
meteo_api_key = os.getenv("METEO_API_KEY")


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")


# Création du graphe
class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

# Tools section
tavily_search_tool = TavilySearchResults(max_results=2)
weather_tool = WeatherForecastTool()
whatsapp_tool = WhatsAppTool()
flights_tool = FlightSearchTool()
hotels_tool = HotelSearchTool()
tools = [tavily_search_tool, weather_tool, whatsapp_tool, flights_tool, hotels_tool]
memory = MemorySaver()

# Node chatbot qui utilise l'API OpenAI
llm = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18")
llm_with_tools = llm.bind_tools(tools)

# Configuration du chatbot
today = date.today()
system_prompt = f"""
You are a travel planner assistant. Today is the {today}, so only make research for after this date. And we're in Paris, France.

For a full trip request, you have to provide the following information:
- The departure and destination city
- Dates of departure and return (if round trip)
- Total price and price per person
- Avions and hotels options
- Meteo information

For meteo research: 
- If the chosen dates are in the next seven days, use the weather tool. Otherwise, use the Tavily tool.
- Make sure to use the right city name when you look for information. For example, the full name for Tenerife is 'Santa Cruz de Tenerife'.

For flight research: 
- When the user mentions a city, you have to search for all airports nearby. For example for 'Paris', the departure airports as 'CDG,ORY,BVA' (all major Paris airports).
- If the user provides only one date, treat the request as a one-way trip (type=2).
- If the user provides two dates, treat the request as a round-trip (type=1).
- If no information is given on the expected results, give only the best result with those info: Departure airport, Arrival airport, Departure date and hour, Flight duration, Airline, Price per person

For hotel research:
- If no information is given on the expected results, give only the best result with those info: Hotel name and number of stars, Price per night, Rating, Address
"""


def chatbot(state: State):
    response = llm_with_tools.invoke([("system", system_prompt)] + state["messages"])
    return {"messages": [response]}


# Definition du graphe
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer=memory)

# Affichage du graphe
try:
    img_data = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img_data)
    img = mpimg.imread("graph.png")
    plt.imshow(img)

    plt.axis("off")
    plt.show()
except Exception:
    print("You need to install graphviz and mermaid to display the graph")


def stream_graph_updates(user_input: str):
    events = graph.stream(
        {"messages": [("user", user_input)]}, config, stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()


config = {"configurable": {"thread_id": "1"}}
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except Exception as e:
        # fallback if input() is not available
        print(f"An error occurred: {e}")
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break

# snapshot = graph.get_state(config)
# print(snapshot)
