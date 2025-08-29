#!/usr/bin/env python3
"""
Script de test des requêtes SQLite sur la base de pompes Grundfos
"""

import sqlite3
from pathlib import Path

def test_queries():
    """Teste diverses requêtes sur la base de pompes"""
    db_path = Path("grundfos_pompes_230_modeles_complet_pompes.db")
    
    if not db_path.exists():
        print("❌ Base SQLite non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 ANALYSE DES POMPES GRUNDFOS")
        print("=" * 50)
        
        # 1. Statistiques générales
        cursor.execute("""
            SELECT COUNT(*) as total, 
                   AVG(capex_estime_eur) as capex_moyen, 
                   AVG(opex_par_kwh_eur) as opex_moyen 
            FROM pompes
        """)
        row = cursor.fetchone()
        print(f"📊 Total: {row[0]} pompes")
        print(f"💰 CAPEX moyen: {row[1]:.0f}€")
        print(f"⚡ OPEX moyen: {row[2]:.3f}€/kWh")
        
        # 2. Répartition par plage de débit
        print("\n💧 Répartition par plage de débit:")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN debit_exploitation_m3h_max <= 5 THEN '0-5 m³/h'
                    WHEN debit_exploitation_m3h_max <= 20 THEN '5-20 m³/h'
                    WHEN debit_exploitation_m3h_max <= 100 THEN '20-100 m³/h'
                    ELSE '100+ m³/h'
                END as plage,
                COUNT(*) as nb
            FROM pompes 
            GROUP BY plage 
            ORDER BY nb DESC
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} pompes")
        
        # 3. Types de moteur
        print("\n🏗️ Types de moteur:")
        cursor.execute("""
            SELECT type_moteur, COUNT(*) as nb 
            FROM pompes 
            GROUP BY type_moteur 
            ORDER BY nb DESC 
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} pompes")
        
        # 4. Plages HMT
        print("\n📏 Répartition par plage HMT:")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN hmt_max_m <= 50 THEN '0-50m'
                    WHEN hmt_max_m <= 100 THEN '50-100m'
                    WHEN hmt_max_m <= 200 THEN '100-200m'
                    WHEN hmt_max_m <= 400 THEN '200-400m'
                    ELSE '400m+'
                END as plage_hmt,
                COUNT(*) as nb
            FROM pompes 
            GROUP BY plage_hmt 
            ORDER BY nb DESC
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} pompes")
        
        # 5. Pompes les plus performantes (rendement > 70%)
        print("\n⭐ Pompes les plus performantes (rendement > 70%):")
        cursor.execute("""
            SELECT designation, rendement_pompe_moteur_pct, capex_estime_eur
            FROM pompes 
            WHERE rendement_pompe_moteur_pct > 70
            ORDER BY rendement_pompe_moteur_pct DESC
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]:.1f}%, {row[2]:.0f}€")
        
        # 6. Recherche par plage de débit spécifique
        print("\n🔍 Pompes pour débit ~10 m³/h:")
        cursor.execute("""
            SELECT designation, debit_exploitation_m3h_min, debit_exploitation_m3h_max, 
                   hmt_min_m, hmt_max_m, capex_estime_eur
            FROM pompes 
            WHERE debit_exploitation_m3h_min <= 10.0 
              AND debit_exploitation_m3h_max >= 10.0
            ORDER BY capex_estime_eur
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}-{row[2]} m³/h, HMT {row[3]}-{row[4]}m, {row[5]:.0f}€")
        
        # 7. Analyse des coûts par type
        print("\n💰 Analyse des coûts par type de moteur:")
        cursor.execute("""
            SELECT type_moteur, 
                   COUNT(*) as nb,
                   AVG(capex_estime_eur) as capex_moyen,
                   AVG(opex_par_kwh_eur) as opex_moyen
            FROM pompes 
            GROUP BY type_moteur 
            ORDER BY capex_moyen DESC
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} pompes, CAPEX {row[2]:.0f}€, OPEX {row[3]:.3f}€/kWh")
        
        conn.close()
        print("\n✅ Tests des requêtes terminés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_queries()
