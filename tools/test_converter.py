#!/usr/bin/env python3
"""
Script de test pour le convertisseur CSV → YAML/SQLite
Teste les fonctionnalités principales sur un petit échantillon de données
"""

import sys
import tempfile
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour importer le convertisseur
sys.path.insert(0, str(Path(__file__).parent))

from csv_to_yaml_sqlite_converter import PumpDataConverter


def create_test_csv():
    """Crée un fichier CSV de test avec quelques pompes Grundfos"""
    csv_content = """Désignation,Marque,Nom du produit,Type de moteur,Poids net (kg),Débit exploitation (m³/h),Diamètre moteur,HMT (m),Fréquence (Hz),Tension (V),Intensité nominale (A),Puissance P2 (kW),Cos φ,Rendement pompe (%),Rendement pompe+moteur (%),Matériaux,Classe protection,Classe isolation,Temp max liquide (°C),Certification eau potable,Courbe H(Q) (points approximatifs),CAPEX Estimé (€),OPEX par kWh Estimé (€/kWh)
SP 1A-9,Grundfos,SP 1A-9,MS 402,10,0.3-1.5,4 pouces,10-60,50,1x230/3x400,1.9/1.1,0.37,0.85,50,42,AISI 304,IP68,F,40,Oui,"[(0, 60.0), (0.525, 57.0), (1.05, 51.0), (1.35, 36.0), (1.5, 24.0)]",37,0.357
SP 1A-14,Grundfos,SP 1A-14,MS 402,11,0.3-1.5,4 pouces,15-90,50,1x230/3x400,1.9/1.1,0.37,0.85,50,42,AISI 304,IP68,F,40,Oui,"[(0, 90.0), (0.525, 85.5), (1.05, 76.5), (1.35, 54.0), (1.5, 36.0)]",37,0.357
CR 1s-8,Grundfos,CR 1s-8,IEC 80,30,0.3-1.1,Surface,20-60,50,3x400,2.8,0.75,0.85,35,30,Fonte/AISI 304,IP55,F,120,Oui,"[(0, 60.0), (0.385, 57.0), (0.77, 51.0), (0.99, 36.0), (1.1, 24.0)]",60,0.5"""
    
    # Créer un fichier temporaire
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8')
    temp_file.write(csv_content)
    temp_file.close()
    
    return temp_file.name


def test_converter():
    """Teste le convertisseur avec le fichier de test"""
    print("🧪 Test du convertisseur CSV → YAML/SQLite")
    print("=" * 50)
    
    # Créer le fichier CSV de test
    test_csv = create_test_csv()
    print(f"📁 Fichier CSV de test créé: {test_csv}")
    
    try:
        # Créer le convertisseur
        converter = PumpDataConverter(test_csv, "test_output")
        print("✅ Convertisseur initialisé")
        
        # Tester le parsing CSV
        print("\n📊 Test du parsing CSV...")
        data = converter.parse_csv()
        print(f"✅ {len(data)} lignes parsées")
        
        # Afficher un exemple de données nettoyées
        if data:
            print("\n📋 Exemple de données nettoyées:")
            example = data[0]
            for key, value in list(example.items())[:5]:  # Afficher les 5 premiers champs
                print(f"  {key}: {value}")
        
        # Tester la conversion YAML
        print("\n📄 Test de la conversion YAML...")
        yaml_file = converter.to_yaml(data)
        print(f"✅ YAML généré: {yaml_file}")
        
        # Tester la conversion SQLite
        print("\n🗄️ Test de la conversion SQLite...")
        sqlite_file = converter.to_sqlite(data)
        print(f"✅ SQLite généré: {sqlite_file}")
        
        # Tester la génération du rapport
        print("\n📋 Test de la génération du rapport...")
        report_file = converter.generate_report(data, yaml_file, sqlite_file)
        print(f"✅ Rapport généré: {report_file}")
        
        print("\n🎉 Tous les tests ont réussi!")
        
        # Afficher les fichiers générés
        print("\n📁 Fichiers générés:")
        output_dir = Path("test_output")
        for file_path in output_dir.glob("*"):
            print(f"  - {file_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer le fichier temporaire
        try:
            os.unlink(test_csv)
            print(f"\n🧹 Fichier temporaire supprimé: {test_csv}")
        except:
            pass
    
    return True


def test_sqlite_queries():
    """Teste quelques requêtes SQLite sur la base générée"""
    print("\n🔍 Test des requêtes SQLite...")
    
    try:
        import sqlite3
        db_path = "test_output/grundfos_pompes_230_modeles_complet_pompes.db"
        
        if not os.path.exists(db_path):
            print("⚠️ Base SQLite non trouvée, test des requêtes ignoré")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test 1: Compter le nombre total de pompes
        cursor.execute("SELECT COUNT(*) FROM pompes")
        total = cursor.fetchone()[0]
        print(f"  📊 Total pompes: {total}")
        
        # Test 2: Lister les marques disponibles
        cursor.execute("SELECT DISTINCT marque FROM pompes")
        marques = [row[0] for row in cursor.fetchall()]
        print(f"  🏷️ Marques: {', '.join(marques)}")
        
        # Test 3: Trouver les pompes par plage de débit
        cursor.execute("""
            SELECT designation, debit_exploitation_m3h_min, debit_exploitation_m3h_max 
            FROM pompes 
            WHERE debit_exploitation_m3h_min <= 1.0 AND debit_exploitation_m3h_max >= 1.0
            LIMIT 3
        """)
        pompes_debit_1 = cursor.fetchall()
        print(f"  💧 Pompes avec débit ~1 m³/h: {len(pompes_debit_1)} trouvées")
        
        # Test 4: Statistiques des coûts
        cursor.execute("SELECT MIN(capex_estime_eur), MAX(capex_estime_eur), AVG(capex_estime_eur) FROM pompes WHERE capex_estime_eur IS NOT NULL")
        min_capex, max_capex, avg_capex = cursor.fetchone()
        print(f"  💰 CAPEX: min={min_capex:.0f}€, max={max_capex:.0f}€, moy={avg_capex:.0f}€")
        
        conn.close()
        print("✅ Tests des requêtes SQLite réussis")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests SQLite: {e}")


if __name__ == "__main__":
    print("🚀 Démarrage des tests du convertisseur...")
    
    # Test principal
    success = test_converter()
    
    if success:
        # Test des requêtes SQLite
        test_sqlite_queries()
        
        print("\n" + "=" * 50)
        print("🎯 Tests terminés avec succès!")
        print("📁 Consultez le dossier 'test_output' pour voir les résultats")
        print("=" * 50)
    else:
        print("\n❌ Tests échoués")
        sys.exit(1)
