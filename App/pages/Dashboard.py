# # Import des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(
    page_title="Dashboard de contrôle",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour styliser la sidebar et le contenu principal
st.markdown("""
<style>
    /* Sidebar styling - Fond bleu foncé brillant */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
    }
    /* Sidebar text color - Blanc pour contraste */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Button styling - Ajusté pour s'intégrer au bleu foncé */
    .stButton > button {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
        width: 100% !important;
        padding: 15px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin: 10px 0 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.2) !important;
        border-color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    /* Main content area - Fond bleu clair personnalisé */
    .main .block-container {
        background: #aaddf5 !important;
        background-image: 
            linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%),
            linear-gradient(-45deg, rgba(255,255,255,0.3) 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, rgba(255,255,255,0.3) 75%),
            linear-gradient(-45deg, transparent 75%, rgba(255,255,255,0.3) 75%);
        background-size: 30px 30px;
        background-position: 0 0, 0 15px, 15px -15px, -15px 0px;
        padding-top: 2rem;
        max-width: 100%;
    }
    /* Card styling - Fond blanc pour contraste */
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    /* Page title - Bleu foncé pour harmonie */
    .page-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar avec navigation
with st.sidebar:
    # Titre de la sidebar
    st.markdown("# 🏠 Menu de Navigation")
    
    # Menu hamburger (décoratif)
    st.markdown("---")
    
    # Boutons de navigation avec émojis
    machine_options = ["Marchesini", "Noack", "Hoonga", "Romaco"]
    selected_machine = st.selectbox("⚙️ Machines", options=[""] + machine_options, key="machines_select")
    page_home = st.button("🏠 Home", key="home") 
    page_users = st.button("👥 Users", key="users")
    page_databases = st.button("🗄️ Bases de données", key="databases")
    page_help = st.button("❓ Aide", key="help")

# Gestion de l'état de la page
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Navigation logic
if page_home:
    st.session_state.current_page = 'home'
elif page_users:
    st.session_state.current_page = 'users'
elif page_databases:
    st.session_state.current_page = 'databases'
elif page_help:
    st.session_state.current_page = 'help'

# Barre de recherche en haut

# Contenu principal basé sur la page sélectionnée

if st.session_state.current_page == 'home':

    # Affichage du contenu selon la machine sélectionnée
    if selected_machine == "Marchesini":
        # Trois barres symétriques pour les métriques Marchesini avec fond bleu et taille uniforme
        metric_card_style = """
            background: linear-gradient(135deg, #3B82F6 60%, #1E3A8A 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 1rem 1rem;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        """
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Fréquence changement format global</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Temps total de changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Suivi changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        # Ajoutez ici des métriques ou du contenu spécifique à Marchesini
    elif selected_machine == "Noack":
         # Trois barres symétriques pour les métriques Marchesini avec fond bleu et taille uniforme
        metric_card_style = """
            background: linear-gradient(135deg, #3B82F6 60%, #1E3A8A 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 1rem 1rem;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        """
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Fréquence changement format global</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Temps total de changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Suivi changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        # Ajoutez ici des métriques ou du contenu spécifique à Noack
    elif selected_machine == "Hoonga":
         # Trois barres symétriques pour les métriques Hoonga avec fond bleu et taille uniforme
        metric_card_style = """
            background: linear-gradient(135deg, #3B82F6 60%, #1E3A8A 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 1rem 1rem;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        """
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Fréquence changement format global</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Temps total de changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Suivi changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        # Ajoutez ici des métriques ou du contenu spécifique à Hoonga
    elif selected_machine == "Romaco":
         # Trois barres symétriques pour les métriques Romaco avec fond bleu et taille uniforme
        metric_card_style = """
            background: linear-gradient(135deg, #3B82F6 60%, #1E3A8A 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 1rem 1rem;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        """
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Fréquence changement format global</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Temps total de changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">Suivi changement de format</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">--</div>
            </div>
            """, unsafe_allow_html=True)
        # Ajoutez ici des métriques ou du contenu spécifique à Romaco
    else:
        st.markdown("""
        <div class="content-card">
            <h3>👋 Bienvenue dans votre application</h3>
            <p>Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.</p>
        </div>
        """, unsafe_allow_html=True)


elif st.session_state.current_page == 'users':
    st.markdown('<div class="page-title">👥 Gestion des Utilisateurs</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="content-card">
        <h3>👤 Liste des utilisateurs</h3>
        <p>Gérez les comptes utilisateurs et leurs permissions.</p>
    </div>
    """, unsafe_allow_html=True)

    # Tableau fictif des utilisateurs
    users_data = {
        'Nom': ['Alice Martin', 'Bob Dupont', 'Claire Moreau', 'David Bernard'],
        'Email': ['alice@example.com', 'bob@example.com', 'claire@example.com', 'david@example.com'],
        'Rôle': ['Admin', 'Utilisateur', 'Moderateur', 'Utilisateur'],
        'Statut': ['Actif', 'Actif', 'Inactif', 'Actif']
    }
    df_users = pd.DataFrame(users_data)
    st.dataframe(df_users, use_container_width=True)

elif st.session_state.current_page == 'databases':

    st.markdown("""
    <div class="content-card" style="
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    ">
        <h3>🗄️ Bases de Données</h3>
        <p>Intégrez, surveillez et gérez vos bases de données.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Liste des bases de données
    dbs = [
        ("📁 Données format", "format"),
        ("🗃️ Données SMED MARCHESINI", "marchesini"),
        ("🗄️ Données SMED NOACK", "noack"),
        ("📦 Données SMED HOONGA", "hoonga"),
        ("📦 Données SMED ROMACO", "romaco"),
        ("🛠️ Données produits/équipements", "produits_equipements"),
    ]

    # Stockage des dataframes en session_state
    if 'db_data' not in st.session_state:
        st.session_state.db_data = {}

    # Charger le fichier Formats.xlsx au besoin
    def load_formats():
        if 'format' not in st.session_state.db_data:
            try:
                df = pd.read_excel("Assets/donnees/Formats.xlsx", engine='openpyxl')
                st.session_state.db_data['format'] = df
            except Exception as e:
                st.session_state.db_data['format'] = None
                st.error(f"Erreur lors du chargement de Formats.xlsx : {e}")

    # Ajout de style CSS pour ajuster la largeur et l'espacement vertical des boutons
    st.markdown("""
    <style>
    .custom-db-btn > button {
        width: 90% !important;
        margin-top: 80px !important;
        margin-bottom: 50px !important;
        min-width: 200px;
        max-width: 300px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Répartition en deux colonnes (3 à gauche, 3 à droite)
    col_gauche, col_droite = st.columns(2)
    for idx, (label, key) in enumerate(dbs):
        target_col = col_gauche if idx < 3 else col_droite
        with target_col:
            if st.button(label, key=f"dbbtn_{key}", help=None, type="secondary", use_container_width=False):
                with st.expander(f"{label} - Actions rapides"):
                    col_v, col_i, col_e = st.columns(3)
                    with col_v:
                        if st.button("👁️ Voir", key=f"voir_{key}"):
                            if key == "format":
                                load_formats()
                                df = st.session_state.db_data.get('format')
                                if df is not None:
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.warning("Aucune donnée à afficher pour Formats.xlsx.")
                            else:
                                st.info(f"Affichage de {label} (fonctionnalité à venir)")
                    with col_i:
                        uploaded_file = st.file_uploader(
                            "Sélectionnez un fichier Excel à importer",
                            type=["xlsx"],
                            key=f"import_uploader_{key}",
                            label_visibility="collapsed"
                        )
                        if uploaded_file is not None:
                            save_dir = "Assets/donnees"
                            os.makedirs(save_dir, exist_ok=True)
                            save_path = os.path.join(save_dir, uploaded_file.name)
                            with open(save_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            st.success(f"Fichier '{uploaded_file.name}' importé et sauvegardé dans '{save_dir}'.")
                    with col_e:
                        if st.button("⬇️ Exporter", key=f"export_{key}"):
                            st.info(f"Export de {label} (fonctionnalité à venir)")
            st.markdown('<div class="custom-db-btn"></div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'help':
     
    st.markdown("""
    <div class="content-card">
        <h3>❓ Aide</h3>
        <p>Prenez l'application en main pour une meilleure navigabilité.</p>
    </div>
    """, unsafe_allow_html=True)

      # Menu hamburger (décoratif)
    st.markdown("---")


# Footer
st.markdown("---")
st.markdown("*Application développée avec Streamlit* 🚀")