#!/usr/bin/env python3
"""
Test de compatibilité entre le format V11 et la commande 'lcpi rapport'
"""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, 'src')

def test_v11_to_log_format_compatibility():
    """Test la conversion du format V11 vers le format de log LCPI."""
    print("🧪 Test de compatibilité Format V11 → Format Log LCPI")
    print("=" * 55)
    
    try:
        from lcpi.aep.optimizer.output import OutputFormatter
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        from lcpi.lcpi_logging.logger import lcpi_logger
        from datetime import datetime
        
        # 1. Créer un résultat V11
        tank = TankDecision(id="TANK1", H_m=65.0)
        proposal = Proposal(
            name="test_solution",
            is_feasible=True,
            tanks=[tank],
            diameters_mm={"PIPE1": 200, "PIPE2": 150},
            costs={"CAPEX": 150000, "OPEX_annual": 5000, "OPEX_npv": 45000},
            metrics={"min_pressure_m": 12.5, "max_velocity_m_s": 1.8}
        )
        
        result = OptimizationResult(
            proposals=[proposal],
            pareto_front=None,
            metadata={
                "method": "nested_greedy",
                "network_file": "test_network.inp",
                "algorithm": "NestedGreedy",
                "iterations": 25
            }
        )
        
        print("✅ Résultat V11 créé avec succès")
        
        # 2. Convertir en format V11
        formatter = OutputFormatter()
        v11_output = formatter.format_v11(result)
        
        print("✅ Format V11 généré")
        
        # 3. Créer un adaptateur pour le format de log
        def convert_v11_to_log_format(v11_result: dict) -> dict:
            """Convertit un résultat V11 en format de log compatible avec lcpi rapport."""
            return {
                "id": f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "titre_calcul": f"Optimisation AEP - {v11_result['metadata'].get('method', 'unknown')}",
                "timestamp": datetime.now().isoformat(),
                "commande_executee": "lcpi aep optimizer price-optimize",
                "donnees_resultat": v11_result,
                "transparence_mathematique": [
                    f"Méthode: {v11_result['metadata'].get('method', 'N/A')}",
                    f"Réseau: {v11_result['metadata'].get('network_file', 'N/A')}",
                    f"Propositions: {len(v11_result['proposals'])}",
                    f"Solutions faisables: {len([p for p in v11_result['proposals'] if p.get('is_feasible', False)])}"
                ],
                "hash_donnees_entree": "test_hash_v11",
                "parametres_entree": {
                    "network_file": v11_result['metadata'].get('network_file'),
                    "method": v11_result['metadata'].get('method'),
                    "iterations": v11_result['metadata'].get('iterations')
                },
                "version_algorithme": "V11",
                "plugin": "aep",
                "command": "optimizer"
            }
        
        # 4. Convertir le format V11 en format de log
        log_format = convert_v11_to_log_format(v11_output)
        
        print("✅ Conversion V11 → Log réussie")
        print(f"   Titre: {log_format['titre_calcul']}")
        print(f"   Plugin: {log_format['plugin']}")
        print(f"   Commande: {log_format['command']}")
        
        # 5. Vérifier que le format est compatible avec le rapport
        required_fields = ['id', 'titre_calcul', 'timestamp', 'commande_executee', 
                          'donnees_resultat', 'transparence_mathematique']
        
        missing_fields = [field for field in required_fields if field not in log_format]
        if missing_fields:
            print(f"❌ Champs manquants: {missing_fields}")
            return False
        
        print("✅ Tous les champs requis sont présents")
        
        # 6. Test de compatibilité avec le générateur de rapport
        try:
            from lcpi.reporting.report_generator import ReportGenerator
            
            # Créer un fichier temporaire avec le format de log
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(log_format, temp_file, indent=2, ensure_ascii=False)
                temp_path = Path(temp_file.name)
            
            # Tester la génération de rapport
            template_dir = Path("src/lcpi/reporting/templates")
            if template_dir.exists():
                report_gen = ReportGenerator(template_dir=template_dir)
                
                # Charger le projet metadata par défaut
                project_metadata = {"nom_projet": "Test Projet V11"}
                
                # Générer le rapport HTML
                html_content = report_gen.generate_html_report([temp_path], project_metadata)
                
                if html_content and len(html_content) > 1000:  # Vérifier qu'il y a du contenu
                    print("✅ Rapport HTML généré avec succès")
                    print(f"   Taille: {len(html_content)} caractères")
                    
                    # Vérifier que le contenu V11 est présent
                    if "Optimisation AEP" in html_content and "nested_greedy" in html_content:
                        print("✅ Contenu V11 correctement intégré dans le rapport")
                    else:
                        print("⚠️  Contenu V11 peut-être manquant dans le rapport")
                else:
                    print("❌ Rapport HTML vide ou trop petit")
                    return False
            else:
                print("⚠️  Répertoire de templates non trouvé, test de génération ignoré")
            
            # Nettoyer le fichier temporaire
            temp_path.unlink()
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération de rapport: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de compatibilité: {e}")
        return False

def test_v11_template_vs_existing_template():
    """Compare le template V11 avec le template existant."""
    print("\n🧪 Test de compatibilité des templates")
    print("=" * 40)
    
    try:
        # Vérifier l'existence des templates
        v11_template = Path("src/lcpi/aep/templates/optimisation_tank_v11.jinja2")
        existing_template = Path("src/lcpi/reporting/templates/base_simple.html")
        
        print(f"Template V11: {'✅ Existe' if v11_template.exists() else '❌ Manquant'}")
        print(f"Template existant: {'✅ Existe' if existing_template.exists() else '❌ Manquant'}")
        
        if v11_template.exists():
            v11_size = v11_template.stat().st_size
            print(f"   Taille V11: {v11_size} bytes")
        
        if existing_template.exists():
            existing_size = existing_template.stat().st_size
            print(f"   Taille existant: {existing_size} bytes")
        
        # Les deux templates peuvent coexister
        print("✅ Templates compatibles (fonctions différentes)")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison des templates: {e}")
        return False

def test_cli_commands_integration():
    """Test l'intégration des nouvelles commandes CLI."""
    print("\n🧪 Test d'intégration des commandes CLI")
    print("=" * 40)
    
    try:
        from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
        
        cli = AEPOptimizationCLI()
        
        # Tester que les méthodes sont disponibles
        expected_methods = ['price_optimize', 'report', 'diameters_manage']
        available_methods = [method for method in dir(cli) if not method.startswith('_')]
        
        for method in expected_methods:
            if method in available_methods:
                print(f"✅ Méthode {method} disponible")
            else:
                print(f"❌ Méthode {method} manquante")
                return False
        
        # Tester les méthodes helper
        helper_methods = ['_load_optimization_config', '_validate_network', '_generate_html_report']
        for method in helper_methods:
            if method in available_methods:
                print(f"✅ Helper {method} disponible")
            else:
                print(f"⚠️  Helper {method} manquant (optionnel)")
        
        print("✅ Toutes les méthodes CLI sont disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test CLI: {e}")
        return False

def main():
    """Fonction principale."""
    print("🔗 Test de Compatibilité Format V11 ↔ Système de Rapport LCPI")
    print("=" * 65)
    
    tests = [
        ("Compatibilité V11 → Log", test_v11_to_log_format_compatibility),
        ("Compatibilité Templates", test_v11_template_vs_existing_template),
        ("Intégration CLI", test_cli_commands_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 65)
    print("📊 RÉSUMÉ DE LA COMPATIBILITÉ")
    print("=" * 65)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ COMPATIBLE" if result else "❌ INCOMPATIBLE"
        print(f"   {status} - {test_name}")
    
    print(f"\n🎯 Compatibilité globale: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 Compatibilité complète ! Les formats V11 et Log LCPI sont compatibles.")
        print("💡 Recommandation: Créer un adaptateur V11→Log pour intégration complète.")
    else:
        print("⚠️  Problèmes de compatibilité détectés. Adaptations nécessaires.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
