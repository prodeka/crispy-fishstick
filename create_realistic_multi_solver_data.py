#!/usr/bin/env python3
"""
Script pour créer des données multi-solveurs réalistes avec des différences entre EPANET et LCPI
"""

import json
import random
from pathlib import Path
from datetime import datetime

def create_realistic_solver_data(solver_name, base_capex, base_pressure):
    """Crée des données réalistes pour un solveur spécifique"""
    
    # Variations réalistes entre solveurs
    if solver_name == "epanet":
        # EPANET tend à être plus conservateur
        capex_variation = random.uniform(0.95, 1.05)  # ±5%
        pressure_variation = random.uniform(0.98, 1.02)  # ±2%
        efficiency_factor = 0.92  # EPANET moins efficace
    else:  # lcpi
        # LCPI tend à être plus optimisé
        capex_variation = random.uniform(0.88, 0.98)  # -12% à -2%
        pressure_variation = random.uniform(1.02, 1.08)  # +2% à +8%
        efficiency_factor = 1.08  # LCPI plus efficace
    
    # Créer plusieurs propositions avec variations
    proposals = []
    for i in range(5):
        # Variation progressive
        progress_factor = 1 + (i * 0.1)  # Chaque proposition est 10% plus chère
        
        capex = base_capex * capex_variation * progress_factor
        min_pressure = base_pressure * pressure_variation * (1 + random.uniform(-0.05, 0.05))
        max_pressure = min_pressure * random.uniform(1.2, 1.5)
        max_velocity = random.uniform(1.8, 2.2)
        
        proposal = {
            "CAPEX": round(capex, 2),
            "min_pressure_m": round(min_pressure, 3),
            "max_pressure_m": round(max_pressure, 3),
            "max_velocity_ms": round(max_velocity, 2),
            "efficiency_score": round(efficiency_factor * random.uniform(0.9, 1.1), 3),
            "diameter_optimization": round(random.uniform(0.85, 0.95), 3),
            "pressure_distribution": round(random.uniform(0.88, 0.98), 3),
            "velocity_distribution": round(random.uniform(0.92, 0.99), 3),
            "total_length_m": round(random.uniform(8500, 9500), 1),
            "avg_diameter_mm": round(random.uniform(120, 180), 1),
            "pipe_count": random.randint(180, 220),
            "junction_count": random.randint(190, 210),
            "tank_count": 3,
            "pump_count": 0,
            "valve_count": 0
        }
        
        # Ajouter des métriques spécifiques au solveur
        if solver_name == "epanet":
            proposal["epanet_specific"] = {
                "headloss_model": "Hazen-Williams",
                "convergence_iterations": random.randint(15, 25),
                "hydraulic_accuracy": round(random.uniform(0.001, 0.005), 4)
            }
        else:  # lcpi
            proposal["lcpi_specific"] = {
                "optimization_algorithm": "Genetic Algorithm",
                "generations": random.randint(50, 100),
                "population_size": random.randint(20, 50),
                "mutation_rate": round(random.uniform(0.05, 0.15), 3),
                "crossover_rate": round(random.uniform(0.7, 0.9), 3)
            }
        
        proposals.append(proposal)
    
    # Trier par CAPEX croissant
    proposals.sort(key=lambda x: x["CAPEX"])
    
    return {
        "meta": {
            "solver": solver_name,
            "method": "genetic",
            "input_file": "src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp",
            "constraints": {
                "min_pressure_m": 12.0,
                "max_velocity_ms": 2.0
            },
            "generation_date": datetime.now().isoformat(),
            "execution_time_seconds": random.randint(45, 120)
        },
        "proposals": proposals,
        "best_proposal": proposals[0],
        "statistics": {
            "total_proposals": len(proposals),
            "avg_capex": round(sum(p["CAPEX"] for p in proposals) / len(proposals), 2),
            "min_capex": proposals[0]["CAPEX"],
            "max_capex": proposals[-1]["CAPEX"],
            "avg_pressure": round(sum(p["min_pressure_m"] for p in proposals) / len(proposals), 3),
            "avg_velocity": round(sum(p["max_velocity_ms"] for p in proposals) / len(proposals), 2)
        }
    }

def create_multi_solver_metadata():
    """Crée le fichier de métadonnées multi-solveurs"""
    
    return {
        "meta": {
            "solvers": ["epanet", "lcpi"],
            "method": "genetic",
            "input_file": "src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp",
            "constraints": {
                "min_pressure_m": 12.0,
                "max_velocity_ms": 2.0
            },
            "generation_date": datetime.now().isoformat(),
            "comparison_metrics": [
                "CAPEX",
                "min_pressure_m", 
                "max_pressure_m",
                "max_velocity_ms",
                "efficiency_score"
            ]
        },
        "results": {
            "epanet": "results/out_multi_epanet_realistic.json",
            "lcpi": "results/out_multi_lcpi_realistic.json"
        }
    }

def main():
    """Fonction principale"""
    
    print("🔧 Création de données multi-solveurs réalistes")
    print("=" * 60)
    
    # Valeurs de base pour Bismark
    base_capex = 1250000  # 1.25M euros
    base_pressure = 15.5  # 15.5 m
    
    # Créer les répertoires si nécessaire
    Path("results").mkdir(exist_ok=True)
    
    # Générer les données pour chaque solveur
    solvers = ["epanet", "lcpi"]
    
    for solver in solvers:
        print(f"🔄 Génération des données pour {solver.upper()}...")
        
        data = create_realistic_solver_data(solver, base_capex, base_pressure)
        
        output_file = f"results/out_multi_{solver}_realistic.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        best = data["best_proposal"]
        print(f"✅ {solver.upper()} généré:")
        print(f"   CAPEX: {best['CAPEX']:,} €")
        print(f"   Pression min: {best['min_pressure_m']} m")
        print(f"   Vitesse max: {best['max_velocity_ms']} m/s")
        print(f"   Fichier: {output_file}")
        print()
    
    # Créer le fichier de métadonnées multi-solveurs
    print("🔄 Création du fichier multi-solveurs...")
    multi_data = create_multi_solver_metadata()
    
    multi_file = "results/out_multi_multi_realistic.json"
    with open(multi_file, 'w', encoding='utf-8') as f:
        json.dump(multi_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fichier multi-solveurs créé: {multi_file}")
    
    # Afficher un résumé de comparaison
    print("\n📊 Résumé de comparaison:")
    print("=" * 60)
    
    epanet_data = None
    lcpi_data = None
    
    with open("results/out_multi_epanet_realistic.json", 'r') as f:
        epanet_data = json.load(f)
    with open("results/out_multi_lcpi_realistic.json", 'r') as f:
        lcpi_data = json.load(f)
    
    epanet_best = epanet_data["best_proposal"]
    lcpi_best = lcpi_data["best_proposal"]
    
    print(f"EPANET  - CAPEX: {epanet_best['CAPEX']:,} € | Pression: {epanet_best['min_pressure_m']} m")
    print(f"LCPI    - CAPEX: {lcpi_best['CAPEX']:,} € | Pression: {lcpi_best['min_pressure_m']} m")
    
    capex_diff = lcpi_best['CAPEX'] - epanet_best['CAPEX']
    capex_diff_pct = (capex_diff / epanet_best['CAPEX']) * 100
    
    print(f"\nDifférence CAPEX: {capex_diff:+,.0f} € ({capex_diff_pct:+.1f}%)")
    
    if capex_diff < 0:
        print("✅ LCPI est plus économique")
    else:
        print("✅ EPANET est plus économique")
    
    print(f"\n🎯 Prochaines étapes:")
    print(f"1. Tester le rapport: python test_multi_solver_report.py")
    print(f"2. Générer le rapport HTML avec les nouvelles données")
    print(f"3. Vérifier que les différences sont bien visibles")

if __name__ == "__main__":
    main()
