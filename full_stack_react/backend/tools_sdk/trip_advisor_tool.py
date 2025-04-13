import os
import requests
from typing import List
from pydantic import BaseModel, Field
from agents import function_tool
import json
from trip_types import Activity

# Définir l'URL de base pour l'API TripAdvisor (vérifiez votre documentation)
TRIPADVISOR_BASE_URL = "https://api.content.tripadvisor.com/api/v1"


class TripAdvisorActivitySearchInput(BaseModel):
    search_query: str = Field(
        ..., description="Ville or region to search for activities (ex: 'Bali')"
    )


@function_tool
def tripadvisor_activity_search(input: TripAdvisorActivitySearchInput) -> str:
    tripadvisor_key = os.getenv("TRIPADVISOR_API_KEY")
    if not tripadvisor_key:
        return json.dumps({"error": "No TripAdvisor API key provided."})
    return tripadvisor_search(input, "attractions", tripadvisor_key=tripadvisor_key)


@function_tool
def tripadvisor_restaurants_search(input: TripAdvisorActivitySearchInput) -> str:
    tripadvisor_key = os.getenv("TRIPADVISOR_API_KEY")
    if not tripadvisor_key:
        return json.dumps({"error": "No TripAdvisor API key provided."})
    return tripadvisor_search(input, "restaurants", tripadvisor_key=tripadvisor_key)


def tripadvisor_search(
    input: TripAdvisorActivitySearchInput, category: str, tripadvisor_key
) -> str:
    """
    Use this tool to search for activities in a specific location using the TripAdvisor API.
    The function will return a JSON string containing a list of activities with their details.
    """

    headers = {"accept": "application/json"}

    # Premier appel : rechercher des locations
    search_url = f"{TRIPADVISOR_BASE_URL}/location/search"
    search_params = {
        "searchQuery": input.search_query,
        "category": category,
        "language": "en",
        "key": tripadvisor_key,
    }
    try:
        search_resp = requests.get(
            search_url, headers=headers, params=search_params, timeout=30
        )
        search_resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during search API call: {str(e)}")
        return json.dumps({"error": f"Error during search API call: {str(e)}"})

    search_data = search_resp.json()
    if "error" in search_data and search_data["error"]:
        return json.dumps({"error": search_data["error"]})

    activities_list: List[Activity] = []
    # Boucler sur les résultats de recherche (jusqu'à input.limit)
    for result in search_data.get("data", []):
        location_id = result.get("location_id")
        if not location_id:
            continue

        # Second appel : récupérer la photo
        photos_url = f"{TRIPADVISOR_BASE_URL}/location/{location_id}/photos"
        photos_params = {"language": "en", "key": tripadvisor_key}
        try:
            photos_resp = requests.get(
                photos_url, headers=headers, params=photos_params, timeout=30
            )
            photos_resp.raise_for_status()
            photos_data = photos_resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during photos API call for location {location_id}: {str(e)}")
            photos_data = {}

        photo_url = None
        if (
            "data" in photos_data
            and isinstance(photos_data["data"], list)
            and photos_data["data"]
        ):
            # Chercher la première photo disponible
            first_photo = photos_data["data"][0]
            if "images" in first_photo and "original" in first_photo["images"]:
                photo_url = first_photo["images"]["original"].get("url")

        # Troisième appel : obtenir les détails de la location
        details_url = f"{TRIPADVISOR_BASE_URL}/location/{location_id}/details"
        details_params = {
            "language": "en",
            "currency": "EUR",  # ou "EUR" selon vos besoins
            "key": tripadvisor_key,
        }
        try:
            details_resp = requests.get(
                details_url, headers=headers, params=details_params, timeout=30
            )
            details_resp.raise_for_status()
            details_data = details_resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during details API call for location {location_id}: {str(e)}")
            details_data = {}

        # Préparer les données pour l'objet Activity
        title = details_data.get("name") or result.get("name")
        description = details_data.get("description", "")
        rating = details_data.get("rating")
        image = photo_url
        link = details_data.get("web_url")

        activity = Activity(
            title=title,
            description=description,
            rating=str(rating) if rating is not None else "N/A",
            vibe="N/A",
            image=image,
            link=link,
        )
        activities_list.append(activity)

    # Retourner la liste d'activités convertie en JSON (string)
    return json.dumps([activity.dict() for activity in activities_list])
