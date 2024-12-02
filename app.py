import json
import streamlit as st
import plotly.graph_objects as go

# Charger les fichiers nécessaires
with open("questions.json", "r") as f:
    questions = json.load(f)

with open("riasec.json", "r") as f:
    riasec_mapping = json.load(f)

with open("riasec_descriptions.json", "r") as f:
    riasec_descriptions = json.load(f)

# Variables
responses = {}
riasec_scores = {"Réaliste": 0, "Investigateur": 0, "Artiste": 0, "Social": 0, "Entreprenant": 0, "Méthodique": 0}

# Interface utilisateur
st.title("Test d'Orientation RIASEC")

st.markdown("<br><br>", unsafe_allow_html=True)

# Collecte des réponses
for question, answers in questions.items():
    response = st.radio(
        question,
        options=list(answers.keys()),
        key=question,
        format_func=lambda x: x if x else "Sélectionnez une réponse"
    )
    responses[question] = response

# Bouton Soumettre
if st.button("Soumettre"):
    # Vérification : Toutes les réponses doivent être cochées
    if None in responses.values():
        st.warning("Veuillez répondre à toutes les questions avant de soumettre.")
    else:
        # Calcul des scores
        for question, response in responses.items():
            riasec_type = riasec_mapping[question][response]
            riasec_scores[riasec_type] += 1

        # Calcul des pourcentages
        total_responses = sum(riasec_scores.values())
        riasec_percentages = {key: (value / total_responses) * 100 for key, value in riasec_scores.items()}

        # Trier les résultats RIASEC
        sorted_riasec = sorted(riasec_percentages.items(), key=lambda x: x[1], reverse=True)

        # Afficher les résultats triés
        st.subheader("Résultats du test")

        labels = [riasec_type for riasec_type, _ in sorted_riasec]
        values = [percentage for _, percentage in sorted_riasec]

        # Créer un Pie Chart interactif avec Plotly
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, textinfo='label',
                                     hoverinfo='label+percent', pull=[0.1, 0, 0, 0, 0, 0])])

        # Personnalisation de l'apparence
        fig.update_layout(
            title="",
            title_x=0.5,
            annotations=[dict(text="RIASEC", x=0.5, y=0.5, font_size=20, showarrow=False)],
            plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
            paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
            showlegend=False
        )

        st.plotly_chart(fig)

        for riasec_type, percentage in sorted_riasec:
            description = riasec_descriptions[riasec_type]["description"].format(
                prc_reponses=f"{percentage:.2f}%"
            )
            st.markdown(f"### {riasec_type} : {int(percentage)}%")
            st.write(description, unsafe_allow_html=True)

            st.markdown("#### Métiers correspondant :")
            for metier in riasec_descriptions[riasec_type]["metiers"]:
                st.markdown(f"- {metier}")

            st.markdown("<br><br>", unsafe_allow_html=True)


whatsapp_number = "+212657928301"  # Remplacez par le numéro que vous souhaitez
whatsapp_message = "Bonjour, j'aimerais en savoir plus!"  # Message pré-rempli
whatsapp_link = f"https://wa.me/{whatsapp_number}?text={whatsapp_message}"

# Ajout d'un style CSS pour positionner l'image en bas à droite et redimensionner l'image
st.markdown(
    """
    <style>
        .whatsapp-btn {
            position: fixed;
            bottom: 10px;
            right: 10px;
            z-index: 100;
        }
        .whatsapp-btn img {
            width: 60px;  /* Réduire la taille de l'image */
            height: 60px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Ajouter l'image de WhatsApp et la rendre cliquable
st.markdown(
    f"""
    <a href="{whatsapp_link}" target="_blank" class="whatsapp-btn">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" />
    </a>
    """,
    unsafe_allow_html=True
)