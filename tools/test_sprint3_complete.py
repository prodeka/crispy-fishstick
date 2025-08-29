#!/usr/bin/env python3
"""
Test complet des fonctionnalités Sprint 3
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, 'src')

def test_sprint3_features():
    """Test toutes les fonctionnalités Sprint 3"""
    print("🧪 Test des fonctionnalités Sprint 3")
    print("=" * 50)
    
    try:
        # Test 1: Import des modules
        print("1. Test des imports...")
        from lcpi.aep.optimizer.output import OutputFormatter
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        from lcpi.aep.optimizer.report_adapter import v11_adapter
        from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
        print("   ✅ Tous les modules importés avec succès")
        
        # Test 2: Création des instances
        print("2. Test de création des instances...")
        formatter = OutputFormatter()
        cli = AEPOptimizationCLI()
        adapter = v11_adapter
        print("   ✅ Toutes les classes créées avec succès")
        
        # Test 3: Création des données de test
        print("3. Test de création des données...")
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
        
        # Test 4: Format V11
        print("4. Test du format V11...")
        v11_output = formatter.format_v11(result)
        print(f"   ✅ Format V11: {v11_output['metadata']['version']}")
        
        # Test 5: Conversion log
        print("5. Test de conversion log...")
        log_format = adapter.convert_v11_to_log_format(result)
        print(f"   ✅ Conversion log: {log_format['id']}")
        
        # Test 6: Rapport HTML
        print("6. Test de génération HTML...")
        html_report = cli._generate_html_report(
            {'proposals': [proposal], 'metadata': {'method': 'test'}},
            'optimisation_tank_v11.jinja2'
        )
        print(f"   ✅ Rapport HTML: {len(html_report)} caractères")
        
        # Test 7: Validation réseau
        print("7. Test de validation réseau...")
        network_valid = cli._validate_network('examples/test_network.inp')
        print(f"   ✅ Validation réseau: {network_valid}")
        
        # Test 8: Configuration
        print("8. Test de configuration...")
        config = cli._load_optimization_config(None, 0.5, 'nested')
        print(f"   ✅ Configuration: {config.method} (λ={config.objectives.lambda_opex})")
        
        print("\n🎉 Toutes les fonctionnalités Sprint 3 sont opérationnelles !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sprint3_features()
    sys.exit(0 if success else 1)
