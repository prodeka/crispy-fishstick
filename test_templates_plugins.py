#!/usr/bin/env python3
"""
Test des templates spécifiques par plugin
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_aep_templates():
    """Test des templates AEP"""
    print("🔵 TEST TEMPLATES AEP")
    print("-" * 40)
    
    try:
        from lcpi.templates.plugin_templates import PluginTemplates, generate_plugin_report_content
        
        # Test des templates AEP
        aep_templates = PluginTemplates.get_aep_templates()
        
        print(f"✅ Templates AEP chargés")
        print(f"   Titre: {aep_templates['title']}")
        print(f"   Description: {aep_templates['description']}")
        print(f"   Sections: {len(aep_templates['sections'])}")
        
        # Test de génération de contenu
        test_data = {
            "population": 1000,
            "besoin_brut_m3j": 291.2,
            "debit_pointe_m3s": 0.007
        }
        
        content = generate_plugin_report_content("aep", test_data)
        
        if content and "Rapport AEP" in content:
            print(f"✅ Contenu AEP généré avec succès")
            print(f"   Longueur: {len(content)} caractères")
            return True
        else:
            print(f"❌ Erreur génération contenu AEP")
            return False
            
    except Exception as e:
        print(f"❌ Erreur templates AEP: {e}")
        return False

def test_all_templates():
    """Test de tous les templates"""
    print("🔵 TEST TOUS LES TEMPLATES")
    print("-" * 40)
    
    try:
        from lcpi.templates.plugin_templates import PluginTemplates
        
        all_templates = PluginTemplates.get_all_templates()
        
        print(f"✅ Tous les templates chargés")
        print(f"   Plugins disponibles: {list(all_templates.keys())}")
        
        success_count = 0
        for plugin_name, template in all_templates.items():
            try:
                print(f"   📊 {plugin_name.upper()}:")
                print(f"      Titre: {template['title']}")
                print(f"      Sections: {len(template['sections'])}")
                
                # Vérifier qu'il y a des formules
                total_formulas = 0
                for section in template['sections']:
                    total_formulas += len(section['formulas'])
                
                print(f"      Formules: {total_formulas}")
                
                if total_formulas > 0:
                    success_count += 1
                    print(f"      ✅ OK")
                else:
                    print(f"      ⚠️ Aucune formule")
                    
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
        
        print(f"\n📈 Résultat: {success_count}/{len(all_templates)} plugins avec formules")
        return success_count == len(all_templates)
        
    except Exception as e:
        print(f"❌ Erreur tous les templates: {e}")
        return False

def test_template_generation():
    """Test de génération de contenu pour chaque plugin"""
    print("🔵 TEST GÉNÉRATION DE CONTENU")
    print("-" * 40)
    
    try:
        from lcpi.templates.plugin_templates import generate_plugin_report_content
        
        plugins = ["aep", "cm", "bois", "beton", "hydrodrain"]
        test_data = {"test": "data"}
        
        success_count = 0
        for plugin in plugins:
            try:
                content = generate_plugin_report_content(plugin, test_data)
                
                if content and len(content) > 100:  # Contenu minimal
                    print(f"   ✅ {plugin.upper()}: Contenu généré ({len(content)} caractères)")
                    success_count += 1
                else:
                    print(f"   ❌ {plugin.upper()}: Contenu insuffisant")
                    
            except Exception as e:
                print(f"   ❌ {plugin.upper()}: Erreur - {e}")
        
        print(f"\n📈 Résultat: {success_count}/{len(plugins)} plugins avec contenu généré")
        return success_count == len(plugins)
        
    except Exception as e:
        print(f"❌ Erreur génération contenu: {e}")
        return False

def test_mathematical_formulas():
    """Test des formules mathématiques"""
    print("🔵 TEST FORMULES MATHÉMATIQUES")
    print("-" * 40)
    
    try:
        from lcpi.templates.plugin_templates import PluginTemplates
        
        all_templates = PluginTemplates.get_all_templates()
        
        total_formulas = 0
        plugins_with_formulas = 0
        
        for plugin_name, template in all_templates.items():
            plugin_formulas = 0
            for section in template['sections']:
                for formula in section['formulas']:
                    if 'latex' in formula and formula['latex']:
                        plugin_formulas += 1
                        total_formulas += 1
            
            if plugin_formulas > 0:
                plugins_with_formulas += 1
                print(f"   ✅ {plugin_name.upper()}: {plugin_formulas} formules LaTeX")
            else:
                print(f"   ❌ {plugin_name.upper()}: Aucune formule LaTeX")
        
        print(f"\n📊 Statistiques:")
        print(f"   Total formules: {total_formulas}")
        print(f"   Plugins avec formules: {plugins_with_formulas}/{len(all_templates)}")
        
        return plugins_with_formulas == len(all_templates) and total_formulas > 0
        
    except Exception as e:
        print(f"❌ Erreur formules mathématiques: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST TEMPLATES SPÉCIFIQUES PAR PLUGIN")
    print("=" * 60)
    print("Ce test vérifie les templates et formules par plugin.")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Templates AEP", test_aep_templates),
        ("Tous les templates", test_all_templates),
        ("Génération de contenu", test_template_generation),
        ("Formules mathématiques", test_mathematical_formulas)
    ]
    
    success_count = 0
    for test_name, test_func in tests:
        print(f"\n📊 Test: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                success_count += 1
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    # Résumé
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS TEMPLATES")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ RÉUSSI" if i < success_count else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests de templates sont réussis !")
        print("✅ Les templates spécifiques par plugin fonctionnent parfaitement.")
        return True
    else:
        print("⚠️ Certains tests de templates ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 