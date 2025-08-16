#!/usr/bin/env python3
"""
Test du nouveau système de projets LCPI.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_templates():
    """Test de la gestion des templates."""
    print("🧪 Test des templates...")
    
    try:
        from lcpi.core.template_manager import (
            get_available_templates,
            get_template_description,
            get_template_type
        )
        
        templates = get_available_templates()
        print(f"✅ Templates disponibles: {len(templates)}")
        
        for template in templates[:3]:  # Afficher les 3 premiers
            desc = get_template_description(template)
            type_ = get_template_type(template)
            print(f"  - {template}: {type_} - {desc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur templates: {e}")
        return False

def test_examples():
    """Test de la gestion des exemples."""
    print("\n🧪 Test des exemples...")
    
    try:
        from lcpi.core.example_manager import (
            get_available_examples,
            get_example_description,
            get_example_category
        )
        
        examples = get_available_examples()
        print(f"✅ Exemples disponibles: {len(examples)}")
        
        for example in examples[:3]:  # Afficher les 3 premiers
            desc = get_example_description(example)
            cat = get_example_category(example)
            print(f"  - {example}: {cat} - {desc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur exemples: {e}")
        return False

def test_global_config():
    """Test de la configuration globale."""
    print("\n🧪 Test de la configuration globale...")
    
    try:
        from lcpi.core.global_config import global_config
        
        info = global_config.get_config_info()
        print(f"✅ Configuration chargée: {info['config_file']}")
        print(f"  - Projets: {info['total_projects']}")
        print(f"  - Projet actif: {info['active_project']}")
        print(f"  - Sandbox: {'Actif' if info['sandbox_active'] else 'Inactif'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur config globale: {e}")
        return False

def test_project_context():
    """Test du contexte de projet."""
    print("\n🧪 Test du contexte de projet...")
    
    try:
        from lcpi.core.context import project_context
        
        summary = project_context.get_context_summary()
        print(f"✅ Contexte récupéré: {summary['type']}")
        print(f"  - Nom: {summary['name']}")
        print(f"  - Chemin: {summary['path']}")
        print(f"  - Projet actif: {summary['project_active']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur contexte projet: {e}")
        return False

def test_project_creation():
    """Test de la création de projet."""
    print("\n🧪 Test de la création de projet...")
    
    try:
        import shutil
        from lcpi.core.project_manager import project_manager
        
        # Créer un projet de test
        test_project_name = "test_project_system"
        test_project_path = Path.cwd() / test_project_name
        
        # Nettoyer si existe
        if test_project_path.exists():
            shutil.rmtree(test_project_path)
        
        # Créer le projet
        project_path = project_manager.create_project(
            nom_projet=test_project_name,
            force=True
        )
        
        print(f"✅ Projet créé: {project_path}")
        
        # Vérifier la structure
        expected_dirs = ["data", "output", "docs", "temp", "scripts"]
        for dir_name in expected_dirs:
            dir_path = project_path / dir_name
            if dir_path.exists():
                print(f"  ✅ {dir_name}/ créé")
            else:
                print(f"  ❌ {dir_name}/ manquant")
        
        # Vérifier les fichiers
        expected_files = ["lcpi.yml", "README.md", ".gitignore"]
        for file_name in expected_files:
            file_path = project_path / file_name
            if file_path.exists():
                print(f"  ✅ {file_name} créé")
            else:
                print(f"  ❌ {file_name} manquant")
        
        # Nettoyer
        shutil.rmtree(test_project_path)
        print("  🧹 Projet de test supprimé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création projet: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test du nouveau système de projets LCPI")
    print("=" * 50)
    
    tests = [
        test_templates,
        test_examples,
        test_global_config,
        test_project_context,
        test_project_creation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 Résumé des tests:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
