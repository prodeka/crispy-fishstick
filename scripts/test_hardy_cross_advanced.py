#!/usr/bin/env python3
"""Test de l'algorithme Hardy-Cross avancé"""

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.lcpi.aep.calculations.hardy_cross_enhanced import HardyCrossEnhanced
from scripts.generate_paris_network import ParisNetworkGenerator

def test_advanced_algorithm():
    """Teste l'algorithme avancé"""
    print("🌊 Génération du réseau Paris...")
    
    # Générer le réseau
    generator = ParisNetworkGenerator()
    network_data = generator.generate_network_data()
    
    # Extraire les tronçons
    pipes = list(network_data["network"]["pipes"].values())
    troncons = []
    
    for pipe in pipes:
        troncon = {
            "id": pipe["id"],
            "noeud_amont": pipe["noeud_amont"],
            "noeud_aval": pipe["noeud_aval"],
            "longueur": pipe["longueur"],
            "diametre": pipe["diametre"],
            "coefficient_rugosite": pipe["coefficient_rugosite"],
            "debit_initial": pipe["debit_initial"]
        }
        troncons.append(troncon)
    
    print(f"📊 Réseau: {len(network_data['network']['nodes'])} nœuds, {len(troncons)} conduites")
    
    # Tester la détection de boucles
    print("\n🔍 Test de la détection de boucles...")
    hardy_cross = HardyCrossEnhanced()
    
    start_time = time.time()
    loops = hardy_cross._identify_loops(troncons)
    detection_time = time.time() - start_time
    
    print(f"✅ Boucles détectées: {len(loops)}")
    print(f"⏱️  Temps: {detection_time:.4f} secondes")
    
    # Analyser les boucles
    loop_sizes = [len(loop) - 1 for loop in loops]
    avg_size = sum(loop_sizes) / len(loop_sizes) if loop_sizes else 0
    
    print(f"📈 Taille moyenne: {avg_size:.1f} nœuds")
    print(f"🎯 Plus grande boucle: {max(loop_sizes) if loop_sizes else 0} nœuds")
    
    return {
        "total_loops": len(loops),
        "detection_time": detection_time,
        "avg_loop_size": avg_size,
        "max_loop_size": max(loop_sizes) if loop_sizes else 0
    }

if __name__ == "__main__":
    results = test_advanced_algorithm()
    print(f"\n🎉 Test terminé: {results['total_loops']} boucles détectées") 