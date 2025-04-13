import os
import json
import requests
from typing import Optional
from pydantic import BaseModel, Field
from agents import function_tool

################################################################################
# Schéma Pydantic pour les paramètres d'hôtels
################################################################################


class HotelSearchInput(BaseModel):
    """
    Schéma d'entrée pour la recherche d'hôtels via l'API Google Hotels (SerpApi).

    Champs obligatoires:
      - q (ex: "Hotels in Paris")
      - check_in_date, check_out_date (format YYYY-MM-DD, ex: "2025-01-04")

    Champs facultatifs selon la documentation.
    """

    api_key: Optional[str] = Field(
        None,
        description="Clé d'API SerpApi (si non fourni, on prendra la valeur de SERPAPI_API_KEY).",
    )
    q: str = Field(..., description="Requête de recherche (ex: 'Hotels in Paris').")
    check_in_date: str = Field(
        ..., description="Date d'arrivée (format YYYY-MM-DD, ex: '2025-01-04')."
    )
    check_out_date: str = Field(
        ..., description="Date de départ (format YYYY-MM-DD, ex: '2025-01-05')."
    )
    gl: Optional[str] = Field(
        None,
        description="Pays (code 2 lettres, ex: 'fr', 'us', etc.). Always put 'fr'.",
    )
    hl: Optional[str] = Field(
        None,
        description="Langue (code 2 lettres, ex: 'fr', 'en', etc.). Always put 'fr'.",
    )
    currency: Optional[str] = Field(
        None, description="Devise (ex: 'EUR', 'USD'). Always put 'EUR'."
    )
    adults: int = Field(..., description="Nombre d'adultes.")
    children: int = Field(..., description="Nombre d'enfants.")
    children_ages: Optional[str] = Field(
        None, description="Âges des enfants séparés par des virgules (ex: '5,8,10')."
    )
    sort_by: Optional[int] = Field(
        None,
        description="Tri par:\n -'3': Lowest Price,\n -'8' : Highest rating,\n -'13' : Most reviewed.",
    )
    min_price: Optional[int] = Field(None, description="Prix minimum.")
    max_price: Optional[int] = Field(None, description="Prix maximum.")
    property_types: Optional[str] = Field(
        None,
        description=(
            "Types de propriété, ex: '17,12,18' pour plusieurs. "
            "12: Beach hotels, 13: Boutique hotels, 14: Hostels, 15: Inns, "
            "16: Motels, 17: Resorts, 18: Spa hotels, 19: Bed and breakfasts, "
            "21: Apartment hotels, 22: Minshuku, 23: Japanese-style business hotels, "
            "24: Ryokan."
            " Do not put anyone of these values if the user do not ask for specific types."
        ),
    )
    amenities: Optional[str] = Field(
        None,
        description=(
            "Commodités, ex: '35,9,19'. "
            "1: Free parking, 3: Parking, 4: Indoor pool, 5: Outdoor pool, 6: Pool, "
            "7: Fitness center, 8: Restaurant, 9: Free breakfast, 10: Spa, 11: Beach access, "
            "12: Child-friendly, 15: Bar, 19: Pet-friendly, 22: Room service, 35: Free Wi-Fi, "
            "40: Air-conditioned, 52: All-inclusive available, 53: Wheelchair accessible, 61: EV charger."
            " Do not put anyone of these values if the user do not ask for specific amenities."
        ),
    )
    rating: Optional[int] = Field(
        None, description="Filtre de note des hôtels (7 = 3.5+, 8 = 4.0+, 9 = 4.5+)."
    )
    hotel_class: Optional[str] = Field(
        None,
        description="Filtre sur la classe: 2 = 2 étoiles, 3 = 3 étoiles, 4 = 4 étoiles, 5 = 5 étoiles. Pour plusieurs, utilisez '2,3,4'.",
    )
    free_cancellation: bool = Field(
        ..., description="Activer le filtre 'annulation gratuite'."
    )
    special_offers: bool = Field(
        ..., description="Activer le filtre 'offres spéciales'."
    )
    eco_certified: bool = Field(..., description="Filtre 'hôtel éco-certifié'.")
    property_token: Optional[str] = Field(
        None, description="Pour récupérer des détails sur une propriété."
    )


################################################################################
# Outil de recherche d'hôtels (Google Hotels via SerpApi)
################################################################################


@function_tool
def hotel_search(input: HotelSearchInput) -> str:
    """
    Effectue une recherche d'hôtels en construisant une requête GET vers l'API SerpApi.
    """
    serpapi_key = input.api_key or os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        return "Error: No SerpApi key provided (SERPAPI_API_KEY)."

    params = {
        "engine": "google_hotels",
        "api_key": serpapi_key,
        "q": input.q,
        "check_in_date": input.check_in_date,
        "check_out_date": input.check_out_date,
        "adults": input.adults,
        "children": input.children,
    }
    if input.gl:
        params["gl"] = input.gl
    if input.hl:
        params["hl"] = input.hl
    if input.currency:
        params["currency"] = input.currency
    if input.children_ages:
        params["children_ages"] = input.children_ages
    if input.sort_by is not None:
        params["sort_by"] = input.sort_by
    if input.min_price is not None:
        params["min_price"] = input.min_price
    if input.max_price is not None:
        params["max_price"] = input.max_price
    if input.property_types:
        params["property_types"] = input.property_types
    if input.amenities:
        params["amenities"] = input.amenities
    if input.rating is not None:
        params["rating"] = input.rating
    if input.hotel_class:
        params["hotel_class"] = input.hotel_class
    if input.free_cancellation:
        params["free_cancellation"] = "true"
    if input.special_offers:
        params["special_offers"] = "true"
    if input.eco_certified:
        params["eco_certified"] = "true"
    if input.property_token:
        params["property_token"] = input.property_token

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error during API call: {str(e)}"

    # Exemple de traitement de la réponse : filtrer et nettoyer quelques résultats
    raw_data = response.json()
    properties = raw_data.get("properties", [])
    hotel_results = [p for p in properties if p.get("type") == "hotel"]
    if not hotel_results:
        return "No hotels found for the given criteria."

    # Ne garder que les 3 premiers résultats et nettoyer les données
    hotel_results = hotel_results[:3]
    cleaned_results = []
    for hotel in hotel_results:
        cleaned_results.append(
            {
                "name": hotel.get("name"),
                "description": hotel.get("description"),
                "rating": hotel.get("overall_rating"),
                "price": hotel.get("rate_per_night", {}).get("lowest"),
                "hotel_class": hotel.get("extracted_hotel_class"),
                "address": hotel.get("nearby_places", [{}])[0].get(
                    "name", "No address info"
                ),
                "url": hotel.get("link"),
            }
        )

    mini_json = json.dumps(
        {
            "results": cleaned_results,
            "raw_meta": {
                "search_parameters": params,
                "serpapi_metadata": raw_data.get("search_metadata", {}),
            },
        },
        ensure_ascii=False,
    )

    return mini_json
