#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration du logo LCPI Engineering
dans tous les templates améliorés.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_logo_in_html():
    """Teste la présence du logo dans le template HTML."""
    try:
        template_path = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates" / "network_optimize_unified_enhanced.html"
        
        if not template_path.exists():
            print("❌ Template HTML non trouvé")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier la présence du logo
        logo_checks = [
            ('🏗️', "Emoji bâtiment"),
            ('LCPI Engineering', "Titre LCPI"),
            ('logo-section', "Classe CSS logo-section"),
            ('logo-icon', "Classe CSS logo-icon"),
            ('logo-title', "Classe CSS logo-title"),
            ('logo-subtitle', "Classe CSS logo-subtitle"),
            ('logo-bounce', "Animation CSS logo-bounce")
        ]
        
        all_present = True
        for check, description in logo_checks:
            if check in content:
                print(f"✅ {description} : Présent")
            else:
                print(f"❌ {description} : Manquant")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Erreur lors du test HTML : {e}")
        return False

def test_logo_in_markdown():
    """Teste la présence du logo dans le template Markdown."""
    try:
        template_path = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates" / "network_optimize_unified_enhanced.md"
        
        if not template_path.exists():
            print("❌ Template Markdown non trouvé")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier la présence du logo
        logo_checks = [
            ('🏗️', "Emoji bâtiment"),
            ('LCPI Engineering', "Titre LCPI"),
            ('Analyse et Dimensionnement Hydraulique', "Sous-titre")
        ]
        
        all_present = True
        for check, description in logo_checks:
            if check in content:
                print(f"✅ {description} : Présent")
            else:
                print(f"❌ {description} : Manquant")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Erreur lors du test Markdown : {e}")
        return False

def test_logo_in_pdf():
    """Teste la présence du logo dans le template PDF."""
    try:
        template_path = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates" / "network_optimize_unified_pdf_enhanced.jinja2"
        
        if not template_path.exists():
            print("❌ Template PDF non trouvé")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier la présence du logo
        logo_checks = [
            ('🏗️', "Emoji bâtiment"),
            ('LCPI Engineering', "Titre LCPI"),
            ('logo-section', "Classe CSS logo-section"),
            ('logo-icon', "Classe CSS logo-icon"),
            ('logo-title', "Classe CSS logo-title"),
            ('logo-subtitle', "Classe CSS logo-subtitle")
        ]
        
        all_present = True
        for check, description in logo_checks:
            if check in content:
                print(f"✅ {description} : Présent")
            else:
                print(f"❌ {description} : Manquant")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Erreur lors du test PDF : {e}")
        return False

def test_logo_consistency():
    """Teste la cohérence du logo entre tous les templates."""
    print("\n🔍 Test de cohérence du logo...")
    
    # Vérifier que tous les templates utilisent le même emoji
    emoji = "🏗️"
    company_name = "LCPI Engineering"
    subtitle = "Analyse et Dimensionnement Hydraulique"
    
    templates = [
        ("HTML", "network_optimize_unified_enhanced.html"),
        ("Markdown", "network_optimize_unified_enhanced.md"),
        ("PDF", "network_optimize_unified_pdf_enhanced.jinja2")
    ]
    
    all_consistent = True
    for template_name, filename in templates:
        template_path = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates" / filename
        
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la cohérence
            if emoji in content and company_name in content and subtitle in content:
                print(f"✅ {template_name} : Logo cohérent")
            else:
                print(f"❌ {template_name} : Logo incohérent")
                all_consistent = False
        else:
            print(f"❌ {template_name} : Fichier non trouvé")
            all_consistent = False
    
    return all_consistent

def main():
    """Fonction principale de test."""
    print("🏗️ Test d'Intégration du Logo LCPI Engineering")
    print("=" * 50)
    
    # Test des templates individuels
    print("\n1️⃣ Test du template HTML...")
    html_ok = test_logo_in_html()
    
    print("\n2️⃣ Test du template Markdown...")
    md_ok = test_logo_in_markdown()
    
    print("\n3️⃣ Test du template PDF...")
    pdf_ok = test_logo_in_pdf()
    
    # Test de cohérence
    print("\n4️⃣ Test de cohérence...")
    consistency_ok = test_logo_consistency()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"HTML        : {'✅ OK' if html_ok else '❌ ÉCHEC'}")
    print(f"Markdown    : {'✅ OK' if md_ok else '❌ ÉCHEC'}")
    print(f"PDF         : {'✅ OK' if pdf_ok else '❌ ÉCHEC'}")
    print(f"Cohérence   : {'✅ OK' if consistency_ok else '❌ ÉCHEC'}")
    
    if all([html_ok, md_ok, pdf_ok, consistency_ok]):
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("🏗️ Le logo LCPI Engineering est correctement intégré dans tous les templates.")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez l'intégration du logo.")
    
    return all([html_ok, md_ok, pdf_ok, consistency_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
