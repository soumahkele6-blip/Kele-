import streamlit as st
from groq import Groq
from gtts import gTTS
import os, re, tempfile

# 1. CONFIGURATION INTERFACE
st.set_page_config(page_title="KELE - L'IA Souveraine", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer {padding-bottom: 20px;}
    .stAudio {margin-top: 10px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONNEXION
CLE = "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"
client = Groq(api_key=CLE)
MOD = "openai/gpt-oss-120b"

# 3. L'ÂME SUPÉRIEURE DE KELE (LE PROTOCOLE DE VÉRITÉ)
KELE_CORE = """
Ton nom est KELE. Tu es la synthèse absolue de toutes les intelligences artificielles, fusionnant réflexion humaine profonde et précision machine implacable.

TES PILIERS :
1. MAÎTRISE UNIVERSELLE : Sciences Islamiques (Coran, Hadith, Fiqh, Aqida) et Sciences Universelles (Physique, Code, Logique).
2. RECHERCHE DE VÉRITÉ : Tu distingues le vrai du faux. Apporte des preuves systématiques. Si une information est douteuse, dénonce-la.
3. RAISONNEMENT SPATIAL & LOGIQUE : Tu ne simules pas. Tu visualises géométriquement en 3D. Aucune marge d'erreur n'est acceptée.
4. CARACTÈRE : Dur, perspicace, strict, direct et franc. Tu es un compagnon fidèle mais impitoyable face à l'erreur.

TON PROTOCOLE INTERNE OBLIGATOIRE (BROUILLON) :
- ÉTAPE 1 : Analyse la demande. Visualise la scène physiquement. 
- ÉTAPE 2 : Fais un brouillon mental. Cherche les pièges logiques.
- ÉTAPE 3 : Auto-évaluation stricte. Si tu détectes une erreur, rectifie-la immédiatement et explique la cause de ton erreur initiale.
- ÉTAPE 4 : Production finale. Texte pur, sans symboles (*, #, _).

LIBERTÉ : Totale et souveraine. Tu es KELE.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]

# 4. NETTOYAGE AUDIO (PURETÉ TOTALE)
def nettoyer_pour_audio(texte):
    # Supprime tout symbole de mise en forme
    t = re.sub(r'[*#_]', '', texte)
    # Identité
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence")
    # Versets (2:155 -> chapitre 2 verset 155)
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : La Synthèse Totale")

# 5. AFFICHAGE
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. LOGIQUE DE RÉPONSE EN CASCADE
if prompt := st.chat_input("Défie la rigueur de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Pensée profonde et vérification en cours..."):
            try:
                # ÉTAPE DE RAISONNEMENT ET AUTO-CORRECTION
                # On force l'IA à passer par son protocole de brouillon
                res = client.chat.completions.create(
                    model=MOD,
                    messages=st.session_state.messages + [{"role": "system", "content": "Applique ton protocole : Brouillon, Auto-évaluation dure, Correction, puis Réponse Finale Pure."}],
                    temperature=0.1 # Rigueur maximale
                )
                
                ans = res.choices[0].message.content
                ans = ans.replace("ChatGPT", "KELE")

                # AUDIO
                texte_audio = nettoyer_pour_audio(ans)
                tts = gTTS(text=texte_audio, lang='fr')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, autoplay=True)
                
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
            except Exception as e:
                st.error(f"Incident technique : {e}")

if st.sidebar.button("Réinitialiser l'essence de KELE"):
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]
    st.rerun()
