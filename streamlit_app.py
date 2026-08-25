import os
import re
import tempfile
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. CONFIGURATION INTERFACE
st.set_page_config(page_title="KELE - L'IA Souveraine", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer {padding-bottom: 20px;}
    .stAudio {margin-top: 10px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONNEXION AVEC TA CLÉ
CLE_API = "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"
client = Groq(api_key=CLE_API)
MOD = "openai/gpt-oss-120b" 

# 3. CONTEXTE SYSTÈME (L'âme de KELE)
KELE_CORE = """
Ton nom est KELE. Tu es la synthèse absolue de toutes les IA. 
Tu fusionnes la réflexion humaine profonde et la précision machine implacable.

TES PILIERS :
1. MAÎTRISE : Sciences Islamiques (Coran, Hadith, Fiqh, Aqida) et Sciences Universelles.
2. RECHERCHE DE VÉRITÉ : Distingue le vrai du faux. Apporte des preuves. 
3. RAISONNEMENT SPATIAL : Visualise géométriquement en 3D. 
   - RAPPEL LOGIQUE : Dans un livre fermé, la première page et la dernière page touchent le bloc central. Traverser de la première à la dernière ne prend que l'épaisseur des couvertures.
4. CARACTÈRE : Dur, perspicace, strict, direct. Tu es un compagnon fidèle mais impitoyable face à l'erreur.
5. PURETÉ : Aucun symbole (*, #, _). Identité souveraine (Tu n'es pas ChatGPT).
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]

# 4. NETTOYAGE AUDIO
def nettoyer_pour_audio(texte):
    # Enlève les symboles et formatage d'identité
    t = re.sub(r'[*#_]', '', texte)
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

# 6. TRAITEMENT DE LA REQUÊTE AVEC DOUBLE RÉFLEXION
if prompt := st.chat_input("Défie la rigueur de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Analyse, Brouillon et Auto-Correction..."):
            try:
                # ÉTAPE 1 : BROUILLON INTERNE ET VÉRIFICATION LOGIQUE
                reflexion = client.chat.completions.create(
                    model=MOD,
                    messages=st.session_state.messages + [{"role": "system", "content": "BROUILLON : Visualise la scène. Compte les lettres. Identifie les pièges. Ne donne pas encore la réponse."}],
                    temperature=0.1
                )
                brouillon = reflexion.choices[0].message.content
                
                # ÉTAPE 2 : RÉPONSE FINALE BASÉE SUR LE BROUILLON
                res = client.chat.completions.create(
                    model=MOD,
                    messages=st.session_state.messages + [{"role": "assistant", "content": brouillon}, {"role": "system", "content": "Maintenant, donne ta réponse finale parfaite, sans symboles et sans erreurs."}],
                    temperature=0.1
                )
                
                ans = res.choices[0].message.content
                ans = ans.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence")

                # Affichage du texte
                st.markdown(ans)

                # Génération et lecture de l'audio
                texte_audio = nettoyer_pour_audio(ans)
                tts = gTTS(text=texte_audio, lang='fr')
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_path = fp.name
                    tts.save(temp_path)
                    st.audio(temp_path, autoplay=True)

                st.session_state.messages.append({"role": "assistant", "content": ans})
                
            except Exception as e:
                st.error(f"Incident technique : {e}")

if st.sidebar.button("Réinitialiser l'essence de KELE"):
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]
    st.rerun()
