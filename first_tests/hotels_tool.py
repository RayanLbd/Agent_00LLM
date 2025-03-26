import os
import json
import requests
from typing import Optional, Type
from pydantic import BaseModel, Field

# LangChain / LangGraph
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool

################################################################################
# Schéma Pydantic pour les paramètres d'hôtels
################################################################################


class HotelSearchInput(BaseModel):
    """
    Schéma d'entrée pour la recherche d'hôtels via l'API Google Hotels (SerpApi).

    Champs obligatoires:
    - q (ex: "hotels in paris")
    - check_in_date, check_out_date (ex: "2025-01-04")

    Champs facultatifs selon la doc.
    """

    api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("SERPAPI_API_KEY", ""),
        description="Clé d'API SerpApi (si non fourni, on prend SERPAPI_API_KEY).",
    )
    q: str = Field(..., description="Requête de recherche (ex: 'Hotels in Paris')")
    check_in_date: str = Field(
        ..., description="Date d'arrivée (format YYYY-MM-DD, ex: 2025-01-04)"
    )
    check_out_date: str = Field(
        ..., description="Date de départ (format YYYY-MM-DD, ex: 2025-01-05)"
    )

    # Localisation & devise
    gl: Optional[str] = Field(
        None, description="Pays (code 2 lettres, ex: 'fr', 'us', etc.)"
    )
    hl: Optional[str] = Field(
        None, description="Langue (code 2 lettres, ex: 'fr', 'en', etc.)"
    )
    currency: Optional[str] = Field(None, description="Devise (ex: 'EUR', 'USD')")

    # Nombre de personnes
    adults: int = Field(2, description="Nombre d'adultes (défaut=2).")
    children: int = Field(0, description="Nombre d'enfants (défaut=0).")
    children_ages: Optional[str] = Field(
        None, description="Âges des enfants séparés par des virgules (ex: '5,8,10')."
    )

    # Filtres
    sort_by: Optional[int] = Field(
        None, description="Tri (3=lowest price, 8=highest rating, etc.)"
    )
    min_price: Optional[int] = Field(None, description="Prix min.")
    max_price: Optional[int] = Field(None, description="Prix max.")
    property_types: Optional[str] = Field(
        None, description="Types de propriété, ex: '17,12,18' pour plusieurs."
    )
    amenities: Optional[str] = Field(None, description="Commodités, ex: '35,9,19'.")
    rating: Optional[int] = Field(
        None, description="Filtre de note (7=3.5+, 8=4.0+, 9=4.5+)."
    )
    brands: Optional[str] = Field(
        None, description="Filtre sur des marques spécifiques, ex: '33,67'."
    )
    hotel_class: Optional[str] = Field(
        None, description="Filtre sur la classe (2,3,4,5 étoiles)."
    )
    free_cancellation: bool = Field(
        False, description="Activer le filtre 'annulation gratuite'."
    )
    special_offers: bool = Field(
        False, description="Activer le filtre 'offres spéciales'."
    )
    eco_certified: bool = Field(False, description="Filtre 'hôtel éco-certifié'.")
    vacation_rentals: bool = Field(
        False, description="Chercher uniquement des locations de vacances."
    )
    bedrooms: int = Field(0, description="Min bedrooms (vacation rentals seulement).")
    bathrooms: int = Field(0, description="Min bathrooms (vacation rentals seulement).")

    # Pagination
    next_page_token: Optional[str] = Field(
        None, description="Pour récupérer la page suivante."
    )

    # Property details
    property_token: Optional[str] = Field(
        None, description="Pour récupérer des détails sur une propriété."
    )


################################################################################
# Classe outil
################################################################################


class HotelSearchTool(BaseTool):
    """
    Outil de recherche d'hôtels (Google Hotels via SerpApi).

    Il suffit d'invoquer cet outil avec un JSON respectant 'HotelSearchInput'.
    """

    name: str = "hotel_search_tool"
    description: str = (
        "Recherche les hôtels (et/ou locations de vacances) disponibles via l'API Google Hotels (SerpApi). "
        "Paramètres attendus : voir HotelSearchInput."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(
        self,
        # On reprend tous les champs du HotelSearchInput
        api_key: Optional[str] = None,
        q: str = None,
        check_in_date: str = None,
        check_out_date: str = None,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        currency: Optional[str] = None,
        adults: int = 2,
        children: int = 0,
        children_ages: Optional[str] = None,
        sort_by: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        property_types: Optional[str] = None,
        amenities: Optional[str] = None,
        rating: Optional[int] = None,
        brands: Optional[str] = None,
        hotel_class: Optional[str] = None,
        free_cancellation: bool = False,
        special_offers: bool = False,
        eco_certified: bool = False,
        vacation_rentals: bool = False,
        bedrooms: int = 0,
        bathrooms: int = 0,
        next_page_token: Optional[str] = None,
        property_token: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # 1) Récupérer la clé d'API
        serpapi_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not serpapi_key:
            return "Error: No SerpApi key provided (SERPAPI_API_KEY)."

        # 2) Construire les paramètres pour l'appel GET
        params = {
            "engine": "google_hotels",
            "api_key": serpapi_key,
            "q": q,  # Ex: "hotels in paris"
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": adults,
            "children": children,
        }

        # Ajout des champs optionnels
        if gl:
            params["gl"] = gl
        if hl:
            params["hl"] = hl
        if currency:
            params["currency"] = currency
        if children_ages:
            params["children_ages"] = children_ages
        if sort_by is not None:
            params["sort_by"] = sort_by
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if property_types:
            params["property_types"] = property_types
        if amenities:
            params["amenities"] = amenities
        if rating is not None:
            params["rating"] = rating
        if brands:
            params["brands"] = brands
        if hotel_class:
            params["hotel_class"] = hotel_class
        if free_cancellation:
            params["free_cancellation"] = "true"
        if special_offers:
            params["special_offers"] = "true"
        if eco_certified:
            params["eco_certified"] = "true"
        if vacation_rentals:
            params["vacation_rentals"] = "true"
        if bedrooms > 0:
            params["bedrooms"] = bedrooms
        if bathrooms > 0:
            params["bathrooms"] = bathrooms
        if next_page_token:
            params["next_page_token"] = next_page_token
        if property_token:
            params["property_token"] = property_token

        # 3) Effectuer la requête
        try:
            response = requests.get(
                "https://serpapi.com/search", params=params, timeout=60
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error during API call: {str(e)}"

        # 4) (Optionnel) Parser ou filtrer la réponse
        #    Par exemple, vous pouvez limiter les résultats pour réduire le nombre de tokens

        raw_data = response.json()
        # Ex: On peut récupérer "hotel_results" si présent
        prop_list = raw_data.get("properties", [])
        hotel_results = [p for p in prop_list if p.get("type") == "hotel"]
        if not hotel_results:
            return "No hotels found for the given criteria."

        # On peut décider d'en prendre les 3 premiers
        hotel_results = hotel_results[:3]
        # On peut aussi nettoyer les données pour ne garder que ce qui nous intéresse
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

        # Convertir en JSON
        mini_json = json.dumps(
            {
                "results": cleaned_results,
                "raw_meta": {
                    # On peut stocker des infos additionnelles si besoin
                    "search_parameters": params,
                    "serpapi_metadata": raw_data.get("search_metadata", {}),
                },
            },
            ensure_ascii=False,
        )

        return mini_json

    async def _arun(
        self,
        # Même signature que _run, version async
        api_key: Optional[str] = None,
        q: str = None,
        check_in_date: str = None,
        check_out_date: str = None,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        currency: Optional[str] = None,
        adults: int = 2,
        children: int = 0,
        children_ages: Optional[str] = None,
        sort_by: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        property_types: Optional[str] = None,
        amenities: Optional[str] = None,
        rating: Optional[int] = None,
        brands: Optional[str] = None,
        hotel_class: Optional[str] = None,
        free_cancellation: bool = False,
        special_offers: bool = False,
        eco_certified: bool = False,
        vacation_rentals: bool = False,
        bedrooms: int = 0,
        bathrooms: int = 0,
        next_page_token: Optional[str] = None,
        property_token: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # Ici, on réutilise la logique synchrone
        return self._run(
            api_key=api_key,
            q=q,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            gl=gl,
            hl=hl,
            currency=currency,
            adults=adults,
            children=children,
            children_ages=children_ages,
            sort_by=sort_by,
            min_price=min_price,
            max_price=max_price,
            property_types=property_types,
            amenities=amenities,
            rating=rating,
            brands=brands,
            hotel_class=hotel_class,
            free_cancellation=free_cancellation,
            special_offers=special_offers,
            eco_certified=eco_certified,
            vacation_rentals=vacation_rentals,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            next_page_token=next_page_token,
            property_token=property_token,
            run_manager=run_manager,
        )
