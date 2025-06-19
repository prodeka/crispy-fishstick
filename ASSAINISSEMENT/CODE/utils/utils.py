# utils.py
import sys
import subprocess
import importlib.util
import os
import getpass
import logging

try:
    from colorama import init, Fore, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

def initialize_colors():
    """Initialise colorama si disponible."""
    if COLORAMA_AVAILABLE:
        init(autoreset=True)

def check_and_install_packages(packages):
    """Vérifie et installe les dépendances manquantes."""
    print("Vérification des dépendances requises...")
    missing_packages = [pkg for pkg in packages if importlib.util.find_spec(pkg.split('==')[0]) is None]
    
    if missing_packages:
        print(f"Paquets manquants : {', '.join(missing_packages)}")
        print("Tentative d'installation avec pip...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                print(f"\nERREUR CRITIQUE : Impossible d'installer '{package}'.")
                print(f"Veuillez l'installer manuellement : pip install {package}")
                sys.exit(1)
        print("Toutes les dépendances sont maintenant installées.")
        global COLORAMA_AVAILABLE
        if 'colorama' in missing_packages and importlib.util.find_spec('colorama'):
            from colorama import init, Fore, Style
            COLORAMA_AVAILABLE = True
    else:
        print("Toutes les dépendances sont déjà présentes.")

def print_colored(text, color_name="yellow", bold=False):
    """Affiche du texte en couleur en utilisant colorama si possible."""
    if COLORAMA_AVAILABLE:
        color_map = {
            "yellow": Fore.YELLOW, "green": Fore.GREEN, "cyan": Fore.CYAN,
            "red": Fore.RED, "magenta": Fore.MAGENTA, "white": Fore.WHITE,
        }
        style = Style.BRIGHT if bold else ""
        color = color_map.get(color_name.lower(), Fore.WHITE)
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def setup_logging():
    """Configure un logger pour écrire dans un fichier."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='dimensionnement.log',
        filemode='w' # 'w' pour écraser le log à chaque lancement, 'a' pour ajouter
    )
    # Ajouter un handler pour aussi afficher les messages dans la console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s') # Format simple pour la console
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
