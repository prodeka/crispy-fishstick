#!/usr/bin/env python3
"""
Script de test pour la classe PriceDB mise à jour avec les corrections de la Section A.
"""

from src.lcpi.aep.optimizer.db import PriceDB, PipeData

def test_price_db():
    """Teste la classe PriceDB mise à jour."""
    print("=== Test de la classe PriceDB mise à jour ===\n")
    
    try:
        # Créer une instance
        print("1. Création d'une instance PriceDB...")
        db = PriceDB()
        print("   ✓ Instance créée avec succès !")
        
        # Vérifier les informations de base
        print("\n2. Informations de la base de données :")
        info = db.get_database_info()
        print(f"   Type de source: {info.get('type', 'N/A')}")
        print(f"   Nombre de diamètres: {info.get('diameter_count', 'N/A')}")
        print(f"   Fallback utilisé: {info.get('fallback_used', 'N/A')}")
        print(f"   Version DB: {info.get('db_version', 'N/A')}")
        
        # Vérifier les diamètres candidats
        print("\n3. Diamètres candidats disponibles :")
        diameters = db.get_candidate_diameters()
        print(f"   Total: {len(diameters)} diamètres")
        
        if diameters:
            print("   Exemples (5 premiers):")
            for i, d in enumerate(diameters[:5]):
                print(f"     {i+1}. DN {d['dn_mm']}mm - {d['material']} - {d['total_fcfa_per_m']} FCFA/m")
        
        # Test de la méthode get_closest_diameter
        print("\n4. Test de get_closest_diameter :")
        target = 120  # mm
        closest = db.get_closest_diameter(target)
        if closest:
            print(f"   Diamètre cible: {target}mm")
            print(f"   Plus proche: DN {closest['dn_mm']}mm - {closest['material']}")
            print(f"   Différence: {abs(closest['dn_mm'] - target)}mm")
        
        # Test avec matériau spécifique
        print("\n5. Test avec matériau spécifique (PVC-U) :")
        pvc_diameters = db.get_candidate_diameters("PVC-U")
        print(f"   Diamètres PVC-U disponibles: {len(pvc_diameters)}")
        if pvc_diameters:
            print("   Exemples PVC-U:")
            for i, d in enumerate(pvc_diameters[:3]):
                print(f"     {i+1}. DN {d['dn_mm']}mm - {d['total_fcfa_per_m']} FCFA/m")
        
        # Test de get_diameter_price
        print("\n6. Test de get_diameter_price :")
        test_dn = 110
        price = db.get_diameter_price(test_dn, "PVC-U")
        if price:
            print(f"   Prix DN {test_dn}mm PVC-U: {price} FCFA/m")
        else:
            print(f"   Prix DN {test_dn}mm PVC-U: Non trouvé")
        
        print("\n=== Tous les tests ont réussi ! ===")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_price_db()
