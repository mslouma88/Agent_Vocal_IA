import streamlit as st
import speech_recognition as sr
import openai
import random
from gtts import gTTS
import pygame
from textblob import TextBlob
import io
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

#st.write("Test d'affichage")
# Configuration de l'API OpenAI
openai.api_key = st.secrets["openai"]["api_key"]

# Initialisation de pygame pour la lecture audio
pygame.mixer.init()

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
    # Créer un objet gTTS
    tts = gTTS(text=text, lang='fr')
    
    # Créer un tampon en mémoire
    fp = io.BytesIO()
    
    # Sauvegarder l'audio dans le tampon en mémoire
    tts.write_to_fp(fp)
    
    # Rembobiner le tampon au début
    fp.seek(0)
    
    try:
        # Charger l'audio depuis le tampon en mémoire
        pygame.mixer.music.load(fp)
        
        # Jouer l'audio
        pygame.mixer.music.play()
        
        # Attendre que la lecture soit terminée
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    except Exception as e:
        st.error(f"Erreur lors de la lecture audio : {e}")
    
    finally:
        # Nettoyer le tampon en mémoire
        fp.close()

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
st.title("🤖 Agent Vocal et Textuel Futuriste v2.1")

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
    # Zone de saisie de texte
    user_input = st.text_input("Écrivez votre message ici")
    
    # Déplacer la case à cocher avant le bouton d'envoi
    read_aloud = st.checkbox("Lire la réponse à voix haute")

    # Interroger ChatGPT
    response = ask_openai(user_input, st.session_state.context)
    st.write(f"**Agent** : {response}")

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

# Bouton pour effacer l'historique
if st.button("🗑️ Effacer l'historique"):
    st.session_state.context = []
    update_conversation()
    st.success("Historique effacé !")

# Afficher des statistiques
st.sidebar.title("📊 Statistiques")
st.sidebar.write(f"Nombre de messages : {len(st.session_state.context)}")
st.sidebar.write(f"Longueur moyenne des réponses : {sum(len(msg['content']) for msg in st.session_state.context) // len(st.session_state.context) if st.session_state.context else 0} caractères")

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
