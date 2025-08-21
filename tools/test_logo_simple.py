#!/usr/bin/env python3
"""
Script de test simple pour vérifier l'intégration du logo LCPI Engineering.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_logo_in_templates():
    """Teste la présence du logo dans tous les templates."""
    print("🏗️ Test d'Intégration du Logo LCPI Engineering")
    print("=" * 50)
    
    templates_dir = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates"
    
    # Tests à effectuer
    logo_checks = [
        ('🏗️', "Emoji bâtiment"),
        ('LCPI Engineering', "Titre LCPI"),
        ('Analyse et Dimensionnement Hydraulique', "Sous-titre")
    ]
    
    # Templates à tester
    templates = [
        ("HTML", "network_optimize_unified_enhanced.html"),
        ("Markdown", "network_optimize_unified_enhanced.md"),
        ("PDF", "network_optimize_unified_pdf_enhanced.jinja2")
    ]
    
    all_passed = True
    
    for template_name, filename in templates:
        print(f"\n📄 Test du template {template_name}...")
        template_path = templates_dir / filename
        
        if not template_path.exists():
            print(f"❌ Fichier {filename} non trouvé")
            all_passed = False
            continue
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            template_ok = True
            for check, description in logo_checks:
                if check in content:
                    print(f"  ✅ {description}")
                else:
                    print(f"  ❌ {description} : Manquant")
                    template_ok = False
            
            if template_ok:
                print(f"  🎉 Template {template_name} : OK")
            else:
                print(f"  ⚠️ Template {template_name} : Problèmes détectés")
                all_passed = False
                
        except Exception as e:
            print(f"  ❌ Erreur lors de la lecture : {e}")
            all_passed = False
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ")
    print("=" * 50)
    
    if all_passed:
        print("🎉 Tous les templates contiennent le logo LCPI Engineering !")
        print("🏗️ L'intégration est réussie.")
    else:
        print("⚠️ Certains templates ont des problèmes avec le logo.")
        print("🔧 Vérifiez l'intégration.")
    
    return all_passed

def main():
    """Fonction principale."""
    success = test_logo_in_templates()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
