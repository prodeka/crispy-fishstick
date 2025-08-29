#!/usr/bin/env python3
"""
Script pour relancer les tests comparatifs améliorés entre EPANET et LCPI.

Ce script utilise les paramètres harmonisés pour exécuter une comparaison
équitable entre les deux solveurs et analyser les résultats.
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

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

def find_test_network() -> Optional[Path]:
    """Trouve un réseau de test approprié."""
    candidates = [
        Path("bismark_inp.inp"),
        Path("examples/bismark-Administrator.inp"),
        Path("examples/bismark-Administrator.inp.backup"),
        Path("test_validation/hardy_cross_test.yml"),
        Path("examples/hardy_cross_test.yml")
    ]
    
    for candidate in candidates:
        if candidate.exists():
            print(f"✅ Réseau de test trouvé: {candidate}")
            return candidate
    
    print("❌ Aucun réseau de test trouvé")
    return None

def run_optimization_with_solver(input_path: Path, solver: str, 
                                configs: Dict[str, Any], output_prefix: str) -> Dict[str, Any]:
    """Exécute l'optimisation avec un solveur spécifique."""
    
    print(f"\n🔄 Exécution avec {solver.upper()}")
    print(f"   📄 Réseau: {input_path}")
    
    # Paramètres d'optimisation harmonisés (respectant les contraintes Pydantic)
    generations = max(20, 10)  # Minimum 10
    population = max(30, 20)   # Minimum 20
    
    # Paramètres de simulation harmonisés
    tolerance = configs.get("simulation", {}).get("convergence", {}).get("tolerance", 1e-6)
    max_iterations = configs.get("simulation", {}).get("convergence", {}).get("max_iterations", 200)
    
    # Contraintes harmonisées
    constraints = configs.get("constraints", {})
    pressure_min = constraints.get("pressure", {}).get("min_mce", 10.0)
    velocity_max = constraints.get("velocity", {}).get("max_ms", 3.0)
    velocity_min = constraints.get("velocity", {}).get("min_ms", 0.3)
    
    # Commande d'optimisation (exécutée depuis le répertoire src pour éviter les problèmes d'imports relatifs)
    cmd = [
        sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
        str(Path("../") / input_path.name if input_path.is_absolute() else input_path),
        "--method", "genetic",
        "--generations", str(generations),
        "--population", str(population),
        "--tolerance", str(tolerance),
        "--max-iterations", str(max_iterations),
        "--solver", solver,
        "--pression-min", str(pressure_min),
        "--vitesse-max", str(velocity_max),
        "--vitesse-min", str(velocity_min),
        "--show-stats",
        "--output", f"{output_prefix}_{solver}",
        "--verbose",
        "--no-log"
    ]
    
    # Changer vers le répertoire src pour l'exécution
    original_cwd = Path.cwd()
    src_dir = Path(__file__).resolve().parents[1] / "src"
    
    print(f"   ⚙️ Paramètres:")
    print(f"      • Générations: {generations}")
    print(f"      • Population: {population}")
    print(f"      • Tolérance: {tolerance}")
    print(f"      • Itérations max: {max_iterations}")
    print(f"      • Pression min: {pressure_min} mCE")
    print(f"      • Vitesse max: {velocity_max} m/s")
    print(f"      • Vitesse min: {velocity_min} m/s")
    
    # Exécuter la commande
    start_time = time.time()
    try:
        # Exécuter depuis le répertoire src pour éviter les problèmes d'imports relatifs
        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=600, cwd=src_dir)
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"   ✅ Exécution réussie en {execution_time:.1f}s")
            return {
                "success": True,
                "execution_time": execution_time,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "output_file": f"{output_prefix}_{solver}"
            }
        else:
            print(f"   ❌ Erreur d'exécution: code de retour {result.returncode}")
            print(f"   📄 Sortie standard: {result.stdout[:500]}...")
            print(f"   ⚠️ Erreurs: {result.stderr[:500]}...")
            return {"success": False, "error": f"Code de retour {result.returncode}", "returncode": result.returncode}
        
    except subprocess.TimeoutExpired:
        print(f"   ⏱️ Timeout après 600s")
        return {"success": False, "error": "timeout"}
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return {"success": False, "error": str(e)}

def load_optimization_results(output_file: str) -> Optional[Dict[str, Any]]:
    """Charge les résultats d'optimisation depuis le fichier JSON."""
    result_paths = [
        Path(f"{output_file}.json"),
        Path("results") / f"{output_file}.json",
        Path(f"{output_file}_*.json")
    ]
    
    for result_path in result_paths:
        if result_path.exists():
            if "*" in str(result_path):
                # Chercher le fichier le plus récent
                matches = list(Path(".").glob(f"{output_file}_*.json"))
                if matches:
                    result_path = max(matches, key=lambda p: p.stat().st_mtime)
            
            try:
                with open(result_path, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                print(f"   📊 Résultats chargés: {result_path}")
                return results
            except Exception as e:
                print(f"   ❌ Erreur lecture {result_path}: {e}")
    
    return None

def analyze_optimization_results(results: Dict[str, Any], solver: str) -> Dict[str, Any]:
    """Analyse les résultats d'optimisation."""
    
    analysis = {
        "solver": solver,
        "timestamp": datetime.now().isoformat(),
        "meta": results.get("meta", {}),
        "proposals_count": len(results.get("proposals", [])),
        "best_solution": {},
        "statistics": {}
    }
    
    proposals = results.get("proposals", [])
    if proposals:
        best = proposals[0]
        analysis["best_solution"] = {
            "CAPEX": best.get("CAPEX", 0),
            "constraints_ok": best.get("constraints_ok", False),
            "feasibility_score": best.get("feasibility_score", 0),
            "diameter_distribution": best.get("diameter_distribution", {}),
            "violations": best.get("violations", {})
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

def compare_solver_results(epanet_results: Dict[str, Any], 
                          lcpi_results: Dict[str, Any]) -> Dict[str, Any]:
    """Compare les résultats des deux solveurs."""
    
    print(f"\n📊 COMPARAISON DES RÉSULTATS")
    print("=" * 60)
    
    comparison = {
        "timestamp": datetime.now().isoformat(),
        "cost_comparison": {},
        "feasibility_comparison": {},
        "performance_comparison": {},
        "recommendations": []
    }
    
    # Comparaison des coûts
    epanet_cost = epanet_results.get("best_solution", {}).get("CAPEX", 0)
    lcpi_cost = lcpi_results.get("best_solution", {}).get("CAPEX", 0)
    
    if epanet_cost > 0 and lcpi_cost > 0:
        delta = lcpi_cost - epanet_cost
        delta_percent = (delta / epanet_cost) * 100
        
        comparison["cost_comparison"] = {
            "epanet_cost": epanet_cost,
            "lcpi_cost": lcpi_cost,
            "delta": delta,
            "delta_percent": delta_percent,
            "lcpi_vs_epanet": "higher" if delta > 0 else "lower" if delta < 0 else "equal"
        }
        
        print(f"💰 Comparaison des coûts:")
        print(f"   • EPANET: {epanet_cost:,.0f} FCFA")
        print(f"   • LCPI  : {lcpi_cost:,.0f} FCFA")
        print(f"   • Différence: {delta:+,.0f} FCFA ({delta_percent:+.1f}%)")
        
        if abs(delta_percent) > 10:
            comparison["recommendations"].append(
                f"Écart de coût significatif ({delta_percent:+.1f}%) - investiguer les causes"
            )
    
    # Comparaison de la faisabilité
    epanet_feasible = epanet_results.get("best_solution", {}).get("constraints_ok", False)
    lcpi_feasible = lcpi_results.get("best_solution", {}).get("constraints_ok", False)
    
    comparison["feasibility_comparison"] = {
        "epanet_feasible": epanet_feasible,
        "lcpi_feasible": lcpi_feasible,
        "both_feasible": epanet_feasible and lcpi_feasible,
        "feasibility_consistency": epanet_feasible == lcpi_feasible
    }
    
    print(f"✅ Comparaison de la faisabilité:")
    print(f"   • EPANET: {'✅' if epanet_feasible else '❌'}")
    print(f"   • LCPI  : {'✅' if lcpi_feasible else '❌'}")
    print(f"   • Cohérence: {'✅' if epanet_feasible == lcpi_feasible else '⚠️'}")
    
    if not epanet_feasible and not lcpi_feasible:
        comparison["recommendations"].append(
            "Aucun solveur n'a trouvé de solution faisable - vérifier les contraintes"
        )
    elif epanet_feasible != lcpi_feasible:
        comparison["recommendations"].append(
            "Incohérence de faisabilité entre les solveurs - harmoniser les critères"
        )
    
    # Comparaison des performances
    epanet_time = epanet_results.get("execution_time", 0)
    lcpi_time = lcpi_results.get("execution_time", 0)
    
    if epanet_time > 0 and lcpi_time > 0:
        time_ratio = lcpi_time / epanet_time
        comparison["performance_comparison"] = {
            "epanet_time": epanet_time,
            "lcpi_time": lcpi_time,
            "time_ratio": time_ratio,
            "lcpi_vs_epanet_speed": "faster" if time_ratio < 1 else "slower"
        }
        
        print(f"⏱️ Comparaison des performances:")
        print(f"   • EPANET: {epanet_time:.1f}s")
        print(f"   • LCPI  : {lcpi_time:.1f}s")
        print(f"   • Ratio LCPI/EPANET: {time_ratio:.2f}x")
    
    # Générer des recommandations
    if not comparison["recommendations"]:
        comparison["recommendations"].append(
            "✅ Résultats cohérents - aucune action corrective nécessaire"
        )
    
    return comparison

def save_comparison_report(comparison: Dict[str, Any], 
                          epanet_results: Dict[str, Any],
                          lcpi_results: Dict[str, Any],
                          output_path: str = "enhanced_comparison_report.json") -> bool:
    """Sauvegarde le rapport de comparaison complet."""
    
    full_report = {
        "comparison": comparison,
        "epanet_results": epanet_results,
        "lcpi_results": lcpi_results,
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "description": "Rapport de comparaison amélioré entre EPANET et LCPI"
        }
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport de comparaison sauvegardé: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def main():
    """Fonction principale."""
    print("🚀 TESTS COMPARATIFS AMÉLIORÉS EPANET vs LCPI")
    print("=" * 60)
    
    try:
        # Charger les configurations harmonisées
        configs = load_harmonized_configs()
        
        # Trouver le réseau de test
        test_network = find_test_network()
        if not test_network:
            return 1
        
        # Préfixe de sortie avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_prefix = f"enhanced_comparison_{timestamp}"
        
        print(f"\n🎯 Configuration de test:")
        print(f"   • Réseau: {test_network}")
        print(f"   • Préfixe sortie: {output_prefix}")
        
        # Exécuter l'optimisation avec EPANET
        epanet_results = run_optimization_with_solver(
            test_network, "epanet", configs, output_prefix
        )
        
        if not epanet_results.get("success", False):
            print("❌ Échec de l'optimisation EPANET")
            return 1
        
        # Exécuter l'optimisation avec LCPI
        lcpi_results = run_optimization_with_solver(
            test_network, "lcpi", configs, output_prefix
        )
        
        if not lcpi_results.get("success", False):
            print("❌ Échec de l'optimisation LCPI")
            return 1
        
        # Charger et analyser les résultats
        print(f"\n📊 ANALYSE DES RÉSULTATS")
        print("=" * 60)
        
        epanet_data = load_optimization_results(epanet_results["output_file"])
        lcpi_data = load_optimization_results(lcpi_results["output_file"])
        
        if not epanet_data or not lcpi_data:
            print("❌ Impossible de charger les résultats d'optimisation")
            return 1
        
        # Analyser les résultats
        epanet_analysis = analyze_optimization_results(epanet_data, "epanet")
        lcpi_analysis = analyze_optimization_results(lcpi_data, "lcpi")
        
        # Comparer les résultats
        comparison = compare_solver_results(epanet_analysis, lcpi_analysis)
        
        # Sauvegarder le rapport
        save_comparison_report(comparison, epanet_analysis, lcpi_analysis)
        
        print(f"\n✅ Tests comparatifs améliorés terminés avec succès!")
        
        # Afficher un résumé
        print(f"\n📋 RÉSUMÉ DES RÉSULTATS")
        print("=" * 60)
        print(f"   • EPANET: {epanet_analysis['best_solution'].get('CAPEX', 0):,.0f} FCFA")
        print(f"   • LCPI  : {lcpi_analysis['best_solution'].get('CAPEX', 0):,.0f} FCFA")
        print(f"   • Faisabilité EPANET: {'✅' if epanet_analysis['best_solution'].get('constraints_ok') else '❌'}")
        print(f"   • Faisabilité LCPI  : {'✅' if lcpi_analysis['best_solution'].get('constraints_ok') else '❌'}")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests comparatifs: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
