#!/usr/bin/env python3
"""
Script pour tester l'optimisation avec des contraintes harmonisées entre EPANET et LCPI.
"""

import subprocess
import sys
import json
import os
from pathlib import Path

def run_optimization_with_constraints(input_file, solver, pressure_min=15.0, velocity_max=2.0, generations=15, population=30):
    """Exécute l'optimisation avec des contraintes spécifiques."""
    
    output_file = f"harmonized_{solver}"
    
    cmd = [
        sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
        input_file,
        "--method", "genetic",
        "--generations", str(generations),
        "--population", str(population),
        "--solver", solver,
        "--pression-min", str(pressure_min),
        "--vitesse-max", str(velocity_max),
        "--show-stats",
        "--output", output_file,
        "--no-log"
    ]
    
    print(f"\n🔄 Exécution {solver.upper()} avec contraintes harmonisées:")
    print(f"   Pression min: {pressure_min} m")
    print(f"   Vitesse max: {velocity_max} m/s")
    print(f"   Générations: {generations}")
    print(f"   Population: {population}")
    
    try:
        # Forcer l'encodage UTF-8 pour le terminal
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', env=env)
        print(f"✅ {solver.upper()} exécuté avec succès")
        return Path(output_file)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de {solver}: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return None

def analyze_results(epanet_file, lcpi_file):
    """Analyse les résultats des deux solveurs."""
    
    if not epanet_file.exists() or not lcpi_file.exists():
        print("❌ Fichiers de résultats manquants")
        return
    
    # Charger les résultats
    with open(epanet_file, 'r', encoding='utf-8') as f:
        epanet_results = json.load(f)
    
    with open(lcpi_file, 'r', encoding='utf-8') as f:
        lcpi_results = json.load(f)
    
    # Extraire les données
    epanet_props = epanet_results.get("proposals", [])
    lcpi_props = lcpi_results.get("proposals", [])
    
    if not epanet_props or not lcpi_props:
        print("❌ Aucune proposition trouvée")
        return
    
    epanet_best = epanet_props[0]
    lcpi_best = lcpi_props[0]
    
    # Analyser les coûts
    epanet_cost = epanet_best.get("CAPEX", 0)
    lcpi_cost = lcpi_best.get("CAPEX", 0)
    
    # Analyser la faisabilité
    epanet_feasible = epanet_best.get("constraints_ok", False)
    lcpi_feasible = lcpi_best.get("constraints_ok", False)
    
    # Analyser les diamètres
    epanet_diameters = epanet_best.get("diameters_mm", {})
    lcpi_diameters = lcpi_best.get("diameters_mm", {})
    
    print(f"\n📊 RÉSULTATS AVEC CONTRAINTES HARMONISÉES")
    print("=" * 60)
    
    print(f"\n💰 COÛTS:")
    print(f"   EPANET: {epanet_cost:,.0f} FCFA")
    print(f"   LCPI  : {lcpi_cost:,.0f} FCFA")
    
    if epanet_cost > 0:
        delta = lcpi_cost - epanet_cost
        delta_percent = (delta / epanet_cost) * 100
        print(f"   Différence: {delta:+,.0f} FCFA ({delta_percent:+.1f}%)")
    
    print(f"\n✅ FAISABILITÉ:")
    print(f"   EPANET: {'✅ Faisable' if epanet_feasible else '❌ Non faisable'}")
    print(f"   LCPI  : {'✅ Faisable' if lcpi_feasible else '❌ Non faisable'}")
    
    # Analyser les diamètres
    if epanet_diameters and lcpi_diameters:
        epanet_diams = list(epanet_diameters.values())
        lcpi_diams = list(lcpi_diameters.values())
        
        print(f"\n🔧 DIAMÈTRES:")
        print(f"   EPANET - Moyen: {sum(epanet_diams)/len(epanet_diams):.1f} mm")
        print(f"   LCPI   - Moyen: {sum(lcpi_diams)/len(lcpi_diams):.1f} mm")
        
        epanet_large = sum(1 for d in epanet_diams if d >= 400)
        lcpi_large = sum(1 for d in lcpi_diams if d >= 400)
        
        print(f"   EPANET - ≥400mm: {epanet_large} conduites")
        print(f"   LCPI   - ≥400mm: {lcpi_large} conduites")

def main():
    """Fonction principale."""
    
    input_file = "bismark_inp.inp"
    
    if not Path(input_file).exists():
        print(f"❌ Fichier d'entrée non trouvé: {input_file}")
        sys.exit(1)
    
    print("🔧 TEST AVEC CONTRAINTES HARMONISÉES")
    print("=" * 60)
    print("Objectif: Comparer EPANET et LCPI avec les mêmes contraintes")
    print("Note: Respect des contraintes Pydantic (g≥10, p≥20)")
    
    # Test avec contraintes plus strictes (respectant Pydantic)
    print(f"\n🎯 Test avec contraintes strictes (pression min: 15m, vitesse max: 2.0 m/s)")
    
    epanet_file = run_optimization_with_constraints(
        input_file, "epanet", 
        pressure_min=15.0, velocity_max=2.0,
        generations=15, population=25
    )
    
    lcpi_file = run_optimization_with_constraints(
        input_file, "lcpi", 
        pressure_min=15.0, velocity_max=2.0,
        generations=15, population=25
    )
    
    if epanet_file and lcpi_file:
        analyze_results(epanet_file, lcpi_file)
    
    # Test avec contraintes plus souples (respectant Pydantic)
    print(f"\n🎯 Test avec contraintes souples (pression min: 8m, vitesse max: 3.0 m/s)")
    
    epanet_file2 = run_optimization_with_constraints(
        input_file, "epanet", 
        pressure_min=8.0, velocity_max=3.0,
        generations=15, population=25
    )
    
    lcpi_file2 = run_optimization_with_constraints(
        input_file, "lcpi", 
        pressure_min=8.0, velocity_max=3.0,
        generations=15, population=25
    )
    
    if epanet_file2 and lcpi_file2:
        analyze_results(epanet_file2, lcpi_file2)

if __name__ == "__main__":
    main()
