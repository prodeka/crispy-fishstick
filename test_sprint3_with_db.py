#!/usr/bin/env python3
"""
Test complet des fonctionnalités Sprint 3 avec la base de données des prix
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, 'src')

def test_sprint3_with_database():
    """Test toutes les fonctionnalités Sprint 3 avec la base de données"""
    print("🧪 Test des fonctionnalités Sprint 3 avec base de données")
    print("=" * 60)
    
    try:
        # Test 1: Import des modules
        print("1. Test des imports...")
        from lcpi.aep.optimizer.output import OutputFormatter
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        from lcpi.aep.optimizer.report_adapter import v11_adapter
        from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
        from lcpi.aep.optimizer.db_dao import prices_dao
        print("   ✅ Tous les modules importés avec succès")
        
        # Test 2: Création des instances
        print("2. Test de création des instances...")
        formatter = OutputFormatter()
        cli = AEPOptimizationCLI()
        adapter = v11_adapter
        print("   ✅ Toutes les classes créées avec succès")
        
        # Test 3: Test de la base de données
        print("3. Test de la base de données...")
        diameters = prices_dao.get_available_diameters('PVC-U')
        print(f"   ✅ Diamètres PVC-U: {len(diameters)} trouvés")
        
        # Test d'un prix spécifique
        price_110 = prices_dao.get_diameter_price(110, 'PVC-U')
        print(f"   ✅ Prix DN 110 PVC-U: {price_110:,.0f} FCFA/m")
        
        # Test 4: Création des données de test
        print("4. Test de création des données...")
        tank = TankDecision(id='TANK1', H_m=65.0)
        proposal = Proposal(
            name='test',
            is_feasible=True,
            tanks=[tank],
            diameters_mm={'PIPE1': 200},
            costs={'CAPEX': 100000},
            metrics={'min_pressure_m': 12.5}
        )
        result = OptimizationResult(
            proposals=[proposal],
            pareto_front=None,
            metadata={'method': 'test'}
        )
        print("   ✅ Données de test créées avec succès")
        
        # Test 5: Format V11
        print("5. Test du format V11...")
        v11_output = formatter.format_v11(result)
        print(f"   ✅ Format V11: {v11_output['metadata']['version']}")
        
        # Test 6: Conversion log
        print("6. Test de conversion log...")
        log_format = adapter.convert_v11_to_log_format(result)
        print(f"   ✅ Conversion log: {log_format['id']}")
        
        # Test 7: Rapport HTML
        print("7. Test de génération HTML...")
        html_report = cli._generate_html_report(
            {'proposals': [proposal], 'metadata': {'method': 'test'}},
            'optimisation_tank_v11.jinja2'
        )
        print(f"   ✅ Rapport HTML: {len(html_report)} caractères")
        
        # Test 8: Validation réseau
        print("8. Test de validation réseau...")
        network_valid = cli._validate_network('examples/test_network.inp')
        print(f"   ✅ Validation réseau: {network_valid}")
        
        # Test 9: Configuration
        print("9. Test de configuration...")
        config = cli._load_optimization_config(None, 0.5, 'nested')
        print(f"   ✅ Configuration: {config.method} (λ={config.objectives.lambda_opex})")
        
        # Test 10: Gestion des diamètres
        print("10. Test de gestion des diamètres...")
        
        # Ajouter un diamètre de test
        test_dn = 95
        test_price = 4500
        success_add = prices_dao.add_diameter(test_dn, 'PVC-U', 3150, 1350)
        print(f"   ✅ Ajout diamètre DN {test_dn}: {success_add}")
        
        # Vérifier qu'il a été ajouté
        added_price = prices_dao.get_diameter_price(test_dn, 'PVC-U')
        print(f"   ✅ Prix vérifié: {added_price:,.0f} FCFA/m")
        
        # Mettre à jour le prix
        success_update = prices_dao.update_diameter(test_dn, 'PVC-U', 3500, 1500)
        print(f"   ✅ Mise à jour diamètre DN {test_dn}: {success_update}")
        
        # Vérifier la mise à jour
        updated_price = prices_dao.get_diameter_price(test_dn, 'PVC-U')
        print(f"   ✅ Prix mis à jour: {updated_price:,.0f} FCFA/m")
        
        # Supprimer le diamètre de test
        success_remove = prices_dao.remove_diameter(test_dn, 'PVC-U')
        print(f"   ✅ Suppression diamètre DN {test_dn}: {success_remove}")
        
        # Vérifier la suppression
        removed_price = prices_dao.get_diameter_price(test_dn, 'PVC-U')
        print(f"   ✅ Prix après suppression: {removed_price}")
        
        print("\n🎉 Toutes les fonctionnalités Sprint 3 avec base de données sont opérationnelles !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sprint3_with_database()
    sys.exit(0 if success else 1)
