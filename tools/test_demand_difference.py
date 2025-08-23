#!/usr/bin/env python3
"""
Test de différence de demande avec des valeurs extrêmes
"""
import subprocess
import json
from pathlib import Path

def run_optimization(demand_value, output_file):
    """Lance une optimisation avec une valeur de demande spécifique"""
    cmd = (
        f'python -m lcpi.aep.cli network-optimize-unified "bismark_inp.inp" '
        f'--method genetic --solver epanet --epanet-backend dll '
        f'--generations 5 --population 10 --demand {demand_value} '
        f'--no-confirm --no-cache --no-surrogate '
        f'--output "{output_file}"'
    )
    
    print(f"Running optimization with demand={demand_value}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {output_file}")
            return True
        else:
            print(f"❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def analyze_result(file_path):
    """Analyse un fichier de résultat"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        meta = data.get('meta', {})
        cost = meta.get('best_cost')
        sim_time = meta.get('sim_time_seconds_total')
        solver_calls = meta.get('solver_calls')
        
        # Extraire les diamètres
        proposals = data.get('proposals', [])
        diameters = {}
        if proposals:
            diameters = proposals[0].get('diameters_mm', {})
        
        return {
            'cost': cost,
            'sim_time': sim_time,
            'solver_calls': solver_calls,
            'diameters_count': len(diameters),
            'diameters_sample': list(diameters.values())[:5] if diameters else []
        }
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def main():
    # Test avec des valeurs très différentes
    tests = [
        (100, "temp/test_demand_100.json"),
        (1000, "temp/test_demand_1000.json"),
        (2000, "temp/test_demand_2000.json")
    ]
    
    results = {}
    
    for demand, output_file in tests:
        if run_optimization(demand, output_file):
            result = analyze_result(output_file)
            if result:
                results[demand] = result
    
    # Analyse comparative
    print("\n" + "="*60)
    print("ANALYSE COMPARATIVE")
    print("="*60)
    
    for demand, result in results.items():
        print(f"\nDemande {demand}:")
        print(f"  Coût: {result['cost']:,} FCFA")
        print(f"  Temps simulation: {result['sim_time']:.2f}s")
        print(f"  Appels solveur: {result['solver_calls']}")
        print(f"  Nombre conduites: {result['diameters_count']}")
        print(f"  Échantillon diamètres: {result['diameters_sample']}")
    
    # Vérification des différences
    costs = [r['cost'] for r in results.values()]
    if len(set(costs)) == 1:
        print(f"\n⚠️  PROBLÈME: Tous les coûts sont identiques ({costs[0]:,} FCFA)")
        print("   Le paramètre --demand ne semble pas fonctionner correctement")
    else:
        print(f"\n✅ SUCCÈS: Les coûts diffèrent entre les scénarios")
        print(f"   Coûts: {costs}")

if __name__ == "__main__":
    main()
