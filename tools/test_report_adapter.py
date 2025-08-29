#!/usr/bin/env python3
"""
Test de l'adaptateur de rapport V11.
"""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, 'src')

def test_v11_report_adapter():
    """Test complet de l'adaptateur de rapport V11."""
    print("🧪 Test de l'Adaptateur de Rapport V11")
    print("=" * 40)
    
    try:
        from lcpi.aep.optimizer.report_adapter import V11ReportAdapter
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        
        # 1. Créer un résultat V11 de test
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
                "iterations": 25,
                "pressure_min_m": 10.0
            }
        )
        
        print("✅ Résultat V11 de test créé")
        
        # 2. Créer l'adaptateur
        adapter = V11ReportAdapter()
        
        # 3. Métadonnées d'exécution
        execution_metadata = {
            "execution_time": "00:02:15",
            "lambda_opex": 15.0,
            "command": "price-optimize"
        }
        
        # 4. Convertir en format de log
        log_format = adapter.convert_v11_to_log_format(result, execution_metadata)
        
        print("✅ Conversion V11 → Log réussie")
        print(f"   ID: {log_format['id']}")
        print(f"   Titre: {log_format['titre_calcul']}")
        print(f"   Plugin: {log_format['plugin']}")
        
        # 5. Vérifier les champs requis
        required_fields = [
            'id', 'titre_calcul', 'timestamp', 'commande_executee',
            'donnees_resultat', 'transparence_mathematique', 'plugin', 'command'
        ]
        
        missing_fields = [field for field in required_fields if field not in log_format]
        if missing_fields:
            print(f"❌ Champs manquants: {missing_fields}")
            return False
        
        print("✅ Tous les champs requis sont présents")
        
        # 6. Vérifier le contenu de la transparence mathématique
        transparence = log_format['transparence_mathematique']
        print(f"✅ Transparence mathématique ({len(transparence)} étapes):")
        for i, step in enumerate(transparence[:3], 1):  # Afficher les 3 premières
            print(f"   {i}. {step}")
        if len(transparence) > 3:
            print(f"   ... et {len(transparence) - 3} autres étapes")
        
        # 7. Test de sauvegarde
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        log_id = adapter.save_v11_result_as_log(result, temp_path, execution_metadata)
        
        if temp_path.exists():
            print(f"✅ Sauvegarde réussie: {temp_path}")
            print(f"   Log ID: {log_id}")
            
            # Vérifier le contenu sauvegardé
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            if saved_data['id'] == log_id:
                print("✅ Contenu sauvegardé vérifié")
            else:
                print("❌ Problème avec le contenu sauvegardé")
                return False
            
            # Nettoyer
            temp_path.unlink()
        else:
            print("❌ Échec de la sauvegarde")
            return False
        
        # 8. Test du contexte hybride
        v11_data = adapter.formatter.format_v11(result)
        hybrid_context = adapter.create_hybrid_template_context(v11_data)
        
        expected_keys = ['logs_selectionnes', 'proposals', 'metadata', 'format_type']
        missing_keys = [key for key in expected_keys if key not in hybrid_context]
        
        if missing_keys:
            print(f"❌ Clés manquantes dans le contexte hybride: {missing_keys}")
            return False
        
        print("✅ Contexte hybride créé avec succès")
        print(f"   Format type: {hybrid_context['format_type']}")
        print(f"   Is V11: {hybrid_context['is_v11_format']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de l'adaptateur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_adapter_integration_with_reporting():
    """Test l'intégration avec le système de rapport existant."""
    print("\n🧪 Test d'intégration avec le système de rapport")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.report_adapter import create_log_from_v11_result
        from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
        
        # Créer un résultat de test
        tank = TankDecision(id="TANK1", H_m=70.0)
        proposal = Proposal(
            name="integration_test",
            is_feasible=True,
            tanks=[tank],
            diameters_mm={"PIPE1": 250},
            costs={"CAPEX": 200000, "OPEX_npv": 60000},
            metrics={"min_pressure_m": 15.0}
        )
        
        result = OptimizationResult(
            proposals=[proposal],
            pareto_front=None,
            metadata={
                "method": "global_optimization",
                "network_file": "integration_test.inp",
                "algorithm": "NSGA-II",
                "population_size": 50,
                "generations": 100
            }
        )
        
        # Test de la fonction utilitaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        execution_metadata = {
            "execution_time": "00:10:30",
            "lambda_opex": 20.0
        }
        
        log_id = create_log_from_v11_result(result, temp_path, execution_metadata)
        
        print("✅ Fonction utilitaire testée avec succès")
        print(f"   Log ID: {log_id}")
        print(f"   Fichier: {temp_path}")
        
        # Vérifier que le fichier peut être lu par le système de rapport
        if temp_path.exists():
            with open(temp_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            # Vérifier la structure pour compatibilité avec lcpi rapport
            if ('titre_calcul' in log_data and 
                'donnees_resultat' in log_data and 
                'transparence_mathematique' in log_data):
                print("✅ Structure compatible avec 'lcpi rapport'")
            else:
                print("❌ Structure incompatible")
                return False
            
            # Nettoyer
            temp_path.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        return False

def main():
    """Fonction principale."""
    print("🔧 Test de l'Adaptateur de Rapport V11")
    print("Vérification de la compatibilité avec 'lcpi rapport'")
    print("=" * 60)
    
    tests = [
        ("Adaptateur V11", test_v11_report_adapter),
        ("Intégration Rapport", test_adapter_integration_with_reporting)
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
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n🎯 Résultat global: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 Adaptateur fonctionnel ! Compatibilité V11 ↔ 'lcpi rapport' assurée.")
        print("💡 L'adaptateur peut être utilisé pour intégrer les résultats V11.")
    else:
        print("⚠️  Problèmes détectés dans l'adaptateur.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
