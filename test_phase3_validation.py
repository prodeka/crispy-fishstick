#!/usr/bin/env python3
"""
Script de validation de la Phase 3 : Réparation Douce (Soft Repair)
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_repairs_module():
    """Test du module de réparation"""
    print("🧪 Test du module de réparation...")
    
    try:
        from lcpi.aep.optimization.repairs import soft_repair_solution
        print("✅ Import du module repairs réussi")
        
        # Test simple
        diameters_map = {"P1": 110, "P2": 90, "P3": 110}
        sim_metrics = {"headlosses_m": {"P1": 5.2, "P2": 15.8, "P3": 10.1}}
        candidate_diameters = [75, 90, 110, 125, 160]
        
        repaired_map, changes = soft_repair_solution(
            diameters_map, sim_metrics, candidate_diameters, max_changes_fraction=0.20
        )
        
        print(f"✅ Test de réparation réussi:")
        print(f"   - Changements effectués: {changes['total_changes']}")
        print(f"   - Conduite réparée: {changes['repaired_pipes'][0]['pipe_id'] if changes['repaired_pipes'] else 'Aucune'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du module repairs: {e}")
        return False

def test_genetic_algorithm_integration():
    """Test de l'intégration dans l'algorithme génétique"""
    print("\n🧪 Test de l'intégration dans l'AG...")
    
    try:
        from lcpi.aep.optimization.genetic_algorithm import GeneticOptimizerV2
        print("✅ Import de GeneticOptimizerV2 réussi")
        
        # Vérifier que la méthode _apply_soft_repair existe
        if hasattr(GeneticOptimizerV2, '_apply_soft_repair'):
            print("✅ Méthode _apply_soft_repair trouvée")
        else:
            print("❌ Méthode _apply_soft_repair manquante")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        return False

def test_unit_tests():
    """Test des tests unitaires"""
    print("\n🧪 Test des tests unitaires...")
    
    try:
        import pytest
        from pathlib import Path
        
        test_file = Path(__file__).parent / "tests" / "optimizer" / "test_repairs.py"
        
        if test_file.exists():
            print("✅ Fichier de test trouvé")
            
            # Exécuter les tests
            result = pytest.main([str(test_file), "-v"])
            
            if result == 0:
                print("✅ Tous les tests unitaires passent")
                return True
            else:
                print("❌ Certains tests unitaires ont échoué")
                return False
        else:
            print("❌ Fichier de test manquant")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🚀 Validation de la Phase 3 : Réparation Douce (Soft Repair)")
    print("=" * 60)
    
    tests = [
        ("Module de réparation", test_repairs_module),
        ("Intégration AG", test_genetic_algorithm_integration),
        ("Tests unitaires", test_unit_tests)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Phase 3 validée avec succès !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
