import sqlite3
import pandas as pd
from pathlib import Path

# Chemin de la base de données (fichier SQLite local)
DB_PATH = Path(__file__).parent / "users.db"

def init_db():
    """Initialise la base de données SQLite si elle n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            code_secret TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_users():
    """Récupère tous les utilisateurs depuis la base de données."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

def add_user(nom, code_secret):
    """Ajoute un nouvel utilisateur à la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (nom, code_secret) VALUES (?, ?)",
            (nom, code_secret)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Erreur lors de l'ajout.")
    finally:
        conn.close()

def delete_user(user_id):
    """Supprime un utilisateur de la base de données en fonction de son ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Utilisateur non trouvé.")
    finally:
        conn.close()

# Initialisation de la base de données au premier import
init_db()

# Exemple : Ajouter des utilisateurs de test (à commenter ou supprimer après usage)
if __name__ == "__main__":
    add_user("reda", "123")
    add_user("rydouane", "456")
    add_user("abou", "789")