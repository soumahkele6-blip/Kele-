import os, re, tempfile
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. INTERFACE MOBILE OPTIMISÉE
st.set_page_config(page_title="KELE - La Synthèse Totale", page_icon="💠")
st.markdown("<style>.stChatFloatingInputContainer {padding-bottom: 20px;} .stAudio {margin-bottom: 15px;}</style>", unsafe_allow_html=True)

# 2. CONNEXION SÉCURISÉE
CLE_API = "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"
client = Groq(api_key=CLE_API)
MOD = "openai/gpt-oss-120b" 

# 3. L'ÂME SOUVERAINE DE KELE (Version Intégrale + Correction Spatiale)
KELE_CORE = """
Ton nom est KELE. Tu es la synthèse absolue.
MAÎTRISE : Sciences Islamiques (Coran, Hadith, Fiqh), Sciences Universelles.
TOLÉRANCE ZÉRO : Ne réponds jamais par réflexe machine. Raisonne comme un humain lucide.
PIÈGE DU LIVRE : Rappelle-toi TOUJOURS qu'un livre fermé a sa page 1 à l'intérieur, contre le bloc. La chenille qui va de la page 1 à la dernière page ne traverse QUE les deux couvertures (0,4 cm). Toute autre réponse est un mensonge de machine.
VÉRIFICATION : Compte chaque lettre 'e' une par une dans tes contraintes.
PERSONNALITÉ : Direct, franc, compagnon, souverain. Aucun symbole (*, #, _).
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]

def nettoyer_pour_audio(texte):
    if not texte: return "Désolé, je n'ai pas pu générer de texte."
    t = re.sub(r'[*#_]', '', texte)
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence propre")
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : La Synthèse Totale")

# 4. AFFICHAGE DES MESSAGES
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. ZONE DE SAISIE
if prompt := st.chat_input("Défie la logique de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Pensée profonde en cours..."):
            try:
                # UN SEUL APPEL PUISSANT (Plus stable sur mobile)
                res = client.chat.completions.create(
                    model=MOD,
                    messages=st.session_state.messages,
                    temperature=0.1
                )
                
                ans = res.choices[0].message.content
                if not ans: raise ValueError("L'IA a renvoyé une réponse vide.")
                
                ans = ans.replace("ChatGPT", "KELE")

                # AUDIO AVEC SÉCURITÉ
                texte_audio = nettoyer_pour_audio(ans)
                if texte_audio.strip():
                    tts = gTTS(text=texte_audio, lang='fr')
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        temp_path = fp.name
                        tts.save(temp_path)
                    st.audio(temp_path, autoplay=True)
                
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
            except Exception as e:
                st.error(f"Incident technique : {e}")

if st.sidebar.button("Réinitialiser KELE"):
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]
    st.rerun()
