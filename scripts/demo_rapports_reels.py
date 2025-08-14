#!/usr/bin/env python3
"""
Démonstration des améliorations du système de rapports avec les vraies données du projet
"""

import sys
import pathlib
import subprocess
from src.lcpi.reporter import run_analysis_and_generate_report

def demo_rapports_reels():
    """Démonstration avec les vraies données du projet."""
    print("🚀 Démonstration des rapports améliorés avec les vraies données du projet")
    print("=" * 70)
    
    project_dir = pathlib.Path.cwd()
    print(f"📁 Projet analysé: {project_dir.name}")
    
    # Formats à tester
    formats_to_test = [
        ("PDF", "pdf"),
        ("HTML (Moderne)", "html"),
        ("DOCX", "docx"),
        ("CSV", "csv")
    ]
    
    for format_name, format_type in formats_to_test:
        print(f"\n🔄 Génération du rapport {format_name}...")
        print("-" * 50)
        
        try:
            # Utiliser la fonction principale pour analyser le projet réel
            run_analysis_and_generate_report(str(project_dir), format_type)
            print(f"✅ Rapport {format_name} généré avec succès !")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération du rapport {format_name}: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Démonstration terminée !")
    print("\n📊 Fichiers générés dans le dossier 'output/':")
    
    # Lister les fichiers générés
    output_dir = project_dir / "output"
    if output_dir.exists():
        for file in output_dir.glob("rapport_lcpi.*"):
            size_kb = file.stat().st_size / 1024
            print(f"  📄 {file.name} ({size_kb:.1f} KB)")

def demo_template_personnalise():
    """Démonstration avec un template personnalisé."""
    print("\n🎨 Démonstration avec template personnalisé")
    print("=" * 50)
    
    project_dir = pathlib.Path.cwd()
    
    try:
        # Générer un rapport HTML avec le template technique
        run_analysis_and_generate_report(str(project_dir), "html", "technical.html")
        print("✅ Rapport technique généré avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def show_comparison():
    """Affiche une comparaison des différents formats."""
    print("\n📊 Comparaison des formats de rapports")
    print("=" * 50)
    
    comparison = [
        ("PDF", "✅ Impression parfaite", "❌ Non modifiable", "📋 Rapports finaux"),
        ("HTML", "✅ Interactif et moderne", "❌ Nécessite navigateur", "🌐 Partage web"),
        ("DOCX", "✅ Éditable dans Word", "❌ Dépendant Microsoft", "✏️ Édition ultérieure"),
        ("CSV", "✅ Analyse dans Excel", "❌ Pas de graphiques", "📈 Analyse de données"),
        ("JSON", "✅ Données structurées", "❌ Pas lisible humain", "🔧 Intégration API")
    ]
    
    print(f"{'Format':<8} {'Avantages':<25} {'Inconvénients':<25} {'Usage':<20}")
    print("-" * 80)
    
    for format_name, avantages, inconvenients, usage in comparison:
        print(f"{format_name:<8} {avantages:<25} {inconvenients:<25} {usage:<20}")

def main():
    """Fonction principale."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("""
Usage: python demo_rapports_reels.py [option]

Options:
  --help          Affiche cette aide
  --reels         Démonstration avec vraies données (par défaut)
  --template      Test des templates personnalisés
  --comparison    Comparaison des formats
            """)
            return
        elif sys.argv[1] == "--template":
            demo_template_personnalise()
            return
        elif sys.argv[1] == "--comparison":
            show_comparison()
            return
    
    # Démonstration par défaut
    demo_rapports_reels()
    show_comparison()

if __name__ == "__main__":
    main() 