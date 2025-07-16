import pandas as pd
import numpy as np





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