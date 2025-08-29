#!/usr/bin/env python3
"""
Test du solveur LCPI Hardy-Cross.

Ce script teste l'implémentation du solveur Hardy-Cross avec un réseau simple
et affiche la trace de convergence pour vérifier le bon fonctionnement.
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.core.solvers.lcpi_solver import LcpiHardyCrossSolver


def create_test_network():
    """
    Crée un réseau de test simple avec une boucle.
    
    Returns:
        Dictionnaire représentant le réseau de test
    """
    return {
        "noeuds": {
            "N1": {
                "role": "reservoir",
                "cote_m": 150.0,
                "demande_m3_s": 0.0,
                "pression_min_mce": 20,
                "pression_max_mce": 80
            },
            "N2": {
                "role": "consommation",
                "cote_m": 145.0,
                "demande_m3_s": 0.02,
                "profil_consommation": "residential",
                "pression_min_mce": 20,
                "pression_max_mce": 80
            },
            "N3": {
                "role": "consommation",
                "cote_m": 140.0,
                "demande_m3_s": 0.015,
                "profil_consommation": "commercial",
                "pression_min_mce": 20,
                "pression_max_mce": 80
            },
            "N4": {
                "role": "consommation",
                "cote_m": 138.0,
                "demande_m3_s": 0.01,
                "profil_consommation": "residential",
                "pression_min_mce": 20,
                "pression_max_mce": 80
            }
        },
        "conduites": {
            "C1": {
                "noeud_amont": "N1",
                "noeud_aval": "N2",
                "longueur_m": 500,
                "diametre_m": 0.2,
                "rugosite": 100,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            },
            "C2": {
                "noeud_amont": "N2",
                "noeud_aval": "N3",
                "longueur_m": 300,
                "diametre_m": 0.15,
                "rugosite": 120,
                "materiau": "pvc",
                "statut": "nouveau",
                "coefficient_frottement": "hazen_williams"
            },
            "C3": {
                "noeud_amont": "N3",
                "noeud_aval": "N4",
                "longueur_m": 250,
                "diametre_m": 0.125,
                "rugosite": 110,
                "materiau": "pvc",
                "statut": "nouveau",
                "coefficient_frottement": "hazen_williams"
            },
            "C4": {
                "noeud_amont": "N2",
                "noeud_aval": "N4",
                "longueur_m": 400,
                "diametre_m": 0.18,
                "rugosite": 115,
                "materiau": "acier",
                "statut": "existant",
                "coefficient_frottement": "hazen_williams"
            }
        },
        "parametres": {
            "tolerance": 1e-6,
            "max_iterations": 200,
            "methode": "hazen_williams"
        }
    }


def display_convergence_trace(solver_trace):
    """
    Affiche la trace de convergence de manière claire et structurée.
    
    Args:
        solver_trace: Liste des données de trace de convergence
    """
    print("\n" + "="*80)
    print("TRACE DE CONVERGENCE - ALGORITHME HARDY-CROSS")
    print("="*80)
    
    if not solver_trace:
        print("Aucune trace de convergence disponible.")
        return
    
    for trace in solver_trace:
        iteration = trace["iteration"]
        erreur_max = trace["erreur_max"]
        
        print(f"\n--- ITÉRATION {iteration} ---")
        print(f"Erreur maximale: {erreur_max:.2e}")
        
        # Afficher les débits courants
        print("\nDébits courants (m³/s):")
        for conduit_id, debit in trace["debits_courants"].items():
            print(f"  {conduit_id}: {debit:.6f}")
        
        # Afficher les pertes de charge
        print("\nPertes de charge (m):")
        for conduit_id, perte in trace["pertes_charge"].items():
            print(f"  {conduit_id}: {perte:.6f}")
        
        # Afficher les erreurs de boucles
        if trace["erreurs_boucles"]:
            print("\nErreurs de fermeture des boucles (m):")
            for boucle_id, erreur in trace["erreurs_boucles"].items():
                print(f"  {boucle_id}: {erreur:.6f}")
        
        # Afficher les corrections de débit
        if trace["corrections_debit"]:
            print("\nCorrections de débit (m³/s):")
            for boucle_id, correction in trace["corrections_debit"].items():
                print(f"  {boucle_id}: {correction:.6f}")
        
        print("-" * 50)


def test_solver():
    """
    Teste le solveur Hardy-Cross avec le réseau de test.
    """
    print("🧪 TEST DU SOLVEUR LCPI HARDY-CROSS")
    print("=" * 50)
    
    # Créer le réseau de test
    network = create_test_network()
    
    print(f"Réseau créé avec {len(network['noeuds'])} nœuds et {len(network['conduites'])} conduites")
    
    # Créer et configurer le solveur
    solver = LcpiHardyCrossSolver(tolerance=1e-6, max_iterations=200)
    
    print(f"Solveur créé avec tolérance: {solver.tolerance}, max itérations: {solver.max_iterations}")
    
    # Obtenir les informations du solveur
    solver_info = solver.get_solver_info()
    print(f"\nInformations du solveur:")
    for key, value in solver_info.items():
        print(f"  {key}: {value}")
    
    # Valider le réseau
    print("\n🔍 Validation du réseau...")
    validation = solver.validate_network(network)
    
    if validation["valid"]:
        print("✅ Réseau valide")
        if validation["warnings"]:
            print("⚠️  Avertissements:")
            for warning in validation["warnings"]:
                print(f"    - {warning}")
    else:
        print("❌ Réseau invalide:")
        for error in validation["errors"]:
            print(f"    - {error}")
        return
    
    # Exécuter la simulation
    print("\n🚀 Exécution de la simulation...")
    try:
        results = solver.run_simulation(network)
        
        print(f"\n📋 RÉSULTATS BRUTS:")
        print(f"Status: {results.get('status', 'N/A')}")
        print(f"Convergence: {results.get('convergence', 'N/A')}")
        print(f"Diagnostics: {results.get('diagnostics', 'N/A')}")
        
        if results["status"] == "success":
            print("✅ Simulation réussie!")
            
            # Afficher les résultats principaux
            print(f"\n📊 RÉSULTATS PRINCIPAUX:")
            print(f"  Convergence: {'Oui' if results['convergence']['converge'] else 'Non'}")
            print(f"  Itérations: {results['convergence']['iterations']}")
            print(f"  Erreur finale: {results['convergence']['tolerance_atteinte']:.2e}")
            print(f"  Temps d'exécution: {results['execution_time']:.4f} s")
            
            # Afficher les diagnostics
            diagnostics = results["diagnostics"]
            print(f"\n🔍 DIAGNOSTICS:")
            print(f"  Boucles détectées: {diagnostics['boucles_detectees']}")
            print(f"  Pression min: {diagnostics['pression_min']:.2f} m")
            print(f"  Pression max: {diagnostics['pression_max']:.2f} m")
            print(f"  Vitesse min: {diagnostics['vitesse_min']:.2f} m/s")
            print(f"  Vitesse max: {diagnostics['vitesse_max']:.2f} m/s")
            
            # Afficher les débits finaux
            print(f"\n💧 DÉBITS FINAUX (m³/s):")
            for conduit_id, debit in results["flows"].items():
                print(f"  {conduit_id}: {debit:.6f}")
            
            # Afficher les pressions finales
            print(f"\n📏 PRESSIONS FINALES (m):")
            for node_id, pression in results["pressures"].items():
                print(f"  {node_id}: {pression:.2f}")
            
            # Afficher les vitesses finales
            print(f"\n⚡ VITESSES FINALES (m/s):")
            for conduit_id, vitesse in results["velocities"].items():
                print(f"  {conduit_id}: {vitesse:.2f}")
            
            # Afficher la trace de convergence si disponible
            if "solver_trace" in results and results["solver_trace"]:
                display_convergence_trace(results["solver_trace"])
            else:
                print("\n⚠️  Aucune trace de convergence disponible")
                
        else:
            print("❌ Simulation échouée!")
            if "errors" in results:
                print("Erreurs:")
                for error in results["errors"]:
                    print(f"  - {error}")
    
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_solver()
