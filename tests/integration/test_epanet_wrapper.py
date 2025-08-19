"""
Test d'intégration pour le wrapper EPANET.
"""

import pytest
import warnings
from pathlib import Path

# Supprimer les warnings spécifiques pour ces tests
warnings.filterwarnings("ignore", category=UserWarning, 
                       message="pkg_resources is deprecated as an API")
warnings.filterwarnings("ignore", category=DeprecationWarning,
                       message="Use of .. or absolute path in a resource path")
warnings.filterwarnings("ignore", category=UserWarning,
                       module="wntr.epanet.toolkit")
warnings.filterwarnings("ignore", category=DeprecationWarning,
                       module="wntr.epanet.msx.toolkit")

# Vérifier qu'un fichier .inp d'exemple existe
def test_epanet_wrapper():
    """Test basique du wrapper EPANET."""
    # Chercher un fichier .inp d'exemple
    examples_dir = Path("examples")
    candidate = None
    
    if examples_dir.exists():
        for inp_file in examples_dir.glob("*.inp"):
            candidate = inp_file
            break
    
    if not candidate:
        pytest.skip("Pas de .inp d'exemple trouvé")

    from lcpi.aep.optimizer.solvers import EPANETOptimizer
    op = EPANETOptimizer()
    res = op.simulate(candidate, H_tank_map={}, diameters_map={}, duration_h=1, timestep_min=5, timeout_s=30)
    
    # Vérifier que la simulation a réussi
    assert res is not None
    print(f"✅ Simulation EPANET réussie: {res}")


