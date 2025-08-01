"""
Tests unitaires pour les utilitaires de commandes CLI.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lcpi.utils.command_helpers import (
    show_input_parameters,
    create_parameter_dict,
    check_required_params,
    create_typer_option
)


class TestCreateParameterDict:
    """Tests pour la fonction create_parameter_dict."""
    
    def test_create_parameter_dict_basic(self):
        """Test de création d'un paramètre de base."""
        param = create_parameter_dict("test", "Description du test")
        
        assert param["name"] == "test"
        assert param["help"] == "Description du test"
        assert "short" not in param
        assert "default" not in param
    
    def test_create_parameter_dict_with_short(self):
        """Test de création d'un paramètre avec option courte."""
        param = create_parameter_dict("test", "Description", "t")
        
        assert param["name"] == "test"
        assert param["help"] == "Description"
        assert param["short"] == "t"
    
    def test_create_parameter_dict_with_default(self):
        """Test de création d'un paramètre avec valeur par défaut."""
        param = create_parameter_dict("test", "Description", default=42)
        
        assert param["name"] == "test"
        assert param["help"] == "Description"
        assert param["default"] == 42
    
    def test_create_parameter_dict_complete(self):
        """Test de création d'un paramètre complet."""
        param = create_parameter_dict("test", "Description", "t", 42)
        
        assert param["name"] == "test"
        assert param["help"] == "Description"
        assert param["short"] == "t"
        assert param["default"] == 42


class TestCheckRequiredParams:
    """Tests pour la fonction check_required_params."""
    
    def test_check_required_params_all_provided(self):
        """Test avec tous les paramètres fournis."""
        result = check_required_params(1, 2, 3, a=4, b=5)
        assert result is True
    
    def test_check_required_params_none_positional(self):
        """Test avec un paramètre positionnel None."""
        result = check_required_params(1, None, 3)
        assert result is False
    
    def test_check_required_params_none_keyword(self):
        """Test avec un paramètre nommé None."""
        result = check_required_params(1, 2, a=None, b=5)
        assert result is False
    
    def test_check_required_params_empty(self):
        """Test avec aucun paramètre."""
        result = check_required_params()
        assert result is True


class TestCreateTyperOption:
    """Tests pour la fonction create_typer_option."""
    
    def test_create_typer_option_required_with_short(self):
        """Test de création d'une option requise avec option courte."""
        option = create_typer_option("test", "Description", "t", required=True)
        
        # Vérifier que c'est bien une option Typer
        assert hasattr(option, 'default')
        assert option.default is None
    
    def test_create_typer_option_required_without_short(self):
        """Test de création d'une option requise sans option courte."""
        option = create_typer_option("test", "Description", required=True)
        
        assert hasattr(option, 'default')
        assert option.default is None
    
    def test_create_typer_option_optional_with_short(self):
        """Test de création d'une option optionnelle avec option courte."""
        option = create_typer_option("test", "Description", "t", default=42)
        
        assert hasattr(option, 'default')
        assert option.default == 42
    
    def test_create_typer_option_optional_without_short(self):
        """Test de création d'une option optionnelle sans option courte."""
        option = create_typer_option("test", "Description", default=42)
        
        assert hasattr(option, 'default')
        assert option.default == 42


class TestShowInputParameters:
    """Tests pour la fonction show_input_parameters."""
    
    @patch('lcpi.utils.command_helpers.console')
    def test_show_input_parameters_basic(self, mock_console):
        """Test d'affichage basique des paramètres."""
        required_params = [
            create_parameter_dict("param1", "Description 1", "p1"),
            create_parameter_dict("param2", "Description 2", "p2")
        ]
        
        show_input_parameters("Test Command", required_params)
        
        # Vérifier que console.print a été appelé
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        
        # Vérifier que c'est bien un Panel Rich
        from rich.panel import Panel
        assert isinstance(call_args, Panel)
        
        # Vérifier le contenu du panel
        panel_content = call_args.renderable
        assert "Test Command" in str(panel_content)
        assert "param1" in str(panel_content)
        assert "param2" in str(panel_content)
        assert "Description 1" in str(panel_content)
        assert "Description 2" in str(panel_content)
    
    @patch('lcpi.utils.command_helpers.console')
    def test_show_input_parameters_with_optional(self, mock_console):
        """Test d'affichage avec paramètres optionnels."""
        required_params = [
            create_parameter_dict("param1", "Description 1", "p1")
        ]
        
        optional_params = [
            create_parameter_dict("opt1", "Optional 1", "o1", default=42),
            create_parameter_dict("opt2", "Optional 2", default="test")
        ]
        
        show_input_parameters("Test Command", required_params, optional_params)
        
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        
        # Vérifier le contenu du panel
        panel_content = call_args.renderable
        assert "param1" in str(panel_content)
        assert "opt1" in str(panel_content)
        assert "opt2" in str(panel_content)
        assert "42" in str(panel_content)  # Valeur par défaut
        assert "test" in str(panel_content)  # Valeur par défaut
    
    @patch('lcpi.utils.command_helpers.console')
    def test_show_input_parameters_with_examples(self, mock_console):
        """Test d'affichage avec exemples."""
        required_params = [
            create_parameter_dict("param1", "Description 1", "p1")
        ]
        
        examples = [
            "lcpi test command --param1 value1",
            "lcpi test command -p1 value1"
        ]
        
        show_input_parameters("Test Command", required_params, examples=examples)
        
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        
        # Vérifier le contenu du panel
        panel_content = call_args.renderable
        assert "lcpi test command --param1 value1" in str(panel_content)
        assert "lcpi test command -p1 value1" in str(panel_content)
    
    @patch('lcpi.utils.command_helpers.console')
    def test_show_input_parameters_with_description(self, mock_console):
        """Test d'affichage avec description."""
        required_params = [
            create_parameter_dict("param1", "Description 1", "p1")
        ]
        
        description = "Ceci est une description de test"
        
        show_input_parameters("Test Command", required_params, description=description)
        
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        
        # Vérifier le contenu du panel
        panel_content = call_args.renderable
        assert description in str(panel_content)
    
    @patch('lcpi.utils.command_helpers.console')
    def test_show_input_parameters_complete(self, mock_console):
        """Test d'affichage complet avec tous les paramètres."""
        required_params = [
            create_parameter_dict("param1", "Description 1", "p1"),
            create_parameter_dict("param2", "Description 2", "p2")
        ]
        
        optional_params = [
            create_parameter_dict("opt1", "Optional 1", "o1", default=42)
        ]
        
        examples = [
            "lcpi test command --param1 value1 --param2 value2",
            "lcpi test command -p1 value1 -p2 value2 --opt1 100"
        ]
        
        description = "Description complète de la commande"
        
        show_input_parameters(
            "Test Command",
            required_params,
            optional_params,
            examples,
            description
        )
        
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        
        # Vérifier le contenu du panel
        panel_content = call_args.renderable
        
        # Vérifier tous les éléments
        assert "Test Command" in str(panel_content)
        assert "param1" in str(panel_content)
        assert "param2" in str(panel_content)
        assert "opt1" in str(panel_content)
        assert "42" in str(panel_content)
        assert "lcpi test command --param1 value1" in str(panel_content)
        assert "lcpi test command -p1 value1 -p2 value2" in str(panel_content)
        assert description in str(panel_content)


if __name__ == "__main__":
    pytest.main([__file__]) 