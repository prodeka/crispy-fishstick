#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage des fichiers de démonstration temporaires
"""

import os
import shutil
from pathlib import Path

def cleanup_demo_files():
    """Nettoie les fichiers de démonstration temporaires"""
    print("🧹 Nettoyage des fichiers de démonstration temporaires...")
    
    # Fichiers et dossiers à supprimer
    demo_items = [
        "demo_db_fonctionnalites.py",
        "demo_recherche_globale.py",
        "check_tables.py",
        "test_sql_queries.py",
        "export_bois_demo.csv"
    ]
    
    for item in demo_items:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"✅ Dossier supprimé: {item}")
            else:
                path.unlink()
                print(f"✅ Fichier supprimé: {item}")
        else:
            print(f"ℹ️  Non trouvé: {item}")
    
    print("\n🎉 Nettoyage terminé!")
    print("Les fichiers de démonstration temporaires ont été supprimés.")
    print("Les modules principaux sont conservés:")
    print("  - src/lcpi/db_manager.py")
    print("  - src/lcpi/db_global_search.py")
    print("  - src/lcpi/cli_db.py")
    print("  - src/lcpi/cli_global_search.py")
    print("  - repl_db_test.py")

if __name__ == "__main__":
    cleanup_demo_files() 