"""
Tests pour les fonctionnalités du Sprint 3 : Format V11, CLI, Rapports

Ce fichier teste :
1. Format de sortie JSON V11
2. Commandes CLI d'optimisation
3. Génération de rapports V11
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import shutil

from lcpi.aep.optimizer.output import OutputFormatter, formatter
from lcpi.aep.optimizer.models import OptimizationConfig, OptimizationObjectives, Proposal, TankDecision, OptimizationResult
from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI


class TestOutputFormatterV11:
    """Tests pour le formateur de sortie V11."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        self.formatter = OutputFormatter()
        
        # Créer des données de test
        self.tank_decision = TankDecision(id="TANK1", H_m=65.0)
        self.proposal = Proposal(
            name="test_solution",
            is_feasible=True,
            tanks=[self.tank_decision],
            diameters_mm={"PIPE1": 200, "PIPE2": 150},
            costs={"CAPEX": 150000.0, "OPEX_annual": 5000.0, "OPEX_npv": 45000.0},
            metrics={"min_pressure_m": 12.5, "max_velocity_m_s": 1.8}
        )
        
        self.result = OptimizationResult(
            proposals=[self.proposal],
            pareto_front=None,
            metadata={"method": "nested", "network_file": "test_network.inp"}
        )
    
    def test_format_v11_basic(self):
        """Test le formatage V11 de base."""
        v11_output = self.formatter.format_v11(self.result)
        
        # Vérifier la structure
        assert "proposals" in v11_output
        assert "metadata" in v11_output
        assert "pareto_front" in v11_output
        
        # Vérifier les métadonnées
        metadata = v11_output["metadata"]
        assert metadata["version"] == "V11"
        assert metadata["format"] == "lcpi_aep_optimization"
        assert metadata["method"] == "nested"
        
        # Vérifier les propositions
        proposals = v11_output["proposals"]
        assert len(proposals) == 1
        
        proposal = proposals[0]
        assert proposal["name"] == "test_solution"
        assert proposal["is_feasible"] is True
        assert proposal["tanks"][0]["id"] == "TANK1"
        assert proposal["tanks"][0]["H_m"] == 65.0
    
    def test_format_v11_with_execution_metadata(self):
        """Test le formatage V11 avec métadonnées d'exécution."""
        execution_metadata = {
            "execution_time": "00:05:23",
            "iterations": 150,
            "algorithm": "nested_greedy"
        }
        
        v11_output = self.formatter.format_v11(self.result, execution_metadata)
        
        # Vérifier que les métadonnées d'exécution sont fusionnées
        metadata = v11_output["metadata"]
        assert metadata["execution_time"] == "00:05:23"
        assert metadata["iterations"] == 150
        assert metadata["algorithm"] == "nested_greedy"
    
    def test_format_proposal_costs_dict(self):
        """Test le formatage des coûts quand ils sont dans un dict."""
        # Créer un objet Proposal au lieu d'un dict
        proposal = Proposal(
            name="test",
            is_feasible=True,
            tanks=[],
            diameters_mm={},
            costs={"CAPEX": 100000, "OPEX_npv": 30000},
            metrics={"min_pressure_m": 10.0, "max_velocity_m_s": 2.0}
        )
        
        formatted = self.formatter._format_proposal(proposal)
        
        assert formatted["costs"]["CAPEX"] == 100000
        assert formatted["costs"]["OPEX_npv"] == 30000
    
    def test_save_and_load_v11_json(self):
        """Test la sauvegarde et le chargement de fichiers V11."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.json"
            
            # Sauvegarder
            self.formatter.save_v11_json(self.result, output_path)
            assert output_path.exists()
            
            # Charger
            loaded_data = self.formatter.load_v11_json(output_path)
            
            # Vérifier que les données sont identiques
            assert loaded_data["proposals"][0]["name"] == "test_solution"
            assert loaded_data["metadata"]["method"] == "nested"
    
    def test_validate_v11_format(self):
        """Test la validation du format V11."""
        # Données valides
        valid_data = {
            "proposals": [{
                "name": "test",
                "is_feasible": True,
                "tanks": [],
                "diameters_mm": {},
                "costs": {},
                "metrics": {}
            }],
            "metadata": {}
        }
        
        assert self.formatter.validate_v11_format(valid_data) is True
        
        # Données invalides
        invalid_data = {"proposals": []}  # Manque metadata
        assert self.formatter.validate_v11_format(invalid_data) is False
        
        invalid_data2 = {"metadata": {}, "proposals": "not_a_list"}
        assert self.formatter.validate_v11_format(invalid_data2) is False


class TestAEPOptimizationCLI:
    """Tests pour l'interface CLI d'optimisation."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        self.cli = AEPOptimizationCLI()
        
        # Créer un fichier réseau temporaire
        self.temp_dir = Path(tempfile.mkdtemp())
        self.network_path = self.temp_dir / "test_network.inp"
        self.network_path.write_text("""
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
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_validate_network_valid(self):
        """Test la validation d'un réseau valide."""
        assert self.cli._validate_network(self.network_path) is True
    
    def test_validate_network_invalid_extension(self):
        """Test la validation d'un réseau avec extension invalide."""
        invalid_path = self.temp_dir / "test.txt"
        invalid_path.write_text("test content")
        assert self.cli._validate_network(invalid_path) is False
    
    def test_validate_network_missing_sections(self):
        """Test la validation d'un réseau avec sections manquantes."""
        invalid_network = self.temp_dir / "invalid.inp"
        invalid_network.write_text("[TITLE]\nTest\n[END]")
        assert self.cli._validate_network(invalid_network) is False
    
    def test_load_optimization_config_default(self):
        """Test le chargement de configuration par défaut."""
        config = self.cli._load_optimization_config(None, 15.0, "nested")
        
        assert config.method == "nested"
        assert config.objectives.lambda_opex == 15.0
        assert config.h_bounds_m["TANK1"] == (50.0, 100.0)
        assert config.pressure_min_m == 10.0
    
    def test_load_optimization_config_from_file(self):
        """Test le chargement de configuration depuis un fichier."""
        config_file = self.temp_dir / "config.yml"
        config_file.write_text("""
method: global
objectives:
  capex: true
  opex: true
  lambda_opex: 20.0
h_bounds_m:
  TANK1: [60.0, 120.0]
pressure_min_m: 15.0
        """.strip())
        
        config = self.cli._load_optimization_config(config_file, 10.0, "nested")
        
        assert config.method == "global"
        assert config.objectives.lambda_opex == 20.0
        assert config.h_bounds_m["TANK1"] == (60.0, 120.0)  # Utiliser la valeur du fichier
        assert config.pressure_min_m == 15.0
    
    def test_list_diameters(self):
        """Test la liste des diamètres disponibles."""
        # Mock de get_candidate_diameters
        with patch('lcpi.aep.optimizer.cli_commands.get_candidate_diameters') as mock_get:
            mock_get.return_value = [
                {"d_mm": 150, "cost_per_m": 5000},
                {"d_mm": 200, "cost_per_m": 8000}
            ]
            
            # Cette méthode ne devrait pas lever d'exception
            try:
                self.cli._list_diameters()
                assert True
            except Exception:
                pytest.fail("La méthode _list_diameters a levé une exception")
    
    def test_diameters_manage_list(self):
        """Test la commande de gestion des diamètres - list."""
        with patch('lcpi.aep.optimizer.cli_commands.get_candidate_diameters') as mock_get:
            mock_get.return_value = [{"d_mm": 150, "cost_per_m": 5000}]
            
            try:
                self.cli.diameters_manage("list")
                assert True
            except Exception:
                pytest.fail("La commande diameters_manage list a levé une exception")
    
    def test_diameters_manage_invalid_action(self):
        """Test la commande de gestion des diamètres avec action invalide."""
        with pytest.raises(Exception):
            self.cli.diameters_manage("invalid_action")


class TestSprint3Integration:
    """Tests d'intégration pour le Sprint 3."""
    
    def test_output_formatter_import(self):
        """Test que le module OutputFormatter peut être importé."""
        try:
            from lcpi.aep.optimizer.output import OutputFormatter, formatter
            assert True
        except ImportError as e:
            pytest.fail(f"Import échoué: {e}")
    
    def test_cli_commands_import(self):
        """Test que le module CLI peut être importé."""
        try:
            from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
            assert True
        except ImportError as e:
            pytest.fail(f"Import échoué: {e}")
    
    def test_template_v11_exists(self):
        """Test que le template V11 existe."""
        template_path = Path("src/lcpi/reporting/templates/optimisation_tank_v11.jinja2")
        assert template_path.exists(), f"Le template V11 n'existe pas: {template_path}"
    
    def test_v11_format_structure(self):
        """Test que la structure V11 est cohérente."""
        # Créer un résultat de test
        tank = TankDecision(id="TANK1", H_m=65.0)
        proposal = Proposal(
            name="test",
            is_feasible=True,
            tanks=[tank],
            diameters_mm={"PIPE1": 200},
            costs={"CAPEX": 100000, "OPEX_annual": 5000, "OPEX_npv": 45000},
            metrics={"min_pressure_m": 12.5, "max_velocity_m_s": 1.8}
        )
        
        result = OptimizationResult(
            proposals=[proposal],
            pareto_front=None,
            metadata={"method": "test", "network_file": "test.inp"}
        )
        
        # Formater en V11
        formatter = OutputFormatter()
        v11_output = formatter.format_v11(result)
        
        # Vérifier la structure
        assert "proposals" in v11_output
        assert "metadata" in v11_output
        assert "pareto_front" in v11_output
        
        # Vérifier les propositions
        assert len(v11_output["proposals"]) == 1
        proposal_v11 = v11_output["proposals"][0]
        
        assert proposal_v11["name"] == "test"
        assert proposal_v11["is_feasible"] is True
        assert proposal_v11["tanks"][0]["id"] == "TANK1"
        assert proposal_v11["tanks"][0]["H_m"] == 65.0
        assert proposal_v11["diameters_mm"]["PIPE1"] == 200
        assert proposal_v11["costs"]["CAPEX"] == 100000
        assert proposal_v11["metrics"]["min_pressure_m"] == 12.5


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
