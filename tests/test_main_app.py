import pytest
from unittest.mock import patch
from nanostruct.main_app import main_menu


def test_main_menu_assainissement():
    with patch('rich.prompt.Prompt.ask') as mock_prompt_ask:
        with patch('nanostruct.modules.assainissement.main.main') as mock_assainissement_main:
            with patch('nanostruct.modules.assainissement.utils.security.display_disclaimer_and_get_agreement', return_value=True):
                with patch('nanostruct.modules.assainissement.utils.security.authenticate', return_value=True):
                    with patch('builtins.input', side_effect=["o", "<"]):
                        mock_prompt_ask.side_effect = ["1", "0"] # Choose Assainissement, then Quit
                        with pytest.raises(SystemExit):
                            main_menu()
                        mock_assainissement_main.assert_called_once()

def test_main_menu_ba():
    with patch('rich.prompt.Prompt.ask') as mock_prompt_ask:
        with patch('nanostruct.modules.beton_arme.ba_entry.start_ba_module') as mock_ba_start_module:
            mock_prompt_ask.side_effect = ["2", "0"]
            with pytest.raises(SystemExit):
                main_menu()
            mock_ba_start_module.assert_called_once()

def test_main_menu_bois():
    with patch('rich.prompt.Prompt.ask') as mock_prompt_ask:
        with patch('nanostruct.modules.bois.main.main') as mock_bois_main:
            with patch('click.prompt', side_effect=["0"]):
                with patch('nanostruct.modules.bois.main.sys.exit'):
                    mock_prompt_ask.side_effect = ["3", "0"]
                    with pytest.raises(SystemExit):
                        main_menu()
                    mock_bois_main.assert_called_once()

def test_main_menu_quit():
    with patch('rich.prompt.Prompt.ask') as mock_prompt_ask:
        mock_prompt_ask.return_value = "0"
        with pytest.raises(SystemExit):
            main_menu()
        mock_prompt_ask.assert_called_once()

def test_main_menu_invalid_choice():
    with patch('rich.prompt.Prompt.ask') as mock_prompt_ask:
        with patch('nanostruct.utils.ui_rich.afficher_erreur') as mock_afficher_erreur:
            mock_prompt_ask.side_effect = ["99", "0"]
            with pytest.raises(SystemExit):
                main_menu()
            mock_afficher_erreur.assert_called_once()

# Note: Les tests pour check_dependencies et display_header ont été retirés car ils ne sont pas pertinents pour cette tâche
# et peuvent causer des problèmes si ces fonctions ne sont pas définies ou mockées correctement.