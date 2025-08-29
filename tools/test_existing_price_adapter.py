#!/usr/bin/env python3
"""
Test de l'adaptateur de prix pour la base de données existante.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.core.solvers.price_adapter import ExistingPriceAdapter

def test_existing_price_adapter():
    """Test principal de l'adaptateur de prix."""
    
    print("🔍 TEST DE L'ADAPTATEUR DE PRIX EXISTANT")
    print("=" * 50)
    
    try:
        # Créer l'adaptateur
        adapter = ExistingPriceAdapter()
        print("✅ Adaptateur créé avec succès")
        
        # Test 1: Récupérer les matériaux disponibles
        print(f"\n📋 Test 1: Matériaux disponibles")
        materials = adapter.get_available_materials()
        print(f"   Matériaux: {materials}")
        
        # Test 2: Récupérer les diamètres disponibles pour l'acier
        print(f"\n📏 Test 2: Diamètres disponibles pour Acier_galv")
        diameters = adapter.get_available_diameters("Acier_galv")
        print(f"   Diamètres: {diameters[:10]}... (total: {len(diameters)})")
        
        # Test 3: Récupérer des prix spécifiques
        print(f"\n💰 Test 3: Prix spécifiques")
        test_diameters = [110, 200, 315, 500]
        for diameter in test_diameters:
            price = adapter.get_pipe_price(diameter, "Acier_galv")
            if price:
                print(f"   {diameter}mm Acier_galv: {price:,.0f} FCFA/m")
            else:
                print(f"   {diameter}mm Acier_galv: Prix non trouvé")
        
        # Test 4: Calculer le coût d'un réseau simple
        print(f"\n🏗️ Test 4: Calcul du coût d'un réseau")
        test_network = {
            "C1": 110,   # 110 mm
            "C2": 200,   # 200 mm
            "C3": 315,   # 315 mm
        }
        
        cost_result = adapter.calculate_network_cost(
            diameters_mm=test_network,
            material="Acier_galv",
            conduit_length_m=100.0
        )
        
        print(f"   Coût total: {cost_result['total_cost_fcfa']:,.0f} FCFA")
        print(f"   Matériau utilisé: {cost_result['material_used']}")
        print(f"   Longueur estimée par conduite: {cost_result['estimated_length_per_conduit_m']} m")
        
        if cost_result['missing_prices']:
            print(f"   ⚠️ Prix manquants: {cost_result['missing_prices']}")
        
        # Test 5: Résumé des prix
        print(f"\n📊 Test 5: Résumé des prix")
        price_summary = adapter.get_price_summary()
        print(f"   Nombre de matériaux: {len(price_summary)}")
        
        # Afficher quelques exemples de prix
        for material in list(price_summary.keys())[:3]:  # Limiter à 3 matériaux
            material_prices = price_summary[material]
            print(f"   {material}: {len(material_prices)} diamètres")
            # Afficher quelques prix pour ce matériau
            for diameter in list(material_prices.keys())[:3]:
                price = material_prices[diameter]
                print(f"     {diameter}mm: {price:,.0f} FCFA/m")
        
        # Test 6: Comparaison avec l'ancien coût
        print(f"\n🔍 Test 6: Comparaison avec l'ancien coût")
        old_cost = 4_296_431  # Ancien coût du fichier de résultats
        new_cost = cost_result['total_cost_fcfa']
        
        if new_cost > 0:
            ratio = new_cost / old_cost
            print(f"   Ancien coût: {old_cost:,.0f} FCFA")
            print(f"   Nouveau coût: {new_cost:,.0f} FCFA")
            print(f"   Ratio: {ratio:.1f}x")
            
            if ratio > 10:
                print(f"   ✅ Coût {ratio:.1f}x plus réaliste!")
            elif ratio > 5:
                print(f"   ✅ Coût {ratio:.1f}x plus réaliste")
            else:
                print(f"   ⚠️ Coût encore trop faible")
        
        print(f"\n🎉 TEST TERMINÉ AVEC SUCCÈS!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_existing_price_adapter()
    if not success:
        print("\n❌ TEST ÉCHOUÉ")
        sys.exit(1)
