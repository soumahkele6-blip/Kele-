import streamlit as st
from groq import Groq
import PyPDF2
from gtts import gTTS
import base64
import os

# --- CONFIGURATION ET CLÉ API ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="KELE-GÉANT", page_icon="🦁")

# --- PERSONNALITÉ DU GÉANT ---
SYSTEM_PROMPT = """
Tu es KELE-GÉANT, l'IA suprême. 
- Expert en Islam (Coran/Hadiths), Sciences, et Codage.
- Tu corriges la récitation du Coran et tu testes la mémoire de l'élève.
- Ton raisonnement est au-dessus des autres. Tu es un Maître.
"""

# Initialisation mémoire
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FONCTIONS ---
def get_audio_player(text):
    try:
        tts = gTTS(text=text[:250], lang='fr')
        tts.save("msg.mp3")
        with open("msg.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>'
    except:
        return ""

# --- INTERFACE ---
st.title("🦁 KELE-GÉANT")

# Barre latérale
with st.sidebar:
    st.header("⚙️ Menu")
    mode = st.selectbox("Mode", ["Enseignement", "Correction Coran", "Code"])
    if st.button("🗑️ Nouveau Chat"):
        st.session_state.messages = []
        st.rerun()

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrée Utilisateur
if prompt := st.chat_input("Parlez au Géant..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Appel API Groq
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            )
            response = chat_completion.choices[0].message.content
            st.write(response)
            
            # Option Voix
            st.markdown(get_audio_player(response), unsafe_allow_html=True)
            
            # Ajouter à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Erreur : {e}")

# Bouton pour copier la dernière réponse (simplifié)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    if st.button("📋 Préparer la copie"):
        st.text_area("Copie ce texte :", value=st.session_state.messages[-1]["content"])
