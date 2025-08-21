#!/usr/bin/env python3
"""
Script de démonstration des templates améliorés de network-optimize-unified.
Montre comment utiliser les différents formats de rapport (HTML, Markdown, PDF).
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def load_real_data():
    """Charge des données réelles depuis un fichier de résultats existant."""
    # Chercher un fichier de résultats récent
    results_dir = Path(__file__).parent.parent / "results"
    if not results_dir.exists():
        print("❌ Dossier 'results' non trouvé. Utilisation de données d'exemple.")
        return create_sample_data()
    
    # Chercher le fichier le plus récent
    json_files = list(results_dir.glob("*.json"))
    if not json_files:
        print("❌ Aucun fichier JSON trouvé dans 'results'. Utilisation de données d'exemple.")
        return create_sample_data()
    
    # Prendre le fichier le plus récent
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"📁 Utilisation du fichier de résultats : {latest_file.name}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Normaliser les données si nécessaire
        if "hydraulics" not in data and "statistics" in data:
            data["hydraulics"] = {"statistics": data["statistics"]}
        
        return data
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {latest_file}: {e}")
        print("🔄 Utilisation de données d'exemple...")
        return create_sample_data()

def create_sample_data():
    """Crée des données d'exemple si aucun fichier réel n'est disponible."""
    return {
        "meta": {
            "method": "Algorithme Génétique",
            "solver": "EPANET",
            "generations": 15,
            "population": 25,
            "duration_seconds": 45.7,
            "solver_calls": 375,
            "pressure_min_m": 10,
            "velocity_max_m_s": 3.0,
            "hmax": 50
        },
        "proposals": [
            {
                "id": "OPT_001",
                "CAPEX": 12500000,
                "H_tank_m": 28.5,
                "constraints_ok": True,
                "performance_index": 0.892,
                "diameters_mm": {
                    "N1_N2": 200,
                    "N2_N3": 150,
                    "N3_N4": 100,
                    "N4_N5": 100,
                    "N5_N6": 80,
                    "N6_N7": 80,
                    "N7_N8": 60,
                    "N8_N9": 60,
                    "N9_N10": 40
                }
            }
        ],
        "hydraulics": {
            "statistics": {
                "pressures": {
                    "count": 10,
                    "min": 12.5,
                    "max": 45.2,
                    "mean": 28.7,
                    "median": 29.1,
                    "std": 8.9,
                    "q25": 22.3,
                    "q75": 35.8,
                    "pct_lt_10m": 0.0,
                    "pct_lt_15m": 10.0,
                    "pct_lt_20m": 25.0
                },
                "velocities": {
                    "count": 9,
                    "min": 0.45,
                    "max": 2.85,
                    "mean": 1.67,
                    "median": 1.72,
                    "std": 0.78
                },
                "flows": {
                    "count": 9,
                    "min": -0.23,
                    "max": 0.45,
                    "mean": 0.12,
                    "median": 0.15,
                    "std": 0.18,
                    "min_abs": 0.05,
                    "max_abs": 0.45,
                    "mean_abs": 0.23,
                    "median_abs": 0.18,
                    "positive_flows": 7,
                    "negative_flows": 2,
                    "zero_flows": 0
                },
                "diameters": {
                    "count": 9,
                    "min": 40,
                    "max": 200,
                    "mean": 98.9,
                    "median": 100,
                    "std": 58.7
                },
                "headlosses": {
                    "count": 9,
                    "min": 0.12,
                    "max": 3.45,
                    "mean": 1.78,
                    "median": 1.65,
                    "std": 0.89
                },
                "performance_index": 0.892
            }
        },
        "constraints": {
            "pressure_min_m": 10,
            "velocity_max_m_s": 3.0,
            "hmax": 50
        }
    }

def generate_html_report(data, output_dir):
    """Génère un rapport HTML amélioré."""
    try:
        from jinja2 import Environment, FileSystemLoader
        
        template_dir = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        
        template = env.get_template("network_optimize_unified_enhanced.html")
        
        context = {
            "meta": data.get("meta", {}),
            "proposals": data.get("proposals", []),
            "hydraulics": data.get("hydraulics", {}),
            "constraints": data.get("constraints", {}),
            "input_file": data.get("input_file", "N/A"),
            "version": "1.0.0",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        html_content = template.render(**context)
        
        output_file = output_dir / "rapport_enhanced.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Rapport HTML généré : {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération HTML : {e}")
        return None

def generate_markdown_report(data, output_dir):
    """Génère un rapport Markdown amélioré."""
    try:
        from jinja2 import Environment, FileSystemLoader
        
        template_dir = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        
        template = env.get_template("network_optimize_unified_enhanced.md")
        
        context = {
            "meta": data.get("meta", {}),
            "proposals": data.get("proposals", []),
            "hydraulics": data.get("hydraulics", {}),
            "constraints": data.get("constraints", {}),
            "input_file": data.get("input_file", "N/A"),
            "version": "1.0.0",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        md_content = template.render(**context)
        
        output_file = output_dir / "rapport_enhanced.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Rapport Markdown généré : {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération Markdown : {e}")
        return None

def generate_pdf_report(data, output_dir):
    """Génère un rapport PDF amélioré."""
    try:
        from lcpi.reporting.network_optimize_unified_pdf_generator import NetworkOptimizeUnifiedPDFGenerator
        
        generator = NetworkOptimizeUnifiedPDFGenerator()
        
        pdf_content = generator.generate_pdf_report(
            result_data=data,
            input_file=data.get("input_file", "N/A"),
            version="1.0.0"
        )
        
        output_file = output_dir / "rapport_enhanced.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ Rapport PDF généré : {output_file}")
        print(f"📊 Taille du PDF : {len(pdf_content)} bytes")
        return output_file
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération PDF : {e}")
        return None

def generate_all_reports(data, output_dir):
    """Génère tous les formats de rapport."""
    print("🚀 Génération de tous les formats de rapport...")
    print("=" * 50)
    
    # Créer le dossier de sortie
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Générer les rapports
    html_file = generate_html_report(data, output_dir)
    md_file = generate_markdown_report(data, output_dir)
    pdf_file = generate_pdf_report(data, output_dir)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA GÉNÉRATION")
    print("=" * 50)
    print(f"HTML     : {'✅' if html_file else '❌'}")
    print(f"Markdown : {'✅' if md_file else '❌'}")
    print(f"PDF      : {'✅' if pdf_file else '❌'}")
    
    if all([html_file, md_file, pdf_file]):
        print("\n🎉 Tous les rapports ont été générés avec succès !")
        print(f"📁 Dossier de sortie : {output_dir}")
    else:
        print("\n⚠️ Certains rapports n'ont pas pu être générés.")
    
    return html_file, md_file, pdf_file

def show_report_preview(data):
    """Affiche un aperçu des données qui seront utilisées pour les rapports."""
    print("📋 APERÇU DES DONNÉES")
    print("=" * 30)
    
    meta = data.get("meta", {})
    proposals = data.get("proposals", [])
    hydraulics = data.get("hydraulics", {})
    
    print(f"Méthode     : {meta.get('method', 'N/A')}")
    print(f"Solveur     : {meta.get('solver', 'N/A')}")
    print(f"Générations : {meta.get('generations', 'N/A')}")
    print(f"Population  : {meta.get('population', 'N/A')}")
    print(f"Durée       : {meta.get('duration_seconds', 0):.1f}s")
    print(f"Simulations : {meta.get('solver_calls', 0)}")
    
    if proposals:
        best = proposals[0]
        print(f"\n🏆 Meilleure proposition :")
        print(f"   CAPEX : {best.get('CAPEX', 0):,} FCFA")
        print(f"   Hauteur réservoir : {best.get('H_tank_m', 0) or 0:.1f} m")
        print(f"   Contraintes OK : {'✅' if best.get('constraints_ok') else '❌'}")
        print(f"   Conduites : {len(best.get('diameters_mm', {}) or {})}")
    
    if hydraulics and "statistics" in hydraulics:
        stats = hydraulics["statistics"]
        print(f"\n📊 Statistiques hydrauliques :")
        if "pressures" in stats:
            p = stats["pressures"]
            print(f"   Pressions : {p.get('count', 0)} nœuds, {p.get('min', 0):.1f}-{p.get('max', 0):.1f} m")
        if "flows" in stats:
            f = stats["flows"]
            print(f"   Débits : {f.get('count', 0)} conduites, {f.get('positive_flows', 0)} sens normal, {f.get('negative_flows', 0)} sens inverse")

def main():
    """Fonction principale."""
    print("🎨 Démonstration des Templates Améliorés de network-optimize-unified")
    print("=" * 70)
    
    # Charger ou créer les données
    print("\n1️⃣ Chargement des données...")
    data = load_real_data()
    
    # Afficher l'aperçu
    print("\n2️⃣ Aperçu des données...")
    show_report_preview(data)
    
    # Dossier de sortie
    output_dir = Path(__file__).parent / "rapports_enhanced"
    
    # Générer tous les rapports
    print("\n3️⃣ Génération des rapports...")
    html_file, md_file, pdf_file = generate_all_reports(data, output_dir)
    
    # Instructions d'utilisation
    print("\n4️⃣ Instructions d'utilisation :")
    print("=" * 50)
    if html_file:
        print(f"🌐 Rapport HTML : Ouvrez {html_file} dans votre navigateur")
    if md_file:
        print(f"📝 Rapport Markdown : Ouvrez {md_file} dans un éditeur Markdown")
    if pdf_file:
        print(f"📄 Rapport PDF : Ouvrez {pdf_file} avec un lecteur PDF")
    
    print("\n💡 Pour intégrer ces templates dans votre workflow :")
    print("   - Utilisez --report html pour le format HTML")
    print("   - Utilisez --report md pour le format Markdown")
    print("   - Utilisez --report pdf pour le format PDF")
    
    return all([html_file, md_file, pdf_file])

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Démonstration terminée avec succès !")
    else:
        print("\n⚠️ La démonstration a rencontré des problèmes.")
    
    sys.exit(0 if success else 1)