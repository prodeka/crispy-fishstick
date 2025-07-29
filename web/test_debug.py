#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

API_URL = "http://localhost:5001"

def test_endpoint(endpoint, data):
    """Test un endpoint spécifique."""
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data, timeout=10)
        print(f"\n🔧 Test {endpoint}:")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Succès: {result.get('success', False)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    print("🔧 DIAGNOSTIC DES ERREURS 500")
    print("=" * 50)
    
    # Test 1: Poteau BA avancé
    data_poteau = {
        "Nu": 500,  # kN
        "Mu": 50,   # kN.m
        "b": 0.3,   # m
        "h": 0.3,   # m
        "L": 3.0,   # m
        "k": 1.0    # coefficient de flambement
    }
    test_endpoint("/api/beton_arme/poteau_avance", data_poteau)
    
    # Test 2: Compression centrée
    data_compression = {
        "Nu": 500,  # kN
        "b": 0.3,   # m
        "h": 0.3,   # m
        "L": 3.0,   # m
        "k": 1.0    # coefficient de flambement
    }
    test_endpoint("/api/beton_arme/compression_centree", data_compression)
    
    # Test 3: Flexion bois avancée
    data_flexion = {
        "longueur": 4.0,
        "charges": {"G": 2.0, "Q": 3.0, "W": 0.0, "S": 0.0},
        "classe_bois": "C24",
        "classe_service": 2,
        "duree_charge": "moyen_terme",
        "b": 100,
        "h": 200
    }
    test_endpoint("/api/bois/flexion_avance", data_flexion)
    
    # Test 4: Radier
    data_radier = {
        "nombre_poteaux": 4,
        "charges_poteaux": [
            {"G": 50, "Q": 30},
            {"G": 50, "Q": 30},
            {"G": 50, "Q": 30},
            {"G": 50, "Q": 30}
        ],
        "coordonnees_poteaux": [
            {"x": 0, "y": 0},
            {"x": 6, "y": 0},
            {"x": 0, "y": 6},
            {"x": 6, "y": 6}
        ],
        "contrainte_admissible_sol": 200,
        "dimensions_radier": {"A": 8, "B": 8, "h": 0.4}
    }
    test_endpoint("/api/beton_arme/radier", data_radier)

if __name__ == "__main__":
    main() 