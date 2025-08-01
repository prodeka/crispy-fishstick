#!/usr/bin/env python3
"""
Script principal pour exécuter tous les tests automatisés de LCPI-CLI.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def run_test_file(test_file):
    """Exécute un fichier de test et retourne les résultats."""
    print(f"\n{'='*60}")
    print(f"🧪 EXÉCUTION DES TESTS: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.path.dirname(__file__)
        )
        
        print("📤 Sortie standard:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Erreurs:")
            print(result.stderr)
        
        print(f"📊 Code de retour: {result.returncode}")
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: Le test a pris trop de temps")
        return False
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

def run_quick_cli_tests():
    """Exécute des tests rapides des commandes CLI."""
    print(f"\n{'='*60}")
    print("🚀 TESTS RAPIDES DES COMMANDES CLI")
    print(f"{'='*60}")
    
    # Liste des commandes à tester rapidement
    test_commands = [
        ["cm", "check-poteau"],
        ["bois", "check-poteau"],
        ["beton", "calc-poteau"],
        ["hydro", "plomberie", "dimensionner"],
        ["hydro", "reservoir", "equilibrage"],
        ["hydro", "reservoir", "incendie"],
    ]
    
    success_count = 0
    total_count = len(test_commands)
    
    for cmd in test_commands:
        print(f"\n🔍 Test de: lcpi {' '.join(cmd)}")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "lcpi"] + cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.dirname(__file__)
            )
            
            if result.returncode == 0 and "Paramètres d'entrée" in result.stdout:
                print("✅ SUCCÈS: Affichage des paramètres correct")
                success_count += 1
            else:
                print("❌ ÉCHEC: Pas d'affichage des paramètres ou erreur")
                print(f"   Sortie: {result.stdout[:200]}...")
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
    
    print(f"\n📈 Résultats: {success_count}/{total_count} tests réussis")
    return success_count == total_count

def main():
    """Fonction principale."""
    print("🎯 TESTS AUTOMATISÉS LCPI-CLI")
    print("=" * 60)
    print(f"📁 Répertoire de travail: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")
    print(f"⏰ Début: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("src/lcpi"):
        print("❌ ERREUR: Répertoire src/lcpi non trouvé. Assurez-vous d'être dans le répertoire racine du projet.")
        return 1
    
    # Tests des utilitaires
    test_files = [
        "tests/test_command_helpers.py",
        "tests/test_cli_commands.py"
    ]
    
    all_tests_passed = True
    
    # Exécuter les tests unitaires
    for test_file in test_files:
        if os.path.exists(test_file):
            if not run_test_file(test_file):
                all_tests_passed = False
        else:
            print(f"⚠️  Fichier de test non trouvé: {test_file}")
    
    # Tests rapides CLI
    if not run_quick_cli_tests():
        all_tests_passed = False
    
    # Résumé final
    print(f"\n{'='*60}")
    print("📋 RÉSUMÉ FINAL")
    print(f"{'='*60}")
    
    if all_tests_passed:
        print("🎉 TOUS LES TESTS ONT RÉUSSI !")
        print("✅ L'affichage automatique des paramètres d'entrée fonctionne correctement")
        print("✅ Toutes les commandes CLI sont opérationnelles")
        return 0
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus et corrigez les problèmes")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 