import sqlite3
import os
import sys

# Ajoute la racine du projet au path pour permettre les imports relatifs
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

def create_db_indexes(db_path: str):
    """Crée les index recommandés sur la base de données aep_prices.db."""
    if not os.path.exists(db_path):
        print(f"Erreur : Le fichier de base de données n'a pas été trouvé à '{db_path}'")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Création de l'index sur 'diameters(dn_mm, material)'...")
        # L'index sera créé seulement s'il n'existe pas déjà
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_diameters_dn_material ON diameters (dn_mm, material);")
        
        conn.commit()
        conn.close()
        print("Index créé ou déjà existant. Opération terminée.")
        
    except sqlite3.Error as e:
        print(f"Une erreur SQLite est survenue : {e}")

if __name__ == '__main__':
    # Utilise la classe PriceDB pour trouver le chemin de la DB par défaut de manière fiable
    try:
        from src.lcpi.aep.optimizer.db import PriceDB
        default_db_path = PriceDB().db_path
        if default_db_path:
            print(f"Base de données détectée à : {default_db_path}")
            create_db_indexes(default_db_path)
        else:
            print("Base de données par défaut non trouvée. Spécifiez le chemin manuellement.")
    except ImportError:
        print("Impossible d'importer PriceDB. Assurez-vous que le script est lancé depuis la racine du projet.")
        print("Exemple: python tools/database/create_indexes.py")
