#!/usr/bin/env python3
"""
Script de test pour vérifier les templates améliorés de network-optimize-unified.
Teste la génération HTML, Markdown et PDF avec des données d'exemple.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def create_sample_data():
    """Crée des données d'exemple pour tester les templates."""
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
            },
            {
                "id": "OPT_002",
                "CAPEX": 13800000,
                "H_tank_m": 32.1,
                "constraints_ok": True,
                "performance_index": 0.876,
                "diameters_mm": {
                    "N1_N2": 250,
                    "N2_N3": 200,
                    "N3_N4": 150,
                    "N4_N5": 100,
                    "N5_N6": 100,
                    "N6_N7": 80,
                    "N7_N8": 80,
                    "N8_N9": 60,
                    "N9_N10": 60
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

def test_html_template():
    """Teste la génération du template HTML amélioré."""
    try:
        from jinja2 import Environment, FileSystemLoader
        
        # Chemin vers les templates
        template_dir = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # Charger le template HTML
        template = env.get_template("network_optimize_unified_enhanced.html")
        
        # Données de test
        data = create_sample_data()
        context = {
            "meta": data["meta"],
            "proposals": data["proposals"],
            "hydraulics": data["hydraulics"],
            "constraints": data["constraints"],
            "input_file": "test_network.inp",
            "version": "1.0.0",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Générer le HTML
        html_content = template.render(**context)
        
        # Sauvegarder le résultat
        output_file = Path(__file__).parent / "test_output_enhanced.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Template HTML généré avec succès : {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération HTML : {e}")
        return False

def test_markdown_template():
    """Teste la génération du template Markdown amélioré."""
    try:
        from jinja2 import Environment, FileSystemLoader
        
        # Chemin vers les templates
        template_dir = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # Charger le template Markdown
        template = env.get_template("network_optimize_unified_enhanced.md")
        
        # Données de test
        data = create_sample_data()
        context = {
            "meta": data["meta"],
            "proposals": data["proposals"],
            "hydraulics": data["hydraulics"],
            "constraints": data["constraints"],
            "input_file": "test_network.inp",
            "version": "1.0.0",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Générer le Markdown
        md_content = template.render(**context)
        
        # Sauvegarder le résultat
        output_file = Path(__file__).parent / "test_output_enhanced.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Template Markdown généré avec succès : {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération Markdown : {e}")
        return False

def test_pdf_template():
    """Teste la génération du template PDF amélioré."""
    try:
        from jinja2 import Environment, FileSystemLoader
        
        # Chemin vers les templates
        template_dir = Path(__file__).parent.parent / "src" / "lcpi" / "reporting" / "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # Charger le template PDF
        template = env.get_template("network_optimize_unified_pdf_enhanced.jinja2")
        
        # Données de test
        data = create_sample_data()
        context = {
            "meta": data["meta"],
            "proposals": data["proposals"],
            "hydraulics": data["hydraulics"],
            "constraints": data["constraints"],
            "input_file": "test_network.inp",
            "version": "1.0.0",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Générer le HTML pour PDF
        html_content = template.render(**context)
        
        # Sauvegarder le résultat
        output_file = Path(__file__).parent / "test_output_enhanced_pdf.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Template PDF généré avec succès : {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération PDF : {e}")
        return False

def test_pdf_generator():
    """Teste le générateur PDF complet."""
    try:
        from lcpi.reporting.network_optimize_unified_pdf_generator import NetworkOptimizeUnifiedPDFGenerator
        
        # Créer le générateur
        generator = NetworkOptimizeUnifiedPDFGenerator()
        
        # Données de test
        data = create_sample_data()
        
        # Générer le PDF
        pdf_content = generator.generate_pdf_report(
            result_data=data,
            input_file="test_network.inp",
            version="1.0.0"
        )
        
        # Sauvegarder le PDF
        output_file = Path(__file__).parent / "test_output_enhanced.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF généré avec succès : {output_file}")
        print(f"📊 Taille du PDF : {len(pdf_content)} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération PDF : {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🧪 Test des Templates Améliorés de network-optimize-unified")
    print("=" * 60)
    
    # Test des templates individuels
    print("\n1️⃣ Test du template HTML...")
    html_ok = test_html_template()
    
    print("\n2️⃣ Test du template Markdown...")
    md_ok = test_markdown_template()
    
    print("\n3️⃣ Test du template PDF...")
    pdf_template_ok = test_pdf_template()
    
    # Test du générateur PDF complet
    print("\n4️⃣ Test du générateur PDF complet...")
    pdf_gen_ok = test_pdf_generator()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"HTML Template     : {'✅ OK' if html_ok else '❌ ÉCHEC'}")
    print(f"Markdown Template : {'✅ OK' if md_ok else '❌ ÉCHEC'}")
    print(f"PDF Template      : {'✅ OK' if pdf_template_ok else '❌ ÉCHEC'}")
    print(f"PDF Generator     : {'✅ OK' if pdf_gen_ok else '❌ ÉCHEC'}")
    
    if all([html_ok, md_ok, pdf_template_ok, pdf_gen_ok]):
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("📁 Les fichiers de sortie sont disponibles dans le dossier 'tools/'")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return all([html_ok, md_ok, pdf_template_ok, pdf_gen_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)