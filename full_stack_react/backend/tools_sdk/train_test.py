import os
import requests


def search_places(query: str):
    # Récupération de la clé API SNCF depuis la variable d'environnement
    api_key = os.getenv("SNCF_API_KEY")
    if not api_key:
        print("Erreur : la variable d'environnement SNCF_API_KEY n'est pas définie.")
        return None

    # URL de l'endpoint de recherche de lieux
    url = "https://api.sncf.com/v1/coverage/sncf/places"

    # Paramètres de la requête
    params = {"q": query}

    # En-tête d'authentification
    headers = {"Authorization": api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel API : {e}")
        return None

    # Conversion de la réponse en JSON
    return response.json()


if __name__ == "__main__":
    query = "Paris"
    result = search_places(query)
    if result:
        # Affiche le résultat au format JSON
        import json

        print(json.dumps(result, indent=4, ensure_ascii=False))
