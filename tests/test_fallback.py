#!/usr/bin/env python3
"""
Script de test pour vérifier le comportement de fallback de la classe PriceDB.
"""

from src.lcpi.aep.optimizer.db import PriceDB

def test_fallback():
    """Teste le comportement de fallback."""
    print("=== Test du comportement de fallback ===\n")
    
    try:
        # Créer une instance avec un chemin inexistant pour forcer le fallback
        print("1. Création d'une instance PriceDB avec chemin inexistant...")
        db = PriceDB("chemin/inexistant/vers/db.db")
        print("   ✓ Instance créée avec succès !")
        
        # Vérifier les informations de base
        print("\n2. Informations de la base de données :")
        info = db.get_database_info()
        print(f"   Type de source: {info.get('type', 'N/A')}")
        print(f"   Nombre de diamètres: {info.get('diameter_count', 'N/A')}")
        print(f"   Fallback utilisé: {info.get('fallback_used', 'N/A')}")
        
        # Vérifier les diamètres candidats
        print("\n3. Diamètres candidats disponibles (fallback) :")
        diameters = db.get_candidate_diameters()
        print(f"   Total: {len(diameters)} diamètres")
        
        if diameters:
            print("   Exemples (5 premiers):")
            for i, d in enumerate(diameters[:5]):
                print(f"     {i+1}. DN {d['dn_mm']}mm - {d['material']} - {d['total_fcfa_per_m']} FCFA/m")
        
        # Test de la méthode get_closest_diameter avec fallback
        print("\n4. Test de get_closest_diameter (fallback) :")
        target = 120  # mm
        closest = db.get_closest_diameter(target)
        if closest:
            print(f"   Diamètre cible: {target}mm")
            print(f"   Plus proche: DN {closest['dn_mm']}mm - {closest['material']}")
            print(f"   Différence: {abs(closest['dn_mm'] - target)}mm")
        
        # Test avec matériau spécifique (fallback)
        print("\n5. Test avec matériau spécifique PVC (fallback) :")
        pvc_diameters = db.get_candidate_diameters("PVC")
        print(f"   Diamètres PVC disponibles: {len(pvc_diameters)}")
        if pvc_diameters:
            print("   Exemples PVC:")
            for i, d in enumerate(pvc_diameters[:3]):
                print(f"     {i+1}. DN {d['dn_mm']}mm - {d['total_fcfa_per_m']} FCFA/m")
        
        print("\n=== Test de fallback réussi ! ===")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test de fallback: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fallback()
