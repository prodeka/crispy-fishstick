#!/usr/bin/env python3
"""
Tests unitaires complets pour les modules des suggestions AEP

Ce fichier teste tous les modules créés pour les suggestions :
- Database (Suggestion 1)
- Import Automatique (Suggestion 2) 
- Validation Données (Suggestion 3)
- Recalcul Automatique (Suggestion 6)
"""

import pytest
import tempfile
import shutil
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Tests pour le module Database (Suggestion 1)
class TestAEPDatabase:
    """Tests pour la base de données centralisée"""
    
    def setup_method(self):
        """Initialise la base de données de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_aep.db")
        
        try:
            from lcpi.aep.core.database import AEPDatabase
            self.database = AEPDatabase(self.db_path)
        except ImportError as e:
            pytest.skip(f"Module database non disponible: {e}")
    
    def teardown_method(self):
        """Nettoie après les tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialisation_base(self):
        """Test l'initialisation de la base de données"""
        # Vérifier que la base existe
        assert os.path.exists(self.db_path)
        
        # Vérifier les informations de base
        info = self.database.obtenir_info_base()
        assert info["chemin"] == self.db_path
        assert info["taille_fichier"] > 0
        assert "projets" in info["tables"]
        assert "releves_terrain" in info["tables"]
    
    def test_ajout_projet(self):
        """Test l'ajout d'un projet"""
        projet_id = self.database.ajouter_projet(
            "Projet Test", 
            "Description du projet test",
            {"client": "Test Client", "region": "Test Region"}
        )
        
        assert projet_id > 0
        
        # Vérifier que le projet a été ajouté
        projets = self.database.obtenir_projets()
        assert len(projets) == 1
        assert projets[0]["nom"] == "Projet Test"
        assert projets[0]["description"] == "Description du projet test"
    
    def test_ajout_releve_terrain(self):
        """Test l'ajout d'un relevé terrain"""
        # Créer un projet d'abord
        projet_id = self.database.ajouter_projet("Projet Relevé", "Test relevé")
        
        # Ajouter un relevé
        releve_id = self.database.ajouter_releve_terrain(
            projet_id=projet_id,
            type_releve="forage",
            nom_point="Forage Test",
            donnees={"profondeur": 50, "debit_test": 10.5},
            coordonnees_gps="12.345,67.890",
            altitude=100.0,
            operateur="Testeur",
            notes="Relevé de test"
        )
        
        assert releve_id > 0
        
        # Vérifier le relevé
        releves = self.database.obtenir_releves_projet(projet_id)
        assert len(releves) == 1
        assert releves[0]["type_releve"] == "forage"
        assert releves[0]["nom_point"] == "Forage Test"
        assert releves[0]["donnees"]["profondeur"] == 50
    
    def test_sauvegarde_resultat_calcul(self):
        """Test la sauvegarde d'un résultat de calcul"""
        projet_id = self.database.ajouter_projet("Projet Calcul", "Test calcul")
        
        resultat_id = self.database.sauvegarder_resultat_calcul(
            projet_id=projet_id,
            type_calcul="population",
            nom_calcul="Projection 2030",
            parametres_entree={"population_base": 1000, "taux_croissance": 0.025},
            resultats={"population_2030": 1280},
            duree_calcul=1.5,
            version_algorithme="1.0"
        )
        
        assert resultat_id > 0
        
        # Vérifier le résultat
        resultats = self.database.obtenir_resultats_calculs(projet_id)
        assert len(resultats) == 1
        assert resultats[0]["type_calcul"] == "population"
        assert resultats[0]["nom_calcul"] == "Projection 2030"
    
    def test_statistiques_projet(self):
        """Test les statistiques de projet"""
        projet_id = self.database.ajouter_projet("Projet Stats", "Test statistiques")
        
        # Ajouter quelques données
        self.database.ajouter_releve_terrain(projet_id, "forage", "F1", {"test": 1})
        self.database.ajouter_releve_terrain(projet_id, "pompe", "P1", {"test": 1})
        self.database.sauvegarder_resultat_calcul(projet_id, "test", "calc1", {}, {})
        
        stats = self.database.obtenir_statistiques_projet(projet_id)
        assert stats["total_releves"] == 2
        assert stats["total_calculs"] == 1
        assert "forage" in stats["releves_par_type"]
        assert "pompe" in stats["releves_par_type"]
    
    def test_recherche_donnees(self):
        """Test la recherche de données"""
        projet_id = self.database.ajouter_projet("Projet Recherche", "Test recherche")
        
        # Ajouter des données avec des mots-clés
        self.database.ajouter_releve_terrain(
            projet_id, "forage", "Forage Principal", {"test": 1}, notes="Important forage"
        )
        
        resultats = self.database.rechercher_donnees(projet_id, "Principal")
        assert len(resultats["releves"]) == 1
        assert resultats["releves"][0]["nom_point"] == "Forage Principal"
    
    def test_export_projet(self):
        """Test l'export de projet"""
        projet_id = self.database.ajouter_projet("Projet Export", "Test export")
        
        # Ajouter des données
        self.database.ajouter_releve_terrain(projet_id, "forage", "F1", {"test": 1})
        self.database.sauvegarder_resultat_calcul(projet_id, "test", "calc1", {}, {})
        
        # Exporter en JSON
        export_json = self.database.exporter_projet(projet_id, "json")
        export_data = json.loads(export_json)
        
        assert "projet" in export_data
        assert "releves_terrain" in export_data
        assert "resultats_calculs" in export_data
        assert len(export_data["releves_terrain"]) == 1
        assert len(export_data["resultats_calculs"]) == 1

# Tests pour le module Validation Données (Suggestion 3)
class TestAEPDataValidator:
    """Tests pour la validation des données"""
    
    def setup_method(self):
        """Initialise le validateur de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_validator.db")
        
        try:
            from lcpi.aep.core.database import AEPDatabase
            from lcpi.aep.core.validation_donnees import AEPDataValidator
            self.database = AEPDatabase(self.db_path)
            self.validateur = AEPDataValidator(self.database)
        except ImportError as e:
            pytest.skip(f"Module validation non disponible: {e}")
    
    def teardown_method(self):
        """Nettoie après les tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_validation_coordonnees_gps_valides(self):
        """Test validation de coordonnées GPS valides"""
        resultat = self.validateur.valider_coordonnees_gps("12.345,67.890")
        assert resultat.valide is True
        assert len(resultat.erreurs) == 0
        
        resultat = self.validateur.valider_coordonnees_gps("-45.123;120.456")
        assert resultat.valide is True
        assert len(resultat.erreurs) == 0
    
    def test_validation_coordonnees_gps_invalides(self):
        """Test validation de coordonnées GPS invalides"""
        resultat = self.validateur.valider_coordonnees_gps("invalid")
        assert resultat.valide is False
        assert len(resultat.erreurs) > 0
        
        resultat = self.validateur.valider_coordonnees_gps("91.0,0.0")  # Latitude hors limites
        assert resultat.valide is False
        assert len(resultat.erreurs) > 0
        
        resultat = self.validateur.valider_coordonnees_gps("0.0,181.0")  # Longitude hors limites
        assert resultat.valide is False
        assert len(resultat.erreurs) > 0
    
    def test_validation_releve_terrain(self):
        """Test validation d'un relevé terrain"""
        releve = {
            "id": 1,
            "nom_point": "Test Point",
            "type_releve": "forage",
            "donnees": {
                "profondeur": 50,
                "debit_test": 10.5
            },
            "coordonnees_gps": "12.345,67.890"
        }
        
        resultat = self.validateur.valider_releve_terrain(releve)
        assert resultat.valide is True
    
    def test_validation_releve_terrain_invalide(self):
        """Test validation d'un relevé terrain invalide"""
        releve = {
            "id": 1,
            "nom_point": "",  # Nom manquant
            "type_releve": "forage",
            "donnees": {
                "profondeur": -10,  # Valeur négative
                "debit_test": 10.5
            }
        }
        
        resultat = self.validateur.valider_releve_terrain(releve)
        assert resultat.valide is False
        assert len(resultat.erreurs) > 0
    
    def test_validation_projet_complet(self):
        """Test validation d'un projet complet"""
        # Créer un projet avec des données
        projet_id = self.database.ajouter_projet("Projet Validation", "Test validation")
        
        # Ajouter des relevés valides
        self.database.ajouter_releve_terrain(
            projet_id, "forage", "F1", {"profondeur": 50, "debit_test": 10.5}
        )
        
        # Valider le projet
        resultat = self.validateur.valider_projet_complet(projet_id)
        assert resultat.valide is True
    
    def test_validation_fichier_import(self):
        """Test validation d'un fichier d'import"""
        # Créer un fichier de test
        test_file = os.path.join(self.temp_dir, "test.csv")
        with open(test_file, 'w') as f:
            f.write("nom_forage,profondeur,debit_test\n")
            f.write("F1,50,10.5\n")
        
        resultat = self.validateur.valider_fichier_import(test_file, "forages")
        assert resultat.valide is True
    
    def test_obtenir_recommandations(self):
        """Test obtention des recommandations"""
        projet_id = self.database.ajouter_projet("Projet Rec", "Test recommandations")
        
        # Ajouter un relevé sans GPS
        self.database.ajouter_releve_terrain(
            projet_id, "forage", "F1", {"profondeur": 50}
        )
        
        recommandations = self.validateur.obtenir_recommandations(projet_id)
        assert len(recommandations) > 0
        assert any("GPS" in rec for rec in recommandations)

# Tests pour le module Recalcul Automatique (Suggestion 6)
class TestAEPRecalculEngine:
    """Tests pour le moteur de recalcul automatique"""
    
    def setup_method(self):
        """Initialise le moteur de recalcul de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_recalcul.db")
        
        try:
            from lcpi.aep.core.database import AEPDatabase
            from lcpi.aep.core.recalcul_automatique import AEPRecalculEngine, TypeRecalcul
            self.database = AEPDatabase(self.db_path)
            self.moteur = AEPRecalculEngine(self.database)
            self.TypeRecalcul = TypeRecalcul
        except ImportError as e:
            pytest.skip(f"Module recalcul non disponible: {e}")
    
    def teardown_method(self):
        """Nettoie après les tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_ajout_tache_recalcul(self):
        """Test ajout d'une tâche de recalcul"""
        projet_id = self.database.ajouter_projet("Projet Recalcul", "Test recalcul")
        
        task_id = self.moteur.ajouter_tache_recalcul(
            self.TypeRecalcul.POPULATION,
            projet_id,
            {"population_base": 1000, "taux_croissance": 0.025, "annees": 5}
        )
        
        assert task_id is not None
        assert "population" in task_id
        
        # Vérifier que la tâche est en attente
        statut = self.moteur.obtenir_statut_taches()
        assert statut["taches_en_attente"] == 1
        assert statut["taches_par_type"]["population"] == 1
    
    def test_recalcul_cascade(self):
        """Test recalcul en cascade"""
        projet_id = self.database.ajouter_projet("Projet Cascade", "Test cascade")
        
        taches = self.moteur.declencher_recalcul_cascade(
            self.TypeRecalcul.NETWORK,
            projet_id,
            {"parametres": "test"}
        )
        
        # Vérifier que plusieurs tâches ont été créées (réseau + dépendances)
        assert len(taches) > 1
        
        statut = self.moteur.obtenir_statut_taches()
        assert statut["taches_en_attente"] > 1
    
    @pytest.mark.asyncio
    async def test_execution_taches(self):
        """Test exécution des tâches en attente"""
        projet_id = self.database.ajouter_projet("Projet Execution", "Test execution")
        
        # Ajouter une tâche
        self.moteur.ajouter_tache_recalcul(
            self.TypeRecalcul.POPULATION,
            projet_id,
            {"population_base": 1000, "taux_croissance": 0.025, "annees": 3}
        )
        
        # Exécuter les tâches
        resultats = await self.moteur.executer_taches_en_attente()
        
        assert resultats["taches_executees"] == 1
        assert resultats["erreurs"] == 0
        assert len(resultats["details"]) == 1
        assert resultats["details"][0]["statut"] == "succes"
        
        # Vérifier que le résultat a été sauvegardé
        resultats_db = self.database.obtenir_resultats_calculs(projet_id)
        assert len(resultats_db) == 1
        assert resultats_db[0]["type_calcul"] == "population"
    
    def test_calcul_population(self):
        """Test du calcul de population"""
        parametres = {"population_base": 1000, "taux_croissance": 0.025, "annees": 5}
        resultat = self.moteur._calculer_population(parametres)
        
        assert "population_base" in resultat
        assert "taux_croissance" in resultat
        assert "projections" in resultat
        assert resultat["population_base"] == 1000
        assert len(resultat["projections"]) == 6  # années 0 à 5
    
    def test_calcul_reservoir(self):
        """Test du calcul de réservoir"""
        parametres = {"volume_journalier": 100, "coefficient_pointe": 1.5}
        resultat = self.moteur._calculer_reservoir(parametres)
        
        assert "volume_reservoir" in resultat
        assert "hauteur_recommandee" in resultat
        assert resultat["volume_journalier"] == 100
        assert resultat["coefficient_pointe"] == 1.5
    
    def test_calcul_pumping(self):
        """Test du calcul de pompage"""
        parametres = {"debit": 50, "hauteur_manometrique": 30, "rendement": 0.7}
        resultat = self.moteur._calculer_pumping(parametres)
        
        assert "puissance_hydraulique" in resultat
        assert "puissance_moteur" in resultat
        assert resultat["debit"] == 50
        assert resultat["hauteur_manometrique"] == 30
        assert resultat["rendement"] == 0.7
    
    def test_generer_rapport_recalcul(self):
        """Test génération de rapport de recalcul"""
        resultats = {
            "taches_executees": 2,
            "erreurs": 0,
            "details": [
                {"tache_id": "task1", "statut": "succes", "message": "Succès 1"},
                {"tache_id": "task2", "statut": "succes", "message": "Succès 2"}
            ]
        }
        
        rapport = self.moteur.generer_rapport_recalcul(resultats)
        
        assert "Rapport de Recalcul Automatique" in rapport
        assert "Tâches exécutées: 2" in rapport
        assert "Erreurs: 0" in rapport
        assert "task1" in rapport
        assert "task2" in rapport

# Tests pour le module Import Automatique (Suggestion 2)
class TestAEPImportAutomatique:
    """Tests pour l'import automatique"""
    
    def setup_method(self):
        """Initialise l'importateur de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_import.db")
        
        try:
            from lcpi.aep.core.database import AEPDatabase
            from lcpi.aep.core.import_automatique import AEPImportAutomatique
            self.database = AEPDatabase(self.db_path)
            self.importateur = AEPImportAutomatique(self.database)
        except ImportError as e:
            pytest.skip(f"Module import non disponible: {e}")
    
    def teardown_method(self):
        """Nettoie après les tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_types_import_supportes(self):
        """Test des types d'import supportés"""
        types = self.importateur.obtenir_types_import_supportes()
        
        assert "forages" in types
        assert "pompes" in types
        assert "reservoirs" in types
        assert "constantes" in types
        assert "enquetes" in types
        assert "releves_terrain" in types
    
    def test_generer_template(self):
        """Test génération de template"""
        template_path = os.path.join(self.temp_dir, "template_forages.xlsx")
        
        success = self.importateur.generer_template("forages", template_path)
        assert success is True
        assert os.path.exists(template_path)
    
    def test_valider_fichier(self):
        """Test validation de fichier"""
        # Créer un fichier CSV valide
        csv_path = os.path.join(self.temp_dir, "forages.csv")
        with open(csv_path, 'w') as f:
            f.write("nom_forage,profondeur,debit_test\n")
            f.write("F1,50,10.5\n")
            f.write("F2,60,12.0\n")
        
        resultat = self.importateur.valider_fichier(csv_path, "forages")
        assert resultat["valide"] is True
        assert resultat["statistiques"]["lignes"] == 2
        assert resultat["statistiques"]["colonnes"] == 3
    
    def test_valider_fichier_invalide(self):
        """Test validation de fichier invalide"""
        # Créer un fichier CSV invalide (colonnes manquantes)
        csv_path = os.path.join(self.temp_dir, "forages_invalide.csv")
        with open(csv_path, 'w') as f:
            f.write("nom_forage,profondeur\n")  # debit_test manquant
            f.write("F1,50\n")
        
        resultat = self.importateur.valider_fichier(csv_path, "forages")
        assert resultat["valide"] is False
        assert "debit_test" in resultat["erreur"]
    
    def test_importer_forages(self):
        """Test import de forages"""
        projet_id = self.database.ajouter_projet("Projet Import", "Test import")
        
        # Créer un fichier CSV de forages
        csv_path = os.path.join(self.temp_dir, "forages.csv")
        with open(csv_path, 'w') as f:
            f.write("nom_forage,profondeur,debit_test,diametre\n")
            f.write("F1,50,10.5,200\n")
            f.write("F2,60,12.0,250\n")
        
        resultat = self.importateur.importer_fichier(csv_path, "forages", projet_id)
        
        assert resultat["importes"] == 2
        assert resultat["erreurs"] == 0
        assert len(resultat["details"]) == 2
        
        # Vérifier que les données ont été importées
        releves = self.database.obtenir_releves_projet(projet_id, "forage")
        assert len(releves) == 2
        assert releves[0]["nom_point"] == "F1"
        assert releves[0]["donnees"]["profondeur"] == 50.0
    
    def test_importer_pompes(self):
        """Test import de pompes"""
        projet_id = self.database.ajouter_projet("Projet Pompes", "Test pompes")
        
        # Créer un fichier CSV de pompes
        csv_path = os.path.join(self.temp_dir, "pompes.csv")
        with open(csv_path, 'w') as f:
            f.write("nom_pompe,type_pompe,debit_nominal,puissance\n")
            f.write("P1,centrifuge,50,10.5\n")
            f.write("P2,submersible,30,8.0\n")
        
        resultat = self.importateur.importer_fichier(csv_path, "pompes", projet_id)
        
        assert resultat["importes"] == 2
        assert resultat["erreurs"] == 0
        
        # Vérifier les données
        releves = self.database.obtenir_releves_projet(projet_id, "pompe")
        assert len(releves) == 2
        assert releves[0]["nom_point"] == "P1"
        assert releves[0]["donnees"]["type_pompe"] == "centrifuge"
    
    def test_generer_rapport_import(self):
        """Test génération de rapport d'import"""
        resultat = {
            "importes": 3,
            "erreurs": 1,
            "details": [
                {"ligne": 2, "type": "succes", "message": "Importé avec succès"},
                {"ligne": 3, "type": "succes", "message": "Importé avec succès"},
                {"ligne": 4, "type": "succes", "message": "Importé avec succès"},
                {"ligne": 5, "type": "erreur", "message": "Erreur d'import"}
            ]
        }
        
        rapport = self.importateur.generer_rapport_import(resultat, "forages")
        
        assert "Rapport d'Import - FORAGES" in rapport
        assert "Importés avec succès: 3" in rapport
        assert "Erreurs: 1" in rapport
        assert "Taux de succès: 75.0%" in rapport

if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
