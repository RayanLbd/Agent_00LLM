import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
meteo_api_key = os.getenv("METEO_API_KEY")


def fetch_city_coordinates(city_name, country_code, api_key, state_code=""):
    """
    Fetch the latitude and longitude of a city using OpenWeatherMap Geo API.

    Parameters:
        city_name (str): Name of the city.
        country_code (str): ISO 3166 country code.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        tuple: (latitude, longitude) of the city.
    """
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city_name},{state_code},{country_code}",
        "limit": 1,
        "appid": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            print("City not found.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None


def fetch_weather_data(lat, lon, api_key):
    """
    Fetch weather data from OpenWeatherMap API.

    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict: JSON response from the API.
    """
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "exclude": "minutely,hourly,current,alerts",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Fonction pour convertir un timestamp en date lisible
def get_readable_date(timestamp, timezone_offset):
    utc_time = datetime.fromtimestamp(timestamp, timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%Y-%m-%d %A")


# Example usage
if __name__ == "__main__":
    # Replace with your actual latitude, longitude, and API key
    latitude = 48.8566  # Example: Latitude for Paris
    longitude = 2.3522  # Example: Longitude for Paris
    city = "Paris"
    country_code = "FR"
    api_key = meteo_api_key
    city_coordinates = fetch_city_coordinates(city, country_code, api_key)
    if city_coordinates:
        latitude, longitude = city_coordinates
        print(f"City: {city}, Latitude: {latitude}, Longitude: {longitude}")

    weather_data = fetch_weather_data(latitude, longitude, api_key)

    if weather_data:
        for day in weather_data["daily"]:
            date = get_readable_date(day["dt"], weather_data["timezone_offset"])
            summary = day["summary"]
            temp_day = day["temp"]["day"]
            temp_min = day["temp"]["min"]
            temp_max = day["temp"]["max"]

            print(f"Date: {date}")
            print(f"Résumé: {summary}")
            print(
                f"Température - Jour: {temp_day}°C, Min: {temp_min}°C, Max: {temp_max}°C"
            )
            print("-" * 40)

    else:
        print("Failed to fetch weather data.")
