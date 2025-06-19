# utils/ui.py
import sys
import subprocess
import importlib.util
import os

try:
    from colorama import init, Fore, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# ... (les fonctions initialize_colors, print_colored, check_and_install_packages ne changent pas) ...
def initialize_colors():
    """Initialise colorama si disponible."""
    if COLORAMA_AVAILABLE:
        init(autoreset=True)

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

def check_and_install_packages(packages):
    """Vérifie et installe les dépendances manquantes."""
    print_colored("Vérification des dépendances requises...", "cyan")
    missing_packages = [pkg for pkg in packages if importlib.util.find_spec(pkg.split('==')[0]) is None]
    
    if missing_packages:
        print_colored(f"Paquets manquants : {', '.join(missing_packages)}", "yellow")
        print_colored("Tentative d'installation avec pip...", "yellow")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                print_colored(f"\nERREUR CRITIQUE : Impossible d'installer '{package}'.", "red", bold=True)
                print_colored(f"Veuillez l'installer manuellement : pip install {package}", "red")
                sys.exit(1)
        print_colored("Toutes les dépendances sont maintenant installées.", "green")
        if 'colorama' in missing_packages and importlib.util.find_spec('colorama'):
            global COLORAMA_AVAILABLE
            from colorama import init, Fore, Style
            COLORAMA_AVAILABLE = True
    else:
        print_colored("Toutes les dépendances sont déjà présentes.", "green")


# ***** MODIFIÉ : Ajout de la possibilité de retour *****
def get_input_with_default(prompt, default, type_converter=float):
    """
    Demande une entrée à l'utilisateur, avec une valeur par défaut.
    L'utilisateur peut taper '<' pour retourner en arrière (la fonction renvoie None).
    """
    while True:
        user_input = input(f"{prompt} (ou '<' pour retour) [défaut: {default}] : ").strip().replace(',', '.')
        if user_input == "<":
            return None # Signal pour retourner en arrière
        if user_input == "":
            return default
        try:
            return type_converter(user_input)
        except ValueError:
            print_colored(f"Entrée invalide. Veuillez entrer un nombre ou '<'.", "red")

# ***** MODIFIÉ : Ajout de la possibilité de retour *****
def get_menu_choice(prompt, options):
    """
    Affiche un menu numéroté et retourne la clé du choix de l'utilisateur.
    L'utilisateur peut taper '<' pour retourner en arrière (la fonction renvoie None).
    """
    while True:
        print_colored(prompt, "bold")
        for key, value in options.items():
            print(f"  [{key}] {value}")
        print_colored("  [<] Retour", "yellow") # Option de retour visible
        
        choix = input("Votre choix : ").strip().lower()
        
        if choix == '<':
            return None # Signal pour retourner en arrière
        if choix in options:
            return choix
            
        print_colored("Choix non valide. Veuillez réessayer.", "red")