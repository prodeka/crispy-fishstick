#!/usr/bin/env python3
"""
Tests simplifiés pour l'architecture Strategy Pattern des solveurs hydrauliques.

Ce module teste l'implémentation du Strategy Pattern pour les solveurs
hydrauliques sans dépendre d'EPANET.
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.solvers import (
    HydraulicSolver,
    LcpiHardyCrossSolver,
    SolverFactory
)


class TestStrategyPatternSimple:
    """Tests simplifiés pour l'architecture Strategy Pattern."""
    
    def test_hydraulic_solver_interface(self):
        """Test que l'interface HydraulicSolver est bien définie."""
        # Vérifier que c'est une classe abstraite
        assert hasattr(HydraulicSolver, '__abstractmethods__')
        
        # Vérifier les méthodes abstraites requises
        required_methods = ['run_simulation', 'get_solver_info', 'validate_network']
        for method in required_methods:
            assert method in HydraulicSolver.__abstractmethods__
    
    def test_lcpi_solver_implementation(self):
        """Test l'implémentation du solveur LCPI Hardy-Cross."""
        solver = LcpiHardyCrossSolver()
        
        # Vérifier que c'est une instance de HydraulicSolver
        assert isinstance(solver, HydraulicSolver)
        
        # Vérifier les méthodes requises
        assert hasattr(solver, 'run_simulation')
        assert hasattr(solver, 'get_solver_info')
        assert hasattr(solver, 'validate_network')
        assert hasattr(solver, 'get_supported_formulas')
        assert hasattr(solver, 'get_solver_parameters')
        
        # Vérifier les informations du solveur
        info = solver.get_solver_info()
        assert info['name'] == 'LCPI Hardy-Cross'
        assert 'version' in info
        assert 'description' in info
        assert 'capabilities' in info
    
    def test_solver_factory_basic(self):
        """Test de base de la SolverFactory."""
        # Vérifier les solveurs disponibles
        solvers = SolverFactory.list_available_solvers()
        assert 'lcpi' in solvers
        assert 'hardy_cross' in solvers  # Alias
        
        # Vérifier les informations des solveurs
        for name, info in solvers.items():
            assert 'name' in info
            assert 'version' in info
            assert 'description' in info
            assert 'capabilities' in info
    
    def test_solver_factory_get_solver(self):
        """Test de récupération des solveurs via la factory."""
        # Test du solveur LCPI
        lcpi_solver = SolverFactory.get_solver('lcpi')
        assert isinstance(lcpi_solver, LcpiHardyCrossSolver)
        
        # Test de l'alias hardy_cross
        hardy_solver = SolverFactory.get_solver('hardy_cross')
        assert isinstance(hardy_solver, LcpiHardyCrossSolver)
        
        # Test d'erreur pour un solveur inexistant
        with pytest.raises(ValueError, match="Solveur 'inexistant' inconnu"):
            SolverFactory.get_solver('inexistant')
    
    def test_solver_factory_capabilities(self):
        """Test des capacités des solveurs."""
        # Test des capacités du solveur LCPI
        lcpi_capabilities = SolverFactory.get_solver_capabilities('lcpi')
        assert 'info' in lcpi_capabilities
        assert 'supported_formulas' in lcpi_capabilities
        assert 'default_parameters' in lcpi_capabilities
        
        # Vérifier les formules supportées
        formulas = lcpi_capabilities['supported_formulas']
        assert 'hazen_williams' in formulas
        assert 'darcy_weisbach' in formulas
    
    def test_network_validation(self):
        """Test de validation des réseaux par les solveurs."""
        # Réseau de test valide
        valid_network = {
            "noeuds": {
                "N1": {
                    "role": "reservoir",
                    "cote_m": 100.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 95.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        # Test avec le solveur LCPI
        lcpi_solver = LcpiHardyCrossSolver()
        lcpi_validation = lcpi_solver.validate_network(valid_network)
        assert lcpi_validation['valid'] is True
        assert len(lcpi_validation['errors']) == 0
    
    def test_network_validation_invalid(self):
        """Test de validation avec un réseau invalide."""
        # Réseau invalide (pas de réservoir)
        invalid_network = {
            "noeuds": {
                "N1": {
                    "role": "consommation",  # Pas de réservoir !
                    "cote_m": 100.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {}
        }
        
        # Test avec le solveur LCPI
        lcpi_solver = LcpiHardyCrossSolver()
        lcpi_validation = lcpi_solver.validate_network(invalid_network)
        assert lcpi_validation['valid'] is False
        assert len(lcpi_validation['errors']) > 0
        assert any("reservoir" in error.lower() for error in lcpi_validation['errors'])
    
    def test_solver_factory_validation(self):
        """Test de validation des choix de solveur via la factory."""
        # Réseau de test
        test_network = {
            "noeuds": {
                "N1": {
                    "role": "reservoir",
                    "cote_m": 100.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 95.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        # Test de validation pour LCPI
        lcpi_validation = SolverFactory.validate_solver_choice('lcpi', test_network)
        assert lcpi_validation['solver_name'] == 'lcpi'
        assert lcpi_validation['compatible'] is True
        assert 'validation' in lcpi_validation
        assert 'capabilities' in lcpi_validation
    
    def test_solver_parameters(self):
        """Test des paramètres par défaut des solveurs."""
        # Test des paramètres LCPI
        lcpi_solver = LcpiHardyCrossSolver()
        lcpi_params = lcpi_solver.get_solver_parameters()
        assert 'tolerance' in lcpi_params
        assert 'max_iterations' in lcpi_params
        assert 'formula' in lcpi_params
        assert lcpi_params['tolerance'] == 1e-6
        assert lcpi_params['max_iterations'] == 200
    
    def test_solver_formulas(self):
        """Test des formules supportées par les solveurs."""
        # Test des formules LCPI
        lcpi_solver = LcpiHardyCrossSolver()
        lcpi_formulas = lcpi_solver.get_supported_formulas()
        assert 'hazen_williams' in lcpi_formulas
        assert 'darcy_weisbach' in lcpi_formulas


class TestStrategyPatternIntegrationSimple:
    """Tests d'intégration simplifiés pour l'architecture Strategy Pattern."""
    
    def test_solver_interchangeability(self):
        """Test que les solveurs sont interchangeables."""
        # Réseau de test
        test_network = {
            "noeuds": {
                "N1": {
                    "role": "reservoir",
                    "cote_m": 100.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 95.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        # Test avec LCPI
        lcpi_solver = SolverFactory.get_solver('lcpi')
        lcpi_results = lcpi_solver.run_simulation(test_network)
        
        # Vérifier la structure des résultats
        assert 'status' in lcpi_results
        assert 'solver' in lcpi_results
        assert 'convergence' in lcpi_results
        assert lcpi_results['solver'] == 'lcpi_hardy_cross'
    
    def test_factory_registration(self):
        """Test de l'enregistrement de nouveaux solveurs."""
        # Créer un solveur mock pour le test
        class MockSolver(HydraulicSolver):
            def run_simulation(self, network_data):
                return {
                    "pressions": {"N1": 25.0, "N2": 22.0},
                    "flows": {"C1": 0.02},
                    "velocities": {"C1": 1.0},
                    "status": "success",
                    "solver": "mock"
                }
            
            def get_solver_info(self):
                return {
                    "name": "Mock Solver",
                    "version": "1.0",
                    "description": "Solveur de test",
                    "capabilities": "Test uniquement"
                }
            
            def validate_network(self, network_data):
                return {
                    "valid": True,
                    "errors": [],
                    "warnings": []
                }
        
        # Enregistrer le solveur mock
        SolverFactory.register_solver('mock', MockSolver)
        
        # Vérifier qu'il est disponible
        solvers = SolverFactory.list_available_solvers()
        assert 'mock' in solvers
        
        # Tester son utilisation
        mock_solver = SolverFactory.get_solver('mock')
        assert isinstance(mock_solver, MockSolver)
        
        # Test de simulation
        test_network = {"noeuds": {}, "conduites": {}}
        results = mock_solver.run_simulation(test_network)
        assert results['solver'] == 'mock'
        assert results['status'] == 'success'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
