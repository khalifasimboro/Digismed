import pandas as pd
import numpy as np
from typing import List, Dict

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