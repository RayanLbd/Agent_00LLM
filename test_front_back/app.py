# app.py
import streamlit as st
from backend import process_user_input

# Configuration de la page
st.set_page_config(page_title="Agent organisateur de voyage", page_icon="✈️", layout="wide")

# CSS modernisé pour l'interface
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        /* Global */
        body {
            background: #f0f2f6;
            font-family: 'Roboto', sans-serif;
        }
        h1 {
            font-weight: 500;
            margin-top: 20px;
        }
        /* Conteneur de la discussion */
        .chat-container {
            max-width: 700px;
            margin: 20px auto;
            padding: 20px 15px;
            padding-bottom: 140px; /* pour laisser de l'espace à la zone d'entrée */
        }
        /* Boîtes de messages */
        .message-box {
            display: flex;
            margin-bottom: 16px;
        }
        .message-box.user {
            justify-content: flex-end;
        }
        .message-box.bot {
            justify-content: flex-start;
        }
        .chat-message {
            padding: 12px 16px;
            border-radius: 20px;
            max-width: 80%;
            line-height: 1.5;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            font-size: 15px;
        }
        .user .chat-message {
            background-color: #a0c4ff;
            color: #fff;
        }
        .bot .chat-message {
            background-color: #e2e8f0;
            color: #333;
        }
        /* Zone d'entrée fixée en bas avec largeur fixe */
        .input-container {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 400px;  /* largeur fixe pour la zone d'entrée */
            background-color: #fff;
            border-radius: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 1000;
            overflow: hidden;
            padding: 0;
        }
        /* Masquer l'étiquette par défaut du champ de saisie */
        .stTextInput label {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 style='text-align: center; color: #333;'>✈️ Agent organisateur de voyage</h1>", unsafe_allow_html=True)

# Stockage des messages en session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique des messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role = message["role"]
    text = message["text"]
    css_class = "user" if role == "user" else "bot"
    st.markdown(f"""
        <div class="message-box {css_class}">
            <div class="chat-message">{text}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Zone d'entrée fixée en bas avec formulaire utilisant des colonnes pour aligner horizontalement
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    cols = st.columns([9, 1])
    with cols[0]:
        user_input = st.text_input("", placeholder="Votre question...", key="input")
    with cols[1]:
        submitted = st.form_submit_button("→")
    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "text": user_input})
        with st.spinner("Génération de la réponse..."):
            response = process_user_input(user_input)
        st.session_state.messages.append({"role": "bot", "text": response})
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
