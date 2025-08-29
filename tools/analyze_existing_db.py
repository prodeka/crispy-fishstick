#!/usr/bin/env python3
"""
Script d'analyse détaillée de la base de données existante.
"""

import sqlite3
from pathlib import Path

def analyze_existing_database():
    """Analyse en détail la base de données existante."""
    
    db_path = Path("src/lcpi/db/aep_prices.db")
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 ANALYSE DÉTAILLÉE DE LA BASE DE DONNÉES EXISTANTE")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Analyser la table 'diameters'
        print(f"\n📏 ANALYSE DE LA TABLE 'diameters':")
        cursor.execute("PRAGMA table_info(diameters)")
        columns = cursor.fetchall()
        print(f"   Structure:")
        for col in columns:
            print(f"     {col[1]} ({col[2]})")
        
        cursor.execute("SELECT COUNT(*) FROM diameters")
        count = cursor.fetchone()[0]
        print(f"   Nombre d'entrées: {count}")
        
        # Afficher quelques exemples
        cursor.execute("SELECT * FROM diameters LIMIT 5")
        samples = cursor.fetchall()
        print(f"   Exemples (5 premiers):")
        for sample in samples:
            print(f"     {sample}")
        
        # Analyser la table 'accessories'
        print(f"\n🔧 ANALYSE DE LA TABLE 'accessories':")
        cursor.execute("PRAGMA table_info(accessories)")
        columns = cursor.fetchall()
        print(f"   Structure:")
        for col in columns:
            print(f"     {col[1]} ({col[2]})")
        
        cursor.execute("SELECT COUNT(*) FROM accessories")
        count = cursor.fetchone()[0]
        print(f"   Nombre d'entrées: {count}")
        
        # Afficher quelques exemples
        cursor.execute("SELECT * FROM accessories LIMIT 5")
        samples = cursor.fetchall()
        print(f"   Exemples (5 premiers):")
        for sample in samples:
            print(f"     {sample}")
        
        # Vérifier s'il y a des informations de prix dans ces tables
        print(f"\n💰 RECHERCHE D'INFORMATIONS DE PRIX:")
        
        # Chercher des colonnes contenant 'price', 'cost', 'prix', 'cout'
        cursor.execute("PRAGMA table_info(diameters)")
        diameter_columns = [col[1].lower() for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(accessories)")
        accessory_columns = [col[1].lower() for col in cursor.fetchall()]
        
        price_related_diameter = [col for col in diameter_columns if any(word in col for word in ['price', 'cost', 'prix', 'cout', 'fcfa'])]
        price_related_accessory = [col for col in accessory_columns if any(word in col for word in ['price', 'cost', 'prix', 'cout', 'fcfa'])]
        
        if price_related_diameter:
            print(f"   Colonnes liées aux prix dans 'diameters': {price_related_diameter}")
        else:
            print(f"   Aucune colonne de prix trouvée dans 'diameters'")
            
        if price_related_accessory:
            print(f"   Colonnes liées aux prix dans 'accessories': {price_related_accessory}")
        else:
            print(f"   Aucune colonne de prix trouvée dans 'accessories'")
        
        # Analyser le contenu des colonnes pour trouver des prix
        print(f"\n🔍 ANALYSE DU CONTENU:")
        
        # Vérifier la table diameters plus en détail
        if 'diameters' in [col[1] for col in cursor.execute("PRAGMA table_info(diameters)").fetchall()]:
            cursor.execute("SELECT DISTINCT diameters FROM diameters LIMIT 10")
            diameter_values = cursor.fetchall()
            print(f"   Valeurs de diamètres disponibles: {[d[0] for d in diameter_values]}")
        
        # Chercher des colonnes numériques qui pourraient contenir des prix
        cursor.execute("PRAGMA table_info(diameters)")
        numeric_columns = []
        for col in cursor.fetchall():
            if 'real' in col[2].lower() or 'int' in col[2].lower():
                numeric_columns.append(col[1])
        
        if numeric_columns:
            print(f"   Colonnes numériques dans 'diameters': {numeric_columns}")
            
            # Analyser le contenu de ces colonnes
            for col in numeric_columns[:3]:  # Limiter à 3 colonnes
                cursor.execute(f"SELECT DISTINCT {col} FROM diameters WHERE {col} IS NOT NULL LIMIT 5")
                values = cursor.fetchall()
                print(f"     {col}: {[v[0] for v in values]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

def suggest_adaptation():
    """Suggère comment adapter le solveur LCPI à la base existante."""
    
    print(f"\n🎯 SUGGESTIONS D'ADAPTATION:")
    print("=" * 40)
    
    print(f"1. 📊 ANALYSE DE LA SITUATION:")
    print(f"   - Base de données existante: 192 KB")
    print(f"   - Tables disponibles: diameters, accessories")
    print(f"   - Problème: Pas de table 'prices' standard")
    
    print(f"\n2. 🔧 SOLUTIONS POSSIBLES:")
    print(f"   A) Adapter le code pour utiliser la table 'diameters' existante")
    print(f"   B) Créer une vue SQL qui simule la table 'prices'")
    print(f"   C) Modifier le solveur pour lire depuis les tables existantes")
    
    print(f"\n3. 💡 RECOMMANDATION:")
    print(f"   Utiliser la solution A: Adapter le code LCPI pour lire")
    print(f"   directement depuis la table 'diameters' existante")
    
    print(f"\n4. 📝 PLAN D'ACTION:")
    print(f"   - Analyser la structure exacte de 'diameters'")
    print(f"   - Identifier les colonnes contenant les prix")
    print(f"   - Modifier le code de calcul des coûts")
    print(f"   - Tester avec la base existante")

if __name__ == "__main__":
    analyze_existing_database()
    suggest_adaptation()
