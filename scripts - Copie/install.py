

import os
import subprocess
import sys
import urllib.request

def check_internet_connection(url='http://www.google.com', timeout=5):
    """Tente d'ouvrir une URL pour vérifier la connexion Internet. Plus fiable."""
    try:
        urllib.request.urlopen(url, timeout=timeout)
        print("Connexion Internet détectée.")
        return True
    except (urllib.error.URLError, ConnectionResetError):
        print("Pas de connexion Internet détectée.")
        return False

def install_requirements(offline=False):
    """Installe les dépendances en ligne ou hors ligne."""
    if offline:
        print("\nTentative d'installation des dépendances en mode hors ligne...")
        vendor_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vendor', 'packages'))
        
        if not os.path.isdir(vendor_dir):
            print(f"ERREUR : Le dossier des paquets hors ligne n'a pas été trouvé : {vendor_dir}", file=sys.stderr)
            return False
        
        command = [
            sys.executable, "-m", "pip", "install",
            "--no-index",
            f"--find-links={vendor_dir}",
            "-r", "requirements.txt"
        ]
    else:
        print("\nTentative d'installation des dépendances en ligne...")
        command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

    try:
        # Exécuter la commande depuis la racine du projet
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        subprocess.check_call(command, cwd=project_root)
        print("Dépendances installées avec succès.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERREUR lors de l'installation : {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("ERREUR: Le fichier 'requirements.txt' est introuvable à la racine du projet.", file=sys.stderr)
        return False


def setup_project():
    """Met en place la structure du projet."""
    print("Configuration du projet terminée.")

def main():
    online_retries = 0
    max_online_retries = 3

    while True:
        # Toujours tenter en ligne d'abord si les re-essais ne sont pas épuisés
        if online_retries < max_online_retries and check_internet_connection():
            if install_requirements(offline=False):
                setup_project()
                return # Succès, on sort

        # Si on arrive ici, c'est que l'installation en ligne a échoué ou n'était pas possible
        print("\nL'installation en ligne a échoué ou la connexion est instable.")
        
        choice = ''
        if online_retries < max_online_retries:
            prompt = "Choisissez une option : [R]éessayer en ligne, [O]ffline, [N]e rien faire : "
            valid_choices = ['r', 'o', 'n']
        else:
            print("Le nombre maximum de tentatives en ligne a été atteint.")
            prompt = "Choisissez une option : [O]ffline, [N]e rien faire : "
            valid_choices = ['o', 'n']

        while choice not in valid_choices:
            choice = input(prompt).lower().strip()

        if choice == 'r':
            online_retries += 1
            continue # Boucle pour réessayer en ligne
        elif choice == 'o':
            if install_requirements(offline=True):
                setup_project()
            else:
                print("\nL'installation hors ligne a également échoué. Vérifiez que le dossier 'vendor/packages' est complet.", file=sys.stderr)
            return # Termine, que ce soit un succès ou un échec
        elif choice == 'n':
            print("Installation annulée.")
            return # Termine

if __name__ == "__main__":
    main()
