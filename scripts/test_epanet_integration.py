#!/usr/bin/env python3
"""Test d'intégration EPANET avec Hardy-Cross"""

import sys
import os
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.calculations.hardy_cross_enhanced import hardy_cross_network_enhanced
from lcpi.aep.epanet_wrapper import validate_hardy_cross_with_epanet
import sys
sys.path.append('scripts')
from generate_paris_network import ParisNetworkGenerator

def test_epanet_integration():
    """Test d'intégration EPANET"""
    
    print("🌊 Test d'intégration EPANET avec Hardy-Cross")
    
    # Générer réseau
    generator = ParisNetworkGenerator()
    network_data = generator.generate_network_data()
    
    print(f"✅ Réseau : {len(network_data['network']['nodes'])} nœuds")
    
    # Convertir la structure pour Hardy-Cross
    hardy_cross_data = {
        "metadata": network_data["metadata"],
        "troncons": list(network_data["network"]["pipes"].values()),
        "noeuds": list(network_data["network"]["nodes"].values())
    }
    
    # Hardy-Cross
    hardy_cross_results = hardy_cross_network_enhanced(
        hardy_cross_data, max_iterations=50, tolerance=1e-6
    )
    
    print(f"✅ Hardy-Cross : {len(hardy_cross_results.get('iterations', []))} itérations")
    
    # Validation EPANET
    validation_results = validate_hardy_cross_with_epanet(
        network_data, hardy_cross_results
    )
    
    if "error" in validation_results:
        print(f"❌ Erreur : {validation_results['error']}")
        return False
    
    validation = validation_results.get("validation", {})
    status = validation.get("status", "unknown")
    
    print(f"✅ Validation EPANET : {status}")
    print(f"   - Pressions similaires : {len(validation.get('pressure_similarities', []))}")
    print(f"   - Débits similaires : {len(validation.get('flow_similarities', []))}")
    
    return status in ["validated", "differences_found"]

if __name__ == "__main__":
    success = test_epanet_integration()
    if success:
        print("\n✅ Test d'intégration EPANET réussi !")
    else:
        print("\n❌ Test d'intégration EPANET échoué.")
        sys.exit(1) 