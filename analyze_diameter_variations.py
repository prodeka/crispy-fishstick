#!/usr/bin/env python3
"""
Script d'analyse détaillée des variations de diamètres
entre les propositions générées avec --num-prop
"""

import json
from pathlib import Path

def analyze_diameter_variations():
    """Analyse les variations de diamètres entre les propositions"""
    
    # Analyser le fichier principal
    file_path = Path("results/test_multi_prop.json")
    
    if not file_path.exists():
        print("❌ Fichier test_multi_prop.json non trouvé")
        return
    
    print("🔍 ANALYSE DÉTAILLÉE DES VARIATIONS DE DIAMÈTRES")
    print("=" * 80)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    proposals = data.get("proposals", [])
    
    if len(proposals) < 2:
        print("❌ Pas assez de propositions pour l'analyse")
        return
    
    # Analyser la première proposition (base)
    base_prop = proposals[0]
    base_diameters = base_prop.get("diameters_mm", {})
    base_capex = base_prop.get("CAPEX", 0)
    
    print(f"\n📊 PROPOSITION DE BASE (genetic_best)")
    print(f"   - CAPEX: {base_capex:,.2f} FCFA")
    print(f"   - Contraintes respectées: {'✅' if base_prop.get('constraints_ok') else '❌'}")
    print(f"   - Diamètres: {len(base_diameters)} conduites")
    
    # Analyser chaque variation
    for i in range(1, len(proposals)):
        variation_prop = proposals[i]
        variation_diameters = variation_prop.get("diameters_mm", {})
        variation_capex = variation_prop.get("CAPEX", 0)
        
        print(f"\n🔄 VARIATION {i} ({variation_prop.get('id', 'unknown')})")
        print(f"   - CAPEX: {variation_capex:,.2f} FCFA")
        print(f"   - Différence de coût: {variation_capex - base_capex:,.2f} FCFA")
        print(f"   - Contraintes respectées: {'✅' if variation_prop.get('constraints_ok') else '❌'}")
        
        # Identifier les diamètres modifiés
        modified_diameters = {}
        for pipe_id in base_diameters:
            if pipe_id in variation_diameters:
                base_diam = base_diameters[pipe_id]
                var_diam = variation_diameters[pipe_id]
                
                if base_diam != var_diam:
                    modified_diameters[pipe_id] = {
                        'base': base_diam,
                        'variation': var_diam,
                        'difference': var_diam - base_diam
                    }
        
        print(f"   - Diamètres modifiés: {len(modified_diameters)}")
        
        if modified_diameters:
            print(f"   - Détail des modifications:")
            for pipe_id, changes in list(modified_diameters.items())[:10]:  # Afficher les 10 premiers
                print(f"     {pipe_id}: {changes['base']} → {changes['variation']} ({changes['difference']:+d})")
            
            if len(modified_diameters) > 10:
                print(f"     ... et {len(modified_diameters) - 10} autres modifications")
        
        # Vérifier la cohérence des variations
        if len(modified_diameters) == 0:
            print(f"   ⚠️  ATTENTION: Aucune variation de diamètre détectée!")
        elif len(modified_diameters) < 3:
            print(f"   ⚠️  ATTENTION: Très peu de variations ({len(modified_diameters)} < 3)")
        else:
            print(f"   ✅ Nombre de variations acceptable ({len(modified_diameters)})")
    
    # Analyser la cohérence globale
    print(f"\n🔍 ANALYSE DE COHÉRENCE GLOBALE")
    print("-" * 50)
    
    # Vérifier que les coûts sont dans l'ordre attendu
    capex_values = [prop.get("CAPEX", 0) for prop in proposals]
    sorted_capex = sorted(capex_values)
    
    if capex_values == sorted_capex:
        print("✅ Coûts en ordre croissant (logique)")
    else:
        print("⚠️  Coûts pas en ordre croissant")
        print(f"   Ordre actuel: {[f'{c:,.0f}' for c in capex_values]}")
        print(f"   Ordre attendu: {[f'{c:,.0f}' for c in sorted_capex]}")
    
    # Vérifier la distribution des coûts
    cost_range = max(capex_values) - min(capex_values)
    cost_ratio = max(capex_values) / min(capex_values) if min(capex_values) > 0 else 0
    
    print(f"   - Plage de coûts: {cost_range:,.2f} FCFA")
    print(f"   - Ratio max/min: {cost_ratio:.2f}")
    
    if cost_ratio > 10:
        print("   ⚠️  ATTENTION: Ratio de coût très élevé (>10)")
    elif cost_ratio > 5:
        print("   ⚠️  Ratio de coût élevé (>5)")
    else:
        print("   ✅ Ratio de coût raisonnable")
    
    # Vérifier la cohérence des contraintes
    valid_props = [prop for prop in proposals if prop.get("constraints_ok", False)]
    invalid_props = [prop for prop in proposals if not prop.get("constraints_ok", False)]
    
    print(f"   - Propositions valides: {len(valid_props)}/{len(proposals)}")
    print(f"   - Propositions invalides: {len(invalid_props)}/{len(proposals)}")
    
    if len(valid_props) == 0:
        print("   ❌ ATTENTION: Aucune proposition valide!")
    elif len(valid_props) < len(proposals) // 2:
        print("   ⚠️  ATTENTION: Moins de la moitié des propositions sont valides")
    else:
        print("   ✅ Majorité des propositions valides")

def check_variation_algorithm():
    """Vérifie la logique de l'algorithme de variation"""
    
    print(f"\n🔧 VÉRIFICATION DE L'ALGORITHME DE VARIATION")
    print("=" * 60)
    
    # Lire le code source du contrôleur
    controller_path = Path("src/lcpi/aep/optimizer/controllers.py")
    
    if not controller_path.exists():
        print("❌ Fichier controllers.py non trouvé")
        return
    
    try:
        with open(controller_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier la présence de la méthode de variation
        if "_create_proposal_variation" in content:
            print("✅ Méthode _create_proposal_variation trouvée")
        else:
            print("❌ Méthode _create_proposal_variation manquante")
        
        # Vérifier la logique de variation
        if "diametres_candidats" in content:
            print("✅ Diamètres candidats définis")
        else:
            print("❌ Diamètres candidats non définis")
        
        if "random.uniform" in content:
            print("✅ Variation aléatoire implémentée")
        else:
            print("❌ Variation aléatoire manquante")
        
        if "copy.deepcopy" in content:
            print("✅ Copie profonde implémentée")
        else:
            print("❌ Copie profonde manquante")
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du contrôleur: {e}")

if __name__ == "__main__":
    analyze_diameter_variations()
    check_variation_algorithm()
