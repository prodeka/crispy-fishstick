#!/usr/bin/env python3
"""
Script de test pour le système de génération de rapports multi-solveurs
"""

import json
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.reporting.report_generator import ReportGenerator

def test_multi_solver_report():
    """Teste la génération d'un rapport multi-solveurs"""
    
    # Chemin vers les templates
    template_dir = Path("src/lcpi/reporting/templates")
    
    # Créer le générateur de rapports
    generator = ReportGenerator(template_dir)
    
    # Chemin vers le fichier multi-solveurs
    multi_solver_file = Path("results/out_multi_multi_realistic.json")
    
    if not multi_solver_file.exists():
        print(f"❌ Fichier multi-solveurs non trouvé: {multi_solver_file}")
        return False
    
    # Métadonnées du projet
    project_metadata = {
        "nom_projet": "Test Multi-Solveurs",
        "client": "Client Test",
        "description": "Test du système de génération de rapports multi-solveurs"
    }
    
    try:
        # Générer le rapport
        print("🔄 Génération du rapport multi-solveurs...")
        html_content = generator.generate_html_report(
            selected_logs_paths=[multi_solver_file],
            project_metadata=project_metadata,
            lcpi_version="1.0.0"
        )
        
        # Sauvegarder le rapport
        output_file = Path("results/test_multi_solver_report_realistic.html")
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"✅ Rapport généré avec succès: {output_file}")
        print(f"📊 Taille du rapport: {len(html_content)} caractères")
        
        # Vérifier que le contenu contient les éléments attendus
        expected_elements = [
            "Comparaison Multi-Solveurs",
            "Vue d'ensemble",
            "Comparaison détaillée",
            "EPANET",
            "LCPI"
        ]
        
        missing_elements = []
        for element in expected_elements:
            if element not in html_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"⚠️  Éléments manquants dans le rapport: {missing_elements}")
        else:
            print("✅ Tous les éléments attendus sont présents")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_detection_multi_solver():
    """Teste la détection des données multi-solveurs"""
    
    template_dir = Path("src/lcpi/reporting/templates")
    generator = ReportGenerator(template_dir)
    
    # Charger les données de test
    multi_solver_file = Path("results/out_multi_multi_realistic.json")
    
    if not multi_solver_file.exists():
        print(f"❌ Fichier de test non trouvé: {multi_solver_file}")
        return False
    
    try:
        with open(multi_solver_file, 'r', encoding='utf-8') as f:
            logs_data = [json.load(f)]
        
        # Tester la détection
        is_multi_solver, multi_solver_data = generator._detect_multi_solver_data(logs_data)
        
        print(f"🔍 Détection multi-solveurs: {'✅' if is_multi_solver else '❌'}")
        
        if is_multi_solver:
            print(f"📋 Solveurs détectés: {multi_solver_data.get('solvers', [])}")
            print(f"📊 Données des solveurs: {list(multi_solver_data.get('solver_data', {}).keys())}")
            
            # Vérifier que les données sont chargées
            for solver, data in multi_solver_data.get('solver_data', {}).items():
                if data:
                    print(f"  ✅ {solver}: données chargées")
                else:
                    print(f"  ⚠️  {solver}: pas de données")
        
        return is_multi_solver
        
    except Exception as e:
        print(f"❌ Erreur lors du test de détection: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test du système de génération de rapports multi-solveurs")
    print("=" * 60)
    
    # Test 1: Détection multi-solveurs
    print("\n1️⃣ Test de détection multi-solveurs")
    detection_ok = test_detection_multi_solver()
    
    # Test 2: Génération du rapport
    print("\n2️⃣ Test de génération du rapport")
    generation_ok = test_multi_solver_report()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📋 Résumé des tests:")
    print(f"  Détection multi-solveurs: {'✅' if detection_ok else '❌'}")
    print(f"  Génération du rapport: {'✅' if generation_ok else '❌'}")
    
    if detection_ok and generation_ok:
        print("\n🎉 Tous les tests sont passés avec succès!")
        print("📄 Le rapport est disponible dans: results/test_multi_solver_report.html")
        return True
    else:
        print("\n❌ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
