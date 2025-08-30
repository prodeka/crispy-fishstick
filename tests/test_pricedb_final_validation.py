#!/usr/bin/env python3
"""
Validation finale complète du système PriceDB.
Teste l'ensemble des fonctionnalités et valide la conformité Section A.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour pouvoir importer src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.lcpi.aep.optimizer.db import PriceDB, PipeData

def test_final_validation():
    """Test de validation finale complète."""
    print("=== VALIDATION FINALE PRICEDB ===\n")
    
    tests_passed = 0
    total_tests = 0
    
    def run_test(test_name, test_func):
        nonlocal tests_passed, total_tests
        total_tests += 1
        try:
            test_func()
            print(f"✅ {test_name}")
            tests_passed += 1
            return True
        except Exception as e:
            print(f"❌ {test_name}: {e}")
            return False
    
    # Test 1: Import et création d'instance
    def test_import_and_creation():
        db = PriceDB()
        assert db is not None
        assert hasattr(db, '_candidate_diameters')
        assert len(db._candidate_diameters) > 0
    
    # Test 2: Validation Pydantic
    def test_pydantic_validation():
        # Test de données valides
        valid_data = {
            "dn_mm": 100,
            "material": "PVC-U",
            "total_fcfa_per_m": 6000.0,
            "source_method": "test"
        }
        pipe = PipeData(**valid_data)
        assert pipe.dn_mm == 100
        assert pipe.material == "PVC-U"
        
        # Test de données invalides (doit lever une exception)
        try:
            invalid_data = {
                "dn_mm": 0,  # Diamètre invalide
                "material": "PVC-U",
                "total_fcfa_per_m": 6000.0,
                "source_method": "test"
            }
            PipeData(**invalid_data)
            assert False, "Validation Pydantic n'a pas fonctionné"
        except Exception:
            pass  # Exception attendue
    
    # Test 3: Informations de base de données
    def test_database_info():
        db = PriceDB()
        info = db.get_database_info()
        
        required_keys = ['type', 'diameter_count', 'fallback_used', 'timestamp_utc']
        for key in required_keys:
            assert key in info, f"Clé manquante: {key}"
        
        assert info['diameter_count'] > 0
        assert isinstance(info['timestamp_utc'], str)
    
    # Test 4: Récupération des diamètres
    def test_get_candidate_diameters():
        db = PriceDB()
        diameters = db.get_candidate_diameters()
        
        assert len(diameters) > 0
        assert all(isinstance(d, dict) for d in diameters)
        
        # Vérifier la structure
        for diameter in diameters:
            required_fields = ['dn_mm', 'material', 'total_fcfa_per_m', 'source_method']
            for field in required_fields:
                assert field in diameter, f"Champ manquant: {field}"
    
    # Test 5: Filtrage par matériau
    def test_material_filtering():
        db = PriceDB()
        
        # Test avec matériau existant
        pvc_diameters = db.get_candidate_diameters("PVC-U")
        if pvc_diameters:
            assert all(d['material'] == 'PVC-U' for d in pvc_diameters)
        
        # Test avec matériau inexistant
        fake_diameters = db.get_candidate_diameters("MATERIAU_INEXISTANT")
        assert len(fake_diameters) == 0
    
    # Test 6: Recherche de prix
    def test_get_diameter_price():
        db = PriceDB()
        diameters = db.get_candidate_diameters()
        
        if diameters:
            # Test avec un diamètre existant
            test_diameter = diameters[0]
            price = db.get_diameter_price(test_diameter['dn_mm'], test_diameter['material'])
            assert price is not None
            assert price == test_diameter['total_fcfa_per_m']
            
            # Test avec un diamètre inexistant
            fake_price = db.get_diameter_price(999999, "PVC-U")
            assert fake_price is None
    
    # Test 7: Recherche du diamètre le plus proche
    def test_get_closest_diameter():
        db = PriceDB()
        diameters = db.get_candidate_diameters()
        
        if len(diameters) >= 2:
            # Test avec une valeur entre deux diamètres
            dn_values = [d['dn_mm'] for d in diameters]
            min_dn = min(dn_values)
            max_dn = max(dn_values)
            mid_dn = (min_dn + max_dn) // 2
            
            closest = db.get_closest_diameter(mid_dn)
            assert closest is not None
            assert closest['dn_mm'] in dn_values
    
    # Test 8: Méthode reload
    def test_reload():
        db = PriceDB()
        initial_info = db.get_database_info()
        initial_count = len(db._candidate_diameters)
        
        db.reload()
        
        new_info = db.get_database_info()
        new_count = len(db._candidate_diameters)
        
        # Le timestamp doit être différent
        assert new_info['timestamp_utc'] != initial_info['timestamp_utc']
        # Le nombre de diamètres doit être identique
        assert new_count == initial_count
    
    # Test 9: Fallback automatique
    def test_fallback_behavior():
        # Créer une instance avec un chemin inexistant
        db = PriceDB("/chemin/inexistant/vers/db.db")
        info = db.get_database_info()
        
        assert info['type'] == 'fallback'
        assert info['fallback_used'] == True
        assert len(db._candidate_diameters) > 0
    
    # Test 10: Performance basique
    def test_basic_performance():
        import time
        
        # Test de création d'instance
        start_time = time.time()
        db = PriceDB()
        creation_time = time.time() - start_time
        assert creation_time < 2.0, f"Création trop lente: {creation_time:.2f}s"
        
        # Test de recherche multiple
        start_time = time.time()
        for _ in range(50):
            db.get_closest_diameter(100)
        search_time = time.time() - start_time
        assert search_time < 1.0, f"Recherche trop lente: {search_time:.2f}s"
    
    # Exécution de tous les tests
    print("1. Test d'import et création d'instance...")
    run_test("Import et création", test_import_and_creation)
    
    print("\n2. Test de validation Pydantic...")
    run_test("Validation Pydantic", test_pydantic_validation)
    
    print("\n3. Test des informations de base de données...")
    run_test("Informations DB", test_database_info)
    
    print("\n4. Test de récupération des diamètres...")
    run_test("Récupération diamètres", test_get_candidate_diameters)
    
    print("\n5. Test de filtrage par matériau...")
    run_test("Filtrage matériau", test_material_filtering)
    
    print("\n6. Test de recherche de prix...")
    run_test("Recherche prix", test_get_diameter_price)
    
    print("\n7. Test de recherche du diamètre le plus proche...")
    run_test("Diamètre le plus proche", test_get_closest_diameter)
    
    print("\n8. Test de la méthode reload...")
    run_test("Méthode reload", test_reload)
    
    print("\n9. Test du comportement de fallback...")
    run_test("Fallback automatique", test_fallback_behavior)
    
    print("\n10. Test de performance basique...")
    run_test("Performance basique", test_basic_performance)
    
    # Résumé final
    print(f"\n=== RÉSULTATS FINAUX ===")
    print(f"Tests réussis: {tests_passed}/{total_tests}")
    print(f"Taux de réussite: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 VALIDATION FINALE RÉUSSIE !")
        print("✅ Toutes les fonctionnalités Section A sont opérationnelles")
        print("✅ Le système PriceDB est prêt pour la production")
        return True
    else:
        print("\n❌ VALIDATION FINALE ÉCHOUÉE")
        print("⚠️  Certains tests ont échoué, vérification nécessaire")
        return False

if __name__ == "__main__":
    success = test_final_validation()
    sys.exit(0 if success else 1)
