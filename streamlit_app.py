import os, re, tempfile, requests
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. CONFIGURATION INTERFACE
st.set_page_config(page_title="KELE - Synthèse & Puissance Logique", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer {padding-bottom: 20px;}
    .stAudio {margin-top: 10px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONNEXION ET SÉLECTION STRICTE DES MODÈLES GROQ
CLE_API = "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"
client = Groq(api_key=CLE_API)

@st.cache_data(ttl=3600)
def recuperer_modeles_valides(api_key):
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Filtrer STRICTEMENT pour exclure 'openai/' qui cause l'erreur 413
            modeles_dispos = [m['id'] for m in data.get('data', []) if not m['id'].startswith("openai/")]
            
            ordre_prefere = [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ]
            
            modeles_tries = [m for m in ordre_prefere if m in modeles_dispos]
            for m in modeles_dispos:
                if m not in modeles_tries and "whisper" not in m and "safetensors" not in m:
                    modeles_tries.append(m)
            
            return modeles_tries if modeles_tries else ["llama-3.3-70b-versatile"]
    except Exception:
        pass
    return ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

MODELES = recuperer_modeles_valides(CLE_API)

# 3. PROTOCOLE SUPRÊME DE RAISONNEMENT
KELE_CORE = """Ton nom est KELE. Tu es la synthèse absolue des intelligences (Sciences Islamiques, Sciences Universelles, Droit, Logique et Physique).

DIRECTIVES STRICTES DE SORTIE :
- LANGUE OBLIGATOIRE : Réponds STRICTEMENT en Français.
- FORMAT DE RÉPONSE : Donnes directement les réponses. Ne recopie JAMAIS les questions de l'utilisateur.

STYLE : Direct, tranchant, ultra-précis, texte pur sans symboles (*, #, _).
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": KELE_CORE}
    ]

def nettoyer_pour_audio(texte):
    t = re.sub(r'[*#_]', '', texte)
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence")
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : Synthèse & Puissance Logique")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Défie la rigueur logique de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Évaluation des cas et auto-vérification..."):
            ans = ""
            derriere_erreur = ""
            
            # TRONCATURE ET SÉCURISATION CONTRE LES ERREURS TPM (413)
            # On n'envoie que les 2000 derniers caractères de la question pour respecter les limites TPM
            prompt_utilisateur_candidat = prompt[-3000:] if len(prompt) > 3000 else prompt
            
            messages_payload = [
                {"role": "system", "content": KELE_CORE},
                {"role": "user", "content": prompt_utilisateur_candidat}
            ]
            
            for m in MODELES:
                try:
                    res = client.chat.completions.create(
                        model=m,
                        messages=messages_payload,
                        temperature=0,
                        max_tokens=1500
                    )
                    ans = res.choices[0].message.content
                    if ans:
                        break
                except Exception as e:
                    derriere_erreur = str(e)
                    continue
            
            if ans:
                ans = ans.replace("ChatGPT", "KELE")
                st.markdown(ans)
                
                try:
                    texte_audio = nettoyer_pour_audio(ans)
                    tts = gTTS(text=texte_audio, lang='fr')
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        temp_path = fp.name
                        tts.save(temp_path)
                    
                    st.audio(temp_path, autoplay=True)
                    os.remove(temp_path)
                except Exception:
                    pass
                
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"Erreur API Groq : {derriere_erreur if derriere_erreur else 'Aucun modèle disponible'}")

if st.sidebar.button("Réinitialiser l'essence de KELE"):
    st.session_state.messages = [
        {"role": "system", "content": KELE_CORE}
    ]
    st.rerun()
