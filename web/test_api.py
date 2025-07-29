#!/usr/bin/env python3
"""
Script de test pour l'API Nanostruct Web
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:5000"

def test_health():
    """Test de la santé de l'API"""
    print("🏥 Test de santé de l'API...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API en ligne: {data['message']}")
            return True
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        return False

def test_assainissement():
    """Test du calcul d'assainissement"""
    print("\n💧 Test du calcul d'assainissement...")
    
    data = {
        "surface": 1000.0,
        "coefficient_ruissellement": 0.9,
        "intensite_pluie": 50.0
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/assainissement/calcul",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul assainissement réussi")
                print(f"   Débit: {result['resultat']['debit_ls']} L/s")
                print(f"   Diamètre: {result['resultat']['diametre_approximatif_m']} m")
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

def test_beton_arme():
    """Test du calcul béton armé"""
    print("\n🏗️ Test du calcul béton armé...")
    
    data = {
        "hauteur": 3.0,
        "section": 0.25,
        "charge_axiale": 500000,  # 500 kN
        "resistance_beton": 25
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/beton_arme/poteau",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul béton armé réussi")
                print(f"   Contrainte: {result['resultat']['contrainte_compression_mpa']} MPa")
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

def test_bois():
    """Test du calcul bois"""
    print("\n🌳 Test du calcul bois...")
    
    data = {
        "hauteur": 3.0,
        "section": 0.04,
        "charge_axiale": 50000,  # 50 kN
        "classe_bois": "C24"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/bois/poteau",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calcul bois réussi")
                print(f"   Contrainte: {result['resultat']['contrainte_compression_mpa']} MPa")
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

def test_coefficients():
    """Test des endpoints de données de référence"""
    print("\n📊 Test des coefficients de référence...")
    
    endpoints = [
        "/api/assainissement/coefficients",
        "/api/beton_arme/classes",
        "/api/bois/classes"
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: {len(data)} éléments")
                success_count += 1
            else:
                print(f"❌ {endpoint}: Erreur {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur {e}")
    
    return success_count == len(endpoints)

def main():
    """Fonction principale de test"""
    print("🧪 Tests de l'API Nanostruct Web")
    print("=" * 50)
    
    # Attendre que l'API soit prête
    print("⏳ Attente du démarrage de l'API...")
    time.sleep(3)
    
    tests = [
        test_health,
        test_assainissement,
        test_beton_arme,
        test_bois,
        test_coefficients
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
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    test_names = [
        "Santé API",
        "Calcul Assainissement",
        "Calcul Béton Armé", 
        "Calcul Bois",
        "Coefficients"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{i+1}. {name}: {status}")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 Résultat global: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 Tous les tests sont passés ! L'API fonctionne correctement.")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")

if __name__ == "__main__":
    main() 