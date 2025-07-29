import pytest
from unittest.mock import patch
from nanostruct.main_app import main_menu

def test_main_menu_exit():
    """
    Tests if the main_menu function exits gracefully when the user chooses '0'.
    """
    with patch('builtins.input', return_value='0'):
        with pytest.raises(SystemExit) as e:
            main_menu()
    assert e.type is SystemExit
    assert e.value.code == 0

def test_main_menu_selection():
    """
    Tests if the main_menu function correctly calls the selected module.
    """
    with patch('builtins.input', side_effect=['1', '0']):
        with patch('nanostruct.main_app.start_assainissement_module') as mock_start_assainissement:
             with pytest.raises(SystemExit):
                main_menu()
    mock_start_assainissement.assert_called_once()
