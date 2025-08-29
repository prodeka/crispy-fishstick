#!/usr/bin/env python3
"""
Script de vérification de la base de données des prix AEP.
"""

import sqlite3
import os
from pathlib import Path

def check_price_database():
    """Vérifie la base de données des prix AEP."""
    
    db_path = Path("src/lcpi/db/aep_prices.db")
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 Vérification de la base de données: {db_path}")
    print(f"📁 Taille du fichier: {db_path.stat().st_size / 1024:.1f} KB")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lister les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\n📊 Tables trouvées: {[t[0] for t in tables]}")
        
        # Vérifier la table prices
        if ('prices',) in tables:
            cursor.execute("SELECT COUNT(*) FROM prices")
            count = cursor.fetchone()[0]
            print(f"📈 Nombre d'entrées dans 'prices': {count}")
            
            if count > 0:
                # Afficher quelques exemples de prix
                cursor.execute("SELECT * FROM prices LIMIT 5")
                sample_prices = cursor.fetchall()
                print(f"\n💰 Exemples de prix (5 premiers):")
                for price in sample_prices:
                    print(f"   {price}")
                
                # Vérifier la structure de la table
                cursor.execute("PRAGMA table_info(prices)")
                columns = cursor.fetchall()
                print(f"\n🏗️ Structure de la table 'prices':")
                for col in columns:
                    print(f"   {col[1]} ({col[2]})")
                
                # Vérifier les diamètres disponibles
                cursor.execute("SELECT DISTINCT diameter_mm FROM prices ORDER BY diameter_mm")
                diameters = cursor.fetchall()
                print(f"\n📏 Diamètres disponibles: {[d[0] for d in diameters]}")
                
                # Vérifier les prix par diamètre
                print(f"\n💵 Prix par diamètre:")
                for diameter in diameters[:10]:  # Limiter à 10 pour éviter le spam
                    cursor.execute("SELECT price_fcfa_per_m FROM prices WHERE diameter_mm = ? LIMIT 1", (diameter[0],))
                    price = cursor.fetchone()
                    if price:
                        print(f"   {diameter[0]} mm: {price[0]} FCFA/m")
                
            else:
                print("❌ Table 'prices' vide!")
        
        # Vérifier d'autres tables potentielles
        for table in tables:
            if table[0] != 'prices':
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"📊 Table '{table[0]}': {count} entrées")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'accès à la base de données: {e}")

def check_network_diameters():
    """Vérifie les diamètres du réseau optimisé."""
    
    print(f"\n🔍 Vérification des diamètres du réseau optimisé...")
    
    # Lire le fichier de résultats
    result_file = "test_lcpi_validation_final_v2"
    if not os.path.exists(result_file):
        print(f"❌ Fichier de résultats non trouvé: {result_file}")
        return
    
    try:
        import json
        with open(result_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Extraire les diamètres
        if 'proposals' in results and len(results['proposals']) > 0:
            proposal = results['proposals'][0]
            if 'diameters_mm' in proposal:
                diameters = proposal['diameters_mm']
                print(f"📏 Nombre de conduites avec diamètres: {len(diameters)}")
                
                # Analyser la distribution des diamètres
                diameter_counts = {}
                for conduit_id, diameter in diameters.items():
                    if diameter not in diameter_counts:
                        diameter_counts[diameter] = 0
                    diameter_counts[diameter] += 1
                
                print(f"📊 Distribution des diamètres:")
                for diameter in sorted(diameter_counts.keys()):
                    count = diameter_counts[diameter]
                    print(f"   {diameter} mm: {count} conduites")
                
                # Vérifier la cohérence des diamètres
                min_diameter = min(diameters.values())
                max_diameter = max(diameters.values())
                print(f"📏 Plage des diamètres: {min_diameter} - {max_diameter} mm")
                
                # Vérifier le coût total
                capex = proposal.get('CAPEX', 0)
                print(f"💰 Coût total (CAPEX): {capex:,.0f} FCFA")
                
                # Estimer le coût par mètre
                total_length = len(diameters) * 100  # Estimation: 100m par conduite
                cost_per_meter = capex / total_length if total_length > 0 else 0
                print(f"💵 Coût estimé par mètre: {cost_per_meter:,.0f} FCFA/m")
                
                # Comparer avec des prix typiques
                print(f"\n🔍 Analyse de cohérence:")
                if cost_per_meter < 1000:
                    print(f"   ⚠️ Coût par mètre très faible: {cost_per_meter:,.0f} FCFA/m")
                    print(f"   💡 Prix typique attendu: 5,000 - 50,000 FCFA/m")
                elif cost_per_meter < 10000:
                    print(f"   ⚠️ Coût par mètre faible: {cost_per_meter:,.0f} FCFA/m")
                    print(f"   💡 Prix typique attendu: 10,000 - 50,000 FCFA/m")
                else:
                    print(f"   ✅ Coût par mètre cohérent: {cost_per_meter:,.0f} FCFA/m")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des résultats: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNOSTIC COMPLET DE LA BASE DE DONNÉES DES PRIX")
    print("=" * 60)
    
    check_price_database()
    check_network_diameters()
    
    print(f"\n🎯 RECOMMANDATIONS:")
    print(f"   1. Vérifier que la base de données contient des prix réalistes")
    print(f"   2. Vérifier les unités des prix (FCFA/m vs FCFA/mm)")
    print(f"   3. Vérifier que les diamètres sont bien en millimètres")
    print(f"   4. Comparer avec des prix de référence du marché")
