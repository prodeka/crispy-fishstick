#!/usr/bin/env python3
"""Script pour vérifier les diamètres candidats utilisés par LCPI."""

import sys
sys.path.insert(0, 'src')

from lcpi.aep.optimizer.db_dao import get_candidate_diameters

def main():
    print("🔍 Vérification des diamètres candidats LCPI")
    print("=" * 50)
    
    # Obtenir tous les diamètres candidats
    candidates = get_candidate_diameters('PVC-U')
    
    print(f"Total diamètres candidats: {len(candidates)}")
    print("\nPremiers 15 diamètres:")
    for i, candidate in enumerate(candidates[:15]):
        print(f"  {i+1:2d}. DN {candidate['d_mm']:3d}mm: {candidate['cost_per_m']:8,.0f} FCFA/m")
    
    print(f"\nDerniers 10 diamètres:")
    for i, candidate in enumerate(candidates[-10:]):
        print(f"  {len(candidates)-9+i:2d}. DN {candidate['d_mm']:3d}mm: {candidate['cost_per_m']:8,.0f} FCFA/m")
    
    # Vérifier si les grands diamètres sont présents
    large_diameters = [c for c in candidates if c['d_mm'] >= 500]
    print(f"\nGrands diamètres (≥500mm): {len(large_diameters)}")
    for candidate in large_diameters:
        print(f"  DN {candidate['d_mm']:3d}mm: {candidate['cost_per_m']:8,.0f} FCFA/m")

if __name__ == "__main__":
    main()
