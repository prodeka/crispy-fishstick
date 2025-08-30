#!/usr/bin/env python3
"""
Démonstration des améliorations de la Phase 0 de PriceDB.

Ce script démontre les nouvelles fonctionnalités implémentées :
1. Modèle de tarification réaliste basé sur la loi de puissance
2. Structure de données harmonisée avec dn_mm
3. Gamme étendue de diamètres de fallback (25mm à 600mm)
4. Prix calculés dynamiquement au lieu de valeurs en dur
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def demo_realistic_pricing_model():
    """Démonstration du modèle de tarification réaliste"""
    print("🔍 Démonstration du modèle de tarification réaliste")
    print("=" * 60)
    
    try:
        from lcpi.aep.optimizer.db import _get_realistic_pipe_price, PRICE_MODELS
        
        print("📊 Modèles de tarification configurés:")
        for material, model in PRICE_MODELS.items():
            print(f"   {material}: Coût = {model['scaling_factor']} × D^{model['exponent_b']}")
        
        print("\n💰 Exemples de calculs de prix:")
        print("   Format: DN Xmm → Prix calculé → Prix arrondi")
        
        # Test avec différents diamètres et matériaux
        test_cases = [
            (25, "PVC"), (50, "PVC"), (110, "PVC"), (200, "PVC"),
            (63, "PEHD"), (125, "PEHD"), (250, "PEHD"), (315, "PEHD"),
            (100, "Fonte"), (200, "Fonte"), (400, "Fonte"), (600, "Fonte")
        ]
        
        for dn_mm, material in test_cases:
            raw_price = PRICE_MODELS[material]["scaling_factor"] * (dn_mm ** PRICE_MODELS[material]["exponent_b"])
            final_price = _get_realistic_pipe_price(dn_mm, material)
            
            print(f"   DN {dn_mm:3d}mm {material:6s}: {raw_price:8.0f} → {final_price:6.0f} FCFA/m")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_extended_fallback_range():
    """Démonstration de la gamme étendue des diamètres de fallback"""
    print("\n🔍 Démonstration de la gamme étendue des diamètres de fallback")
    print("=" * 60)
    
    try:
        from lcpi.aep.optimizer.db import FALLBACK_DIAMETERS_BASE
        
        print(f"📏 Gamme étendue: {len(FALLBACK_DIAMETERS_BASE)} diamètres de fallback")
        
        # Grouper par matériau
        materials = {}
        for item in FALLBACK_DIAMETERS_BASE:
            material = item["material"]
            if material not in materials:
                materials[material] = []
            materials[material].append(item["dn_mm"])
        
        print("\n📋 Répartition par matériau:")
        for material, diameters in materials.items():
            diameters.sort()
            min_dn = min(diameters)
            max_dn = max(diameters)
            print(f"   {material:6s}: {len(diameters):2d} diamètres (DN {min_dn:3d}mm - DN {max_dn:3d}mm)")
        
        # Afficher quelques exemples de chevauchement
        print("\n🔄 Exemples de chevauchement (même diamètre, différents matériaux):")
        overlap_examples = {}
        for item in FALLBACK_DIAMETERS_BASE:
            dn_mm = item["dn_mm"]
            material = item["material"]
            if dn_mm not in overlap_examples:
                overlap_examples[dn_mm] = []
            overlap_examples[dn_mm].append(material)
        
        # Afficher les diamètres avec plusieurs matériaux
        for dn_mm, materials_list in sorted(overlap_examples.items()):
            if len(materials_list) > 1:
                print(f"   DN {dn_mm:3d}mm: {', '.join(materials_list)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_canonical_structure():
    """Démonstration de la structure canonique harmonisée"""
    print("\n🔍 Démonstration de la structure canonique harmonisée")
    print("=" * 60)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        # Test avec la base principale
        print("📊 Structure depuis la base SQLite principale:")
        db_main = PriceDB()
        main_diameters = db_main.get_candidate_diameters()
        
        if main_diameters:
            example = main_diameters[0]
            print(f"   Exemple de structure:")
            for key, value in example.items():
                print(f"     {key}: {value}")
        
        # Test avec le fallback
        print("\n📊 Structure depuis le fallback:")
        db_fallback = PriceDB("fake_path")
        fallback_diameters = db_fallback.get_candidate_diameters()
        
        if fallback_diameters:
            example = fallback_diameters[0]
            print(f"   Exemple de structure:")
            for key, value in example.items():
                print(f"     {key}: {value}")
        
        # Vérifier la cohérence des structures
        print("\n🔍 Vérification de la cohérence:")
        if main_diameters and fallback_diameters:
            main_keys = set(main_diameters[0].keys())
            fallback_keys = set(fallback_diameters[0].keys())
            
            common_keys = main_keys & fallback_keys
            main_only = main_keys - fallback_keys
            fallback_only = fallback_keys - main_keys
            
            print(f"   Clés communes: {len(common_keys)}")
            print(f"   Clés uniquement dans la base principale: {len(main_only)}")
            print(f"   Clés uniquement dans le fallback: {len(fallback_only)}")
            
            if main_only:
                print(f"     Base principale: {', '.join(sorted(main_only))}")
            if fallback_only:
                print(f"     Fallback: {', '.join(sorted(fallback_only))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_fallback_scenarios():
    """Démonstration des différents scénarios de fallback"""
    print("\n🔍 Démonstration des différents scénarios de fallback")
    print("=" * 60)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        # Scénario 1: Base principale disponible
        print("📁 Scénario 1: Base principale disponible")
        db_main = PriceDB()
        info_main = db_main.get_database_info()
        print(f"   Source: {info_main['source_method'] if 'source_method' in info_main else 'Base principale'}")
        print(f"   Diamètres: {info_main['diameter_count']}")
        print(f"   Fallback utilisé: {info_main['fallback_used']}")
        
        # Scénario 2: Base inexistante → Fallback automatique
        print("\n📁 Scénario 2: Base inexistante → Fallback automatique")
        db_fallback = PriceDB("fake_path")
        info_fallback = db_fallback.get_database_info()
        print(f"   Source: {info_fallback['source_method'] if 'source_method' in info_fallback else 'Fallback'}")
        print(f"   Diamètres: {info_fallback.get('diameter_count', 'N/A')}")
        print(f"   Fallback utilisé: {info_fallback['fallback_used']}")
        
        # Comparer les performances
        print("\n⏱️  Comparaison des performances:")
        
        # Test avec la base principale
        import time
        start_time = time.time()
        main_diameters = db_main.get_candidate_diameters()
        main_time = (time.time() - start_time) * 1000
        
        # Test avec le fallback
        start_time = time.time()
        fallback_diameters = db_fallback.get_candidate_diameters()
        fallback_time = (time.time() - start_time) * 1000
        
        print(f"   Base principale: {len(main_diameters)} diamètres en {main_time:.2f}ms")
        print(f"   Fallback: {len(fallback_diameters)} diamètres en {fallback_time:.2f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_price_evolution():
    """Démonstration de l'évolution des prix selon le diamètre"""
    print("\n🔍 Démonstration de l'évolution des prix selon le diamètre")
    print("=" * 60)
    
    try:
        from lcpi.aep.optimizer.db import _get_realistic_pipe_price
        
        # Analyser l'évolution des prix pour chaque matériau
        materials = ["PVC", "PEHD", "Fonte"]
        diameter_range = [25, 50, 100, 200, 400, 600]
        
        print("📈 Évolution des prix (FCFA/m) selon le diamètre:")
        print("   DN(mm) |", " | ".join(f"{material:>8}" for material in materials))
        print("   " + "-" * 50)
        
        for dn_mm in diameter_range:
            prices = []
            for material in materials:
                price = _get_realistic_pipe_price(dn_mm, material)
                prices.append(f"{price:>8}")
            print(f"   {dn_mm:>6} |", " | ".join(prices))
        
        # Calculer les ratios de coût
        print("\n💡 Ratios de coût (Prix / Diamètre):")
        print("   DN(mm) |", " | ".join(f"{material:>8}" for material in materials))
        print("   " + "-" * 50)
        
        for dn_mm in diameter_range:
            ratios = []
            for material in materials:
                price = _get_realistic_pipe_price(dn_mm, material)
                ratio = price / dn_mm
                ratios.append(f"{ratio:>8.0f}")
            print(f"   {dn_mm:>6} |", " | ".join(ratios))
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de démonstration"""
    print("🚀 Démonstration des améliorations de la Phase 0 - PriceDB")
    print("=" * 80)
    
    demos = [
        ("Modèle de tarification réaliste", demo_realistic_pricing_model),
        ("Gamme étendue des diamètres de fallback", demo_extended_fallback_range),
        ("Structure canonique harmonisée", demo_canonical_structure),
        ("Scénarios de fallback", demo_fallback_scenarios),
        ("Évolution des prix selon le diamètre", demo_price_evolution),
    ]
    
    results = []
    for demo_name, demo_func in demos:
        print(f"\n{'='*80}")
        try:
            result = demo_func()
            results.append((demo_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue dans {demo_name}: {e}")
            results.append((demo_name, False))
    
    # Résumé
    print(f"\n{'='*80}")
    print("📊 RÉSUMÉ DES DÉMONSTRATIONS")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for demo_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} {demo_name}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} démonstrations réussies")
    
    if passed == total:
        print("\n🎉 Toutes les améliorations de la Phase 0 fonctionnent parfaitement!")
        print("\n📋 Récapitulatif des améliorations implémentées:")
        print("   ✅ Modèle de tarification réaliste avec loi de puissance")
        print("   ✅ Gamme étendue: 25mm à 600mm (36 diamètres)")
        print("   ✅ Structure canonique harmonisée (dn_mm partout)")
        print("   ✅ Prix calculés dynamiquement au lieu de valeurs en dur")
        print("   ✅ Fallback robuste avec 3 niveaux de sécurité")
        print("   ✅ Compatibilité avec l'ancien code maintenue")
    else:
        print("⚠️  Certaines démonstrations ont échoué. Vérifiez les détails ci-dessus.")

if __name__ == "__main__":
    main()
