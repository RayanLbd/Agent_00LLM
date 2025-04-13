from pydantic import BaseModel, Field
from typing import List, Optional


class DayFlight(BaseModel):
    from_: Optional[str] = Field(
        ...,
        alias="from",
        description="Departure location for the day's flight (only the city name, not the airport)",
    )
    to: Optional[str] = Field(
        ...,
        description="Arrival location for the day's flight (only the city name, not the airport)",
    )
    time: Optional[str] = Field(..., description="Departure time for the day's flight")


class DayHotel(BaseModel):
    name: Optional[str] = Field(..., description="Name of the hotel for the day")
    nights: Optional[int] = Field(
        ..., description="Total number of nights booked for the day"
    )


class Activity(BaseModel):
    title: Optional[str] = Field(..., description="Title of the activity")
    description: Optional[str] = Field(
        ..., description="Very concise description of the activity"
    )
    rating: Optional[str] = Field(..., description="Rating of the activity")
    vibe: Optional[str] = Field(
        ...,
        description="Vibe or mood of the activity in one word, based on the description",
    )
    image: Optional[str] = Field(..., description="URL for the activity's image")
    link: Optional[str] = Field(
        ..., description="Optional link associated with the activity"
    )


class FoodRecommendation(BaseModel):
    title: Optional[str] = Field(..., description="Title of the food recommendation")
    description: Optional[str] = Field(
        ..., description="Description of the food recommendation"
    )
    image: Optional[str] = Field(
        ..., description="URL for the food recommendation's image"
    )
    link: Optional[str] = Field(
        ..., description="Optional link associated with the food recommendation"
    )


class Day(BaseModel):
    dayLabel: Optional[str] = Field(
        ..., description="Label or number of the day, e.g. Day 1"
    )
    date: Optional[str] = Field(..., description="Date for the day (format YYYY-MM-DD)")
    dayTitle: Optional[str] = Field(
        ..., description="Title of the day, e.g. Beach and Local Culture"
    )
    dayDescription: Optional[str] = Field(
        ..., description="Detailed description of the day"
    )
    flight: Optional[DayFlight] = Field(
        ...,
        description="Flight information for the day (can be null, if there is no flight planned this day). Generally, the outbound flight is the first flight of the trip and the inbound flight is the last flight of the trip.",
    )
    hotel: Optional[DayHotel] = Field(..., description="Hotel information for the day")
    activities: Optional[List[Activity]] = Field(
        ...,
        description="List of activities planned for the day: What to do at this destination on this day?",
    )
    foodRecommendations: Optional[List[FoodRecommendation]] = Field(
        ..., description="List of food recommendations for the day"
    )


class FlightDetail(BaseModel):
    fromCity: Optional[str] = Field(..., description="City of departure for the flight")
    toCity: Optional[str] = Field(..., description="City of arrival for the flight")
    departureTime: Optional[str] = Field(..., description="Flight departure time")
    duration: Optional[str] = Field(..., description="Duration of the flight")
    airline: Optional[str] = Field(..., description="Airline operating the flight")
    flightClass: Optional[str] = Field(..., description="Class of the flight")
    fromAirport: Optional[str] = Field(..., description="Departure airport")
    toAirport: Optional[str] = Field(..., description="Arrival airport")
    baggage: Optional[str] = Field(
        ..., description="Baggage information included with the flight"
    )


class FlightBlockData(BaseModel):
    outbound: Optional[FlightDetail] = Field(
        ..., description="Details of the outbound flight"
    )
    inbound: Optional[FlightDetail] = Field(
        ..., description="Details of the return flight"
    )


class HotelData(BaseModel):
    name: Optional[str] = Field(..., description="Name of the hotel")
    nights: Optional[int] = Field(..., description="Total number of nights booked")
    rating: Optional[float] = Field(..., description="Hotel rating")
    reviewsCount: Optional[int] = Field(
        ..., description="Number of reviews for the hotel"
    )
    location: Optional[str] = Field(..., description="Location of the hotel")
    amenities: Optional[List[str]] = Field(..., description="List of hotel amenities")
    room: Optional[str] = Field(..., description="Type of room booked")
    website: Optional[str] = Field(..., description="URL of the hotel's website")
    mapLink: Optional[str] = Field(
        ..., description="Link to the hotel's location on a map"
    )


class Message(BaseModel):
    role: Optional[str] = Field(..., description="Sender role (assistant or user)")
    content: Optional[str] = Field(..., description="Content of the message")


class Passengers(BaseModel):
    adults: Optional[int] = Field(..., description="Number of adults")
    children: Optional[int] = Field(..., description="Number of children")


class Interface(BaseModel):
    price: Optional[float] = Field(..., description="Total price of the trip")
    dateRange: Optional[str] = Field(
        ..., description="Date range for the trip, e.g. May 9–13"
    )
    location: Optional[str] = Field(..., description="Destination of the trip")
    nights: Optional[int] = Field(..., description="Total number of nights")
    days: Optional[List[Day]] = Field(
        ...,
        description="Detailed itinerary by day: this is the program per day for the user. Make sure to fill all days: if the user asks for a detailed trip, you have to provide all the details for each day. It does not make sense to provide only the first day for a 7 days trip.",
    )
    topActivities: Optional[List[Activity]] = Field(
        ...,
        description="List of top activities for the trip from all the activities planned in the days",
    )
    flightBlockData: Optional[FlightBlockData] = Field(
        ..., description="Details of the outbound and inbound flights"
    )
    hotelData: Optional[HotelData] = Field(..., description="Hotel details")
    passengers: Optional[Passengers] = Field(
        ...,
        description="Number of adults and children for the trip. If not provided, use 1 adult and 0 children.",
    )


class TripData(BaseModel):
    interface: Interface = Field(
        ...,
        description="Data to populate a trip interface with all travel details.",
    )
    messages: List[Message] = Field(
        ...,
        description="History of messages between the assistant and the user. Add your answer here with the 'assistant' tag.",
    )
