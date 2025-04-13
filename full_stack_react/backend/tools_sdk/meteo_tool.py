import os
import requests
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
from agents import function_tool

########################################
# Fonctions utilitaires
########################################


def fetch_city_coordinates(
    city_name: str, country_code: str, api_key: str, state_code: str = ""
):
    """
    Récupère la latitude et la longitude d'une ville en utilisant l'API Geo d'OpenWeatherMap.
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
            return None, None
    except requests.exceptions.RequestException:
        return None, None


def fetch_weather_data(lat: float, lon: float, api_key: str):
    """
    Récupère les données météo journalières depuis l'API One Call d'OpenWeatherMap.
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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def get_readable_date(timestamp: int, timezone_offset: int) -> str:
    """
    Convertit un timestamp Unix et un offset en une date lisible.
    """
    utc_time = datetime.fromtimestamp(timestamp, timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%Y-%m-%d %A")


########################################
# Schéma d'arguments pour l'outil météo
########################################


class WeatherToolInput(BaseModel):
    """
    Schéma d'entrée pour l'outil de météo.
    """

    city_name: str = Field(
        ..., description="Nom de la ville pour laquelle obtenir la météo."
    )
    country_code: str = Field(
        ..., description="Code ISO 3166 du pays (ex: 'FR' pour la France)."
    )


########################################
# Outil météo
########################################


@function_tool
def weather_forecast(input: WeatherToolInput) -> str:
    """
    Récupère la météo quotidienne pour la ville spécifiée.
    """
    meteo_api_key = os.getenv("METEO_API_KEY", "")
    if not meteo_api_key:
        return "Error: No METEO_API_KEY found in environment."

    # 1) Récupérer les coordonnées de la ville
    lat, lon = fetch_city_coordinates(
        input.city_name, input.country_code, meteo_api_key
    )
    if lat is None or lon is None:
        return f"City '{input.city_name}' not found or error in fetching coordinates."

    # 2) Récupérer les données météo
    weather_data = fetch_weather_data(lat, lon, meteo_api_key)
    if not weather_data:
        return "Failed to fetch weather data."

    # 3) Extraire les prévisions journalières
    daily_data = weather_data.get("daily", [])
    if not daily_data:
        return "No daily forecast found in the weather data."

    timezone_offset = weather_data.get("timezone_offset", 0)
    forecasts = []
    for day in daily_data:
        date_str = get_readable_date(day["dt"], timezone_offset)
        weather_desc = (
            day["weather"][0]["description"]
            if "weather" in day and day["weather"]
            else ""
        )
        temp_day = day["temp"]["day"]
        temp_min = day["temp"]["min"]
        temp_max = day["temp"]["max"]
        forecasts.append(
            f"{date_str}: {weather_desc}, day={temp_day}°C (min={temp_min}°C, max={temp_max}°C)"
        )

    return "\n".join(forecasts)


# Optionnel : version asynchrone
async def weather_forecast_arun(input: WeatherToolInput) -> str:
    return weather_forecast(input)
