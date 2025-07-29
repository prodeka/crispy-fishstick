#!/usr/bin/env python3
"""
Script de test pour l'API Nanostruct Web Avancée
"""

import requests
import json
import time
import os

# Configuration
API_BASE_URL = "http://localhost:5001"

def test_health():
    """Test de la santé de l'API avancée"""
    print("🏥 Test de santé de l'API avancée...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API avancée en ligne: {data['message']}")
            print(f"📋 Version: {data['version']}")
            return True
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API avancée")
        return False

def test_assainissement_avance():
    """Test du calcul d'assainissement avancé"""
    print("\n💧 Test du calcul d'assainissement avancé...")
    
    data = {
        "surface": 1000.0,
        "coefficient_ruissellement": 0.9,
        "intensite_pluie": 50.0,
        "pente": 0.02,
        "rugosite": 0.013
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/assainissement/calcul_avance",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul assainissement avancé réussi")
                print(f"   Débit: {result['resultat']['debit_ls']} L/s")
                print(f"   Diamètre: {result['resultat']['diametre_mm']} mm")
                print(f"   Vitesse: {result['resultat']['vitesse_ms']} m/s")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_poteau_ba_avance():
    """Test du calcul de poteau BA avancé"""
    print("\n🏗️ Test du calcul de poteau BA avancé...")
    
    data = {
        "Nu": 500000,  # 500 kN
        "Mu": 50000,    # 50 kN.m
        "b": 0.3,       # 30 cm
        "h": 0.3,       # 30 cm
        "L": 3.0,       # 3 m
        "k": 1.0,       # coefficient de flambement
        "fc28": 25.0,
        "fe": 500.0
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/beton_arme/poteau_avance",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul poteau BA avancé réussi")
                print(f"   Section acier: {result['resultat']['section_acier_requise_cm2']} cm²")
                print(f"   Vérification: {result['resultat']['verification']}")
                print(f"   Élancement: {result['resultat']['elancement']}")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_compression_centree():
    """Test du calcul de compression centrée"""
    print("\n🏗️ Test du calcul de compression centrée...")
    
    data = {
        "Nu": 800000,  # 800 kN
        "b": 0.4,      # 40 cm
        "h": 0.4,      # 40 cm
        "L": 3.5,      # 3.5 m
        "k": 1.0,      # coefficient de flambement
        "fc28": 30.0,
        "fe": 500.0
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/beton_arme/compression_centree",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul compression centrée réussi")
                print(f"   Section acier: {result['resultat']['section_acier_requise_cm2']} cm²")
                print(f"   Vérification: {result['resultat']['verification']}")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_moment_poutre():
    """Test du calcul de moment d'encastrement"""
    print("\n🏗️ Test du calcul de moment d'encastrement...")
    
    data = {
        "q": 25.0,        # 25 kN/m
        "L": 5.0,         # 5 m
        "is_end_span": True
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/beton_arme/moment_poutre",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul moment d'encastrement réussi")
                print(f"   Moment: {result['resultat']['moment_encastrement_knm']} kN.m")
                print(f"   Type: {result['resultat']['type_poutre']}")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_flexion_bois_avance():
    """Test de la vérification de flexion bois avancée"""
    print("\n🌳 Test de la vérification de flexion bois avancée...")
    
    data = {
        "longueur": 4.0,      # 4 m
        "b": 150,             # 150 mm
        "h": 200,             # 200 mm
        "classe_bois": "C24",
        "classe_service": 2,
        "duree_charge": "moyen terme",
        "charge_g": 2.5,      # 2.5 kN/m
        "charge_q": 3.0,      # 3.0 kN/m
        "charge_w": 0.0,
        "charge_s": 0.0
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/bois/flexion_avance",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Vérification flexion bois avancée réussi")
                print(f"   Moment max: {result['resultat']['moment_maximal_knm']} kN.m")
                print(f"   Section adéquate: {result['resultat']['section_adequate']}")
                print(f"   Message: {result['resultat']['message']}")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_traction_bois_avance():
    """Test de la vérification de traction bois avancée"""
    print("\n🌳 Test de la vérification de traction bois avancée...")
    
    data = {
        "N": 5000,            # 5000 daN
        "b": 100,             # 100 mm
        "h": 100,             # 100 mm
        "classe_bois": "C24",
        "classe_service": 2,
        "duree_charge": "moyen terme"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/bois/traction_avance",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Vérification traction bois avancée réussi")
                print(f"   Effort traction: {result['resultat']['effort_traction_kn']} kN")
                print(f"   Section adéquate: {result['resultat']['section_adequate']}")
                print(f"   Message: {result['resultat']['message']}")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_traitement_lot_assainissement():
    """Test du traitement par lot pour l'assainissement"""
    print("\n📊 Test du traitement par lot assainissement...")
    
    # Créer un fichier CSV temporaire pour le test
    import tempfile
    import csv
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'surface', 'coefficient_ruissellement', 'intensite_pluie', 'pente', 'rugosite'])
        writer.writerow([1, 1000.0, 0.9, 50.0, 0.02, 0.013])
        writer.writerow([2, 2000.0, 0.8, 60.0, 0.03, 0.015])
        temp_file = f.name
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE_URL}/api/assainissement/batch",
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Traitement par lot assainissement réussi")
                print(f"   Éléments traités: {result['total_traites']}")
                return True
            else:
                print(f"❌ Erreur traitement: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    finally:
        os.unlink(temp_file)

def test_traitement_lot_beton_arme():
    """Test du traitement par lot pour le béton armé"""
    print("\n📊 Test du traitement par lot béton armé...")
    
    import tempfile
    import csv
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'Nu', 'Mu', 'b', 'h', 'L', 'k', 'fc28', 'fe'])
        writer.writerow([1, 500000, 50000, 0.3, 0.3, 3.0, 1.0, 25.0, 500.0])
        writer.writerow([2, 800000, 80000, 0.4, 0.4, 3.5, 1.0, 30.0, 500.0])
        temp_file = f.name
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE_URL}/api/beton_arme/batch",
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Traitement par lot béton armé réussi")
                print(f"   Poteaux traités: {result['total_traites']}")
                return True
            else:
                print(f"❌ Erreur traitement: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    finally:
        os.unlink(temp_file)

def test_traitement_lot_bois():
    """Test du traitement par lot pour le bois"""
    print("\n📊 Test du traitement par lot bois...")
    
    import tempfile
    import csv
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'longueur', 'b', 'h', 'classe_bois', 'charge_g', 'charge_q', 'classe_service'])
        writer.writerow([1, 4.0, 150, 200, 'C24', 2.5, 3.0, 2])
        writer.writerow([2, 5.0, 200, 250, 'C30', 3.0, 4.0, 2])
        temp_file = f.name
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE_URL}/api/bois/batch",
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Traitement par lot bois réussi")
                print(f"   Éléments traités: {result['total_traites']}")
                return True
            else:
                print(f"❌ Erreur traitement: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    finally:
        os.unlink(temp_file)

def test_radier_beton_arme():
    """Test du dimensionnement de radier"""
    print("\n🏗️ Test du dimensionnement de radier...")
    
    data = {
        "poteaux": [
            {"P_ser_kN": 500.0, "P_u_kN": 700.0},
            {"P_ser_kN": 600.0, "P_u_kN": 800.0},
            {"P_ser_kN": 400.0, "P_u_kN": 600.0}
        ],
        "dimensions_plan": {"A": 10.0, "B": 8.0},
        "sigma_sol_adm": 150.0,
        "fc28": 25.0,
        "fe": 500.0
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/beton_arme/radier",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Dimensionnement radier réussi")
                print(f"   Surface: {result['resultat']['dimensions']['surface_m2']} m²")
                print(f"   Épaisseur: {result['resultat']['dimensions']['epaisseur_estimee_m']} m")
                print(f"   Vérification sol: {result['resultat']['verification_sol']['verification_ok']}")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_etude_comparative_assainissement():
    """Test de l'étude comparative assainissement"""
    print("\n💧 Test de l'étude comparative assainissement...")
    
    data = {
        "surface": 1000.0,
        "coefficient_ruissellement": 0.9,
        "scenarios": [
            {"nom": "Scénario 1", "intensite_pluie": 50.0, "pente": 0.02, "rugosite": 0.013},
            {"nom": "Scénario 2", "intensite_pluie": 60.0, "pente": 0.03, "rugosite": 0.015},
            {"nom": "Scénario 3", "intensite_pluie": 40.0, "pente": 0.01, "rugosite": 0.012}
        ]
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/assainissement/comparaison",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Étude comparative assainissement réussi")
                print(f"   Scénarios analysés: {result['total_scenarios']}")
                print(f"   Scénarios réussis: {result['scenarios_reussis']}")
                if result['analyse_comparative']:
                    print(f"   Variation débit: {result['analyse_comparative']['variation_debit_pourcent']}%")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_calcul_idf():
    """Test du calcul IDF"""
    print("\n🌧️ Test du calcul IDF...")
    
    data = {
        "formule": "montana",
        "periode_retour": 10,
        "parametres": {"a": 100.0, "b": -0.5}
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/assainissement/calcul_idf",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul IDF réussi")
                print(f"   Formule: {result['resultat']['formule']}")
                print(f"   Intensité: {result['resultat']['intensite_mmh']} mm/h")
                return True
            else:
                print(f"❌ Erreur calcul: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_generation_rapport_pdf():
    """Test de la génération de rapport PDF"""
    print("\n📄 Test de la génération de rapport PDF...")
    
    data = {
        "module": "assainissement",
        "donnees": {
            "surface": 1000.0,
            "coefficient_ruissellement": 0.9,
            "intensite_pluie": 50.0,
            "pente": 0.02,
            "rugosite": 0.013
        },
        "resultats": {
            "debit_ls": 12.5,
            "diametre_mm": 160,
            "vitesse_ms": 0.62
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/rapports/generer_pdf",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Génération rapport PDF réussi")
                print(f"   Fichier: {result['fichier']}")
                return True
            else:
                print(f"❌ Erreur génération: {result.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_endpoints_avances_completes():
    """Test des endpoints avancés complets"""
    print("\n📊 Test des endpoints avancés complets...")
    
    endpoints = [
        "/api/assainissement/formules_idf",
        "/api/assainissement/formules_tc",
        "/api/beton_arme/materiaux",
        "/api/bois/classes_avancees",
        "/api/rapports/liste"
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/api/assainissement/formules_idf":
                    print(f"✅ {endpoint}: {len(data)} formules IDF")
                elif endpoint == "/api/assainissement/formules_tc":
                    print(f"✅ {endpoint}: {len(data)} formules Tc")
                elif endpoint == "/api/beton_arme/materiaux":
                    print(f"✅ {endpoint}: {len(data['betons'])} bétons, {len(data['aciers'])} aciers")
                elif endpoint == "/api/bois/classes_avancees":
                    print(f"✅ {endpoint}: {len(data)} classes de bois")
                elif endpoint == "/api/rapports/liste":
                    print(f"✅ {endpoint}: {data['total']} rapport(s)")
                success_count += 1
            else:
                print(f"❌ {endpoint}: Erreur {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur {e}")
    
    return success_count == len(endpoints)

def main():
    """Fonction principale de test"""
    print("🧪 Tests de l'API Nanostruct Web Avancée - Version Complète")
    print("=" * 70)
    
    # Attendre que l'API soit prête
    print("⏳ Attente du démarrage de l'API avancée...")
    time.sleep(3)
    
    tests = [
        test_health,
        test_assainissement_avance,
        test_poteau_ba_avance,
        test_compression_centree,
        test_moment_poutre,
        test_flexion_bois_avance,
        test_traction_bois_avance,
        test_traitement_lot_assainissement,
        test_traitement_lot_beton_arme,
        test_traitement_lot_bois,
        test_radier_beton_arme,
        test_etude_comparative_assainissement,
        test_calcul_idf,
        test_generation_rapport_pdf,
        test_endpoints_avances_completes
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result if result is not None else False)
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ DES TESTS AVANCÉS COMPLETS")
    print("=" * 70)
    
    test_names = [
        "Santé API Avancée",
        "Calcul Assainissement Avancé",
        "Calcul Poteau BA Avancé",
        "Compression Centrée",
        "Moment Poutre",
        "Flexion Bois Avancée",
        "Traction Bois Avancée",
        "Traitement Lot Assainissement",
        "Traitement Lot Béton Armé",
        "Traitement Lot Bois",
        "Dimensionnement Radier",
        "Étude Comparative Assainissement",
        "Calcul IDF",
        "Génération Rapport PDF",
        "Endpoints Avancés Complets"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{i+1:2d}. {name}: {status}")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 Résultat global: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 Tous les tests avancés sont passés ! La migration CLI→Web est COMPLÈTE !")
    elif success_count >= total_count * 0.8:
        print("✅ La plupart des tests sont passés. Migration quasi-complète.")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")

if __name__ == "__main__":
    main() 