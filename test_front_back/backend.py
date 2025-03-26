# backend.py
import time

def process_user_input(user_input):
    """
    Fonction simulant le traitement de la requête utilisateur
    Remplacez cela par un appel au graphe LangGraph dans la version finale
    """
    dummy_responses = [
        "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        "Je cherche des informations, un instant...",
        "Voici ce que j'ai trouvé : ...",
        "Je n'ai pas bien compris, pouvez-vous reformuler ?"
    ]
    time.sleep(3)  # Simule un délai de réponse
    return dummy_responses[len(user_input) % len(dummy_responses)]
