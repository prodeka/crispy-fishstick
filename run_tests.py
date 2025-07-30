#!/usr/bin/env python3
"""
Script pour exécuter les tests unitaires du plugin hydro.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Exécute une commande et affiche le résultat."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Commande: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"\n✅ {description} - SUCCÈS")
        else:
            print(f"\n❌ {description} - ÉCHEC (code: {result.returncode})")
        return result.returncode == 0
    except Exception as e:
        print(f"\n❌ {description} - ERREUR: {e}")
        return False

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Exécuter les tests unitaires du plugin hydro")
    parser.add_argument("--module", choices=["collector", "reservoir", "hydraulique", "all"], 
                       default="all", help="Module à tester")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard", "all"], 
                       default="all", help="Difficulté des tests")
    parser.add_argument("--coverage", action="store_true", 
                       help="Générer un rapport de couverture")
    parser.add_argument("--html", action="store_true", 
                       help="Générer un rapport HTML de couverture")
    parser.add_argument("--fast", action="store_true", 
                       help="Exécuter seulement les tests rapides")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Mode verbeux")
    
    args = parser.parse_args()
    
    # Vérifier que pytest est installé
    try:
        subprocess.run(["pytest", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest n'est pas installé. Installez-le avec: pip install pytest pytest-cov")
        return 1
    
    # Construire la commande pytest
    cmd = ["pytest"]
    
    # Ajouter les options de base
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Sélectionner le module
    if args.module != "all":
        cmd.extend(["-m", args.module])
    
    # Sélectionner la difficulté
    if args.difficulty != "all":
        cmd.extend(["-m", args.difficulty])
    
    # Exclure les tests lents si demandé
    if args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Ajouter la couverture si demandée
    if args.coverage:
        cmd.extend([
            "--cov=src/lcpi/hydrodrain",
            "--cov-report=term-missing"
        ])
    
    if args.html:
        cmd.extend([
            "--cov=src/lcpi/hydrodrain",
            "--cov-report=html:htmlcov"
        ])
    
    # Ajouter les fichiers de test spécifiques
    test_files = []
    if args.module == "collector" or args.module == "all":
        test_files.append("tests/test_collector_assainissement.py")
    if args.module == "reservoir" or args.module == "all":
        test_files.append("tests/test_reservoir_aep.py")
    if args.module == "hydraulique" or args.module == "all":
        test_files.append("tests/test_hydraulique.py")
    
    if test_files:
        cmd.extend(test_files)
    
    # Exécuter les tests
    success = run_command(cmd, f"Tests unitaires - Module: {args.module}, Difficulté: {args.difficulty}")
    
    # Afficher un résumé
    print(f"\n{'='*60}")
    if success:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
    print(f"{'='*60}")
    
    # Afficher les informations sur les tests
    print("\n📊 INFORMATIONS SUR LES TESTS:")
    print(f"   - Module testé: {args.module}")
    print(f"   - Difficulté: {args.difficulty}")
    print(f"   - Couverture: {'Oui' if args.coverage or args.html else 'Non'}")
    print(f"   - Mode rapide: {'Oui' if args.fast else 'Non'}")
    
    # Afficher les commandes utiles
    print("\n🔧 COMMANDES UTILES:")
    print("   - Tests rapides: python run_tests.py --fast")
    print("   - Tests avec couverture: python run_tests.py --coverage")
    print("   - Tests verbeux: python run_tests.py --verbose")
    print("   - Tests d'un module: python run_tests.py --module collector")
    print("   - Tests faciles: python run_tests.py --difficulty easy")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 