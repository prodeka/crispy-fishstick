#!/usr/bin/env python3
"""
Script de test simple pour vérifier l'affichage des paramètres d'entrée des commandes CLI.
"""

import sys
import os
import subprocess

def test_command(module, command):
    """Teste une commande CLI."""
    print(f"\n🔍 Test: lcpi {module} {command}")
    
    try:
        # Utiliser UTF-8 et ignorer les erreurs d'encodage
        result = subprocess.run(
            [sys.executable, "-m", "lcpi", module, command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode == 0:
            if "Paramètres d'entrée" in result.stdout:
                print("✅ SUCCÈS: Affichage des paramètres correct")
                return True
            else:
                print("❌ ÉCHEC: Pas d'affichage des paramètres")
                return False
        else:
            print(f"❌ ERREUR: Code de retour {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def main():
    """Fonction principale."""
    print("🚀 TESTS SIMPLES DES COMMANDES CLI")
    print("=" * 50)
    
    # Liste des commandes à tester
    commands = [
        ("cm", "check-poteau"),
        ("cm", "check-deversement"),
        ("cm", "check-tendu"),
        ("cm", "check-compose"),
        ("cm", "check-fleche"),
        ("cm", "check-assemblage-boulon"),
        ("cm", "check-assemblage-soude"),
        ("cm", "optimize-section"),
        
        ("bois", "check-poteau"),
        ("bois", "check-deversement"),
        ("bois", "check-cisaillement"),
        ("bois", "check-compression-perp"),
        ("bois", "check-compose"),
        ("bois", "check"),
        ("bois", "check-fleche"),
        ("bois", "check-assemblage-pointe"),
        ("bois", "check-assemblage-embrevement"),
        
        ("beton", "calc-poteau"),
        ("beton", "calc-radier"),
        
        ("hydro", "plomberie", "dimensionner"),
        ("hydro", "reservoir", "equilibrage"),
        ("hydro", "reservoir", "incendie"),
        ("hydro", "reservoir", "complet"),
        ("hydro", "reservoir", "verifier-pression"),
        ("hydro", "util", "prevoir-population"),
        ("hydro", "util", "estimer-demande-eau"),
        ("hydro", "util", "diagramme-ombro"),
    ]
    
    success_count = 0
    total_count = len(commands)
    
    for cmd in commands:
        if len(cmd) == 2:
            module, command = cmd
            if test_command(module, command):
                success_count += 1
        elif len(cmd) == 3:
            module, submodule, command = cmd
            if test_command(f"{module} {submodule}", command):
                success_count += 1
    
    # Résumé final
    print(f"\n{'='*50}")
    print("📋 RÉSUMÉ FINAL")
    print(f"{'='*50}")
    print(f"✅ Tests réussis: {success_count}/{total_count}")
    print(f"📊 Taux de réussite: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 TOUS LES TESTS ONT RÉUSSI !")
        print("✅ L'affichage automatique des paramètres d'entrée fonctionne parfaitement")
        return 0
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 