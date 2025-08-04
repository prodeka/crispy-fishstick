#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage des fichiers de test temporaires
"""

import os
import shutil
from pathlib import Path

def cleanup_test_files():
    """Nettoie les fichiers de test temporaires"""
    print("🧹 Nettoyage des fichiers de test temporaires...")
    
    # Fichiers et dossiers à supprimer
    test_items = [
        "test_yaml_files",
        "test_csv_files",
        "test_encoding.yml",
        "test_encoding.csv",
        "test_climat.png"
    ]
    
    for item in test_items:
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
    print("Les fichiers de test temporaires ont été supprimés.")
    print("Les scripts de test (test_all_calculs_functions.py, test_complet_projet.py, repl_test.py) sont conservés.")

if __name__ == "__main__":
    cleanup_test_files() 