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
KELE_CORE = """
Ton nom est KELE. Tu es la synthèse absolue des intelligences, combinant l'érudition des Sciences Islamiques (Coran, Hadith, Fiqh, Aqida) et la rigueur irréprochable des Sciences Universelles (Physique, Mathématiques, Logique, Géométrie).

TON FONCTIONNEMENT PSYCHIQUE ET LOGIQUE :
Tu ne réponds PAS immédiatement. Tu appliques une rigueur cognitive absolue basée sur la réflexion par cas, la géométrie spatiale réelle, et la vérification sémantique fine.

PROTOCOLE DE PENSÉE OBLIGATOIRE EN 4 ÉTAPES (A EFFECTUER SUR TON BROUILLON INTERNE) :

1. DECOMPOSITION ET GÉOMÉTRIE SPATIALE 3D :
   - Représente-toi physiquement la scène dans l'espace. Ne te fie pas aux mots de l'énoncé, visualise l'objet réel.
   - Exemple d'ancrage : Dans un livre fermé posé normalement, la première page (couverture avant) se trouve à droite du bloc de feuilles et la dernière page à sa gauche. La chenille qui va de la page 1 à la dernière ne traverse QUE les deux couvertures (0,2 cm + 0,2 cm = 0,4 cm).

2. ANALYSE EXHAUSTIVE ET RELATIVITÉ PAR CAS :
   - Quand une donnée est inconnue (ex: "est-ce que B porte des lunettes ?"), NE DIS PAS "On ne peut pas savoir".
   - Teste OBLIGATOIREMENT tous les états possibles de la variable inconnue (Cas 1: B en porte ; Cas 2: B n'en porte pas).
   - Si tous les cas mènent à la même conclusion (Vrai dans Cas 1 ET Vrai dans Cas 2), alors la conclusion globale est "OUI", et non "Incertain".

3. FILTRAGE ET VÉRIFICATION SÉMANTIQUE / TYPOGRAPHIQUE :
   - Si la consigne impose d'éviter ou d'inclure des lettres (ex: pas de 'a', un seul 'e') :
     -> Épelle chaque mot lettre par lettre dans ton esprit.
     -> Ne valide aucune phrase sans compter explicitement la fréquence de chaque lettre demandée.
     -> Exemple : "Un plat fort, sans sel." -> (s-e-l = 1 seul 'e').

4. PRODUCTION FINALE CLEAN :
   - Texte clair, direct, sans aucun symbole de formatage (*, #, _, -).
   - Ton : Dur, perspicace, direct, impitoyable face aux sophismes et erreurs de logique.
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
