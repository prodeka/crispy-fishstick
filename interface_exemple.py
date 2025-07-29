from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


def afficher_action(message: str):
    """Affiche un message d'action dans un panneau neutre."""
    console.print(
        Panel(message, style="white on default", title="Action", title_align="left")
    )


def afficher_resultat(message: str):
    """Affiche un message de résultat dans un panneau vert."""
    console.print(
        Panel(message, style="green on default", title="Résultat", title_align="left")
    )


def afficher_erreur(message: str):
    """Affiche un message d'erreur dans un panneau rouge."""
    console.print(
        Panel(message, style="red on default", title="Erreur", title_align="left")
    )


def poser_question(question: str, default: str = None) -> str:
    """Pose une question à l'utilisateur et retourne sa réponse."""
    console.print(
        Panel(question, style="yellow on default", title="Question", title_align="left")
    )
    return Prompt.ask("Votre réponse", default=default)


if __name__ == "__main__":
    afficher_action("Initialisation du processus...")
    afficher_resultat("Opération terminée avec succès !")
    afficher_erreur("Une erreur inattendue est survenue.")
    reponse = poser_question("Voulez-vous continuer ?", default="oui")
    afficher_resultat(f"Votre réponse : {reponse}")
