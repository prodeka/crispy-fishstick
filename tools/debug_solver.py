#!/usr/bin/env python3
"""
Script de debug pour diagnostiquer le problème de transmission du solveur
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def debug_solver_transmission():
    """Debug la transmission du solveur"""
    
    print("🔍 DEBUG DE LA TRANSMISSION DU SOLVEUR")
    print("=" * 60)
    
    try:
        from lcpi.aep.optimizer.controllers import OptimizationController
        
        print("✅ Import du contrôleur réussi")
        
        # Créer une instance du contrôleur
        controller = OptimizationController()
        print("✅ Instance du contrôleur créée")
        
        # Tester l'import de l'optimiseur génétique
        try:
            optimizer_class = controller._import_optimizer_class("genetic")
            print("✅ Classe de l'optimiseur génétique importée")
            
            # Créer une instance de l'optimiseur
            optimizer = optimizer_class(
                network_model="test.inp",
                solver="lcpi",  # Tester avec LCPI
                price_db=None,
                config=None
            )
            print("✅ Instance de l'optimiseur génétique créée")
            
            # Vérifier l'attribut solver
            print(f"🔍 Solveur stocké: {getattr(optimizer, 'solver', 'NON TROUVÉ')}")
            print(f"🔍 Type de l'attribut solver: {type(getattr(optimizer, 'solver', None))}")
            
            # Tester l'optimisation (dry run)
            result = optimizer.optimize(
                constraints={"pressure_min_m": 10.0},
                objective="price",
                seed=None
            )
            
            print("✅ Optimisation (dry run) réussie")
            print(f"🔍 Métadonnées retournées: {result.get('meta', {})}")
            print(f"🔍 Solveur dans les métadonnées: {result.get('meta', {}).get('solver', 'NON TROUVÉ')}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'optimiseur: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_solver_transmission()
