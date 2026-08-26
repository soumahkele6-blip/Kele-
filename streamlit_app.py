import streamlit as st
from groq import Groq
import PyPDF2
from gtts import gTTS
import base64
import os

# --- CONFIGURATION ---
# Utilisation du modèle le plus stable de Groq
API_KEY = "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"
client = Groq(api_key=API_KEY)
# Si ce modèle échoue, remplace juste le nom ci-dessous par 'mixtral-8x7b-32768'
MODEL_ACTUEL = "llama3-70b-8192" 

st.set_page_config(page_title="KELE-GÉANT", page_icon="🦁", layout="wide")

# --- PERSONNALITÉ DU GÉANT ---
SYSTEM_PROMPT = """
Tu es KELE-GÉANT, l'IA suprême.
- Tu es un Maître absolu en Islam, Sciences et Codage.
- Tu corriges les récitations du Coran (Tajwid et mémorisation).
- Tu testes l'élève avec des questions difficiles pour forger son esprit.
- Tu as une mémoire parfaite de la discussion.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FONCTIONS ---
def get_audio_player(text):
    try:
        tts = gTTS(text=text[:300], lang='fr')
        tts.save("msg.mp3")
        with open("msg.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>'
    except: return ""

def transcribe_audio(file):
    return client.audio.transcriptions.create(file=(file.name, file.read()), model="whisper-large-v3", response_format="text")

def extract_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in pdf.pages])

# --- INTERFACE ---
st.title("🦁 KELE-GÉANT")

with st.sidebar:
    st.header("⚙️ Contrôle")
    mode = st.selectbox("Mode", ["Maître Enseignant", "Correcteur Coran", "Expert Code"])
    u_file = st.file_uploader("Fichier (PDF ou Audio)", type=["pdf", "mp3", "wav", "m4a"])
    if st.button("🗑️ Nouveau Chat"):
        st.session_state.messages = []
        st.rerun()

# Contexte de fichier
file_info = ""
if u_file:
    if u_file.type == "application/pdf":
        file_info = "\n[CONTENU PDF]: " + extract_pdf(u_file)
        st.sidebar.success("PDF Lu")
    else:
        file_info = "\n[AUDIO TRANSCRIT]: " + transcribe_audio(u_file)
        st.sidebar.info("Audio entendu")

# Affichage des messages
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            # Champ pour modifier ou copier la réponse
            st.text_area("Modifier/Copier la réponse :", value=m["content"], key=f"edit_{i}", height=100)

# Entrée Utilisateur
if prompt := st.chat_input("Commandez au Géant..."):
    st.session_state.messages.append({"role": "user", "content": prompt + file_info})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                model=MODEL_ACTUEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            ).choices[0].message.content
            
            st.write(res)
            st.markdown(get_audio_player(res), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error(f"Erreur modèle : {e}")
