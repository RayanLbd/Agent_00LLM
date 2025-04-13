import os
import requests
from typing import Optional
from pydantic import BaseModel, Field
from agents import function_tool


class TrainSearchInput(BaseModel):
    """
    Schéma d'entrée pour la recherche d'itinéraires en train via l'API SNCF.
    """

    api_key: Optional[str] = Field(
        None,
        description="Clé d'API SNCF. Si non précisée, la variable d'environnement SNCF_API_KEY sera utilisée.",
    )
    departure: str = Field(
        ...,
        description="Identifiant ou code de la gare de départ (ex: 'admin:7444extern' pour Paris Gare de Lyon).",
    )
    arrival: str = Field(
        ...,
        description="Identifiant ou code de la gare d'arrivée (ex: 'admin:120965extern' pour Lyon Part-Dieu).",
    )
    datetime: str = Field(
        ...,
        description="Date et heure de départ au format YYYYMMDDTHHMMSS (ex: '20250123T140151').",
    )
    # Vous pouvez ajouter d'autres paramètres optionnels selon vos besoins


@function_tool
def train_search(input: TrainSearchInput) -> str:
    """
    Effectue une recherche d'itinéraires en train via l'API SNCF.
    """
    # Récupération de la clé API SNCF
    api_key = input.api_key or os.getenv("SNCF_API_KEY")
    if not api_key:
        return "Error: No SNCF API key provided. Please set the SNCF_API_KEY environment variable."

    # Préparation des en-têtes d'authentification
    headers = {"Authorization": api_key}

    # URL de base et paramètres de la requête
    base_url = "https://api.sncf.com/v1/coverage/sncf/journeys"
    params = {"from": input.departure, "to": input.arrival, "datetime": input.datetime}

    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error during SNCF API call: {str(e)}"

    return response.text
