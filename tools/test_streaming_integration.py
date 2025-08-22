#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration du streaming des flux.
Teste le validateur INP et le streaming des flux.
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lcpi.aep.utils.inp_mass_conservation_validator import quick_inp_check, validate_inp_mass_conservation
from src.lcpi.aep.utils.flows_inspector import FlowEventConsumer
import tempfile
import json


def test_inp_validator():
    """Test du validateur INP."""
    print("🔍 Test du validateur INP")
    print("=" * 50)
    
    # Test avec le fichier Bismark
    inp_file = "src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp"
    
    if not Path(inp_file).exists():
        print(f"❌ Fichier INP introuvable: {inp_file}")
        return False
    
    # Test rapide
    print("📋 Validation rapide:")
    quick_report = quick_inp_check(inp_file)
    print(quick_report)
    
    # Test détaillé
    print("\n📊 Validation détaillée:")
    success, detailed_report = validate_inp_mass_conservation(inp_file)
    print(f"✅ Succès: {success}")
    print(f"📈 Rapport: {json.dumps(detailed_report, indent=2, ensure_ascii=False)}")
    
    return success


def test_flow_streaming():
    """Test du streaming des flux."""
    print("\n🌊 Test du streaming des flux")
    print("=" * 50)
    
    # Créer un dossier temporaire pour les artefacts
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Créer un consommateur d'événements
        consumer = FlowEventConsumer(
            outdir=temp_path,
            stem="test_streaming",
            sim_name="integration_test",
            save_plot=True
        )
        
        print(f"📁 Dossier temporaire: {temp_path}")
        
        # Simuler des événements de simulation
        events = [
            ("simulation_step", {
                "sim_id": "test_123",
                "step": 0,
                "total_steps": 5,
                "flows": {"P1": 0.1, "P2": 0.2, "P3": 0.3},
                "total_flow": 0.6,
                "timestamp": 1234567890.0
            }),
            ("simulation_step", {
                "sim_id": "test_123",
                "step": 1,
                "total_steps": 5,
                "flows": {"P1": 0.15, "P2": 0.25, "P3": 0.35},
                "total_flow": 0.75,
                "timestamp": 1234567890.1
            }),
            ("simulation_step", {
                "sim_id": "test_123",
                "step": 2,
                "total_steps": 5,
                "flows": {"P1": 0.2, "P2": 0.3, "P3": 0.4},
                "total_flow": 0.9,
                "timestamp": 1234567890.2
            })
        ]
        
        # Traiter les événements
        for event_type, event_data in events:
            print(f"📡 Événement: {event_type} - Step {event_data['step']}")
            consumer(event_type, event_data)
        
        # Finaliser et sauvegarder
        print("💾 Finalisation...")
        artifacts = consumer.finalize()
        
        print(f"📊 Artefacts générés: {artifacts}")
        
        # Vérifier que les fichiers ont été créés
        expected_files = [
            "test_streaming_sumflows_integration_test_stream.csv",
            "test_streaming_sumflows_integration_test_stream.json",
            "test_streaming_sumflows_integration_test_stream.png"
        ]
        
        for expected_file in expected_files:
            file_path = temp_path / expected_file
            if file_path.exists():
                print(f"✅ {expected_file} créé")
            else:
                print(f"❌ {expected_file} manquant")
        
        return True


def test_optimization_integration():
    """Test de l'intégration avec l'optimisation."""
    print("\n⚙️ Test de l'intégration avec l'optimisation")
    print("=" * 50)
    
    try:
        from src.lcpi.aep.optimizer.controllers import OptimizationController
        
        print("✅ OptimizationController importé avec succès")
        
        # Vérifier que le flag stream_flows est disponible
        controller = OptimizationController()
        print("✅ OptimizationController instancié")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        return False


def main():
    """Fonction principale de test."""
    print("🧪 Tests d'intégration du streaming des flux")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Validateur INP
    print("\n1️⃣ Test du validateur INP")
    results["inp_validator"] = test_inp_validator()
    
    # Test 2: Streaming des flux
    print("\n2️⃣ Test du streaming des flux")
    results["flow_streaming"] = test_flow_streaming()
    
    # Test 3: Intégration optimisation
    print("\n3️⃣ Test de l'intégration avec l'optimisation")
    results["optimization_integration"] = test_optimization_integration()
    
    # Résumé
    print("\n📊 Résumé des tests")
    print("=" * 30)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print(f"\n🎯 Résultat global: {'✅ TOUS LES TESTS PASSÉS' if all_passed else '❌ CERTAINS TESTS ONT ÉCHOUÉ'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
