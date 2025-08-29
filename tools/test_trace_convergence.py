#!/usr/bin/env python3
"""
Test de la transparence mathématique et de la trace de convergence.

Ce script teste l'affichage détaillé de la trace de convergence
pour vérifier que tous les calculs sont transparents.
"""

import sys
import json
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.core.solvers.lcpi_solver import LcpiHardyCrossSolver


def create_simple_network():
    """
    Crée un réseau très simple avec une seule boucle pour faciliter l'analyse.
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
                "noeud_aval": "R1",
                "longueur_m": 120.0,
                "diametre_m": 0.10,
                "rugosite": 100.0,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            }
        }
    }


def display_convergence_trace(trace_data, verbose=True):
    """
    Affiche la trace de convergence de manière détaillée.
    
    Args:
        trace_data: Liste des données de trace de convergence
        verbose: Si True, affiche tous les détails
    """
    print(f"\n📊 TRACE DE CONVERGENCE DÉTAILLÉE ({len(trace_data)} itérations)")
    print("=" * 80)
    
    for i, iteration in enumerate(trace_data):
        print(f"\n🔄 ITÉRATION {iteration['iteration']}")
        print("-" * 40)
        
        # Afficher l'erreur maximale
        erreur_max = iteration.get('erreur_max', 0.0)
        print(f"📈 Erreur maximale: {erreur_max:.6f} m")
        
        # Afficher les corrections de débit pour chaque boucle
        corrections = iteration.get('corrections_debit', {})
        if corrections:
            print("💧 Corrections de débit (ΔQ):")
            for boucle_id, correction in corrections.items():
                print(f"   {boucle_id}: {correction:.6e} m³/s")
        
        # Afficher les erreurs de fermeture des boucles
        erreurs_boucles = iteration.get('erreurs_boucles', {})
        if erreurs_boucles:
            print("🔍 Erreurs de fermeture des boucles:")
            for boucle_id, erreur in erreurs_boucles.items():
                print(f"   {boucle_id}: {erreur:.6f} m")
        
        # En mode verbose, afficher les débits et pertes de charge
        if verbose and i < 3:  # Limiter aux 3 premières itérations pour éviter le spam
            print("📊 Détails des débits et pertes de charge:")
            debits = iteration.get('debits_courants', {})
            pertes = iteration.get('pertes_charge', {})
            
            for conduit_id in debits:
                debit = debits[conduit_id]
                perte = pertes.get(conduit_id, 0.0)
                print(f"   {conduit_id}: Q={debit:.6f} m³/s, hf={perte:.6f} m")
        
        # Afficher la progression de convergence
        if i > 0:
            prev_iter = trace_data[i-1]
            prev_erreur = prev_iter.get('erreur_max', 0.0)
            if erreur_max > 0 and prev_erreur > 0:
                ratio = erreur_max / prev_erreur
                if ratio < 1.0:
                    print(f"✅ Convergence: erreur réduite de {ratio:.2%}")
                else:
                    print(f"⚠️ Pas de convergence: erreur augmentée de {ratio:.2%}")


def test_mathematical_transparency():
    """
    Test principal de la transparence mathématique.
    """
    print("🔍 TEST DE LA TRANSPARENCE MATHÉMATIQUE")
    print("=" * 50)
    
    # Créer le solveur avec une tolérance plus élevée pour la démonstration
    solver = LcpiHardyCrossSolver(tolerance=1e-3, max_iterations=20)
    
    # Créer le réseau de test
    network = create_simple_network()
    
    print("📋 Réseau de test créé:")
    print(f"   - Nœuds: {len(network['noeuds'])}")
    print(f"   - Conduites: {len(network['conduites'])}")
    
    # Détecter les boucles
    noeuds = network["noeuds"]
    conduites = network["conduites"]
    boucles = solver._detect_loops(noeuds, conduites)
    
    print(f"🔍 Boucles détectées: {len(boucles)}")
    for i, boucle in enumerate(boucles):
        print(f"   Boucle {i+1}: {boucle}")
    
    # Exécuter la simulation
    print("\n🔄 Exécution de la simulation Hardy-Cross...")
    results = solver.run_simulation(network)
    
    # Afficher les résultats de base
    print(f"\n📊 RÉSULTATS DE LA SIMULATION:")
    print(f"   - Statut: {results.get('status', 'N/A')}")
    print(f"   - Convergence: {results.get('convergence', {}).get('converge', 'N/A')}")
    print(f"   - Itérations: {results.get('convergence', {}).get('iterations', 'N/A')}")
    print(f"   - Tolérance finale: {results.get('convergence', {}).get('tolerance_atteinte', 'N/A'):.2e}")
    
    # Afficher la trace de convergence
    if "solver_trace" in results:
        trace = results["solver_trace"]
        display_convergence_trace(trace, verbose=True)
        
        # Analyser la qualité de la convergence
        print(f"\n📈 ANALYSE DE LA CONVERGENCE:")
        if trace:
            erreurs = [it.get('erreur_max', 0.0) for it in trace]
            print(f"   - Erreur initiale: {erreurs[0]:.6f} m")
            print(f"   - Erreur finale: {erreurs[-1]:.6f} m")
            
            if len(erreurs) > 1:
                reduction = (erreurs[0] - erreurs[-1]) / erreurs[0] * 100
                print(f"   - Réduction totale: {reduction:.2f}%")
                
                # Vérifier la monotonie de la convergence
                monotone = all(erreurs[i] >= erreurs[i+1] for i in range(len(erreurs)-1))
                print(f"   - Convergence monotone: {'✅ Oui' if monotone else '❌ Non'}")
        
        # Afficher les résultats finaux
        print(f"\n🎯 RÉSULTATS FINAUX:")
        if "debits_finaux" in results:
            debits = results["debits_finaux"]
            print(f"   Débits finaux:")
            for conduit_id, debit in debits.items():
                print(f"     {conduit_id}: {debit:.6f} m³/s")
        
        if "pressions_noeuds" in results:
            pressions = results["pressions_noeuds"]
            print(f"   Pressions aux nœuds:")
            for node_id, pression in pressions.items():
                print(f"     {node_id}: {pression:.2f} m")
        
        if "vitesses" in results:
            vitesses = results["vitesses"]
            print(f"   Vitesses dans les conduites:")
            for conduit_id, vitesse in vitesses.items():
                print(f"     {conduit_id}: {vitesse:.2f} m/s")
    
    else:
        print("❌ Trace de convergence non trouvée dans les résultats")
    
    return True


if __name__ == "__main__":
    success = test_mathematical_transparency()
    if not success:
        print("\n❌ TEST ÉCHOUÉ")
        sys.exit(1)
