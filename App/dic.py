import streamlit as st
import pandas as pd
import os
from typing import List, Dict
from sqlalchemy import create_engine,text
from functions import upload_and_optimize, calculer_changements_formats
import usersdb

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
    machine_options = ["MARCHESINI", "NOACK", "HOONGA", "ROMACO"]
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

temps_standard = {
        "MARCHESINI": 12.0,  # 5 minutes par changement
        "NOACK": 10.0,   # 3 minutes par changement
        "HOONGA": 5.0,  # 5 minutes par changement
        "ROMACO": 2.0   # 3 minutes par changement
    }

#Fonction de création et affichage des métrics
def create_machine_metrics(values: List[str] = None):
    """
    Crée les cartes de métriques pour toutes les machines
    
    Args:
        machine_name (str): Nom de la machine pour personnalisation
        values (list): Valeurs réelles à afficher (optionnel)
    """
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
    
    # Définition des métriques
    metrics = [
        "Fréquence changement format global",
        "Temps total de changement de format"
    ]

    # Valeurs par défaut ou personnalisées
    if values is None:
        values = ["--","--"]
    
    # Création des colonnes
    col_a, col_b = st.columns(2)
    columns = [col_a, col_b]
    
    # Génération des cartes
    for col, metric, values in zip(columns, metrics, values):
        with col:
            st.markdown(f"""
            <div class="content-card" style="{metric_card_style}">
            <h4 style="color:white;">{metric}</h4>
            <div style="font-size:2rem; color:white; font-weight:bold;">{values}</div>
            </div>
            """, unsafe_allow_html=True)


#fonction pour afficher les données de la machine sélectionnée
def afficher_resultats(optimized_orders: Dict[str, List[str]]):
    """Affiche les résultats d'optimisation pour une machine sélectionnée"""
    if not optimized_orders:
        st.write("❌ Aucun résultat d'optimisation disponible")
        return
    keys = list(optimized_orders.keys())
    # Afficher les résultats pour la machine sélectionnée
    if selected_machine in optimized_orders:
        order = optimized_orders[selected_machine]
        data = {"Classement": range(1, len(order) + 1), "Produits": order}
        st.write(f"Classement des ordres de conditionnement pour la {selected_machine}")
        df_display = pd.DataFrame(data)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        st.write(optimized_orders)
    else:
        st.write(optimized_orders)
        #st.write(f"❌ Aucune donnée pour la machine {selected_machine}")


# Contenu principal basé sur la page sélectionnée
if st.session_state.current_page == 'home':
        
        if selected_machine in ["MARCHESINI", "NOACK", "HOONGA", "ROMACO"]:
            # Ajoutez ici des métriques ou du contenu spécifique à chaque machine si nécessaire
            # Contenu spécifique à Marchesini
            if selected_machine == "MARCHESINI":
                optimized_orders = upload_and_optimize()
                resultats = calculer_changements_formats(temps_standard)
                values = resultats["MARCHESINI"]
                create_machine_metrics(values)
                if optimized_orders:
                   afficher_resultats(optimized_orders)

            # Contenu spécifique à Noack
            elif selected_machine == "NOACK":
                optimized_orders = upload_and_optimize()
                resultats = calculer_changements_formats(temps_standard)
                values = resultats["MARCHESINI"]
                create_machine_metrics(values)
                if optimized_orders:
                   afficher_resultats(optimized_orders)
            # Contenu spécifique à Hoonga
            elif selected_machine == "HOONGA":
                optimized_orders = upload_and_optimize()
                resultats = calculer_changements_formats(temps_standard)
                values = resultats["MARCHESINI"]
                create_machine_metrics(values)
                if optimized_orders:
                   afficher_resultats(optimized_orders)
            # Contenu spécifique à Romaco
            elif selected_machine == "ROMACO":
                optimized_orders = upload_and_optimize()
                resultats = calculer_changements_formats(temps_standard)
                values = resultats["MARCHESINI"]
                create_machine_metrics(values)
                if optimized_orders:
                   afficher_resultats(optimized_orders)
        else:
             # Contenu centré
            st.markdown(
                """
                <style>
                .centered-content {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 80vh; /* Réduit la hauteur minimale pour remonter */
                    width: 100%;
                    flex-direction: column;
                    text-align: center;
                    margin-top: -10vh; /* Ajuste cette valeur pour remonter davantage si besoin */
                }
                .content-card {
                    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                    color: white;
                    padding: 2rem;
                    border-radius: 15px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    max-width: 80%;
                    margin: 0 auto;
                }
                </style>
                <div class="centered-content">
                    <div class="content-card">
                        <h3>👋 Bienvenue sur votre Dashboard de controle</h3>
                        <p>Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


elif st.session_state.current_page == 'users':
    st.markdown("""
    <div class="content-card" style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white;">
        <h3>👤 Liste des utilisateurs</h3>
        <p>Gérez les comptes utilisateurs et leurs codes secrets.</p>
    </div>
    """, unsafe_allow_html=True)

    # Importer la base de données des utilisateurs
    try:
        df_users = usersdb.get_users()
        if not df_users.empty:
            st.dataframe(df_users, use_container_width=True, hide_index=True)
        else:
            st.warning("Aucun utilisateur trouvé.")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des utilisateurs : {e}")
        st.stop()

    # Formulaire pour ajouter un utilisateur
    st.markdown("---")
    st.subheader("Ajouter un utilisateur")
    with st.form(key="add_user_form"):
        nom = st.text_input("Nom")
        code_secret = st.text_input("Code secret", type="password")  # Masque le mot de passe
        submit_button = st.form_submit_button(label="Ajouter")

        if submit_button:
            if nom and code_secret:
                try:
                    usersdb.add_user(nom, code_secret)
                    st.success("Utilisateur ajouté avec succès !")
                    st.write(f"[DEBUG] Ajouté : {nom}, {code_secret}")
                    st.rerun()  # Rafraîchir la page
                except ValueError as e:
                    st.error(str(e))
            else:
                st.error("Veuillez remplir tous les champs.")

    # Section pour supprimer un utilisateur
    st.markdown("---")
    st.subheader("Supprimer un utilisateur")
    if not df_users.empty:
        user_id = st.selectbox("Sélectionner un utilisateur à supprimer", options=df_users['id'].tolist())
        if st.button("Supprimer"):
            try:
                usersdb.delete_user(user_id)
                st.success(f"Utilisateur avec ID {user_id} supprimé avec succès !")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
    else:
        st.warning("Aucun utilisateur à supprimer.")

elif st.session_state.current_page == 'databases':
    # Connexion à Supabase avec gestion d'erreur détaillée
    try:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        engine = create_engine(SUPABASE_URL)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        st.success("Connexion à Supabase réussie.")
    except KeyError:
        st.error("Le fichier secrets.toml est manquant ou mal configuré. Vérifiez .streamlit/secrets.toml ou les secrets sur SCC.")
        st.stop()
    except Exception as e:
        st.error(f"[ERROR] Erreur de connexion à Supabase : {e}")
        st.write(f"[DEBUG] Détails : {str(e)}")
        st.stop()

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

    # Liste des bases de données avec mappage vers les tables Supabase
    dbs = [
        ("📁 Données format", "format"),
        ("🗃️ Données SMED MARCHESINI", "marchesini"),
        ("🗄️ Données SMED NOACK", "noack"),
        ("📦 Données SMED HOONGA", "hoonga"),
        ("📦 Données SMED ROMACO", "romaco"),
        ("🛠️ Données produits/équipements", "produits_equipements"),
    ]
    table_mapping = {
        "format": "Format_database",
        "marchesini": "Marchesini_database",
        "noack": "Noack_database",
        "hoonga": "Hoonga_database",
        "romaco": "Romaco_database",
        "produits_equipements": "Produits_equipements_database",
    }

    # Stockage des dataframes en session_state
    if 'db_data' not in st.session_state:
        st.session_state.db_data = {}

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
                st.write(f"[DEBUG] Bouton {label} cliqué, clé : {key}")
                with st.expander(f"{label} - Actions rapides", expanded=True):
                    col_v, col_i, col_e = st.columns([2, 1, 1])
                    with col_v:
                        if st.button("👁️ Voir", key=f"voir_{key}"):
                            st.write(f"[DEBUG] Bouton Voir cliqué pour {label}, clé : {key}")
                            table_name = table_mapping.get(key)
                            if table_name:
                                try:
                                    st.write(f"[DEBUG] Tentative de lecture de {table_name}")
                                    df = pd.read_sql(text(f"SELECT * FROM {table_name}"), engine)
                                    st.write(f"[DEBUG] Requête exécutée. Nombre de lignes : {len(df)}")
                                    if not df.empty:
                                        st.session_state.db_data[key] = df
                                        st.write("[DEBUG] Aperçu des données :", df.head())
                                        st.container()
                                        st.dataframe(df, use_container_width=True)
                                        st.write("[DEBUG] Données stockées :", st.session_state.db_data[key])
                                    else:
                                        st.warning(f"Aucune donnée dans {table_name}. Vérifiez Supabase.")
                                        st.container()
                                        st.write("[DEBUG] Aucun tableau à afficher.")
                                except Exception as e:
                                    st.error(f"[ERROR] Erreur lors de la lecture de {table_name} : {e}")
                                    st.write(f"[DEBUG] Détails : {str(e)}")
                            else:
                                st.info(f"Affichage de {label} (table non configurée)")
                    with col_i:
                        uploaded_file = st.file_uploader(
                            "Sélectionnez un fichier Excel à importer",
                            type=["xlsx"],
                            key=f"import_uploader_{key}",
                            label_visibility="collapsed"
                        )
                        if uploaded_file is not None:
                            table_name = table_mapping.get(key)
                            if table_name:
                                try:
                                    st.write(f"Importation dans {table_name}...")
                                    df_new = pd.read_excel(uploaded_file)
                                    df_new.to_sql(table_name, engine, if_exists='replace', index=False)
                                    st.success(f"Données importées avec succès dans {table_name}.")
                                except Exception as e:
                                    st.error(f"Erreur lors de l'import dans {table_name} : {e}")
                            else:
                                st.warning(f"Import non disponible pour {label}.")
                    with col_e:
                        if st.button("⬇️ Exporter", key=f"export_{key}"):
                            df = st.session_state.db_data.get(key)
                            table_name = table_mapping.get(key)
                            if df is not None and table_name:
                                try:
                                    st.write(f"Exportation de {table_name}...")
                                    csv_path = os.path.join("Assets", f"{table_name}_export.csv")
                                    df.to_csv(csv_path, index=False)
                                    st.success(f"Données exportées dans '{csv_path}'.")
                                    csv_data = df.to_csv(index=False).encode('utf-8')
                                    st.download_button(
                                        label="Télécharger le CSV",
                                        data=csv_data,
                                        file_name=f"{table_name}_export.csv",
                                        mime_type="text/csv"
                                    )
                                except Exception as e:
                                    st.error(f"Erreur lors de l'export de {table_name} : {e}")
                            else:
                                st.warning(f"Aucune donnée à exporter pour {table_name}.")
            st.markdown('<div class="custom-db-btn"></div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'help':
    # Chemin absolu du fichier d'aide
    aide_path = "aide.txt"
    try:
        with open(aide_path, "r", encoding="utf-8") as f:
            aide_content = f.read()
    except Exception as e:
        aide_content = f"Impossible de charger le fichier d'aide : {e}"

    st.markdown("""
    <div class="content-card" style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white;">
        <h3>❓ Aide</h3>
    <p>Prenez votre application en main.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(aide_content)



















import pandas as pd
import numpy as np
import streamlit as st
from typing import List, Dict,Optional


# Colonnes de format à prendre en compte (toutes sauf "Couverture" et colonnes non numériques si présentes)
format_columns = [
    "Type Blister", "Dim blister", "Nbre d'unité / blstr", "Réf format",
    "Réf formage", "Réf Souflage", "Réf Alimentation Auto", "Réf scellage Sup",
    "Réf scellage inf", "Réf Refroidissement"
]

#Fonctions de calcul et d'optimisation 

# Fonction pour parser et normaliser les valeurs (remplace "Non disponible" par 0)
def normalize_value(value):
    if pd.isna(value) or value == "Non disponible":
        return 0
    try:
        return float(str(value).replace("cm", "").strip()) if isinstance(value, str) else float(value)
    except:
        return 0

# Calculer la différence de format entre deux produits (distance euclidienne)
def format_difference(row1: pd.Series, row2: pd.Series) -> float:
    diff_sum = 0
    for col in format_columns:
        val1 = normalize_value(row1[col])
        val2 = normalize_value(row2[col])
        diff_sum += (val1 - val2) ** 2
    return np.sqrt(diff_sum)

# Algorithme d'optimisation
def optimize_fabrication_order(machine_df: pd.DataFrame) -> List[str]:    
    if machine_df.empty:
        return []

    # Trier initialement par couverture (priorité faible -> haut)
    sorted_df = machine_df.sort_values(by="Couverture")
    
    # Liste des designations ordonnées
    order = [sorted_df.iloc[0]["Designation"]]  # Premier produit
    remaining = sorted_df.iloc[1:].index.tolist()
    
    while remaining:
        # Sélectionner la ligne courante par Designation
        current_row = sorted_df[sorted_df["Designation"] == order[-1]].iloc[0]
        min_diff = float('inf')
        next_product = None
        
        # Trouver le produit suivant avec la plus petite différence de format
        for idx in remaining:
            next_row = sorted_df.loc[idx]
            diff = format_difference(current_row, next_row)
            if diff < min_diff:
                min_diff = diff
                next_product = idx
        
        order.append(sorted_df.loc[next_product, "Designation"])
        remaining.remove(next_product)
    
    return order

def optimiser_ordre_fabrication(df_result: pd.DataFrame) -> Dict[str, List[str]]:
    """Optimise l'ordre de fabrication par machine (sans affichage)"""
    if "Machines" not in df_result.columns:
        return {}
    
    machines = df_result["Machines"].unique()
    optimized_orders = {}
    
    for machine in machines:
        machine_df = df_result[df_result["Machines"] == machine].copy()
        optimized_orders[machine] = optimize_fabrication_order(machine_df)
    
    return optimized_orders


def upload_and_optimize() -> Optional[Dict[str, List[str]]]:
    """
    Gère l'upload des fichiers et retourne les ordres optimisés
    
    Returns:
        Optional[Dict[str, List[str]]]: Ordres optimisés par machine (None si pas de fichiers ou erreur)
    """
    
    # Interface d'upload
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_format = st.file_uploader(
            "Charger le fichier Format",
            type=["xlsx", "csv"],
            key="format_upload"
        )
    
    with col2:
        uploaded_production = st.file_uploader(
            "Charger le fichier Plan de production",
            type=["xlsx", "csv"],
            key="production_upload"
        )
    
    # Initialisation des variables
    df_format, df_production = None, None
    
    # Traitement du fichier Format
    if uploaded_format is not None:
        try:
            if uploaded_format.name.endswith('.csv'):
                df_format = pd.read_csv(uploaded_format)
            else:
                df_format = pd.read_excel(uploaded_format)
            st.success("Fichier Format chargé avec succès.")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier Format : {e}")
            return None
        
        st.markdown("---")
        st.write("Aperçu du fichier Format :")
        st.dataframe(df_format.head())
    
    # Traitement du fichier Plan de production
    if uploaded_production is not None:
        try:
            if uploaded_production.name.endswith('.csv'):
                df_production = pd.read_csv(uploaded_production)
            else:
                df_production = pd.read_excel(uploaded_production)
            st.success("Fichier Plan de production chargé avec succès.")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier Plan de production : {e}")
            return None
        
        st.markdown("---")
        st.write("Aperçu du fichier Plan de production :")
        st.dataframe(df_production.head())
        st.markdown("---")
    
    # Vérification des données chargées
    if df_format is not None and df_production is not None:
        try:
            output_file_path = "/home/falleiz/Bureau/Digismed/Assets/donnees/test1.xlsx"
            # Fusionner les DataFrames sur la colonne commune "Designation"
            df_merged = pd.merge(df_production, df_format, on="Designation", how="left", suffixes=('_prod', '_format'))

            # Sélectionner uniquement les colonnes nécessaires
            columns_to_keep = [col for col in df_production.columns] + [col for col in df_format.columns if col != "Designation"]
            df_result = df_merged[columns_to_keep]

            # Remplacer les valeurs NaN par une chaîne vide ou une valeur par défaut si nécessaire
            df_result = df_result.fillna("Non disponible")

            # Ajouter une colonne "Couverture" avec des valeurs décimales aléatoires entre 0 et 10
            df_result["Couverture"] = np.random.uniform(0, 10, size=len(df_result)).round(2)

            # Sauvegarder le résultat dans un nouveau fichier Excel
            df_result.to_excel(output_file_path, index=False)
            # Utilisation
            optimized_orders = optimiser_ordre_fabrication(df_result)
            
            return optimized_orders
            
            
        except Exception as e:
            st.error(f"Erreur lors du traitement des données : {e}")
            return None
    
    # Retour None si les fichiers ne sont pas encore chargés
    #return None