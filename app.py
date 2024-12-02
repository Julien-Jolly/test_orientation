import json
import streamlit as st
import plotly.graph_objects as go

with open("questions.json", "r") as f:
    questions = json.load(f)

with open("riasec.json", "r") as f:
    riasec_mapping = json.load(f)

with open("riasec_descriptions.json", "r") as f:
    riasec_descriptions = json.load(f)

responses = {}
riasec_scores = {"Réaliste": 0, "Investigateur": 0, "Artiste": 0, "Social": 0, "Entreprenant": 0, "Méthodique": 0}

whatsapp_number = "+212657928301"
whatsapp_message = "Bonjour, j'aimerais en savoir plus!"
whatsapp_link = f"https://wa.me/{whatsapp_number}?text={whatsapp_message}"

# Titre principal avec l'image à gauche
st.markdown(
    """
    <style>

        /* Bandeau fixe en bas, couleur blanche */
        .whatsapp-btn-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;  /* Fond blanc */
            padding: 15px 20px;  /* Ajouter un peu d'espace autour */
            display: flex;
            justify-content: flex-end;  /* Aligner le texte et l'icône à droite */
            align-items: center;
            z-index: 100;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);  /* Ombre légère pour le bandeau */
        }

        .whatsapp-btn-container .whatsapp-text {
            font-size: 16px;  /* Taille du texte */
            color: #25D366;   /* Couleur verte de WhatsApp */
            margin-right: 10px;  /* Espacement entre le texte et l'icône */
        }

        .whatsapp-btn-container a {
            display: block;
        }

        /* Réduire la taille de l'image WhatsApp */
        .whatsapp-btn-container img {
            width: 60px;  /* Taille ajustée */
            height: 60px;
        }

        /* Adapter le texte pour les mobiles */
        body {
            font-family: Arial, sans-serif;
            line-height: 1;
            margin-bottom: 80px;  /* Laisser de l'espace pour le bandeau */
            margin-top: 80px; /* Laisser de l'espace pour le bandeau en haut */
        }

        /* Responsivité du texte */
        @media only screen and (max-width: 600px) {
            body {
                font-size: 14px;
            }
        }

        /* Ajouter un espacement entre les sections */
        .content-section {
            margin-bottom: 40px;
        }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.image("https://www.capstudies.com/wp-content/uploads/2020/10/logo-site-web-1.png", width=200)

st.sidebar.markdown(
    """
    ## Qu'est-ce que le modèle RIASEC ?

    Le modèle RIASEC (ou Hexaco) est un outil d'orientation professionnelle qui classifie les individus selon six grands types de personnalités. Chaque type est associé à un ensemble d'intérêts professionnels et de comportements typiques :

    - **Réaliste** : Préfère les tâches pratiques et concrètes, souvent liées à des activités techniques ou manuelles.
    - **Investigateur** : Aime résoudre des problèmes et analyser des informations, souvent dans des environnements académiques ou scientifiques.
    - **Artiste** : Recherche des opportunités créatives, souvent dans des domaines comme l'art, la musique ou l'écriture.
    - **Social** : Préfère aider et interagir avec les autres, souvent dans des rôles éducatifs, sociaux ou de conseil.
    - **Entreprenant** : Aime influencer et diriger les autres, souvent dans des environnements de vente ou de gestion.
    - **Conventionnel** : Aussi appelé "Méthodique", préfère des tâches organisées et structurées, souvent liées à la gestion, l'administration ou l'informatique.

    Ce test vous aidera à découvrir quel profil RIASEC correspond le mieux à vos intérêts et à vos compétences professionnelles.
    """, unsafe_allow_html=True
)

st.title("Test d'Orientation RIASEC")

# Code pour gérer les questions et afficher les résultats
st.markdown("<br><br>", unsafe_allow_html=True)

for question, answers in questions.items():
    response = st.radio(
        question,
        options=list(answers.keys()),
        key=question,
        format_func=lambda x: x if x else "Sélectionnez une réponse"
    )
    responses[question] = response

if st.button("Soumettre"):
    if None in responses.values():
        st.warning("Veuillez répondre à toutes les questions avant de soumettre.")
    else:
        for question, response in responses.items():
            riasec_type = riasec_mapping[question][response]
            riasec_scores[riasec_type] += 1

        total_responses = sum(riasec_scores.values())
        riasec_percentages = {key: (value / total_responses) * 100 for key, value in riasec_scores.items()}

        sorted_riasec = sorted(riasec_percentages.items(), key=lambda x: x[1], reverse=True)

        st.subheader("Résultats du test")

        labels = [riasec_type for riasec_type, _ in sorted_riasec]
        values = [percentage for _, percentage in sorted_riasec]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, textinfo='label',
                                     hoverinfo='label+percent', pull=[0.1, 0, 0, 0, 0, 0])])

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

# Ajouter le bouton WhatsApp
st.markdown(
    f"""
    <div class="whatsapp-btn-container">
        <div class="whatsapp-text">Discutons de vos résultats sur WhatsApp et trouvons votre plan d'orientation idéal</div>
        <a href="{whatsapp_link}" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
