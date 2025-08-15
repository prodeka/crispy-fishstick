#!/usr/bin/env python3
"""
Script de démonstration des améliorations du système de rapports LCPI-CLI
"""

import sys
import pathlib
from src.lcpi.reporter import ReportGenerator

def create_sample_data():
    """Crée des données d'exemple pour tester les rapports."""
    return [
        {
            "element_id": "Poutre_P1",
            "plugin": "beton",
            "statut": "OK",
            "resultats": {
                "moment_flechissant": "125.5 kN.m",
                "effort_tranchant": "45.2 kN",
                "contrainte_beton": "12.3 MPa",
                "contrainte_acier": "235.0 MPa",
                "verification": "Satisfaisant"
            }
        },
        {
            "element_id": "Canal_C1",
            "plugin": "hydrodrain",
            "statut": "OK",
            "resultats": {
                "debit_calcul": "2.5 m³/s",
                "vitesse_ecoulement": "1.8 m/s",
                "pente_hydraulique": "0.002",
                "diametre_optimal": "800 mm",
                "type_canal": "Béton"
            }
        },
        {
            "element_id": "Panne_T1",
            "plugin": "bois",
            "statut": "Avertissement",
            "resultats": {
                "contrainte_flexion": "8.5 MPa",
                "contrainte_admissible": "10.0 MPa",
                "coefficient_securite": "1.18",
                "verification": "Limite"
            }
        },
        {
            "element_id": "Reservoir_R1",
            "plugin": "hydrodrain",
            "statut": "Erreur",
            "resultats": {
                "volume_calcule": "150 m³",
                "pression_max": "45.0 m",
                "pression_min": "30.0 m",
                "erreur": "Pression insuffisante"
            }
        }
    ]

def test_report_formats():
    """Teste tous les formats de rapports disponibles."""
    print("🚀 Test des améliorations du système de rapports LCPI-CLI")
    print("=" * 60)
    
    # Créer le générateur de rapports
    project_dir = pathlib.Path.cwd()
    generator = ReportGenerator(str(project_dir))
    
    # Créer des données d'exemple
    sample_data = create_sample_data()
    
    print(f"📊 Données d'exemple créées: {len(sample_data)} éléments")
    
    # Tester chaque format
    formats_to_test = [
        ("PDF", "pdf"),
        ("HTML (Template par défaut)", "html"),
        ("HTML (Template technique)", "html"),
        ("DOCX", "docx"),
        ("CSV", "csv")
    ]
    
    for format_name, format_type in formats_to_test:
        print(f"\n🔄 Test du format {format_name}...")
        
        try:
            if format_type == "html":
                # Tester les deux templates HTML
                for template in ["default.html", "technical.html"]:
                    output_path = generator.generate_html_report(sample_data, template)
                    if output_path:
                        print(f"  ✅ Template {template}: {output_path}")
                    else:
                        print(f"  ❌ Échec du template {template}")
            else:
                if format_type == "pdf":
                    output_path = generator.generate_pdf_report(sample_data)
                elif format_type == "docx":
                    output_path = generator.generate_docx_report(sample_data)
                elif format_type == "csv":
                    output_path = generator.generate_csv_report(sample_data)
                
                if output_path:
                    print(f"  ✅ {format_name}: {output_path}")
                else:
                    print(f"  ❌ Échec du format {format_name}")
                    
        except Exception as e:
            print(f"  ❌ Erreur lors de la génération {format_name}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test terminé ! Vérifiez les fichiers générés dans le dossier 'output/'")

def show_usage_examples():
    """Affiche des exemples d'utilisation."""
    print("\n📖 Exemples d'utilisation:")
    print("-" * 40)
    
    examples = [
        ("Rapport PDF standard", "python -m src.lcpi.reporter --format pdf"),
        ("Rapport HTML moderne", "python -m src.lcpi.reporter --format html --template default.html"),
        ("Rapport HTML technique", "python -m src.lcpi.reporter --format html --template technical.html"),
        ("Rapport Word", "python -m src.lcpi.reporter --format docx"),
        ("Export CSV", "python -m src.lcpi.reporter --format csv"),
        ("Sortie JSON", "python -m src.lcpi.reporter --format json")
    ]
    
    for desc, cmd in examples:
        print(f"  {desc}:")
        print(f"    {cmd}")
        print()

def main():
    """Fonction principale."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_usage_examples()
        return
    
    test_report_formats()
    show_usage_examples()

if __name__ == "__main__":
    main() 