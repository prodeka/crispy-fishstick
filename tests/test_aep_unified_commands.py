"""
Tests unitaires pour les commandes unifiées AEP

Ce module teste toutes les fonctionnalités des commandes *-unified :
- Options communes (--input, --mode, --export, --output, --verbose)
- Routage automatique (auto|simple|enhanced)
- Export vers différents formats
- Gestion d'erreurs
- Validation des données
"""

import pytest
import tempfile
import json
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os
import click

# Ajouter le chemin pour importer les modules AEP
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lcpi.aep.cli import (
    population_unified,
    demand_unified,
    network_unified,
    reservoir_unified,
    pumping_unified,
    hardy_cross_unified,
    validate_input,
    validate_population,
    validate_network
)
from lcpi.aep.core.validators import AEPValidationError


class TestAEPUnifiedCommands:
    """Tests pour les commandes unifiées AEP"""
    
    @pytest.fixture
    def temp_dir(self):
        """Crée un répertoire temporaire pour les tests"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    
    @pytest.fixture
    def population_data(self):
        """Données de test pour population"""
        return {
            "population_base": 1000,
            "taux_croissance": 0.02,
            "annees": 5,
            "methode": "malthus"
        }
    
    @pytest.fixture
    def population_enhanced_data(self):
        """Données de test pour population enhanced"""
        return {
            "population_base": 2000,
            "taux_croissance": 0.025,
            "annees": 10,
            "methode": "malthus",
            "verbose": True
        }
    
    @pytest.fixture
    def hardy_cross_data(self):
        """Données de test pour Hardy-Cross"""
        return {
            "noeuds": [
                {"id": "N1", "cote": 100, "demande": 0.0},
                {"id": "N2", "cote": 95, "demande": 0.05},
                {"id": "N3", "cote": 90, "demande": 0.05}
            ],
            "troncons": [
                {
                    "id": "P1",
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur": 100,
                    "diametre": 0.2,
                    "coefficient_rugosite": 130,
                    "debit_initial": 0.1
                },
                {
                    "id": "P2",
                    "noeud_amont": "N2",
                    "noeud_aval": "N3",
                    "longueur": 50,
                    "diametre": 0.15,
                    "coefficient_rugosite": 130,
                    "debit_initial": 0.05
                }
            ],
            "boucles": []
        }

    def test_population_unified_simple_mode(self, temp_dir, population_data):
        """Test population-unified en mode simple"""
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=population_data["population_base"],
                taux_croissance=population_data["taux_croissance"],
                annees=population_data["annees"],
                methode=population_data["methode"],
                verbose=False,
                input_file=None,
                mode="simple",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_population_unified_enhanced_mode(self, temp_dir, population_enhanced_data):
        """Test population-unified en mode enhanced"""
        # Créer un fichier YAML temporaire
        yaml_file = temp_dir / "test_population.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(population_enhanced_data, f)
        
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=None,
                taux_croissance=0.037,
                annees=20,
                methode="malthus",
                verbose=False,
                input_file=yaml_file,
                mode="enhanced",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_population_unified_auto_mode_with_input(self, temp_dir, population_data):
        """Test population-unified en mode auto avec --input"""
        # Créer un fichier YAML temporaire
        yaml_file = temp_dir / "test_population.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(population_data, f)
        
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=None,
                taux_croissance=0.037,
                annees=20,
                methode="malthus",
                verbose=False,
                input_file=yaml_file,
                mode="auto",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_population_unified_auto_mode_without_input(self, temp_dir):
        """Test population-unified en mode auto sans --input"""
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=1000,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="auto",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_population_unified_export_to_file(self, temp_dir, population_data):
        """Test population-unified avec export vers fichier"""
        output_file = temp_dir / "output.json"
        
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=population_data["population_base"],
                taux_croissance=population_data["taux_croissance"],
                annees=population_data["annees"],
                methode=population_data["methode"],
                verbose=False,
                input_file=None,
                mode="simple",
                export="json",
                output=output_file
            )
            
            # Vérifier que le fichier est créé
            assert output_file.exists()
            
            # Vérifier le contenu du fichier
            with open(output_file, 'r') as f:
                result = json.load(f)
                assert "valeurs" in result
                assert "diagnostics" in result
                assert "iterations" in result

    def test_population_unified_export_formats(self, temp_dir, population_data):
        """Test population-unified avec différents formats d'export"""
        formats = ["json", "yaml", "markdown", "csv", "html"]
        
        for fmt in formats:
            with patch('typer.echo') as mock_echo:
                population_unified(
                    population_base=population_data["population_base"],
                    taux_croissance=population_data["taux_croissance"],
                    annees=population_data["annees"],
                    methode=population_data["methode"],
                    verbose=False,
                    input_file=None,
                    mode="simple",
                    export=fmt,
                    output=None
                )
                
                # Vérifier que la sortie est générée
                mock_echo.assert_called()
                call_args = mock_echo.call_args_list
                output = None
                for call in call_args:
                    if call[0][0] and not call[0][0].startswith('✅'):
                        output = call[0][0]
                        break
                
                assert output is not None
                
                # Vérifier le format selon le type
                if fmt == "json":
                    assert output.startswith('{')
                elif fmt == "yaml":
                    assert "valeurs:" in output
                elif fmt == "markdown":
                    assert output.startswith('#')
                elif fmt == "csv":
                    assert "key,value" in output
                elif fmt == "html":
                    assert output.startswith('<!DOCTYPE html>')

    def test_population_unified_verbose_mode(self, temp_dir, population_data):
        """Test population-unified avec mode verbose"""
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=population_data["population_base"],
                taux_croissance=population_data["taux_croissance"],
                annees=population_data["annees"],
                methode=population_data["methode"],
                verbose=True,
                input_file=None,
                mode="simple",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_population_unified_error_handling(self, temp_dir):
        """Test population-unified avec gestion d'erreurs"""
        # Test avec mode enhanced sans --input
        with pytest.raises(click.exceptions.Exit):
            population_unified(
                population_base=None,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="enhanced",
                export="json",
                output=None
            )
        
        # Test avec mode simple sans population_base
        with pytest.raises(click.exceptions.Exit):
            population_unified(
                population_base=None,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="simple",
                export="json",
                output=None
            )
        
        # Test avec mode invalide
        with pytest.raises(click.exceptions.Exit):
            population_unified(
                population_base=1000,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="invalid",
                export="json",
                output=None
            )

    def test_hardy_cross_unified(self, temp_dir, hardy_cross_data):
        """Test hardy-cross-unified"""
        # Créer un fichier YAML temporaire
        yaml_file = temp_dir / "test_hardy_cross.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(hardy_cross_data, f)
        
        with patch('typer.echo') as mock_echo:
            hardy_cross_unified(
                input_file=yaml_file,
                tolerance=1e-6,
                max_iterations=100,
                formule="hazen_williams",
                export="json",
                output=None,
                verbose=False
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_hardy_cross_unified_error_handling(self, temp_dir):
        """Test hardy-cross-unified avec gestion d'erreurs"""
        # Test sans --input
        with pytest.raises(click.exceptions.Exit):
            hardy_cross_unified(
                input_file=None,
                tolerance=1e-6,
                max_iterations=100,
                formule="hazen_williams",
                export="json",
                output=None,
                verbose=False
            )

    def test_validate_population(self, temp_dir, population_data):
        """Test validate-population"""
        # Créer un fichier YAML temporaire
        yaml_file = temp_dir / "test_population.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(population_data, f)
        
        with patch('typer.echo') as mock_echo:
            validate_population(
                input_file=yaml_file,
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_validate_population_invalid_data(self, temp_dir):
        """Test validate-population avec données invalides"""
        # Créer un fichier YAML avec données invalides
        invalid_data = {
            "population_base": -1000,  # Population négative
            "taux_croissance": 0.03,
            "annees": 10,
            "methode": "malthus"
        }
        yaml_file = temp_dir / "test_invalid.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(invalid_data, f)
        
        with pytest.raises(click.exceptions.Exit):
            validate_population(
                input_file=yaml_file,
                export="json",
                output=None
            )

    def test_validate_input_auto_detection(self, temp_dir, population_data):
        """Test validate-input avec détection automatique"""
        # Créer un fichier YAML temporaire
        yaml_file = temp_dir / "test_population.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(population_data, f)
        
        with patch('typer.echo') as mock_echo:
            validate_input(
                input_file=yaml_file,
                data_type="auto",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie JSON est générée
            mock_echo.assert_called()
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            assert "diagnostics" in result
            assert "iterations" in result

    def test_export_formats_consistency(self, temp_dir, population_data):
        """Test que tous les formats d'export produisent des résultats cohérents"""
        formats = ["json", "yaml", "markdown", "csv", "html"]
        results = {}
        
        for fmt in formats:
            with patch('typer.echo') as mock_echo:
                population_unified(
                    population_base=population_data["population_base"],
                    taux_croissance=population_data["taux_croissance"],
                    annees=population_data["annees"],
                    methode=population_data["methode"],
                    verbose=False,
                    input_file=None,
                    mode="simple",
                    export=fmt,
                    output=None
                )
                
                # Récupérer la sortie
                call_args = mock_echo.call_args_list
                output = None
                for call in call_args:
                    if call[0][0] and not call[0][0].startswith('✅'):
                        output = call[0][0]
                        break
                
                results[fmt] = output
        
        # Vérifier que tous les formats produisent une sortie
        for fmt, output in results.items():
            assert output is not None, f"Format {fmt} n'a pas produit de sortie"
            
            # Vérifier que la sortie contient les informations essentielles
            if fmt == "json":
                result = json.loads(output)
                assert "valeurs" in result
                assert "population_base" in result["valeurs"]
            elif fmt == "yaml":
                assert "valeurs:" in output
                assert "population_base:" in output
            elif fmt == "markdown":
                assert "#" in output
                assert "population_base" in output
            elif fmt == "csv":
                assert "key,value" in output
                assert "population_base" in output
            elif fmt == "html":
                assert "<!DOCTYPE html>" in output
                assert "population_base" in output

    def test_mode_routing_logic(self, temp_dir, population_data):
        """Test de la logique de routage des modes"""
        # Créer un fichier YAML temporaire
        yaml_file = temp_dir / "test_population.yml"
        with open(yaml_file, 'w') as f:
            yaml.dump(population_data, f)
        
        # Test mode auto avec --input (doit basculer sur enhanced)
        with patch('typer.echo') as mock_echo:
            population_unified(
                population_base=None,
                taux_croissance=0.037,
                annees=20,
                methode="malthus",
                verbose=False,
                input_file=yaml_file,
                mode="auto",
                export="json",
                output=None
            )
            
            # Vérifier que la sortie contient les méthodes multiples (mode enhanced)
            call_args = mock_echo.call_args_list
            json_output = None
            for call in call_args:
                if call[0][0].startswith('{'):
                    json_output = call[0][0]
                    break
            
            assert json_output is not None
            result = json.loads(json_output)
            assert "valeurs" in result
            # Le mode enhanced produit des résultats avec arithmetique, geometrique, logistique
            if "arithmetique" in result["valeurs"]:
                assert "geometrique" in result["valeurs"]
                assert "logistique" in result["valeurs"]

    def test_error_messages_consistency(self, temp_dir):
        """Test de la cohérence des messages d'erreur"""
        # Test mode enhanced sans --input
        with pytest.raises(click.exceptions.Exit):
            population_unified(
                population_base=None,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="enhanced",
                export="json",
                output=None
            )
        
        # Test mode simple sans population_base
        with pytest.raises(click.exceptions.Exit):
            population_unified(
                population_base=None,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="simple",
                export="json",
                output=None
            )
        
        # Test mode invalide
        with pytest.raises(click.exceptions.Exit):
            population_unified(
                population_base=1000,
                taux_croissance=0.02,
                annees=5,
                methode="malthus",
                verbose=False,
                input_file=None,
                mode="invalid",
                export="json",
                output=None
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
