import pandas as pd
import numpy as np
import io
from typing import List, Dict
from pages.Dashboard import df_production, df_format

def fusionner_fichiers_excel(file_a, file_b):

    # Fusionner les DataFrames sur la colonne commune "Designation"
    df_merged = pd.merge(df_production, df_format, on="Designation", how="left", suffixes=('_B', '_A'))

    # Sélectionner uniquement les colonnes nécessaires
    columns_to_keep = [col for col in df_production] + [col for col in df_format.columns if col != "Designation"]
    df_result = df_merged[columns_to_keep]

    # Remplacer les valeurs NaN par une chaîne vide ou une valeur par défaut si nécessaire
    df_result = df_result.fillna("Non disponible")

    # Ajouter une colonne "Couverture" avec des valeurs décimales aléatoires entre 0 et 10
    df_result["Couverture"] = np.random.uniform(0, 10, size=len(df_result)).round(2)

    # Sauvegarder le résultat dans un fichier Excel en mémoire
    output = io.BytesIO()
    df_result.to_excel(output, index=False)
    output.seek(0)
    return output