#!/usr/bin/env python3
"""
Démonstration du convertisseur CSV → YAML/SQLite avec support FCFA
Montre comment utiliser les nouvelles fonctionnalités:
- Conversion automatique EUR → FCFA
- Conversion des débits m³/h → m³/s
- Estimation OPEX basée sur la puissance absorbée
"""

import sys
from pathlib import Path
import sqlite3
import yaml

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from csv_to_yaml_sqlite_converter import PumpDataConverter


def demo_conversion_complete():
    """Démonstration de la conversion complète"""
    print("🚀 DÉMONSTRATION DU CONVERTISSEUR FCFA")
    print("=" * 60)
    
    # Chemin vers le fichier CSV source
    csv_source = Path("../src/lcpi/db/grundfos_pompes_230_modeles_complet.csv")
    
    if not csv_source.exists():
        print(f"❌ Fichier source non trouvé: {csv_source}")
        print("   Assurez-vous d'être dans le bon répertoire")
        return
    
    print(f"📁 Source: {csv_source}")
    print(f"📊 Taille: {csv_source.stat().st_size / 1024:.1f} KB")
    
    # Créer le convertisseur avec paramètres FCFA
    print(f"\n🔄 Configuration du convertisseur:")
    print(f"   - Taux de change: 1 EUR = 655.957 FCFA (BCEAO)")
    print(f"   - Coût électricité: 98.39 FCFA/kWh")
    
    converter = PumpDataConverter(
        str(csv_source),
        "demo_output_fcfa",
        eur_to_fcfa_rate=655.957,
        energy_cost_fcfa_kwh=98.39
    )
    
    try:
        print(f"\n🔄 Début de la conversion...")
        results = converter.convert(['yaml', 'sqlite'])
        
        print(f"\n✅ Conversion terminée avec succès!")
        print(f"📁 Fichiers générés:")
        
        for format_type, file_path in results.items():
            if format_type == 'report':
                print(f"   📋 Rapport: {file_path}")
            else:
                print(f"   ✅ {format_type.upper()}: {file_path}")
        
        return results
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion: {e}")
        return None


def demo_analyse_yaml(yaml_file):
    """Analyse le fichier YAML généré"""
    print(f"\n🔍 ANALYSE DU FICHIER YAML")
    print("=" * 40)
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if 'pompes' not in data:
            print("❌ Structure YAML invalide")
            return
        
        pompes = data['pompes']
        print(f"📊 Total pompes: {len(pompes)}")
        
        # Analyser quelques pompes
        for i, pompe in enumerate(pompes[:3]):
            print(f"\n🔍 Pompe {i+1}: {pompe['designation']}")
            print(f"   - Marque: {pompe['marque']}")
            print(f"   - Débit: {pompe['debit_exploitation_m3h_min']:.3f} - {pompe['debit_exploitation_m3h_max']:.3f} m³/h")
            print(f"   - Débit (m³/s): {pompe['debit_exploitation_m3s_min']:.6f} - {pompe['debit_exploitation_m3s_max']:.6f} m³/s")
            print(f"   - HMT: {pompe['hmt_min_m']:.0f} - {pompe['hmt_max_m']:.0f} m")
            print(f"   - CAPEX: {pompe['capex_estime_eur']:.2f} € → {pompe['capex_estime_fcfa']:,.0f} FCFA")
            print(f"   - Puissance P2: {pompe['puissance_p2_kw']:.2f} kW")
            print(f"   - Puissance absorbée: {pompe['puissance_absorbe_kw']:.2f} kW")
            print(f"   - OPEX estimé: {pompe['opex_estime_fcfa_kwh']:.2f} FCFA/kWh")
            
            # Vérifier les conversions
            if pompe['capex_estime_eur'] and pompe['capex_estime_fcfa']:
                taux = pompe['capex_estime_fcfa'] / pompe['capex_estime_eur']
                print(f"   ✅ Taux vérifié: {taux:.3f}")
            
            if pompe['debit_exploitation_m3h_min'] and pompe['debit_exploitation_m3s_min']:
                facteur = pompe['debit_exploitation_m3h_min'] / pompe['debit_exploitation_m3s_min']
                print(f"   ✅ Conversion débit: {facteur:.1f}")
    
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse YAML: {e}")


def demo_analyse_sqlite(db_file):
    """Analyse la base SQLite générée"""
    print(f"\n🗄️  ANALYSE DE LA BASE SQLITE")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Structure de la base
        cursor.execute("PRAGMA table_info(pompes)")
        columns = cursor.fetchall()
        
        print(f"📋 Structure de la table 'pompes':")
        print(f"   - Colonnes: {len(columns)}")
        
        # Afficher les nouvelles colonnes FCFA
        fcfa_columns = [col[1] for col in columns if 'fcfa' in col[1].lower()]
        print(f"   - Colonnes FCFA: {len(fcfa_columns)}")
        for col in fcfa_columns:
            print(f"     • {col}")
        
        # Statistiques des données
        cursor.execute("SELECT COUNT(*) FROM pompes")
        total = cursor.fetchone()[0]
        print(f"\n📊 Statistiques des données:")
        print(f"   - Total pompes: {total}")
        
        # Analyse des coûts FCFA
        cursor.execute("SELECT MIN(capex_estime_fcfa), MAX(capex_estime_fcfa), AVG(capex_estime_fcfa) FROM pompes WHERE capex_estime_fcfa IS NOT NULL")
        capex_stats = cursor.fetchone()
        if capex_stats[0]:
            print(f"   - CAPEX FCFA: {capex_stats[0]:,.0f} - {capex_stats[1]:,.0f} (moy: {capex_stats[2]:,.0f})")
        
        cursor.execute("SELECT MIN(opex_estime_fcfa_kwh), MAX(opex_estime_fcfa_kwh), AVG(opex_estime_fcfa_kwh) FROM pompes WHERE opex_estime_fcfa_kwh IS NOT NULL")
        opex_stats = cursor.fetchone()
        if opex_stats[0]:
            print(f"   - OPEX FCFA: {opex_stats[0]:.2f} - {opex_stats[1]:.2f} (moy: {opex_stats[2]:.2f})")
        
        # Analyse des débits convertis
        cursor.execute("SELECT MIN(debit_exploitation_m3s_min), MAX(debit_exploitation_m3s_max) FROM pompes WHERE debit_exploitation_m3s_min IS NOT NULL")
        debit_stats = cursor.fetchone()
        if debit_stats[0]:
            print(f"   - Débits (m³/s): {debit_stats[0]:.6f} - {debit_stats[1]:.6f}")
        
        # Exemple de requête complexe
        print(f"\n🔍 Exemple de requête - Pompes économiques:")
        cursor.execute("""
            SELECT designation, capex_estime_fcfa, opex_estime_fcfa_kwh, rendement_pompe_moteur_pct
            FROM pompes 
            WHERE capex_estime_fcfa < 50000 AND rendement_pompe_moteur_pct > 40
            ORDER BY capex_estime_fcfa ASC
            LIMIT 5
        """)
        
        pompes_economiques = cursor.fetchall()
        for pompe in pompes_economiques:
            print(f"   • {pompe[0]}: {pompe[1]:,.0f} FCFA, {pompe[2]:.2f} FCFA/kWh, η={pompe[3]:.1f}%")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse SQLite: {e}")


def demo_requetes_avancees(db_file):
    """Démonstration de requêtes avancées"""
    print(f"\n🔍 REQUÊTES AVANCÉES")
    print("=" * 30)
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 1. Recherche par plage de débit
        print(f"1️⃣  Recherche par plage de débit (0.5-2.0 m³/h):")
        cursor.execute("""
            SELECT designation, debit_exploitation_m3h_min, debit_exploitation_m3h_max, 
                   capex_estime_fcfa, hmt_min_m, hmt_max_m
            FROM pompes 
            WHERE debit_exploitation_m3h_min <= 2.0 AND debit_exploitation_m3h_max >= 0.5
            ORDER BY capex_estime_fcfa ASC
            LIMIT 5
        """)
        
        for pompe in cursor.fetchall():
            print(f"   • {pompe[0]}: {pompe[1]:.1f}-{pompe[2]:.1f} m³/h, {pompe[3]:,.0f} FCFA, HMT {pompe[4]:.0f}-{pompe[5]:.0f} m")
        
        # 2. Analyse des rendements
        print(f"\n2️⃣  Analyse des rendements par type de moteur:")
        cursor.execute("""
            SELECT type_moteur, 
                   COUNT(*) as total,
                   AVG(rendement_pompe_moteur_pct) as rendement_moyen,
                   AVG(capex_estime_fcfa) as capex_moyen
            FROM pompes 
            WHERE rendement_pompe_moteur_pct IS NOT NULL
            GROUP BY type_moteur
            ORDER BY rendement_moyen DESC
        """)
        
        for moteur in cursor.fetchall():
            print(f"   • {moteur[0]}: {moteur[1]} pompes, η={moteur[2]:.1f}%, CAPEX={moteur[3]:,.0f} FCFA")
        
        # 3. Optimisation coût/rendement
        print(f"\n3️⃣  Top 5 pompes optimisées (coût/rendement):")
        cursor.execute("""
            SELECT designation, 
                   capex_estime_fcfa,
                   rendement_pompe_moteur_pct,
                   (capex_estime_fcfa / rendement_pompe_moteur_pct) as ratio_cout_rendement
            FROM pompes 
            WHERE rendement_pompe_moteur_pct > 30 AND capex_estime_fcfa IS NOT NULL
            ORDER BY ratio_cout_rendement ASC
            LIMIT 5
        """)
        
        for pompe in cursor.fetchall():
            print(f"   • {pompe[0]}: {pompe[1]:,.0f} FCFA, η={pompe[2]:.1f}%, ratio={pompe[3]:.1f}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors des requêtes avancées: {e}")


def main():
    """Fonction principale de démonstration"""
    print("🎯 DÉMONSTRATION DU CONVERTISSEUR CSV → YAML/SQLITE AVEC SUPPORT FCFA")
    print("=" * 80)
    
    # Étape 1: Conversion
    results = demo_conversion_complete()
    if not results:
        print("❌ Impossible de continuer sans conversion réussie")
        return
    
    # Étape 2: Analyse YAML
    if 'yaml' in results:
        demo_analyse_yaml(results['yaml'])
    
    # Étape 3: Analyse SQLite
    if 'sqlite' in results:
        demo_analyse_sqlite(results['sqlite'])
        demo_requetes_avancees(results['sqlite'])
    
    print(f"\n🎉 DÉMONSTRATION TERMINÉE!")
    print(f"📁 Vérifiez les fichiers générés dans: demo_output_fcfa/")
    print(f"💡 Utilisez ces données pour vos optimisations LCPI avec coûts en FCFA!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️  Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
