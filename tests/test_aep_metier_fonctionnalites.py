"""
Tests unitaires pour les fonctionnalités métier AEP

Ce module teste les nouvelles fonctionnalités implémentées :
- Analyse de sensibilité
- Phasage et planification
- Courbes de charge horaire
- Gestion dynamique des constantes
"""

import pytest
import tempfile
import json
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lcpi.aep.calculations.sensitivity_analysis import (
    AEPSensitivityAnalyzer, SensitivityParameter, SensitivityResult
)
from lcpi.aep.calculations.phasing_planning import (
    AEPPhasingPlanner, Phase, PlanningResult, HorizonResult, TypePlanning
)
from lcpi.aep.calculations.load_curves import (
    AEPLoadCurveManager, LoadCurve, LoadCurvePoint, TypeCourbe, MethodeCalcul, CalculResult
)
from lcpi.aep.core.dynamic_constants import (
    AEPDynamicConstantsManager, ReferenceLocale, DotationLocale, CoefficientLocal
)

class TestAEPSensitivityAnalysis:
    """Tests pour l'analyse de sensibilité"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.analyzer = AEPSensitivityAnalyzer()
    
    def test_initialisation_parametres_standard(self):
        """Test l'initialisation des paramètres standard"""
        assert "dotation" in self.analyzer.parametres_standard
        assert "croissance_demographique" in self.analyzer.parametres_standard
        assert "fuites" in self.analyzer.parametres_standard
        assert "coefficient_pointe" in self.analyzer.parametres_standard
    
    def test_analyser_sensibilite_dotation(self):
        """Test l'analyse de sensibilité de la dotation"""
        resultat = self.analyzer.analyser_sensibilite_dotation(
            population=1000,
            dotation_base=60.0,
            variation_pct=10.0,
            pas=2.0
        )
        
        assert resultat.parametre == "dotation"
        assert resultat.impact_max > 0
        assert resultat.impact_min < 0
        assert resultat.classe_impact in ["faible", "moyen", "élevé"]
        assert len(resultat.variations) > 0
        assert len(resultat.impacts) > 0
    
    def test_analyser_sensibilite_croissance_demographique(self):
        """Test l'analyse de sensibilité de la croissance démographique"""
        resultat = self.analyzer.analyser_sensibilite_croissance_demographique(
            population_base=1000,
            taux_base=0.025,
            annees=10,
            variation_pct=30.0,
            pas=5.0
        )
        
        assert resultat.parametre == "croissance_demographique"
        assert resultat.impact_max > 0
        assert resultat.impact_min < 0
        assert resultat.classe_impact in ["faible", "moyen", "élevé"]
    
    def test_analyser_sensibilite_fuites(self):
        """Test l'analyse de sensibilité des fuites"""
        resultat = self.analyzer.analyser_sensibilite_fuites(
            demande_nette=100.0,
            rendement_base=0.95,
            variation_pct=20.0,
            pas=2.0
        )
        
        assert resultat.parametre == "fuites"
        assert resultat.impact_max > 0
        assert resultat.impact_min < 0
        assert resultat.classe_impact in ["faible", "moyen", "élevé"]
    
    def test_analyser_sensibilite_globale(self):
        """Test l'analyse de sensibilité globale"""
        resultats = self.analyzer.analyser_sensibilite_globale(
            population=1000,
            dotation=60.0,
            taux_croissance=0.025,
            rendement=0.95,
            annees=10
        )
        
        assert "dotation" in resultats
        assert "croissance_demographique" in resultats
        assert "fuites" in resultats
        
        for nom, resultat in resultats.items():
            assert isinstance(resultat, SensitivityResult)
            assert resultat.parametre == nom
    
    def test_generer_rapport_sensibilite_json(self):
        """Test la génération de rapport JSON"""
        resultats = self.analyzer.analyser_sensibilite_globale(
            population=1000, dotation=60.0, taux_croissance=0.025
        )
        
        rapport = self.analyzer.generer_rapport_sensibilite(resultats, "json")
        data = json.loads(rapport)
        
        assert "analyse_sensibilite" in data
        assert "resultats" in data["analyse_sensibilite"]
    
    def test_generer_rapport_sensibilite_markdown(self):
        """Test la génération de rapport Markdown"""
        resultats = self.analyzer.analyser_sensibilite_globale(
            population=1000, dotation=60.0, taux_croissance=0.025
        )
        
        rapport = self.analyzer.generer_rapport_sensibilite(resultats, "markdown")
        
        assert "# 📊 Rapport d'Analyse de Sensibilité AEP" in rapport
        assert "## 🎯 Résumé des Analyses" in rapport
    
    def test_generer_rapport_sensibilite_html(self):
        """Test la génération de rapport HTML"""
        resultats = self.analyzer.analyser_sensibilite_globale(
            population=1000, dotation=60.0, taux_croissance=0.025
        )
        
        rapport = self.analyzer.generer_rapport_sensibilite(resultats, "html")
        
        assert "<!DOCTYPE html>" in rapport
        assert "<title>Rapport d'Analyse de Sensibilité AEP</title>" in rapport
    
    def test_format_sortie_invalide(self):
        """Test la gestion d'un format de sortie invalide"""
        resultats = self.analyzer.analyser_sensibilite_globale(
            population=1000, dotation=60.0, taux_croissance=0.025
        )
        
        with pytest.raises(ValueError, match="Format de sortie non supporté"):
            self.analyzer.generer_rapport_sensibilite(resultats, "invalid_format")

class TestAEPPhasingPlanning:
    """Tests pour le phasage et la planification"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.planner = AEPPhasingPlanner()
    
    def test_initialisation_phases_standard(self):
        """Test l'initialisation des phases standard"""
        assert "court_terme" in self.planner.phases_standard
        assert "moyen_terme" in self.planner.phases_standard
        assert "long_terme" in self.planner.phases_standard
        
        assert self.planner.horizons_standard == [2025, 2030, 2035, 2040, 2045, 2050]
    
    def test_calculer_planning_standard(self):
        """Test le calcul de planning standard"""
        resultats = self.planner.calculer_planning_standard(
            population_base=1000,
            taux_croissance=0.025,
            dotation=60.0,
            cout_infrastructure_m3=1000.0
        )
        
        assert "Court terme" in resultats
        assert "Moyen terme" in resultats
        assert "Long terme" in resultats
        
        for nom_phase, resultat in resultats.items():
            assert isinstance(resultat, PlanningResult)
            assert resultat.phase == nom_phase  # Le nom de la phase est maintenant la clé
            assert resultat.population_phase > 0
            assert resultat.besoins_phase > 0
            assert resultat.cout_estime > 0
    
    def test_calculer_planning_horizons(self):
        """Test le calcul de planning par horizons"""
        horizons = [2025, 2030, 2035]
        resultats = self.planner.calculer_planning_horizons(
            population_base=1000,
            taux_croissance=0.025,
            horizons=horizons,
            dotation=60.0
        )
        
        for horizon in horizons:
            assert horizon in resultats
            resultat = resultats[horizon]
            assert isinstance(resultat, HorizonResult)
            assert resultat.annee == horizon
            assert resultat.population > 0
            assert resultat.besoins > 0
            assert resultat.cout_estime > 0
    
    def test_calculer_planning_phases_pourcentages(self):
        """Test le calcul de planning avec phases par pourcentages"""
        pourcentages_population = [0.50, 0.30, 0.20]
        pourcentages_infrastructure = [0.60, 0.30, 0.10]
        noms_phases = ["Phase 1", "Phase 2", "Phase 3"]
        
        resultats = self.planner.calculer_planning_phases_pourcentages(
            population_base=1000,
            taux_croissance=0.025,
            pourcentages_population=pourcentages_population,
            pourcentages_infrastructure=pourcentages_infrastructure,
            noms_phases=noms_phases,
            dotation=60.0,
            cout_infrastructure_m3=1000.0
        )
        
        for nom_phase in noms_phases:
            assert nom_phase in resultats
            resultat = resultats[nom_phase]
            assert isinstance(resultat, PlanningResult)
            assert resultat.phase == nom_phase
            assert resultat.population_phase > 0
            assert resultat.besoins_phase > 0
    
    def test_generer_rapport_planning_json(self):
        """Test la génération de rapport JSON"""
        resultats = self.planner.calculer_planning_standard(
            population_base=1000, taux_croissance=0.025
        )
        
        rapport = self.planner.generer_rapport_planning(resultats, "json")
        data = json.loads(rapport)
        
        assert "planning_aep" in data
        assert "Court terme" in data["planning_aep"]["resultats"]
        assert "Moyen terme" in data["planning_aep"]["resultats"]
        assert "Long terme" in data["planning_aep"]["resultats"]
    
    def test_generer_rapport_planning_markdown(self):
        """Test la génération de rapport Markdown"""
        resultats = self.planner.calculer_planning_standard(
            population_base=1000, taux_croissance=0.025
        )
        
        rapport = self.planner.generer_rapport_planning(resultats, "markdown")
        
        assert "# 📅 Rapport de Planning AEP" in rapport
        assert "## 🎯 Résumé des Phases" in rapport
    
    def test_generer_rapport_planning_html(self):
        """Test la génération de rapport HTML"""
        resultats = self.planner.calculer_planning_standard(
            population_base=1000, taux_croissance=0.025
        )
        
        rapport = self.planner.generer_rapport_planning(resultats, "html")
        
        assert "<!DOCTYPE html>" in rapport
        assert "<title>Rapport de Planning AEP</title>" in rapport
    
    def test_validation_phases_invalides(self):
        """Test la validation des phases invalides"""
        # Test avec pourcentages cumulés > 100%
        phases_invalides = [
            Phase("Phase 1", 2025, 2030, 0.60, 0.40, "Phase 1", 1),
            Phase("Phase 2", 2030, 2035, 0.50, 0.30, "Phase 2", 2)
        ]
        
        with pytest.raises(ValueError, match="pourcentages de population cumulés"):
            self.planner._valider_phases(phases_invalides)
        
        # Test avec priorités dupliquées
        phases_priorites_dupliquees = [
            Phase("Phase 1", 2025, 2030, 0.50, 0.40, "Phase 1", 1),
            Phase("Phase 2", 2030, 2035, 0.50, 0.60, "Phase 2", 1)
        ]
        
        with pytest.raises(ValueError, match="priorités des phases doivent être uniques"):
            self.planner._valider_phases(phases_priorites_dupliquees)
        
        # Test avec années incohérentes
        phases_annees_incoherentes = [
            Phase("Phase 1", 2025, 2030, 0.50, 0.40, "Phase 1", 1),
            Phase("Phase 2", 2031, 2035, 0.50, 0.60, "Phase 2", 2)  # 2031 != 2030
        ]
        
        with pytest.raises(ValueError, match="année de début"):
            self.planner._valider_phases(phases_annees_incoherentes)
    
    def test_planning_generique(self):
        """Test la méthode générique de planning"""
        phases = [
            Phase("Phase Test 1", 2025, 2030, 0.60, 0.50, "Phase de test 1", 1),
            Phase("Phase Test 2", 2030, 2035, 0.40, 0.50, "Phase de test 2", 2)
        ]
        
        resultats = self.planner.calculer_planning_generique(
            population_base=1000,
            taux_croissance=0.025,
            phases=phases,
            dotation=60.0,
            cout_infrastructure_m3=1000.0
        )
        
        assert "Phase Test 1" in resultats
        assert "Phase Test 2" in resultats
        
        for nom_phase, resultat in resultats.items():
            assert isinstance(resultat, PlanningResult)
            assert resultat.type_planning == TypePlanning.PHASES
            assert resultat.population_phase > 0
            assert resultat.besoins_phase > 0

class TestAEPLoadCurves:
    """Tests pour les courbes de charge"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.manager = AEPLoadCurveManager()
    
    def test_initialisation_courbes_standard(self):
        """Test l'initialisation des courbes standard"""
        courbes_disponibles = self.manager.lister_courbes_disponibles()
        
        assert "journaliere_standard" in courbes_disponibles
        assert "horaire_detaille" in courbes_disponibles
        assert "saisonniere" in courbes_disponibles
    
    def test_obtenir_courbe(self):
        """Test l'obtention d'une courbe"""
        courbe = self.manager.obtenir_courbe("journaliere_standard")
        
        assert courbe is not None
        assert courbe.nom == "Courbe journalière standard"
        assert courbe.type == TypeCourbe.JOURNALIERE
        assert len(courbe.points) > 0
        assert courbe.coefficient_moyen == 1.0
        assert courbe.coefficient_max > 1.0
    
    def test_calculer_coefficient_pointe_horaire(self):
        """Test le calcul du coefficient de pointe horaire"""
        # Test formule génie rural
        cph = self.manager.calculer_coefficient_pointe_horaire(
            debit_moyen_horaire_m3h=100.0,
            methode="formule_genie_rural"
        )
        assert cph > 1.5
        
        # Test formule OMS
        cph_oms = self.manager.calculer_coefficient_pointe_horaire(
            debit_moyen_horaire_m3h=50.0,
            methode="formule_oms"
        )
        assert cph_oms == 1.8
        
        # Test formule empirique
        cph_emp = self.manager.calculer_coefficient_pointe_horaire(
            debit_moyen_horaire_m3h=100.0,
            methode="formule_empirique"
        )
        assert cph_emp > 0
    
    def test_calculer_coefficient_pointe_journalier(self):
        """Test le calcul du coefficient de pointe journalier"""
        # Test formule standard
        cpj = self.manager.calculer_coefficient_pointe_journalier(
            population=1000,
            methode="formule_standard"
        )
        assert cpj == 1.5
        
        # Test formule population
        cpj_pop = self.manager.calculer_coefficient_pointe_journalier(
            population=1000,
            methode="formule_population"
        )
        assert cpj_pop > 1.0
        
        # Test formule zone
        cpj_zone = self.manager.calculer_coefficient_pointe_journalier(
            population=500,
            methode="formule_zone"
        )
        assert cpj_zone == 1.8  # Zone rurale
    
    def test_calculer_coefficient_pointe_global(self):
        """Test le calcul du coefficient de pointe global"""
        resultats = self.manager.calculer_coefficient_pointe_global(
            population=1000,
            debit_moyen_horaire_m3h=100.0
        )
        
        assert "coefficient_pointe_journalier" in resultats
        assert "coefficient_pointe_horaire" in resultats
        assert "coefficient_pointe_global" in resultats
        
        assert resultats["coefficient_pointe_global"] == (
            resultats["coefficient_pointe_journalier"] * 
            resultats["coefficient_pointe_horaire"]
        )
    
    def test_generer_courbe_personnalisee(self):
        """Test la génération d'une courbe personnalisée"""
        points = [
            (0, 0.5, "Test 0h"),
            (12, 1.5, "Test 12h"),
            (24, 0.5, "Test 24h")
        ]
        
        courbe = self.manager.generer_courbe_personnalisee(
            nom="Test",
            type_courbe="test",
            points=points
        )
        
        assert courbe.nom == "Test"
        assert courbe.type == TypeCourbe.PERSONNALISEE
        assert len(courbe.points) == 3
        assert courbe.coefficient_moyen == 0.833
        assert courbe.coefficient_max == 1.5
    
    def test_calculer_besoin_pointe(self):
        """Test le calcul des besoins de pointe"""
        resultats = self.manager.calculer_besoin_pointe(
            besoin_moyen_journalier=100.0,
            coefficient_pointe_journalier=1.5,
            coefficient_pointe_horaire=1.8
        )
        
        assert resultats["besoin_moyen_journalier_m3_j"] == 100.0
        assert resultats["besoin_pointe_journalier_m3_j"] == 150.0
        assert resultats["coefficient_pointe_global"] == 2.7
    
    def test_methode_non_supportee(self):
        """Test la gestion d'une méthode non supportée"""
        with pytest.raises(ValueError, match="Méthode non supportée"):
            self.manager.calculer_coefficient_pointe_horaire(
                debit_moyen_horaire_m3h=100.0,
                methode="methode_invalide"
            )
        
        with pytest.raises(ValueError, match="Méthode non supportée"):
            self.manager.calculer_coefficient_pointe_journalier(
                population=1000,
                methode="methode_invalide"
            )
    
    def test_validation_entrees_positives(self):
        """Test la validation des entrées positives"""
        # Test avec population négative
        with pytest.raises(ValueError, match="population.*doit être un nombre positif"):
            self.manager.calculer_coefficient_pointe_journalier(population=-1000)
        
        # Test avec débit nul
        with pytest.raises(ValueError, match="debit_moyen_horaire_m3h.*doit être un nombre positif"):
            self.manager.calculer_coefficient_pointe_horaire(debit_moyen_horaire_m3h=0)
        
        # Test avec besoin négatif
        with pytest.raises(ValueError, match="besoin_moyen_journalier.*doit être un nombre positif"):
            self.manager.calculer_besoin_pointe(
                besoin_moyen_journalier=-100.0,
                coefficient_pointe_journalier=1.5,
                coefficient_pointe_horaire=1.8
            )
    
    def test_calculer_coefficient_pointe_unifie(self):
        """Test la méthode unifiée de calcul des coefficients"""
        # Test coefficients horaires
        resultats_horaires = self.manager.calculer_coefficient_pointe_unifie(
            parametres={"debit_moyen_horaire_m3h": 100.0},
            methodes=[MethodeCalcul.GENIE_RURAL, MethodeCalcul.OMS],
            type_calcul="horaire"
        )
        
        assert "formule_genie_rural" in resultats_horaires
        assert "formule_oms" in resultats_horaires
        assert isinstance(resultats_horaires["formule_genie_rural"], CalculResult)
        assert resultats_horaires["formule_oms"].valeur == 1.8
        
        # Test coefficients journaliers
        resultats_journaliers = self.manager.calculer_coefficient_pointe_unifie(
            parametres={"population": 1000},
            methodes=[MethodeCalcul.STANDARD, MethodeCalcul.POPULATION],
            type_calcul="journalier"
        )
        
        assert "formule_standard" in resultats_journaliers
        assert "formule_population" in resultats_journaliers
        assert resultats_journaliers["formule_standard"].valeur == 1.5
    
    def test_generer_rapport_dimensionnement(self):
        """Test la génération de rapport de dimensionnement"""
        rapport = self.manager.generer_rapport_dimensionnement(
            population=1000,
            dotation=60.0,
            nom_courbe="horaire_detaille"
        )
        
        assert "parametres_entree" in rapport
        assert "besoins" in rapport
        assert "coefficients_pointe" in rapport
        assert "dimensionnement_equipements" in rapport
        assert "courbe_utilisee" in rapport
        
        # Vérifier les paramètres d'entrée
        assert rapport["parametres_entree"]["population"] == 1000
        assert rapport["parametres_entree"]["dotation_l_j_hab"] == 60.0
        
        # Vérifier les besoins
        assert rapport["besoins"]["besoin_moyen_journalier_m3_j"] > 0
        assert rapport["besoins"]["besoin_pointe_journalier_m3_j"] > 0
        assert rapport["besoins"]["besoin_pointe_horaire_m3_h"] > 0
        
        # Vérifier le dimensionnement
        assert rapport["dimensionnement_equipements"]["volume_reservoir_m3"] > 0
        assert rapport["dimensionnement_equipements"]["puissance_pompe_kw"] > 0
        assert rapport["dimensionnement_equipements"]["diametre_conduite_mm"] > 0
    
    def test_generer_rapport_complet(self):
        """Test la génération de rapport complet"""
        # Test format JSON
        rapport_json = self.manager.generer_rapport_complet(
            population=1000,
            dotation=60.0,
            format_sortie="json"
        )
        data = json.loads(rapport_json)
        assert "parametres_entree" in data
        
        # Test format Markdown
        rapport_md = self.manager.generer_rapport_complet(
            population=1000,
            dotation=60.0,
            format_sortie="markdown"
        )
        assert "# 📊 Rapport de Dimensionnement AEP" in rapport_md
        assert "## 🎯 Paramètres d'Entrée" in rapport_md
        
        # Test format HTML
        rapport_html = self.manager.generer_rapport_complet(
            population=1000,
            dotation=60.0,
            format_sortie="html"
        )
        assert "<!DOCTYPE html>" in rapport_html
        assert "<title>Rapport de Dimensionnement AEP</title>" in rapport_html
    
    def test_comparer_methodes_calcul(self):
        """Test la comparaison des méthodes de calcul"""
        resultats = self.manager.comparer_methodes_calcul(
            population=1000,
            debit_moyen_horaire_m3h=100.0
        )
        
        assert "coefficients_journaliers" in resultats
        assert "coefficients_horaires" in resultats
        assert "coefficients_globaux" in resultats
        
        # Vérifier les méthodes journalières
        assert "formule_standard" in resultats["coefficients_journaliers"]
        assert "formule_population" in resultats["coefficients_journaliers"]
        assert "formule_zone" in resultats["coefficients_journaliers"]
        
        # Vérifier les méthodes horaires
        assert "formule_genie_rural" in resultats["coefficients_horaires"]
        assert "formule_oms" in resultats["coefficients_horaires"]
        assert "formule_empirique" in resultats["coefficients_horaires"]
    
    def test_analyser_sensibilite_courbe(self):
        """Test l'analyse de sensibilité des courbes"""
        resultats = self.manager.analyser_sensibilite_courbe(
            population=1000,
            dotation=60.0,
            variation_population=10.0,
            variation_dotation=10.0
        )
        
        assert "parametres_reference" in resultats
        assert "resultats_reference" in resultats
        assert "sensibilite_population" in resultats
        assert "sensibilite_dotation" in resultats
        
        # Vérifier les paramètres de référence
        assert resultats["parametres_reference"]["population"] == 1000
        assert resultats["parametres_reference"]["dotation"] == 60.0
        assert resultats["parametres_reference"]["variation_population_pct"] == 10.0
        
        # Vérifier la sensibilité population
        sens_pop = resultats["sensibilite_population"]
        assert sens_pop["population_min"] == 900
        assert sens_pop["population_max"] == 1100
        assert sens_pop["impact_besoin_min"] > 0
        assert sens_pop["impact_besoin_max"] > 0
    
    def test_ajouter_courbe_zone(self):
        """Test l'ajout de courbe pour une zone spécifique"""
        # Créer une courbe personnalisée
        points = [
            (0, 0.5, "Nuit"),
            (12, 1.5, "Midi"),
            (24, 0.5, "Nuit")
        ]
        
        courbe = self.manager.generer_courbe_personnalisee(
            nom="Test Zone",
            type_courbe="test",
            points=points,
            zone="zone_test"
        )
        
        # Ajouter la courbe à une zone
        success = self.manager.ajouter_courbe_zone("village_test", courbe)
        assert success is True
        
        # Vérifier que la courbe est disponible
        courbe_zone = self.manager.obtenir_courbes_zone("village_test")
        assert courbe_zone is not None
        assert courbe_zone.nom == "Test Zone"
        assert courbe_zone.zone == "village_test"
        
        # Vérifier la liste des zones
        zones = self.manager.lister_zones()
        assert "village_test" in zones
    
    def test_generer_graphique_courbe(self):
        """Test la génération de graphique de courbe"""
        # Test avec une courbe existante
        nom_fichier = self.manager.generer_graphique_courbe("horaire_detaille")
        assert nom_fichier.endswith(".png")
        
        # Vérifier que le fichier a été créé
        import os
        assert os.path.exists(nom_fichier)
        
        # Nettoyer
        os.remove(nom_fichier)
    
    def test_export_import_courbe_json(self):
        """Test l'export et import de courbe JSON"""
        # Exporter une courbe
        json_data = self.manager.exporter_courbe_json("horaire_detaille")
        data = json.loads(json_data)
        
        assert "nom" in data
        assert "type" in data
        assert "points" in data
        assert data["nom"] == "Courbe horaire détaillée"
        
        # Importer la courbe
        courbe_importee = self.manager.importer_courbe_json(json_data)
        assert courbe_importee.nom == "Courbe horaire détaillée"
        assert len(courbe_importee.points) > 0

class TestAEPDynamicConstants:
    """Tests pour la gestion dynamique des constantes"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = AEPDynamicConstantsManager(self.temp_dir)
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_ajouter_reference_locale(self):
        """Test l'ajout d'une référence locale"""
        success = self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=42.0,
            unite="m",
            source="Test",
            description="Référence de test"
        )
        
        assert success is True
        assert "test_ref" in self.manager.references_locales
        
        # Test ajout d'une référence existante
        success2 = self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=43.0,
            unite="m",
            source="Test",
            description="Référence de test 2"
        )
        
        assert success2 is False
    
    def test_ajouter_dotation_locale(self):
        """Test l'ajout d'une dotation locale"""
        success = self.manager.ajouter_dotation_locale(
            nom="test_dotation",
            valeur=80.0,
            unite="L/j/hab",
            type_zone="zone_test",
            source="Test",
            description="Dotation de test"
        )
        
        assert success is True
        assert "test_dotation" in self.manager.dotations_locales
    
    def test_ajouter_coefficient_local(self):
        """Test l'ajout d'un coefficient local"""
        success = self.manager.ajouter_coefficient_local(
            nom="test_coeff",
            valeur=1.8,
            unite="",
            type_calcul="test",
            source="Test",
            description="Coefficient de test"
        )
        
        assert success is True
        assert "test_coeff" in self.manager.coefficients_locaux
    
    def test_valider_reference(self):
        """Test la validation d'une référence"""
        self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=42.0,
            unite="m",
            source="Test",
            description="Référence de test"
        )
        
        success = self.manager.valider_reference("test_ref", "validateur_test")
        assert success is True
        assert self.manager.references_locales["test_ref"].statut == "valide"
        assert self.manager.references_locales["test_ref"].validateur == "validateur_test"
    
    def test_obtenir_references_valides(self):
        """Test l'obtention des références validées"""
        # Ajouter et valider une référence
        self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=42.0,
            unite="m",
            source="Test",
            description="Référence de test"
        )
        self.manager.valider_reference("test_ref", "validateur")
        
        # Ajouter une référence non validée
        self.manager.ajouter_reference_locale(
            nom="test_ref2",
            valeur=43.0,
            unite="m",
            source="Test",
            description="Référence de test 2"
        )
        
        refs_valides = self.manager.obtenir_references_valides()
        assert "test_ref" in refs_valides
        assert "test_ref2" not in refs_valides
    
    def test_rechercher_references(self):
        """Test la recherche de références"""
        self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=42.0,
            unite="m",
            source="Test",
            description="Référence de test"
        )
        
        resultats = self.manager.rechercher_references("test")
        assert len(resultats) == 1
        assert resultats[0].nom == "test_ref"
    
    def test_generer_rapport_statut(self):
        """Test la génération du rapport de statut"""
        # Ajouter quelques éléments
        self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=42.0,
            unite="m",
            source="Test",
            description="Référence de test"
        )
        
        self.manager.ajouter_dotation_locale(
            nom="test_dotation",
            valeur=80.0,
            unite="L/j/hab",
            type_zone="zone_test",
            source="Test",
            description="Dotation de test"
        )
        
        rapport = self.manager.generer_rapport_statut()
        
        assert "references_locales" in rapport
        assert "dotations_locales" in rapport
        assert "coefficients_locaux" in rapport
        
        assert rapport["references_locales"]["total"] == 1
        assert rapport["dotations_locales"]["total"] == 1
        assert rapport["coefficients_locaux"]["total"] == 0
    
    def test_export_import_configuration(self):
        """Test l'export et l'import de configuration"""
        # Ajouter des éléments
        self.manager.ajouter_reference_locale(
            nom="test_ref",
            valeur=42.0,
            unite="m",
            source="Test",
            description="Référence de test"
        )
        
        # Exporter
        config_json = self.manager.exporter_configuration("json")
        config_data = json.loads(config_json)
        
        assert "references_locales" in config_data
        assert "test_ref" in config_data["references_locales"]
        
        # Créer un nouveau manager et importer
        import tempfile
        new_manager = AEPDynamicConstantsManager(tempfile.mkdtemp())
        
        # Créer un fichier temporaire pour l'import
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write(config_json)
            temp_file = f.name
        
        try:
            success = new_manager.importer_configuration(temp_file)
            assert success is True
            assert "test_ref" in new_manager.references_locales
        finally:
            # Nettoyer
            import os
            os.unlink(temp_file)
            import shutil
            shutil.rmtree(new_manager.config_dir)

if __name__ == "__main__":
    pytest.main([__file__])
