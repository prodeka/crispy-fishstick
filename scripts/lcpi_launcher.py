#!/usr/bin/env python3
"""
Script de lancement LCPI-CLI qui fonctionne depuis n'importe où
"""

import sys
import os

def main():
    """Point d'entrée principal pour LCPI-CLI"""
    try:
        # Ajouter le répertoire du projet au path
        project_root = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(project_root, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Importer et lancer l'application
        from lcpi.main import app
        app()
    except Exception as e:
        print(f"❌ Erreur lors du lancement de LCPI-CLI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
