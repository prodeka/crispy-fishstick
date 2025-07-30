# utils/__init__.py

# Ce fichier transforme le dossier 'utils' en un paquet Python.
# Nous importons ici les fonctions les plus importantes de chaque sous-module
# pour les rendre directement accessibles depuis le paquet.
#
# Cela permet d'écrire "from utils import print_colored"
# au lieu de "from utils.ui import print_colored", ce qui est plus court et plus propre.

from .ui import (
    check_and_install_packages,
    initialize_colors,
    print_colored,
    get_input_with_default,
    get_menu_choice,
)

from .security import authenticate, display_disclaimer_and_get_agreement

from .logging_config import setup_logging

# La variable __all__ définit ce qui est importé si quelqu'un fait "from utils import *"
# C'est une bonne pratique de la définir.
__all__ = [
    "check_and_install_packages",
    "initialize_colors",
    "print_colored",
    "get_input_with_default",
    "get_menu_choice",
    "authenticate",
    "display_disclaimer_and_get_agreement",
    "setup_logging",
]
