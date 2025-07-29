#!/usr/bin/env python3
"""
Test Complet des Corrections - Migration CLI → Web
"""

import requests
import json
import time

# Configuration
API_AVANCEE_URL = "http://localhost:5001"

def test_endpoints_corriges():
    """Test des endpoints corrigés"""
    print("🔧 Test des endpoints corrigés...")
    
    tests = []
    
    # Test 1: Poteau BA avancé (corrigé)
    try:
        data = {
            "Nu": 500,  # kN
            "Mu": 50,   # kN.m
            "b": 0.3,   # m
            "h": 0.3,   # m
            "L": 3.0,   # m
            "k": 1.0    # coefficient de flambement
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/beton_arme/poteau_avance", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Poteau BA avancé: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Poteau BA avancé: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Poteau BA avancé: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Poteau BA avancé: Erreur {e}")
        tests.append(False)
    
    # Test 2: Compression centrée (corrigée)
    try:
        data = {
            "Nu": 500,  # kN
            "b": 0.3,   # m
            "h": 0.3,   # m
            "L": 3.0,   # m
            "k": 1.0    # coefficient de flambement
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/beton_arme/compression_centree", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Compression centrée: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Compression centrée: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Compression centrée: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Compression centrée: Erreur {e}")
        tests.append(False)
    
    # Test 3: Flexion bois avancée (corrigée)
    try:
        data = {
            "longueur": 4.0,      # m
            "b": 150,              # mm
            "h": 200,              # mm
            "classe_bois": "C24",
            "charge_g": 2.0,       # kN/m
            "charge_q": 3.0,       # kN/m
            "classe_service": 2,
            "duree_charge": "moyen_terme"
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/bois/flexion_avance", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Flexion bois avancée: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Flexion bois avancée: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Flexion bois avancée: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Flexion bois avancée: Erreur {e}")
        tests.append(False)
    
    # Test 4: Traction bois avancée (corrigée)
    try:
        data = {
            "N": 5000,             # daN
            "b": 100,              # mm
            "h": 100,              # mm
            "classe_bois": "C24",
            "classe_service": 2,
            "duree_charge": "moyen_terme"
        }
        response = requests.post(f"{API_AVANCEE_URL}/api/bois/traction_avance", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Traction bois avancée: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Traction bois avancée: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Traction bois avancée: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Traction bois avancée: Erreur {e}")
        tests.append(False)
    
    # Test 5: Dimensionnement radier (corrigé)
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
    
    return tests

def test_endpoints_fonctionnels():
    """Test des endpoints déjà fonctionnels"""
    print("\n✅ Test des endpoints déjà fonctionnels...")
    
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
    
    # Test 2: Moment poutre
    try:
        data = {"q": 10.0, "L": 5.0, "is_end_span": True}
        response = requests.post(f"{API_AVANCEE_URL}/api/beton_arme/moment_poutre", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Moment poutre: RÉUSSI")
                tests.append(True)
            else:
                print("❌ Moment poutre: ÉCHOUÉ")
                tests.append(False)
        else:
            print(f"❌ Moment poutre: HTTP {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Moment poutre: Erreur {e}")
        tests.append(False)
    
    # Test 3: Traitement par lot assainissement
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
        
        import os
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
    
    return tests

def generer_rapport_corrections(tests_corriges, tests_fonctionnels):
    """Génère un rapport des corrections"""
    print("\n" + "=" * 80)
    print("🔧 RAPPORT DES CORRECTIONS - Migration CLI → Web")
    print("=" * 80)
    
    # Statistiques
    total_corriges = len(tests_corriges)
    reussis_corriges = sum(tests_corriges)
    total_fonctionnels = len(tests_fonctionnels)
    reussis_fonctionnels = sum(tests_fonctionnels)
    
    print(f"\n📊 STATISTIQUES DES CORRECTIONS:")
    print(f"   Endpoints Corrigés: {reussis_corriges}/{total_corriges} ({reussis_corriges/total_corriges*100:.1f}%)")
    print(f"   Endpoints Fonctionnels: {reussis_fonctionnels}/{total_fonctionnels} ({reussis_fonctionnels/total_fonctionnels*100:.1f}%)")
    
    # Évaluation des corrections
    taux_reussite = (reussis_corriges + reussis_fonctionnels) / (total_corriges + total_fonctionnels) * 100
    
    print(f"\n🎯 ÉVALUATION DES CORRECTIONS:")
    if taux_reussite >= 90:
        print(f"   🎉 EXCELLENTE ({taux_reussite:.1f}%) - Toutes les corrections sont réussies")
    elif taux_reussite >= 75:
        print(f"   ✅ TRÈS BONNE ({taux_reussite:.1f}%) - La plupart des corrections sont réussies")
    elif taux_reussite >= 50:
        print(f"   ⚠️ BONNE ({taux_reussite:.1f}%) - Corrections partiellement réussies")
    else:
        print(f"   ❌ INSUFFISANTE ({taux_reussite:.1f}%) - Corrections à améliorer")
    
    # Détail des corrections
    print(f"\n🔧 DÉTAIL DES CORRECTIONS:")
    corrections = [
        ("Poteau BA avancé", tests_corriges[0] if len(tests_corriges) > 0 else False),
        ("Compression centrée", tests_corriges[1] if len(tests_corriges) > 1 else False),
        ("Flexion bois avancée", tests_corriges[2] if len(tests_corriges) > 2 else False),
        ("Traction bois avancée", tests_corriges[3] if len(tests_corriges) > 3 else False),
        ("Dimensionnement radier", tests_corriges[4] if len(tests_corriges) > 4 else False)
    ]
    
    for nom, statut in corrections:
        icone = "✅" if statut else "❌"
        print(f"   {icone} {nom}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    if taux_reussite >= 90:
        print("   🚀 Toutes les corrections sont réussies ! L'API est prête pour la production.")
    elif taux_reussite >= 75:
        print("   ⚡ La plupart des corrections sont réussies. Quelques ajustements mineurs nécessaires.")
    elif taux_reussite >= 50:
        print("   🔧 Les corrections progressent bien. Continuer les améliorations.")
    else:
        print("   🛠️ Les corrections nécessitent des améliorations importantes.")
    
    print(f"\n🎉 TEST DES CORRECTIONS TERMINÉ !")

def main():
    """Fonction principale"""
    print("🔧 TEST COMPLET DES CORRECTIONS - Migration CLI → Web")
    print("=" * 80)
    
    # Test de connectivité
    try:
        response = requests.get(f"{API_AVANCEE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Avancée connectée")
        else:
            print("❌ API Avancée non accessible")
            return
    except:
        print("❌ API Avancée non accessible")
        return
    
    # Tests des corrections
    tests_corriges = test_endpoints_corriges()
    tests_fonctionnels = test_endpoints_fonctionnels()
    
    # Rapport
    generer_rapport_corrections(tests_corriges, tests_fonctionnels)

if __name__ == "__main__":
    main() 