"""
Tests pour le module Rich UI.
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.utils.rich_ui import RichUI, console, show_calculation_results, show_network_diagnostics

class TestRichUI:
    """Tests pour la classe RichUI."""
    
    def test_print_success(self, capsys):
        """Test de la méthode print_success."""
        RichUI.print_success("Test de succès")
        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "Test de succès" in captured.out
    
    def test_print_error(self, capsys):
        """Test de la méthode print_error."""
        RichUI.print_error("Test d'erreur")
        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "Test d'erreur" in captured.out
    
    def test_print_warning(self, capsys):
        """Test de la méthode print_warning."""
        RichUI.print_warning("Test d'avertissement")
        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "Test d'avertissement" in captured.out
    
    def test_print_info(self, capsys):
        """Test de la méthode print_info."""
        RichUI.print_info("Test d'information")
        captured = capsys.readouterr()
        assert "ℹ️" in captured.out
        assert "Test d'information" in captured.out
    
    def test_create_parameters_table(self):
        """Test de la création d'un tableau de paramètres."""
        parameters = {
            "Population": (15000, "habitants"),
            "Dotation": (150, "L/hab/j"),
            "Demande": (2250, "m³/jour")
        }
        
        table = RichUI.create_parameters_table("Test Paramètres", parameters)
        
        assert table.title == "Test Paramètres"
        assert len(table.columns) == 3  # Paramètre, Valeur, Unité
    
    def test_create_results_table(self):
        """Test de la création d'un tableau de résultats."""
        data = [
            {"Année": 2020, "Population": 15000, "Demande": 2250},
            {"Année": 2030, "Population": 18000, "Demande": 2700},
            {"Année": 2050, "Population": 22000, "Demande": 3300}
        ]
        
        table = RichUI.create_results_table("Test Résultats", data)
        
        assert table.title == "Test Résultats"
        assert len(table.columns) == 3  # Année, Population, Demande
    
    def test_create_results_table_empty(self):
        """Test de la création d'un tableau vide."""
        table = RichUI.create_results_table("Test Vide", [])
        
        assert table.title == "Test Vide"
        assert not table.show_header  # Pas d'en-tête pour un tableau vide

class TestShowFunctions:
    """Tests pour les fonctions d'affichage."""
    
    def test_show_calculation_results(self, capsys):
        """Test de l'affichage des résultats de calcul."""
        results = {
            "valeurs": {
                "population": 15000,
                "demande": 2250.5,
                "cout": 150000
            },
            "diagnostics": {
                "validation_ok": True,
                "convergence": False,
                "performance": 0.85
            },
            "iterations": {
                "total": 15,
                "temps": 2.5
            }
        }
        
        show_calculation_results(results, "Test Calcul")
        captured = capsys.readouterr()
        
        assert "Test Calcul" in captured.out
        assert "Valeurs principales" in captured.out
        assert "Diagnostics" in captured.out
        assert "Détails des itérations" in captured.out
    
    def test_show_network_diagnostics(self, capsys):
        """Test de l'affichage des diagnostics réseau."""
        diagnostics = {
            "Connectivité": {"status": "OK", "details": "Tous les nœuds connectés"},
            "Pression": {"status": "ERREUR", "details": "Pression insuffisante au nœud N3"},
            "Vitesse": {"status": "OK", "details": "Vitesses dans les limites"}
        }
        
        show_network_diagnostics(diagnostics)
        captured = capsys.readouterr()
        
        assert "Diagnostics du Réseau" in captured.out
        assert "État du Réseau" in captured.out
        assert "Connectivité" in captured.out
        assert "Pression" in captured.out
        assert "Vitesse" in captured.out

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
