"""
Outil permettant de faire des recherches de vols via l'API Google Flights
(SerpApi). Permet de récupérer les disponibilités et prix de billets d'avion.
"""

import os
import requests
from typing import Optional, Type
from pydantic import BaseModel, Field

# Pour LangChain / LangGraph
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool

# -- Constantes pour l'API SerpApi (paramètre 'engine')
GOOGLE_FLIGHTS_ENGINE = "google_flights"


class FlightSearchInput(BaseModel):
    """
    Schéma d'entrée pour la recherche de vols.

    Champs facultatifs : l'utilisateur peut être plus ou moins précis.
    """

    # Paramètre obligatoire pour activer Google Flights
    api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("SERPAPI_API_KEY", ""),
        description=(
            "Clé d'API SerpApi. "
            "Si vous ne la passez pas dans la requête, on la prend depuis SERPAPI_API_KEY."
        ),
    )

    departure_id: Optional[str] = Field(
        None, description="Code aéroport ou kgmid de départ (ex: 'CDG', '/m/0vzm')."
    )
    arrival_id: Optional[str] = Field(
        None, description="Code aéroport ou kgmid d'arrivée (ex: 'AUS', '/m/04jpl')."
    )

    # Paramètres dates
    outbound_date: Optional[str] = Field(
        None, description="Date de départ au format 'YYYY-MM-DD' (ex: 2025-01-04)."
    )
    return_date: Optional[str] = Field(
        None, description="Date de retour au format 'YYYY-MM-DD' (ex: 2025-01-10)."
    )

    # Paramètre pour le type de vol
    # 1 - Round trip (par défaut), 2 - One way, 3 - Multi-city
    type: int = Field(
        1, description="Type de vol : 1 (Round trip), 2 (One way), 3 (Multi-city)."
    )

    # Classe de voyage
    # 1 - Economy (défaut), 2 - Premium economy, 3 - Business, 4 - First
    travel_class: int = Field(
        1, description="Classe de voyage (1=Econ, 2=Premium, 3=Business, 4=First)."
    )

    # Localisation
    gl: Optional[str] = Field(
        None, description="Pays (ex: 'us', 'fr') pour la recherche."
    )
    hl: Optional[str] = Field(
        None, description="Langue (ex: 'en', 'fr') pour la recherche."
    )
    currency: Optional[str] = Field(
        None, description="Devise du prix (ex: 'USD', 'EUR')."
    )

    # Nombre de passagers
    adults: int = Field(1, description="Nombre d'adultes (défaut = 1).")
    children: int = Field(0, description="Nombre d'enfants (défaut = 0).")
    infants_in_seat: int = Field(
        0, description="Nombre de bébés avec siège (défaut = 0)."
    )
    infants_on_lap: int = Field(
        0, description="Nombre de bébés sur les genoux (défaut = 0)."
    )

    # Filtres
    stops: int = Field(
        0,
        description=(
            "Nombre d'escales : 0=peu importe, 1=Nonstop only, 2=1 stop or fewer, 3=2 stops or fewer."
        ),
    )
    max_price: Optional[int] = Field(
        None, description="Prix max en unité de 'currency'."
    )

    # Paramètres horaires
    outbound_times: Optional[str] = Field(
        None,
        description=(
            "Tranche horaire départ/arrivée aller (ex: '4,18' pour 4h-18h départ, "
            "'4,18,3,19' pour départ 4h-18h + arrivée 3h-19h)."
        ),
    )
    return_times: Optional[str] = Field(
        None,
        description=(
            "Tranche horaire départ/arrivée retour (ex: '0,23,3,19'). "
            "Uniquement pour un round trip."
        ),
    )

    # Profondeur de recherche
    deep_search: bool = Field(
        False,
        description="Activer deep_search pour de meilleurs résultats (réponse + lente).",
    )

    # TODO: Ajouter plus de champs (multi_city_json, exclude_airlines, etc.) si besoin.


class FlightSearchTool(BaseTool):
    """
    Outil de recherche de vols (Google Flights via SerpApi).

    Il suffit d'invoquer cet outil avec un JSON respectant 'FlightSearchInput'.
    """

    name: str = "flight_search_tool"
    description: str = (
        "Recherche les vols disponibles (prix, horaires) via l'API Google Flights (SerpApi). "
        "Paramètres attendus : voir FlightSearchInput."
    )
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(
        self,
        # On reprend les champs de FlightSearchInput
        api_key: Optional[str] = None,
        departure_id: Optional[str] = None,
        arrival_id: Optional[str] = None,
        outbound_date: Optional[str] = None,
        return_date: Optional[str] = None,
        type: int = 1,
        travel_class: int = 1,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        currency: Optional[str] = None,
        adults: int = 1,
        children: int = 0,
        infants_in_seat: int = 0,
        infants_on_lap: int = 0,
        stops: int = 0,
        max_price: Optional[int] = None,
        outbound_times: Optional[str] = None,
        return_times: Optional[str] = None,
        deep_search: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Méthode synchrone pour exécuter la recherche de vols.

        Construire la requête GET vers:
        https://serpapi.com/search?engine=google_flights&...
        """
        # 1) Récupérer la clé d’API
        serpapi_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not serpapi_key:
            return "Error: No SerpApi key provided (SERPAPI_API_KEY)."

        # 2) Construire les paramètres
        params = {
            "engine": GOOGLE_FLIGHTS_ENGINE,
            "api_key": serpapi_key,
            # Principaux
            "type": type,  # 1=RoundTrip, 2=OneWay, 3=MultiCity
            "travel_class": travel_class,
            "adults": adults,
            "children": children,
            "infants_in_seat": infants_in_seat,
            "infants_on_lap": infants_on_lap,
            "stops": stops,
        }

        # Dates
        if outbound_date:
            params["outbound_date"] = outbound_date
        if return_date and type == 1:
            params["return_date"] = return_date

        # Aéroports
        if departure_id:
            params["departure_id"] = departure_id
        if arrival_id:
            params["arrival_id"] = arrival_id

        # Localisation & devise
        if gl:
            params["gl"] = gl
        if hl:
            params["hl"] = hl
        if currency:
            params["currency"] = currency

        # Filtres supplémentaires
        if max_price is not None:
            params["max_price"] = max_price
        if outbound_times:
            params["outbound_times"] = outbound_times
        if return_times and type == 1:
            params["return_times"] = return_times
        if deep_search:
            params["deep_search"] = "true"

        # 3) Appeler l'API
        try:
            response = requests.get(
                "https://serpapi.com/search", params=params, timeout=60
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error during API call: {str(e)}"

        # 4) Retourner le résultat brut en JSON
        return response.text  # ou .json() si vous préférez traiter le JSON avant

    async def _arun(
        self,
        # Même signature que _run, sauf qu'on gère l'async
        api_key: Optional[str] = None,
        departure_id: Optional[str] = None,
        arrival_id: Optional[str] = None,
        outbound_date: Optional[str] = None,
        return_date: Optional[str] = None,
        type: int = 1,
        travel_class: int = 1,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        currency: Optional[str] = None,
        adults: int = 1,
        children: int = 0,
        infants_in_seat: int = 0,
        infants_on_lap: int = 0,
        stops: int = 0,
        max_price: Optional[int] = None,
        outbound_times: Optional[str] = None,
        return_times: Optional[str] = None,
        deep_search: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Version asynchrone (si nécessaire). On peut utiliser aiohttp ou httpx, etc.
        """
        # Simplement on appelle la version synchrone dans cet exemple.
        return self._run(
            api_key=api_key,
            departure_id=departure_id,
            arrival_id=arrival_id,
            outbound_date=outbound_date,
            return_date=return_date,
            type=type,
            travel_class=travel_class,
            gl=gl,
            hl=hl,
            currency=currency,
            adults=adults,
            children=children,
            infants_in_seat=infants_in_seat,
            infants_on_lap=infants_on_lap,
            stops=stops,
            max_price=max_price,
            outbound_times=outbound_times,
            return_times=return_times,
            deep_search=deep_search,
            run_manager=run_manager,
        )
