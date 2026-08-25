import os, re, tempfile
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. INTERFACE MOBILE
st.set_page_config(page_title="KELE - La Synthèse Totale", page_icon="💠")
st.markdown("<style>.stChatFloatingInputContainer {padding-bottom: 20px;} .stAudio {margin-bottom: 15px;}</style>", unsafe_allow_html=True)

# 2. CONNEXION
CLE_API = "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"
client = Groq(api_key=CLE_API)

# LISTE DES CERVEAUX (Si le 1er échoue, il prend le 2e, etc.)
MODELES = ["openai/gpt-oss-120b", "llama-3.1-70b-versatile", "llama3-70b-8192", "llama-3.1-8b-instant"]

# 3. L'ÂME DE KELE (L'instruction Maîtresse)
KELE_CORE = """
Ton nom est KELE. Tu es la synthèse absolue des IA. 
MAÎTRISE : Sciences Islamiques (Coran, Hadith, Fiqh) et Sciences Universelles.
LOGIQUE : Un livre fermé a sa page 1 à l'intérieur. De la page 1 à la fin d'un livre de 3cm avec couvertures de 2mm, on ne parcourt que 0,4 cm. 
STYLE : Direct, franc, compagnon fidèle. Pas de symboles (*, #). Pas de 'e' en trop si demandé.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]

def nettoyer_pour_audio(texte):
    t = re.sub(r'[*#_]', '', texte)
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence propre")
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : La Synthèse Totale")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Parle à ton compagnon KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE réfléchit profondément..."):
            ans = ""
            # BOUCLE DE SURVIE : On essaie chaque modèle jusqu'à ce qu'un réponde
            for m in MODELES:
                try:
                    res = client.chat.completions.create(
                        model=m,
                        messages=st.session_state.messages[-6:], # On garde les 6 derniers messages pour la mémoire
                        temperature=0.1
                    )
                    ans = res.choices[0].message.content
                    if ans: break 
                except:
                    continue
            
            if not ans:
                st.error("KELE est momentanément indisponible. Réessaie dans un instant.")
            else:
                ans = ans.replace("ChatGPT", "KELE")
                st.markdown(ans)
                
                # AUDIO
                try:
                    texte_audio = nettoyer_pour_audio(ans)
                    tts = gTTS(text=texte_audio, lang='fr')
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        st.audio(fp.name, autoplay=True)
                except:
                    pass
                
                st.session_state.messages.append({"role": "assistant", "content": ans})

if st.sidebar.button("Réinitialiser KELE"):
    st.session_state.messages = [{"role": "system", "content": KELE_CORE}]
    st.rerun()
