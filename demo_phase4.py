#!/usr/bin/env python3
"""
Démonstration des nouvelles fonctionnalités de la Phase 4 - Améliorations de Performance et Parallélisation.

Ce script démontre :
- Gestion du cache intelligent
- Monitoring des performances
- Analyse Monte Carlo parallélisée
- Nouvelles commandes CLI
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_cache_manager():
    """Démonstration du gestionnaire de cache intelligent."""
    print("🗄️ DÉMONSTRATION DU CACHE INTELLIGENT")
    print("=" * 50)
    
    try:
        from lcpi.aep.core.cache_manager import get_cache_manager, clear_cache
        
        # Créer une instance du cache
        cache = get_cache_manager(max_size_mb=100, max_entries=200)
        print("✅ Cache manager créé avec succès")
        
        # Test des opérations de base
        print("\n📊 Test des opérations de base...")
        
        # Mettre des données en cache
        cache.set("network_config_1", {"nodes": 4, "pipes": 4, "type": "maillé"}, ["config"])
        cache.set("hardy_cross_result_1", {"iterations": 12, "convergence": True}, ["network_config_1"])
        cache.set("epanet_result_1", {"pressures": {"N1": 25.0, "N2": 22.0}}, ["network_config_1"])
        
        print("  ✅ 3 objets mis en cache")
        
        # Récupération des données
        network_config = cache.get("network_config_1")
        hardy_result = cache.get("hardy_cross_result_1")
        epanet_result = cache.get("epanet_result_1")
        
        print(f"  ✅ Données récupérées: {network_config['nodes']} nœuds, {network_config['pipes']} conduites")
        print(f"  ✅ Hardy-Cross: {hardy_result['iterations']} itérations, convergence: {hardy_result['convergence']}")
        print(f"  ✅ EPANET: {len(epanet_result.get('pressions', {}))} pressions calculées")
        
        # Test des dépendances
        print("\n🔗 Test des dépendances...")
        cache.invalidate_by_dependency("config")
        
        # Vérifier que les objets dépendants sont supprimés
        network_config_after = cache.get("network_config_1")
        hardy_result_after = cache.get("hardy_cross_result_1")
        
        print(f"  ✅ Après invalidation des dépendances:")
        print(f"     - Network config: {'❌ Supprimé' if network_config_after is None else '✅ Conservé'}")
        print(f"     - Hardy-Cross: {'❌ Supprimé' if hardy_result_after is None else '✅ Conservé'}")
        
        # Statistiques du cache
        stats = cache.get_stats()
        print(f"\n📈 Statistiques du cache:")
        print(f"  - Taux de succès: {stats['hit_rate']*100:.1f}%")
        print(f"  - Entrées actuelles: {stats['current_entries']}")
        print(f"  - Taille actuelle: {stats['current_size_mb']:.1f} MB")
        print(f"  - Hits: {stats['hits']}")
        print(f"  - Misses: {stats['misses']}")
        
        # Nettoyage
        clear_cache()
        print("\n🧹 Cache vidé avec succès")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la démonstration du cache: {e}")
        return False


def demo_performance_monitor():
    """Démonstration du moniteur de performance."""
    print("\n📊 DÉMONSTRATION DU MONITEUR DE PERFORMANCE")
    print("=" * 50)
    
    try:
        from lcpi.aep.utils.performance_monitor import get_performance_monitor, profile_algorithm
        
        # Créer une instance du moniteur
        monitor = get_performance_monitor()
        print("✅ Moniteur de performance créé avec succès")
        
        # Test du profiling
        print("\n🔍 Test du profiling d'algorithmes...")
        
        # Simuler plusieurs algorithmes
        algorithms = ["hardy_cross", "epanet_simulation", "optimization_genetic"]
        
        for i, alg_name in enumerate(algorithms):
            with profile_algorithm(f"{alg_name}_test_{i}") as profiler:
                # Simulation d'un algorithme
                time.sleep(0.1)  # Simulation d'un calcul
                
                # Ajouter des métriques
                profiler.add_metric("iterations", i + 5, "count", "Nombre d'itérations")
                profiler.add_metric("convergence", 0.95 + i * 0.01, "ratio", "Taux de convergence")
                profiler.add_metric("memory_peak", 50 + i * 10, "MB", "Pic de mémoire")
                
                # Marquer une itération
                profiler.add_iteration()
                
                print(f"  ✅ {alg_name}: profilé avec succès")
        
        # Statistiques globales
        stats = monitor.get_global_stats()
        print(f"\n📈 Statistiques globales:")
        print(f"  - Total d'algorithmes: {stats['total_algorithms']}")
        print(f"  - Temps d'exécution total: {stats['total_execution_time']:.3f}s")
        print(f"  - Pic de mémoire global: {stats['total_memory_peak']:.1f} MB")
        print(f"  - Exécutions réussies: {stats['successful_runs']}")
        
        # Statistiques par algorithme
        print(f"\n🔍 Statistiques par algorithme:")
        for alg_name in algorithms:
            alg_stats = monitor.get_algorithm_stats(f"{alg_name}_test_0")
            if "error" not in alg_stats:
                print(f"  - {alg_name}: {alg_stats['total_runs']} exécutions, "
                      f"taux de succès: {alg_stats['success_rate']*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la démonstration du moniteur: {e}")
        return False


def demo_parallel_monte_carlo():
    """Démonstration de l'analyse Monte Carlo parallélisée."""
    print("\n🚀 DÉMONSTRATION MONTE CARLO PARALLÉLISÉ")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimization.parallel_monte_carlo import run_parallel_monte_carlo
        
        # Données de test
        base_network = {
            "nodes": {
                "N1": {"demand": 0.001, "elevation": 100},
                "N2": {"demand": 0.0008, "elevation": 95},
                "N3": {"demand": 0.0006, "elevation": 90}
            },
            "pipes": {
                "P1": {"from": "N1", "to": "N2", "length": 100, "diameter": 150},
                "P2": {"from": "N2", "to": "N3", "length": 80, "diameter": 125}
            }
        }
        
        parameter_distributions = {
            "node_demand": {
                "type": "normal",
                "mean": 0.001,
                "std": 0.0002,
                "min": 0.0001,
                "max": 0.002
            },
            "pipe_roughness": {
                "type": "uniform",
                "min": 100,
                "max": 150
            }
        }
        
        print("📋 Configuration de l'analyse Monte Carlo:")
        print(f"  - Réseau: {len(base_network['nodes'])} nœuds, {len(base_network['pipes'])} conduites")
        print(f"  - Paramètres variables: {len(parameter_distributions)}")
        print(f"  - Simulations: 20 (petit nombre pour la démo)")
        print(f"  - Workers: 2")
        
        # Lancer l'analyse Monte Carlo parallélisée
        print("\n⚡ Lancement de l'analyse...")
        start_time = time.time()
        
        results = run_parallel_monte_carlo(
            base_network=base_network,
            parameter_distributions=parameter_distributions,
            num_simulations=20,  # Petit nombre pour la démo
            solver_name="lcpi",
            max_workers=2,
            use_cache=True
        )
        
        execution_time = time.time() - start_time
        
        # Affichage des résultats
        print(f"\n✅ Analyse terminée en {execution_time:.3f} secondes")
        
        analysis = results['analysis']
        stats = results['stats']
        
        print(f"\n📊 Résultats de l'analyse:")
        print(f"  - Total de simulations: {analysis['total_simulations']}")
        print(f"  - Simulations réussies: {analysis['successful_simulations']}")
        print(f"  - Taux de succès: {analysis['success_rate']*100:.1f}%")
        print(f"  - Taux de cache: {analysis['cache_hit_rate']*100:.1f}%")
        print(f"  - Temps moyen par simulation: {analysis['average_execution_time']:.3f}s")
        
        print(f"\n⚡ Statistiques des workers:")
        print(f"  - Workers utilisés: {stats.get('max_workers', 'N/A')}")
        print(f"  - Tâches totales: {stats.get('total_tasks', 'N/A')}")
        print(f"  - Tâches complétées: {stats.get('completed_tasks', 'N/A')}")
        print(f"  - Cache hits: {stats.get('cache_hits', 'N/A')}")
        print(f"  - Cache misses: {stats.get('cache_misses', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la démonstration Monte Carlo: {e}")
        return False


def demo_cli_commands():
    """Démonstration des nouvelles commandes CLI."""
    print("\n🔧 DÉMONSTRATION DES NOUVELLES COMMANDES CLI")
    print("=" * 50)
    
    try:
        # Test des commandes de performance
        from lcpi.aep.commands.performance import app as performance_app
        print("✅ Commande performance créée avec succès")
        
        # Test des commandes de sensibilité
        from lcpi.aep.commands.sensitivity import app as sensitivity_app
        print("✅ Commande sensitivity créée avec succès")
        
        # Test des commandes principales
        from lcpi.aep.commands.main import app as main_app
        print("✅ Commandes principales créées avec succès")
        
        print("\n📋 Commandes disponibles:")
        print("  🚀 Performance:")
        print("    - lcpi aep performance profile")
        print("    - lcpi aep performance monitor")
        print("    - lcpi aep performance cache")
        print("    - lcpi aep performance benchmark")
        print("    - lcpi aep performance report")
        print("    - lcpi aep performance optimize")
        
        print("  📊 Sensibilité:")
        print("    - lcpi aep sensitivity parallel")
        print("    - lcpi aep sensitivity distributions")
        print("    - lcpi aep sensitivity validate")
        
        print("  🌊 Principales:")
        print("    - lcpi aep version")
        print("    - lcpi aep status")
        print("    - lcpi aep help")
        print("    - lcpi aep demo")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la démonstration des commandes CLI: {e}")
        return False


def main():
    """Fonction principale de démonstration."""
    print("🎉 DÉMONSTRATION DES NOUVELLES FONCTIONNALITÉS DE LA PHASE 4")
    print("🚀 Améliorations de Performance et Parallélisation")
    print("=" * 70)
    
    demos = [
        ("Gestionnaire de Cache Intelligent", demo_cache_manager),
        ("Moniteur de Performance", demo_performance_monitor),
        ("Monte Carlo Parallélisé", demo_parallel_monte_carlo),
        ("Nouvelles Commandes CLI", demo_cli_commands)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*70}")
        try:
            success = demo_func()
            results.append((demo_name, success))
        except Exception as e:
            print(f"❌ Erreur inattendue lors de {demo_name}: {e}")
            results.append((demo_name, False))
    
    # Résumé des démonstrations
    print(f"\n{'='*70}")
    print("📊 RÉSUMÉ DES DÉMONSTRATIONS")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for demo_name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"  {status} {demo_name}")
    
    print(f"\n🎯 Résultat: {passed}/{total} démonstrations réussies")
    
    if passed == total:
        print("\n🎉 Toutes les démonstrations sont réussies !")
        print("🚀 La Phase 4 est pleinement opérationnelle.")
        print("\n💡 Prochaines étapes:")
        print("  1. Tester les commandes CLI avec de vrais fichiers de configuration")
        print("  2. Optimiser les performances sur des réseaux plus complexes")
        print("  3. Documenter les nouvelles fonctionnalités")
        print("  4. Préparer la Phase 5 : Interface Utilisateur")
    else:
        print(f"\n⚠️  {total - passed} démonstration(s) à corriger")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
