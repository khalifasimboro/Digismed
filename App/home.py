import streamlit as st

# Définir le style CSS personnalisé pour l'arrière-plan et le bouton
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('background.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0;
        padding: 0;
    }
    .welcome-text {
        color: black;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .start-button {
        background-color: #f0e68c; /* Jaune clair similaire à l'image */
        color: black;
        font-size: 24px;
        padding: 10px 20px;
        border: none;
        border-radius: 50px; /* Forme arrondie */
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        text-align: center;
        display: inline-block;
        text-decoration: none;
    }
    .start-button:hover {
        background-color: #e6d85c; /* Légère variation au survol */
    }
    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Conteneur pour centrer "Bienvenu sur Digismed" verticalement et horizontalement
with st.container():
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        st.markdown('<div class="welcome-text">Bienvenu sur Digismed</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Conteneur pour centrer le contenu verticalement et horizontalement
with st.container():
    col4, col5, col6 = st.columns([5, 15, 5])
    with col2:
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        st.markdown('<a href="#" class="start-button" id="start-button">Démarer</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Ajouter un script pour détecter le clic sur le bouton personnalisé
st.markdown(
    """
    <script>
    document.getElementById("start-button").addEventListener("click", function() {
        // Simuler une action lors du clic
        alert("Démarrer cliqué !");
    });
    </script>
    """,
    unsafe_allow_html=True
)

# Masquer le menu et le pied de page Streamlit par défaut
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)