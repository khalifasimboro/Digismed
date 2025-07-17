import pandas as pd
import numpy as np
from typing import List, Dict
from pages.Dashboard import df_production, df_format


 
def fusionner_fichiers_excel():
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
    return df_result