#!/usr/bin/env python3
"""
Script pour ajouter la table metadata manquante à aep_prices.db
"""
import sqlite3
from pathlib import Path
from datetime import datetime

def fix_metadata_table():
    db_path = Path("src/lcpi/db/aep_prices.db")
    print(f"🔧 Réparation de la base de données: {db_path}")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table metadata existe déjà
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'")
        if cursor.fetchone():
            print("✅ Table 'metadata' existe déjà")
            return True
        
        # Créer la table metadata
        print("📝 Création de la table 'metadata'...")
        cursor.execute("""
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insérer les métadonnées de base
        metadata_values = [
            ("db_version", "1.0.0"),
            ("created_at", datetime.now().isoformat()),
            ("description", "Base de données des prix AEP - LCPI"),
            ("last_updated", datetime.now().isoformat())
        ]
        
        cursor.executemany("INSERT INTO metadata (key, value) VALUES (?, ?)", metadata_values)
        
        conn.commit()
        print("✅ Table 'metadata' créée avec succès")
        
        # Vérifier le contenu
        cursor.execute("SELECT * FROM metadata")
        rows = cursor.fetchall()
        print(f"📊 Métadonnées insérées: {rows}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la réparation: {e}")
        return False

if __name__ == "__main__":
    success = fix_metadata_table()
    if success:
        print("\n🎉 Réparation terminée ! Le warning 'Table metadata non trouvée' ne devrait plus apparaître.")
    else:
        print("\n💥 Échec de la réparation.")
