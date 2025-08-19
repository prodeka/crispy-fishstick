"""
Test d'intégration complet pour le Sprint 3 : Format V11, CLI, Rapports

Ce test vérifie que toutes les fonctionnalités fonctionnent ensemble :
1. Format de sortie JSON V11
2. Commandes CLI d'optimisation
3. Génération de rapports V11
4. Intégration avec les algorithmes d'optimisation
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch
import shutil

from lcpi.aep.optimizer.output import OutputFormatter, formatter
from lcpi.aep.optimizer.models import OptimizationConfig, OptimizationObjectives, Proposal, TankDecision, OptimizationResult
from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI


class TestSprint3CompleteIntegration:
    """Test d'intégration complet pour le Sprint 3."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        self.formatter = OutputFormatter()
        self.cli = AEPOptimizationCLI()
        
        # Créer des données de test complètes
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
            pareto_front=None,  # Pas de front Pareto pour ce test
            metadata={
                "method": "nested",
                "network_file": "test_network.inp",
                "algorithm": "NestedGreedy",
                "iterations": 25
            }
        )
        
        # Créer un répertoire temporaire
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
    
    def test_complete_v11_workflow(self):
        """Test le workflow complet V11 : création → formatage → sauvegarde → chargement."""
        # 1. Créer le résultat
        assert len(self.result.proposals) == 1
        assert self.result.proposals[0].name == "test_solution"
        
        # 2. Formater en V11
        v11_output = self.formatter.format_v11(self.result)
        assert v11_output["metadata"]["version"] == "V11"
        assert v11_output["metadata"]["format"] == "lcpi_aep_optimization"
        assert len(v11_output["proposals"]) == 1
        
        # 3. Sauvegarder
        output_path = self.temp_dir / "test_output.json"
        self.formatter.save_v11_json(self.result, output_path)
        assert output_path.exists()
        
        # 4. Charger
        loaded_data = self.formatter.load_v11_json(output_path)
        assert loaded_data["proposals"][0]["name"] == "test_solution"
        assert loaded_data["metadata"]["method"] == "nested"
        
        # 5. Valider
        assert self.formatter.validate_v11_format(loaded_data) is True
        
        print("✅ Workflow V11 complet : OK")
    
    def test_cli_commands_integration(self):
        """Test l'intégration des commandes CLI."""
        # Test de validation de réseau
        assert self.cli._validate_network(self.network_path) is True
        
        # Test de chargement de configuration
        config = self.cli._load_optimization_config(None, 15.0, "nested")
        assert config.method == "nested"
        assert config.objectives.lambda_opex == 15.0
        
        # Test de gestion des diamètres (avec mock)
        with patch('lcpi.aep.optimizer.cli_commands.get_candidate_diameters') as mock_get:
            mock_get.return_value = [{"d_mm": 150, "cost_per_m": 5000}]
            try:
                self.cli._list_diameters()
                assert True
            except Exception:
                pytest.fail("La méthode _list_diameters a levé une exception")
        
        print("✅ Intégration CLI : OK")
    
    def test_report_generation_integration(self):
        """Test la génération de rapports intégrée."""
        # Convertir le résultat en format V11
        v11_output = self.formatter.format_v11(self.result)
        
        # Générer le rapport HTML
        html_content = self.cli._generate_html_report(v11_output, "default")
        
        # Vérifier que le rapport contient les bonnes informations
        assert "Rapport d'Optimisation AEP" in html_content
        assert "test_solution" in html_content
        assert "150,000" in html_content  # CAPEX formaté
        assert "TANK1" in html_content
        assert "65.00 m" in html_content  # Hauteur du tank
        
        print("✅ Génération de rapports : OK")
    
    def test_template_v11_rendering(self):
        """Test le rendu du template V11."""
        from jinja2 import Environment, FileSystemLoader
        
        # Charger le template V11
        template_dir = Path("src/lcpi/aep/templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("optimisation_tank_v11.jinja2")
        
        # Préparer le contexte
        context = {
            "proposals": [self.proposal],
            "pareto_front": self.result.pareto_front,
            "metadata": self.result.metadata,
            "now": Mock(strftime=lambda fmt: "01/01/2024 à 12:00")
        }
        
        # Rendre le template
        html_output = template.render(**context)
        
        # Vérifier le contenu
        assert "Rapport d'Optimisation AEP" in html_output
        assert "Version V11" in html_output
        assert "test_solution" in html_output
        assert "TANK1" in html_output
        assert "65.00 m" in html_output
        assert "150,000" in html_output
        
        print("✅ Rendu du template V11 : OK")
    
    def test_algorithm_compatibility(self):
        """Test la compatibilité avec les algorithmes d'optimisation."""
        # Vérifier que tous les algorithmes peuvent être importés
        try:
            from lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer
            from lcpi.aep.optimizer.algorithms.multi_tank import MultiTankOptimizer
            from lcpi.aep.optimizer.algorithms.nested import NestedGreedyOptimizer
            from lcpi.aep.optimizer.algorithms.surrogate import SurrogateOptimizer
            assert True
        except ImportError as e:
            pytest.fail(f"Import d'algorithme échoué: {e}")
        
        # Vérifier que les algorithmes retournent des OptimizationResult
        # (cette vérification nécessiterait des mocks plus complexes)
        print("✅ Compatibilité des algorithmes : OK")
    
    def test_cli_main_integration(self):
        """Test l'intégration dans le CLI principal."""
        try:
            from lcpi.aep.cli import app
            assert True
        except ImportError as e:
            pytest.fail(f"Import du CLI principal échoué: {e}")
        
        print("✅ Intégration CLI principal : OK")
    
    def test_end_to_end_workflow(self):
        """Test le workflow end-to-end complet."""
        # 1. Créer un résultat d'optimisation
        result = self.result
        
        # 2. Formater en V11
        v11_output = self.formatter.format_v11(result)
        
        # 3. Sauvegarder
        output_path = self.temp_dir / "end_to_end_test.json"
        self.formatter.save_v11_json(result, output_path)
        
        # 4. Charger et valider
        loaded_data = self.formatter.load_v11_json(output_path)
        assert self.formatter.validate_v11_format(loaded_data)
        
        # 5. Générer le rapport
        html_content = self.cli._generate_html_report(loaded_data, "default")
        assert "test_solution" in html_content
        
        print("✅ Workflow end-to-end : OK")
    
    def test_error_handling(self):
        """Test la gestion des erreurs."""
        # Test avec des données invalides
        invalid_data = {"proposals": "not_a_list"}
        assert self.formatter.validate_v11_format(invalid_data) is False
        
        # Test avec des données manquantes
        invalid_data2 = {"proposals": []}
        assert self.formatter.validate_v11_format(invalid_data2) is False
        
        print("✅ Gestion des erreurs : OK")


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
