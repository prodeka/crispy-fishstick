# utils/security.py
import getpass
from .ui import print_colored  # On importe depuis le même paquet 'utils'

# ==============================================================================
# MODULE DE GESTION DE LA SÉCURITÉ
# ==============================================================================


def authenticate():
    """
    Gère un système d'authentification avec 3 tentatives,
    puis demande s'il faut réessayer.
    """
    PASSWORD = "nano14TD"  # Le mot de passe

    while True:  # Boucle principale pour permettre de réessayer
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                entered_password = getpass.getpass("Veuillez entrer le mot de passe : ")
                if entered_password == PASSWORD:
                    print_colored("Authentification réussie.", "green")
                    return True  # L'authentification a réussi, on sort de tout
            except Exception as e:
                print_colored(f"Une erreur est survenue lors de la saisie : {e}", "red")
                # On considère cela comme une tentative échouée

            remaining_attempts = max_attempts - (attempt + 1)
            if remaining_attempts > 0:
                print_colored(
                    f"Mot de passe incorrect. Il vous reste {remaining_attempts} essai(s).",
                    "red",
                )
            else:
                print_colored(
                    "\nNombre maximum de tentatives atteint.", "red", bold=True
                )

        # Après les 3 tentatives, on demande à l'utilisateur s'il veut recommencer
        while True:
            retry = (
                input("Voulez-vous réessayer l'authentification ? [o/n] : ")
                .lower()
                .strip()
            )
            if retry == "o":
                break  # On sort de cette petite boucle pour recommencer la grande boucle
            elif retry == "n":
                print_colored(
                    "Authentification échouée. Le programme va se fermer.", "red"
                )
                return False  # L'utilisateur abandonne
            else:
                print_colored(
                    "Réponse invalide. Veuillez entrer 'o' pour oui ou 'n' pour non.",
                    "yellow",
                )

        # Si l'utilisateur a tapé 'o', la grande boucle while recommencera


def display_disclaimer_and_get_agreement():
    """Affiche l'avertissement et demande l'accord de l'utilisateur."""
    disclaimer = """
    AVERTISSEMENT ET CONDITIONS D'UTILISATION
    -------------------------------------------
    Ce programme est fourni à des fins purement ÉDUCATIVES et comme
    démonstration de concepts d'ingénierie. Les calculs qu'il effectue
    peuvent contenir des erreurs ou des simplifications.

    L'UTILISATEUR EST SEUL RESPONSABLE de la vérification, de la validation
    et de l'interprétation des résultats. L'auteur ne peut être tenu
    responsable des conséquences de l'utilisation de ce logiciel.
    """
    print_colored(disclaimer, "yellow")
    while True:
        choice = input("Acceptez-vous ces conditions ? [o/n] : ").lower().strip()
        if choice == "o":
            return True
        elif choice == "n":
            print_colored(
                "Vous avez refusé les conditions. Le programme va se fermer.", "red"
            )
            return False
        else:
            print_colored("Veuillez répondre par 'o' (oui) ou 'n' (non).", "red")
