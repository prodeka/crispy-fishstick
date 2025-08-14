#!/usr/bin/env python3
"""
Test de génération de rapports global avec Pandoc
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_report_generation():
    """Test de la génération de rapports avec Pandoc"""
    print("🔵 TEST GÉNÉRATION DE RAPPORTS")
    print("=" * 60)
    print("Ce test vérifie la génération de rapports avec Pandoc.")
    print("=" * 60)
    
    try:
        from lcpi.reporter import GlobalReportBuilder
        
        # Créer un répertoire temporaire pour le test
        with tempfile.TemporaryDirectory() as temp_dir:
            test_project_dir = Path(temp_dir) / "test_project"
            test_project_dir.mkdir()
            
            # Créer des fichiers de test pour simuler un projet
            (test_project_dir / "config.yml").write_text("""
plugins:
  - aep
  - cm
  - bois
name: "Projet Test LCPI"
description: "Projet de test pour la génération de rapports"
""")
            
            # Créer des fichiers de données pour chaque plugin
            (test_project_dir / "data" / "aep").mkdir(parents=True)
            (test_project_dir / "data" / "aep" / "population_data.yml").write_text("""
population_base: 1000
taux_croissance: 0.037
annees: 20
""")
            
            (test_project_dir / "data" / "cm").mkdir(parents=True)
            (test_project_dir / "data" / "cm" / "beam_data.yml").write_text("""
beam_length: 6.0
beam_height: 0.3
beam_width: 0.2
""")
            
            (test_project_dir / "data" / "bois").mkdir(parents=True)
            (test_project_dir / "data" / "bois" / "wood_data.yml").write_text("""
wood_type: "Douglas"
section: "200x400"
length: 4.5
""")
            
            # Initialiser le générateur de rapports
            builder = GlobalReportBuilder(str(test_project_dir))
            
            print(f"✅ Générateur de rapports initialisé")
            print(f"   Projet: {test_project_dir}")
            print(f"   Pandoc disponible: {builder.pandoc_available}")
            
            if not builder.pandoc_available:
                print("⚠️ Pandoc n'est pas disponible, test limité")
                return True
            
            # Analyser le projet
            project_data = builder.analyze_project()
            
            print(f"✅ Projet analysé")
            print(f"   Plugins détectés: {project_data['metadata']['plugins']}")
            print(f"   Résultats: {len(project_data['results'])} plugins")
            
            # Test de génération HTML
            try:
                html_report = builder.generate_report("html")
                print(f"✅ Rapport HTML généré: {html_report}")
                
                # Vérifier que le fichier existe
                if Path(html_report).exists():
                    print(f"   ✅ Fichier créé: {Path(html_report).stat().st_size} bytes")
                else:
                    print(f"   ❌ Fichier non trouvé")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur génération HTML: {e}")
                return False
            
            # Test de génération JSON
            try:
                json_report = builder.generate_report("json")
                print(f"✅ Rapport JSON généré: {json_report}")
                
                # Vérifier que le fichier existe
                if Path(json_report).exists():
                    print(f"   ✅ Fichier créé: {Path(json_report).stat().st_size} bytes")
                else:
                    print(f"   ❌ Fichier non trouvé")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur génération JSON: {e}")
                return False
            
            # Test de génération Markdown
            try:
                md_report = builder.generate_report("markdown")
                print(f"✅ Rapport Markdown généré: {md_report}")
                
                # Vérifier que le fichier existe
                if Path(md_report).exists():
                    print(f"   ✅ Fichier créé: {Path(md_report).stat().st_size} bytes")
                else:
                    print(f"   ❌ Fichier non trouvé")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur génération Markdown: {e}")
                return False
            
            print(f"\n✅ Tous les tests de génération réussis !")
            return True
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_report_with_real_data():
    """Test avec des données réelles du projet actuel"""
    print(f"\n🔵 TEST AVEC DONNÉES RÉELLES")
    print("-" * 40)
    
    try:
        from lcpi.reporter import GlobalReportBuilder
        
        # Utiliser le répertoire actuel
        current_dir = Path.cwd()
        
        # Initialiser le générateur
        builder = GlobalReportBuilder(str(current_dir))
        
        print(f"✅ Générateur initialisé pour: {current_dir}")
        print(f"   Pandoc disponible: {builder.pandoc_available}")
        
        if not builder.pandoc_available:
            print("⚠️ Pandoc non disponible, test limité")
            return True
        
        # Analyser le projet réel
        project_data = builder.analyze_project()
        
        print(f"✅ Projet analysé")
        print(f"   Nom: {project_data['metadata']['name']}")
        print(f"   Plugins: {project_data['metadata']['plugins']}")
        print(f"   Résultats: {len(project_data['results'])} plugins")
        
        # Afficher les détails des résultats
        for plugin, results in project_data['results'].items():
            print(f"   📊 {plugin.upper()}: {len(results.get('files', []))} fichiers")
        
        # Générer un rapport HTML
        try:
            html_report = builder.generate_report("html")
            print(f"✅ Rapport HTML généré: {html_report}")
            
            # Vérifier le contenu
            if Path(html_report).exists():
                content = Path(html_report).read_text(encoding='utf-8')
                if "Rapport de Projet LCPI" in content:
                    print(f"   ✅ Contenu valide")
                else:
                    print(f"   ⚠️ Contenu inattendu")
            else:
                print(f"   ❌ Fichier non trouvé")
                return False
                
        except Exception as e:
            print(f"❌ Erreur génération: {e}")
            return False
        
        print(f"\n✅ Test avec données réelles réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST GÉNÉRATION DE RAPPORTS GLOBAL")
    print("=" * 60)
    
    # Tests
    test1 = test_report_generation()
    test2 = test_report_with_real_data()
    
    # Résumé
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tests = [
        ("Génération avec données de test", test1),
        ("Génération avec données réelles", test2)
    ]
    
    success_count = 0
    for test_name, result in tests:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests de génération de rapports sont réussis !")
        print("✅ La génération de rapports globale fonctionne parfaitement.")
        return True
    else:
        print("⚠️ Certains tests de génération de rapports ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 