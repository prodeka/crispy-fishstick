#!/usr/bin/env python3
"""
Tests pour la commande network_complete_unified.

Ce module teste l'implémentation de la commande network_complete_unified
qui utilise l'architecture Strategy Pattern pour les solveurs hydrauliques.
"""

import pytest
import sys
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.calculations.network_complete_unified import (
    network_complete_unified,
    load_yaml_config,
    export_results,
    _perform_post_processing
)
from lcpi.aep.core.pydantic_models import ReseauCompletConfig


class TestNetworkCompleteUnified:
    """Tests pour la commande network_complete_unified."""
    
    def test_load_yaml_config_valid(self):
        """Test du chargement d'un fichier YAML valide."""
        # Créer un fichier YAML temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml_data = {
                "nom": "Réseau Test",
                "type": "maillé",
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
            yaml.dump(yaml_data, f)
            yaml_file = f.name
        
        try:
            # Tester le chargement
            config = load_yaml_config(Path(yaml_file))
            assert config["nom"] == "Réseau Test"
            assert config["type"] == "maillé"
            assert "noeuds" in config
            assert "conduites" in config
        finally:
            Path(yaml_file).unlink()
    
    def test_load_yaml_config_invalid_file(self):
        """Test du chargement d'un fichier YAML inexistant."""
        with pytest.raises(ValueError, match="Fichier non trouvé"):
            load_yaml_config(Path("fichier_inexistant.yml"))
    
    def test_load_yaml_config_invalid_yaml(self):
        """Test du chargement d'un fichier YAML invalide."""
        # Créer un fichier YAML invalide
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            yaml_file = f.name
        
        try:
            with pytest.raises(ValueError, match="Erreur de parsing YAML"):
                load_yaml_config(Path(yaml_file))
        finally:
            Path(yaml_file).unlink()
    
    def test_export_results_json(self):
        """Test de l'export au format JSON."""
        test_data = {
            "valeurs": {"test": "value"},
            "diagnostics": {"status": True}
        }
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_results(test_data, "json", output_path)
            assert output_path.exists()
            
            # Vérifier le contenu
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '"test": "value"' in content
                assert '"status": true' in content
        finally:
            output_path.unlink()
    
    def test_export_results_yaml(self):
        """Test de l'export au format YAML."""
        test_data = {
            "valeurs": {"test": "value"},
            "diagnostics": {"status": True}
        }
        
        with tempfile.NamedTemporaryFile(suffix='.yml', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_results(test_data, "yaml", output_path)
            assert output_path.exists()
            
            # Vérifier le contenu
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "test: value" in content
                assert "status: true" in content
        finally:
            output_path.unlink()
    
    def test_export_results_csv(self):
        """Test de l'export au format CSV."""
        test_data = {
            "valeurs": {"param1": "value1", "param2": "value2"},
            "diagnostics": {"status": True}
        }
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_results(test_data, "csv", output_path)
            assert output_path.exists()
            
            # Vérifier le contenu
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Section,Paramètre,Valeur" in content
                assert "Valeurs,param1,value1" in content
                assert "Diagnostics,status,True" in content
        finally:
            output_path.unlink()
    
    def test_export_results_html(self):
        """Test de l'export au format HTML."""
        test_data = {
            "valeurs": {"param1": "value1"},
            "diagnostics": {"status": True}
        }
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_results(test_data, "html", output_path)
            assert output_path.exists()
            
            # Vérifier le contenu
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "<!DOCTYPE html>" in content
                assert "Résultats de l'Analyse Réseau" in content
                assert "param1: value1" in content
        finally:
            output_path.unlink()
    
    def test_export_results_invalid_format(self):
        """Test de l'export avec un format invalide."""
        test_data = {"test": "data"}
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            with pytest.raises(ValueError, match="Format d'export 'invalid' non supporté"):
                export_results(test_data, "invalid", output_path)
        finally:
            output_path.unlink()
    
    def test_perform_post_processing(self):
        """Test du post-traitement des résultats."""
        # Créer une configuration de réseau
        reseau_config = ReseauCompletConfig(
            nom="Test",
            type="maillé",
            noeuds={
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
            conduites={
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        )
        
        # Résultats de simulation
        simulation_results = {
            "pressures": {"N1": 25.0, "N2": 18.0},  # N2 en violation
            "velocities": {"C1": 0.3},  # Vitesse trop faible
            "flows": {"C1": 0.02}
        }
        
        # Effectuer le post-traitement
        diagnostics = _perform_post_processing(simulation_results, reseau_config)
        
        # Vérifier les résultats
        assert diagnostics["connectivite_ok"] is True
        assert diagnostics["pression_ok"] is False  # N2 en violation
        assert diagnostics["vitesse_ok"] is False  # Vitesse trop faible
        assert len(diagnostics["violations"]) == 2
        
        # Vérifier les violations
        violation_types = [v["type"] for v in diagnostics["violations"]]
        assert "pression_min" in violation_types
        assert "vitesse_min" in violation_types


class TestNetworkCompleteUnifiedIntegration:
    """Tests d'intégration pour network_complete_unified."""
    
    @patch('lcpi.aep.calculations.network_complete_unified.SolverFactory')
    @patch('lcpi.aep.calculations.network_complete_unified.RichUI')
    @patch('lcpi.aep.calculations.network_complete_unified.console')
    def test_network_complete_unified_basic(self, mock_console, mock_rich_ui, mock_factory):
        """Test de base de la commande network_complete_unified."""
        # Mock de la factory
        mock_solver = MagicMock()
        mock_solver.get_solver_info.return_value = {
            "name": "Test Solver",
            "version": "1.0",
            "description": "Test",
            "capabilities": "Test"
        }
        mock_solver.run_simulation.return_value = {
            "status": "success",
            "pressions": {"N1": 25.0, "N2": 22.0},
            "flows": {"C1": 0.02},
            "velocities": {"C1": 1.0},
            "convergence": {"converge": True, "iterations": 5},
            "diagnostics": {"boucles_detectees": 1}
        }
        
        mock_factory.get_solver.return_value = mock_solver
        mock_factory.validate_solver_choice.return_value = {
            "compatible": True,
            "validation": {"valid": True, "errors": [], "warnings": []},
            "capabilities": {}
        }
        
        # Mock de la console
        mock_console.status.return_value.__enter__ = MagicMock()
        mock_console.status.return_value.__exit__ = MagicMock()
        
        # Créer un fichier YAML temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml_data = {
                "nom": "Réseau Test",
                "type": "maillé",
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
            yaml.dump(yaml_data, f)
            yaml_file = f.name
        
        try:
            # Tester la commande
            with patch('typer.Exit') as mock_exit:
                network_complete_unified(
                    input_file=Path(yaml_file),
                    solver="lcpi",
                    mode="auto",
                    export="json",
                    output=None,
                    verbose=False
                )
                
                # Vérifier que la commande s'est exécutée sans erreur
                mock_exit.assert_not_called()
                
                # Vérifier que le solveur a été appelé
                mock_factory.get_solver.assert_called_once_with("lcpi")
                mock_solver.run_simulation.assert_called_once()
                
        finally:
            Path(yaml_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
