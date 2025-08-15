"""
Tests unitaires pour les nouvelles fonctionnalités AEP

Teste les modules :
- Base de données centralisée
- Import automatique
- Validation des données
"""

import pytest
import tempfile
import os
import json
import pandas as pd
from pathlib import Path
import sys

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.database import AEPDatabase
from lcpi.aep.core.import_automatique import AEPImportAutomatique
from lcpi.aep.core.validation_donnees import AEPDataValidator, ValidationError, ValidationResult

class TestAEPDatabase:
    """Tests pour la base de données centralisée"""
    
    def setup_method(self):
        """Initialise la base de données de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_aep.db")
        self.database = AEPDatabase(self.db_path)
    
    def teardown_method(self):
        """Nettoie après les tests"""
        import shutil
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
    
    def test_ajouter_projet(self):
        """Test l'ajout d'un projet"""
        projet_id = self.database.ajouter_projet(
            nom="Projet Test",
            description="Description du projet test",
            metadata={"type": "test", "version": "1.0"}
        )
        
        assert projet_id > 0
        
        # Vérifier que le projet existe
        projets = self.database.obtenir_projets()
        assert len(projets) == 1
        assert projets[0]["nom"] == "Projet Test"
        assert projets[0]["description"] == "Description du projet test"
    
    def test_ajouter_releve_terrain(self):
        """Test l'ajout d'un relevé terrain"""
        # Créer un projet d'abord
        projet_id = self.database.ajouter_projet("Projet Test")
        
        # Ajouter un relevé
        releve_id = self.database.ajouter_releve_terrain(
            projet_id=projet_id,
            type_releve="forage",
            nom_point="FOR001",
            donnees={"profondeur": 50, "debit": 10},
            coordonnees_gps="12.345, -1.234",
            altitude=300,
            operateur="Testeur",
            notes="Relevé de test"
        )
        
        assert releve_id > 0
        
        # Vérifier le relevé
        releves = self.database.obtenir_releves_projet(projet_id)
        assert len(releves) == 1
        assert releves[0]["type_releve"] == "forage"
        assert releves[0]["nom_point"] == "FOR001"
    
    def test_sauvegarder_resultat_calcul(self):
        """Test la sauvegarde d'un résultat de calcul"""
        projet_id = self.database.ajouter_projet("Projet Test")
        
        resultat_id = self.database.sauvegarder_resultat_calcul(
            projet_id=projet_id,
            type_calcul="hardy_cross",
            nom_calcul="Calcul réseau principal",
            parametres_entree={"debit": 100, "longueur": 1000},
            resultats={"debits": [10, 20, 30], "pertes": [5, 10, 15]},
            duree_calcul=2.5,
            version_algorithme="1.0"
        )
        
        assert resultat_id > 0
        
        # Vérifier le résultat
        resultats = self.database.obtenir_resultats_calculs(projet_id)
        assert len(resultats) == 1
        assert resultats[0]["type_calcul"] == "hardy_cross"
        assert resultats[0]["nom_calcul"] == "Calcul réseau principal"
    
    def test_statistiques_projet(self):
        """Test les statistiques de projet"""
        projet_id = self.database.ajouter_projet("Projet Test")
        
        # Ajouter quelques données
        self.database.ajouter_releve_terrain(projet_id, "forage", "FOR001", {"profondeur": 50})
        self.database.ajouter_releve_terrain(projet_id, "pompe", "POMP001", {"debit": 10})
        self.database.sauvegarder_resultat_calcul(projet_id, "hardy_cross", "Test", {}, {})
        
        # Obtenir les statistiques
        stats = self.database.obtenir_statistiques_projet(projet_id)
        
        assert "releves_par_type" in stats
        assert "calculs_par_type" in stats
        assert stats["releves_par_type"]["forage"] == 1
        assert stats["releves_par_type"]["pompe"] == 1
        assert stats["calculs_par_type"]["hardy_cross"] == 1
    
    def test_recherche_donnees(self):
        """Test la recherche de données"""
        projet_id = self.database.ajouter_projet("Projet Test")
        
        # Ajouter des données avec des noms spécifiques
        self.database.ajouter_releve_terrain(projet_id, "forage", "FORAGE_PRINCIPAL", {"profondeur": 50})
        self.database.ajouter_releve_terrain(projet_id, "pompe", "POMPE_SECONDAIRE", {"debit": 10})
        
        # Rechercher
        resultats = self.database.rechercher_donnees(projet_id, "PRINCIPAL")
        
        assert "releves" in resultats
        assert len(resultats["releves"]) == 1
        assert resultats["releves"][0]["nom_point"] == "FORAGE_PRINCIPAL"
    
    def test_export_projet(self):
        """Test l'export de projet"""
        projet_id = self.database.ajouter_projet("Projet Test")
        self.database.ajouter_releve_terrain(projet_id, "forage", "FOR001", {"profondeur": 50})
        
        # Exporter en JSON
        export_json = self.database.exporter_projet(projet_id, "json")
        donnees = json.loads(export_json)
        
        assert "projet" in donnees
        assert "releves_terrain" in donnees
        assert donnees["projet"]["nom"] == "Projet Test"
        assert len(donnees["releves_terrain"]) == 1

class TestAEPImportAutomatique:
    """Tests pour l'import automatique"""
    
    def setup_method(self):
        """Initialise l'import automatique"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_import.db")
        self.database = AEPDatabase(self.db_path)
        self.importateur = AEPImportAutomatique(self.database)
        self.projet_id = self.database.ajouter_projet("Projet Import Test")
    
    def teardown_method(self):
        """Nettoie après les tests"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_types_import_supportes(self):
        """Test les types d'import supportés"""
        types = self.importateur.obtenir_types_import_supportes()
        
        assert "releves_terrain" in types
        assert "pompes" in types
        assert "forages" in types
        assert "reservoirs" in types
        assert "constantes" in types
        assert "enquetes" in types
    
    def test_generer_template(self):
        """Test la génération de template"""
        template_path = os.path.join(self.temp_dir, "template_forages.xlsx")
        
        self.importateur.generer_template("forages", template_path)
        
        assert os.path.exists(template_path)
        
        # Vérifier le contenu du template
        df = pd.read_excel(template_path, sheet_name="Template")
        assert "nom_forage" in df.columns
        assert "profondeur" in df.columns
        assert "debit_test" in df.columns
    
    def test_validation_fichier(self):
        """Test la validation de fichier"""
        # Créer un fichier CSV de test
        csv_path = os.path.join(self.temp_dir, "test_forages.csv")
        donnees_test = pd.DataFrame([
            {"nom_forage": "FOR001", "profondeur": 50, "debit_test": 10},
            {"nom_forage": "FOR002", "profondeur": 80, "debit_test": 15}
        ])
        donnees_test.to_csv(csv_path, index=False)
        
        # Valider le fichier
        resultat = self.importateur.valider_fichier(csv_path, "forages")
        
        assert resultat["valide"] is True
        assert resultat["statistiques"]["lignes"] == 2
        assert resultat["statistiques"]["colonnes"] == 3
    
    def test_import_forages(self):
        """Test l'import de forages"""
        # Créer un fichier CSV de test
        csv_path = os.path.join(self.temp_dir, "forages.csv")
        donnees_test = pd.DataFrame([
            {"nom_forage": "FOR001", "profondeur": 50, "debit_test": 10, "diametre": 200},
            {"nom_forage": "FOR002", "profondeur": 80, "debit_test": 15, "diametre": 250}
        ])
        donnees_test.to_csv(csv_path, index=False)
        
        # Importer
        resultat = self.importateur.importer_fichier(csv_path, "forages", self.projet_id)
        
        assert resultat["importes"] == 2
        assert resultat["erreurs"] == 0
        
        # Vérifier dans la base
        releves = self.database.obtenir_releves_projet(self.projet_id, "forage")
        assert len(releves) == 2
    
    def test_import_pompes(self):
        """Test l'import de pompes"""
        # Créer un fichier CSV de test
        csv_path = os.path.join(self.temp_dir, "pompes.csv")
        donnees_test = pd.DataFrame([
            {"nom_pompe": "POMP001", "type_pompe": "centrifuge", "debit_nominal": 5.0, "puissance": 2.5},
            {"nom_pompe": "POMP002", "type_pompe": "submersible", "debit_nominal": 8.0, "puissance": 4.0}
        ])
        donnees_test.to_csv(csv_path, index=False)
        
        # Importer
        resultat = self.importateur.importer_fichier(csv_path, "pompes", self.projet_id)
        
        assert resultat["importes"] == 2
        assert resultat["erreurs"] == 0
        
        # Vérifier dans la base
        releves = self.database.obtenir_releves_projet(self.projet_id, "pompe")
        assert len(releves) == 2
    
    def test_rapport_import(self):
        """Test la génération de rapport d'import"""
        resultat_test = {
            "importes": 5,
            "erreurs": 1,
            "details": [
                {"ligne": 2, "type": "succes", "message": "Importé avec succès", "id": 1},
                {"ligne": 3, "type": "erreur", "message": "Erreur de validation"}
            ]
        }
        
        rapport = self.importateur.generer_rapport_import(resultat_test, "forages")
        
        assert "Rapport d'Import - FORAGES" in rapport
        assert "Importés avec succès: 5" in rapport
        assert "Erreurs: 1" in rapport
        assert "Taux de succès: 83.3%" in rapport

class TestAEPDataValidator:
    """Tests pour la validation des données"""
    
    def setup_method(self):
        """Initialise le validateur"""
        self.validateur = AEPDataValidator()
    
    def test_validation_donnees_forage(self):
        """Test la validation des données de forage"""
        donnees_forage = {
            "profondeur": 50,
            "debit_test": 10,
            "diametre": 200,
            "niveau_statique": 15,
            "niveau_dynamique": 25,
            "qualite_eau": "bonne"
        }
     