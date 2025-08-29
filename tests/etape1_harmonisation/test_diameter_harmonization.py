#!/usr/bin/env python3
"""
Script de test pour vérifier l'harmonisation des diamètres candidats
entre tous les algorithmes d'optimisation.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_diameter_manager():
    """Test du gestionnaire centralisé des diamètres."""
    print("🔍 Test du gestionnaire centralisé des diamètres...")
    
    try:
        from lcpi.aep.optimizer.diameter_manager import get_diameter_manager
        
        manager = get_diameter_manager()
        candidates = manager.get_candidate_diameters()
        
        print(f"✅ {len(candidates)} diamètres chargés")
        print("📊 Échantillon des diamètres et prix:")
        
        for i, candidate in enumerate(candidates[:10]):  # Afficher les 10 premiers
            print(f"   {i+1:2d}. {candidate.diameter_mm:3d}mm -> {candidate.cost_per_m:6.0f} FCFA/m")
        
        if len(candidates) > 10:
            print(f"   ... et {len(candidates) - 10} autres diamètres")
        
        # Vérifier la cohérence des prix
        prices = [c.cost_per_m for c in candidates]
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        
        print(f"\n💰 Analyse des prix:")
        print(f"   Prix minimum: {min_price:6.0f} FCFA/m")
        print(f"   Prix maximum: {max_price:6.0f} FCFA/m")
        print(f"   Prix moyen:   {avg_price:6.0f} FCFA/m")
        print(f"   Ratio max/min: {max_price/min_price:.1f}")
        
        # Vérifier que les prix ne sont pas uniformes
        unique_prices = len(set(prices))
        if unique_prices == 1:
            print("❌ ERREUR: Tous les diamètres ont le même prix (uniforme)")
            return False
        else:
            print(f"✅ Prix différenciés: {unique_prices} prix uniques sur {len(candidates)} diamètres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du gestionnaire: {e}")
        return False

def test_controller_diameters():
    """Test du contrôleur d'optimisation."""
    print("\n🔍 Test du contrôleur d'optimisation...")
    
    try:
        from lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
        
        diam_rows = get_standard_diameters_with_prices("PVC-U")
        
        print(f"✅ {len(diam_rows)} diamètres retournés par le contrôleur")
        print("📊 Échantillon des diamètres et prix:")
        
        for i, row in enumerate(diam_rows[:10]):
            diameter = row.get("d_mm")
            cost = row.get("cost_per_m")
            print(f"   {i+1:2d}. {diameter:3d}mm -> {cost:6.0f} FCFA/m")
        
        # Vérifier la cohérence des prix
        prices = [row.get("cost_per_m", 0) for row in diam_rows]
        unique_prices = len(set(prices))
        
        if unique_prices == 1:
            print("❌ ERREUR: Tous les diamètres ont le même prix (uniforme)")
            return False
        else:
            print(f"✅ Prix différenciés: {unique_prices} prix uniques")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du contrôleur: {e}")
        return False

def test_algorithm_compatibility():
    """Test de la compatibilité avec les algorithmes existants."""
    print("\n🔍 Test de compatibilité avec les algorithmes...")
    
    try:
        from lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
        
        # Simuler l'utilisation dans les algorithmes
        diam_rows = get_standard_diameters_with_prices("PVC-U")
        
        # Test 1: Format compatible avec l'algorithme génétique
        from lcpi.aep.optimization.models import DiametreCommercial
        
        diam_cands = []
        for row in diam_rows:
            candidate = DiametreCommercial(
                diametre_mm=int(row.get("d_mm")),
                cout_fcfa_m=float(row.get("cost_per_m", row.get("total_fcfa_per_m", 1000.0)))
            )
            diam_cands.append(candidate)
        
        print(f"✅ {len(diam_cands)} objets DiametreCommercial créés")
        
        # Test 2: Format compatible avec les algorithmes nested et global
        diameters_list = [int(row.get("d_mm")) for row in diam_rows]
        print(f"✅ {len(diameters_list)} diamètres convertis en liste d'entiers")
        
        # Test 3: Vérifier que les diamètres sont dans l'ordre croissant
        if diameters_list == sorted(diameters_list):
            print("✅ Diamètres correctement triés par ordre croissant")
        else:
            print("❌ ERREUR: Les diamètres ne sont pas triés")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de compatibilité: {e}")
        return False

def test_price_realism():
    """Test du réalisme des prix."""
    print("\n🔍 Test du réalisme des prix...")
    
    try:
        from lcpi.aep.optimizer.diameter_manager import get_standard_diameters_with_prices
        
        diam_rows = get_standard_diameters_with_prices("PVC-U")
        
        # Vérifier que les prix augmentent avec la taille
        price_increases = 0
        total_comparisons = 0
        
        for i in range(len(diam_rows) - 1):
            current_diam = diam_rows[i]["d_mm"]
            current_price = diam_rows[i]["cost_per_m"]
            next_diam = diam_rows[i + 1]["d_mm"]
            next_price = diam_rows[i + 1]["cost_per_m"]
            
            if next_diam > current_diam:
                total_comparisons += 1
                if next_price > current_price:
                    price_increases += 1
                else:
                    print(f"⚠️  Prix décroissant: {current_diam}mm ({current_price}) -> {next_diam}mm ({next_price})")
        
        if total_comparisons > 0:
            success_rate = (price_increases / total_comparisons) * 100
            print(f"✅ Taux de cohérence prix/taille: {success_rate:.1f}% ({price_increases}/{total_comparisons})")
            
            if success_rate >= 90:
                print("✅ Prix cohérents avec la taille des diamètres")
                return True
            else:
                print("⚠️  Certains prix ne suivent pas la logique taille/coût")
                return False
        else:
            print("⚠️  Impossible de tester la cohérence des prix")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test de réalisme: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test d'harmonisation des diamètres candidats")
    print("=" * 60)
    
    tests = [
        ("Gestionnaire centralisé", test_diameter_manager),
        ("Contrôleur d'optimisation", test_controller_diameters),
        ("Compatibilité algorithmes", test_algorithm_compatibility),
        ("Réalisme des prix", test_price_realism),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test '{test_name}': {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'harmonisation est réussie.")
        return 0
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
