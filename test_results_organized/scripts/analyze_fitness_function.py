#!/usr/bin/env python3
"""
Script pour analyser et améliorer la fonction d'évaluation (fitness) de l'algorithme génétique LCPI.
Objectif : Améliorer la capacité de LCPI à trouver des solutions faisables.
"""

import sys
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Any

def analyze_current_fitness_function():
    """Analyse la fonction d'évaluation actuelle."""
    
    print("🔍 ANALYSE DE LA FONCTION D'ÉVALUATION ACTUELLE")
    print("=" * 60)
    
    # Analyser les fichiers de scoring
    scoring_files = [
        "src/lcpi/aep/optimization/genetic_algorithm.py",
        "src/lcpi/aep/optimizer/constraints_handler.py",
        "src/lcpi/aep/optimizer/controllers.py"
    ]
    
    print("\n📊 FONCTIONS DE SCORING IDENTIFIÉES:")
    
    for file_path in scoring_files:
        if Path(file_path).exists():
            print(f"\n📁 {file_path}:")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Chercher les fonctions de pénalité
            if "_calculate_adaptive_penalties" in content:
                print("   ✅ _calculate_adaptive_penalties() - Pénalités adaptatives")
                
            if "apply_constraints" in content:
                print("   ✅ apply_constraints() - Application des contraintes")
                
            if "_apply_constraints_and_penalties" in content:
                print("   ✅ _apply_constraints_and_penalties() - Contraintes et pénalités")
                
            # Analyser les valeurs de pénalité
            if "1e6" in content:
                print("   💰 Pénalité forte: 1e6 (échec de simulation)")
                
            if "0.1" in content and "deficit" in content:
                print("   📏 Pénalité pression: 10% du coût par mètre de déficit")
                
            if "0.05" in content and "excess" in content:
                print("   🏃 Pénalité vitesse: 5% du coût par m/s d'excès")

def test_fitness_improvement():
    """Teste l'amélioration de la fonction d'évaluation."""
    
    print("\n🧪 TEST D'AMÉLIORATION DE LA FONCTION D'ÉVALUATION")
    print("=" * 60)
    
    input_file = "bismark_inp.inp"
    
    if not Path(input_file).exists():
        print(f"❌ Fichier d'entrée non trouvé: {input_file}")
        return
    
    # Test avec paramètres d'optimisation plus stricts
    test_configs = [
        {
            "name": "Paramètres Standard",
            "generations": 15,
            "population": 25,
            "pressure_min": 15.0,
            "velocity_max": 2.0
        },
        {
            "name": "Paramètres Améliorés (Plus de Générations)",
            "generations": 30,
            "population": 50,
            "pressure_min": 15.0,
            "velocity_max": 2.0
        },
        {
            "name": "Paramètres Très Stricts",
            "generations": 50,
            "population": 100,
            "pressure_min": 15.0,
            "velocity_max": 2.0
        }
    ]
    
    results = []
    
    for config in test_configs:
        print(f"\n🎯 Test: {config['name']}")
        print(f"   Générations: {config['generations']}")
        print(f"   Population: {config['population']}")
        print(f"   Pression min: {config['pressure_min']} m")
        print(f"   Vitesse max: {config['velocity_max']} m/s")
        
        # Exécuter l'optimisation LCPI
        output_file = f"fitness_test_{config['generations']}_{config['population']}"
        
        cmd = [
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
            input_file,
            "--method", "genetic",
            "--generations", str(config['generations']),
            "--population", str(config['population']),
            "--solver", "lcpi",
            "--pression-min", str(config['pressure_min']),
            "--vitesse-max", str(config['velocity_max']),
            "--show-stats",
            "--output", output_file,
            "--no-log"
        ]
        
        try:
            # Forcer l'encodage UTF-8
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', env=env)
            
            # Analyser les résultats
            result_file = Path(f"{output_file}.json")
            if result_file.exists():
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                proposals = data.get("proposals", [])
                if proposals:
                    best = proposals[0]
                    capex = best.get("CAPEX", 0)
                    feasible = best.get("constraints_ok", False)
                    
                    print(f"   💰 Coût: {capex:,.0f} FCFA")
                    print(f"   ✅ Faisable: {'Oui' if feasible else 'Non'}")
                    
                    results.append({
                        "config": config,
                        "capex": capex,
                        "feasible": feasible
                    })
                else:
                    print("   ❌ Aucune proposition trouvée")
            else:
                print("   ❌ Fichier de résultats non trouvé")
                
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erreur d'exécution: {e}")
    
    return results

def analyze_results_comparison(results: List[Dict[str, Any]]):
    """Analyse la comparaison des résultats."""
    
    print("\n📊 ANALYSE COMPARATIVE DES RÉSULTATS")
    print("=" * 60)
    
    if not results:
        print("❌ Aucun résultat à analyser")
        return
    
    print("\n📈 COMPARAISON DES CONFIGURATIONS:")
    
    for i, result in enumerate(results):
        config = result["config"]
        capex = result["capex"]
        feasible = result["feasible"]
        
        print(f"\n{i+1}. {config['name']}:")
        print(f"   💰 Coût: {capex:,.0f} FCFA")
        print(f"   ✅ Faisable: {'Oui' if feasible else 'Non'}")
        print(f"   ⚙️  Paramètres: G={config['generations']}, P={config['population']}")
    
    # Analyser l'impact des paramètres
    feasible_results = [r for r in results if r["feasible"]]
    infeasible_results = [r for r in results if not r["feasible"]]
    
    print(f"\n📊 STATISTIQUES:")
    print(f"   Solutions faisables: {len(feasible_results)}/{len(results)}")
    print(f"   Solutions non faisables: {len(infeasible_results)}/{len(results)}")
    
    if feasible_results:
        min_cost_feasible = min(r["capex"] for r in feasible_results)
        print(f"   💰 Coût minimum (faisable): {min_cost_feasible:,.0f} FCFA")
    
    if infeasible_results:
        min_cost_infeasible = min(r["capex"] for r in infeasible_results)
        print(f"   💰 Coût minimum (non faisable): {min_cost_infeasible:,.0f} FCFA")

def generate_improvement_recommendations():
    """Génère des recommandations d'amélioration."""
    
    print("\n💡 RECOMMANDATIONS D'AMÉLIORATION")
    print("=" * 60)
    
    recommendations = [
        {
            "category": "Paramètres d'Optimisation",
            "items": [
                "Augmenter le nombre de générations (30-50 au lieu de 15)",
                "Augmenter la taille de population (50-100 au lieu de 25)",
                "Ajuster les taux de mutation et de croisement"
            ]
        },
        {
            "category": "Fonction d'Évaluation",
            "items": [
                "Renforcer les pénalités pour violations de contraintes",
                "Implémenter des pénalités progressives (plus fortes avec le temps)",
                "Ajouter des pénalités pour solutions non faisables"
            ]
        },
        {
            "category": "Contraintes Hydrauliques",
            "items": [
                "Harmoniser précisément les contraintes avec EPANET",
                "Vérifier les seuils de pression et vitesse",
                "Implémenter des contraintes de robustesse"
            ]
        },
        {
            "category": "Exploration de l'Espace de Solutions",
            "items": [
                "Forcer l'exploration des grands diamètres si nécessaire",
                "Implémenter des opérateurs génétiques spécialisés",
                "Ajouter des mécanismes de diversification"
            ]
        }
    ]
    
    for rec in recommendations:
        print(f"\n📋 {rec['category']}:")
        for item in rec['items']:
            print(f"   • {item}")

def main():
    """Fonction principale."""
    
    print("🔧 ANALYSE ET AMÉLIORATION DE LA FONCTION D'ÉVALUATION LCPI")
    print("=" * 80)
    print("Objectif: Améliorer la capacité de LCPI à trouver des solutions faisables")
    
    # 1. Analyser la fonction actuelle
    analyze_current_fitness_function()
    
    # 2. Tester les améliorations
    results = test_fitness_improvement()
    
    # 3. Analyser les résultats
    analyze_results_comparison(results)
    
    # 4. Générer les recommandations
    generate_improvement_recommendations()
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Implémenter les recommandations d'amélioration")
    print("2. Tester avec des paramètres optimisés")
    print("3. Comparer avec EPANET sur des solutions faisables")
    print("4. Documenter les améliorations apportées")

if __name__ == "__main__":
    main()
