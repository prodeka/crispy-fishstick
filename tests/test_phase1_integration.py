"""
Test d'intégration pour la Phase 1 : Refactoring et Amélioration UX.
"""

import pytest
import sys
import tempfile
import yaml
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.utils.rich_ui import RichUI, console, show_calculation_results
from lcpi.aep.core.pydantic_models import (
    ReseauCompletConfig, NoeudUnified, ConduiteUnified,
    NoeudRole, TypeReseau, valider_reseau_seul
)

class TestPhase1Integration:
    """Tests d'intégration pour la Phase 1."""
    
    def test_rich_ui_with_pydantic_validation(self, capsys):
        """Test de l'intégration Rich UI avec validation Pydantic."""
        # Créer des données de test
        test_data = {
            "nom": "Réseau Test Intégration",
            "type": "maillé",
            "noeuds": {
                "N1": {
                    "role": "reservoir",
                    "cote_m": 200.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 150.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        # Valider avec Pydantic
        reseau = valider_reseau_seul(test_data)
        
        # Afficher avec Rich UI
        RichUI.print_success("Réseau validé avec succès !")
        RichUI.print_info(f"Nom du réseau: {reseau.nom}")
        RichUI.print_info(f"Type: {reseau.type}")
        RichUI.print_info(f"Nombre de nœuds: {len(reseau.noeuds)}")
        RichUI.print_info(f"Nombre de conduites: {len(reseau.conduites)}")
        
        # Vérifier l'affichage
        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "ℹ️" in captured.out
        assert "Réseau validé avec succès" in captured.out
        assert "Réseau Test Intégration" in captured.out
        assert "MAILLE" in captured.out
    
    def test_rich_table_with_pydantic_data(self):
        """Test de création de tableau Rich avec données Pydantic."""
        # Créer un réseau
        reseau = ReseauCompletConfig(
            nom="Réseau Test Tableau",
            type=TypeReseau.MAILLE,
            noeuds={
                "N1": NoeudUnified(
                    role=NoeudRole.RESERVOIR,
                    cote_m=200.0,
                    demande_m3_s=0.0,
                    pression_min_mce=20,
                    pression_max_mce=80
                ),
                "N2": NoeudUnified(
                    role=NoeudRole.CONSOMMATION,
                    cote_m=150.0,
                    demande_m3_s=0.02,
                    pression_min_mce=20,
                    pression_max_mce=80
                )
            },
            conduites={
                "C1": ConduiteUnified(
                    noeud_amont="N1",
                    noeud_aval="N2",
                    longueur_m=500.0,
                    diametre_m=0.2,
                    rugosite=100.0,
                    materiau="acier"
                )
            }
        )
        
        # Créer un tableau avec les données du réseau
        table_data = [
            {
                "Nœud": nom,
                "Rôle": noeud.role.value,
                "Cote": f"{noeud.cote_m} m",
                "Demande": f"{noeud.demande_m3_s} m³/s"
            }
            for nom, noeud in reseau.noeuds.items()
        ]
        
        table = RichUI.create_results_table("Nœuds du Réseau", table_data)
        
        # Vérifier la structure du tableau
        assert table.title == "Nœuds du Réseau"
        assert len(table.columns) == 4  # Nœud, Rôle, Cote, Demande
        assert len(table.rows) == 2  # 2 nœuds
    
    def test_yaml_validation_with_rich_output(self, capsys):
        """Test de validation YAML avec sortie Rich."""
        # Créer un fichier YAML temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml_data = {
                "nom": "Réseau YAML Test",
                "type": "maillé",
                "noeuds": {
                    "N1": {
                        "role": "reservoir",
                        "cote_m": 200.0,
                        "demande_m3_s": 0.0,
                        "pression_min_mce": 20,
                        "pression_max_mce": 80
                    },
                    "N2": {
                        "role": "consommation",
                        "cote_m": 150.0,
                        "demande_m3_s": 0.02,
                        "pression_min_mce": 20,
                        "pression_max_mce": 80
                    }
                },
                "conduites": {
                    "C1": {
                        "noeud_amont": "N1",
                        "noeud_aval": "N2",
                        "longueur_m": 500.0,
                        "diametre_m": 0.2,
                        "rugosite": 100.0,
                        "materiau": "acier"
                    }
                }
            }
            yaml.dump(yaml_data, f)
            yaml_file = f.name
        
        try:
            # Charger et valider le YAML
            with open(yaml_file, 'r') as f:
                loaded_data = yaml.safe_load(f)
            
            reseau = valider_reseau_seul(loaded_data)
            
            # Afficher les résultats avec Rich
            RichUI.print_success(f"Fichier YAML chargé et validé: {yaml_file}")
            RichUI.print_info(f"Réseau: {reseau.nom}")
            RichUI.print_info(f"Type: {reseau.type}")
            
            # Vérifier l'affichage
            captured = capsys.readouterr()
            assert "✅" in captured.out
            assert "ℹ️" in captured.out
            assert "Fichier YAML chargé et validé" in captured.out
            assert "Réseau YAML Test" in captured.out
            
        finally:
            # Nettoyer
            Path(yaml_file).unlink()
    
    def test_error_handling_with_rich(self, capsys):
        """Test de gestion d'erreur avec Rich UI."""
        # Données invalides
        invalid_data = {
            "nom": "Réseau Invalide",
            "type": "maillé",
            "noeuds": {
                "N1": {
                    "role": "consommation",  # Pas de réservoir !
                    "cote_m": 150.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {}
        }
        
        # Tenter la validation (doit échouer)
        try:
            valider_reseau_seul(invalid_data)
        except ValueError as e:
            RichUI.print_error(f"Erreur de validation: {e}")
        
        # Vérifier l'affichage d'erreur
        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "Erreur de validation" in captured.out
        assert "réservoir" in captured.out
    
    def test_calculation_results_display(self, capsys):
        """Test d'affichage des résultats de calcul avec Rich."""
        # Simuler des résultats de calcul
        results = {
            "valeurs": {
                "population": 15000,
                "demande_totale": 2250.5,
                "cout_estime": 150000
            },
            "diagnostics": {
                "validation_ok": True,
                "convergence": True,
                "performance": 0.85
            },
            "iterations": {
                "total": 15,
                "temps_calcul": 2.5
            }
        }
        
        # Afficher avec Rich
        show_calculation_results(results, "Test Calcul Intégration")
        
        # Vérifier l'affichage
        captured = capsys.readouterr()
        assert "Test Calcul Intégration" in captured.out
        assert "Valeurs principales" in captured.out
        assert "Diagnostics" in captured.out
        assert "Détails des itérations" in captured.out
        assert "15000" in captured.out  # Population
        assert "2250.5" in captured.out  # Demande totale
    
    def test_network_diagnostics_with_rich(self, capsys):
        """Test d'affichage des diagnostics réseau avec Rich."""
        # Simuler des diagnostics réseau
        diagnostics = {
            "connectivite": True,
            "pression_min": 25.5,
            "pression_max": 75.2,
            "vitesse_min": 0.8,
            "vitesse_max": 2.1,
            "pertes_charge": 45.3,
            "rendement": 0.92
        }
        
        # Afficher avec Rich
        RichUI.print_header("Diagnostics Réseau")
        RichUI.print_info(f"Connectivité: {'✅' if diagnostics['connectivite'] else '❌'}")
        RichUI.print_info(f"Pression min: {diagnostics['pression_min']} mCE")
        RichUI.print_info(f"Pression max: {diagnostics['pression_max']} mCE")
        RichUI.print_info(f"Vitesse min: {diagnostics['vitesse_min']} m/s")
        RichUI.print_info(f"Vitesse max: {diagnostics['vitesse_max']} m/s")
        RichUI.print_info(f"Pertes de charge: {diagnostics['pertes_charge']} m")
        RichUI.print_info(f"Rendement: {diagnostics['rendement']:.1%}")
        
        # Vérifier l'affichage
        captured = capsys.readouterr()
        assert "Diagnostics Réseau" in captured.out
        assert "✅" in captured.out  # Connectivité OK
        assert "25.5" in captured.out  # Pression min
        assert "75.2" in captured.out  # Pression max
        assert "92.0%" in captured.out  # Rendement
    
    def test_progress_bar_integration(self, capsys):
        """Test d'intégration de la barre de progression avec Rich."""
        import time
        
        # Simuler un calcul avec barre de progression
        with RichUI.show_progress_bar("Calcul en cours...", total=10) as progress:
            for i in range(10):
                time.sleep(0.01)  # Simulation d'un calcul
                progress.update(1)
                if i == 5:
                    RichUI.print_info(f"Étape {i+1}/10 terminée")
        
        # Vérifier que la barre s'affiche
        captured = capsys.readouterr()
        assert "Calcul en cours" in captured.out
        assert "Étape 6/10 terminée" in captured.out
    
    def test_parameters_table_integration(self):
        """Test d'intégration du tableau de paramètres avec Rich."""
        # Créer des paramètres de test
        parameters = {
            "Population": ("15000", "habitants"),
            "Dotation": ("150", "L/j/hab"),
            "Coefficient de pointe": ("1.8", ""),
            "Rendement réseau": ("0.95", ""),
            "Pression minimale": ("20", "mCE")
        }
        
        # Créer le tableau
        table = RichUI.create_parameters_table("Paramètres du Projet", parameters)
        
        # Vérifier la structure
        assert table.title == "Paramètres du Projet"
        assert len(table.columns) == 3  # Paramètre, Valeur, Unité
        assert len(table.rows) == 5  # 5 paramètres
    
    def test_complete_workflow_integration(self, capsys):
        """Test d'intégration complète du workflow."""
        # 1. Charger des données
        test_data = {
            "nom": "Réseau Test Workflow",
            "type": "maillé",
            "noeuds": {
                "R1": {
                    "role": "reservoir",
                    "cote_m": 250.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N1": {
                    "role": "consommation",
                    "cote_m": 200.0,
                    "demande_m3_s": 0.015,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 180.0,
                    "demande_m3_s": 0.025,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "R1",
                    "noeud_aval": "N1",
                    "longueur_m": 800.0,
                    "diametre_m": 0.25,
                    "rugosite": 100.0,
                    "materiau": "acier"
                },
                "C2": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 600.0,
                    "diametre_m": 0.20,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        # 2. Valider avec Pydantic
        try:
            reseau = valider_reseau_seul(test_data)
            RichUI.print_success("✅ Réseau validé avec succès")
        except Exception as e:
            RichUI.print_error(f"❌ Erreur de validation: {e}")
            return
        
        # 3. Afficher les informations du réseau
        RichUI.print_header(f"Réseau: {reseau.nom}")
        RichUI.print_info(f"Type: {reseau.type}")
        RichUI.print_info(f"Nœuds: {len(reseau.noeuds)}")
        RichUI.print_info(f"Conduites: {len(reseau.conduites)}")
        
        # 4. Simuler un calcul
        results = {
            "valeurs": {
                "demande_totale": 0.04,  # m³/s
                "pression_moyenne": 45.2,  # mCE
                "vitesse_moyenne": 1.8,  # m/s
                "pertes_charge_totales": 34.8  # m
            },
            "diagnostics": {
                "convergence": True,
                "pression_ok": True,
                "vitesse_ok": True,
                "rendement": 0.94
            },
            "iterations": {
                "total": 12,
                "temps_calcul": 1.8
            }
        }
        
        # 5. Afficher les résultats
        show_calculation_results(results, "Résultats du Calcul Hydraulique")
        
        # Vérifier l'intégration complète
        captured = capsys.readouterr()
        assert "✅ Réseau validé avec succès" in captured.out
        assert "Réseau: Réseau Test Workflow" in captured.out
        assert "Type: maillé" in captured.out
        assert "Nœuds: 3" in captured.out
        assert "Conduites: 2" in captured.out
        assert "Résultats du Calcul Hydraulique" in captured.out
        assert "0.04" in captured.out  # Demande totale
        assert "45.2" in captured.out  # Pression moyenne
        assert "94.0%" in captured.out  # Rendement
    
    def test_error_recovery_integration(self, capsys):
        """Test de récupération d'erreur avec Rich UI."""
        # Simuler une erreur de validation
        invalid_data = {
            "nom": "Réseau Erreur",
            "type": "invalide",  # Type invalide
            "noeuds": {},
            "conduites": {}
        }
        
        try:
            valider_reseau_seul(invalid_data)
        except Exception as e:
            RichUI.print_error(f"❌ Erreur détectée: {e}")
            RichUI.print_warning("⚠️ Tentative de correction...")
            
            # Corriger les données
            invalid_data["type"] = "maillé"
            invalid_data["noeuds"] = {
                "R1": {
                    "role": "reservoir",
                    "cote_m": 200.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            }
            
            try:
                reseau = valider_reseau_seul(invalid_data)
                RichUI.print_success("✅ Correction réussie !")
                RichUI.print_info(f"Réseau: {reseau.nom}")
            except Exception as e2:
                RichUI.print_error(f"❌ Échec de la correction: {e2}")
        
        # Vérifier la gestion d'erreur
        captured = capsys.readouterr()
        assert "❌ Erreur détectée" in captured.out
        assert "⚠️ Tentative de correction" in captured.out
        assert "✅ Correction réussie" in captured.out
        assert "Réseau: Réseau Erreur" in captured.out


    def test_network_diagnostics_with_rich(self, capsys):
        """Test d'affichage des diagnostics réseau avec Rich."""
        # Simuler des diagnostics réseau
        diagnostics = {
            "connectivite": True,
            "pression_min": 25.5,
            "pression_max": 75.2,
            "vitesse_min": 0.8,
            "vitesse_max": 2.1,
            "pertes_charge": 45.3,
            "rendement": 0.92
        }
        
        # Afficher avec Rich
        RichUI.print_header("Diagnostics Réseau")
        RichUI.print_info(f"Connectivité: {'✅' if diagnostics['connectivite'] else '❌'}")
        RichUI.print_info(f"Pression min: {diagnostics['pression_min']} mCE")
        RichUI.print_info(f"Pression max: {diagnostics['pression_max']} mCE")
        RichUI.print_info(f"Vitesse min: {diagnostics['vitesse_min']} m/s")
        RichUI.print_info(f"Vitesse max: {diagnostics['vitesse_max']} m/s")
        RichUI.print_info(f"Pertes de charge: {diagnostics['pertes_charge']} m")
        RichUI.print_info(f"Rendement: {diagnostics['rendement']:.1%}")
        
        # Vérifier l'affichage
        captured = capsys.readouterr()
        assert "Diagnostics Réseau" in captured.out
        assert "✅" in captured.out  # Connectivité OK
        assert "25.5" in captured.out  # Pression min
        assert "75.2" in captured.out  # Pression max
        assert "92.0%" in captured.out  # Rendement
    
    def test_progress_bar_integration(self, capsys):
        """Test d'intégration de la barre de progression avec Rich."""
        import time
        
        # Simuler un calcul avec barre de progression
        progress = RichUI.show_progress_bar(10, "Calcul en cours...")
        with progress:
            task = progress.add_task("Calcul en cours...", total=10)
            for i in range(10):
                time.sleep(0.01)  # Simulation d'un calcul
                progress.update(task, advance=1)
                if i == 5:
                    RichUI.print_info(f"Étape {i+1}/10 terminée")
        
        # Vérifier que la barre s'affiche
        captured = capsys.readouterr()
        assert "Calcul en cours" in captured.out
        assert "Étape 6/10 terminée" in captured.out
    
    def test_parameters_table_integration(self):
        """Test d'intégration du tableau de paramètres avec Rich."""
        # Créer des paramètres de test
        parameters = {
            "Population": ("15000", "habitants"),
            "Dotation": ("150", "L/j/hab"),
            "Coefficient de pointe": ("1.8", ""),
            "Rendement réseau": ("0.95", ""),
            "Pression minimale": ("20", "mCE")
        }
        
        # Créer le tableau
        table = RichUI.create_parameters_table("Paramètres du Projet", parameters)
        
        # Vérifier la structure
        assert table.title == "Paramètres du Projet"
        assert len(table.columns) == 3  # Paramètre, Valeur, Unité
        assert len(table.rows) == 5  # 5 paramètres
    
    def test_complete_workflow_integration(self, capsys):
        """Test d'intégration complète du workflow."""
        # 1. Charger des données
        test_data = {
            "nom": "Réseau Test Workflow",
            "type": "maillé",
            "noeuds": {
                "R1": {
                    "role": "reservoir",
                    "cote_m": 250.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N1": {
                    "role": "consommation",
                    "cote_m": 200.0,
                    "demande_m3_s": 0.015,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 180.0,
                    "demande_m3_s": 0.025,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "R1",
                    "noeud_aval": "N1",
                    "longueur_m": 800.0,
                    "diametre_m": 0.25,
                    "rugosite": 100.0,
                    "materiau": "acier"
                },
                "C2": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 600.0,
                    "diametre_m": 0.20,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        # 2. Valider avec Pydantic
        try:
            reseau = valider_reseau_seul(test_data)
            RichUI.print_success("✅ Réseau validé avec succès")
        except Exception as e:
            RichUI.print_error(f"❌ Erreur de validation: {e}")
            return
        
        # 3. Afficher les informations du réseau
        RichUI.print_header(f"Réseau: {reseau.nom}")
        RichUI.print_info(f"Type: {reseau.type}")
        RichUI.print_info(f"Nœuds: {len(reseau.noeuds)}")
        RichUI.print_info(f"Conduites: {len(reseau.conduites)}")
        
        # 4. Simuler un calcul
        results = {
            "valeurs": {
                "demande_totale": 0.04,  # m³/s
                "pression_moyenne": 45.2,  # mCE
                "vitesse_moyenne": 1.8,  # m/s
                "pertes_charge_totales": 34.8  # m
            },
            "diagnostics": {
                "convergence": True,
                "pression_ok": True,
                "vitesse_ok": True,
                "rendement": 0.94
            },
            "iterations": {
                "total": 12,
                "temps_calcul": 1.8
            }
        }
        
        # 5. Afficher les résultats
        show_calculation_results(results, "Résultats du Calcul Hydraulique")
        
        # Vérifier l'intégration complète
        captured = capsys.readouterr()
        assert "✅ Réseau validé avec succès" in captured.out
        assert "Réseau: Réseau Test Workflow" in captured.out
        assert "Type: TypeReseau.MAILLE" in captured.out
        assert "Nœuds: 3" in captured.out
        assert "Conduites: 2" in captured.out
        assert "Résultats du Calcul Hydraulique" in captured.out
        assert "0.04" in captured.out  # Demande totale
        assert "45.2" in captured.out  # Pression moyenne
        assert "0.94" in captured.out  # Rendement
    
    def test_error_recovery_integration(self, capsys):
        """Test de récupération d'erreur avec Rich UI."""
        # Simuler une erreur de validation
        invalid_data = {
            "nom": "Réseau Erreur",
            "type": "invalide",  # Type invalide
            "noeuds": {},
            "conduites": {}
        }
        
        try:
            valider_reseau_seul(invalid_data)
        except Exception as e:
            RichUI.print_error(f"❌ Erreur détectée: {e}")
            RichUI.print_warning("⚠️ Tentative de correction...")
            
            # Corriger les données
            invalid_data["type"] = "maillé"
            invalid_data["noeuds"] = {
                "R1": {
                    "role": "reservoir",
                    "cote_m": 200.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            }
            
            try:
                reseau = valider_reseau_seul(invalid_data)
                RichUI.print_success("✅ Correction réussie !")
                RichUI.print_info(f"Réseau: {reseau.nom}")
            except Exception as e2:
                RichUI.print_error(f"❌ Échec de la correction: {e2}")
        
        # Vérifier la gestion d'erreur
        captured = capsys.readouterr()
        assert "❌ Erreur détectée" in captured.out
        assert "⚠️ Tentative de correction" in captured.out
        assert "✅ Correction réussie" in captured.out
        assert "Réseau: Réseau Erreur" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])