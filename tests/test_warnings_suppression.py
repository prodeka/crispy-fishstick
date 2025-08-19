"""
Test de vérification de la suppression des warnings EPANET.

Ce test vérifie que tous les warnings liés aux wrappers EPANET sont bien supprimés.
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


class TestWarningsSuppression:
    """Test que la suppression des warnings EPANET fonctionne."""
    
    def test_no_epanet_warnings_on_import(self):
        """Test qu'il n'y a pas de warnings lors de l'import des wrappers EPANET."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Importer les wrappers EPANET
            from lcpi.aep.core.epanet_wrapper import (
                EpanetSimulator, EPANETOptimizer, EpanetWrapper
            )
            
            # Vérifier qu'il n'y a pas de warnings EPANET
            epanet_warnings = [
                warning for warning in w 
                if any(keyword in str(warning.message).lower() 
                      for keyword in ['pkg_resources', 'resource path', 'wntr'])
            ]
            
            assert len(epanet_warnings) == 0, f"Warnings EPANET détectés: {epanet_warnings}"
            print("✅ Aucun warning EPANET lors de l'import")
    
    def test_no_epanet_warnings_on_creation(self):
        """Test qu'il n'y a pas de warnings lors de la création des instances."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            try:
                from lcpi.aep.core.epanet_wrapper import EPANETOptimizer
                optimizer = EPANETOptimizer()
                
                # Vérifier qu'il n'y a pas de warnings EPANET
                epanet_warnings = [
                    warning for warning in w 
                    if any(keyword in str(warning.message).lower() 
                          for keyword in ['pkg_resources', 'resource path', 'wntr'])
                ]
                
                assert len(epanet_warnings) == 0, f"Warnings EPANET détectés: {epanet_warnings}"
                print("✅ Aucun warning EPANET lors de la création d'EPANETOptimizer")
                
            except ImportError as e:
                pytest.skip(f"EPANETOptimizer non disponible: {e}")
    
    def test_no_epanet_warnings_on_simulation(self):
        """Test qu'il n'y a pas de warnings lors de la simulation."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            try:
                from lcpi.aep.core.epanet_wrapper import EPANETOptimizer
                optimizer = EPANETOptimizer()
                
                # Créer un fichier .inp simple pour le test
                test_inp = Path("test_warnings.inp")
                test_inp.write_text("""
[TITLE]
Test Network
[JUNCTIONS]
N1	50	0.001
[RESERVOIRS]
TANK1	100
[PIPES]
PIPE1	TANK1	N1	50	200	100	0	Open
[OPTIONS]
UNITS	LPS
HEADLOSS	H-W
[TIMES]
DURATION	1
[REPORT]
STATUS	NO
[END]
                """.strip())
                
                try:
                    # Lancer une simulation courte
                    results = optimizer.simulate(
                        test_inp,
                        H_tank_map={},
                        diameters_map={},
                        duration_h=1,
                        timestep_min=5,
                        timeout_s=10
                    )
                    
                    # Vérifier qu'il n'y a pas de warnings EPANET
                    epanet_warnings = [
                        warning for warning in w 
                        if any(keyword in str(warning.message).lower() 
                              for keyword in ['pkg_resources', 'resource path', 'wntr'])
                    ]
                    
                    assert len(epanet_warnings) == 0, f"Warnings EPANET détectés: {epanet_warnings}"
                    print("✅ Aucun warning EPANET lors de la simulation")
                    
                finally:
                    # Nettoyer
                    if test_inp.exists():
                        test_inp.unlink()
                        
            except ImportError as e:
                pytest.skip(f"EPANETOptimizer non disponible: {e}")
    
    def test_warnings_suppression_configuration(self):
        """Test que la configuration de suppression des warnings est correcte."""
        # Vérifier que les warnings sont bien configurés
        from lcpi.aep.core.epanet_wrapper import _suppress_warnings
        
        # La fonction doit exister et être callable
        assert callable(_suppress_warnings)
        print("✅ Fonction de suppression des warnings disponible")
        
        # Vérifier que les warnings sont bien supprimés
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Appeler la fonction de suppression
            _suppress_warnings()
            
            # Vérifier qu'il n'y a pas de warnings EPANET
            epanet_warnings = [
                warning for warning in w 
                if any(keyword in str(warning.message).lower() 
                      for keyword in ['pkg_resources', 'resource path', 'wntr'])
            ]
            
            assert len(epanet_warnings) == 0, f"Warnings EPANET détectés: {epanet_warnings}"
            print("✅ Configuration de suppression des warnings fonctionne")


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
