import streamlit as st
import usersdb


# Configuration de la page
st.set_page_config(page_title="DIGISMED", page_icon="🏠", layout="centered", initial_sidebar_state="collapsed")

# Style personnalisé pour les boutons en forme de gélule
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #617fe8;
        color: black;
        font-size: 24px;
        padding: 10px 30px;
        border: none;
        border-radius: 50px;
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        width: 300px;
        text-align: center;
    }
    .stButton > button:hover {
        background-color: #617fe8;
    }
    .css-1aumxhk {
        text-align: center;
    }
    /* Centrer le bouton */
    .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Arrière-plan avec l'image
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://sothema.com/wp-content/uploads/2015/10/bgBiotechnologies.jpg?id=2937");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }
    
    /* Cacher complètement la sidebar sur la page d'accueil */
    .css-1d391kg {
        display: none !important;
    }
    .css-6qob1r {
        display: none !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Contenu de la page d'accueil
st.markdown(
    """
    <h1 style='
        text-align: center; 
        color: black; 
        font-size: 4rem; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        margin-top: 17vh;
        margin-bottom: 8rem;
        font-weight: bold;
    '>
    Bienvenue sur DIGISMED
    </h1>
    """,
    unsafe_allow_html=True
)

# Gestion de l'état de la connexion
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

if st.button("Démarrer"):
    st.session_state.show_login = True

if st.session_state.get('show_login', False):
    # Style pour les labels du formulaire en noir
    st.markdown(
        """
        <style>
        label, .stTextInput label {
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

        if submitted:
            if username and password:
                try:
                    users = usersdb.get_users()
                    # Recherche de l'utilisateur avec une correspondance exacte (sensible à la casse)
                    user = users[(users['nom'] == username) & (users['code_secret'] == password)]
                    if not user.empty:
                        st.session_state.show_login = False
                        st.success("Connexion réussie !")
                        st.switch_page("pages/Dashboard.py")
                    else:
                        st.error("Nom d'utilisateur ou mot de passe incorrect.")
                except Exception as e:
                    st.error(f"Erreur lors de la vérification : {e}")
            else:
                st.error("Veuillez remplir tous les champs.")

# Ajout d'un espace pour centrer visuellement
st.markdown("<br><br>", unsafe_allow_html=True)