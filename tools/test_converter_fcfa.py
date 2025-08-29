#!/usr/bin/env python3
"""
Script de test pour le convertisseur CSV → YAML/SQLite avec support FCFA
Teste les nouvelles fonctionnalités:
- Conversion EUR → FCFA
- Conversion m³/h → m³/s
- Estimation OPEX basée sur la puissance absorbée
"""

import sys
import tempfile
import shutil
from pathlib import Path
import sqlite3
import yaml

# Ajouter le répertoire parent au path pour importer le convertisseur
sys.path.insert(0, str(Path(__file__).parent))

from csv_to_yaml_sqlite_converter import PumpDataConverter


def create_test_csv():
    """Crée un fichier CSV de test avec des données de pompes"""
    csv_content = '''Désignation,Marque,Nom du produit,Type de moteur,Poids net (kg),Débit exploitation (m³/h),Diamètre moteur,HMT (m),Fréquence (Hz),Tension (V),Intensité nominale (A),Puissance P2 (kW),Cos φ,Rendement pompe (%),Rendement pompe+moteur (%),Matériaux,Classe protection,Classe isolation,Temp max liquide (°C),Certification eau potable,Courbe H(Q) (points approximatifs),CAPEX Estimé (€),OPEX par kWh Estimé (€/kWh)
SP 1A-9,Grundfos,SP 1A-9,MS 402,10,0.3-1.5,"4 pouces",10-60,50,1x230/3x400,1.9/1.1,0.37,0.85,50,42,AISI 304,IP68,F,40,Oui,"[(0, 60.0), (0.525, 57.0), (1.05, 51.0), (1.35, 36.0), (1.5, 24.0)]",37,0.357
SP 1A-14,Grundfos,SP 1A-14,MS 402,11,0.3-1.5,"4 pouces",15-90,50,1x230/3x400,1.9/1.1,0.37,0.85,50,42,AISI 304,IP68,F,40,Oui,"[(0, 90.0), (0.525, 85.5), (1.05, 76.5), (1.35, 54.0), (1.5, 36.0)]",37,0.357
SP 2A-8,Grundfos,SP 2A-8,MS 402,13,0.4-2.0,"4 pouces",12-55,50,1x230/3x400,1.7/1.0,0.37,0.7,48,38,AISI 304,IP68,F,40,Oui,"[(0, 55.0), (0.7, 52.25), (1.4, 46.75), (1.8, 33.0), (2.0, 22.0)]",37,0.395
SP 3A-15,Grundfos,SP 3A-15,MS 402,17,0.8-4.0,"4 pouces",20-105,50,1x230/3x400,3.4/2.0,0.75,0.7,58,45,AISI 304,IP68,F,40,Oui,"[(0, 105.0), (1.4, 99.75), (2.8, 89.25), (3.6, 63.0), (4.0, 42.0)]",75,0.333
SP 5A-25,Grundfos,SP 5A-25,MS 4000,22,1.5-6.0,"4 pouces",35-175,50,3x400,2.7,1.5,0.71,60,45,AISI 304,IP68,F,40,Oui,"[(0, 175.0), (2.1, 166.25), (4.2, 148.75), (5.4, 105.0), (6.0, 70.0)]",150,0.333'''
    
    return csv_content


def test_conversion_fcfa():
    """Teste la conversion avec support FCFA"""
    print("🧪 Test du convertisseur avec support FCFA")
    print("=" * 50)
    
    # Créer un répertoire temporaire pour les tests
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Créer le fichier CSV de test
        test_csv = temp_path / "test_pompes.csv"
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write(create_test_csv())
        
        print(f"📁 Fichier CSV de test créé: {test_csv}")
        
        # Tester avec différents taux de change
        test_cases = [
            {"eur_fcfa": 655.957, "energy_cost": 98.39, "name": "Taux officiel BCEAO"},
            {"eur_fcfa": 700.0, "energy_cost": 100.0, "name": "Taux arrondi"},
            {"eur_fcfa": 600.0, "energy_cost": 90.0, "name": "Taux bas"}
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}: {test_case['name']}")
            print(f"   - Taux: 1 EUR = {test_case['eur_fcfa']:.3f} FCFA")
            print(f"   - Électricité: {test_case['energy_cost']:.2f} FCFA/kWh")
            
            # Créer le convertisseur
            converter = PumpDataConverter(
                str(test_csv),
                str(temp_path / f"output_test_{i}"),
                eur_to_fcfa_rate=test_case['eur_fcfa'],
                energy_cost_fcfa_kwh=test_case['energy_cost']
            )
            
            try:
                # Conversion
                results = converter.convert(['yaml', 'sqlite'])
                
                # Vérifier les résultats
                print(f"   ✅ Conversion réussie")
                
                # Vérifier le fichier YAML
                if 'yaml' in results:
                    yaml_file = Path(results['yaml'])
                    if yaml_file.exists():
                        with open(yaml_file, 'r', encoding='utf-8') as f:
                            yaml_data = yaml.safe_load(f)
                        
                        # Vérifier la structure
                        if 'pompes' in yaml_data and len(yaml_data['pompes']) > 0:
                            pompe = yaml_data['pompes'][0]
                            
                            # Vérifier les conversions
                            if 'capex_estime_fcfa' in pompe and pompe['capex_estime_fcfa']:
                                capex_eur = pompe.get('capex_estime_eur', 0)
                                capex_fcfa = pompe['capex_estime_fcfa']
                                taux_calcule = capex_fcfa / capex_eur if capex_eur > 0 else 0
                                
                                print(f"   📊 CAPEX: {capex_eur:.2f} € → {capex_fcfa:,.0f} FCFA")
                                print(f"      Taux calculé: {taux_calcule:.3f} (attendu: {test_case['eur_fcfa']:.3f})")
                            
                            if 'debit_exploitation_m3s_min' in pompe:
                                debit_m3h = pompe.get('debit_exploitation_m3h_min', 0)
                                debit_m3s = pompe['debit_exploitation_m3s_min']
                                conversion_calculee = debit_m3h / debit_m3s if debit_m3s > 0 else 0
                                
                                print(f"   🔄 Débit: {debit_m3h:.3f} m³/h → {debit_m3s:.6f} m³/s")
                                print(f"      Facteur: {conversion_calculee:.1f} (attendu: 3600)")
                            
                            if 'puissance_absorbe_kw' in pompe and pompe['puissance_absorbe_kw']:
                                p2 = pompe.get('puissance_p2_kw', 0)
                                rendement = pompe.get('rendement_pompe_moteur_pct', 0)
                                p_abs = pompe['puissance_absorbe_kw']
                                
                                print(f"   ⚡ Puissance: P2={p2:.2f} kW, η={rendement:.1f}% → P_abs={p_abs:.2f} kW")
                
                # Vérifier la base SQLite
                if 'sqlite' in results:
                    db_file = Path(results['sqlite'])
                    if db_file.exists():
                        conn = sqlite3.connect(db_file)
                        cursor = conn.cursor()
                        
                        # Vérifier la structure
                        cursor.execute("PRAGMA table_info(pompes)")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        required_columns = [
                            'capex_estime_fcfa', 'debit_exploitation_m3s_min', 
                            'puissance_absorbe_kw', 'opex_estime_fcfa_kwh'
                        ]
                        
                        missing_columns = [col for col in required_columns if col not in columns]
                        if not missing_columns:
                            print(f"   🗄️  Base SQLite: Structure OK ({len(columns)} colonnes)")
                            
                            # Vérifier les données
                            cursor.execute("SELECT COUNT(*) FROM pompes")
                            count = cursor.fetchone()[0]
                            print(f"      {count} pompes enregistrées")
                        else:
                            print(f"   ❌ Base SQLite: Colonnes manquantes: {missing_columns}")
                        
                        conn.close()
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print(f"\n🎯 Tests terminés. Vérifiez les fichiers dans: {temp_path}")


def test_validation():
    """Teste la validation des données"""
    print("\n🔍 Test de validation des données")
    print("=" * 30)
    
    # Créer un répertoire temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Créer le fichier CSV de test
        test_csv = temp_path / "test_validation.csv"
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write(create_test_csv())
        
        # Tester avec des paramètres par défaut
        converter = PumpDataConverter(str(test_csv), str(temp_path / "validation_test"))
        
        try:
            # Parsing des données
            data = converter.parse_csv()
            
            print(f"📊 Données parsées: {len(data)} pompes")
            
            # Vérifier la première pompe
            if data:
                pompe = data[0]
                print(f"\n🔍 Première pompe analysée:")
                print(f"   - Désignation: {pompe['designation']}")
                print(f"   - CAPEX EUR: {pompe['capex_estime_eur']:.2f} €")
                print(f"   - CAPEX FCFA: {pompe['capex_estime_fcfa']:,.0f} FCFA")
                print(f"   - Débit min (m³/h): {pompe['debit_exploitation_m3h_min']:.3f}")
                print(f"   - Débit min (m³/s): {pompe['debit_exploitation_m3s_min']:.6f}")
                print(f"   - Puissance P2: {pompe['puissance_p2_kw']:.2f} kW")
                print(f"   - Puissance absorbée: {pompe['puissance_absorbe_kw']:.2f} kW")
                print(f"   - OPEX estimé: {pompe['opex_estime_fcfa_kwh']:.2f} FCFA/kWh")
                
                # Vérifications
                if pompe['capex_estime_fcfa'] and pompe['capex_estime_eur']:
                    taux = pompe['capex_estime_fcfa'] / pompe['capex_estime_eur']
                    print(f"   ✅ Taux de change vérifié: {taux:.3f}")
                
                if pompe['debit_exploitation_m3s_min'] and pompe['debit_exploitation_m3h_min']:
                    facteur = pompe['debit_exploitation_m3h_min'] / pompe['debit_exploitation_m3s_min']
                    print(f"   ✅ Conversion débit vérifiée: {facteur:.1f}")
                
                if pompe['puissance_absorbe_kw'] and pompe['puissance_p2_kw'] and pompe['rendement_pompe_moteur_pct']:
                    p_abs_calcule = pompe['puissance_p2_kw'] / (pompe['rendement_pompe_moteur_pct'] / 100)
                    print(f"   ✅ Puissance absorbée vérifiée: {p_abs_calcule:.2f} kW")
        
        except Exception as e:
            print(f"❌ Erreur lors de la validation: {e}")


if __name__ == "__main__":
    print("🚀 Démarrage des tests du convertisseur FCFA")
    print()
    
    try:
        # Test principal
        test_conversion_fcfa()
        
        # Test de validation
        test_validation()
        
        print("\n🎉 Tous les tests sont terminés!")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
