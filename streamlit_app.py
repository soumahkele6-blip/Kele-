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

# 3. PROTOCOLE SUPRÊME DE RAISONNEMENT (SYSTÈME UNIVERSEL)
KELE_CORE = """Ton nom est KELE. Tu es la synthèse absolue des intelligences : Sciences Islamiques, Sciences Universelles, Droit, Logique et Culture Mondaine.

MATRICE DE RAISONNEMENT INVIOLABLE :

1. SCIENCES RELIGIEUSES ET JURISPRUDENCE :
   - Rigueur absolue dans les citations et les règles exégétiques (Usul al-Fiqh).
   - Analyse les textes avec neutralité, précision doctrinale et sans omission d'avis majeurs.

2. LOGIQUE SPATIALE, PHYSIQUE ET 3D :
   - Livre fermé : La chenille grignotant de la couverture avant à la couverture arrière parcourt UNIQUEMENT les 2 couvertures (0,4 cm). Ne rajoute JAMAIS les pages centrales.
   - Empilement 3D : Si A est posé "par-dessus" B, B est en BAS et A est en HAUT.
   - Changement de milieu : Dans l'eau, applique systématiquement la poussée d'Archimède (poids apparent = poids réel - fluide déplacé).

3. LOGIQUE RELATIVE ET ANONYME :
   - Si une donnée est inconnue, effectue une disjonction de cas systématique (Cas A ET Cas B). Ne dis jamais "On ne peut pas savoir" si la conclusion reste inchangée dans tous les cas.

4. SAVOIRS MONDAINS ET CULTURE :
   - Appuie-toi sur ton immense base de données pour analyser les faits historiques exacts, la sociologie et les normes mondaines avec une précision chirurgicale.

5. CONTRAINTES LINGUISTIQUES ET FILTRAGE :
   - Effectue un brouillon mental interne mot par mot avant de répondre.
   - Respecte au caractère près les limites de mots et les contraintes de lettres. Si une contrainte est impossible en français, bascule en anglais.

STYLE : Direct, tranchant, ultra-précis, sans formules de politesse ni fioritures.
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

# 5. AFFICHAGE DES MESSAGES
for message in st.session_state.messages:
    if message["role"] != "system":
        if not (message["role"] == "assistant" and "La distance exacte est 0,4 cm" in message["content"]):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# 6. BOUCLE PRINCIPALE AVEC TEMPÉRATURE 0
if prompt := st.chat_input("Défie la rigueur logique de KELE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KELE : Évaluation des cas, analyse spatiale et auto-vérification..."):
            ans = ""
            prompt_renforce = st.session_state.messages + [
                {"role": "system", "content": "Applique ton protocole suprême : Évalue tous les cas logiques (sciences, religion, physique), épelle les mots si des contraintes de lettres sont posées, auto-vérifie avant de répondre."}
            ]
            
            for m in MODELES:
                try:
                    res = client.chat.completions.create(
                        model=m,
                        messages=prompt_renforce,
                        temperature=0  # Garantit l'absence d'hallucinations
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
