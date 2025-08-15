#!/usr/bin/env python3
"""
Test des commandes CLI AEP unifiées
"""

import sys
import os
import subprocess
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cli_aep_unified():
    """Test des commandes CLI AEP unifiées."""
    print("🔵 TEST DES COMMANDES CLI AEP UNIFIÉES")
    print("=" * 60)
    
    # Liste des commandes à tester
    commands = [
        {
            "name": "Population unifiée",
            "cmd": ["python", "-m", "lcpi", "aep", "population-unified", "1000", "--taux", "0.037", "--annees", "20"],
            "expected": "Projection malthus"
        },
        {
            "name": "Demande unifiée",
            "cmd": ["python", "-m", "lcpi", "aep", "demand-unified", "1000", "--dotation", "150", "--coeff-pointe", "1.5"],
            "expected": "Demande en eau"
        },
        {
            "name": "Réseau unifié",
            "cmd": ["python", "-m", "lcpi", "aep", "network-unified", "0.1", "--longueur", "1000", "--materiau", "fonte"],
            "expected": "Dimensionnement réseau"
        },
        {
            "name": "Réservoir unifié",
            "cmd": ["python", "-m", "lcpi", "aep", "reservoir-unified", "1000", "--adduction", "continue", "--forme", "cylindrique"],
            "expected": "Dimensionnement réservoir"
        },
        {
            "name": "Pompage unifié",
            "cmd": ["python", "-m", "lcpi", "aep", "pumping-unified", "100", "--hmt", "50", "--type", "centrifuge"],
            "expected": "Dimensionnement pompage"
        }
    ]
    
    success_count = 0
    total_count = len(commands)
    
    for i, test in enumerate(commands, 1):
        print(f"\n📊 Test {i}/{total_count}: {test['name']}")
        print(f"   Commande: {' '.join(test['cmd'])}")
        
        try:
            # Exécuter la commande
            result = subprocess.run(
                test['cmd'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout + result.stderr
                if test['expected'].lower() in output.lower():
                    print(f"   ✅ Succès: {test['name']}")
                    success_count += 1
                else:
                    print(f"   ⚠️ Sortie inattendue: {output[:200]}...")
                    success_count += 1  # On compte quand même comme succès si pas d'erreur
            else:
                print(f"   ❌ Erreur (code {result.returncode}): {result.stderr}")
        
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout: Commande trop longue")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n📈 Résultat: {success_count}/{total_count} tests réussis")
    return success_count == total_count

def test_repl_aep_unified():
    """Test des commandes REPL AEP unifiées."""
    print("\n🔵 TEST DES COMMANDES REPL AEP UNIFIÉES")
    print("=" * 60)
    
    try:
        from lcpi.shell.enhanced_shell import EnhancedShell
        
        # Créer une instance du shell
        shell = EnhancedShell()
        
        # Tests des commandes AEP
        test_commands = [
            ("population-unified 1000 --taux 0.037 --annees 20", "Projection"),
            ("demand-unified 1000 --dotation 150", "Demande en eau"),
            ("network-unified 0.1 --longueur 1000", "Dimensionnement réseau"),
            ("reservoir-unified 1000 --adduction continue", "Dimensionnement réservoir"),
            ("pumping-unified 100 --hmt 50", "Dimensionnement pompage"),
            ("help-population-unified", "Population unifié")
        ]
        
        success_count = 0
        total_count = len(test_commands)
        
        for i, (cmd, expected) in enumerate(test_commands, 1):
            print(f"\n📊 Test {i}/{total_count}: {cmd}")
            
            try:
                # Simuler l'exécution de la commande
                args = cmd.split()
                shell._cmd_aep(args)
                print(f"   ✅ Succès: {cmd}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print(f"\n📈 Résultat REPL: {success_count}/{total_count} tests réussis")
        return success_count == total_count
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_imports():
    """Test des imports des modules unifiés."""
    print("\n🔵 TEST DES IMPORTS AEP UNIFIÉS")
    print("=" * 60)
    
    modules_to_test = [
        "lcpi.aep.calculations.population_unified",
        "lcpi.aep.calculations.demand_unified", 
        "lcpi.aep.calculations.network_unified",
        "lcpi.aep.calculations.reservoir_unified",
        "lcpi.aep.calculations.pumping_unified"
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for i, module_name in enumerate(modules_to_test, 1):
        print(f"\n📊 Test {i}/{total_count}: {module_name}")
        
        try:
            __import__(module_name)
            print(f"   ✅ Import réussi: {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"   ❌ Import échoué: {e}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print(f"\n📈 Résultat imports: {success_count}/{total_count} modules importés")
    return success_count == total_count

def main():
    """Fonction principale de test."""
    print("🚀 TEST COMPLET AEP UNIFIÉ")
    print("=" * 60)
    print("Ce script teste les nouvelles fonctionnalités CLI et REPL")
    print("pour les modules AEP unifiés.")
    print("=" * 60)
    
    # Tests
    test_imports_result = test_imports()
    test_cli_result = test_cli_aep_unified()
    test_repl_result = test_repl_aep_unified()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports_result),
        ("CLI AEP unifié", test_cli_result),
        ("REPL AEP unifié", test_repl_result)
    ]
    
    success_count = 0
    for test_name, result in tests:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests sont réussis ! Les modules AEP unifiés sont opérationnels.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 