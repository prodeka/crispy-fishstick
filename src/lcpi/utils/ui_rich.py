from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()


def afficher_action(message: str):
    """Affiche une action ou une étape en cours."""
    console.print(
        Panel(
            Text(message, style="bold blue"),
            title="[bold blue]Action[/bold blue]",
            border_style="blue",
        )
    )


def afficher_resultat(message: str):
    """Affiche un résultat ou une information importante."""
    console.print(
        Panel(
            Text(message, style="bold green"),
            title="[bold green]Résultat[/bold green]",
            border_style="green",
        )
    )


def afficher_erreur(message: str):
    """Affiche un message d'erreur."""
    console.print(
        Panel(
            Text(message, style="bold red"),
            title="[bold red]Erreur[/bold red]",
            border_style="red",
        )
    )


def poser_question(question, default=None, choices=None, password=False, value_type=str):
    """
    Pose une question stylisée à l'utilisateur et gère la conversion de type.
    """
    console.print(Panel(question, title="Question", style="yellow", border_style="dim"))
    while True:
        try:
            reponse_str = Prompt.ask(
                "Votre réponse",
                default=str(default) if default is not None else None,
                choices=choices,
                password=password
            )
            valeur_convertie = value_type(reponse_str)
            return valeur_convertie
        except (ValueError, TypeError):
            afficher_erreur(f"Entrée invalide. Veuillez entrer une valeur de type '{value_type.__name__}'.")


def afficher_menu_et_choisir(titre_menu, options_dict, default=None):
    """Affiche un menu stylisé dans un Panel et demande un choix."""
    
    # Construit le texte des options à partir du dictionnaire
    texte_options = "\n".join([f"[{k}] {v}" for k, v in options_dict.items()])
    
    # Affiche le panneau contenant les options
    console.print(
        Panel(
            texte_options,
            title=titre_menu,
            style="white",
            border_style="dim"
        )
    )
    
    # Pose la question pour le choix
    choix = Prompt.ask("Votre choix", choices=options_dict.keys(), default=default)
    return choix
