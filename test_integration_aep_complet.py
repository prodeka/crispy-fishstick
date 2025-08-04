#!/usr/bin/env python3
"""
Test d'intégration complet pour les workflows AEP unifiés
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_workflow_aep_complet():
    """Test d'un workflow AEP complet : Population → Demande → Réseau → Réservoir → Pompage"""
    print("🔵 TEST WORKFLOW AEP COMPLET")
    print("=" * 60)
    print("Ce test simule un projet AEP complet avec tous les modules unifiés.")
    print("=" * 60)
    
    try:
        # Import des modules unifiés
        from lcpi.aep.calculations.population_unified import calculate_population_projection_unified
        from lcpi.aep.calculations.demand_unified import calculate_water_demand_unified
        from lcpi.aep.calculations.network_unified import dimension_network_unified
        from lcpi.aep.calculations.reservoir_unified import dimension_reservoir_unified
        from lcpi.aep.calculations.pumping_unified import dimension_pumping_unified
        
        print("✅ Modules unifiés importés avec succès")
        
        # Données du projet
        population_initial = 5000
        taux_croissance = 0.025
        annees_projection = 15
        
        print(f"\n📊 DONNÉES DU PROJET:")
        print(f"   Population initiale: {population_initial} habitants")
        print(f"   Taux de croissance: {taux_croissance:.1%}")
        print(f"   Période de projection: {annees_projection} ans")
        
        # =============================================================================
        # ÉTAPE 1: PROJECTION DÉMOGRAPHIQUE
        # =============================================================================
        print(f"\n🔢 ÉTAPE 1: PROJECTION DÉMOGRAPHIQUE")
        print("-" * 40)
        
        resultat_population = calculate_population_projection_unified(
            population_base=population_initial,
            taux_croissance=taux_croissance,
            annees=annees_projection,
            methode="malthus",
            verbose=True
        )
        
        if resultat_population['statut'] == 'SUCCES':
            population_finale = resultat_population['population_finale']
            print(f"✅ Population projetée: {population_finale:.0f} habitants")
        else:
            print(f"❌ Erreur projection: {resultat_population['message']}")
            return False
        
        # =============================================================================
        # ÉTAPE 2: CALCUL DE DEMANDE EN EAU
        # =============================================================================
        print(f"\n💧 ÉTAPE 2: CALCUL DE DEMANDE EN EAU")
        print("-" * 40)
        
        resultat_demande = calculate_water_demand_unified(
            population=population_finale,
            dotation_l_j_hab=180,  # Dotation élevée pour zone urbaine
            coefficient_pointe=1.8,  # Coefficient de pointe élevé
            verbose=True
        )
        
        if resultat_demande['statut'] == 'SUCCES':
            besoin_brut = resultat_demande['besoin_brut_m3j']
            debit_pointe = resultat_demande['debit_pointe_m3s']
            print(f"✅ Besoin brut: {besoin_brut:.1f} m³/j")
            print(f"✅ Débit de pointe: {debit_pointe:.3f} m³/s")
        else:
            print(f"❌ Erreur demande: {resultat_demande['message']}")
            return False
        
        # =============================================================================
        # ÉTAPE 3: DIMENSIONNEMENT RÉSEAU
        # =============================================================================
        print(f"\n🔧 ÉTAPE 3: DIMENSIONNEMENT RÉSEAU")
        print("-" * 40)
        
        # Calculer le débit pour le dimensionnement réseau (débit de pointe)
        debit_reseau = debit_pointe
        
        resultat_reseau = dimension_network_unified({
            "debit_m3s": debit_reseau,
            "longueur_m": 2500,  # Longueur typique d'un réseau de distribution
            "materiau": "fonte",
            "perte_charge_max_m": 15.0,  # Perte de charge maximale
            "methode": "darcy"
        }, verbose=True)
        
        if resultat_reseau['statut'] == 'SUCCES':
            diametre = resultat_reseau['reseau']['diametre_optimal_mm']
            vitesse = resultat_reseau['reseau']['vitesse_ms']
            print(f"✅ Diamètre optimal: {diametre} mm")
            print(f"✅ Vitesse: {vitesse:.2f} m/s")
        else:
            print(f"❌ Erreur réseau: {resultat_reseau['message']}")
            return False
        
        # =============================================================================
        # ÉTAPE 4: DIMENSIONNEMENT RÉSERVOIR
        # =============================================================================
        print(f"\n🏗️ ÉTAPE 4: DIMENSIONNEMENT RÉSERVOIR")
        print("-" * 40)
        
        resultat_reservoir = dimension_reservoir_unified({
            "volume_journalier_m3": besoin_brut,
            "type_adduction": "continue",
            "forme_reservoir": "cylindrique",
            "type_zone": "ville_francaise_peu_importante"
        }, verbose=True)
        
        if resultat_reservoir['statut'] == 'SUCCES':
            volume_utile = resultat_reservoir['reservoir']['volume_utile_m3']
            capacite_pratique = resultat_reservoir['reservoir']['capacite_pratique_m3']
            print(f"✅ Volume utile: {volume_utile:.1f} m³")
            print(f"✅ Capacité pratique: {capacite_pratique:.1f} m³")
        else:
            print(f"❌ Erreur réservoir: {resultat_reservoir['message']}")
            return False
        
        # =============================================================================
        # ÉTAPE 5: DIMENSIONNEMENT POMPAGE
        # =============================================================================
        print(f"\n⚡ ÉTAPE 5: DIMENSIONNEMENT POMPAGE")
        print("-" * 40)
        
        # Calculer le débit de pompage (débit journalier en m³/h)
        debit_pompage = (besoin_brut * 1000) / 24  # Conversion m³/j → m³/h
        
        resultat_pompage = dimension_pumping_unified({
            "debit_m3h": debit_pompage,
            "hmt_m": 45.0,  # Hauteur manométrique typique
            "type_pompe": "centrifuge",
            "rendement_pompe": 0.78
        }, verbose=True)
        
        if resultat_pompage['statut'] == 'SUCCES':
            puissance_electrique = resultat_pompage['pompage']['puissance_electrique_kw']
            puissance_groupe = resultat_pompage['pompage']['puissance_groupe_kva']
            print(f"✅ Puissance électrique: {puissance_electrique:.1f} kW")
            print(f"✅ Puissance groupe: {puissance_groupe:.1f} kVA")
        else:
            print(f"❌ Erreur pompage: {resultat_pompage['message']}")
            return False
        
        # =============================================================================
        # RÉSUMÉ DU PROJET
        # =============================================================================
        print(f"\n📊 RÉSUMÉ DU PROJET AEP")
        print("=" * 60)
        
        resume = {
            "population": {
                "initiale": population_initial,
                "finale": population_finale,
                "croissance": ((population_finale - population_initial) / population_initial) * 100
            },
            "demande": {
                "besoin_brut_m3j": besoin_brut,
                "debit_pointe_m3s": debit_pointe
            },
            "reseau": {
                "diametre_mm": diametre,
                "vitesse_ms": vitesse,
                "longueur_m": 2500
            },
            "reservoir": {
                "volume_utile_m3": volume_utile,
                "capacite_pratique_m3": capacite_pratique
            },
            "pompage": {
                "puissance_electrique_kw": puissance_electrique,
                "puissance_groupe_kva": puissance_groupe
            }
        }
        
        print(f"👥 POPULATION:")
        print(f"   Initiale: {resume['population']['initiale']:,} habitants")
        print(f"   Finale: {resume['population']['finale']:.0f} habitants")
        print(f"   Croissance: {resume['population']['croissance']:.1f}%")
        
        print(f"\n💧 DEMANDE EN EAU:")
        print(f"   Besoin brut: {resume['demande']['besoin_brut_m3j']:.1f} m³/j")
        print(f"   Débit de pointe: {resume['demande']['debit_pointe_m3s']:.3f} m³/s")
        
        print(f"\n🔧 RÉSEAU DE DISTRIBUTION:")
        print(f"   Diamètre: {resume['reseau']['diametre_mm']} mm")
        print(f"   Vitesse: {resume['reseau']['vitesse_ms']:.2f} m/s")
        print(f"   Longueur: {resume['reseau']['longueur_m']:,} m")
        
        print(f"\n🏗️ RÉSERVOIR DE STOCKAGE:")
        print(f"   Volume utile: {resume['reservoir']['volume_utile_m3']:.1f} m³")
        print(f"   Capacité pratique: {resume['reservoir']['capacite_pratique_m3']:.1f} m³")
        
        print(f"\n⚡ ÉQUIPEMENTS DE POMPAGE:")
        print(f"   Puissance électrique: {resume['pompage']['puissance_electrique_kw']:.1f} kW")
        print(f"   Puissance groupe: {resume['pompage']['puissance_groupe_kva']:.1f} kVA")
        
        # Sauvegarder le résumé
        with open("resume_projet_aep.json", "w", encoding="utf-8") as f:
            json.dump(resume, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résumé sauvegardé dans 'resume_projet_aep.json'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_workflow_scenarios():
    """Test de différents scénarios AEP"""
    print("\n🔵 TEST DE SCÉNARIOS AEP")
    print("=" * 60)
    
    scenarios = [
        {
            "nom": "Petite commune rurale",
            "population": 1500,
            "taux_croissance": 0.01,
            "dotation": 120,
            "coefficient_pointe": 1.3
        },
        {
            "nom": "Ville moyenne",
            "population": 15000,
            "taux_croissance": 0.02,
            "dotation": 160,
            "coefficient_pointe": 1.6
        },
        {
            "nom": "Grande agglomération",
            "population": 50000,
            "taux_croissance": 0.03,
            "dotation": 200,
            "coefficient_pointe": 1.8
        }
    ]
    
    try:
        from lcpi.aep.calculations.population_unified import calculate_population_projection_unified
        from lcpi.aep.calculations.demand_unified import calculate_water_demand_unified
        
        success_count = 0
        total_count = len(scenarios)
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📊 Scénario {i}/{total_count}: {scenario['nom']}")
            print(f"   Population: {scenario['population']:,} habitants")
            print(f"   Taux croissance: {scenario['taux_croissance']:.1%}")
            
            # Projection démographique
            resultat_pop = calculate_population_projection_unified(
                population_base=scenario['population'],
                taux_croissance=scenario['taux_croissance'],
                annees=10,
                methode="malthus"
            )
            
            if resultat_pop['statut'] == 'SUCCES':
                population_finale = resultat_pop['population_finale']
                
                # Calcul de demande
                resultat_demande = calculate_water_demand_unified(
                    population=population_finale,
                    dotation_l_j_hab=scenario['dotation'],
                    coefficient_pointe=scenario['coefficient_pointe']
                )
                
                if resultat_demande['statut'] == 'SUCCES':
                    besoin_brut = resultat_demande['besoin_brut_m3j']
                    print(f"   ✅ Population finale: {population_finale:.0f} habitants")
                    print(f"   ✅ Besoin brut: {besoin_brut:.1f} m³/j")
                    success_count += 1
                else:
                    print(f"   ❌ Erreur demande: {resultat_demande['message']}")
            else:
                print(f"   ❌ Erreur projection: {resultat_pop['message']}")
        
        print(f"\n📈 Résultat scenarios: {success_count}/{total_count} réussis")
        return success_count == total_count
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test d'intégration."""
    print("🚀 TEST D'INTÉGRATION AEP COMPLET")
    print("=" * 60)
    print("Ce script teste les workflows AEP complets avec tous les modules unifiés.")
    print("=" * 60)
    
    # Tests
    test_workflow_result = test_workflow_aep_complet()
    test_scenarios_result = test_workflow_scenarios()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION")
    print("=" * 60)
    
    tests = [
        ("Workflow AEP complet", test_workflow_result),
        ("Scénarios multiples", test_scenarios_result)
    ]
    
    success_count = 0
    for test_name, result in tests:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests d'intégration sont réussis !")
        print("✅ Les modules AEP unifiés fonctionnent parfaitement ensemble.")
        return True
    else:
        print("⚠️ Certains tests d'intégration ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 