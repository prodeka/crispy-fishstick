import sys
import argparse  # <-- Import de la bibliothèque pour les arguments
from nanostruct.utils import settings  # <-- On importe le module settings directement
from nanostruct.utils.ui_helpers import display_header, check_dependencies
from colorama import init

from nanostruct.modules.beton_arme.ba_entry import start_ba_module
from nanostruct.modules.assainissement.main import main as start_assainissement_module
from nanostruct.modules.bois.main import main as start_bois_module

init(autoreset=True)

def main():
    """Fonction principale contenant la logique du programme."""
    display_header()
    
    if not check_dependencies():
        sys.exit(1)
    
    # Le menu principal reste le même
    main_menu()

def main_menu():
    """Affiche le menu principal et gère la navigation entre les domaines."""
    while True:
        print("\n--- Menu Principal ---")
        print("Veuillez choisir un domaine de calcul :")
        print("[1] Assainissement")
        print("[2] Béton Armé (BA)")
        print("[3] Bois")
        print("[0] Quitter")
        
        choice = input("Votre choix : ").strip() # .strip() nettoie les espaces
        
        if not choice: # Si l'utilisateur a juste appuyé sur Entrée, on continue
            continue
            
        if choice == '1':
            start_assainissement_module()
        elif choice == '2':
            start_ba_module()
        elif choice == '3':
            start_bois_module()
        elif choice == '0':
            print("Merci d'avoir utilisé le programme. À bientôt !")
            sys.exit(0)
        else:
            print("Choix invalide ou fonctionnalité non implémentée.")

# C'est ici que la magie opère
if __name__ == "__main__":
    # 1. On configure le parser d'arguments
    parser = argparse.ArgumentParser(description="Plateforme de calcul pour l'ingénierie.")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',  # Si le flag est présent, la valeur devient True
        help="Active l'affichage détaillé des calculs (mode pédagogique)."
    )
    args = parser.parse_args()

    # 2. On met à jour notre variable globale de configuration
    # Si l'utilisateur a tapé "-v", args.verbose sera True.
    settings.VERBOSE = args.verbose
    
    # 3. On lance le programme principal
    main()