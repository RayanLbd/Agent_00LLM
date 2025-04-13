import os
import requests
from typing import Optional, Type
from pydantic import BaseModel, Field
from agents import function_tool

# Constante pour l'API SerpApi
GOOGLE_FLIGHTS_ENGINE = "google_flights"


class FlightSearchInput(BaseModel):
    """
    Schéma d'entrée pour la recherche de vols.

    Champs facultatifs : l'utilisateur peut être plus ou moins précis.
    """

    api_key: Optional[str] = Field(
        None,
        description=(
            "Clé d'API SerpApi. Si non précisée, la valeur de SERPAPI_API_KEY est utilisée."
        ),
    )
    departure_id: Optional[str] = Field(
        None,
        description="Code aéroport (ou kgmid) de départ (ex: 'CDG'). Obligatoire si type=1 ou 2.",
    )
    arrival_id: Optional[str] = Field(
        None,
        description="Code aéroport (ou kgmid) d'arrivée (ex: 'AUS'). Obligatoire si type=1 ou 2.",
    )
    outbound_date: Optional[str] = Field(
        None,
        description="Date de départ au format 'YYYY-MM-DD' (ex: '2025-01-04'). Obligatoire si type=1 ou 2.",
    )
    return_date: Optional[str] = Field(
        None,
        description="Date de retour au format 'YYYY-MM-DD' (ex: '2025-01-10'). Obligatoire si type=1.",
    )
    type: int = Field(
        ...,
        description="Type de vol : 1 = Aller-retour, 2 = Aller simple, 3 = Multi-city.",
    )
    travel_class: int = Field(
        ...,
        description="Classe de voyage (1 = Economy, 2 = Premium Economy, 3 = Business, 4 = First). Do not use this parameter if the user did not specify a class.",
    )
    gl: Optional[str] = Field(
        None,
        description="Code pays (ex: 'us', 'fr') pour la recherche. Always put 'fr'.",
    )
    hl: Optional[str] = Field(
        None,
        description="Code langue (ex: 'en', 'fr') pour la recherche. Always put 'fr'.",
    )
    currency: Optional[str] = Field(
        None, description="Devise souhaitée (ex: 'USD', 'EUR'). Always put 'EUR'."
    )
    adults: int = Field(
        ...,
        description="Nombre d'adultes (ex: 1).",
    )
    children: int = Field(
        ...,
        description="Nombre d'enfants (ex: 0).",
    )
    infants_in_seat: int = Field(
        ...,
        description="Nombre de bébés avec siège (ex: 0).",
    )
    infants_on_lap: int = Field(
        ...,
        description="Nombre de bébés sur les genoux (ex: 0).",
    )
    stops: int = Field(
        ...,
        description=(
            "Nombre d'escales : 0 = peu importe, 1 = nonstop only, 2 = 1 stop or fewer, 3 = 2 stops or fewer. If the user did not specify a number of stops, use 0."
        ),
    )
    max_price: Optional[int] = Field(
        None, description="Prix maximum en unité de 'currency'."
    )
    outbound_times: Optional[str] = Field(
        None,
        description="Tranche horaire de départ/arrivée aller (ex: '4,18' ou '4,18,3,19').",
    )
    return_times: Optional[str] = Field(
        None,
        description="Tranche horaire de départ/arrivée retour (ex: '0,23,3,19'). Valable uniquement pour type=1.",
    )
    deep_search: bool = Field(
        ...,
        description="Activer deep_search pour des résultats améliorés (plus lent). By default, use false. We want it fast!",
    )
    sort_by: Optional[int] = Field(
        None,
        description=(
            "Ordre de tri : 1 = Top flights, 2 = Price, 3 = Departure time, 4 = Arrival time, 5 = Duration, 6 = Emissions. If the user did not specify a sort, use 1."
        ),
    )
    bags: Optional[int] = Field(
        None, description="Nombre de bagages cabine inclus (ex: 0). "
    )
    layover_duration: Optional[str] = Field(
        None,
        description="Durée d'escale minimale et maximale (ex: '90,330' pour entre 1h30 et 5h30).",
    )
    include_airlines: Optional[str] = Field(
        None,
        description="Liste de compagnies (codes IATA séparés par des virgules, ex: 'UA,AF').",
    )
    multi_city_json: Optional[str] = Field(
        None,
        description=(
            "JSON décrivant plusieurs segments de vols (exemple : "
            "[{'departure_id':'CDG','arrival_id':'NRT','date':'2025-03-12'}, "
            "{'departure_id':'NRT','arrival_id':'LAX','date':'2025-03-19'}])."
        ),
    )


@function_tool
def flight_search(input: FlightSearchInput) -> str:
    """
    Effectue une recherche de vols en construisant une requête GET vers l'API SerpApi.
    """
    serpapi_key = input.api_key or os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        return "Error: No SerpApi key provided (SERPAPI_API_KEY)."

    params = {
        "engine": GOOGLE_FLIGHTS_ENGINE,
        "api_key": serpapi_key,
        "type": input.type,
        "travel_class": input.travel_class,
        "adults": input.adults,
        "children": input.children,
        "infants_in_seat": input.infants_in_seat,
        "infants_on_lap": input.infants_on_lap,
        "stops": input.stops,
    }
    if input.outbound_date:
        params["outbound_date"] = input.outbound_date
    if input.return_date and input.type == 1:
        params["return_date"] = input.return_date
    if input.departure_id:
        params["departure_id"] = input.departure_id
    if input.arrival_id:
        params["arrival_id"] = input.arrival_id
    if input.type == 3 and input.multi_city_json:
        params["multi_city_json"] = input.multi_city_json
    if input.gl:
        params["gl"] = input.gl
    if input.hl:
        params["hl"] = input.hl
    if input.currency:
        params["currency"] = input.currency
    if input.max_price is not None:
        params["max_price"] = input.max_price
    if input.outbound_times:
        params["outbound_times"] = input.outbound_times
    if input.return_times and input.type == 1:
        params["return_times"] = input.return_times
    if input.deep_search:
        params["deep_search"] = "true"
    if input.sort_by is not None:
        params["sort_by"] = input.sort_by
    if input.bags is not None:
        params["bags"] = input.bags
    if input.layover_duration:
        params["layover_duration"] = input.layover_duration
    if input.include_airlines:
        params["include_airlines"] = input.include_airlines

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error during API call: {str(e)}"

    return response.text
