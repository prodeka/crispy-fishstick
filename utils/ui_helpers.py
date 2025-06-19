# PROJET_DIMENTIONEMENT/utils/ui_helpers.py
# Contient les fonctions pour communiquer avec l'utilisateur

# --- Toutes les importations sont regroupées en haut ---
import sys
from datetime import datetime
from utils import settings
from colorama import Fore, Style, init

# On initialise colorama une seule fois ici aussi par sécurité
init(autoreset=True)

def display_header():
    """Affiche l'en-tête de copyright en couleur."""
    current_year = datetime.now().year
    header = f"""
===================================================================
    Copyright (c) {current_year} TABE DJATO Serge / intrepidcore
    Auteur : TABE DJATO Serge
    Dépôt GitHub : https://github.com/prodeka
===================================================================
    """
    print(Fore.CYAN + header)

def check_dependencies():
    """Vérifie si les dépendances critiques sont bien installées."""
    try:
        import pandas
        import numpy
        print(f"{Fore.GREEN}Vérification des dépendances... OK")
        return True
    except ImportError as e:
        print(f"{Fore.RED}ERREUR: Dépendance critique manquante : {e.name}.")
        print(f"{Fore.YELLOW}Veuillez lancer le programme via 'install_and_run.bat' ou './install_and_run.sh'.")
        return False

def get_user_input(prompt, default_value=None, data_type=float):
    """Pose une question à l'utilisateur et gère les erreurs de saisie."""
    while True:
        if default_value is not None:
            prompt_message = f"{prompt} (défaut: {default_value}): "
        else:
            prompt_message = f"{prompt}: "
            
        user_input = input(prompt_message).strip()
        
        if not user_input and default_value is not None:
            return default_value
        
        try:
            return data_type(user_input)
        except (ValueError, TypeError):
            print(f"{Fore.RED}Erreur : Veuillez entrer une valeur valide de type '{data_type.__name__}'.")

def v_print(label, formula, numeric_app, result, unit=""):
    """
    Affiche un calcul détaillé en suivant un format pédagogique multi-lignes
    et coloré, uniquement si le mode VERBOSE est activé.
    """
    if settings.VERBOSE:
        if isinstance(result, float):
            result_str = f"{result:.2f}"
        else:
            result_str = str(result)
        
        # On utilise des f-strings pour insérer les couleurs et les réinitialiser manuellement
        # pour un contrôle total sur l'affichage.
        print(f"\n  -> {Fore.WHITE}{Style.BRIGHT}{label}{Style.RESET_ALL}")
        print(f"     {Fore.GREEN}Formule       : {formula}{Style.RESET_ALL}")
        print(f"     {Fore.YELLOW}Application   : {numeric_app}{Style.RESET_ALL}")
        print(f"     {Fore.CYAN}Résultat      : {result_str} {unit}{Style.RESET_ALL}")