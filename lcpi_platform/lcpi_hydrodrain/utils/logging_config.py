# utils/logging_config.py
import logging


def setup_logging():
    """Configure un logger pour écrire dans un fichier et dans la console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="dimensionnement.log",
        filemode="w",  # 'w' pour écraser le log à chaque lancement
    )

    # Créer un handler pour la console qui affiche uniquement les messages INFO
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # On utilise un formatter vide pour la console pour un affichage plus propre
    # car print_colored gère déjà l'affichage
    console.setFormatter(logging.Formatter("%(message)s"))

    # Eviter d'ajouter plusieurs fois le handler si la fonction est appelée plusieurs fois
    if not logging.getLogger("").handlers:
        logging.getLogger("").addHandler(console)
