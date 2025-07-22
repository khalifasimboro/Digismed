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


def optimize(df_format,df_production):
    """
    Gère l'upload des fichiers et retourne les ordres optimisés
    
    Returns:
        Optional[Dict[str, List[str]]]: Ordres optimisés par machine (None si pas de fichiers ou erreur)
    """
    resultats = {}
    temps_standard = {
        "MARCHESINI": 5.0,  # Temps standard pour Machine A
        "NOACK": 3.0,  # Temps standard pour Machine B  
        "HOONGA": 4.0,  # Temps standard pour Machine C
        "ROMACO": 5.0   # Temps standard pour Machine C
    }

    # Vérification des données chargées
    if df_format is not None and df_production is not None:

        try:
            # Chemin de sortie pour le fichier Excel
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
            

            for machine, order in optimized_orders.items():
                if not order:  # Si la liste est vide
                    resultats[machine] = (0, 0.0)
                    continue
                
                # Compter les changements de format
                changements = 0
                for i in range(1, len(order)):
                    if order[i] != order[i-1]:  # Changement si produits différents
                        changements += 1
                
                # Temps total (nombre de changements * temps standard de la machine)
                temps_std = temps_standard.get(machine, 0.0)  # Utilise 0 si la machine n'est pas dans temps_standard
                temps_total = changements * temps_std
                
                resultats[machine] = (changements, temps_total)
    
            return optimized_orders, resultats
            
            
        except Exception as e:
            st.error(f"Erreur lors du traitement des données : {e}")
            return None