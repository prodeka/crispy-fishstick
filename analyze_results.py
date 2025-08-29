#!/usr/bin/env python3
"""
Script d'analyse des résultats de comparaison des solveurs
"""

import json
from pathlib import Path

def analyze_solver_results(filename: str, solver_name: str):
    """Analyse les résultats d'un solveur spécifique."""
    print(f"\n🔍 ANALYSE {solver_name.upper()}")
    print("=" * 50)
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Informations de base
        meta = data.get("meta", {})
        best_proposal = data.get("proposals", [{}])[0]
        
        print(f"Coût total: {meta.get('best_cost', 0):,.0f} FCFA")
        print(f"Faisabilité: {meta.get('best_constraints_ok', 'N/A')}")
        print(f"Hauteur réservoir: {best_proposal.get('H_tank_m', 'N/A'):.2f} m")
        
        # Analyse des diamètres
        diameters = best_proposal.get("diameters_mm", {})
        if diameters:
            diameter_values = list(diameters.values())
            unique_diameters = sorted(set(diameter_values))
            
            print(f"\n📏 ANALYSE DES DIAMÈTRES:")
            print(f"Nombre de conduites: {len(diameters)}")
            print(f"Plage: {min(diameter_values)}-{max(diameter_values)} mm")
            print(f"Diamètres uniques: {unique_diameters}")
            
            # Distribution des diamètres
            print(f"\n📊 DISTRIBUTION:")
            for diam in unique_diameters:
                count = diameter_values.count(diam)
                percentage = (count / len(diameter_values)) * 100
                print(f"  DN {diam} mm: {count} conduites ({percentage:.1f}%)")
        
        # Informations sur la base de prix
        price_db = meta.get("price_db_info", {})
        if price_db:
            print(f"\n💰 BASE DE PRIX:")
            print(f"Chemin: {price_db.get('path', 'N/A')}")
            print(f"Checksum: {price_db.get('checksum', 'N/A')[:16]}...")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de {filename}: {e}")

def main():
    """Fonction principale d'analyse."""
    print("🚀 ANALYSE DES RÉSULTATS DE COMPARAISON DES SOLVEURS")
    print("=" * 70)
    
    # Analyser les résultats EPANET
    epanet_file = "test_lcpi_enhanced_comparison_epanet"
    if Path(epanet_file).exists():
        analyze_solver_results(epanet_file, "EPANET")
    else:
        print(f"❌ Fichier {epanet_file} non trouvé")
    
    # Analyser les résultats LCPI
    lcpi_file = "test_lcpi_enhanced_comparison_lcpi"
    if Path(lcpi_file).exists():
        analyze_solver_results(lcpi_file, "LCPI")
    else:
        print(f"❌ Fichier {lcpi_file} non trouvé")
    
    # Lire le rapport de comparaison
    compare_file = "test_lcpi_enhanced_comparison_compare_report.txt"
    if Path(compare_file).exists():
        print(f"\n📋 RAPPORT DE COMPARAISON")
        print("=" * 50)
        with open(compare_file, 'r') as f:
            print(f.read())
    else:
        print(f"❌ Fichier {compare_file} non trouvé")

if __name__ == "__main__":
    main()
