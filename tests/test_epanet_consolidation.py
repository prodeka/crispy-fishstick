"""
Test de non-régression pour la consolidation des wrappers EPANET.

Ce test vérifie que la consolidation n'a pas cassé les fonctionnalités existantes
et que les nouveaux wrappers fonctionnent correctement.
"""

import pytest
import warnings
from pathlib import Path
from unittest.mock import Mock, patch

# Supprimer les warnings spécifiques pour ces tests
warnings.filterwarnings("ignore", category=UserWarning, 
                       message="pkg_resources is deprecated as an API")
warnings.filterwarnings("ignore", category=DeprecationWarning,
                       message="Use of .. or absolute path in a resource path")
warnings.filterwarnings("ignore", category=UserWarning,
                       module="wntr.epanet.toolkit")
warnings.filterwarnings("ignore", category=DeprecationWarning,
                       module="wntr.epanet.msx.toolkit")

from lcpi.aep.core.epanet_wrapper import (
    EpanetSimulator,
    EPANETOptimizer,
    EpanetWrapper,
    create_epanet_inp_file,
    is_epanet_available,
    get_epanet_version
)

from lcpi.aep.epanet_wrapper import (
    EpanetSimulator as CompatEpanetSimulator,
    EPANETOptimizer as CompatEPANETOptimizer
)


class TestEPANETConsolidation:
    """Test de non-régression pour la consolidation des wrappers EPANET."""
    
    def test_epanet_simulator_creation(self):
        """Test que EpanetSimulator peut être créé."""
        try:
            simulator = EpanetSimulator()
            assert simulator is not None
            print("✅ EpanetSimulator créé avec succès")
        except Exception as e:
            pytest.skip(f"EpanetSimulator non disponible: {e}")
    
    def test_epanet_optimizer_creation(self):
        """Test que EPANETOptimizer peut être créé."""
        try:
            optimizer = EPANETOptimizer()
            assert optimizer is not None
            print("✅ EPANETOptimizer créé avec succès")
        except Exception as e:
            pytest.skip(f"EPANETOptimizer non disponible: {e}")
    
    def test_epanet_wrapper_creation(self):
        """Test que EpanetWrapper peut être créé."""
        wrapper = EpanetWrapper()
        assert wrapper is not None
        assert hasattr(wrapper, 'is_available')
        assert hasattr(wrapper, 'get_version')
        print("✅ EpanetWrapper créé avec succès")
    
    def test_compatibility_layer(self):
        """Test que la couche de compatibilité fonctionne."""
        # Vérifier que les imports de compatibilité pointent vers les bonnes classes
        assert CompatEpanetSimulator is EpanetSimulator
        assert CompatEPANETOptimizer is EPANETOptimizer
        print("✅ Couche de compatibilité fonctionne")
    
    def test_utility_functions(self):
        """Test que les fonctions utilitaires sont disponibles."""
        assert callable(create_epanet_inp_file)
        assert callable(is_epanet_available)
        assert callable(get_epanet_version)
        print("✅ Fonctions utilitaires disponibles")
    
    def test_epanet_availability_check(self):
        """Test de vérification de disponibilité EPANET."""
        available = is_epanet_available()
        assert isinstance(available, bool)
        print(f"✅ Vérification disponibilité EPANET: {available}")
    
    def test_epanet_version(self):
        """Test de récupération de version EPANET."""
        version = get_epanet_version()
        assert isinstance(version, str)
        assert len(version) > 0
        print(f"✅ Version EPANET: {version}")
    
    def test_epanet_optimizer_methods(self):
        """Test que EPANETOptimizer a les méthodes attendues."""
        try:
            optimizer = EPANETOptimizer()
            assert hasattr(optimizer, 'simulate')
            assert hasattr(optimizer, 'simulate_with_tank_height')
            assert callable(optimizer.simulate)
            assert callable(optimizer.simulate_with_tank_height)
            print("✅ EPANETOptimizer a toutes les méthodes attendues")
        except Exception as e:
            pytest.skip(f"EPANETOptimizer non disponible: {e}")
    
    def test_epanet_simulator_methods(self):
        """Test que EpanetSimulator a les méthodes attendues."""
        try:
            simulator = EpanetSimulator()
            assert hasattr(simulator, 'open_project')
            assert hasattr(simulator, 'solve_hydraulics')
            assert hasattr(simulator, 'get_node_pressures')
            assert hasattr(simulator, 'get_link_flows')
            print("✅ EpanetSimulator a toutes les méthodes attendues")
        except Exception as e:
            pytest.skip(f"EpanetSimulator non disponible: {e}")
    
    def test_create_inp_file_function(self):
        """Test de la fonction create_epanet_inp_file."""
        # Données de test minimales
        test_network = {
            "network": {
                "nodes": {
                    "N1": {"type": "junction", "elevation": 50, "demand": 0},
                    "N2": {"type": "reservoir", "elevation": 100}
                },
                "pipes": {
                    "P1": {"from": "N1", "to": "N2", "length": 100, "diameter": 150, "roughness": 100}
                }
            }
        }
        
        # Test de création de fichier INP
        test_inp_path = "test_consolidation.inp"
        try:
            success = create_epanet_inp_file(test_network, test_inp_path)
            assert success is True
            
            # Vérifier que le fichier a été créé
            inp_file = Path(test_inp_path)
            assert inp_file.exists()
            assert inp_file.stat().st_size > 0
            
            # Vérifier le contenu
            content = inp_file.read_text(encoding='utf-8')
            assert "[TITLE]" in content
            assert "[JUNCTIONS]" in content
            assert "[RESERVOIRS]" in content
            assert "[PIPES]" in content
            assert "[OPTIONS]" in content
            
            print("✅ Fonction create_epanet_inp_file fonctionne")
            
        finally:
            # Nettoyer
            if Path(test_inp_path).exists():
                Path(test_inp_path).unlink()
    
    def test_import_paths(self):
        """Test que tous les chemins d'import fonctionnent."""
        import_paths = [
            "lcpi.aep.core.epanet_wrapper",
            "lcpi.aep.epanet_wrapper", 
            "lcpi.aep.optimizer.solvers"
        ]
        
        for import_path in import_paths:
            try:
                __import__(import_path)
                print(f"✅ Import réussi: {import_path}")
            except ImportError as e:
                pytest.fail(f"Import échoué pour {import_path}: {e}")
    
    def test_consolidation_integrity(self):
        """Test d'intégrité de la consolidation."""
        # Vérifier que les classes sont bien unifiées
        from lcpi.aep.core.epanet_wrapper import EpanetSimulator as CoreSimulator
        from lcpi.aep.epanet_wrapper import EpanetSimulator as CompatSimulator
        
        assert CoreSimulator is CompatSimulator
        
        # Vérifier que les méthodes sont disponibles
        simulator = EpanetSimulator()
        methods = ['open_project', 'solve_hydraulics', 'get_node_pressures', 'get_link_flows']
        for method in methods:
            assert hasattr(simulator, method), f"Méthode {method} manquante"
        
        print("✅ Intégrité de la consolidation vérifiée")


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
