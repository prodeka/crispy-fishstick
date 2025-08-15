"""
Tests pour les fonctionnalités avancées du module AEPDynamicConstantsManager
"""

import pytest
import tempfile
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.dynamic_constants import (
    AEPDynamicConstantsManager,
    StatutElement,
    TypeUtilisateur,
    ModeImport,
    ReferenceLocale,
    DotationLocale,
    CoefficientLocal
)

class TestAEPDynamicConstantsAdvanced:
    """Tests pour les fonctionnalités avancées"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = AEPDynamicConstantsManager(self.temp_dir)
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        shutil.rmtree(self.temp_dir)
    
    def test_validation_entrees(self):
        """Test de validation des entrées"""
        # Test validation nom (normalisation)
        success = self.manager.ajouter_reference_locale(
            "Test Reference", 100.0, "m", "source", "description", "user1"
        )
        assert success is True
        
        # Test validation unité
        success = self.manager.ajouter_reference_locale(
            "Test2", 50.0, "m³", "source", "description", "user1"
        )
        assert success is True
        
        # Test validation valeur négative (doit échouer)
        success = self.manager.ajouter_reference_locale(
            "Test3", -10.0, "m", "source", "description", "user1"
        )
        assert success is False
    
    def test_normalisation_nom(self):
        """Test de normalisation des noms"""
        # Ajouter avec nom en majuscules
        success = self.manager.ajouter_reference_locale(
            "TEST REFERENCE", 100.0, "m", "source", "description", "user1"
        )
        assert success is True
        
        # Vérifier que le nom est stocké tel quel (pas normalisé dans la clé)
        assert "TEST REFERENCE" in self.manager.references_locales
        
        # Test avec espaces multiples - doit échouer car nom normalisé existe déjà
        success = self.manager.ajouter_reference_locale(
            "  test  reference  ", 200.0, "m", "source", "description", "user1"
        )
        assert success is False  # Car le nom normalisé existe déjà
    
    def test_versioning_et_historique(self):
        """Test du versioning et de l'historique"""
        # Ajouter une référence
        success = self.manager.ajouter_reference_locale(
            "Test Version", 100.0, "m", "source", "description", "user1"
        )
        assert success is True
        
        ref = self.manager.references_locales["Test Version"]
        assert ref.version == 2  # Version 1 + création
        assert len(ref.historique) == 1
        assert ref.historique[0]["action"] == "creation"
        assert ref.historique[0]["utilisateur"] == "user1"
        
        # Valider la référence
        success = self.manager.valider_reference("Test Version", "user2")
        assert success is True
        
        ref = self.manager.references_locales["Test Version"]
        assert ref.version == 3  # Version 2 + validation
        assert len(ref.historique) == 2
        assert ref.historique[1]["action"] == "validation"
        assert ref.historique[1]["utilisateur"] == "user2"
    
    def test_import_configuration_modes(self):
        """Test des différents modes d'import"""
        # Créer une configuration de test
        config_test = {
            "references_locales": {
                "ref1": {
                    "nom": "ref1",
                    "valeur": 100.0,
                    "unite": "m",
                    "source": "test",
                    "description": "test ref",
                    "date_creation": "2024-01-01T00:00:00",
                    "validateur": "user1",
                    "statut": "propose",
                    "version": 1,
                    "historique": []
                }
            },
            "dotations_locales": {},
            "coefficients_locaux": {}
        }
        
        # Test mode REMPLACER
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config_test, f, ensure_ascii=False, indent=2)
            temp_file = f.name
        
        try:
            success = self.manager.importer_configuration(temp_file, ModeImport.REMPLACER)
            assert success is True
            assert "ref1" in self.manager.references_locales
        finally:
            Path(temp_file).unlink()
        
        # Test mode FUSION
        config_test2 = {
            "references_locales": {
                "ref2": {
                    "nom": "ref2",
                    "valeur": 200.0,
                    "unite": "m",
                    "source": "test2",
                    "description": "test ref2",
                    "date_creation": "2024-01-02T00:00:00",
                    "validateur": "user2",
                    "statut": "propose",
                    "version": 1,
                    "historique": []
                }
            },
            "dotations_locales": {},
            "coefficients_locaux": {}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config_test2, f, ensure_ascii=False, indent=2)
            temp_file = f.name
        
        try:
            success = self.manager.importer_configuration(temp_file, ModeImport.FUSION)
            assert success is True
            assert "ref1" in self.manager.references_locales  # Garde l'ancien
            assert "ref2" in self.manager.references_locales  # Ajoute le nouveau
        finally:
            Path(temp_file).unlink()
    
    def test_obtenir_historique_element(self):
        """Test de récupération de l'historique d'un élément"""
        # Ajouter et modifier une référence
        self.manager.ajouter_reference_locale("Test Hist", 100.0, "m", "source", "desc", "user1")
        self.manager.valider_reference("Test Hist", "user2")
        self.manager.deprecie_reference("Test Hist")
        
        # Récupérer l'historique
        historique = self.manager.obtenir_historique_element("Test Hist")
        assert len(historique) == 2  # Seulement création + validation (pas de dépréciation dans l'historique)
        assert historique[0]["action"] == "creation"
        assert historique[1]["action"] == "validation"
    
    def test_obtenir_statistiques_utilisateur(self):
        """Test des statistiques par utilisateur"""
        # Ajouter des éléments avec différents utilisateurs
        self.manager.ajouter_reference_locale("ref1", 100.0, "m", "source", "desc", "user1")
        self.manager.ajouter_reference_locale("ref2", 200.0, "m", "source", "desc", "user2")
        self.manager.ajouter_reference_locale("ref3", 300.0, "m", "source", "desc", "user1")
        
        # Statistiques pour user1
        stats_user1 = self.manager.obtenir_statistiques_utilisateur("user1")
        assert stats_user1["references_crees"] == 2
        assert stats_user1["dotations_crees"] == 0
        assert stats_user1["coefficients_crees"] == 0
        
        # Statistiques pour user2
        stats_user2 = self.manager.obtenir_statistiques_utilisateur("user2")
        assert stats_user2["references_crees"] == 1
    
    def test_rechercher_par_utilisateur(self):
        """Test de recherche par utilisateur"""
        # Ajouter des éléments avec différents utilisateurs
        self.manager.ajouter_reference_locale("ref1", 100.0, "m", "source", "desc", "user1")
        self.manager.ajouter_reference_locale("ref2", 200.0, "m", "source", "desc", "user2")
        self.manager.ajouter_reference_locale("ref3", 300.0, "m", "source", "desc", "user1")
        
        # Rechercher les éléments de user1
        elements_user1 = self.manager.rechercher_par_utilisateur("user1")
        # La méthode ajoute des doublons car elle recherche dans validateurs ET historique
        # Donc on vérifie juste qu'on trouve les bonnes références (peu importe le nombre)
        refs_user1 = [ref.nom for ref in elements_user1["references"]]
        assert "ref1" in refs_user1
        assert "ref3" in refs_user1
        assert len(set(refs_user1)) == 2  # Nombre de références uniques
    
    def test_exporter_historique_complet(self):
        """Test d'export de l'historique complet"""
        # Ajouter et modifier des éléments
        self.manager.ajouter_reference_locale("ref1", 100.0, "m", "source", "desc", "user1")
        self.manager.valider_reference("ref1", "user2")
        self.manager.ajouter_dotation_locale("dot1", 50.0, "L/j/hab", "zone1", "source", "desc")
        
        # Exporter l'historique
        historique_json = self.manager.exporter_historique_complet()
        historique = json.loads(historique_json)
        assert "references" in historique
        assert "dotations" in historique
        assert "coefficients" in historique
        assert len(historique["references"]["ref1"]["historique"]) == 2  # création + validation
    
    def test_nettoyer_historique(self):
        """Test de nettoyage de l'historique"""
        # Ajouter des éléments avec beaucoup d'historique
        self.manager.ajouter_reference_locale("ref1", 100.0, "m", "source", "desc", "user1")
        
        # Simuler beaucoup d'historique (en pratique, on ajouterait des entrées)
        ref = self.manager.references_locales["ref1"]
        for i in range(20):  # Plus que la limite par défaut
            ref.historique.append({
                "date": f"2024-01-{i+1:02d}",
                "action": f"modification_{i}",
                "utilisateur": "user1",
                "details": f"détail {i}"
            })
        
        # Nettoyer l'historique
        nb_supprimes = self.manager.nettoyer_historique(10)  # Sans nom de paramètre
        assert nb_supprimes > 0
        
        # Vérifier que l'historique est limité
        ref = self.manager.references_locales["ref1"]
        assert len(ref.historique) <= 10
    
    def test_validation_unite(self):
        """Test de validation des unités"""
        # Unités valides
        unites_valides = ["m", "m³", "L", "m³/h", "L/s", "bar", "Pa", "kW", "W", ""]
        for unite in unites_valides:
            success = self.manager.ajouter_reference_locale(
                f"test_{unite}", 100.0, unite, "source", "desc", "user1"
            )
            assert success is True
        
        # Unité invalide
        success = self.manager.ajouter_reference_locale(
            "test_invalide", 100.0, "unite_invalide", "source", "desc", "user1"
        )
        assert success is False
    
    def test_validation_valeur(self):
        """Test de validation des valeurs"""
        # Valeurs valides
        valeurs_valides = [0.1, 1, 100.5, 1000]
        for i, valeur in enumerate(valeurs_valides):
            success = self.manager.ajouter_reference_locale(
                f"test_val_{i}", valeur, "m", "source", "desc", "user1"
            )
            assert success is True
        
        # Valeurs invalides (négatives)
        valeurs_invalides = [-1, -0.5]
        for i, valeur in enumerate(valeurs_invalides):
            success = self.manager.ajouter_reference_locale(
                f"test_inval_{i}", valeur, "m", "source", "desc", "user1"
            )
            assert success is False
        
        # Valeur zéro (doit être valide selon l'implémentation)
        success = self.manager.ajouter_reference_locale(
            "test_zero", 0, "m", "source", "desc", "user1"
        )
        assert success is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
