#!/usr/bin/env python3
"""
Script de débogage pour analyser la structure du réseau.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.core.solvers.lcpi_solver import LcpiHardyCrossSolver


def create_test_network():
    """
    Crée un réseau de test simple avec une boucle.
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
        }
    }


def analyze_network_structure():
    """
    Analyse la structure du réseau pour comprendre la détection des boucles.
    """
    print("🔍 ANALYSE DE LA STRUCTURE DU RÉSEAU")
    print("=" * 50)
    
    network = create_test_network()
    solver = LcpiHardyCrossSolver()
    
    # Analyser la structure
    noeuds = network["noeuds"]
    conduites = network["conduites"]
    
    print(f"Nombre de nœuds: {len(noeuds)}")
    print(f"Nombre de conduites: {len(conduites)}")
    
    print("\n📋 NŒUDS:")
    for node_id, node in noeuds.items():
        print(f"  {node_id}: {node['role']} (cote: {node['cote_m']} m)")
    
    print("\n🔗 CONDUITES:")
    for conduit_id, conduit in conduites.items():
        print(f"  {conduit_id}: {conduit['noeud_amont']} -> {conduit['noeud_aval']}")
        print(f"    Longueur: {conduit['longueur_m']} m, Diamètre: {conduit['diametre_m']} m")
    
    # Construire le graphe d'adjacence manuellement
    print("\n🕸️  GRAPHE D'ADJACENCE:")
    graph = {}
    for conduit_id, conduit in conduites.items():
        noeud_amont = conduit["noeud_amont"]
        noeud_aval = conduit["noeud_aval"]
        
        if noeud_amont not in graph:
            graph[noeud_amont] = []
        if noeud_aval not in graph:
            graph[noeud_aval] = []
            
        graph[noeud_amont].append(noeud_aval)
        graph[noeud_aval].append(noeud_amont)
    
    for node, neighbors in graph.items():
        print(f"  {node} -> {neighbors}")
    
    # Analyser les cycles possibles
    print("\n🔄 CYCLES POSSIBLES:")
    
    # Cycle principal: N1 -> N2 -> N3 -> N4 -> N2 (via C4)
    print("  Cycle principal: N1 -> N2 -> N3 -> N4 -> N2")
    print("    Conduites: C1 -> C2 -> C3 -> C4")
    
    # Vérifier s'il y a d'autres cycles
    # N2 -> N3 -> N4 -> N2 (sous-cycle)
    print("  Sous-cycle: N2 -> N3 -> N4 -> N2")
    print("    Conduites: C2 -> C3 -> C4")
    
    # Analyser la méthode de détection des boucles
    print("\n🔍 MÉTHODE DE DÉTECTION DES BOUCLES:")
    print("  L'algorithme DFS peut détecter plusieurs cycles pour le même ensemble de nœuds")
    print("  car il peut commencer la recherche depuis différents nœuds.")
    
    # Tester la détection des boucles
    print("\n🧪 TEST DE DÉTECTION DES BOUCLES:")
    try:
        boucles = solver._detect_loops(noeuds, conduites)
        print(f"  Nombre de boucles détectées: {len(boucles)}")
        
        for i, boucle in enumerate(boucles):
            print(f"  Boucle {i}: {boucle}")
            
    except Exception as e:
        print(f"  Erreur lors de la détection: {e}")


if __name__ == "__main__":
    analyze_network_structure()
