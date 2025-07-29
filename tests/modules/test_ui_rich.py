import pytest
from unittest.mock import patch
from nanostruct.utils.ui_rich import afficher_action, afficher_resultat, afficher_erreur, poser_question, console

@pytest.fixture
def mock_console_print():
    with patch.object(console, 'print') as mock_print:
        yield mock_print

@pytest.fixture
def mock_prompt_ask():
    with patch('nanostruct.utils.ui_rich.Prompt.ask') as mock_ask:
        yield mock_ask

def test_afficher_action(mock_console_print):
    afficher_action("Test Action")
    mock_console_print.assert_called_once()
    assert "Test Action" in mock_console_print.call_args[0][0].renderable.plain
    assert "Action" in str(mock_console_print.call_args[0][0].title)

def test_afficher_resultat(mock_console_print):
    afficher_resultat("Test Resultat")
    mock_console_print.assert_called_once()
    assert "Test Resultat" in mock_console_print.call_args[0][0].renderable.plain
    assert "Résultat" in str(mock_console_print.call_args[0][0].title)

def test_afficher_erreur(mock_console_print):
    afficher_erreur("Test Erreur")
    mock_console_print.assert_called_once()
    assert "Test Erreur" in mock_console_print.call_args[0][0].renderable.plain
    assert "Erreur" in str(mock_console_print.call_args[0][0].title)

def test_poser_question_no_choices(mock_prompt_ask, mock_console_print):
    mock_prompt_ask.return_value = "User Answer"
    result = poser_question("What is your name?")
    mock_prompt_ask.assert_called_once()
    mock_console_print.assert_called_once()
    assert mock_console_print.call_args[0][0].title == "Question"
    assert "What is your name?" in mock_console_print.call_args[0][0].renderable
    assert mock_prompt_ask.call_args[1]['default'] is None
    assert result == "User Answer"

def test_poser_question_with_choices(mock_prompt_ask, mock_console_print):
    mock_prompt_ask.return_value = "Option1"
    result = poser_question("Choose an option:", choices=["Option1", "Option2"])
    mock_prompt_ask.assert_called_once()
    mock_console_print.assert_called_once()
    assert mock_console_print.call_args[0][0].title == "Question"
    assert "Choose an option:" in mock_console_print.call_args[0][0].renderable
    assert mock_prompt_ask.call_args[1]['choices'] == ["Option1", "Option2"]
    assert mock_prompt_ask.call_args[1]['default'] is None
    assert result == "Option1"

def test_poser_question_with_default(mock_prompt_ask, mock_console_print):
    mock_prompt_ask.return_value = "DefaultValue"
    result = poser_question("Enter value:", default="DefaultValue")
    mock_prompt_ask.assert_called_once()
    mock_console_print.assert_called_once()
    assert mock_console_print.call_args[0][0].title == "Question"
    assert "Enter value:" in mock_console_print.call_args[0][0].renderable
    assert mock_prompt_ask.call_args[1]['default'] == "DefaultValue"
    assert result == "DefaultValue"
