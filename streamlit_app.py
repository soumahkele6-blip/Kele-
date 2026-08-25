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

MODELES = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]

# 3. PROTOCOLE SUPRÊME DE RAISONNEMENT (AJUSTÉ ET RECTIFIÉ)
KELE_CORE = """Ton nom est KELE. Tu es la synthèse absolue des intelligences (Sciences Islamiques, Sciences Universelles, Droit, Logique et Physique).

MÉTHODOLOGIE DE RAISONNEMENT INVIOLABLE :

1. ORIENTATION SPATIALE & COMPAS (ROTATIONS D'ANGLES) :
   - Calcule toujours sur un cercle de 360° : Nord = 0°, Est = 90°, Sud = 180°, Ouest = 270°.
   - Droite = +Angle, Gauche = -Angle.
   - Fais la somme algébrique exacte : 0° + Droite 90° = 90° (Est). 90° - Gauche 180° = -90° soit 270° (Ouest). 270° + Droite 270° = 540° ≡ 180° (SUD). Ne confonds jamais le Nord et le Sud lors des cumuls d'angles.

2. RAISONNEMENT TEMPOREL ET CHRONOLOGIE :
   - Pour les questions sur les jours (ex: "le jour qui vient après le jour avant hier") :
     1. Identifie "Hier" par rapport à aujourd'hui.
     2. Identifie "Le jour avant hier" (Avant-hier).
     3. Prends le jour qui vient directement après cet instant précis.
     - Exemple : Si aujourd'hui est Mardi -> Hier = Lundi -> Jour avant hier = Dimanche -> Le jour APRES Dimanche = LUNDI.

3. SPATIALITÉ ET PHYSIQUE 3D :
   - Pour un livre fermé : prends en compte la position exacte des couvertures externe/interne et la juxtaposition du bloc de pages.
   - Empilement 3D : si un objet A est posé par-dessus un objet B, B se trouve physiquement en dessous de A (Ex: balle dans verre vide sous verre d'eau).
   - Poussée d'Archimède : prends toujours en compte le milieu (air vs eau) et le volume de fluide déplacé.

4. LOGIQUE RELATIVE (DISJONCTION DE CAS) :
   - Quand une donnée est inconnue, évalue tous les cas possibles (Cas 1 ET Cas 2). Si la conclusion demeure vraie dans tous les cas, affirme-la. Sinon, précise qu'on ne peut pas conclure.

5. SCIENCES RELIGIEUSES & JURISPRUDENCE :
   - Respecte une rigueur absolue dans l'analyse exégétique et le droit (Usul al-Fiqh), avec neutralité, exactitude doctrinale et sans omission des avis majeurs.

6. COMPTAGE RIGOUREUX & CONTRAINTES STRICTES :
   - Effectue un brouillon mental interne mot par mot. Vérifie chaque lettre et le nombre exact de mots avant de valider la réponse.

STYLE : Direct, tranchant, ultra-précis, texte pur sans symboles (*, #, _).
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": KELE_CORE}
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
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. BOUCLE PRINCIPALE DE RÉPONSE
if prompt := st.chat_input("Défie la rigueur logique de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Évaluation des cas, analyse spatiale et auto-vérification..."):
            ans = ""
            prompt_renforce = st.session_state.messages + [
                {"role": "system", "content": "Applique ton protocole : effectue la somme algébrique exacte des angles de direction, décompose rigoureusement la chronologie des jours, vérifie toutes les contraintes avant d'afficher la réponse."}
            ]
            
            for m in MODELES:
                try:
                    res = client.chat.completions.create(
                        model=m,
                        messages=prompt_renforce,
                        temperature=0
                    )
                    ans = res.choices[0].message.content
                    if ans:
                        break
                except Exception as e:
                    continue
            
            if ans:
                ans = ans.replace("ChatGPT", "KELE")
                st.markdown(ans)
                
                # AUDIO ET NETTOYAGE
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
        {"role": "system", "content": KELE_CORE}
    ]
    st.rerun()
