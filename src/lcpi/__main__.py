#!/usr/bin/env python3
"""
Point d'entrée principal pour l'exécution du module lcpi
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports relatifs
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    try:
        from lcpi.main import app
        import typer
        
        # Exécuter l'application CLI directement
        # Définir le nom de l'application pour l'affichage
        import sys
        sys.argv[0] = "lcpi"
        app()
    except Exception as e:
        print(f"❌ Erreur lors du lancement de LCPI-CLI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
