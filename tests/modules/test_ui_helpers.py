import pytest
from unittest.mock import patch, MagicMock
from nanostruct.utils.ui_helpers import display_header, check_dependencies, get_user_input, v_print
from nanostruct.utils import settings
from nanostruct.utils.ui_rich import console # Import console for v_print assertions

@pytest.fixture
def mock_afficher_resultat():
    with patch('nanostruct.utils.ui_helpers.afficher_resultat') as mock:
        yield mock

@pytest.fixture
def mock_afficher_erreur():
    with patch('nanostruct.utils.ui_helpers.afficher_erreur') as mock:
        yield mock

@pytest.fixture
def mock_console_print():
    with patch.object(console, 'print') as mock:
        yield mock

def test_display_header(mock_afficher_resultat):
    display_header()
    mock_afficher_resultat.assert_called_once()
    assert "Copyright" in mock_afficher_resultat.call_args[0][0]

def test_check_dependencies_success(mock_afficher_resultat, mock_afficher_erreur):
    with patch('importlib.util.find_spec', return_value=MagicMock()): # Mock find_spec to return a non-None value
        result = check_dependencies()
        assert result is True
        mock_afficher_resultat.assert_called_once_with("Vérification des dépendances... OK")
        mock_afficher_erreur.assert_not_called()

def test_check_dependencies_failure(mock_afficher_resultat, mock_afficher_erreur):
    with patch('importlib.util.find_spec', side_effect=[None, MagicMock()]): # pandas missing, numpy present
        result = check_dependencies()
        assert result is False
        assert mock_afficher_erreur.call_count == 2 # Should be called twice for two error messages
        assert "Dépendances critiques manquantes : pandas." in mock_afficher_erreur.call_args_list[0][0][0]
        mock_afficher_resultat.assert_not_called()

def test_get_user_input_valid_float(mock_afficher_erreur):
    with patch('builtins.input', return_value="123.45"):
        result = get_user_input("Enter a float:", data_type=float)
        assert result == 123.45
        mock_afficher_erreur.assert_not_called()

def test_get_user_input_invalid_then_valid(mock_afficher_erreur):
    with patch('builtins.input', side_effect=["abc", "67.89"]):
        result = get_user_input("Enter a float:", data_type=float)
        assert result == 67.89
        mock_afficher_erreur.assert_called_once()
        assert "Veuillez entrer une valeur valide de type 'float'." in mock_afficher_erreur.call_args[0][0]

def test_get_user_input_with_default(mock_afficher_erreur):
    with patch('builtins.input', return_value=""):
        result = get_user_input("Enter a float:", default_value=10.0, data_type=float)
        assert result == 10.0
        mock_afficher_erreur.assert_not_called()

def test_v_print_verbose_on(mock_console_print):
    settings.VERBOSE = True
    v_print("Label", "Formula", "Numeric App", 123.456, "unit")
    assert mock_console_print.call_count == 4
    assert "Label" in mock_console_print.call_args_list[0][0][0]
    assert "Formula" in mock_console_print.call_args_list[1][0][0]
    assert "Numeric App" in mock_console_print.call_args_list[2][0][0]
    assert "123.46 unit" in mock_console_print.call_args_list[3][0][0]

def test_v_print_verbose_off(mock_console_print):
    settings.VERBOSE = False
    v_print("Label", "Formula", "Numeric App", 123.456, "unit")
    mock_console_print.assert_not_called()
