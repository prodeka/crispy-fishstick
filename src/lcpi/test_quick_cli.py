#!/usr/bin/env python3
"""
Script de test rapide pour vérifier l'affichage des paramètres d'entrée des commandes CLI.
"""

import sys
import os
import subprocess
import time

def test_cli_command(module, command, expected_params=None):
    """Teste une commande CLI et vérifie l'affichage des paramètres."""
    print(f"\n🔍 Test: lcpi {module} {command}")
    
    try:
        # Utiliser UTF-8 pour l'encodage
        result = subprocess.run(
            [sys.executable, "-m", "lcpi", module, command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode == 0:
            if "Paramètres d'entrée" in result.stdout:
                print("✅ SUCCÈS: Affichage des paramètres correct")
                
                # Vérifier les paramètres attendus si fournis
                if expected_params:
                    for param in expected_params:
                        if param in result.stdout:
                            print(f"   ✅ Paramètre trouvé: {param}")
                        else:
                            print(f"   ⚠️  Paramètre manquant: {param}")
                
                return True
            else:
                print("❌ ÉCHEC: Pas d'affichage des paramètres")
                print(f"   Sortie: {result.stdout[:200]}...")
                return False
        else:
            print(f"❌ ERREUR: Code de retour {result.returncode}")
            if result.stderr:
                print(f"   Erreur: {result.stderr[:200]}...")
            if result.stdout:
                print(f"   Sortie: {result.stdout[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: Commande trop lente")
        return False
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def main():
    """Fonction principale."""
    print("🚀 TESTS RAPIDES DES COMMANDES CLI")
    print("=" * 50)
    
    # Liste des commandes à tester avec leurs paramètres attendus
    test_commands = [
        # Module CM
        ("cm", "check-poteau", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "check-deversement", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "check-tendu", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "check-compose", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "check-fleche", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "check-assemblage-boulon", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "check-assemblage-soude", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("cm", "optimize-section", ["--check", "(-c)", "--filepath", "(-f)"]),
        
        # Module BOIS
        ("bois", "check-poteau", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check-deversement", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check-cisaillement", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check-compression-perp", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check-compose", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check", ["--filepath", "(-f)", "--batch-file", "(-b)", "--output-file"]),
        ("bois", "check-fleche", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check-assemblage-pointe", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        ("bois", "check-assemblage-embrevement", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        
        # Module BETON
        ("beton", "calc-poteau", ["--filepath", "(-f)", "--batch-file", "(-b)", "--output-file"]),
        ("beton", "calc-radier", ["--filepath", "(-f)", "Chemin vers le fichier YAML"]),
        
        # Module HYDRODRAIN
        ("hydro", "plomberie", "dimensionner", ["--nb-appareils", "(-n)", "--debits-base", "(-d)", "--v-max"]),
        ("hydro", "reservoir", "equilibrage", ["--demande-journaliere", "(-d)", "--cp-jour", "--cp-horaire", "--jours-stockage"]),
        ("hydro", "reservoir", "incendie", ["--population", "(-p)", "--type-zone", "(-t)"]),
        ("hydro", "reservoir", "complet", ["--population", "(-p)", "--dotation", "(-d)", "--cp-jour", "--cp-horaire", "--jours-securite", "--type-zone", "(-t)"]),
        ("hydro", "reservoir", "verifier-pression", ["--cote-reservoir", "(-c)", "--cote-terrain", "(-t)", "--pertes-charge", "(-p)", "--pression-min"]),
        ("hydro", "util", "prevoir-population", ["--method", "(-m)", "--annee", "(-a)"]),
        ("hydro", "util", "estimer-demande-eau", ["--pop", "(-p)", "--dota", "(-d)"]),
        ("hydro", "util", "diagramme-ombro", ["--filepath", "(-f)", "--output", "(-o)"]),
    ]
    
    success_count = 0
    total_count = len(test_commands)
    
    for test_tuple in test_commands:
        module, command, expected_params = test_tuple
        if test_cli_command(module, command, expected_params):
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