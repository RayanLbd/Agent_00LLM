from agents import (
    Agent,
    Runner,
    WebSearchTool,
)
import asyncio
from prompts import (
    research_team_sdk_prompt,
    trip_planner_prompt,
    accomodation_agent_prompt,
    the_supervisor_sdk_prompt,
    pgrm_planner_prompt,
    pgrm_planner_tool_description,
)

# from flights_tool import FlightSearchTool, flight_search
from tools_sdk.google_flight_tool import flight_search
from tools_sdk.google_hotel_tool import hotel_search
from tools_sdk.meteo_tool import weather_forecast
from tools_sdk.trip_advisor_tool import (
    tripadvisor_activity_search,
    tripadvisor_restaurants_search,
)
from tools_sdk.calculator_tool import calculator
from datetime import date
from trip_types import TripData, FlightBlockData, HotelData, Day, Activity
from typing import List

today = date.today()

research_agent = Agent(
    name="Web research agent",
    instructions=research_team_sdk_prompt.format(today=today),
    model="gpt-4o-mini-2024-07-18",
    tools=[WebSearchTool(), weather_forecast],
)

pgrm_planner_agent = Agent(
    name="Program planner agent",
    instructions=pgrm_planner_prompt,
    model="gpt-4o-mini-2024-07-18",
    tools=[tripadvisor_activity_search, tripadvisor_restaurants_search],
    output_type=List[Day],
)

activity_agent = Agent(
    name="Activity agent",
    instructions=pgrm_planner_prompt,
    model="gpt-4o-mini-2024-07-18",
    tools=[WebSearchTool(), tripadvisor_activity_search],
    output_type=List[Activity],
)

transportation_planner_agent = Agent(
    name="Transportation planner agent",
    instructions=f"Today is the {today}" + trip_planner_prompt,
    model="gpt-4o-mini-2024-07-18",
    tools=[flight_search],
    output_type=FlightBlockData,
)

accomodation_agent = Agent(
    name="Accomodation agent",
    instructions=f"Today is the {today}" + accomodation_agent_prompt,
    model="gpt-4o-mini-2024-07-18",
    tools=[hotel_search],
    output_type=HotelData,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"Today is the {today}"
    + the_supervisor_sdk_prompt
    + "\n If you need additionnal help, you can choose an agent to help you answer the user's question",
    tools=[
        accomodation_agent.as_tool(
            tool_name="accomodation_agent",
            tool_description="Accomodation agent for hotel search. You should use it when you have a request about hotel availability. You need to precise dates and location and other criterias if needed.",
        ),
        transportation_planner_agent.as_tool(
            tool_name="transportation_planner_agent",
            tool_description="Trip planner agent for flight search. You should use it when you want some information about the transportation (like flights) for a specific trip (departure, arrival and dates at least, and other criterias if needed).",
        ),
        research_agent.as_tool(
            tool_name="research_agent",
            tool_description="Research agent for web search. You should use it when you have a request about meteo or general information that can be found on the web.",
        ),
        pgrm_planner_agent.as_tool(
            tool_name="pgrm_planner_agent",
            tool_description=pgrm_planner_tool_description,
        ),
        calculator,
    ],
    model="gpt-4o-mini-2024-07-18",
    output_type=TripData,
)


async def chat():
    print("Bienvenue dans le chatbot. Tapez 'exit' pour quitter.\n")
    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["exit", "quit"]:
            print("Au revoir !")
            break
        # Appel de l'agent superviseur avec la requête de l'utilisateur
        result = await Runner.run(triage_agent, user_input)
        print("\nAssistant :", result.final_output, "\n")


if __name__ == "__main__":
    asyncio.run(chat())
