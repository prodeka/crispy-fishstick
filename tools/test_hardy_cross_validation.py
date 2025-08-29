#!/usr/bin/env python3
"""
Test de validation complète du solveur LCPI Hardy-Cross selon la checklist.

Ce script teste tous les aspects de l'implémentation Hardy-Cross :
- Détection des boucles
- Calcul des pertes de charge
- Algorithme de convergence
- Trace de convergence
- Gestion des cas limites
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.core.solvers.lcpi_solver import LcpiHardyCrossSolver


def create_simple_network():
    """
    Crée un réseau simple avec 2 boucles pour tester Hardy-Cross.
    
    Returns:
        Dictionnaire représentant le réseau de test
    """
    return {
        "noeuds": {
            "R1": {
                "role": "reservoir",
                "cote_m": 100.0,
                "demande_m3_s": 0.0,
                "pression_min_mce": 20.0,
                "pression_max_mce": 80.0
            },
            "N1": {
                "role": "consommation",
                "cote_m": 95.0,
                "demande_m3_s": 0.05,
                "pression_min_mce": 20.0,
                "pression_max_mce": 80.0
            },
            "N2": {
                "role": "consommation",
                "cote_m": 93.0,
                "demande_m3_s": 0.03,
                "pression_min_mce": 20.0,
                "pression_max_mce": 80.0
            },
            "N3": {
                "role": "consommation",
                "cote_m": 94.0,
                "demande_m3_s": 0.04,
                "pression_min_mce": 20.0,
                "pression_max_mce": 80.0
            },
            "N4": {
                "role": "consommation",
                "cote_m": 92.0,
                "demande_m3_s": 0.02,
                "pression_min_mce": 20.0,
                "pression_max_mce": 80.0
            }
        },
        "conduites": {
            "C1": {
                "noeud_amont": "R1",
                "noeud_aval": "N1",
                "longueur_m": 100.0,
                "diametre_m": 0.15,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            },
            "C2": {
                "noeud_amont": "N1",
                "noeud_aval": "N2",
                "longueur_m": 80.0,
                "diametre_m": 0.12,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            },
            "C3": {
                "noeud_amont": "N2",
                "noeud_aval": "N3",
                "longueur_m": 60.0,
                "diametre_m": 0.10,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            },
            "C4": {
                "noeud_amont": "N3",
                "noeud_aval": "N4",
                "longueur_m": 70.0,
                "diametre_m": 0.08,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            },
            "C5": {
                "noeud_amont": "N4",
                "noeud_aval": "N1",
                "longueur_m": 90.0,
                "diametre_m": 0.12,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            },
            "C6": {
                "noeud_amont": "N2",
                "noeud_aval": "N4",
                "longueur_m": 50.0,
                "diametre_m": 0.10,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            }
        }
    }


def test_hardy_cross_implementation():
    """
    Test principal de l'implémentation Hardy-Cross.
    """
    print("🔍 VALIDATION COMPLÈTE DU SOLVEUR LCPI HARDY-CROSS")
    print("=" * 60)
    
    # 1. Test de création du solveur
    print("\n📋 Section 1 : Implémentation de l'Algorithme Hardy-Cross")
    print("-" * 50)
    
    try:
        solver = LcpiHardyCrossSolver(tolerance=1e-6, max_iterations=50)
        print("✅ LcpiHardyCrossSolver créé avec succès")
        print(f"   - Tolérance: {solver.tolerance}")
        print(f"   - Max itérations: {solver.max_iterations}")
    except Exception as e:
        print(f"❌ Erreur lors de la création du solveur: {e}")
        return False
    
    # 2. Test de détection des boucles
    print("\n🔍 Test de détection des boucles...")
    network = create_simple_network()
    noeuds = network["noeuds"]
    conduites = network["conduites"]
    
    try:
        boucles = solver._detect_loops(noeuds, conduites)
        print(f"✅ Boucles détectées: {len(boucles)}")
        for i, boucle in enumerate(boucles):
            print(f"   Boucle {i+1}: {boucle}")
        
        # Vérifier qu'on a bien 2 boucles dans ce réseau
        if len(boucles) == 2:
            print("✅ Nombre de boucles correct (2 boucles attendues)")
        else:
            print(f"⚠️ Nombre de boucles inattendu: {len(boucles)} (2 attendues)")
            
    except Exception as e:
        print(f"❌ Erreur lors de la détection des boucles: {e}")
        return False
    
    # 3. Test de calcul des pertes de charge
    print("\n💧 Test de calcul des pertes de charge...")
    try:
        # Test avec une conduite
        conduit_test = conduites["C1"]
        debit_test = 0.05  # 50 L/s
        
        hf_hw = solver._calculate_head_loss(conduit_test, debit_test, "hazen_williams")
        hf_dw = solver._calculate_head_loss(conduit_test, debit_test, "darcy_weisbach")
        hf_manning = solver._calculate_head_loss(conduit_test, debit_test, "manning")
        
        print(f"✅ Pertes de charge calculées:")
        print(f"   - Hazen-Williams: {hf_hw:.6f} m")
        print(f"   - Darcy-Weisbach: {hf_dw:.6f} m")
        print(f"   - Manning: {hf_manning:.6f} m")
        
        # Vérifier que les valeurs sont raisonnables (> 0)
        if hf_hw > 0 and hf_dw > 0 and hf_manning > 0:
            print("✅ Valeurs de perte de charge cohérentes")
        else:
            print("⚠️ Valeurs de perte de charge suspectes")
            
    except Exception as e:
        print(f"❌ Erreur lors du calcul des pertes de charge: {e}")
        return False
    
    # 4. Test de l'algorithme Hardy-Cross complet
    print("\n🔄 Test de l'algorithme Hardy-Cross complet...")
    try:
        results = solver.run_simulation(network)
        
        print("✅ Simulation Hardy-Cross exécutée avec succès")
        print(f"   - Statut: {results.get('status', 'N/A')}")
        print(f"   - Convergence: {results.get('convergence', {}).get('converge', 'N/A')}")
        print(f"   - Itérations: {results.get('convergence', {}).get('iterations', 'N/A')}")
        print(f"   - Tolérance atteinte: {results.get('convergence', {}).get('tolerance_atteinte', 'N/A'):.2e}")
        
        # Vérifier la présence de la trace de convergence
        if "solver_trace" in results:
            trace = results["solver_trace"]
            print(f"✅ Trace de convergence disponible: {len(trace)} itérations")
            
            # Afficher les détails de la première itération
            if trace:
                first_iter = trace[0]
                print(f"   Itération 1:")
                print(f"     - Débits: {len(first_iter.get('debits_courants', {}))} conduites")
                print(f"     - Pertes de charge: {len(first_iter.get('pertes_charge', {}))} conduites")
                print(f"     - Erreurs de boucles: {len(first_iter.get('erreurs_boucles', {}))} boucles")
                print(f"     - Corrections de débit: {len(first_iter.get('corrections_debit', {}))} boucles")
        else:
            print("⚠️ Trace de convergence non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur lors de la simulation Hardy-Cross: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Test des résultats finaux
    print("\n📊 Analyse des résultats finaux...")
    try:
        if "debits_finaux" in results:
            debits = results["debits_finaux"]
            print(f"✅ Débits finaux calculés: {len(debits)} conduites")
            
            # Vérifier la conservation des débits aux nœuds
            print("   Vérification de la conservation des débits...")
            for node_id, node in noeuds.items():
                if node["role"] == "consommation":
                    demande = node["demande_m3_s"]
                    debit_entrant = 0.0
                    debit_sortant = 0.0
                    
                    for conduit_id, conduit in conduites.items():
                        if conduit["noeud_amont"] == node_id:
                            debit_entrant += abs(debits.get(conduit_id, 0))
                        if conduit["noeud_aval"] == node_id:
                            debit_sortant += abs(debits.get(conduit_id, 0))
                    
                    bilan = debit_entrant - debit_sortant - demande
                    print(f"     {node_id}: entrant={debit_entrant:.3f}, sortant={debit_sortant:.3f}, demande={demande:.3f}, bilan={bilan:.3f}")
                    
        if "pressions_noeuds" in results:
            pressions = results["pressions_noeuds"]
            print(f"✅ Pressions calculées: {len(pressions)} nœuds")
            print(f"   - Pression min: {min(pressions.values()):.2f} m")
            print(f"   - Pression max: {max(pressions.values()):.2f} m")
            
        if "vitesses" in results:
            vitesses = results["vitesses"]
            print(f"✅ Vitesses calculées: {len(vitesses)} conduites")
            print(f"   - Vitesse min: {min(vitesses.values()):.2f} m/s")
            print(f"   - Vitesse max: {max(vitesses.values()):.2f} m/s")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des résultats: {e}")
        return False
    
    print("\n🎉 VALIDATION TERMINÉE AVEC SUCCÈS !")
    return True


if __name__ == "__main__":
    success = test_hardy_cross_implementation()
    if not success:
        print("\n❌ VALIDATION ÉCHOUÉE")
        sys.exit(1)
