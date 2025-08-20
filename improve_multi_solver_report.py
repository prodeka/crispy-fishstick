#!/usr/bin/env python3
"""
Script pour améliorer le rapport multi-solveurs existant
"""

import json
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.reporting.report_generator import ReportGenerator

def improve_multi_solver_report():
    """Améliore le rapport multi-solveurs existant"""
    
    # Chemin vers les templates
    template_dir = Path("src/lcpi/reporting/templates")
    
    # Créer le générateur de rapports
    generator = ReportGenerator(template_dir)
    
    # Chemin vers le fichier multi-solveurs
    multi_solver_file = Path("results/out_multi_multi.json")
    
    if not multi_solver_file.exists():
        print(f"❌ Fichier multi-solveurs non trouvé: {multi_solver_file}")
        return False
    
    # Métadonnées du projet améliorées
    project_metadata = {
        "nom_projet": "Optimisation Réseau Multi-Solveurs",
        "client": "Projet LCPI",
        "description": "Comparaison des résultats d'optimisation entre EPANET et LCPI",
        "auteurs": [
            {"nom": "Équipe LCPI", "role": "Développement"}
        ]
    }
    
    try:
        # Générer le rapport amélioré
        print("🔄 Génération du rapport multi-solveurs amélioré...")
        html_content = generator.generate_html_report(
            selected_logs_paths=[multi_solver_file],
            project_metadata=project_metadata,
            lcpi_version="1.0.0"
        )
        
        # Sauvegarder le rapport amélioré
        output_file = Path("results/out_multi_tabs_improved.html")
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"✅ Rapport amélioré généré avec succès: {output_file}")
        print(f"📊 Taille du rapport: {len(html_content)} caractères")
        
        # Comparer avec l'ancien rapport
        old_report_file = Path("results/out_multi_tabs.html")
        if old_report_file.exists():
            old_content = old_report_file.read_text(encoding='utf-8')
            print(f"📈 Amélioration: {len(html_content) - len(old_content)} caractères supplémentaires")
        
        # Vérifier les améliorations
        improvements = [
            "Comparaison Multi-Solveurs",
            "Vue d'ensemble",
            "Comparaison détaillée",
            "Analyse hydraulique",
            "Analyse des diamètres",
            "cost-bar",
            "kpi-grid",
            "comparison-table"
        ]
        
        print("\n🔍 Vérification des améliorations:")
        for improvement in improvements:
            if improvement in html_content:
                print(f"  ✅ {improvement}")
            else:
                print(f"  ❌ {improvement}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport amélioré: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_comparison_script():
    """Crée un script pour comparer les deux rapports"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script pour comparer les rapports multi-solveurs
"""

import webbrowser
from pathlib import Path

def open_reports():
    """Ouvre les deux rapports dans le navigateur"""
    
    old_report = Path("results/out_multi_tabs.html")
    new_report = Path("results/out_multi_tabs_improved.html")
    
    if old_report.exists():
        print(f"🌐 Ouverture de l'ancien rapport: {old_report}")
        webbrowser.open(f"file://{old_report.absolute()}")
    
    if new_report.exists():
        print(f"🌐 Ouverture du nouveau rapport: {new_report}")
        webbrowser.open(f"file://{new_report.absolute()}")
    
    print("📋 Comparaison:")
    print("  - Ancien rapport: out_multi_tabs.html")
    print("  - Nouveau rapport: out_multi_tabs_improved.html")

if __name__ == "__main__":
    open_reports()
'''
    
    script_file = Path("compare_reports.py")
    script_file.write_text(script_content, encoding='utf-8')
    print(f"📝 Script de comparaison créé: {script_file}")

def main():
    """Fonction principale"""
    print("🚀 Amélioration du rapport multi-solveurs")
    print("=" * 50)
    
    # Améliorer le rapport
    success = improve_multi_solver_report()
    
    if success:
        # Créer le script de comparaison
        create_comparison_script()
        
        print("\n" + "=" * 50)
        print("🎉 Amélioration terminée avec succès!")
        print("\n📋 Fichiers générés:")
        print("  - results/out_multi_tabs_improved.html (nouveau rapport)")
        print("  - compare_reports.py (script de comparaison)")
        print("\n🔧 Pour comparer les rapports:")
        print("  python compare_reports.py")
        print("\n🔧 Pour tester avec la commande originale:")
        print("  lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solvers epanet,lcpi --pression-min 12 --vitesse-max 2.0 --output results\\out_multi.json --report html --no-log")
        
        return True
    else:
        print("\n❌ Échec de l'amélioration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
