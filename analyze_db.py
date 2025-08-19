#!/usr/bin/env python3
"""
Analyse de la base de données des prix AEP
"""

import sqlite3
from pathlib import Path

def analyze_database():
    """Analyse la structure et le contenu de la base de données"""
    db_path = Path("src/lcpi/db/aep_prices.db")
    
    if not db_path.exists():
        print(f"❌ Base de données introuvable: {db_path}")
        return
    
    print("🔍 Analyse de la base de données des prix AEP")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Lister les tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        
        print(f"📊 Tables trouvées: {len(tables)}")
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            
            # Structure de la table
            cur.execute(f"PRAGMA table_info({table_name})")
            columns = cur.fetchall()
            print(f"  Colonnes ({len(columns)}):")
            for col in columns:
                print(f"    - {col[1]} ({col[2]})")
            
            # Nombre de lignes
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"  Lignes: {count}")
            
            # Échantillon de données
            cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample = cur.fetchall()
            print(f"  Échantillon:")
            for row in sample:
                print(f"    {row}")
        
        conn.close()
        print("\n✅ Analyse terminée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_database()
