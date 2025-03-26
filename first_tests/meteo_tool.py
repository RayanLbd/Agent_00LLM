# weather_tool.py
import os
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional, Type
from pydantic import BaseModel, Field

# LangChain / LangGraph
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool

########################################
# Fonctions utilitaires
########################################


def fetch_city_coordinates(
    city_name: str, country_code: str, api_key: str, state_code: str = ""
):
    """
    Fetch the latitude and longitude of a city using OpenWeatherMap Geo API.
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
    Fetch daily weather data from OpenWeatherMap API.
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
    except requests.exceptions.RequestException:
        return None


def get_readable_date(timestamp: int, timezone_offset: int) -> str:
    """
    Convert a Unix timestamp + offset en date lisible.
    """
    utc_time = datetime.fromtimestamp(timestamp, timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%Y-%m-%d %A")


########################################
# Schéma d'arguments pour l'outil
########################################


class WeatherToolInput(BaseModel):
    """
    Input pour l'outil de météo.
    """

    city_name: str = Field(..., description="Name of the city")
    country_code: str = Field(
        ..., description="ISO 3166 country code, e.g. 'FR' for France"
    )


########################################
# Classe outil
########################################


class WeatherForecastTool(BaseTool):
    """
    Outil pour récupérer la météo via OpenWeatherMap.
    Hérite de BaseTool (langchain-core) pour être compatible
    avec le pipeline d'outils.
    """

    # Identifiants "officiels" de l'outil
    name: str = "weather_forecast_tool"
    description: str = (
        "Get a daily weather forecast for a given city. "
        "Input arguments: {city_name, country_code}."
    )
    args_schema: Type[BaseModel] = WeatherToolInput

    # On peut stocker la clé API dans un champ Pydantic
    api_key: str = Field(default_factory=lambda: os.getenv("METEO_API_KEY", ""))

    def _run(
        self,
        city_name: str,
        country_code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Version synchrone de l'outil (appelé par .invoke(...) ou .run(...)).
        """
        if not self.api_key:
            return "Error: No METEO_API_KEY found in environment."

        # 1) Récupérer lat/lon
        lat, lon = fetch_city_coordinates(city_name, country_code, self.api_key)
        if lat is None or lon is None:
            return f"City '{city_name}' not found or error in fetching coordinates."

        # 2) Récupérer la météo
        weather_data = fetch_weather_data(lat, lon, self.api_key)
        if not weather_data:
            return "Failed to fetch weather data."

        # 3) Extraire les prévisions journalières
        daily_data = weather_data.get("daily", [])
        if not daily_data:
            return "No daily forecast found in the weather data."

        # 4) Formater la réponse
        timezone_offset = weather_data.get("timezone_offset", 0)
        forecasts = []
        for day in daily_data:
            date_str = get_readable_date(day["dt"], timezone_offset)
            # "summary" peut ne pas être dispo dans l'API onecall
            # on pioche par ex. dans day["weather"] s'il y en a
            weather_desc = day["weather"][0]["description"] if "weather" in day else ""
            temp_day = day["temp"]["day"]
            temp_min = day["temp"]["min"]
            temp_max = day["temp"]["max"]
            forecasts.append(
                f"{date_str}: {weather_desc}, day={temp_day}°C (min={temp_min}°C, max={temp_max}°C)"
            )

        return "\n".join(forecasts)

    async def _arun(
        self,
        city_name: str,
        country_code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Version asynchrone de l'outil (si nécessaire).
        """
        # Vous pouvez soit reprendre la logique synchrone,
        # soit utiliser un async client requests (httpx, etc.)
        return self._run(city_name, country_code, run_manager)
