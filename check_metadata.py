#!/usr/bin/env python3
import sqlite3
from pathlib import Path

def check_metadata():
    db_path = Path("src/lcpi/db/aep_prices.db")
    print(f"Vérification de la base de données: {db_path}")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Vérifier les tables existantes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    print(f"📋 Tables trouvées: {table_names}")
    
    # Vérifier si la table metadata existe
    if 'metadata' in table_names:
        print("✅ Table 'metadata' trouvée")
        cursor.execute("SELECT * FROM metadata")
        metadata_rows = cursor.fetchall()
        print(f"📊 Contenu de metadata: {metadata_rows}")
    else:
        print("❌ Table 'metadata' NON trouvée")
        print("💡 C'est pourquoi vous voyez le warning 'Table metadata non trouvée'")
    
    # Vérifier la table diameters
    if 'diameters' in table_names:
        print("✅ Table 'diameters' trouvée")
        cursor.execute("SELECT COUNT(*) FROM diameters")
        count = cursor.fetchone()[0]
        print(f"📊 Nombre de diamètres: {count}")
    else:
        print("❌ Table 'diameters' NON trouvée")
    
    conn.close()

if __name__ == "__main__":
    check_metadata()
