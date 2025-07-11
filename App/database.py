import streamlit as st
import pandas as pd
import io
from sqlalchemy import create_engine

# Configuration de la page
st.set_page_config(page_title="Gestion des Données avec Supabase", layout="wide")

# Connexion à Supabase via secrets
SUPABASE_URL = st.secrets["https://ycwuqibzardgeelwenyy.supabase.co"]
engine = create_engine(SUPABASE_URL)

# Initialisation de la table (si non existante, gérée par Supabase)
def init_table():
    with engine.connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS donnees (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                valeur REAL
            )
        """)
        connection.commit()

init_table()

# Sidebar pour les actions
st.sidebar.header("Gestion des Données")
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier Excel", type=["xlsx"])

# Mise à jour des données avec remplacement
if uploaded_file is not None:
    df_new = pd.read_excel(uploaded_file)
    df_new = df_new[['nom', 'valeur']].dropna()  # Ajuste selon tes colonnes
    df_new.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Données mises à jour et remplacées avec succès !")

# Option de suppression des données
if st.sidebar.button("Supprimer toutes les données"):
    df_empty = pd.DataFrame(columns=['nom', 'valeur'])
    df_empty.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Toutes les données ont été supprimées !")

# Charger les données actuelles
df_current = pd.read_sql("SELECT * FROM donnees", engine)

# Afficher les données actuelles
st.subheader("Données actuelles")
if not df_current.empty:
    st.dataframe(df_current)
else:
    st.warning("Aucune donnée chargée.")

# Téléchargement des données actuelles
if not df_current.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_current.to_excel(writer, index=False)
    st.download_button(
        label="Télécharger les données (Excel)",
        data=output.getvalue(),
        file_name="donnees_export.xlsx",
        mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Calcul
if st.button("Calculer la moyenne"):
    if not df_current.empty:
        moyenne = df_current['valeur'].mean()
        st.success(f"Moyenne des valeurs : {moyenne}")
    else:
        st.error("Aucune donnée disponible.")

# Footer
st.markdown("---")
st.markdown("*Application développée avec Streamlit* 🚀")import streamlit as st
import pandas as pd
import io
from sqlalchemy import create_engine

# Configuration de la page
st.set_page_config(page_title="Gestion des Données avec Supabase", layout="wide")

# Connexion à Supabase via secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
engine = create_engine(SUPABASE_URL)

# Initialisation de la table (si non existante, gérée par Supabase)
def init_table():
    with engine.connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS donnees (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                valeur REAL
            )
        """)
        connection.commit()

init_table()

# Sidebar pour les actions
st.sidebar.header("Gestion des Données")
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier Excel", type=["xlsx"])

# Mise à jour des données avec remplacement
if uploaded_file is not None:
    df_new = pd.read_excel(uploaded_file)
    df_new = df_new[['nom', 'valeur']].dropna()  # Ajuste selon tes colonnes
    df_new.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Données mises à jour et remplacées avec succès !")

# Option de suppression des données
if st.sidebar.button("Supprimer toutes les données"):
    df_empty = pd.DataFrame(columns=['nom', 'valeur'])
    df_empty.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Toutes les données ont été supprimées !")

# Charger les données actuelles
df_current = pd.read_sql("SELECT * FROM donnees", engine)

# Afficher les données actuelles
st.subheader("Données actuelles")
if not df_current.empty:
    st.dataframe(df_current)
else:
    st.warning("Aucune donnée chargée.")

# Téléchargement des données actuelles
if not df_current.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_current.to_excel(writer, index=False)
    st.download_button(
        label="Télécharger les données (Excel)",
        data=output.getvalue(),
        file_name="donnees_export.xlsx",
        mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Calcul
if st.button("Calculer la moyenne"):
    if not df_current.empty:
        moyenne = df_current['valeur'].mean()
        st.success(f"Moyenne des valeurs : {moyenne}")
    else:
        st.error("Aucune donnée disponible.")

# Footer
st.markdown("---")
st.markdown("*Application développée avec Streamlit* 🚀")import streamlit as st
import pandas as pd
import io
from sqlalchemy import create_engine

# Configuration de la page
st.set_page_config(page_title="Gestion des Données avec Supabase", layout="wide")

# Connexion à Supabase via secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
engine = create_engine(SUPABASE_URL)

# Initialisation de la table (si non existante, gérée par Supabase)
def init_table():
    with engine.connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS donnees (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                valeur REAL
            )
        """)
        connection.commit()

init_table()

# Sidebar pour les actions
st.sidebar.header("Gestion des Données")
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier Excel", type=["xlsx"])

# Mise à jour des données avec remplacement
if uploaded_file is not None:
    df_new = pd.read_excel(uploaded_file)
    df_new = df_new[['nom', 'valeur']].dropna()  # Ajuste selon tes colonnes
    df_new.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Données mises à jour et remplacées avec succès !")

# Option de suppression des données
if st.sidebar.button("Supprimer toutes les données"):
    df_empty = pd.DataFrame(columns=['nom', 'valeur'])
    df_empty.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Toutes les données ont été supprimées !")

# Charger les données actuelles
df_current = pd.read_sql("SELECT * FROM donnees", engine)

# Afficher les données actuelles
st.subheader("Données actuelles")
if not df_current.empty:
    st.dataframe(df_current)
else:
    st.warning("Aucune donnée chargée.")

# Téléchargement des données actuelles
if not df_current.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_current.to_excel(writer, index=False)
    st.download_button(
        label="Télécharger les données (Excel)",
        data=output.getvalue(),
        file_name="donnees_export.xlsx",
        mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Calcul
if st.button("Calculer la moyenne"):
    if not df_current.empty:
        moyenne = df_current['valeur'].mean()
        st.success(f"Moyenne des valeurs : {moyenne}")
    else:
        st.error("Aucune donnée disponible.")

# Footer
st.markdown("---")
st.markdown("*Application développée avec Streamlit* 🚀")import streamlit as st
import pandas as pd
import io
from sqlalchemy import create_engine

# Configuration de la page
st.set_page_config(page_title="Gestion des Données avec Supabase", layout="wide")

# Connexion à Supabase via secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
engine = create_engine(SUPABASE_URL)

# Initialisation de la table (si non existante, gérée par Supabase)
def init_table():
    with engine.connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS donnees (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                valeur REAL
            )
        """)
        connection.commit()

init_table()

# Sidebar pour les actions
st.sidebar.header("Gestion des Données")
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier Excel", type=["xlsx"])

# Mise à jour des données avec remplacement
if uploaded_file is not None:
    df_new = pd.read_excel(uploaded_file)
    df_new = df_new[['nom', 'valeur']].dropna()  # Ajuste selon tes colonnes
    df_new.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Données mises à jour et remplacées avec succès !")

# Option de suppression des données
if st.sidebar.button("Supprimer toutes les données"):
    df_empty = pd.DataFrame(columns=['nom', 'valeur'])
    df_empty.to_sql('donnees', engine, if_exists='replace', index=False)
    st.sidebar.success("Toutes les données ont été supprimées !")

# Charger les données actuelles
df_current = pd.read_sql("SELECT * FROM donnees", engine)

# Afficher les données actuelles
st.subheader("Données actuelles")
if not df_current.empty:
    st.dataframe(df_current)
else:
    st.warning("Aucune donnée chargée.")

# Téléchargement des données actuelles
if not df_current.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_current.to_excel(writer, index=False)
    st.download_button(
        label="Télécharger les données (Excel)",
        data=output.getvalue(),
        file_name="donnees_export.xlsx",
        mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Calcul
if st.button("Calculer la moyenne"):
    if not df_current.empty:
        moyenne = df_current['valeur'].mean()
        st.success(f"Moyenne des valeurs : {moyenne}")
    else:
        st.error("Aucune donnée disponible.")

# Footer
st.markdown("---")
st.markdown("*Application développée avec Streamlit* 🚀")