import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict
from fusionner_fichier_fp import fusionner_fichiers_excel

#Fichier de sortie pour les données fusionnées
df_result = fusionner_fichiers_excel()

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


if "Machines" not in df_result.columns:
    st.write("❌ Colonne 'Machines' manquante dans df_result")
else:
    # Grouper par machine et optimiser l'ordre
    machines = df_result["Machines"].unique()
    optimized_orders = {}
    for machine in machines:
        machine_df = df_result[df_result["Machines"] == machine].copy()
        optimized_orders[machine] = optimize_fabrication_order(machine_df)
    
    # Afficher les résultats
    for machine, order in optimized_orders.items():
        st.write(f"Machine {machine}: {', '.join(order)}")