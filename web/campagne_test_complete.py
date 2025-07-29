#!/usr/bin/env python3
"""
Campagne de Test Complète - Migration CLI → Web
"""

import requests
import json
import time
import os
import subprocess
import sys
from pathlib import Path

# Configuration
API_STANDARD_URL = "http://localhost:5000"
API_AVANCEE_URL = "http://localhost:5001"

def test_connectivite():
    """Test de connectivité des deux APIs"""
    print("🔌 Test de connectivité des APIs...")
    
    # Test API Standard
    try:
        response = requests.get(f"{API_STANDARD_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Standard (Port 5000): Connectée")
            standard_ok = True
        else:
            print("❌ API Standard (Port 5000): Erreur HTTP")
            standard_ok = False
    except:
        print("❌ API Standard (Port 5000): Non connectée")
        standard_ok = False
    
    # Test API Avancée
    try:
        response = requests.get(f"{API_AVANCEE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Avancée (Port 5001): Connectée")
            avancee_ok = True
        else:
            print("❌ API Avancée (Port 5001): Erreur HTTP")
            avancee_ok = False
    except:
        print("❌ API Avancée (Port 5001): Non connectée")
        avancee_ok = False
    
    return standard_ok, avancee_ok

def test_fonctionnalites_standard():
    """Test des fonctionnalités de la version standard"""
    print("\n📊 Test des fonctionnalités Standard (Version 1.0)...")
    
    tests = []
    
    # Test 1: Calcul assainissement simple
    try:
        data = {"surface": 1000.0, "coefficient_ruissellement": 0.9, "intensite_pluie": 50.0}
        response = requests.post(f"{API_STANDARD_URL}/api/assainissement/calcul", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Calcul assainissement standard: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Calcul assainissement standard: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Calcul assainissement standard: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Calcul assainissement standard: Erreur {e}")
        tests.append(False)
    
    # Test 2: Calcul béton armé simple
    try:
        data = {"Nu": 500, "Mu": 50, "b": 0.3, "h": 0.3, "L": 3.0, "k": 1.0}
        response = requests.post(f"{API_STANDARD_URL}/api/beton_arme/poteau", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Calcul béton armé standard: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Calcul béton armé standard: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Calcul béton armé standard: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Calcul béton armé standard: Erreur {e}")
        tests.append(False)
    
    # Test 3: Calcul bois simple
    try:
        data = {"longueur": 4.0, "b": 150, "h": 200, "classe_bois": "C24"}
        response = requests.post(f"{API_STANDARD_URL}/api/bois/poteau", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Calcul bois standard: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Calcul bois standard: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Calcul bois standard: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Calcul bois standard: Erreur {e}")
        tests.append(False)
    
    return tests

def test_fonctionnalites_avancees():
    """Test des fonctionnalités de la version avancée"""
    print("\n🚀 Test des fonctionnalités Avancées (Version 2.0)...")
    
    tests = []
    
    # Test 1: Calcul assainissement avancé
    try:
        data = {"surface": 1000.0, "coefficient_ruissellement": 0.9, "intensite_pluie": 50.0}
        response = requests.post(f"{API_AVANCEE_URL}/api/assainissement/calcul_avance", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Calcul assainissement avancé: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Calcul assainissement avancé: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Calcul assainissement avancé: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Calcul assainissement avancé: Erreur {e}")
        tests.append(False)
    
    # Test 2: Traitement par lot assainissement
    try:
        import tempfile
        import csv
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'surface', 'coefficient_ruissellement', 'intensite_pluie'])
            writer.writerow([1, 1000.0, 0.9, 50.0])
            temp_file = f.name
        
        with open(temp_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_AVANCEE_URL}/api/assainissement/batch", files=files, timeout=15)
        
        os.unlink(temp_file)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Traitement par lot assainissement: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Traitement par lot assainissement: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Traitement par lot assainissement: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Traitement par lot assainissement: Erreur {e}")
        tests.append(False)
    
    # Test 3: Étude comparative
    try:
        data = {
            "surface": 1000.0,
            "coefficient_ruissellement": 0.9,
            "scenarios": [
                {"nom": "Scénario 1", "intensite_pluie": 50.0, "pente": 0.02},
                {"nom": "Scénario 2", "intensite_pluie": 60.0, "pente": 0.03}
            ]
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/assainissement/comparaison", json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Étude comparative assainissement: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Étude comparative assainissement: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Étude comparative assainissement: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Étude comparative assainissement: Erreur {e}")
        tests.append(False)
    
    # Test 4: Dimensionnement radier
    try:
        data = {
            "poteaux": [
                {"P_ser_kN": 500.0, "P_u_kN": 700.0},
                {"P_ser_kN": 600.0, "P_u_kN": 800.0}
            ],
            "dimensions_plan": {"A": 10.0, "B": 8.0},
            "sigma_sol_adm": 150.0
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/beton_arme/radier", json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Dimensionnement radier: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Dimensionnement radier: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Dimensionnement radier: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Dimensionnement radier: Erreur {e}")
        tests.append(False)
    
    # Test 5: Génération rapport PDF
    try:
        data = {
            "module": "assainissement",
            "donnees": {"surface": 1000.0, "coefficient_ruissellement": 0.9},
            "resultats": {"debit_ls": 12.5, "diametre_mm": 160}
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/rapports/generer_pdf", json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Génération rapport PDF: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Génération rapport PDF: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Génération rapport PDF: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Génération rapport PDF: Erreur {e}")
        tests.append(False)
    
    return tests

def test_endpoints_reference():
    """Test des endpoints de référence"""
    print("\n📋 Test des endpoints de référence...")
    
    tests = []
    
    # Test endpoints avancés
    endpoints_avances = [
        "/api/assainissement/formules_idf",
        "/api/assainissement/formules_tc",
        "/api/beton_arme/materiaux",
        "/api/bois/classes_avancees",
        "/api/rapports/liste"
    ]
    
    for endpoint in endpoints_avances:
        try:
            response = requests.get(f"{API_AVANCEE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: RÉUSSI")
                tests.append(True)
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                tests.append(False)
        except Exception as e:
            print(f"❌ {endpoint}: Erreur {e}")
            tests.append(False)
    
    return tests

def generer_rapport_campagne(tests_standard, tests_avancees, tests_reference):
    """Génère un rapport de la campagne de test"""
    print("\n" + "=" * 80)
    print("📊 RAPPORT DE LA CAMPAGNE DE TEST COMPLÈTE")
    print("=" * 80)
    
    # Statistiques générales
    total_standard = len(tests_standard)
    reussis_standard = sum(tests_standard)
    total_avancees = len(tests_avancees)
    reussis_avancees = sum(tests_avancees)
    total_reference = len(tests_reference)
    reussis_reference = sum(tests_reference)
    
    print(f"\n📈 STATISTIQUES GÉNÉRALES:")
    if total_standard > 0:
        print(f"   Version Standard: {reussis_standard}/{total_standard} ({reussis_standard/total_standard*100:.1f}%)")
    else:
        print(f"   Version Standard: Non testée")
    if total_avancees > 0:
        print(f"   Version Avancée: {reussis_avancees}/{total_avancees} ({reussis_avancees/total_avancees*100:.1f}%)")
    else:
        print(f"   Version Avancée: Non testée")
    if total_reference > 0:
        print(f"   Endpoints Référence: {reussis_reference}/{total_reference} ({reussis_reference/total_reference*100:.1f}%)")
    else:
        print(f"   Endpoints Référence: Non testés")
    
    # Évaluation de la migration
    migration_score = (reussis_avancees / total_avancees) * 100 if total_avancees > 0 else 0
    
    print(f"\n🎯 ÉVALUATION DE LA MIGRATION CLI → WEB:")
    if migration_score >= 90:
        print(f"   🎉 EXCELLENTE ({migration_score:.1f}%) - Migration quasi-complète")
    elif migration_score >= 75:
        print(f"   ✅ TRÈS BONNE ({migration_score:.1f}%) - Migration bien avancée")
    elif migration_score >= 50:
        print(f"   ⚠️ BONNE ({migration_score:.1f}%) - Migration en cours")
    else:
        print(f"   ❌ INSUFFISANTE ({migration_score:.1f}%) - Migration à améliorer")
    
    # Fonctionnalités clés
    print(f"\n🔑 FONCTIONNALITÉS CLÉS:")
    fonctionnalites_cles = [
        ("Calculs principaux", tests_avancees[0] if len(tests_avancees) > 0 else False),
        ("Traitement par lot", tests_avancees[1] if len(tests_avancees) > 1 else False),
        ("Étude comparative", tests_avancees[2] if len(tests_avancees) > 2 else False),
        ("Dimensionnement radier", tests_avancees[3] if len(tests_avancees) > 3 else False),
        ("Rapports PDF", tests_avancees[4] if len(tests_avancees) > 4 else False)
    ]
    
    for nom, statut in fonctionnalites_cles:
        icone = "✅" if statut else "❌"
        print(f"   {icone} {nom}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    if migration_score >= 90:
        print("   🚀 La migration est un succès ! L'application est prête pour la production.")
    elif migration_score >= 75:
        print("   ⚡ La migration est bien avancée. Quelques ajustements mineurs nécessaires.")
    elif migration_score >= 50:
        print("   🔧 La migration progresse bien. Continuer le développement des fonctionnalités manquantes.")
    else:
        print("   🛠️ La migration nécessite des améliorations importantes.")
    
    print(f"\n🎉 CAMPAGNE DE TEST TERMINÉE !")

def main():
    """Fonction principale de la campagne de test"""
    print("🧪 CAMPAGNE DE TEST COMPLÈTE - Migration CLI → Web")
    print("=" * 80)
    
    # Test de connectivité
    standard_ok, avancee_ok = test_connectivite()
    
    if not standard_ok and not avancee_ok:
        print("\n❌ Aucune API n'est accessible. Vérifiez que les serveurs sont démarrés.")
        return
    
    # Tests des fonctionnalités
    tests_standard = test_fonctionnalites_standard() if standard_ok else []
    tests_avancees = test_fonctionnalites_avancees() if avancee_ok else []
    tests_reference = test_endpoints_reference() if avancee_ok else []
    
    # Génération du rapport
    generer_rapport_campagne(tests_standard, tests_avancees, tests_reference)

if __name__ == "__main__":
    main() 