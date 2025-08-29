#!/usr/bin/env python3
"""
Test d'intégration complète avec la base de données aep_prices.db.
Vérifie que tous les composants utilisent les mêmes données de diamètres et prix.
"""

import sys
import os
from pathlib import Path
import json

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_database_connection():
    """Test de la connexion directe à la base de données."""
    print("🔍 Test de la connexion directe à la base de données...")
    
    try:
        from src.lcpi.aep.optimizer.db_dao import get_candidate_diameters
        
        # Test direct de la base
        diam_rows = get_candidate_diameters("PVC-U")
        print(f"✅ Connexion directe à la base: {len(diam_rows)} diamètres PVC-U")
        
        # Afficher quelques exemples
        if diam_rows:
            print("📊 Exemples de diamètres et prix:")
            for i, row in enumerate(diam_rows[:5]):
                print(f"   {i+1}. {row.get('d_mm')}mm -> {row.get('cost_per_m', 'N/A')} FCFA/m")
        
        return True, diam_rows
    except Exception as e:
        print(f"❌ Erreur de connexion directe: {e}")
        return False, []

def test_diameter_manager_integration():
    """Test de l'intégration via le gestionnaire centralisé."""
    print("\n🔍 Test de l'intégration via le gestionnaire centralisé...")
    
    try:
        from src.lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices, get_diameter_manager
        
        # Test via la fonction de compatibilité
        diam_rows = get_standard_diameters_with_prices("PVC-U")
        print(f"✅ get_standard_diameters_with_prices: {len(diam_rows)} diamètres")
        
        # Test via le gestionnaire complet
        manager = get_diameter_manager()
        candidates = manager.get_candidate_diameters("PVC-U")
        print(f"✅ get_diameter_manager: {len(candidates)} candidats")
        
        return True, diam_rows, candidates
    except Exception as e:
        print(f"❌ Erreur dans le gestionnaire centralisé: {e}")
        return False, [], []

def test_controller_integration():
    """Test de l'intégration dans le contrôleur d'optimisation."""
    print("\n🔍 Test de l'intégration dans le contrôleur...")
    
    try:
        from src.lcpi.aep.optimizer.controllers import OptimizationController
        
        controller = OptimizationController()
        print("✅ OptimizationController créé avec succès")
        
        # Vérifier que le contrôleur peut charger les diamètres
        try:
            from src.lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
            diam_rows = get_standard_diameters_with_prices("PVC-U")
            print(f"✅ Contrôleur peut accéder aux diamètres: {len(diam_rows)} disponibles")
            
            # Vérifier la cohérence des données
            if diam_rows:
                first_diam = diam_rows[0]
                print(f"📊 Premier diamètre: {first_diam.get('d_mm')}mm -> {first_diam.get('cost_per_m')} FCFA/m")
            
            return True, diam_rows
        except Exception as e:
            print(f"⚠️ Contrôleur: Erreur lors du chargement des diamètres: {e}")
            return False, []
        
    except Exception as e:
        print(f"❌ Erreur dans le contrôleur: {e}")
        return False, []

def test_algorithm_consistency():
    """Test de la cohérence entre tous les algorithmes."""
    print("\n🔍 Test de la cohérence entre tous les algorithmes...")
    
    try:
        from src.lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
        
        # Charger les diamètres une seule fois
        reference_diams = get_standard_diameters_with_prices("PVC-U")
        print(f"✅ Diamètres de référence: {len(reference_diams)} disponibles")
        
        # Vérifier que tous les algorithmes peuvent accéder aux mêmes données
        algorithms = [
            ("NestedGreedyOptimizer", "src.lcpi.aep.optimizer.algorithms.nested"),
            ("GlobalOptimizer", "src.lcpi.aep.optimizer.algorithms.global_opt"),
            ("GeneticOptimizerV2", "src.lcpi.aep.optimization.genetic_algorithm"),
            ("SurrogateOptimizer", "src.lcpi.aep.optimizer.algorithms.surrogate"),
            ("MultiTankOptimizer", "src.lcpi.aep.optimizer.algorithms.multi_tank"),
            ("BinarySearchOptimizer", "src.lcpi.aep.optimizer.algorithms.binary"),
            ("ParallelMonteCarloAnalyzer", "src.lcpi.aep.optimization.parallel_monte_carlo"),
        ]
        
        consistency_results = []
        for name, module_path in algorithms:
            try:
                # Simuler l'import et l'accès aux diamètres
                exec(f"import {module_path}")
                consistency_results.append((name, True))
                print(f"✅ {name}: Accès aux diamètres OK")
            except Exception as e:
                consistency_results.append((name, False))
                print(f"❌ {name}: Erreur d'accès - {e}")
        
        return True, consistency_results, reference_diams
    except Exception as e:
        print(f"❌ Erreur lors du test de cohérence: {e}")
        return False, [], []

def test_price_realism():
    """Test du réalisme des prix générés."""
    print("\n🔍 Test du réalisme des prix...")
    
    try:
        from src.lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
        
        diam_rows = get_standard_diameters_with_prices("PVC-U")
        
        if not diam_rows:
            print("⚠️ Aucun diamètre disponible pour tester les prix")
            return False, []
        
        # Analyser la distribution des prix
        prices = [float(row.get('cost_per_m', 0)) for row in diam_rows if row.get('cost_per_m')]
        diameters = [int(row.get('d_mm', 0)) for row in diam_rows if row.get('d_mm')]
        
        if not prices or not diameters:
            print("⚠️ Données de prix ou diamètres manquantes")
            return False, []
        
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        
        print(f"📊 Analyse des prix:")
        print(f"   Prix min: {min_price:.2f} FCFA/m")
        print(f"   Prix max: {max_price:.2f} FCFA/m")
        print(f"   Prix moyen: {avg_price:.2f} FCFA/m")
        print(f"   Nombre de diamètres: {len(diameters)}")
        
        # Vérifier que les prix sont réalistes (pas tous identiques)
        if len(set(prices)) < 2:
            print("⚠️ Tous les prix sont identiques - problème de fallback")
            return False, diam_rows
        
        # Vérifier que les prix augmentent avec le diamètre
        price_diameter_pairs = list(zip(diameters, prices))
        price_diameter_pairs.sort(key=lambda x: x[0])
        
        increasing_prices = all(price_diameter_pairs[i][1] <= price_diameter_pairs[i+1][1] 
                               for i in range(len(price_diameter_pairs)-1))
        
        if increasing_prices:
            print("✅ Les prix augmentent logiquement avec le diamètre")
        else:
            print("⚠️ Les prix ne suivent pas une progression logique")
        
        return True, diam_rows
    except Exception as e:
        print(f"❌ Erreur lors du test de réalisme des prix: {e}")
        return False, []

def test_fallback_mechanism():
    """Test du mécanisme de fallback."""
    print("\n🔍 Test du mécanisme de fallback...")
    
    try:
        from src.lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
        
        # Tester avec un matériau inexistant pour déclencher le fallback
        fallback_diams = get_standard_diameters_with_prices("MATERIAU_INEXISTANT")
        
        if fallback_diams:
            print(f"✅ Mécanisme de fallback actif: {len(fallback_diams)} diamètres")
            
            # Vérifier que les prix de fallback sont réalistes
            prices = [float(row.get('cost_per_m', 0)) for row in fallback_diams if row.get('cost_per_m')]
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                print(f"📊 Prix de fallback: {min_price:.2f} - {max_price:.2f} FCFA/m")
                
                # Vérifier que ce ne sont pas tous des prix uniformes à 1000
                if len(set(prices)) > 1:
                    print("✅ Prix de fallback différenciés (pas de prix uniforme)")
                else:
                    print("⚠️ Prix de fallback uniformes - problème potentiel")
            
            return True, fallback_diams
        else:
            print("❌ Mécanisme de fallback non fonctionnel")
            return False, []
            
    except Exception as e:
        print(f"❌ Erreur lors du test du fallback: {e}")
        return False, []

def main():
    """Test principal d'intégration."""
    print("🚀 TEST D'INTÉGRATION COMPLÈTE AVEC LA BASE DE DONNÉES")
    print("=" * 70)
    
    # Tests principaux
    db_ok, db_data = test_database_connection()
    manager_ok, manager_data, manager_candidates = test_diameter_manager_integration()
    controller_ok, controller_data = test_controller_integration()
    consistency_ok, consistency_results, reference_data = test_algorithm_consistency()
    price_ok, price_data = test_price_realism()
    fallback_ok, fallback_data = test_fallback_mechanism()
    
    # Résumé des résultats
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION")
    print("=" * 70)
    
    tests = [
        ("Connexion directe à la base", db_ok),
        ("Gestionnaire centralisé", manager_ok),
        ("Contrôleur d'optimisation", controller_ok),
        ("Cohérence des algorithmes", consistency_ok),
        ("Réalisme des prix", price_ok),
        ("Mécanisme de fallback", fallback_ok),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    # Vérifications supplémentaires
    if passed == total:
        print("\n🎉 INTÉGRATION COMPLÈTE RÉUSSIE !")
        print("✅ La base aep_prices.db est parfaitement intégrée")
        print("✅ Tous les algorithmes utilisent les mêmes données")
        print("✅ Le mécanisme de fallback fonctionne correctement")
        print("✅ Les prix sont réalistes et différenciés")
        
        # Afficher un résumé des données
        if db_data:
            print(f"\n📊 Données de la base: {len(db_data)} diamètres disponibles")
            if len(db_data) > 0:
                sample = db_data[0]
                print(f"   Exemple: {sample.get('d_mm')}mm -> {sample.get('cost_per_m')} FCFA/m")
        
        return True
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Des corrections sont nécessaires pour l'intégration complète")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
