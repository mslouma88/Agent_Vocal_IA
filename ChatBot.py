import streamlit as st
import openai
from textblob import TextBlob
import time

# Configuration de la page
st.set_page_config(page_title="Assistant Virtuel Intelligent", page_icon="🤖")

# Configuration de l'API OpenAI
openai.api_key = st.secrets["openai"]["api_key"]

# Fonction pour analyser le sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.1:
        return "positif"
    elif sentiment < -0.1:
        return "négatif"
    else:
        return "neutre"

# Fonction pour interroger l'API OpenAI
def ask_openai(prompt, context):
    messages = [{"role": "system", "content": "Vous êtes un assistant virtuel intelligent multilangue spécialisé dans tous les domaines."}]
    messages.extend(context)
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Erreur lors de la requête à OpenAI : {str(e)}")
        return "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer."

# Interface Streamlit
st.title("🤖 Assistant Virtuel Intelligent")

# Initialiser le contexte de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie de texte
prompt = st.chat_input("Écrivez votre message ici")

if prompt:
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Afficher le message de l'utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)

    # Analyser le sentiment
    sentiment = analyze_sentiment(prompt)
    st.write(f"**Sentiment détecté** : {sentiment}")

    # Afficher la réponse de l'assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = ask_openai(prompt, st.session_state.messages)

        # Simuler un flux de réponse
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Ajouter la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Bouton pour effacer l'historique
if st.button("🗑️ Effacer l'historique"):
    st.session_state.messages = []
    st.success("Historique effacé !")

# Afficher des statistiques
st.sidebar.title("📊 Statistiques")
total_messages = len(st.session_state.messages)
st.sidebar.write(f"**Nombre de messages** : {total_messages}")

# Afficher la date et l'heure actuelles
now = time.strftime("%Y-%m-%d %H:%M")
st.sidebar.write(f"Date et heure : {now}")

# Ajouter un droit d'auteur
st.sidebar.write("© 2023 Assistant Virtuel Intelligent")