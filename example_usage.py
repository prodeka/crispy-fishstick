#!/usr/bin/env python3
"""
Exemple d'utilisation des fonctionnalités Sprint 3
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, 'src')

def example_usage():
    """Exemple d'utilisation des fonctionnalités Sprint 3"""
    print("🚀 Exemple d'utilisation des fonctionnalités Sprint 3")
    print("=" * 60)
    
    try:
        # Import des modules
        from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
        from lcpi.aep.optimizer.output import OutputFormatter
        from lcpi.aep.optimizer.report_adapter import v11_adapter
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        from lcpi.aep.optimizer.db_dao import prices_dao
        
        print("✅ Modules importés avec succès")
        
        # Créer une instance CLI
        cli = AEPOptimizationCLI()
        print("✅ Interface CLI créée")
        
        # Exemple 1: Lister les diamètres disponibles
        print("\n📊 Exemple 1: Liste des diamètres disponibles")
        print("-" * 40)
        cli._list_diameters()
        
        # Exemple 2: Obtenir le prix d'un diamètre spécifique
        print("\n💰 Exemple 2: Prix d'un diamètre spécifique")
        print("-" * 40)
        dn = 200
        material = "PVC-U"
        price = prices_dao.get_diameter_price(dn, material)
        if price:
            print(f"Prix du DN {dn} {material}: {price:,.0f} FCFA/m")
            
            # Détail des prix
            supply_price = prices_dao.get_diameter_supply_price(dn, material)
            pose_price = prices_dao.get_diameter_pose_price(dn, material)
            print(f"  - Fourniture: {supply_price:,.0f} FCFA/m")
            print(f"  - Pose: {pose_price:,.0f} FCFA/m")
        else:
            print(f"Prix non trouvé pour DN {dn} {material}")
        
        # Exemple 3: Créer un résultat d'optimisation
        print("\n🔧 Exemple 3: Création d'un résultat d'optimisation")
        print("-" * 40)
        
        # Créer des données de test
        tank1 = TankDecision(id='TANK1', H_m=65.0)
        tank2 = TankDecision(id='TANK2', H_m=70.0)
        
        proposal1 = Proposal(
            name='Solution_économique',
            is_feasible=True,
            tanks=[tank1],
            diameters_mm={'PIPE1': 200, 'PIPE2': 160},
            costs={'CAPEX': 150000, 'OPEX_npv': 25000},
            metrics={'min_pressure_m': 12.5, 'max_pressure_m': 45.2}
        )
        
        proposal2 = Proposal(
            name='Solution_optimale',
            is_feasible=True,
            tanks=[tank1, tank2],
            diameters_mm={'PIPE1': 250, 'PIPE2': 200},
            costs={'CAPEX': 220000, 'OPEX_npv': 18000},
            metrics={'min_pressure_m': 15.8, 'max_pressure_m': 42.1}
        )
        
        result = OptimizationResult(
            proposals=[proposal1, proposal2],
            pareto_front=[proposal1, proposal2],
            metadata={
                'method': 'nested_greedy',
                'network_file': 'example_network.inp',
                'algorithm': 'Binary Search',
                'iterations': 15,
                'pressure_min_m': 10.0
            }
        )
        
        print(f"✅ Résultat créé avec {len(result.proposals)} propositions")
        print(f"   - Méthode: {result.metadata['method']}")
        print(f"   - Front de Pareto: {len(result.pareto_front)} solutions")
        
        # Exemple 4: Formater en V11
        print("\n📋 Exemple 4: Formatage V11")
        print("-" * 40)
        
        formatter = OutputFormatter()
        v11_output = formatter.format_v11(result)
        
        print(f"✅ Format V11 généré: {v11_output['metadata']['version']}")
        print(f"   - Propositions: {len(v11_output['proposals'])}")
        print(f"   - Métadonnées: {len(v11_output['metadata'])} champs")
        
        # Exemple 5: Conversion pour compatibilité LCPI
        print("\n🔄 Exemple 5: Conversion pour compatibilité LCPI")
        print("-" * 40)
        
        log_format = v11_adapter.convert_v11_to_log_format(result)
        
        print(f"✅ Log LCPI généré: {log_format['id']}")
        print(f"   - Titre: {log_format['titre_calcul']}")
        print(f"   - Transparence: {len(log_format['transparence_mathematique'])} étapes")
        
        # Exemple 6: Génération de rapport HTML
        print("\n🌐 Exemple 6: Génération de rapport HTML")
        print("-" * 40)
        
        html_report = cli._generate_html_report(
            {
                'proposals': [proposal1, proposal2],
                'metadata': result.metadata
            },
            'optimisation_tank_v11.jinja2'
        )
        
        print(f"✅ Rapport HTML généré: {len(html_report)} caractères")
        
        # Sauvegarder le rapport
        report_path = Path("example_report.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        print(f"📁 Rapport sauvegardé: {report_path}")
        
        # Exemple 7: Sauvegarde V11
        print("\n💾 Exemple 7: Sauvegarde au format V11")
        print("-" * 40)
        
        v11_path = Path("example_result_v11.json")
        formatter.save_v11_json(result, v11_path)
        print(f"✅ Résultat V11 sauvegardé: {v11_path}")
        
        # Exemple 8: Sauvegarde comme log LCPI
        print("\n📝 Exemple 8: Sauvegarde comme log LCPI")
        print("-" * 40)
        
        log_path = Path("example_result.log.json")
        log_id = v11_adapter.save_v11_result_as_log(result, log_path)
        print(f"✅ Log LCPI sauvegardé: {log_path}")
        print(f"   - ID du log: {log_id}")
        
        print("\n🎉 Tous les exemples exécutés avec succès !")
        print(f"📁 Fichiers générés:")
        print(f"   - {report_path}")
        print(f"   - {v11_path}")
        print(f"   - {log_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exemple: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = example_usage()
    sys.exit(0 if success else 1)
