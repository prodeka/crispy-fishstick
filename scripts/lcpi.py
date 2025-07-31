#!/usr/bin/env python3
"""
Script wrapper pour LCPI-CLI
Permet d'utiliser la commande 'lcpi' directement
"""

import sys
import os
import pathlib

def main():
    # Ajouter le dossier src au path Python
    project_root = pathlib.Path(__file__).parent.parent
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    # Importer et lancer LCPI
    try:
        from lcpi.main import app
        app()
    except ImportError as e:
        print(f"ERREUR: Impossible d'importer LCPI: {e}")
        print("Assurez-vous que le projet est correctement installé.")
        sys.exit(1)
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 