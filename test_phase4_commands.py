#!/usr/bin/env python3
"""
Test des commandes CLI de la Phase 4 - Améliorations de Performance et Parallélisation.

Ce script teste :
- Gestion du cache intelligent
- Monitoring des performances
- Analyse Monte Carlo parallélisée
- Commandes de performance
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_cache_manager():
    """Test du gestionnaire de cache intelligent."""
    print("🧪 Test du gestionnaire de cache intelligent...")
    
    try:
        from lcpi.aep.core.cache_manager import get_cache_manager, clear_cache, get_cache_stats
        
        # Créer une instance du cache
        cache_manager = get_cache_manager(max_size_mb=50, max_entries=100)
        print("  ✅ Cache manager créé avec succès")
        
        # Test des opérations de base
        cache_manager.set("test_key", {"data": "test_value"}, ["dep1", "dep2"])
        print("  ✅ Données mises en cache")
        
        # Récupération des données
        cached_data = cache_manager.get("test_key")
        if cached_data and cached_data.get("data") == "test_value":
            print("  ✅ Données récupérées du cache")
        else:
            print("  ❌ Erreur lors de la récupération des données")
        
        # Statistiques du cache
        stats = cache_manager.get_stats()
        if "hit_rate" in stats:
            print("  ✅ Statistiques du cache récupérées")
        else:
            print("  ❌ Erreur lors de la récupération des statistiques")
        
        # Nettoyage
        clear_cache()
        print("  ✅ Cache vidé avec succès")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test du cache: {e}")
        return False


def test_performance_monitor():
    """Test du moniteur de performance."""
    print("🧪 Test du moniteur de performance...")
    
    try:
        from lcpi.aep.utils.performance_monitor import get_performance_monitor, profile_algorithm
        
        # Créer une instance du moniteur
        monitor = get_performance_monitor()
        print("  ✅ Moniteur de performance créé avec succès")
        
        # Test du profiling
        with profile_algorithm("test_algorithm") as profiler:
            # Simulation d'un algorithme
            import time
            time.sleep(0.1)
            profiler.add_metric("test_metric", 42.0, "units", "Métrique de test")
            profiler.add_iteration()
        
        print("  ✅ Profiling d'algorithme réussi")
        
        # Statistiques
        stats = monitor.get_global_stats()
        if stats["total_algorithms"] > 0:
            print("  ✅ Statistiques de performance récupérées")
        else:
            print("  ❌ Erreur lors de la récupération des statistiques")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test du moniteur: {e}")
        return False


def test_parallel_monte_carlo():
    """Test de l'analyse Monte Carlo parallélisée."""
    print("🧪 Test de l'analyse Monte Carlo parallélisée...")
    
    try:
        from lcpi.aep.optimization.parallel_monte_carlo import run_parallel_monte_carlo
        
        # Données de test
        base_network = {
            "nodes": {
                "N1": {"demand": 0.001, "elevation": 100},
                "N2": {"demand": 0.0008, "elevation": 95}
            },
            "pipes": {
                "P1": {"from": "N1", "to": "N2", "length": 100, "diameter": 150}
            }
        }
        
        parameter_distributions = {
            "node_demand": {
                "type": "normal",
                "mean": 0.001,
                "std": 0.0002,
                "min": 0.0001,
                "max": 0.002
            }
        }
        
        # Test avec un petit nombre de simulations
        results = run_parallel_monte_carlo(
            base_network=base_network,
            parameter_distributions=parameter_distributions,
            num_simulations=10,  # Petit nombre pour le test
            solver_name="lcpi",
            max_workers=2,
            use_cache=True
        )
        
        if "analysis" in results and "execution_time" in results:
            print("  ✅ Analyse Monte Carlo parallélisée réussie")
            print(f"     Temps d'exécution: {results['execution_time']:.3f}s")
            print(f"     Simulations: {results['analysis']['total_simulations']}")
        else:
            print("  ❌ Erreur lors de l'analyse Monte Carlo")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test Monte Carlo: {e}")
        return False


def test_performance_commands():
    """Test des commandes de performance."""
    print("🧪 Test des commandes de performance...")
    
    try:
        from lcpi.aep.commands.performance import app as performance_app
        
        # Vérifier que l'app est créée
        if hasattr(performance_app, 'commands'):
            print("  ✅ Commande performance créée avec succès")
        else:
            print("  ❌ Erreur lors de la création de la commande performance")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des commandes de performance: {e}")
        return False


def test_sensitivity_commands():
    """Test des commandes de sensibilité."""
    print("🧪 Test des commandes de sensibilité...")
    
    try:
        from lcpi.aep.commands.sensitivity import app as sensitivity_app
        
        # Vérifier que l'app est créée
        if hasattr(sensitivity_app, 'commands'):
            print("  ✅ Commande sensitivity créée avec succès")
        else:
            print("  ❌ Erreur lors de la création de la commande sensitivity")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des commandes de sensibilité: {e}")
        return False


def test_main_commands():
    """Test des commandes principales."""
    print("🧪 Test des commandes principales...")
    
    try:
        from lcpi.aep.commands.main import app as main_app
        
        # Vérifier que l'app est créée
        if hasattr(main_app, 'commands'):
            print("  ✅ Commandes principales créées avec succès")
            
            # Vérifier les sous-commandes
            subcommands = list(main_app.commands.keys())
            expected_subcommands = [
                'solveurs', 'data', 'project', 'network', 
                'performance', 'sensitivity', 'version', 'status', 'help', 'demo'
            ]
            
            missing_subcommands = [cmd for cmd in expected_subcommands if cmd not in subcommands]
            if not missing_subcommands:
                print("  ✅ Toutes les sous-commandes sont présentes")
            else:
                print(f"  ⚠️  Sous-commandes manquantes: {missing_subcommands}")
        else:
            print("  ❌ Erreur lors de la création des commandes principales")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des commandes principales: {e}")
        return False


def main():
    """Fonction principale de test."""
    print("🚀 TEST DES COMMANDES CLI DE LA PHASE 4")
    print("=" * 50)
    
    tests = [
        ("Gestionnaire de Cache", test_cache_manager),
        ("Moniteur de Performance", test_performance_monitor),
        ("Monte Carlo Parallélisé", test_parallel_monte_carlo),
        ("Commandes de Performance", test_performance_commands),
        ("Commandes de Sensibilité", test_sensitivity_commands),
        ("Commandes Principales", test_main_commands)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"  ❌ Erreur inattendue: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! La Phase 4 est opérationnelle.")
        return 0
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
