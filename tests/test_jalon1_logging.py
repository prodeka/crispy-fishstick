#!/usr/bin/env python3
"""
Tests pour le Jalon 1 : Fondations de l'Auditabilité et du Reporting
Teste le système de journalisation et la commande rapport.
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Import des modules à tester
from src.lcpi.logging import (
    log_calculation_result, 
    LogEntryModel, 
    calculate_input_hash,
    list_available_logs,
    load_log_by_id
)


class TestLoggingSystem:
    """Tests pour le système de journalisation."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        # Créer un répertoire temporaire pour les tests
        self.temp_dir = Path(tempfile.mkdtemp())
        self.logs_dir = self.temp_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_log_entry_model_validation(self):
        """Test de validation du modèle LogEntryModel."""
        # Test avec données valides
        valid_data = {
            "id": "20250127_143022",
            "timestamp": "2025-01-27T14:30:22",
            "titre_calcul": "Test de calcul",
            "commande_executee": "lcpi aep network-unified 0.1",
            "donnees_resultat": {"resultat": "test"}
        }
        
        log_entry = LogEntryModel(**valid_data)
        assert log_entry.id == "20250127_143022"
        assert log_entry.titre_calcul == "Test de calcul"
        
        # Test avec données invalides (manque de champs obligatoires)
        invalid_data = {
            "id": "20250127_143022",
            # timestamp manquant
            "titre_calcul": "Test de calcul"
            # commande_executee et donnees_resultat manquants
        }
        
        with pytest.raises(Exception):
            LogEntryModel(**invalid_data)
    
    def test_calculate_input_hash(self):
        """Test du calcul de hash des données d'entrée."""
        input_data = {
            "debit_m3s": 0.1,
            "longueur_m": 1000,
            "materiau": "fonte"
        }
        
        hash1 = calculate_input_hash(input_data)
        hash2 = calculate_input_hash(input_data)
        
        # Le hash doit être reproductible
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 = 64 caractères hex
        
        # Le hash doit être différent pour des données différentes
        input_data2 = {
            "debit_m3s": 0.2,  # Différent
            "longueur_m": 1000,
            "materiau": "fonte"
        }
        hash3 = calculate_input_hash(input_data2)
        assert hash1 != hash3
    
    def test_log_calculation_result(self):
        """Test de la journalisation d'un calcul."""
        titre_calcul = "Test de dimensionnement réseau"
        commande_executee = "lcpi aep network-unified 0.1 --longueur 1000"
        donnees_resultat = {
            "diametre_m": 0.2,
            "vitesse_ms": 1.5,
            "perte_charge_m": 2.3
        }
        parametres_entree = {
            "debit_m3s": 0.1,
            "longueur_m": 1000,
            "materiau": "fonte"
        }
        transparence_mathematique = [
            "Débit: 0.1 m³/s",
            "Longueur: 1000 m",
            "Diamètre calculé: 0.2 m"
        ]
        
        # Journaliser le calcul
        log_id = log_calculation_result(
            titre_calcul=titre_calcul,
            commande_executee=commande_executee,
            donnees_resultat=donnees_resultat,
            projet_dir=self.temp_dir,
            parametres_entree=parametres_entree,
            transparence_mathematique=transparence_mathematique,
            version_algorithme="2.1.0",
            verbose=False
        )
        
        # Vérifier que le fichier a été créé
        log_file = self.logs_dir / f"log_{log_id}.json"
        assert log_file.exists()
        
        # Vérifier le contenu du fichier
        with open(log_file, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        
        assert log_data["id"] == log_id
        assert log_data["titre_calcul"] == titre_calcul
        assert log_data["commande_executee"] == commande_executee
        assert log_data["donnees_resultat"] == donnees_resultat
        assert log_data["parametres_entree"] == parametres_entree
        assert log_data["transparence_mathematique"] == transparence_mathematique
        assert log_data["version_algorithme"] == "2.1.0"
        assert log_data["hash_donnees_entree"] is not None
        
        # Vérifier que le hash correspond aux paramètres d'entrée
        expected_hash = calculate_input_hash(parametres_entree)
        assert log_data["hash_donnees_entree"] == expected_hash
    
    def test_list_available_logs(self):
        """Test de la liste des logs disponibles."""
        # Créer quelques logs de test
        log1_data = {
            "id": "20250127_143022",
            "timestamp": "2025-01-27T14:30:22",
            "titre_calcul": "Calcul 1",
            "commande_executee": "lcpi aep network-unified 0.1",
            "donnees_resultat": {"resultat": "test1"}
        }
        
        log2_data = {
            "id": "20250127_143023",
            "timestamp": "2025-01-27T14:30:23",
            "titre_calcul": "Calcul 2",
            "commande_executee": "lcpi aep demand-unified 1000",
            "donnees_resultat": {"resultat": "test2"}
        }
        
        # Sauvegarder les logs
        with open(self.logs_dir / "log_20250127_143022.json", 'w', encoding='utf-8') as f:
            json.dump(log1_data, f, indent=2)
        
        with open(self.logs_dir / "log_20250127_143023.json", 'w', encoding='utf-8') as f:
            json.dump(log2_data, f, indent=2)
        
        # Lister les logs
        logs = list_available_logs(self.temp_dir)
        
        assert len(logs) == 2
        assert logs[0]["id"] == "20250127_143023"  # Plus récent en premier
        assert logs[1]["id"] == "20250127_143022"
        assert logs[0]["titre_calcul"] == "Calcul 2"
        assert logs[1]["titre_calcul"] == "Calcul 1"
    
    def test_load_log_by_id(self):
        """Test du chargement d'un log par ID."""
        # Créer un log de test
        log_data = {
            "id": "20250127_143022",
            "timestamp": "2025-01-27T14:30:22",
            "titre_calcul": "Test de calcul",
            "commande_executee": "lcpi aep network-unified 0.1",
            "donnees_resultat": {"resultat": "test"}
        }
        
        with open(self.logs_dir / "log_20250127_143022.json", 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        
        # Charger le log
        loaded_data = load_log_by_id("20250127_143022", self.temp_dir)
        
        assert loaded_data is not None
        assert loaded_data["id"] == "20250127_143022"
        assert loaded_data["titre_calcul"] == "Test de calcul"
        
        # Test avec un ID inexistant
        non_existent = load_log_by_id("inexistant", self.temp_dir)
        assert non_existent is None


class TestCLIIntegration:
    """Tests d'intégration avec les commandes CLI."""
    
    def test_network_unified_logging_integration(self):
        """Test de l'intégration de la journalisation dans network-unified."""
        # Ce test simule l'utilisation de la commande network-unified avec journalisation
        # En pratique, cela nécessiterait de mocker les dépendances
        
        # Test de la structure des paramètres d'entrée
        parametres_entree = {
            "debit_m3s": 0.1,
            "longueur_m": 1000,
            "materiau": "fonte",
            "perte_charge_max_m": 10.0,
            "methode": "darcy",
            "mode": "simple",
            "input_file": None
        }
        
        # Vérifier que les paramètres sont valides
        assert parametres_entree["debit_m3s"] > 0
        assert parametres_entree["longueur_m"] > 0
        assert parametres_entree["materiau"] in ["fonte", "acier", "pvc", "pe", "beton", "fibro-ciment"]
        assert parametres_entree["methode"] in ["darcy", "hazen", "manning"]
    
    def test_commande_executee_generation(self):
        """Test de la génération de la commande exécutée."""
        # Simuler la génération de la commande comme dans network-unified
        debit_m3s = 0.1
        longueur_m = 1000
        materiau = "fonte"
        perte_charge_max_m = 10.0
        methode = "darcy"
        verbose = False
        input_file = None
        mode = "auto"
        
        commande_parts = ["lcpi", "aep", "network-unified", str(debit_m3s)]
        if longueur_m != 1000:
            commande_parts.extend(["--longueur", str(longueur_m)])
        if materiau != "fonte":
            commande_parts.extend(["--materiau", materiau])
        if perte_charge_max_m != 10.0:
            commande_parts.extend(["--perte-max", str(perte_charge_max_m)])
        if methode != "darcy":
            commande_parts.extend(["--methode", methode])
        if verbose:
            commande_parts.append("--verbose")
        if input_file:
            commande_parts.extend(["--input", str(input_file)])
        if mode != "auto":
            commande_parts.extend(["--mode", mode])
        
        commande_executee = " ".join(commande_parts)
        
        expected = "lcpi aep network-unified 0.1"
        assert commande_executee == expected
        
        # Test avec des paramètres non-défaut
        debit_m3s = 0.2
        longueur_m = 500
        materiau = "pvc"
        
        commande_parts = ["lcpi", "aep", "network-unified", str(debit_m3s)]
        if longueur_m != 1000:
            commande_parts.extend(["--longueur", str(longueur_m)])
        if materiau != "fonte":
            commande_parts.extend(["--materiau", materiau])
        
        commande_executee = " ".join(commande_parts)
        expected = "lcpi aep network-unified 0.2 --longueur 500 --materiau pvc"
        assert commande_executee == expected


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
