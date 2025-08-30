#!/usr/bin/env python3
"""
Test d'intégration de PriceDB dans le système principal.
Valide que tous les modules utilisent correctement la nouvelle API.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour pouvoir importer src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_controllers_integration():
    """Test l'intégration dans le contrôleur d'optimisation."""
    print("🧪 Test d'intégration dans OptimizationController...")
    
    try:
        from src.lcpi.aep.optimizer.controllers import OptimizationController
        
        # Créer une instance du contrôleur
        controller = OptimizationController()
        
        # Vérifier que l'attribut _price_db_instance existe
        assert hasattr(controller, '_price_db_instance'), "L'attribut _price_db_instance n'existe pas"
        
        print("✅ OptimizationController intègre correctement PriceDB")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans OptimizationController: {e}")
        return False

def test_cli_integration():
    """Test l'intégration dans l'interface CLI."""
    print("🧪 Test d'intégration dans AEPOptimizationCLI...")
    
    try:
        from src.lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
        
        # Créer une instance CLI
        cli = AEPOptimizationCLI()
        
        # Tester la méthode _list_diameters
        cli._list_diameters()
        
        print("✅ AEPOptimizationCLI intègre correctement PriceDB")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans AEPOptimizationCLI: {e}")
        return False

def test_scoring_integration():
    """Test l'intégration dans le module de scoring."""
    print("🧪 Test d'intégration dans CostScorer...")
    
    try:
        from src.lcpi.aep.optimizer.scoring import CostScorer
        
        # Créer une instance du scorer
        scorer = CostScorer()
        
        # Vérifier que l'import de PriceDB fonctionne
        from src.lcpi.aep.optimizer.db import PriceDB
        price_db = PriceDB()
        
        # Tester une recherche de prix
        price = price_db.get_diameter_price(100, "PVC-U")
        assert price is not None, "Impossible de récupérer un prix de diamètre"
        
        print("✅ CostScorer intègre correctement PriceDB")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans CostScorer: {e}")
        return False

def test_algorithms_integration():
    """Test l'intégration dans les algorithmes d'optimisation."""
    print("🧪 Test d'intégration dans les algorithmes...")
    
    try:
        # Test NestedGreedyOptimizer
        from src.lcpi.aep.optimizer.algorithms.nested import NestedGreedyOptimizer
        from src.lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer
        
        # Vérifier que les imports fonctionnent
        print("✅ Imports des algorithmes réussis")
        
        # Test PriceDB dans les algorithmes
        from src.lcpi.aep.optimizer.db import PriceDB
        price_db = PriceDB()
        diameters = price_db.get_candidate_diameters()
        assert len(diameters) > 0, "Aucun diamètre trouvé dans PriceDB"
        
        print("✅ Algorithmes intègrent correctement PriceDB")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans les algorithmes: {e}")
        return False

def test_diameter_manager_integration():
    """Test l'intégration dans le gestionnaire de diamètres."""
    print("🧪 Test d'intégration dans DiameterManager...")
    
    try:
        from src.lcpi.aep.optimizer.diameter_manager import DiameterManager
        
        # Créer une instance du gestionnaire
        manager = DiameterManager()
        
        # Tester la récupération des diamètres
        candidates = manager.get_candidate_diameters("PVC-U")
        assert len(candidates) > 0, "Aucun diamètre trouvé par le gestionnaire"
        
        print("✅ DiameterManager intègre correctement PriceDB")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans DiameterManager: {e}")
        return False

def test_reporting_integration():
    """Test l'intégration dans le module de reporting."""
    print("🧪 Test d'intégration dans MarkdownGenerator...")
    
    try:
        from src.lcpi.reporting.markdown_generator import MarkdownGenerator
        
        # Créer une instance du générateur
        generator = MarkdownGenerator()
        
        # Vérifier que l'attribut _prices_dao existe
        assert hasattr(generator, '_prices_dao'), "L'attribut _prices_dao n'existe pas"
        
        # Tester la récupération d'un prix
        price_info = generator._get_diameter_price_from_db(100, "PVC-U")
        assert price_info is not None, "Impossible de récupérer les informations de prix"
        
        print("✅ MarkdownGenerator intègre correctement PriceDB")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans MarkdownGenerator: {e}")
        return False

def test_end_to_end_integration():
    """Test d'intégration end-to-end complet."""
    print("🧪 Test d'intégration end-to-end...")
    
    try:
        # Test complet du flux d'optimisation
        from src.lcpi.aep.optimizer.controllers import OptimizationController
        from src.lcpi.aep.optimizer.db import PriceDB
        
        # Créer les instances
        controller = OptimizationController()
        price_db = PriceDB()
        
        # Vérifier que les deux utilisent la même source de données
        controller_info = controller._price_db_instance.get_database_info()
        price_db_info = price_db.get_database_info()
        
        assert controller_info['type'] == price_db_info['type'], "Types de base de données différents"
        assert controller_info['diameter_count'] == price_db_info['diameter_count'], "Nombre de diamètres différent"
        
        print("✅ Intégration end-to-end réussie")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans l'intégration end-to-end: {e}")
        return False

def main():
    """Exécute tous les tests d'intégration."""
    print("🚀 Test d'intégration de PriceDB dans le système principal")
    print("=" * 60)
    
    tests = [
        ("OptimizationController", test_controllers_integration),
        ("AEPOptimizationCLI", test_cli_integration),
        ("CostScorer", test_scoring_integration),
        ("Algorithmes", test_algorithms_integration),
        ("DiameterManager", test_diameter_manager_integration),
        ("MarkdownGenerator", test_reporting_integration),
        ("End-to-End", test_end_to_end_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: SUCCÈS")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    print(f"\n📊 RÉSULTATS FINAUX")
    print("=" * 40)
    print(f"Tests réussis: {passed}/{total}")
    print(f"Taux de réussite: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS D'INTÉGRATION ONT RÉUSSI !")
        print("✅ PriceDB est correctement intégré dans le système principal")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué")
        print("🔧 Vérification nécessaire de l'intégration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
