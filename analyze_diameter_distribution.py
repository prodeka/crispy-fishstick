#!/usr/bin/env python3
"""
Script pour analyser la distribution détaillée des diamètres utilisés par EPANET et LCPI.
"""

import json
import sys
from collections import Counter
from pathlib import Path

def analyze_diameter_distribution(diameters_dict, solver_name):
    """Analyse la distribution des diamètres pour un solveur."""
    if not diameters_dict:
        print(f"❌ Aucun diamètre trouvé pour {solver_name}")
        return
    
    # Compter les occurrences de chaque diamètre
    diameter_counts = Counter(diameters_dict.values())
    
    # Trier par diamètre
    sorted_diameters = sorted(diameter_counts.items())
    
    print(f"\n📊 DISTRIBUTION DES DIAMÈTRES - {solver_name}")
    print("=" * 60)
    print(f"Total conduites: {len(diameters_dict)}")
    
    # Grouper par plages de diamètres
    ranges = {
        "Très petits (≤100mm)": [],
        "Petits (110-200mm)": [],
        "Moyens (225-350mm)": [],
        "Grands (400-500mm)": [],
        "Très grands (≥500mm)": []
    }
    
    for diameter, count in sorted_diameters:
        if diameter <= 100:
            ranges["Très petits (≤100mm)"].append((diameter, count))
        elif diameter <= 200:
            ranges["Petits (110-200mm)"].append((diameter, count))
        elif diameter <= 350:
            ranges["Moyens (225-350mm)"].append((diameter, count))
        elif diameter <= 500:
            ranges["Grands (400-500mm)"].append((diameter, count))
        else:
            ranges["Très grands (≥500mm)"].append((diameter, count))
    
    # Afficher par plages
    for range_name, diameters in ranges.items():
        if diameters:
            total_in_range = sum(count for _, count in diameters)
            percentage = (total_in_range / len(diameters_dict)) * 100
            print(f"\n{range_name}: {total_in_range} conduites ({percentage:.1f}%)")
            
            # Afficher les diamètres dans cette plage
            for diameter, count in diameters:
                print(f"  DN {diameter:3d}mm: {count:3d} conduites")
    
    # Statistiques générales
    diameters_list = list(diameters_dict.values())
    print(f"\n📈 STATISTIQUES GÉNÉRALES:")
    print(f"  Diamètre minimum: {min(diameters_list)} mm")
    print(f"  Diamètre maximum: {max(diameters_list)} mm")
    print(f"  Diamètre moyen: {sum(diameters_list) / len(diameters_list):.1f} mm")
    print(f"  Diamètre médian: {sorted(diameters_list)[len(diameters_list)//2]} mm")
    
    # Diamètres les plus utilisés
    most_common = diameter_counts.most_common(5)
    print(f"\n🏆 DIAMÈTRES LES PLUS UTILISÉS:")
    for diameter, count in most_common:
        percentage = (count / len(diameters_dict)) * 100
        print(f"  DN {diameter:3d}mm: {count:3d} conduites ({percentage:.1f}%)")

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_diameter_distribution.py <results_file.json>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    
    if not Path(results_file).exists():
        print(f"❌ Fichier non trouvé: {results_file}")
        sys.exit(1)
    
    # Charger les résultats
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Analyser EPANET
    epanet_diameters = results.get("epanet", {}).get("diameters", {})
    analyze_diameter_distribution(epanet_diameters, "EPANET")
    
    # Analyser LCPI
    lcpi_diameters = results.get("lcpi", {}).get("diameters", {})
    analyze_diameter_distribution(lcpi_diameters, "LCPI")
    
    # Comparaison
    print(f"\n🔍 COMPARAISON DES STRATÉGIES")
    print("=" * 60)
    
    epanet_diams = list(epanet_diameters.values())
    lcpi_diams = list(lcpi_diameters.values())
    
    print(f"EPANET - Diamètre moyen: {sum(epanet_diams) / len(epanet_diams):.1f} mm")
    print(f"LCPI   - Diamètre moyen: {sum(lcpi_diams) / len(lcpi_diams):.1f} mm")
    
    epanet_large = sum(1 for d in epanet_diams if d >= 400)
    lcpi_large = sum(1 for d in lcpi_diams if d >= 400)
    
    print(f"EPANET - Conduites ≥400mm: {epanet_large} ({epanet_large/len(epanet_diams)*100:.1f}%)")
    print(f"LCPI   - Conduites ≥400mm: {lcpi_large} ({lcpi_large/len(lcpi_diams)*100:.1f}%)")

if __name__ == "__main__":
    main()
