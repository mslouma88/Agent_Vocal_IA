<!--![Logo de mon projet](images/IA.png)-->

<img src="images/IA.png" alt="Logo de mon projet" >



# 💬 Agent Vocal avec ChatGPT

Ce projet consiste en un agent vocal interactif qui utilise le modèle de langage GPT (ChatGPT) pour répondre aux questions des utilisateurs. L'application est dotée d'une interface graphique créée avec **Streamlit** et comprend la reconnaissance vocale, l'interaction avec le modèle GPT 3.5, et la synthèse vocale.

## 📋 Description

L'agent vocal capture la voix de l'utilisateur, la convertit en texte à l'aide de la reconnaissance vocale, puis envoie ce texte à l'API OpenAI pour obtenir une réponse. La réponse est affichée dans l'interface graphique et restituée par une synthèse vocale, permettant une interaction naturelle et fluide.

### Fonctionnalités Principales
- **Reconnaissance Vocale** : Capture et transcrit la parole de l'utilisateur en texte.
- **Interaction avec ChatGPT** : Envoie le texte transcrit à ChatGPT et récupère une réponse.
- **Synthèse Vocale** : Convertit la réponse textuelle en audio pour une restitution vocale.
- **Interface Graphique Moderne** : Utilisation de Streamlit pour une interface utilisateur avec un design futuriste.

## 🚀 Démonstration en Ligne

L'application est hébergée sur **Streamlit Cloud** et accessible à l'URL suivante : [Lien vers l'Application](#)  
*(Remplacez `#` par l'URL générée après le déploiement de votre application sur Streamlit Cloud)*

## 🛠️ Installation et Exécution Locale

Suivez les étapes ci-dessous pour exécuter l'application localement sur votre machine.

### Prérequis

Assurez-vous d'avoir les éléments suivants installés :
- [Python 3.7+](https://www.python.org/downloads/)
- `pip` (gestionnaire de paquets pour Python)
- Streamlit
- OpenAI API
- SpeechRecognition
- gTTS (Google Text-to-Speech)
- Pygame
- TextBlob

### Installation des Dépendances

1. Clonez le dépôt GitHub sur votre machine locale :

    ```bash
    git clone https://github.com/mslouma88/Agent_Vocal_IA
    ```

2. Accédez au répertoire du projet :

    ```bash
    cd Agent_Vocal_IA
    ```

3. Créez un environnement virtuel (recommandé) et activez-le :

    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows : env\Scripts\activate
    ```

4. Installez les dépendances requises à partir du fichier `requirements.txt` :

    ```bash
    pip install -r requirements.txt
    ```

### Configuration de la Clé API OpenAI

Pour interagir avec ChatGPT, vous devez configurer votre clé API OpenAI :

1. Créez un fichier `.streamlit/secrets.toml` à la racine du projet.
2. Ajoutez-y les informations suivantes :

    ```toml
    [openai]
    api_key = "VOTRE_CLE_API_OPENAI"
    ```

Remplacez `"VOTRE_CLE_API_OPENAI"` par votre clé API personnelle. Si vous n'avez pas encore de clé, inscrivez-vous sur [OpenAI](https://beta.openai.com/signup/) pour en obtenir une.

### Exécution de l'Application

Lancez l'application Streamlit en exécutant la commande suivante :

```bash
streamlit run agent_vocal_streamlit.py
```

Le navigateur par défaut s'ouvrira avec l'application. Vous pouvez maintenant interagir avec l'agent vocal en cliquant sur le bouton "Parler".

🌐 Déploiement sur Streamlit Cloud
Pour déployer cette application sur Streamlit Cloud :

1. Créez un dépôt GitHub et ajoutez-y le code source du projet.

2. Créez un fichier requirements.txt avec les bibliothèques suivantes :

    ```text
    streamlit==1.39.0
    SpeechRecognition==3.10.4
    openai==0.28.0
    pyttsx3==2.98
    pygame==2.6.1
    gTTS==2.5.3
    textblob==0.18.0.post0
    #pipwin==0.5.2
    PyAudio==0.2.14
    ```

3. Connectez-vous à [Streamlit Cloud](https://streamlit.io/cloud).

4. Cliquez sur "New App" et sélectionnez votre dépôt GitHub.

5. Choisissez le fichier `agent_vocal.py` comme script principal.

6. Cliquez sur Deploy pour lancer le déploiement.

Une fois déployée, l'application sera accessible via une URL publique que vous pourrez partager avec vos utilisateurs.

📚 Documentation

[Documentation OpenAI](https://platform.openai.com/docs/overview)

[Documentation Streamlit](https://docs.streamlit.io)

[Streamlit Cloud Guide](https://docs.streamlit.io/streamlit-cloud)

📝 Licence
Ce projet est sous [licence MIT](LICENCE). Vous êtes libre de l'utiliser, de le modifier et de le distribuer sous les conditions de la licence.

👤 Auteur(e)s

- **Salam MEJRI** 🧑‍💻 - [@github](https://github.com/mslouma88) - Développeur et concepteur principal de l'agent vocal.
- **Nesrine BENAMOR** 🧑‍💻 - [@github](https://github.com/Nes890) - Développeur et concepteur principal de l'agent vocal.

Pour toute question ou suggestion, n'hésitez pas à nous contacter.


Merci d'avoir utilisé cet agent vocal futuriste ! 🚀