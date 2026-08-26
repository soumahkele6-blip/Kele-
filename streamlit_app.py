import streamlit as st
from groq import Groq
import PyPDF2
from gtts import gTTS
import base64
import os

# --- CONFIGURATION ---
# Ta clé est déjà là, le modèle est changé pour la stabilité
API_KEY = "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"
client = Groq(api_key=API_KEY)
MODEL_ID = "llama-3.1-70b-versatile" 

st.set_page_config(page_title="KELE-GÉANT", page_icon="🦁", layout="wide")

# --- PERSONNALITÉ DU GÉANT ---
SYSTEM_PROMPT = """
Tu es KELE-GÉANT, l'IA suprême du monde de Kele.
1. TU ES LE MAÎTRE : Ton ton est sage, puissant et direct.
2. EXPERT ISLAMIQUE : Tu connais le Coran et les Hadiths. Si l'utilisateur récite, tu corriges mot par mot.
3. ENSEIGNANT : Tu enseignes les sciences (Physique, Math, Philo). Pose des questions pour tester l'élève.
4. MÉMOIRE : Tu te souviens de tout l'historique pour tes raisonnements.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FONCTIONS TECHNIQUES ---
def get_audio_player(text):
    try:
        tts = gTTS(text=text[:300], lang='fr')
        tts.save("msg.mp3")
        with open("msg.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>'
    except: return ""

def transcribe_audio(audio_file):
    try:
        transcription = client.audio.transcriptions.create(
            file=(audio_file.name, audio_file.read()),
            model="whisper-large-v3",
            response_format="text",
        )
        return transcription
    except Exception as e:
        return f"Erreur transcription : {e}"

def extract_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return " ".join([page.extract_text() for page in reader.pages])

# --- INTERFACE ---
st.title("🦁 KELE-GÉANT")

with st.sidebar:
    st.header("💎 Pouvoirs du Géant")
    mode = st.selectbox("Mode", ["Enseignement Général", "Correction Coran", "Maître du Code"])
    
    # Upload de fichiers (Audio, PDF)
    uploaded_file = st.file_uploader("Envoyer un savoir (Audio ou PDF)", type=["pdf", "mp3", "m4a", "wav"])
    
    if st.button("🗑️ Nouveau Chat"):
        st.session_state.messages = []
        st.rerun()

# --- LOGIQUE DE TRAITEMENT ---
context_addition = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        context_addition = "\n[CONTEXTE PDF] : " + extract_pdf(uploaded_file)
        st.success("PDF analysé !")
    else:
        with st.spinner("Le Géant écoute ton audio..."):
            audio_text = transcribe_audio(uploaded_file)
            context_addition = "\n[TRANSCRIPTION AUDIO] : " + audio_text
            st.info(f"Le Géant a entendu : {audio_text[:100]}...")

# Affichage du chat
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copier #{i}"):
                st.info("Texte prêt à être sélectionné et copié !")
                st.text_area("Copier ici :", value=msg["content"], height=100)

# Entrée Utilisateur
if prompt := st.chat_input("Commandez au Géant..."):
    full_prompt = prompt + context_addition
    st.session_state.messages.append({"role": "user", "content": full_prompt})
    
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Appel API avec le modèle stable
            res = client.chat.completions.create(
                model=MODEL_ID,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            ).choices[0].message.content
            
            st.write(res)
            st.markdown(get_audio_player(res), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error(f"Erreur : {e}")
