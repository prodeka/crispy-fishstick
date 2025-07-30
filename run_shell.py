# run_shell.py
"""
Script de contournement pour lancer le shell interactif de LCPI-CLI.

Ce script est nécessaire car l'exécution via l'entry-point `lcpi shell`
peut rencontrer des problèmes avec la gestion de l'entrée standard (stdin)
sur certaines plateformes comme Windows, empêchant la boucle interactive
de fonctionner correctement.

En appelant directement la fonction `shell()` avec `python run_shell.py`,
on s'assure que le processus est attaché à une console interactive valide.
"""

import sys
import os

# Ajoute le dossier 'src' au path pour permettre l'import de 'lcpi.main'
# comme si on était dans le contexte du projet.
# Chemin du script -> G:/.../PROJET_DIMENTIONEMENT_2/run_shell.py
# Chemin du dossier src -> G:/.../PROJET_DIMENTIONEMENT_2/src
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    # Importe la fonction shell depuis le module principal
    from lcpi.main import shell
except ImportError as e:
    print(f"Erreur d'importation : {e}")
    print("Assurez-vous que la structure du projet est correcte et que vous lancez ce script depuis la racine.")
    sys.exit(1)

if __name__ == "__main__":
    # Exécute la fonction du shell interactif
    print("--- Lancement du shell interactif en mode direct ---")
    shell()
