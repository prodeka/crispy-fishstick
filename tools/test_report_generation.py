#!/usr/bin/env python3
"""
Script de test pour la génération de rapports.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_report_generation():
    """Test de la génération de rapports."""
    try:
        from lcpi.aep.commands.network_optimize_unified import _generate_reports
        
        # Données de test
        index_data = {
            "meta": {"solvers": ["epanet"]},
            "results": {"epanet": "test.json"}
        }
        
        outputs = {
            "epanet": {
                "meta": {"method": "nested", "solver": "epanet"},
                "proposals": [
                    {
                        "name": "Test Proposal",
                        "CAPEX": 1000000,
                        "constraints_ok": True
                    }
                ]
            }
        }
        
        # Test de génération Markdown
        print("🧪 Test de génération de rapport Markdown...")
        _generate_reports(index_data, outputs, "md", Path("test_output"), True)
        
        print("✅ Test réussi !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_report_generation()
