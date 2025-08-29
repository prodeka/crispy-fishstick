#!/usr/bin/env python3
"""
Script d'analyse détaillée des résultats du comparateur EPANET vs LCPI.
Analyse les diamètres utilisés par chaque solveur et identifie les conduites problématiques.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3

def load_json_results(file_path: str) -> Dict[str, Any]:
    """Charge les résultats JSON du comparateur."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {file_path}: {e}")
        return {}

def get_diameter_price(dn_mm: int, material: str = "PVC-U") -> Optional[float]:
    """Obtient le prix d'un diamètre depuis la base de données."""
    try:
        db_path = Path("src/lcpi/db/aep_prices.db")
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT total_fcfa_per_m FROM diameters WHERE dn_mm=? AND material=? LIMIT 1",
                (dn_mm, material)
            )
            result = cur.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"⚠️  Erreur lors de la lecture du prix DN {dn_mm}: {e}")
        return None

def analyze_diameter_distribution(diameters: Dict[str, int], solver_name: str) -> Dict[str, Any]:
    """Analyse la distribution des diamètres pour un solveur."""
    if not diameters:
        return {"error": "Aucun diamètre trouvé"}
    
    # Compter les occurrences de chaque diamètre
    diameter_counts = {}
    for pipe_id, diameter in diameters.items():
        diameter_counts[diameter] = diameter_counts.get(diameter, 0) + 1
    
    # Trier par diamètre
    sorted_diameters = sorted(diameter_counts.items())
    
    # Identifier les grands diamètres (>= 500 mm)
    large_diameters = {d: count for d, count in sorted_diameters if d >= 500}
    
    # Calculer les statistiques
    total_pipes = len(diameters)
    total_large_pipes = sum(large_diameters.values())
    
    # Calculer le coût total estimé
    total_cost = 0
    cost_by_diameter = {}
    
    for diameter, count in sorted_diameters:
        price_per_m = get_diameter_price(diameter)
        if price_per_m:
            # Estimation basée sur une longueur moyenne de 100m par conduite
            estimated_length = 100  # m
            cost_for_diameter = price_per_m * estimated_length * count
            total_cost += cost_for_diameter
            cost_by_diameter[diameter] = {
                "count": count,
                "price_per_m": price_per_m,
                "estimated_cost": cost_for_diameter
            }
    
    return {
        "solver": solver_name,
        "total_pipes": total_pipes,
        "diameter_distribution": sorted_diameters,
        "large_diameters": large_diameters,
        "large_diameters_percentage": (total_large_pipes / total_pipes * 100) if total_pipes > 0 else 0,
        "estimated_total_cost": total_cost,
        "cost_by_diameter": cost_by_diameter
    }

def identify_problematic_pipes(diameters: Dict[str, int], threshold_mm: int = 500) -> List[Dict[str, Any]]:
    """Identifie les conduites qui utilisent des diamètres problématiques."""
    problematic = []
    
    for pipe_id, diameter in diameters.items():
        if diameter >= threshold_mm:
            price_per_m = get_diameter_price(diameter)
            problematic.append({
                "pipe_id": pipe_id,
                "diameter_mm": diameter,
                "price_per_m": price_per_m,
                "estimated_cost_100m": price_per_m * 100 if price_per_m else None
            })
    
    # Trier par diamètre décroissant
    return sorted(problematic, key=lambda x: x["diameter_mm"], reverse=True)

def analyze_results(results_file: str):
    """Analyse complète des résultats du comparateur."""
    print(f"🔍 Analyse détaillée de {results_file}")
    print("=" * 80)
    
    results = load_json_results(results_file)
    if not results:
        return
    
    # Extraire les données des solveurs
    epanet_data = results.get("epanet", {})
    lcpi_data = results.get("lcpi", {})
    
    print("\n📊 ANALYSE DES DIAMÈTRES PAR SOLVEUR")
    print("-" * 50)
    
    # Analyser EPANET
    if epanet_data:
        epanet_diameters = epanet_data.get("diameters_mm", {})
        epanet_analysis = analyze_diameter_distribution(epanet_diameters, "EPANET")
        
        print(f"\n🎯 EPANET:")
        print(f"   Total conduites: {epanet_analysis['total_pipes']}")
        print(f"   Conduites grands diamètres (≥500mm): {epanet_analysis['large_diameters_percentage']:.1f}%")
        print(f"   Coût total estimé: {epanet_analysis['estimated_total_cost']:,.0f} FCFA")
        
        if epanet_analysis['large_diameters']:
            print(f"   Grands diamètres utilisés:")
            for diameter, count in epanet_analysis['large_diameters'].items():
                price = epanet_analysis['cost_by_diameter'][diameter]['price_per_m']
                print(f"     DN {diameter}mm: {count} conduites, {price:,.0f} FCFA/m")
    
    # Analyser LCPI
    if lcpi_data:
        lcpi_diameters = lcpi_data.get("diameters_mm", {})
        lcpi_analysis = analyze_diameter_distribution(lcpi_diameters, "LCPI")
        
        print(f"\n🔧 LCPI:")
        print(f"   Total conduites: {lcpi_analysis['total_pipes']}")
        print(f"   Conduites grands diamètres (≥500mm): {lcpi_analysis['large_diameters_percentage']:.1f}%")
        print(f"   Coût total estimé: {lcpi_analysis['estimated_total_cost']:,.0f} FCFA")
        
        if lcpi_analysis['large_diameters']:
            print(f"   Grands diamètres utilisés:")
            for diameter, count in lcpi_analysis['large_diameters'].items():
                price = lcpi_analysis['cost_by_diameter'][diameter]['price_per_m']
                print(f"     DN {diameter}mm: {count} conduites, {price:,.0f} FCFA/m")
    
    print("\n🚨 CONDUITES PROBLÉMATIQUES (≥500mm)")
    print("-" * 50)
    
    # Identifier les conduites problématiques pour EPANET
    if epanet_data:
        epanet_problematic = identify_problematic_pipes(epanet_data.get("diameters_mm", {}))
        if epanet_problematic:
            print(f"\n🎯 EPANET - Conduites avec grands diamètres:")
            for pipe in epanet_problematic:
                print(f"   {pipe['pipe_id']}: DN {pipe['diameter_mm']}mm, "
                      f"{pipe['price_per_m']:,.0f} FCFA/m, "
                      f"Coût estimé: {pipe['estimated_cost_100m']:,.0f} FCFA")
        else:
            print("   Aucune conduite problématique trouvée")
    
    # Identifier les conduites problématiques pour LCPI
    if lcpi_data:
        lcpi_problematic = identify_problematic_pipes(lcpi_data.get("diameters_mm", {}))
        if lcpi_problematic:
            print(f"\n🔧 LCPI - Conduites avec grands diamètres:")
            for pipe in lcpi_problematic:
                print(f"   {pipe['pipe_id']}: DN {pipe['diameter_mm']}mm, "
                      f"{pipe['price_per_m']:,.0f} FCFA/m, "
                      f"Coût estimé: {pipe['estimated_cost_100m']:,.0f} FCFA")
        else:
            print("   Aucune conduite problématique trouvée")
    
    print("\n📈 COMPARAISON DES COÛTS")
    print("-" * 30)
    
    if epanet_data and lcpi_data:
        epanet_cost = epanet_analysis.get('estimated_total_cost', 0)
        lcpi_cost = lcpi_analysis.get('estimated_total_cost', 0)
        
        if epanet_cost > 0 and lcpi_cost > 0:
            difference = lcpi_cost - epanet_cost
            percentage_diff = (difference / epanet_cost) * 100
            
            print(f"   Coût EPANET estimé: {epanet_cost:,.0f} FCFA")
            print(f"   Coût LCPI estimé: {lcpi_cost:,.0f} FCFA")
            print(f"   Différence: {difference:+,.0f} FCFA ({percentage_diff:+.1f}%)")
            
            if percentage_diff < -50:
                print(f"   ⚠️  Écart important détecté! LCPI est {abs(percentage_diff):.1f}% moins cher")
            elif percentage_diff > 50:
                print(f"   ⚠️  Écart important détecté! LCPI est {percentage_diff:.1f}% plus cher")
            else:
                print(f"   ✅ Écart acceptable entre les solveurs")

def main():
    """Fonction principale."""
    if len(sys.argv) != 2:
        print("Usage: python analyze_detailed_results.py <results_file.json>")
        print("Exemple: python analyze_detailed_results.py results/comparison_results.json")
        sys.exit(1)
    
    results_file = sys.argv[1]
    
    if not Path(results_file).exists():
        print(f"❌ Fichier non trouvé: {results_file}")
        sys.exit(1)
    
    analyze_results(results_file)

if __name__ == "__main__":
    main()
