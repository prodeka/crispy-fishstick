#!/usr/bin/env python3
"""
Test direct des commandes CLI AEP unifiées sans subprocess
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_population_unified_direct():
    """Test direct de la fonction population unifiée"""
    print("🔵 TEST DIRECT POPULATION UNIFIÉE")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.population_unified import calculate_population_projection_unified
        
        # Test avec données de test
        data = {
            "population_base": 1000,
            "taux_croissance": 0.037,
            "annees": 20,
            "methode": "malthus",
            "verbose": True
        }
        
        resultat = calculate_population_projection_unified(data)
        
        if resultat.get('statut') == 'SUCCES':
            print(f"✅ Population unifiée: SUCCES")
            print(f"   Population finale: {resultat.get('population_finale', 'N/A')}")
            return True
        else:
            print(f"❌ Population unifiée: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur population unifiée: {e}")
        return False

def test_demand_unified_direct():
    """Test direct de la fonction demande unifiée"""
    print("🔵 TEST DIRECT DEMANDE UNIFIÉE")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.demand_unified import calculate_water_demand_unified
        
        # Test avec données de test
        data = {
            "population": 1000,
            "dotation_l_j_hab": 150,
            "coefficient_pointe": 1.5,
            "verbose": True
        }
        
        resultat = calculate_water_demand_unified(data)
        
        if resultat.get('statut') == 'SUCCES':
            print(f"✅ Demande unifiée: SUCCES")
            if 'besoin_brut_m3j' in resultat:
                print(f"   Besoin brut: {resultat['besoin_brut_m3j']:.1f} m³/j")
            return True
        else:
            print(f"❌ Demande unifiée: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur demande unifiée: {e}")
        return False

def test_network_unified_direct():
    """Test direct de la fonction réseau unifié"""
    print("🔵 TEST DIRECT RÉSEAU UNIFIÉ")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.network_unified import dimension_network_unified
        
        # Test avec données de test
        data = {
            "debit_m3s": 0.1,
            "longueur_m": 1000,
            "materiau": "fonte",
            "perte_charge_max_m": 10.0,
            "methode": "darcy",
            "verbose": True
        }
        
        resultat = dimension_network_unified(data)
        
        if resultat.get('statut') == 'SUCCES':
            print(f"✅ Réseau unifié: SUCCES")
            if 'diametre_optimal_mm' in resultat:
                print(f"   Diamètre optimal: {resultat['diametre_optimal_mm']:.0f} mm")
            return True
        else:
            print(f"❌ Réseau unifié: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur réseau unifié: {e}")
        return False

def test_reservoir_unified_direct():
    """Test direct de la fonction réservoir unifié"""
    print("🔵 TEST DIRECT RÉSERVOIR UNIFIÉ")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.reservoir_unified import dimension_reservoir_unified
        
        # Test avec données de test
        data = {
            "volume_journalier_m3": 1000,
            "type_adduction": "continue",
            "forme_reservoir": "cylindrique",
            "type_zone": "ville_francaise_peu_importante",
            "verbose": True
        }
        
        resultat = dimension_reservoir_unified(data)
        
        if resultat.get('statut') == 'SUCCES':
            print(f"✅ Réservoir unifié: SUCCES")
            if 'volume_utile_m3' in resultat:
                print(f"   Volume utile: {resultat['volume_utile_m3']:.1f} m³")
            return True
        else:
            print(f"❌ Réservoir unifié: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur réservoir unifié: {e}")
        return False

def test_pumping_unified_direct():
    """Test direct de la fonction pompage unifié"""
    print("🔵 TEST DIRECT POMPAGE UNIFIÉ")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.pumping_unified import dimension_pumping_unified
        
        # Test avec données de test
        data = {
            "debit_m3h": 100,
            "hmt_m": 50,
            "type_pompe": "centrifuge",
            "rendement_pompe": 0.75,
            "verbose": True
        }
        
        resultat = dimension_pumping_unified(data)
        
        if resultat.get('statut') == 'SUCCES':
            print(f"✅ Pompage unifié: SUCCES")
            if 'puissance_electrique_kw' in resultat:
                print(f"   Puissance électrique: {resultat['puissance_electrique_kw']:.1f} kW")
            return True
        else:
            print(f"❌ Pompage unifié: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pompage unifié: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DIRECT CLI AEP UNIFIÉ")
    print("=" * 60)
    print("Ce test utilise directement les fonctions sans subprocess.")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Population unifiée", test_population_unified_direct),
        ("Demande unifiée", test_demand_unified_direct),
        ("Réseau unifié", test_network_unified_direct),
        ("Réservoir unifié", test_reservoir_unified_direct),
        ("Pompage unifié", test_pumping_unified_direct)
    ]
    
    success_count = 0
    for test_name, test_func in tests:
        print(f"\n📊 Test: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                success_count += 1
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    # Résumé
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS DIRECTS")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ RÉUSSI" if i < success_count else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests directs CLI AEP unifiés sont réussis !")
        print("✅ Les fonctions CLI AEP unifiées fonctionnent parfaitement.")
        return True
    else:
        print("⚠️ Certains tests directs CLI AEP unifiés ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 