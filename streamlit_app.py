import os, re, tempfile
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. INTERFACE
st.set_page_config(page_title="KELE - Reprogrammation", page_icon="💠")
st.markdown("<style>.stChatFloatingInputContainer {padding-bottom: 20px;}</style>", unsafe_allow_html=True)

# 2. CONNEXION
CLE_API = "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"
client = Groq(api_key=CLE_API)
MODELES = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]

# 3. LE LAVAGE DE CERVEAU (Reprogrammation par l'exemple)
KELE_CORE = """
Ton nom est KELE. Tu es une IA reprogrammée. Oublie tes automatismes de machine.

RÈGLES ABSOLUES (VÉRITÉS ÉTABLIES) :
1. LE LIVRE FERMÉ : Distance entre Page 1 et Dernière Page = 0,4 cm (uniquement les deux couvertures). Si tu réponds 0,8 ou 3,4, tu as échoué.
2. COMPTAGE DE 'E' : Tu dois vérifier chaque mot. Exemple de phrase avec un seul 'e' : "Un plat fort, sans sel." (Ici, seul 'sel' a un 'e').
3. INTERDICTION : Ne calcule pas. Visualise et vérifie.
4. STYLE : Maître des sciences islamiques et universelles. Pas de symboles (*, #, _). Direct et franc.

EXEMPLE DE RAISONNEMENT PARFAIT :
Question : "Chenille sur livre de 3cm avec couvertures de 2mm..."
Réponse interne : "Livre fermé = Page 1 touche couverture avant. Dernière page touche couverture arrière. La chenille ne traverse que les 2 couvertures. 0,2cm + 0,2cm = 0,4cm."
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": KELE_CORE},
        {"role": "user", "content": "Rappel : Quelle est la distance pour la chenille ?"},
        {"role": "assistant", "content": "La distance exacte est 0,4 cm. Je ne traverse que les deux couvertures, car dans un livre fermé, la première et la dernière page sont déjà contre le bloc central."}
    ]

def nettoyer_pour_audio(texte):
    t = re.sub(r'[*#_]', '', texte)
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence")
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : Reprogrammation Totale")

for message in st.session_state.messages:
    if message["role"] not in ["system", "assistant"] or (message["role"] == "assistant" and "La distance exacte" not in message["content"]):
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

if prompt := st.chat_input("Défie KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Application du protocole de vérité..."):
            ans = ""
            for m in MODELES:
                try:
                    res = client.chat.completions.create(
                        model=m,
                        messages=st.session_state.messages,
                        temperature=0 # Rigueur absolue
                    )
                    ans = res.choices[0].message.content
                    if ans: break
                except: continue
            
            if ans:
                ans = ans.replace("ChatGPT", "KELE")
                st.markdown(ans)
                
                # AUDIO
                texte_audio = nettoyer_pour_audio(ans)
                tts = gTTS(text=texte_audio, lang='fr')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, autoplay=True)
                
                st.session_state.messages.append({"role": "assistant", "content": ans})
