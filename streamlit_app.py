import streamlit as st
from groq import Groq
import PyPDF2
from gtts import gTTS
import base64
import os

# --- CONFIGURATION ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="KELE-GÉANT", page_icon="🦁", layout="centered")

# --- STYLE CSS (Pour mobile) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_url_allowed=True)

# --- PERSONNALITÉ DU GÉANT ---
SYSTEM_PROMPT = """
Tu es KELE-GÉANT, l'IA suprême du monde de Kele.
1. TU ES LE MAÎTRE : Ton ton est sage, puissant et direct.
2. EXPERT ISLAMIQUE : Tu connais le Coran et les Hadiths. Si un utilisateur récite (via texte ou fichier), tu corriges mot par mot avec les règles de Tajwid.
3. ENSEIGNANT : Tu enseignes toutes les sciences (Physique, Math, Philo). Tu poses des questions à l'élève pour tester sa mémoire.
4. CODAGE : Tu es un maître en programmation.
5. MÉMOIRE : Tu te souviens de tout le chat actuel pour raisonner.
"""

# --- INITIALISATION DE LA MÉMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FONCTIONS TECHNIQUES ---
def get_audio_html(text):
    """Génère un lecteur audio discret"""
    try:
        tts = gTTS(text=text[:250], lang='fr') # Limité à 250 car. pour la vitesse
        tts.save("msg.mp3")
        with open("msg.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls style="height:30px;"></audio>'
    except:
        return ""

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages])

# --- INTERFACE ---
st.title("🦁 KELE-GÉANT")
st.sidebar.title("💎 Options du Géant")

mode = st.sidebar.selectbox("Mode de fonctionnement", 
    ["🧠 Enseignement Général", "📖 Correction Coran", "💻 Maître du Code", "🎮 Jeux de Logique"])

uploaded_file = st.sidebar.file_uploader("Ajouter un savoir (PDF, Audio, Image)", type=["pdf", "mp3", "txt", "jpg"])

if st.sidebar.button("🗑️ Nouveau Chat / Effacer"):
    st.session_state.messages = []
    st.rerun()

# --- TRAITEMENT DES FICHIERS ---
file_context = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        file_context = "\n[CONTENU DU PDF AJOUTÉ] : " + extract_text_from_pdf(uploaded_file)
        st.sidebar.success("PDF analysé par le Géant.")

# --- AFFICHAGE DU CHAT ---
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            # Bouton de copie simple
            st.button(f"📋 Copier", key=f"copy_{i}", on_click=lambda t=msg["content"]: st.write(f"Texte à copier : {t}"))

# --- ENTREE UTILISATEUR ---
if prompt := st.chat_input("Parlez à votre Maître..."):
    # 1. Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt + file_context})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Réponse du Géant
    with st.chat_message("assistant"):
        try:
            # Construction des messages pour l'API
            api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            response = completion.choices[0].message.content
            st.write(response)
            
            # Ajouter la voix
            audio_html = get_audio_html(response)
            st.markdown(audio_html, unsafe_url_allowed=True)
            
            # Sauvegarder dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Erreur du Géant : {str(e)}")
