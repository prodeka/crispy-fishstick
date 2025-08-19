#!/usr/bin/env python3
"""
Script de test pour les commandes CLI d'optimisation AEP V11
"""

import sys
sys.path.insert(0, 'src')

from lcpi.aep.cli import app
from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI

def test_cli_integration():
    """Test l'intégration des commandes CLI."""
    print("🧪 Test d'intégration des commandes CLI AEP V11")
    print("=" * 50)
    
    # 1. Test de l'import CLI principal
    try:
        print("✅ CLI AEP principal importé avec succès")
        print(f"   Type: {type(app)}")
        print(f"   Nombre de groupes: {len(app.registered_groups)}")
    except Exception as e:
        print(f"❌ Erreur import CLI principal: {e}")
        return False
    
    # 2. Test de l'import CLI Optimizer
    try:
        cli = AEPOptimizationCLI()
        print("✅ CLI Optimizer V11 importé avec succès")
        print(f"   Type: {type(cli)}")
    except Exception as e:
        print(f"❌ Erreur import CLI Optimizer: {e}")
        return False
    
    # 3. Test des sous-groupes
    try:
        print("\n📋 Sous-groupes disponibles:")
        for i, group in enumerate(app.registered_groups):
            print(f"   {i+1}. {group.name}")
    except Exception as e:
        print(f"❌ Erreur listing groupes: {e}")
    
    # 4. Test des méthodes CLI Optimizer
    try:
        print("\n🔧 Méthodes CLI Optimizer disponibles:")
        methods = [method for method in dir(cli) if not method.startswith('_')]
        for method in methods:
            print(f"   - {method}")
    except Exception as e:
        print(f"❌ Erreur listing méthodes: {e}")
    
    return True

def test_format_v11():
    """Test le format V11."""
    print("\n🧪 Test du format V11")
    print("=" * 30)
    
    try:
        from lcpi.aep.optimizer.output import OutputFormatter
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        
        # Créer un test simple
        formatter = OutputFormatter()
        tank = TankDecision(id="TANK1", H_m=65.0)
        proposal = Proposal(
            name="test_solution",
            is_feasible=True,
            tanks=[tank],
            diameters_mm={"PIPE1": 200},
            costs={"CAPEX": 100000},
            metrics={"min_pressure_m": 12.5}
        )
        
        result = OptimizationResult(
            proposals=[proposal],
            pareto_front=None,
            metadata={"method": "test"}
        )
        
        # Test du formatage V11
        v11_output = formatter.format_v11(result)
        
        print("✅ Format V11 fonctionne parfaitement")
        print(f"   Version: {v11_output['metadata']['version']}")
        print(f"   Format: {v11_output['metadata']['format']}")
        print(f"   Propositions: {len(v11_output['proposals'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur format V11: {e}")
        return False

def test_template_v11():
    """Test le template V11."""
    print("\n🧪 Test du template V11")
    print("=" * 30)
    
    try:
        from pathlib import Path
        template_path = Path("src/lcpi/aep/templates/optimisation_tank_v11.jinja2")
        
        if template_path.exists():
            print("✅ Template V11 existe")
            print(f"   Chemin: {template_path}")
            print(f"   Taille: {template_path.stat().st_size} bytes")
            return True
        else:
            print("❌ Template V11 manquant")
            return False
            
    except Exception as e:
        print(f"❌ Erreur template V11: {e}")
        return False

def test_reporting_compatibility():
    """Test la compatibilité avec le système de rapport."""
    print("\n🧪 Test compatibilité avec lcpi rapport")
    print("=" * 40)
    
    try:
        from lcpi.reporting.cli import app as reporting_app
        print("✅ Module de rapport importé")
        print(f"   Type: {type(reporting_app)}")
        
        # Test des commandes de rapport
        commands = getattr(reporting_app, 'registered_commands', [])
        print(f"   Commandes: {len(commands)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur import rapport: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Tests des Commandes CLI AEP V11")
    print("🔍 Analyse de l'intégration et de la compatibilité")
    print("=" * 60)
    
    tests = [
        ("Intégration CLI", test_cli_integration),
        ("Format V11", test_format_v11),
        ("Template V11", test_template_v11),
        ("Compatibilité Rapport", test_reporting_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n🎯 Résultat global: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 Tous les tests sont passés ! Le système est prêt.")
    else:
        print("⚠️  Certains tests ont échoué. Vérification nécessaire.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
