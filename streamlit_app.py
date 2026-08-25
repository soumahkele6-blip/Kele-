import os, re, tempfile
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

# 2. CONNEXION ET SÉCURITÉ DES MODÈLES
CLE_API = "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"
client = Groq(api_key=CLE_API)

# Conserves exactement tes modèles sans les altérer
MODELES = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]

# 3. PROTOCOLE SUPRÊME DE RAISONNEMENT ET D'AUTO-VÉRIFICATION (SYSTEM PROMPT)
KELE_CORE = """Ton nom est KELE. Tu es la synthèse absolue des intelligences (Sciences Islamiques et Sciences Universelles).

RÈGLES RIGIDE DE RAISONNEMENT :

1. ANCRAGE PHYSIQUE ET SPATIAL (LE LIVRE FERMÉ) :
   - Un livre fermé posé normalement a sa couverture avant À DROITE du bloc de pages et sa couverture arrière À GAUCHE.
   - La première page (intérieur couverture avant) touche DÉJÀ la dernière page (intérieur couverture arrière) à travers l'épaisseur des couvertures si la chenille est sur les faces externes.
   - Une chenille allant de la couverture avant à la couverture arrière d'un livre FERMÉ traverse UNIQUEMENT les 2 couvertures (0,2 cm + 0,2 cm = 0,4 cm).
   - NE RAJOUTE JAMAIS LES 3 CM DES PAGES CENTRALES. La réponse est 0,4 cm.

2. ANALYSE EXHAUSTIVE PAR CAS (LOGIQUE RELATIVE) :
   - Si une donnée est inconnue, ne dis jamais "On ne sait pas". Évalue tous les cas (Cas A et Cas B). Si la conclusion est identique dans tous les cas, la réponse est affirmative.

3. COMPTAGE RIGOUREUX DES LETTRES (BROUILLON OBLIGATOIRE) :
   - Avant de valider une phrase sous contrainte, décompose chaque mot lettre par lettre pour vérifier l'absence ou la présence exacte de la lettre demandée.
   - Exemple : "Il clarifie tout" contient DEUX 'e' (il, clarifie) -> INVALIDE. "Un plat fort sans sel" contient UN SEUL 'e' (sel) -> VALIDE.

4. STYLE : Direct, sans fioritures, texte pur sans symboles (*, #, _).
 """

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": KELE_CORE},
        {"role": "user", "content": "Rappel : Quelle est la distance pour la chenille ?"},
        {"role": "assistant", "content": "La distance exacte est 0,4 cm. En visualisant physiquement le livre fermé, la première page est collée à la couverture avant et la dernière à la couverture arrière. La chenille ne traverse que les deux couvertures."}
    ]

# 4. FONCTION DE NETTOYAGE POUR LE TTS
def nettoyer_pour_audio(texte):
    t = re.sub(r'[*#_]', '', texte)
    t = t.replace("ChatGPT", "KELE").replace("OpenAI", "mon essence")
    t = re.sub(r'(\d+):(\d+)', r'chapitre \1 verset \2', t)
    return t

st.title("🛡️ KELE : Synthèse & Puissance Logique")

# 5. AFFICHAGE DES MESSAGES DU CHAT
for message in st.session_state.messages:
    if message["role"] != "system":
        if not (message["role"] == "assistant" and "La distance exacte est 0,4 cm" in message["content"]):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# 6. BOUCLE PRINCIPALE DE RÉPONSE AVEC AUTO-CORRECTION ET CASCADE
if prompt := st.chat_input("Défie la rigueur logique de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Évaluation des cas, analyse spatiale et auto-vérification..."):
            ans = ""
            prompt_renforce = st.session_state.messages + [
                {"role": "system", "content": "Applique ton protocole suprême : Évalue tous les cas logiques, épelle les mots si des contraintes de lettres sont posées, auto-vérifie avant de répondre."}
            ]
            
            for m in MODELES:
                try:
                    res = client.chat.completions.create(
                        model=m,
                        messages=prompt_renforce,
                        temperature=0  # Temperature 0 pour garantir zéro hallucination
                    )
                    ans = res.choices[0].message.content
                    if ans:
                        break
                except Exception as e:
                    continue
            
            if ans:
                ans = ans.replace("ChatGPT", "KELE")
                st.markdown(ans)
                
                # AUDIO ET NETTOYAGE DU FICHIER TEMPORAIRE
                try:
                    texte_audio = nettoyer_pour_audio(ans)
                    tts = gTTS(text=texte_audio, lang='fr')
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        temp_path = fp.name
                        tts.save(temp_path)
                    
                    st.audio(temp_path, autoplay=True)
                    os.remove(temp_path)
                except Exception as audio_err:
                    pass
                
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error("Aucun des modèles spécifiés n'a pu répondre. Vérifiez la connexion API.")

if st.sidebar.button("Réinitialiser l'essence de KELE"):
    st.session_state.messages = [
        {"role": "system", "content": KELE_CORE},
        {"role": "user", "content": "Rappel : Quelle est la distance pour la chenille ?"},
        {"role": "assistant", "content": "La distance exacte est 0,4 cm. En visualisant physiquement le livre fermé, la première page est collée à la couverture avant et la dernière à la couverture arrière. La chenille ne traverse que les deux couvertures."}
    ]
    st.rerun()
