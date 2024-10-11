import datetime
import streamlit as st
import speech_recognition as sr
import openai
from gtts import gTTS
from textblob import TextBlob
import io
import base64
import time
import fitz  # PyMuPDF pour la gestion des PDF
import pandas as pd
import os
import tempfile
import random

# Configuration de la page
st.set_page_config(page_title="Agent Vocal", page_icon="images/icon.png")

# Configuration de l'API OpenAI
openai.api_key = st.secrets["openai"]["api_key"]

# Fonction de reconnaissance vocale améliorée
def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        st.write("🎧 **Écoute active...**")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
        return text
    except sr.UnknownValueError:
        return "Je n'ai pas compris. Pouvez-vous répéter ?"
    except sr.RequestError:
        return "Erreur de connexion au service de reconnaissance vocale."

# Fonction pour interroger l'API OpenAI avec contexte
def ask_openai(prompt, context):
    messages = [{"role": "system", "content": "Vous êtes un assistant vocal futuriste, intelligent et serviable."}]
    messages.extend(context)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Fonction pour la synthèse vocale avec gTTS
def speak_text(text):
    tts = gTTS(text=text, lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Encodage de l'audio en base64
    audio_base64 = base64.b64encode(fp.read()).decode()
    
    # Création d'un élément audio HTML
    audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
    
    # Affichage de l'élément audio
    st.markdown(audio_html, unsafe_allow_html=True)

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

# Interface Streamlit
st.title("🤖 Agent Vocal & Textuel v1.0")

# Ajouter un logo à la barre latérale
st.sidebar.image("images/logo3.png", width=280)

# Définition des thèmes (code inchangé)

themes = {
    "Dark Mode": {
        "background-color": "#121212",
        "color": "#FFFFFF",
        "button-background-color": "#FFFFFF",
        "button-color": "#121212",
        "button-box-shadow": "0 0 10px #FFFFFF",
        "sidebar-background-color": "#222222",
        "sidebar-color": "#FFFFFF",
        "sidebar-box-shadow": "0 0 10px #FFFFFF",
    },
    "Razer Chroma": {
        "background-color": "#222222",
        "color": "#00FF00",
        "button-background-color": "#00FF00",
        "button-color": "#000000",
        "button-box-shadow": "0 0 10px #00FF00",
        "sidebar-background-color": "#111111",
        "sidebar-color": "#00FF00",
        "sidebar-box-shadow": "0 0 10px #00FF00",
    },
    "Ocean Blue": {
        "background-color": "rgba(0, 100, 148, 0.9)",
        "color": "#FFFFFF",
        "button-background-color": "#00BFFF",
        "button-color": "#000033",
        "button-box-shadow": "0 0 10px #00BFFF",
        "sidebar-background-color": "rgba(0, 50, 74, 0.9)",
        "sidebar-color": "#FFFFFF",
        "sidebar-box-shadow": "0 0 10px #00BFFF",
    },
    "Neon Sunset": {
        "background-color": "#2C3E50",  # Fond plus sombre pour un meilleur contraste
        "color": "#FFFFFF",  # Texte blanc pour une meilleure lisibilité
        "button-background-color": "#E74C3C",  # Rouge vif pour les boutons
        "button-color": "#FFFFFF",  # Texte blanc sur les boutons
        "button-box-shadow": "0 0 10px #E74C3C",
        "sidebar-background-color": "#34495E",  # Sidebar légèrement plus claire que le fond
        "sidebar-color": "#FFFFFF",  # Texte blanc dans la sidebar
        "sidebar-box-shadow": "0 0 10px #E74C3C",
    },
    "Cyberpunk": {
        "background-color": "#0D0221",
        "color": "#F806CC",
        "button-background-color": "#F806CC",
        "button-color": "#0D0221",
        "button-box-shadow": "0 0 10px #F806CC",
        "sidebar-background-color": "#260650",
        "sidebar-color": "#01FFC3",
        "sidebar-box-shadow": "0 0 10px #01FFC3",
    },
    "Matrix": {
        "background-color": "#000000",
        "color": "#00FF41",
        "button-background-color": "#003B00",
        "button-color": "#00FF41",
        "button-box-shadow": "0 0 10px #00FF41",
        "sidebar-background-color": "#001F00",
        "sidebar-color": "#00FF41",
        "sidebar-box-shadow": "0 0 10px #00FF41",
    },
    "Midnight Galaxy": {
        "background-color": "#0F0F3D",
        "color": "#E6E6FA",
        "button-background-color": "#4B0082",
        "button-color": "#E6E6FA",
        "button-box-shadow": "0 0 10px #9370DB",
        "sidebar-background-color": "#191970",
        "sidebar-color": "#E6E6FA",
        "sidebar-box-shadow": "0 0 10px #9370DB",
    },
    "Retro Wave": {
        "background-color": "#2B0F54",
        "color": "#FF00FF",
        "button-background-color": "#FF00FF",
        "button-color": "#2B0F54",
        "button-box-shadow": "0 0 10px #FF00FF",
        "sidebar-background-color": "#120458",
        "sidebar-color": "#00FFFF",
        "sidebar-box-shadow": "0 0 10px #00FFFF",
    },
    "Forest Mist": {
        "background-color": "#2C5F2D",
        "color": "#D0F0C0",
        "button-background-color": "#97BC62",
        "button-color": "#2C5F2D",
        "button-box-shadow": "0 0 10px #97BC62",
        "sidebar-background-color": "#1E441E",
        "sidebar-color": "#D0F0C0",
        "sidebar-box-shadow": "0 0 10px #97BC62",
    },
}

# Set the initial theme
theme = "Razer Chroma"

# Define a function to update the theme
def update_theme(theme):
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {themes[theme]['background-color']};
            color: {themes[theme]['color']};
            font-family: 'Roboto', sans-serif;
        }}
        .stButton>button {{
            background-color: {themes[theme]['button-background-color']};
            color: {themes[theme]['button-color']};
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: {themes[theme]['button-box-shadow']};
        }}
        .stButton>button:hover {{
            background-color: {themes[theme]['button-color']};
            color: {themes[theme]['button-background-color']};
            border: 2px solid {themes[theme]['button-background-color']};
            box-shadow: 0 0 20px {themes[theme]['button-background-color']};
        }}
        .stSidebar {{
            background-color: {themes[theme]['sidebar-background-color']};
            color: {themes[theme]['sidebar-color']};
            box-shadow: {themes[theme]['sidebar-box-shadow']};
        }}
        .stTextInput>div>div>input {{
            background-color: {themes[theme]['sidebar-background-color']};
            color: {themes[theme]['sidebar-color']};
            border-color: {themes[theme]['sidebar-color']};
        }}
        .stSelectbox>div>div>select {{
            background-color: {themes[theme]['sidebar-background-color']};
            color: {themes[theme]['sidebar-color']};
            border-color: {themes[theme]['sidebar-color']};
        }}
        </style>
    """, unsafe_allow_html=True)

# Add a theme selection dropdown menu to the sidebar
theme = st.sidebar.selectbox("🎨 Choisissez un thème", list(themes.keys()), index=0, on_change=update_theme, args=(theme,))

# Update the theme
update_theme(theme)

# Initialiser le contexte de la conversation
if 'context' not in st.session_state:
    st.session_state.context = []

# Zone de conversation
conversation = st.empty()

def update_conversation():
    conversation.text_area("📜 **Historique de la conversation**", 
                           value="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.context]),
                           height=300)

# Fonction pour résumer le texte en français
def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text in French."},
            {"role": "user", "content": f"Veuillez résumer le texte suivant en français : {text}"}
        ]
    )
    return response.choices[0].message.content

# Fonction pour lire le contenu d'un fichier PDF
def read_pdf(file):
    pdf_reader = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_reader)):
        page = pdf_reader.load_page(page_num)
        text += page.get_text("text")  # Extraire le texte de chaque page
    pdf_reader.close()
    return text

def analyser_donnees(df):
    # Convertir le DataFrame en texte
    data_text = df.head().to_string()
    prompt = f"Analyse les données suivantes et fournis des insights pertinents :\n\n{data_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes un analyste de données."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.3,
    )
    analyse = response.choices[0].message['content'].strip()
    return analyse

# Onglets pour choisir entre chat vocal et écrit
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat Écrit", "🎙️ Chat Vocal", "💬 Chat Écrit v2.0", "📜 Résumeur de Fichiers", "📶 Analyse de Données Structurées" ])

with tab1:
   # Zone de saisie de texte
    user_input = st.text_input("Écrivez votre message ici")
    
    # Déplacer la case à cocher avant le bouton d'envoi
    read_aloud = st.checkbox("🔊Lire la réponse à voix haute")

    if st.button("Envoyer"):
        if user_input:
            # Analyser le sentiment
            sentiment = analyze_sentiment(user_input)
            st.write(f"**Sentiment détecté** : {sentiment}")

            # Interroger ChatGPT
            response = ask_openai(user_input, st.session_state.context)
            st.write(f"**Agent** : {response}")

            # Ajouter au contexte
            st.session_state.context.append({"role": "user", "content": user_input})
            st.session_state.context.append({"role": "assistant", "content": response})

            # Mettre à jour la zone de conversation
            update_conversation()

            # Lire la réponse à voix haute si la case est cochée
            if read_aloud:
                speak_text(response)

with tab2:
    # Bouton pour démarrer la reconnaissance vocale
    if st.button("🎙️ Parler à l'agent"):
        with st.spinner("🔊 Écoute en cours..."):
            recognized_text = recognize_speech()
            st.write(f"**Vous avez dit** : {recognized_text}")

            if "arrêter" in recognized_text.lower():
                st.warning("Arrêt de l'agent vocal.")
                speak_text("Au revoir ! J'espère vous revoir bientôt.")
            else:
                # Analyser le sentiment
                sentiment = analyze_sentiment(recognized_text)
                st.write(f"**Sentiment détecté** : {sentiment}")

                # Interroger ChatGPT
                response = ask_openai(recognized_text, st.session_state.context)
                st.write(f"**Agent** : {response}")

                # Ajouter au contexte
                st.session_state.context.append({"role": "user", "content": recognized_text})
                st.session_state.context.append({"role": "assistant", "content": response})

                # Mettre à jour la zone de conversation
                update_conversation()

                # Synthèse vocale de la réponse
                speak_text(response)

with tab3:

    # Contexte initial pour personnaliser le chatbot
    contexte_initial = [
        {"role": "system", "content": "Vous êtes un assistant virtuel intelligent multilangues spécialisé dans tous les domaines. Vous connaissez tout et vous pouvez donner des conseils."}
    ]


    # Initialiser le contexte de la conversation si ce n'est pas déjà fait
    if "messages" not in st.session_state:
        st.session_state.messages = contexte_initial

    # Afficher les messages de l'historique
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Zone de saisie de texte
    prompt = st.chat_input("Écrivez votre message ici")

    # Case à cocher pour la lecture à voix haute
    read_aloud = st.checkbox("🔊 Lire la réponse à voix haute")

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

            # Simuler un flux de réponse avec un délai en millisecondes
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Ajouter un curseur clignotant pour simuler la frappe
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # Ajouter la réponse de l'assistant à l'historique
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Mettre à jour la zone de conversation
        update_conversation()

        # Lire la réponse à voix haute si la case est cochée
        if read_aloud:
            speak_text(full_response)
with tab4:
        st.write("Téléchargez vos fichiers texte ou PDF ci-dessous pour obtenir des résumés en français.")

        # Ajout d'un bouton pour parcourir les fichiers (TXT et PDF)
        uploaded_files = st.file_uploader("Choisissez des fichiers texte ou PDF", type=["txt", "pdf"], accept_multiple_files=True)

        # Bouton pour générer les résumés
        if st.button("Générer des résumés"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    # Vérification du type de fichier (TXT ou PDF)
                    if uploaded_file.name.endswith(".txt"):
                        # Lire le contenu d'un fichier texte
                        file_content = uploaded_file.read().decode("utf-8")
                        st.write(f"Résumé du fichier texte : {uploaded_file.name}")
                    elif uploaded_file.name.endswith(".pdf"):
                        # Lire le contenu d'un fichier PDF
                        file_content = read_pdf(uploaded_file)
                        st.write(f"Résumé du fichier PDF : {uploaded_file.name}")
                    else:
                        st.error("Format de fichier non supporté.")

                    # Appel de la fonction de résumé (en français)
                    summary = summarize_text(file_content)

                    # Afficher le résumé
                    st.markdown(f"<div style='background-color: #001212; padding: 10px; border-radius: 5px;'>{summary}</div>", unsafe_allow_html=True)
            else:
                st.error("Veuillez télécharger au moins un fichier pour générer un résumé.")
with tab5:
        st.write("Téléchargez vos fichiers texte ou PDF ci-dessous pour obtenir")
        fichier = st.file_uploader("Téléchargez un fichier CSV ou Excel", type=["csv", "xlsx"])
        
        if fichier is not None:
            try:
                if fichier.type == "text/csv":
                    df = pd.read_csv(fichier)
                else:
                    df = pd.read_excel(fichier)
                st.subheader("Aperçu des Données")
                st.dataframe(df.head())
                
                if st.button("Analyser les Données"):
                    with st.spinner("Analyse en cours..."):
                        analyse = analyser_donnees(df)
                    st.success("Analyse terminée !")
                    st.write("**Insights :**")
                    st.write(analyse)
            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {e}")
        else:
            st.info("Veuillez télécharger un fichier CSV ou Excel pour commencer.")

# Bouton pour effacer l'historique
if st.button("🗑️ Effacer l'historique"):
    st.session_state.context = []
    update_conversation()
    st.success("Historique effacé !")

# Afficher des statistiques
st.sidebar.title("📊 Statistiques")
total_messages = len(st.session_state.context) - 1  # Exclure le message système
average_length = sum(len(msg['content']) for msg in st.session_state.context if msg['role'] != "system") / total_messages if total_messages > 0 else 0
st.sidebar.write(f"**Nombre de messages** : {total_messages}")
st.sidebar.write(f"**Longueur moyenne des réponses** : {average_length:.0f} caractères")

# Easter egg
if st.sidebar.button("🎁 Surprise !"):
    jokes = [
        "Pourquoi les robots ne prennent-ils jamais de vacances ? Parce qu'ils ont déjà trop de vis !",
        "Comment s'appelle un robot qui fait toujours la même chose ? Un automate.",
        "Que dit un robot quand il tombe en panne ? 'J'ai un bug-out-bag !'",
    ]
    joke = random.choice(jokes)
    st.sidebar.write(joke)
    speak_text(joke)

# Mode nuit
if st.sidebar.checkbox("🌙 Mode nuit"):
    st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Afficher la date et l'heure actuelles
now = datetime.datetime.now()
st.sidebar.write(f"Date : {now.strftime('%Y-%m-%d')}",f"| Heure : {now.strftime('%H:%M')}")

# Ajouter un droit d'auteur
st.sidebar.write(f"© {now.year} Salam & Nesrine")