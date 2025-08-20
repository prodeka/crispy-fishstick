#!/usr/bin/env python3
"""
Script de test final pour vérifier que toutes les corrections ont bien fonctionné
"""

import json
from pathlib import Path

def test_corrections():
    """Teste que toutes les corrections ont bien fonctionné"""
    
    print("🔍 TEST FINAL DES CORRECTIONS")
    print("=" * 60)
    
    # Test 1: Vérifier l'ordre des propositions
    print("\n📊 Test 1: Ordre des propositions")
    test_file = Path("results/test_tri.json")
    
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        proposals = data.get("proposals", [])
        if len(proposals) >= 3:
            # Vérifier que les coûts sont dans l'ordre croissant
            capex_values = [prop.get("CAPEX", 0) for prop in proposals]
            sorted_capex = sorted(capex_values)
            
            if capex_values == sorted_capex:
                print("✅ Ordre des coûts correct (croissant)")
            else:
                print("❌ Ordre des coûts incorrect")
                print(f"   Actuel: {[f'{c:,.0f}' for c in capex_values]}")
                print(f"   Attendu: {[f'{c:,.0f}' for c in sorted_capex]}")
            
            # Vérifier que les propositions valides sont en premier
            valid_first = all(
                proposals[i].get("constraints_ok", False) >= proposals[i+1].get("constraints_ok", False)
                for i in range(len(proposals) - 1)
            )
            
            if valid_first:
                print("✅ Propositions valides en premier")
            else:
                print("❌ Propositions valides pas en premier")
        else:
            print("⚠️  Pas assez de propositions pour tester")
    
    # Test 2: Vérifier les variations de diamètres
    print("\n🔧 Test 2: Variations de diamètres")
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        proposals = data.get("proposals", [])
        if len(proposals) >= 2:
            base_diameters = proposals[0].get("diameters_mm", {})
            variation_diameters = proposals[1].get("diameters_mm", {})
            
            if base_diameters and variation_diameters:
                # Compter les diamètres différents
                different_count = 0
                for pipe_id in base_diameters:
                    if pipe_id in variation_diameters:
                        if base_diameters[pipe_id] != variation_diameters[pipe_id]:
                            different_count += 1
                
                if different_count >= 3:
                    print(f"✅ Nombre de variations suffisant ({different_count} ≥ 3)")
                else:
                    print(f"⚠️  Nombre de variations insuffisant ({different_count} < 3)")
            else:
                print("❌ Diamètres manquants")
        else:
            print("⚠️  Pas assez de propositions pour tester")
    
    # Test 3: Vérifier les métadonnées des solveurs
    print("\n🏷️  Test 3: Métadonnées des solveurs")
    
    # Test mono-solveur
    mono_file = Path("results/test_tri.json")
    if mono_file.exists():
        with open(mono_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        solver = data.get("meta", {}).get("solver", "")
        expected_solver = "epanet"
        
        if solver == expected_solver:
            print(f"✅ Mono-solveur: {solver}")
        else:
            print(f"❌ Mono-solveur: attendu {expected_solver}, trouvé {solver}")
    
    # Test 4: Vérifier la cohérence des coûts
    print("\n💰 Test 4: Cohérence des coûts")
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        proposals = data.get("proposals", [])
        if len(proposals) >= 2:
            capex_values = [prop.get("CAPEX", 0) for prop in proposals]
            cost_range = max(capex_values) - min(capex_values)
            cost_ratio = max(capex_values) / min(capex_values) if min(capex_values) > 0 else 0
            
            print(f"   - Plage de coûts: {cost_range:,.2f} FCFA")
            print(f"   - Ratio max/min: {cost_ratio:.2f}")
            
            if cost_ratio > 10:
                print("   ⚠️  Ratio de coût très élevé (>10)")
            elif cost_ratio > 5:
                print("   ⚠️  Ratio de coût élevé (>5)")
            else:
                print("   ✅ Ratio de coût raisonnable")
        else:
            print("⚠️  Pas assez de propositions pour tester")
    
    # Test 5: Vérifier la qualité des propositions
    print("\n🎯 Test 5: Qualité des propositions")
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        proposals = data.get("proposals", [])
        if proposals:
            valid_props = [prop for prop in proposals if prop.get("constraints_ok", False)]
            invalid_props = [prop for prop in proposals if not prop.get("constraints_ok", False)]
            
            print(f"   - Total: {len(proposals)}")
            print(f"   - Valides: {len(valid_props)}")
            print(f"   - Invalides: {len(invalid_props)}")
            
            if len(valid_props) >= len(proposals) // 2:
                print("   ✅ Majorité des propositions valides")
            else:
                print("   ⚠️  Moins de la moitié des propositions sont valides")
        else:
            print("❌ Aucune proposition trouvée")
    
    print("\n" + "=" * 60)
    print("🎯 TEST TERMINÉ")

if __name__ == "__main__":
    test_corrections()
