# PROJET_DIMENTIONEMENT/utils/ui_helpers.py
# Contient les fonctions pour communiquer avec l'utilisateur

# --- Toutes les importations sont regroupées en haut ---
from datetime import datetime
from lcpi_platform.lcpi_core.utils import settings
import importlib.util
from lcpi_platform.lcpi_core.utils.ui_rich import afficher_resultat, afficher_erreur, console


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
    afficher_resultat(header)


def check_dependencies():
    """Vérifie si les dépendances critiques sont bien installées."""
    required_packages = ["pandas", "numpy"]
    missing_packages = []
    for pkg in required_packages:
        if importlib.util.find_spec(pkg) is None:
            missing_packages.append(pkg)

    if missing_packages:
        afficher_erreur(
            f"Dépendances critiques manquantes : {', '.join(missing_packages)}."
        )
        afficher_erreur(
            "Veuillez lancer le programme via 'install_and_run.bat' ou './install_and_run.sh'."
        )
        return False
    else:
        afficher_resultat("Vérification des dépendances... OK")
        return True


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
            afficher_erreur(
                f"Erreur : Veuillez entrer une valeur valide de type '{data_type.__name__}'."
            )


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
        console.print(f"  -> [bold white]{label}[/bold white]")
        console.print(f"     [green]Formule       : {formula}[/green]")
        console.print(f"     [yellow]Application   : {numeric_app}[/yellow]")
        console.print(f"     [cyan]Résultat      : {result_str} {unit}[/cyan]")
