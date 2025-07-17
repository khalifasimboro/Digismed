import pandas as pd
import numpy as np
import streamlit as st
from typing import List, Dict, Optional

####Fonctions de calcul et d'optimisation

# Colonnes de format à prendre en compte (toutes sauf "Couverture" et colonnes non numériques si présentes)
format_columns = [
    "Type Blister", "Dim blister", "Nbre d'unité / blstr", "Réf format",
    "Réf formage", "Réf Souflage", "Réf Alimentation Auto", "Réf scellage Sup",
    "Réf scellage inf", "Réf Refroidissement"
]

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
    return None