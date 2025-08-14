#!/usr/bin/env python3
"""Test Hardy-Cross avec itérations visibles"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.calculations.hardy_cross_enhanced import hardy_cross_network_enhanced
import sys
sys.path.append('scripts')
from generate_paris_network import ParisNetworkGenerator

def test_hardy_cross_iterations():
    """Test Hardy-Cross avec itérations visibles"""
    
    print("🔧 Test Hardy-Cross avec itérations visibles")
    print("=" * 50)
    
    # Générer réseau
    generator = ParisNetworkGenerator()
    network_data = generator.generate_network_data()
    
    # Convertir structure
    hardy_cross_data = {
        "metadata": network_data["metadata"],
        "troncons": list(network_data["network"]["pipes"].values()),
        "noeuds": list(network_data["network"]["nodes"].values())
    }
    
    print(f"📊 Réseau : {len(hardy_cross_data['troncons'])} tronçons")
    
    # Test avec différentes tolérances
    tolérances = [1e-3, 1e-4, 1e-5, 1e-6]
    
    for tolerance in tolérances:
        print(f"\n🔧 Test avec tolérance = {tolerance}")
        
        try:
            results = hardy_cross_network_enhanced(
                hardy_cross_data, max_iterations=20, tolerance=tolerance
            )
            
            iterations = results.get('iterations', [])
            convergence = results.get('convergence', False)
            
            print(f"   - Itérations : {len(iterations)}")
            print(f"   - Convergence : {convergence}")
            
            if iterations:
                print(f"   - Première itération :")
                first_iter = iterations[0]
                corrections = first_iter.get('corrections', {})
                print(f"     - Corrections calculées : {len(corrections)}")
                print(f"     - Corrections totales : {first_iter.get('corrections_total', 0):.6f}")
                
                # Afficher quelques corrections
                for i, (boucle_id, correction) in enumerate(list(corrections.items())[:3]):
                    delta_Q = correction.get('delta_Q', 0)
                    print(f"     - {boucle_id} : ΔQ = {delta_Q:.6f}")
            
        except Exception as e:
            print(f"   ❌ Erreur : {e}")
    
    return True

if __name__ == "__main__":
    success = test_hardy_cross_iterations()
    if success:
        print("\n✅ Test des itérations terminé !")
    else:
        print("\n❌ Test des itérations échoué")
        sys.exit(1) 