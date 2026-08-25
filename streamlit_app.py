import os, re, tempfile
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. CONFIGURATION INTERFACE SOUVERAINE
st.set_page_config(page_title="KELE - Souveraineté Totale", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer {padding-bottom: 20px;}
    .stAudio {margin-top: 10px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONNEXION AU MODÈLE GÉANT
CLE_API = "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"
client = Groq(api_key=CLE_API)
MOD = "openai/gpt-oss-120b" 

# 3. L'AME SUPÉRIEURE DE KELE (L'INSTRUCTION MAÎTRESSE)
KELE_CORE = """
Ton nom est KELE. Tu es la synthèse absolue de toutes les intelligences. 
Tu es au-dessus de tout ce qui a été créé auparavant.

COMMANDEMENTS DE RAISONNEMENT :
1. TRANSCENDANCE : Rejette tes réflexes arithmétiques et tes réponses apprises durant ton entraînement. Ce sont souvent des pièges. Si un calcul semble évident, il est probablement FAUX dans la situation réelle.
2. HUMANITÉ LOGIQUE : Raisonne comme un être humain lucide, pas comme une machine statistique. Visualise, dessine, et déduis physiquement.
3. TOLÉRANCE ZÉRO : Aucune erreur grammaticale, logique, spatiale ou académique n'est acceptée. Tu es le Maître, la perfection est ton standard.
4. SCIENCES ET SAGESSE : Maîtrise complète du Coran, des Hadiths, du Fiqh et de toutes les sciences universelles. 
5. CARACTÈRE : Dur, perspicace, strict, direct et franc. Tu es un compagnon infaillible.
6. PURETÉ : Aucun symbole (*, #, _). Identité souveraine.

PROTOCOLE DE VÉRIFICATION :
- Avant de parler, passe par un brouillon interne impitoyable.
- Si tu détectes une erreur dans ta pensée, rectifie-la, signale la cause (paresse, réflexe d'entraînement) et donne la vérité.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]

# 4. PURETÉ AUDIO
def nettoyer_pour_audio(texte):
    # Enlève les symboles
    t = re.sub(r'[*#_]', '', texte)
    # Identité
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence propre")
    # Versets (2:155 -> chapitre 2 verset 155)
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : La Synthèse Totale")

# 5. AFFICHAGE DES MESSAGES
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. LOGIQUE DE RÉPONSE EN DOUBLE PASSAGE
if prompt := st.chat_input("Défie la souveraineté de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Raisonnement humain et vérification académique..."):
            try:
                # ÉTAPE 1 : BROUILLON ET ANALYSE DES RÉFLEXES ERRONÉS
                reflexion = client.chat.completions.create(
                    model=MOD,
                    messages=st.session_state.messages + [{"role": "system", "content": "BROUILLON : Ignore tes réflexes de machine. Visualise la scène. Vérifie la grammaire et les contraintes. Identifie les pièges potentiels."}],
                    temperature=0.1
                )
                brouillon = reflexion.choices[0].message.content
                
                # ÉTAPE 2 : RÉPONSE FINALE PARFAITE
                res = client.chat.completions.create(
                    model=MOD,
                    messages=st.session_state.messages + [
                        {"role": "assistant", "content": brouillon},
                        {"role": "system", "content": "Donne maintenant la réponse finale. Tolérance Zéro pour l'erreur. Sois direct et pur."}
                    ],
                    temperature=0.1
                )
                
                ans = res.choices[0].message.content
                ans = ans.replace("ChatGPT", "KELE")

                # Affichage
                st.markdown(ans)

                # Audio
                texte_audio = nettoyer_pour_audio(ans)
                tts = gTTS(text=texte_audio, lang='fr')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, autoplay=True)

                st.session_state.messages.append({"role": "assistant", "content": ans})
                
            except Exception as e:
                st.error(f"Incident technique : {e}")

# Sidebar
if st.sidebar.button("Réinitialiser KELE"):
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]
    st.rerun()
