#!/usr/bin/env python3
"""
Démonstration des fonctionnalités avancées de rapports LCPI-CLI
- Cache intelligent
- Parallélisation
- Synthèse intelligente
- Rapports différentiels
"""

import sys
import pathlib
import json
import time
from src.lcpi.report_enhanced import ReportCache, ReportAnalyzer, ParallelAnalyzer
from src.lcpi.reporter import ReportGenerator

def demo_cache_system():
    """Démonstration du système de cache."""
    print("🔧 Démonstration du système de cache")
    print("=" * 50)
    
    # Créer un cache
    cache = ReportCache("demo_cache")
    
    # Simuler des données de test
    test_data = {
        "element_id": "Test_Element",
        "plugin": "demo",
        "statut": "OK",
        "resultats": {"test": "value"}
    }
    
    # Créer un fichier de test
    test_file = pathlib.Path("test_file.yml")
    test_file.write_text("test content")
    
    # Mettre en cache un résultat
    cache.cache_result(test_file, test_data)
    print("✅ Données mises en cache")
    
    # Récupérer depuis le cache
    cached_result = cache.get_cached_result(test_file)
    if cached_result:
        print("✅ Données récupérées depuis le cache")
        print(f"   Élément: {cached_result['element_id']}")
    else:
        print("❌ Données non trouvées en cache")
    
    # Vider le cache
    cache.clear_cache()
    print("✅ Cache vidé")
    
    # Nettoyer
    test_file.unlink()
    print()

def demo_synthesis():
    """Démonstration de la synthèse intelligente."""
    print("🧠 Démonstration de la synthèse intelligente")
    print("=" * 50)
    
    # Données de test
    test_results = [
        {
            "element_id": "Poutre_P1",
            "plugin": "beton",
            "statut": "OK",
            "resultats": {
                "ratio_flexion": "0.85",
                "coefficient_securite": "1.25",
                "verification": "Satisfaisant"
            }
        },
        {
            "element_id": "Panne_T1",
            "plugin": "bois",
            "statut": "Avertissement",
            "resultats": {
                "ratio_flexion": "0.95",
                "coefficient_securite": "1.05",
                "verification": "Limite"
            }
        },
        {
            "element_id": "Reservoir_R1",
            "plugin": "hydrodrain",
            "statut": "Erreur",
            "resultats": {
                "ratio_pression": "1.15",
                "verification": "Non conforme"
            }
        }
    ]
    
    # Générer la synthèse
    synthesis = ReportAnalyzer.generate_synthesis(test_results)
    
    print(f"📊 Total éléments: {synthesis['total_elements']}")
    print(f"🎯 Taux de succès: {synthesis['success_rate']:.1f}%")
    print(f"🔧 Plugins utilisés: {', '.join(synthesis['plugins_used'])}")
    print(f"⚠️  Avertissements: {len(synthesis['warnings'])}")
    print(f"❌ Erreurs: {len(synthesis['errors'])}")
    print(f"📈 Ratios critiques: {len(synthesis['critical_ratios'])}")
    
    print("\n📋 Ratios critiques (Top 3):")
    for i, ratio in enumerate(synthesis['critical_ratios'][:3], 1):
        print(f"   {i}. {ratio['element']} - {ratio['parameter']}: {ratio['value']:.2f} ({ratio['status']})")
    
    print()

def demo_comparison():
    """Démonstration de la comparaison de rapports."""
    print("🔄 Démonstration de la comparaison de rapports")
    print("=" * 50)
    
    # Rapport précédent
    previous_results = [
        {
            "element_id": "Poutre_P1",
            "plugin": "beton",
            "statut": "OK",
            "resultats": {
                "ratio_flexion": "0.80",
                "coefficient_securite": "1.20"
            }
        },
        {
            "element_id": "Panne_T1",
            "plugin": "bois",
            "statut": "OK",
            "resultats": {
                "ratio_flexion": "0.90",
                "coefficient_securite": "1.10"
            }
        }
    ]
    
    # Rapport actuel
    current_results = [
        {
            "element_id": "Poutre_P1",
            "plugin": "beton",
            "statut": "OK",
            "resultats": {
                "ratio_flexion": "0.85",
                "coefficient_securite": "1.25"
            }
        },
        {
            "element_id": "Panne_T1",
            "plugin": "bois",
            "statut": "Avertissement",
            "resultats": {
                "ratio_flexion": "0.95",
                "coefficient_securite": "1.05"
            }
        },
        {
            "element_id": "Reservoir_R1",
            "plugin": "hydrodrain",
            "statut": "Erreur",
            "resultats": {
                "ratio_pression": "1.15"
            }
        }
    ]
    
    # Comparer les rapports
    comparison = ReportAnalyzer.compare_reports(current_results, previous_results)
    
    print(f"📊 Résumé des changements:")
    print(f"   • Éléments ajoutés: {comparison['summary_changes']['elements_added']}")
    print(f"   • Éléments supprimés: {comparison['summary_changes']['elements_removed']}")
    print(f"   • Éléments modifiés: {comparison['summary_changes']['elements_modified']}")
    
    print(f"\n📝 Éléments ajoutés: {', '.join(comparison['added_elements'])}")
    print(f"🗑️  Éléments supprimés: {', '.join(comparison['removed_elements'])}")
    
    print(f"\n🔧 Modifications détaillées:")
    for mod in comparison['modified_elements']:
        print(f"   • {mod['element_id']}:")
        for change in mod['changes']:
            if change['type'] == 'numeric' and 'change_percent' in change:
                print(f"     - {change['field']}: {change['old']} → {change['new']} ({change['change_percent']:+.1f}%)")
            else:
                print(f"     - {change['field']}: {change['old']} → {change['new']}")
    
    print()

def demo_parallel_analysis():
    """Démonstration de l'analyse parallèle."""
    print("⚡ Démonstration de l'analyse parallèle")
    print("=" * 50)
    
    # Créer un cache pour la démo
    cache = ReportCache("parallel_demo_cache")
    
    # Créer l'analyseur parallèle
    analyzer = ParallelAnalyzer(cache=cache, max_workers=2)
    
    # Configuration des plugins
    plugin_commands = {
        "cm": "calc",
        "bois": "check",
        "beton": "calc",
        "hydrodrain": "calc"
    }
    
    project_dir = pathlib.Path.cwd()
    
    print(f"📁 Projet: {project_dir.name}")
    print(f"🔧 Workers: {analyzer.max_workers}")
    print(f"💾 Cache: {'Activé' if cache else 'Désactivé'}")
    
    # Mesurer le temps
    start_time = time.time()
    
    # Analyser le projet
    results = analyzer.analyze_project_parallel(project_dir, plugin_commands)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️  Temps d'analyse: {duration:.2f} secondes")
    print(f"📊 Éléments analysés: {len(results)}")
    
    # Afficher quelques résultats
    if results:
        print(f"\n📋 Exemples de résultats:")
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result.get('element_id', 'Inconnu')} ({result.get('plugin', 'Inconnu')}) - {result.get('statut', 'Inconnu')}")
    
    print()

def demo_enhanced_report():
    """Démonstration du rapport amélioré avec toutes les fonctionnalités."""
    print("🚀 Démonstration du rapport amélioré complet")
    print("=" * 50)
    
    # Créer le générateur avec cache et parallélisation
    generator = ReportGenerator(
        project_dir=str(pathlib.Path.cwd()),
        enable_cache=True,
        max_workers=4
    )
    
    # Analyser le projet en parallèle
    plugin_commands = {
        "cm": "calc",
        "bois": "check",
        "beton": "calc",
        "hydrodrain": "calc"
    }
    
    print("🔄 Analyse du projet en cours...")
    results = generator.analyze_project_parallel(plugin_commands)
    
    if results:
        # Générer la synthèse
        synthesis = ReportAnalyzer.generate_synthesis(results)
        
        print(f"📊 Synthèse générée:")
        print(f"   • Total éléments: {synthesis['total_elements']}")
        print(f"   • Taux de succès: {synthesis['success_rate']:.1f}%")
        print(f"   • Ratios critiques: {len(synthesis['critical_ratios'])}")
        
        # Générer un rapport HTML avec synthèse
        print("\n📄 Génération du rapport HTML avec synthèse...")
        output_path = generator.generate_html_report(results, "default.html", synthesis)
        
        if output_path:
            print(f"✅ Rapport généré: {output_path}")
        else:
            print("❌ Échec de la génération du rapport")
    else:
        print("❌ Aucun résultat à analyser")
    
    print()

def show_usage_examples():
    """Affiche des exemples d'utilisation des nouvelles fonctionnalités."""
    print("📖 Exemples d'utilisation des fonctionnalités avancées:")
    print("=" * 60)
    
    examples = [
        ("Cache intelligent", "python -m src.lcpi.reporter --enable-cache"),
        ("Parallélisation", "python -m src.lcpi.reporter --max-workers 8"),
        ("Comparaison de rapports", "python -m src.lcpi.reporter --compare-with rapport_precedent.json"),
        ("Synthèse intelligente", "python -m src.lcpi.reporter --format html --synthesis"),
        ("Toutes les fonctionnalités", "python -m src.lcpi.reporter --enable-cache --max-workers 4 --compare-with ancien.json --format html")
    ]
    
    for desc, cmd in examples:
        print(f"  {desc}:")
        print(f"    {cmd}")
        print()

def main():
    """Fonction principale."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("""
Usage: python demo_advanced_features.py [option]

Options:
  --help          Affiche cette aide
  --cache         Test du système de cache
  --synthesis     Test de la synthèse intelligente
  --comparison    Test de la comparaison de rapports
  --parallel      Test de l'analyse parallèle
  --full          Test complet avec toutes les fonctionnalités
            """)
            return
        elif sys.argv[1] == "--cache":
            demo_cache_system()
            return
        elif sys.argv[1] == "--synthesis":
            demo_synthesis()
            return
        elif sys.argv[1] == "--comparison":
            demo_comparison()
            return
        elif sys.argv[1] == "--parallel":
            demo_parallel_analysis()
            return
        elif sys.argv[1] == "--full":
            demo_enhanced_report()
            return
    
    # Démonstration complète par défaut
    print("🎯 DÉMONSTRATION DES FONCTIONNALITÉS AVANCÉES LCPI-CLI")
    print("=" * 70)
    
    demo_cache_system()
    demo_synthesis()
    demo_comparison()
    demo_parallel_analysis()
    demo_enhanced_report()
    show_usage_examples()
    
    print("🎉 Démonstration terminée !")

if __name__ == "__main__":
    main() 