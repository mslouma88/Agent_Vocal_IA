import datetime
import streamlit as st
import speech_recognition as sr
import openai
import random
from gtts import gTTS
from textblob import TextBlob
import io
import os

# Vérifier si on est sur Streamlit Cloud
if os.environ.get('STREAMLIT_SERVER_HEADLESS'):
    # Si on est sur Streamlit Cloud, désactiver pygame ou toute dépendance audio liée à SDL
    st.write("Exécution sur Streamlit Cloud - Pygame désactivé")
    pygame_enabled = False
else:
    # Si on est local, on peut utiliser pygame
    import pygame
    pygame.init()
    pygame.mixer.init()
    pygame_enabled = True
    st.write("Exécution locale - Pygame activé")

# Set page config with an icon
#st.set_page_config(page_title="Agent Vocal", page_icon="images/icon.png")

# Configuration de l'API OpenAI
openai.api_key = st.secrets["openai"]["api_key"]

# Fonction de reconnaissance vocale
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
    # Créer un objet gTTS
    tts = gTTS(text=text, lang='fr')
    
    # Créer un tampon en mémoire
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    if pygame_enabled:
        try:
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            st.error(f"Erreur lors de la lecture audio : {e}")
        finally:
            fp.close()
    else:
        st.audio(fp, format="audio/mp3")

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
st.sidebar.image("images/logo3.png", width=280)

# Initialiser le contexte de la conversation
if 'context' not in st.session_state:
    st.session_state.context = []

# Zone de conversation
conversation = st.empty()

def update_conversation():
    conversation.text_area("📜 **Historique de la conversation**", 
                           value="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.context]),
                           height=300)

# Onglets pour choisir entre chat vocal et écrit
tab1, tab2 = st.tabs(["💬 Chat Écrit", "🎙️ Chat Vocal"])

with tab1:
    user_input = st.text_input("Écrivez votre message ici")
    read_aloud = st.checkbox("🔊Lire la réponse à voix haute")

    if st.button("Envoyer"):
        if user_input:
            sentiment = analyze_sentiment(user_input)
            st.write(f"**Sentiment détecté** : {sentiment}")

            response = ask_openai(user_input, st.session_state.context)
            st.write(f"**Agent** : {response}")

            st.session_state.context.append({"role": "user", "content": user_input})
            st.session_state.context.append({"role": "assistant", "content": response})

            update_conversation()

            if read_aloud:
                speak_text(response)

with tab2:
    if st.button("🎙️ Parler à l'agent"):
        with st.spinner("🔊 Écoute en cours..."):
            recognized_text = recognize_speech()
            st.write(f"**Vous avez dit** : {recognized_text}")

            if "arrêter" in recognized_text.lower():
                st.warning("Arrêt de l'agent vocal.")
                speak_text("Au revoir ! J'espère vous revoir bientôt.")
            else:
                sentiment = analyze_sentiment(recognized_text)
                st.write(f"**Sentiment détecté** : {sentiment}")

                response = ask_openai(recognized_text, st.session_state.context)
                st.write(f"**Agent** : {response}")

                st.session_state.context.append({"role": "user", "content": recognized_text})
                st.session_state.context.append({"role": "assistant", "content": response})

                update_conversation()
                speak_text(response)

# Effacer l'historique
if st.button("🗑️ Effacer l'historique"):
    st.session_state.context = []
    update_conversation()
    st.success("Historique effacé !")

# Afficher des statistiques
st.sidebar.title("📊 Statistiques")
total_messages = len(st.session_state.context) - 1
average_length = sum(len(msg['content']) for msg in st.session_state.context if msg['role'] != "system") / total_messages if total_messages > 0 else 0
st.sidebar.write(f"**Nombre de messages** : {total_messages}")
st.sidebar.write(f"**Longueur moyenne des réponses** : {average_length:.0f} caractères")

# Ajouter un droit d'auteur
now = datetime.datetime.now()
st.sidebar.write(f"© {now.year} Salam & Nesrine")