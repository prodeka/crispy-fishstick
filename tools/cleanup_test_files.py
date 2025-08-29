#!/usr/bin/env python3
"""
Script pour nettoyer les fichiers temporaires générés lors des tests.
"""

import os
from pathlib import Path
import glob

def cleanup_test_files():
    """Nettoie les fichiers temporaires de test."""
    
    print("🧹 Nettoyage des fichiers temporaires de test")
    print("=" * 50)
    
    # Patterns de fichiers à supprimer
    patterns = [
        "harmonized_*",
        "cmp_run_*",
        "bismark_test_*",
        "test_*",
        "*.json",
        "*.txt"
    ]
    
    # Exclure certains fichiers importants
    exclude_files = [
        "bismark_inp.inp",
        "check_candidates.py",
        "analyze_diameter_distribution.py",
        "test_harmonized_constraints.py"
    ]
    
    deleted_count = 0
    
    for pattern in patterns:
        files = glob.glob(pattern)
        for file_path in files:
            file_name = Path(file_path).name
            
            # Vérifier si le fichier doit être exclu
            if file_name in exclude_files:
                continue
                
            try:
                os.remove(file_path)
                print(f"🗑️  Supprimé: {file_name}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur lors de la suppression de {file_name}: {e}")
    
    print(f"\n✅ Nettoyage terminé: {deleted_count} fichiers supprimés")
    
    # Afficher les fichiers restants
    remaining_files = [f for f in os.listdir('.') if f.endswith(('.json', '.txt')) and f not in exclude_files]
    if remaining_files:
        print(f"\n📁 Fichiers restants: {len(remaining_files)}")
        for file_name in remaining_files[:10]:  # Afficher les 10 premiers
            print(f"   - {file_name}")
        if len(remaining_files) > 10:
            print(f"   ... et {len(remaining_files) - 10} autres")

if __name__ == "__main__":
    cleanup_test_files()
