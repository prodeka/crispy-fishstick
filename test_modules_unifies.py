#!/usr/bin/env python3
"""
Test des modules unifiés AEP - Version Fusionnée et Enrichie

Ce script teste les modules unifiés qui fusionnent les fonctionnalités
des versions basiques et enhanced pour offrir une version complète.
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin pour importer les modules AEP
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_network_unified():
    """Test du module réseau unifié."""
    print("🔧 TEST DU MODULE RÉSEAU UNIFIÉ")
    print("=" * 50)
    
    try:
        from lcpi.aep.calculations.network_unified import (
            NetworkCalculationsUnified,
            dimension_network_unified,
            comparer_methodes_network_unified,
            verifier_vitesse_network_unified,
            calculer_pression_requise_network_unified
        )
        
        # Test 1: Dimensionnement réseau
        print("\n📊 Test 1: Dimensionnement réseau")
        data_network = {
            "debit_m3s": 0.1,
            "longueur_m": 1000,
            "materiau": "fonte",
            "perte_charge_max_m": 10.0,
            "methode": "darcy"
        }
        
        result = dimension_network_unified(data_network, verbose=True)
        print(f"✅ Résultat dimensionnement: {result['statut']}")
        if result['statut'] == 'SUCCES':
            print(f"   Diamètre optimal: {result['reseau']['diametre_optimal_mm']} mm")
            print(f"   Vitesse: {result['reseau']['vitesse_ms']:.2f} m/s")
            print(f"   Pertes de charge: {result['reseau']['perte_charge_m']:.2f} m")
        
        # Test 2: Comparaison des méthodes
        print("\n📊 Test 2: Comparaison des méthodes")
        data_comparison = {
            "debit_m3s": 0.1,
            "diametre_m": 0.5,
            "longueur_m": 1000,
            "materiau": "fonte"
        }
        
        result_comp = comparer_methodes_network_unified(data_comparison)
        print(f"✅ Résultat comparaison: {len(result_comp)} méthodes testées")
        if 'analyse' in result_comp:
            print(f"   Méthode min: {result_comp['analyse']['methode_min']}")
            print(f"   Méthode max: {result_comp['analyse']['methode_max']}")
            print(f"   Écart relatif: {result_comp['analyse']['ecart_relatif']:.1f}%")
        
        # Test 3: Vérification vitesse
        print("\n📊 Test 3: Vérification vitesse")
        data_vitesse = {"vitesse_ms": 1.5}
        result_vitesse = verifier_vitesse_network_unified(data_vitesse)
        print(f"✅ Vitesse {result_vitesse['vitesse_ms']} m/s: {result_vitesse['recommandation']}")
        
        # Test 4: Calcul pression requise
        print("\n📊 Test 4: Calcul pression requise")
        data_pression = {"nombre_etages": 5, "hauteur_etage_m": 3.0}
        result_pression = calculer_pression_requise_network_unified(data_pression)
        print(f"✅ Pression requise: {result_pression['pression_requise_bar']:.2f} bar")
        
        print("\n✅ Tous les tests réseau unifié ont réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test réseau unifié: {e}")
        return False

def test_population_unified():
    """Test du module population unifié."""
    print("\n🔢 TEST DU MODULE POPULATION UNIFIÉ")
    print("=" * 50)
    
    try:
        from lcpi.aep.calculations.population_unified import (
            PopulationCalculationsUnified,
            calculate_population_projection_unified,
            calculate_water_demand_unified,
            calculate_well_discharge_unified,
            calculate_population_evolution_unified
        )
        
        # Test 1: Projection démographique
        print("\n📊 Test 1: Projection démographique")
        data_pop = {
            "population_base": 1000,
            "taux_croissance": 0.037,
            "annees": 20,
            "methode": "malthus"
        }
        
        result = calculate_population_projection_unified(
            population_base=1000,
            taux_croissance=0.037,
            annees=20,
            methode="malthus"
        )
        print(f"✅ Résultat projection: {result['statut']}")
        if result['statut'] == 'SUCCES':
            print(f"   Population finale: {result['population_finale']:.0f} habitants")
            print(f"   Méthode: {result['methode']}")
        
        # Test 2: Calcul besoins en eau
        print("\n📊 Test 2: Calcul besoins en eau")
        data_besoins = {
            "population": 1000,
            "dotation_l_hab_j": 150,
            "coefficient_pointe": 1.5
        }
        
        result_besoins = calculate_water_demand_unified(data_besoins)
        print(f"✅ Besoin brut: {result_besoins['besoin_brut_m3j']:.1f} m³/j")
        print(f"   Besoin domestique: {result_besoins['besoin_domestique_m3j']:.1f} m³/j")
        print(f"   Besoin de pointe: {result_besoins['besoin_pointe_m3j']:.1f} m³/j")
        
        # Test 3: Calcul débit puits
        print("\n📊 Test 3: Calcul débit puits")
        data_puits = {
            "K": 1e-4,
            "H": 10.0,
            "h": 5.0,
            "R": 100.0,
            "r": 0.5,
            "type_nappe": "libre"
        }
        
        result_puits = calculate_well_discharge_unified(data_puits)
        print(f"✅ Débit puits: {result_puits['debit_m3s']:.3f} m³/s")
        print(f"   Débit: {result_puits['debit_ls']:.1f} L/s")
        print(f"   Méthode: {result_puits['methode']}")
        
        # Test 4: Évolution population
        print("\n📊 Test 4: Évolution population")
        data_evolution = {
            "population_initial": 1000,
            "taux_croissance": 0.037,
            "nombre_annees": 10
        }
        
        result_evolution = calculate_population_evolution_unified(data_evolution)
        print(f"✅ Population finale: {result_evolution['population_finale']:.0f} habitants")
        print(f"   Croissance totale: {result_evolution['croissance_totale']:.0f} habitants")
        print(f"   Taux croissance total: {result_evolution['taux_croissance_total_pct']:.1f}%")
        
        print("\n✅ Tous les tests population unifié ont réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test population unifié: {e}")
        return False

def test_reservoir_unified():
    """Test du module réservoir unifié."""
    print("\n🏗️ TEST DU MODULE RÉSERVOIR UNIFIÉ")
    print("=" * 50)
    
    try:
        from lcpi.aep.calculations.reservoir_unified import (
            ReservoirCalculationsUnified,
            dimension_reservoir_unified,
            comparer_scenarios_reservoir_unified,
            calculer_temps_sejour_reservoir_unified
        )
        
        # Test 1: Dimensionnement réservoir
        print("\n📊 Test 1: Dimensionnement réservoir")
        data_reservoir = {
            "volume_journalier_m3": 1000,
            "type_adduction": "continue",
            "forme_reservoir": "cylindrique",
            "type_zone": "ville_francaise_peu_importante"
        }
        
        result = dimension_reservoir_unified(data_reservoir, verbose=True)
        print(f"✅ Résultat dimensionnement: {result['statut']}")
        if result['statut'] == 'SUCCES':
            print(f"   Volume utile: {result['reservoir']['volume_utile_m3']:.1f} m³")
            print(f"   Capacité pratique: {result['reservoir']['capacite_pratique_m3']:.1f} m³")
            print(f"   Diamètre: {result['reservoir']['diametre_m']:.2f} m")
        
        # Test 2: Comparaison des scénarios
        print("\n📊 Test 2: Comparaison des scénarios")
        data_scenarios = {"volume_journalier_m3": 1000}
        
        result_scenarios = comparer_scenarios_reservoir_unified(data_scenarios)
        print(f"✅ Résultat comparaison: {len(result_scenarios)} scénarios testés")
        if 'analyse' in result_scenarios:
            print(f"   Volume min: {result_scenarios['analyse']['volume_min']:.1f} m³")
            print(f"   Volume max: {result_scenarios['analyse']['volume_max']:.1f} m³")
        
        # Test 3: Calcul temps de séjour
        print("\n📊 Test 3: Calcul temps de séjour")
        data_temps = {
            "volume_reservoir_m3": 1000,
            "debit_entree_m3h": 100
        }
        
        result_temps = calculer_temps_sejour_reservoir_unified(data_temps)
        print(f"✅ Temps de séjour: {result_temps['temps_sejour_h']:.1f} heures")
        print(f"   Vérification: {result_temps['verification']['recommandation']}")
        
        print("\n✅ Tous les tests réservoir unifié ont réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test réservoir unifié: {e}")
        return False

def test_pumping_unified():
    """Test du module pompage unifié."""
    print("\n⚡ TEST DU MODULE POMPAGE UNIFIÉ")
    print("=" * 50)
    
    try:
        from lcpi.aep.calculations.pumping_unified import (
            PumpingCalculationsUnified,
            dimension_pumping_unified,
            comparer_types_pompes_unified,
            calculer_cout_energie_pompage_unified
        )
        
        # Test 1: Dimensionnement pompage
        print("\n📊 Test 1: Dimensionnement pompage")
        data_pumping = {
            "debit_m3h": 100,
            "hmt_m": 50,
            "type_pompe": "centrifuge"
        }
        
        result = dimension_pumping_unified(data_pumping, verbose=True)
        print(f"✅ Résultat dimensionnement: {result['statut']}")
        if result['statut'] == 'SUCCES':
            print(f"   Puissance hydraulique: {result['pompage']['puissance_hydraulique_kw']:.1f} kW")
            print(f"   Puissance électrique: {result['pompage']['puissance_electrique_kw']:.1f} kW")
            print(f"   Puissance groupe: {result['pompage']['puissance_groupe_kva']:.1f} kVA")
        
        # Test 2: Comparaison des types de pompes
        print("\n📊 Test 2: Comparaison des types de pompes")
        data_comparison = {
            "debit_m3s": 0.1,
            "hmt_m": 50.0
        }
        
        result_comparison = comparer_types_pompes_unified(data_comparison)
        print(f"✅ Résultat comparaison: {len(result_comparison)} types testés")
        if 'analyse' in result_comparison:
            print(f"   Type min puissance: {result_comparison['analyse']['type_min_puissance']}")
            print(f"   Type max rendement: {result_comparison['analyse']['type_max_rendement']}")
        
        # Test 3: Calcul coût énergie
        print("\n📊 Test 3: Calcul coût énergie")
        data_cout = {
            "puissance_electrique_kw": 10.0,
            "temps_fonctionnement_h": 24.0,
            "prix_kwh": 0.15
        }
        
        result_cout = calculer_cout_energie_pompage_unified(data_cout)
        print(f"✅ Énergie consommée: {result_cout['energie_kwh']:.1f} kWh")
        print(f"   Coût: {result_cout['cout_euros']:.2f} €")
        
        print("\n✅ Tous les tests pompage unifié ont réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test pompage unifié: {e}")
        return False

def test_demand_unified():
    """Test du module demande unifié."""
    print("\n💧 TEST DU MODULE DEMANDE UNIFIÉ")
    print("=" * 50)
    
    try:
        from lcpi.aep.calculations.demand_unified import (
            DemandCalculationsUnified,
            calculate_water_demand_unified,
            calculate_water_demand_by_type_unified,
            compare_water_demand_scenarios_unified
        )
        
        # Test 1: Calcul demande en eau
        print("\n📊 Test 1: Calcul demande en eau")
        data_demand = {
            "population": 1000,
            "dotation_l_j_hab": 150,
            "coefficient_pointe": 1.5
        }
        
        result = calculate_water_demand_unified(
            population=1000,
            dotation_l_j_hab=150,
            coefficient_pointe=1.5
        )
        print(f"✅ Résultat demande: {result['statut']}")
        if result['statut'] == 'SUCCES':
            if 'besoin_brut_m3j' in result:
                print(f"   Besoin brut: {result['besoin_brut_m3j']:.1f} m³/j")
            if 'debit_pointe_m3s' in result:
                print(f"   Débit pointe: {result['debit_pointe_m3s']:.3f} m³/s")
            print(f"   Méthode: {result.get('methode', 'N/A')}")
        
        # Test 2: Calcul par type de consommation
        print("\n📊 Test 2: Calcul par type de consommation")
        data_type = {
            "population": 1000,
            "type_consommation": "zone_industrielle"
        }
        
        result_type = calculate_water_demand_by_type_unified(data_type)
        print(f"✅ Besoin industriel: {result_type['besoin_brut_m3j']:.1f} m³/j")
        print(f"   Type: {result_type['type_consommation']}")
        
        # Test 3: Comparaison des scénarios
        print("\n📊 Test 3: Comparaison des scénarios")
        data_scenarios = {
            "population": 1000,
            "scenarios": [
                {"type": "branchement_prive", "coefficient_pointe": 1.5},
                {"type": "borne_fontaine", "coefficient_pointe": 1.8},
                {"type": "zone_industrielle", "coefficient_pointe": 1.3}
            ]
        }
        
        result_scenarios = compare_water_demand_scenarios_unified(data_scenarios)
        print(f"✅ Résultat comparaison: {len(result_scenarios)} scénarios testés")
        if 'analyse' in result_scenarios:
            print(f"   Besoin min: {result_scenarios['analyse']['besoin_min']:.1f} m³/j")
            print(f"   Besoin max: {result_scenarios['analyse']['besoin_max']:.1f} m³/j")
            print(f"   Écart relatif: {result_scenarios['analyse']['ecart_relatif']:.1f}%")
        
        print("\n✅ Tous les tests demande unifié ont réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test demande unifié: {e}")
        return False

def test_integration():
    """Test d'intégration entre les modules."""
    print("\n🔗 TEST D'INTÉGRATION")
    print("=" * 50)
    
    try:
        # Simuler un workflow complet AEP
        print("\n📊 Workflow complet AEP:")
        
        # 1. Projection population
        population_finale = 1500  # Simulé
        
        # 2. Calcul besoins en eau
        data_besoins = {
            "population": population_finale,
            "dotation_l_hab_j": 150,
            "coefficient_pointe": 1.5
        }
        
        from lcpi.aep.calculations.population_unified import calculate_water_demand_unified
        result_besoins = calculate_water_demand_unified(data_besoins)
        besoin_brut = result_besoins['besoin_brut_m3j']
        
        print(f"   1. Population projetée: {population_finale} habitants")
        print(f"   2. Besoin brut: {besoin_brut:.1f} m³/j")
        
        # 3. Dimensionnement réseau
        debit_pointe = besoin_brut / 86400  # Conversion m³/j → m³/s
        
        data_network = {
            "debit_m3s": debit_pointe,
            "longueur_m": 2000,
            "materiau": "pvc",
            "perte_charge_max_m": 15.0,
            "methode": "hazen"
        }
        
        from lcpi.aep.calculations.network_unified import dimension_network_unified
        result_network = dimension_network_unified(data_network)
        
        if result_network['statut'] == 'SUCCES':
            diametre = result_network['reseau']['diametre_optimal_mm']
            vitesse = result_network['reseau']['vitesse_ms']
            print(f"   3. Diamètre réseau: {diametre} mm")
            print(f"   4. Vitesse écoulement: {vitesse:.2f} m/s")
        
        # 5. Dimensionnement réservoir
        data_reservoir = {
            "volume_journalier_m3": besoin_brut,
            "type_adduction": "continue",
            "forme_reservoir": "cylindrique"
        }
        
        from lcpi.aep.calculations.reservoir_unified import dimension_reservoir_unified
        result_reservoir = dimension_reservoir_unified(data_reservoir)
        
        if result_reservoir['statut'] == 'SUCCES':
            volume_reservoir = result_reservoir['reservoir']['capacite_pratique_m3']
            print(f"   5. Volume réservoir: {volume_reservoir:.1f} m³")
        
        # 6. Dimensionnement pompage
        data_pumping = {
            "debit_m3h": besoin_brut * 24 / 1000,  # Conversion m³/j → m³/h
            "hmt_m": 50,
            "type_pompe": "centrifuge"
        }
        
        from lcpi.aep.calculations.pumping_unified import dimension_pumping_unified
        result_pumping = dimension_pumping_unified(data_pumping)
        
        if result_pumping['statut'] == 'SUCCES':
            puissance = result_pumping['pompage']['puissance_electrique_kw']
            print(f"   6. Puissance pompage: {puissance:.1f} kW")
        
        print("\n✅ Workflow d'intégration réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 TEST DES MODULES UNIFIÉS AEP")
    print("=" * 60)
    print("Ce script teste les modules unifiés qui fusionnent les")
    print("fonctionnalités des versions basiques et enhanced.")
    print("=" * 60)
    
    # Tests individuels
    test_network = test_network_unified()
    test_population = test_population_unified()
    test_reservoir = test_reservoir_unified()
    test_pumping = test_pumping_unified()
    test_demand = test_demand_unified()
    
    # Test d'intégration
    test_integration_result = test_integration()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tests = [
        ("Réseau unifié", test_network),
        ("Population unifié", test_population),
        ("Réservoir unifié", test_reservoir),
        ("Pompage unifié", test_pumping),
        ("Demande unifié", test_demand),
        ("Intégration", test_integration_result)
    ]
    
    success_count = 0
    for test_name, result in tests:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests sont réussis ! Les modules unifiés fonctionnent correctement.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 