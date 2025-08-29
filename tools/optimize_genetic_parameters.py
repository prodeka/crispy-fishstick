#!/usr/bin/env python3
"""
Script d'optimisation des paramètres de l'algorithme génétique LCPI.

Ce script teste différentes combinaisons de paramètres pour optimiser
le compromis entre temps de calcul et qualité de la solution.
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import itertools

# Forcer l'encodage UTF-8 pour le terminal
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    # Forcer l'encodage de la console Windows
    try:
        import subprocess
        subprocess.run(['chcp', '65001'], shell=True, check=True, capture_output=True)
    except:
        pass

# Ajouter le répertoire src au path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

def load_harmonized_configs() -> Dict[str, Any]:
    """Charge les configurations harmonisées."""
    configs = {}
    
    # Charger la configuration des paramètres de simulation
    sim_config_path = "harmonized_simulation_config.json"
    if Path(sim_config_path).exists():
        with open(sim_config_path, 'r', encoding='utf-8') as f:
            configs["simulation"] = json.load(f)
        print(f"✅ Configuration simulation chargée: {sim_config_path}")
    else:
        print(f"⚠️ Configuration simulation non trouvée: {sim_config_path}")
    
    # Charger la configuration des contraintes hydrauliques
    constraints_config_path = "harmonized_hydraulic_constraints.json"
    if Path(constraints_config_path).exists():
        with open(constraints_config_path, 'r', encoding='utf-8') as f:
            configs["constraints"] = json.load(f)
        print(f"✅ Configuration contraintes chargée: {constraints_config_path}")
    else:
        print(f"⚠️ Configuration contraintes non trouvée: {constraints_config_path}")
    
    return configs

def find_test_network() -> Path:
    """Trouve un réseau de test approprié."""
    candidates = [
        Path("test_validation/hardy_cross_test.yml"),
        Path("examples/hardy_cross_test.yml"),
        Path("examples/bismark-Administrator.inp"),
        Path("bismark_inp.inp")
    ]
    
    for candidate in candidates:
        if candidate.exists():
            print(f"✅ Réseau de test trouvé: {candidate}")
            return candidate
    
    # Créer un réseau de test simple si aucun n'existe
    print("⚠️ Aucun réseau de test trouvé, création d'un réseau simple...")
    return create_simple_test_network()

def create_simple_test_network() -> Path:
    """Crée un réseau de test simple pour l'optimisation des paramètres."""
    
    simple_network = {
        "nodes": {
            "source": {"type": "tank", "elevation": 100.0, "demand": 0.0},
            "n1": {"type": "junction", "elevation": 90.0, "demand": 0.05},
            "n2": {"type": "junction", "elevation": 85.0, "demand": 0.03},
            "n3": {"type": "junction", "elevation": 80.0, "demand": 0.02}
        },
        "links": {
            "l1": {"from": "source", "to": "n1", "length": 500.0, "diameter": 0.2},
            "l2": {"from": "n1", "to": "n2", "length": 300.0, "diameter": 0.15},
            "l3": {"from": "n2", "to": "n3", "length": 400.0, "diameter": 0.1}
        },
        "tanks": {
            "source": {"elevation": 100.0, "initial_level": 95.0, "min_level": 90.0, "max_level": 100.0}
        }
    }
    
    output_path = Path("simple_test_network.yml")
    try:
        import yaml
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(simple_network, f, default_flow_style=False, indent=2)
        print(f"✅ Réseau de test simple créé: {output_path}")
        return output_path
    except ImportError:
        # Fallback JSON si YAML n'est pas disponible
        with open(output_path.with_suffix('.json'), 'w', encoding='utf-8') as f:
            json.dump(simple_network, f, indent=2, ensure_ascii=False)
        print(f"✅ Réseau de test simple créé: {output_path.with_suffix('.json')}")
        return output_path.with_suffix('.json')

def define_parameter_combinations() -> List[Dict[str, Any]]:
    """Définit les combinaisons de paramètres à tester."""
    
    # Paramètres de base de l'algorithme génétique (respectant les contraintes Pydantic)
    base_params = {
        "generations": [10, 15, 20, 25, 30, 40],  # Minimum 10
        "population": [20, 30, 40, 50, 60, 80],   # Minimum 20
        "mutation_rate": [0.1, 0.15, 0.2],
        "crossover_rate": [0.7, 0.8, 0.9],
        "elite_size": [2, 3, 4]
    }
    
    # Combinaisons à tester (limitées pour éviter une explosion combinatoire)
    combinations = []
    
    # Combinaisons prioritaires (petites populations, peu de générations)
    fast_combinations = [
        {"generations": 10, "population": 20, "mutation_rate": 0.15, "crossover_rate": 0.8, "elite_size": 2},
        {"generations": 15, "population": 25, "mutation_rate": 0.15, "crossover_rate": 0.8, "elite_size": 3},
        {"generations": 20, "population": 30, "mutation_rate": 0.2, "crossover_rate": 0.8, "elite_size": 3},
    ]
    
    # Combinaisons équilibrées
    balanced_combinations = [
        {"generations": 20, "population": 40, "mutation_rate": 0.15, "crossover_rate": 0.8, "elite_size": 4},
        {"generations": 25, "population": 50, "mutation_rate": 0.1, "crossover_rate": 0.9, "elite_size": 4},
    ]
    
    # Combinaisons de qualité (plus de temps, meilleure qualité)
    quality_combinations = [
        {"generations": 30, "population": 60, "mutation_rate": 0.1, "crossover_rate": 0.9, "elite_size": 5},
        {"generations": 40, "population": 80, "mutation_rate": 0.08, "crossover_rate": 0.9, "elite_size": 6},
    ]
    
    combinations.extend(fast_combinations)
    combinations.extend(balanced_combinations)
    combinations.extend(quality_combinations)
    
    print(f"✅ {len(combinations)} combinaisons de paramètres définies:")
    for i, combo in enumerate(combinations):
        print(f"   {i+1}. G:{combo['generations']}, P:{combo['population']}, M:{combo['mutation_rate']}, C:{combo['crossover_rate']}, E:{combo['elite_size']}")
    
    return combinations

def run_optimization_with_params(input_path: Path, params: Dict[str, Any], 
                                configs: Dict[str, Any], output_prefix: str) -> Dict[str, Any]:
    """Exécute l'optimisation avec des paramètres spécifiques."""
    
    print(f"\n🔄 Test avec paramètres:")
    print(f"   • Générations: {params['generations']}")
    print(f"   • Population: {params['population']}")
    print(f"   • Taux mutation: {params['mutation_rate']}")
    print(f"   • Taux croisement: {params['crossover_rate']}")
    print(f"   • Taille élite: {params['elite_size']}")
    
    # Paramètres de simulation harmonisés
    tolerance = configs.get("simulation", {}).get("convergence", {}).get("tolerance", 1e-6)
    max_iterations = configs.get("simulation", {}).get("convergence", {}).get("max_iterations", 200)
    
    # Contraintes harmonisées
    constraints = configs.get("constraints", {})
    pressure_min = constraints.get("pressure", {}).get("min_mce", 10.0)
    velocity_max = constraints.get("velocity", {}).get("max_ms", 3.0)
    velocity_min = constraints.get("velocity", {}).get("min_ms", 0.3)
    
    # Commande d'optimisation
    cmd = [
        sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
        str(input_path),
        "--method", "genetic",
        "--generations", str(params['generations']),
        "--population", str(params['population']),
        "--tolerance", str(tolerance),
        "--max-iterations", str(max_iterations),
        "--solver", "lcpi",
        "--pression-min", str(pressure_min),
        "--vitesse-max", str(velocity_max),
        "--vitesse-min", str(velocity_min),
        "--show-stats",
        "--output", f"{output_prefix}_G{params['generations']}_P{params['population']}",
        "--no-log"
    ]
    
    # Exécuter la commande
    start_time = time.time()
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
        execution_time = time.time() - start_time
        
        print(f"   ✅ Exécution réussie en {execution_time:.1f}s")
        
        return {
            "success": True,
            "execution_time": execution_time,
            "params": params,
            "output_file": f"{output_prefix}_G{params['generations']}_P{params['population']}",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print(f"   ⏱️ Timeout après 300s")
        return {"success": False, "error": "timeout", "params": params}
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erreur d'exécution: {e}")
        return {"success": False, "error": str(e), "params": params, "returncode": e.returncode}
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return {"success": False, "error": str(e), "params": params}

def load_and_analyze_results(output_file: str) -> Optional[Dict[str, Any]]:
    """Charge et analyse les résultats d'optimisation."""
    
    result_paths = [
        Path(f"{output_file}.json"),
        Path("results") / f"{output_file}.json"
    ]
    
    for result_path in result_paths:
        if result_path.exists():
            try:
                with open(result_path, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                
                # Analyser les résultats
                proposals = results.get("proposals", [])
                if proposals:
                    best = proposals[0]
                    
                    analysis = {
                        "output_file": str(result_path),
                        "proposals_count": len(proposals),
                        "best_solution": {
                            "CAPEX": best.get("CAPEX", 0),
                            "constraints_ok": best.get("constraints_ok", False),
                            "feasibility_score": best.get("feasibility_score", 0),
                            "diameter_distribution": best.get("diameter_distribution", {})
                        },
                        "statistics": {}
                    }
                    
                    # Statistiques sur toutes les solutions
                    costs = [p.get("CAPEX", 0) for p in proposals if p.get("CAPEX", 0) > 0]
                    feasible_count = sum(1 for p in proposals if p.get("constraints_ok", False))
                    
                    if costs:
                        analysis["statistics"] = {
                            "cost_min": min(costs),
                            "cost_max": max(costs),
                            "cost_avg": sum(costs) / len(costs),
                            "feasible_count": feasible_count,
                            "feasible_ratio": feasible_count / len(proposals)
                        }
                    
                    return analysis
                    
            except Exception as e:
                print(f"   ❌ Erreur lecture {result_path}: {e}")
    
    return None

def evaluate_parameter_combination(results: Dict[str, Any], 
                                 execution_time: float) -> Dict[str, Any]:
    """Évalue la qualité d'une combinaison de paramètres."""
    
    evaluation = {
        "params": results["params"],
        "execution_time": execution_time,
        "solution_quality": 0.0,
        "efficiency_score": 0.0,
        "overall_score": 0.0
    }
    
    # Score de qualité de la solution (0-100)
    best_solution = results.get("best_solution", {})
    constraints_ok = best_solution.get("constraints_ok", False)
    feasibility_score = best_solution.get("feasibility_score", 0)
    
    if constraints_ok:
        evaluation["solution_quality"] = 80 + (feasibility_score * 20)  # 80-100 si faisable
    else:
        evaluation["solution_quality"] = feasibility_score * 40  # 0-40 si non faisable
    
    # Score d'efficacité (0-100) - basé sur le temps et la population
    population = results["params"]["population"]
    generations = results["params"]["generations"]
    
    # Facteur de complexité (plus la population et les générations sont élevées, plus c'est complexe)
    complexity_factor = (population * generations) / 1000.0
    
    # Score d'efficacité inversement proportionnel à la complexité et au temps
    if execution_time > 0:
        efficiency_score = 100 / (1 + complexity_factor + (execution_time / 60.0))
        evaluation["efficiency_score"] = min(100, efficiency_score)
    
    # Score global (moyenne pondérée)
    evaluation["overall_score"] = (
        evaluation["solution_quality"] * 0.6 + 
        evaluation["efficiency_score"] * 0.4
    )
    
    return evaluation

def rank_parameter_combinations(evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Classe les combinaisons de paramètres par score global."""
    
    # Filtrer les évaluations réussies
    successful_evaluations = [e for e in evaluations if "overall_score" in e]
    
    if not successful_evaluations:
        return []
    
    # Trier par score global décroissant
    ranked = sorted(successful_evaluations, key=lambda x: x["overall_score"], reverse=True)
    
    print(f"\n🏆 CLASSEMENT DES COMBINAISONS DE PARAMÈTRES")
    print("=" * 80)
    
    for i, eval_result in enumerate(ranked[:10]):  # Top 10
        params = eval_result["params"]
        print(f"{i+1:2d}. Score: {eval_result['overall_score']:5.1f} | "
              f"Qualité: {eval_result['solution_quality']:5.1f} | "
              f"Efficacité: {eval_result['efficiency_score']:5.1f} | "
              f"Temps: {eval_result['execution_time']:5.1f}s | "
              f"G:{params['generations']:2d}, P:{params['population']:2d}, "
              f"M:{params['mutation_rate']:4.2f}, C:{params['crossover_rate']:4.2f}, "
              f"E:{params['elite_size']:1d}")
    
    return ranked

def generate_recommendations(ranked_evaluations: List[Dict[str, Any]]) -> None:
    """Génère des recommandations basées sur les meilleures combinaisons."""
    
    if not ranked_evaluations:
        print("❌ Aucune évaluation réussie pour générer des recommandations")
        return
    
    print(f"\n💡 RECOMMANDATIONS D'OPTIMISATION")
    print("=" * 60)
    
    best = ranked_evaluations[0]
    best_params = best["params"]
    
    print(f"🥇 Meilleure combinaison:")
    print(f"   • Générations: {best_params['generations']}")
    print(f"   • Population: {best_params['population']}")
    print(f"   • Taux mutation: {best_params['mutation_rate']}")
    print(f"   • Taux croisement: {best_params['crossover_rate']}")
    print(f"   • Taille élite: {best_params['elite_size']}")
    print(f"   • Score global: {best['overall_score']:.1f}")
    print(f"   • Temps d'exécution: {best['execution_time']:.1f}s")
    
    # Analyser les tendances
    print(f"\n📊 Tendances observées:")
    
    # Analyser la taille de population
    populations = [e["params"]["population"] for e in ranked_evaluations[:5]]
    avg_population = sum(populations) / len(populations)
    print(f"   • Population moyenne (top 5): {avg_population:.0f}")
    
    # Analyser le nombre de générations
    generations = [e["params"]["generations"] for e in ranked_evaluations[:5]]
    avg_generations = sum(generations) / len(generations)
    print(f"   • Générations moyennes (top 5): {avg_generations:.0f}")
    
    # Recommandations spécifiques
    print(f"\n🔧 Recommandations d'implémentation:")
    
    if best_params["population"] <= 30:
        print(f"   • Utiliser une population modérée ({best_params['population']}) pour un bon compromis")
    else:
        print(f"   • Population élevée ({best_params['population']}) - privilégier la qualité")
    
    if best_params["generations"] <= 20:
        print(f"   • Nombre de générations limité ({best_params['generations']}) - optimisation rapide")
    else:
        print(f"   • Nombre de générations élevé ({best_params['generations']}) - convergence lente")
    
    if best_params["mutation_rate"] <= 0.15:
        print(f"   • Taux de mutation conservateur ({best_params['mutation_rate']}) - stabilité")
    else:
        print(f"   • Taux de mutation élevé ({best_params['mutation_rate']}) - exploration")
    
    print(f"\n📝 Actions recommandées:")
    print(f"   1. Implémenter la meilleure combinaison dans genetic_algorithm.py")
    print(f"   2. Tester sur des réseaux plus complexes")
    print(f"   3. Ajuster selon les contraintes de temps du projet")
    print(f"   4. Documenter les paramètres optimaux")

def save_optimization_report(evaluations: List[Dict[str, Any]], 
                            ranked_evaluations: List[Dict[str, Any]],
                            output_path: str = "genetic_parameters_optimization_report.json") -> bool:
    """Sauvegarde le rapport d'optimisation des paramètres."""
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_combinations_tested": len(evaluations),
        "successful_evaluations": len(ranked_evaluations),
        "evaluations": evaluations,
        "ranked_evaluations": ranked_evaluations,
        "best_combination": ranked_evaluations[0] if ranked_evaluations else None,
        "metadata": {
            "version": "1.0",
            "description": "Rapport d'optimisation des paramètres de l'algorithme génétique LCPI"
        }
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport d'optimisation sauvegardé: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def main():
    """Fonction principale."""
    print("🚀 OPTIMISATION DES PARAMÈTRES DE L'ALGORITHME GÉNÉTIQUE LCPI")
    print("=" * 80)
    
    try:
        # Charger les configurations harmonisées
        configs = load_harmonized_configs()
        
        # Trouver le réseau de test
        test_network = find_test_network()
        
        # Définir les combinaisons de paramètres à tester
        parameter_combinations = define_parameter_combinations()
        
        # Préfixe de sortie avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_prefix = f"param_optimization_{timestamp}"
        
        print(f"\n🎯 Configuration de test:")
        print(f"   • Réseau: {test_network}")
        print(f"   • Préfixe sortie: {output_prefix}")
        print(f"   • Combinaisons à tester: {len(parameter_combinations)}")
        
        # Tester chaque combinaison de paramètres
        evaluations = []
        
        for i, params in enumerate(parameter_combinations):
            print(f"\n{'='*60}")
            print(f"🧪 Test {i+1}/{len(parameter_combinations)}")
            print(f"{'='*60}")
            
            # Exécuter l'optimisation
            result = run_optimization_with_params(test_network, params, configs, output_prefix)
            
            if result.get("success", False):
                # Charger et analyser les résultats
                analysis = load_and_analyze_results(result["output_file"])
                
                if analysis:
                    # Évaluer la combinaison de paramètres
                    evaluation = evaluate_parameter_combination(analysis, result["execution_time"])
                    evaluations.append(evaluation)
                    
                    print(f"   📊 Évaluation:")
                    print(f"      • Qualité solution: {evaluation['solution_quality']:.1f}")
                    print(f"      • Score efficacité: {evaluation['efficiency_score']:.1f}")
                    print(f"      • Score global: {evaluation['overall_score']:.1f}")
                else:
                    print(f"   ❌ Impossible d'analyser les résultats")
            else:
                print(f"   ❌ Échec de l'optimisation: {result.get('error', 'unknown')}")
        
        # Classer les combinaisons de paramètres
        ranked_evaluations = rank_parameter_combinations(evaluations)
        
        # Générer les recommandations
        generate_recommendations(ranked_evaluations)
        
        # Sauvegarder le rapport
        save_optimization_report(evaluations, ranked_evaluations)
        
        print(f"\n✅ Optimisation des paramètres terminée avec succès!")
        print(f"   • Combinaisons testées: {len(parameter_combinations)}")
        print(f"   • Évaluations réussies: {len(ranked_evaluations)}")
        
        if ranked_evaluations:
            best = ranked_evaluations[0]
            print(f"   • Meilleur score: {best['overall_score']:.1f}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'optimisation des paramètres: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
