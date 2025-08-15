"""
Tests unitaires pour l'architecture Strategy Pattern des solveurs hydrauliques.
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.solvers import HydraulicSolver, LcpiHardyCrossSolver, SolverFactory


class TestHydraulicSolver:
    """Tests pour l'interface abstraite HydraulicSolver."""
    
    def test_abstract_class_cannot_be_instantiated(self):
        """Test que la classe abstraite ne peut pas être instanciée."""
        with pytest.raises(TypeError):
            HydraulicSolver()
    
    def test_abstract_methods_exist(self):
        """Test que les méthodes abstraites sont définies."""
        assert hasattr(HydraulicSolver, 'run_simulation')
        assert hasattr(HydraulicSolver, 'get_solver_info')
        assert hasattr(HydraulicSolver, 'validate_network')
    
    def test_concrete_methods_exist(self):
        """Test que les méthodes concrètes sont définies."""
        assert hasattr(HydraulicSolver, 'get_supported_formulas')
        assert hasattr(HydraulicSolver, 'get_solver_parameters')


class TestLcpiHardyCrossSolver:
    """Tests pour le solveur LCPI Hardy-Cross."""
    
    def test_solver_initialization(self):
        """Test l'initialisation du solveur."""
        solver = LcpiHardyCrossSolver()
        assert solver.tolerance == 1e-6
        assert solver.max_iterations == 200
        
        # Test avec paramètres personnalisés
        solver = LcpiHardyCrossSolver(tolerance=1e-8, max_iterations=500)
        assert solver.tolerance == 1e-8
        assert solver.max_iterations == 500
    
    def test_get_solver_info(self):
        """Test la récupération des informations du solveur."""
        solver = LcpiHardyCrossSolver()
        info = solver.get_solver_info()
        
        assert info["name"] == "LCPI Hardy-Cross"
        assert info["version"] == "2.0"
        assert "Hardy-Cross" in info["description"]
        assert "boucles" in info["capabilities"]
    
    def test_validate_network_valid(self):
        """Test la validation d'un réseau valide."""
        solver = LcpiHardyCrossSolver()
        
        network_data = {
            "noeuds": {
                "R1": {"role": "reservoir", "cote_m": 200.0},
                "N1": {"role": "consommation", "cote_m": 150.0}
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "R1",
                    "noeud_aval": "N1",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0
                }
            }
        }
        
        validation = solver.validate_network(network_data)
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0
    
    def test_validate_network_invalid_no_reservoir(self):
        """Test la validation d'un réseau sans réservoir."""
        solver = LcpiHardyCrossSolver()
        
        network_data = {
            "noeuds": {
                "N1": {"role": "consommation", "cote_m": 150.0},
                "N2": {"role": "consommation", "cote_m": 140.0}
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 300.0,
                    "diametre_m": 0.15,
                    "rugosite": 120.0
                }
            }
        }
        
        validation = solver.validate_network(network_data)
        assert validation["valid"] is False
        assert len(validation["errors"]) > 0
        assert any("reservoir" in error.lower() for error in validation["errors"])
    
    def test_validate_network_invalid_conduit(self):
        """Test la validation d'un réseau avec conduite invalide."""
        solver = LcpiHardyCrossSolver()
        
        network_data = {
            "noeuds": {
                "R1": {"role": "reservoir", "cote_m": 200.0},
                "N1": {"role": "consommation", "cote_m": 150.0}
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "R1",
                    "noeud_aval": "N1",
                    "longueur_m": -500.0,  # Longueur négative
                    "diametre_m": 0.2,
                    "rugosite": 100.0
                }
            }
        }
        
        validation = solver.validate_network(network_data)
        assert validation["valid"] is False
        assert len(validation["errors"]) > 0
        assert any("longueur" in error.lower() for error in validation["errors"])
    
    def test_run_simulation_success(self):
        """Test l'exécution d'une simulation réussie."""
        solver = LcpiHardyCrossSolver()
        
        network_data = {
            "noeuds": {
                "R1": {"role": "reservoir", "cote_m": 200.0},
                "N1": {"role": "consommation", "cote_m": 150.0}
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "R1",
                    "noeud_aval": "N1",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0
                }
            }
        }
        
        results = solver.run_simulation(network_data)
        
        assert results["status"] == "success"
        assert results["solver"] == "lcpi_hardy_cross"
        assert "pressures" in results
        assert "flows" in results
        assert "velocities" in results
        assert "convergence" in results
        assert "diagnostics" in results
        assert "execution_time" in results
    
    def test_run_simulation_failure(self):
        """Test l'exécution d'une simulation avec réseau invalide."""
        solver = LcpiHardyCrossSolver()
        
        network_data = {
            "noeuds": {
                "N1": {"role": "consommation", "cote_m": 150.0}  # Pas de réservoir
            },
            "conduites": {}
        }
        
        results = solver.run_simulation(network_data)
        
        assert results["status"] == "failure"
        assert results["solver"] == "lcpi_hardy_cross"
        assert len(results["errors"]) > 0


class TestSolverFactory:
    """Tests pour la factory des solveurs."""
    
    def test_get_solver_lcpi(self):
        """Test la récupération du solveur LCPI."""
        solver = SolverFactory.get_solver("lcpi")
        assert isinstance(solver, LcpiHardyCrossSolver)
    
    def test_get_solver_hardy_cross_alias(self):
        """Test la récupération du solveur via l'alias hardy_cross."""
        solver = SolverFactory.get_solver("hardy_cross")
        assert isinstance(solver, LcpiHardyCrossSolver)
    
    def test_get_solver_unknown(self):
        """Test la gestion d'un solveur inconnu."""
        with pytest.raises(ValueError) as exc_info:
            SolverFactory.get_solver("unknown_solver")
        
        assert "unknown_solver" in str(exc_info.value)
        assert "Disponibles" in str(exc_info.value)
    
    def test_list_available_solvers(self):
        """Test la liste des solveurs disponibles."""
        solvers = SolverFactory.list_available_solvers()
        
        assert "lcpi" in solvers
        assert "hardy_cross" in solvers
        
        # Vérifier la structure des informations
        lcpi_info = solvers["lcpi"]
        assert "name" in lcpi_info
        assert "version" in lcpi_info
        assert "description" in lcpi_info
        assert "capabilities" in lcpi_info
    
    def test_get_solver_capabilities(self):
        """Test la récupération des capacités d'un solveur."""
        capabilities = SolverFactory.get_solver_capabilities("lcpi")
        
        assert "info" in capabilities
        assert "supported_formulas" in capabilities
        assert "default_parameters" in capabilities
        
        # Vérifier les formules supportées
        formulas = capabilities["supported_formulas"]
        assert "hazen_williams" in formulas
        assert "darcy_weisbach" in formulas
    
    def test_validate_solver_choice_valid(self):
        """Test la validation du choix de solveur avec réseau valide."""
        network_data = {
            "noeuds": {
                "R1": {"role": "reservoir", "cote_m": 200.0},
                "N1": {"role": "consommation", "cote_m": 150.0}
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "R1",
                    "noeud_aval": "N1",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0
                }
            }
        }
        
        validation = SolverFactory.validate_solver_choice("lcpi", network_data)
        
        assert validation["solver_name"] == "lcpi"
        assert validation["compatible"] is True
        assert "validation" in validation
        assert "capabilities" in validation
    
    def test_validate_solver_choice_invalid(self):
        """Test la validation du choix de solveur avec réseau invalide."""
        network_data = {
            "noeuds": {
                "N1": {"role": "consommation", "cote_m": 150.0}  # Pas de réservoir
            },
            "conduites": {}
        }
        
        validation = SolverFactory.validate_solver_choice("lcpi", network_data)
        
        assert validation["solver_name"] == "lcpi"
        assert validation["compatible"] is False
        assert "validation" in validation
        assert "capabilities" in validation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
