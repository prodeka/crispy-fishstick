#!/usr/bin/env python3
"""
Script de test pour les nouveaux formats de rapport de la commande network-optimize-unified.
"""

import json
import tempfile
from pathlib import Path
from src.lcpi.reporting.markdown_generator import MarkdownGenerator
from src.lcpi.reporting.pdf_generator import PDFGenerator

def test_markdown_generator():
    """Test du générateur Markdown."""
    print("🧪 Test du générateur Markdown...")
    
    # Données de test
    index_data = {
        "meta": {
            "method": "nested",
            "solvers": ["epanet", "lcpi"],
            "constraints": {
                "pressure_min_m": 12.0,
                "velocity_max_m_s": 2.0
            }
        }
    }
    
    outputs = {
        "epanet": {
            "meta": {"method": "nested", "source": "test.inp"},
            "proposals": [
                {
                    "id": "nested_best",
                    "CAPEX": 7500.0,
                    "H_tank_m": 17.0,
                    "constraints_ok": True,
                    "diameters_mm": {"N1_N2": 156, "N2_N3": 108}
                }
            ],
            "execution_time": 1.5,
            "integrity": {
                "checksum": "test123",
                "signature": "sig123",
                "signature_valid": True
            }
        },
        "lcpi": {
            "meta": {"method": "nested", "source": "test.inp"},
            "proposals": [
                {
                    "id": "nested_best",
                    "CAPEX": 7200.0,
                    "H_tank_m": 16.5,
                    "constraints_ok": True,
                    "diameters_mm": {"N1_N2": 150, "N2_N3": 100}
                }
            ],
            "execution_time": 0.8,
            "integrity": {
                "checksum": "test456",
                "signature": "sig456",
                "signature_valid": True
            }
        }
    }
    
    try:
        # Générer le rapport Markdown
        md_generator = MarkdownGenerator()
        md_content = md_generator.generate_optimization_report(index_data, outputs)
        
        # Sauvegarder le rapport
        with open("test_rapport_optimisation.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print("✅ Rapport Markdown généré avec succès: test_rapport_optimisation.md")
        print(f"📏 Taille: {len(md_content)} caractères")
        
        # Afficher un aperçu
        print("\n📋 Aperçu du rapport:")
        lines = md_content.split('\n')[:20]
        for line in lines:
            print(f"   {line}")
        if len(md_content.split('\n')) > 20:
            print("   ...")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération Markdown: {e}")
        import traceback
        traceback.print_exc()

def test_pdf_generator():
    """Test du générateur PDF."""
    print("\n🧪 Test du générateur PDF...")
    
    # Données de test (mêmes que pour Markdown)
    index_data = {
        "meta": {
            "method": "nested",
            "solvers": ["epanet", "lcpi"],
            "constraints": {
                "pressure_min_m": 12.0,
                "velocity_max_m_s": 2.0
            }
        }
    }
    
    outputs = {
        "epanet": {
            "meta": {"method": "nested", "source": "test.inp"},
            "proposals": [
                {
                    "id": "nested_best",
                    "CAPEX": 7500.0,
                    "H_tank_m": 17.0,
                    "constraints_ok": True,
                    "diameters_mm": {"N1_N2": 156, "N2_N3": 108}
                }
            ],
            "execution_time": 1.5,
            "integrity": {
                "checksum": "test123",
                "signature": "sig123",
                "signature_valid": True
            }
        },
        "lcpi": {
            "meta": {"method": "nested", "source": "test.inp"},
            "proposals": [
                {
                    "id": "nested_best",
                    "CAPEX": 7200.0,
                    "H_tank_m": 16.5,
                    "constraints_ok": True,
                    "diameters_mm": {"N1_N2": 150, "N2_N3": 100}
                }
            ],
            "execution_time": 0.8,
            "integrity": {
                "checksum": "test456",
                "signature": "sig456",
                "signature_valid": True
            }
        }
    }
    
    try:
        # Générer le rapport PDF
        pdf_generator = PDFGenerator()
        pdf_content = pdf_generator.generate_optimization_report(index_data, outputs)
        
        # Sauvegarder le rapport
        with open("test_rapport_optimisation.pdf", "wb") as f:
            f.write(pdf_content)
        
        print("✅ Rapport PDF généré avec succès: test_rapport_optimisation.pdf")
        print(f"📏 Taille: {len(pdf_content)} bytes")
        
        # Vérifier que c'est bien un PDF
        if pdf_content.startswith(b'%PDF'):
            print("✅ Format PDF valide détecté")
        else:
            print("⚠️  Le contenu ne semble pas être un PDF standard")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération PDF: {e}")
        import traceback
        traceback.print_exc()

def test_command_integration():
    """Test de l'intégration avec la commande network-optimize-unified."""
    print("\n🧪 Test de l'intégration avec la commande...")
    
    try:
        # Simuler l'appel de la commande
        from src.lcpi.aep.commands.network_optimize_unified import _generate_reports
        
        # Données de test
        index_data = {
            "meta": {
                "method": "nested",
                "solvers": ["epanet"]
            },
            "results": {"epanet": "test.json"}
        }
        
        outputs = {
            "epanet": {
                "meta": {"method": "nested", "source": "test.inp"},
                "proposals": [
                    {
                        "id": "nested_best",
                        "CAPEX": 7500.0,
                        "H_tank_m": 17.0,
                        "constraints_ok": True
                    }
                ]
            }
        }
        
        # Test avec un dossier temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            print(f"📁 Dossier temporaire: {temp_path}")
            
            # Test des différents formats
            for report_format in ["html", "md", "pdf"]:
                try:
                    print(f"   🔄 Test du format {report_format}...")
                    _generate_reports(index_data, outputs, report_format, temp_path, True)
                    print(f"   ✅ Format {report_format} généré avec succès")
                except Exception as e:
                    print(f"   ❌ Erreur avec le format {report_format}: {e}")
        
        print("✅ Tests d'intégration terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests d'intégration: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale de test."""
    print("🚀 Démarrage des tests des nouveaux formats de rapport")
    print("=" * 60)
    
    # Tests des générateurs
    test_markdown_generator()
    test_pdf_generator()
    
    # Test d'intégration
    test_command_integration()
    
    print("\n" + "=" * 60)
    print("🏁 Tests terminés")
    print("\n📁 Fichiers générés:")
    
    # Lister les fichiers créés
    for file_path in Path(".").glob("test_rapport_optimisation.*"):
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   📄 {file_path.name} ({size} bytes)")

if __name__ == "__main__":
    main()
