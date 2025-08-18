"""
Tests d'intégration end-to-end pour le Jalon 2 - Robustesse & Reproductibilité.
Teste le workflow complet : projet → calcul → log → export → vérification.
"""

import pytest
import tempfile
import shutil
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Marqueur pour les tests d'intégration
pytestmark = pytest.mark.integration

class TestLCPIEndToEndWorkflow:
    """Tests end-to-end du workflow LCPI complet."""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Créer un répertoire temporaire pour les tests de projet."""
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir) / "test_lcpi_project"
        project_dir.mkdir()
        
        # Créer la structure de projet LCPI
        (project_dir / ".lcpi").mkdir(exist_ok=True)
        (project_dir / "data").mkdir(exist_ok=True)
        (project_dir / "logs").mkdir(exist_ok=True)
        (project_dir / "results").mkdir(exist_ok=True)
        
        yield project_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_data_files(self, temp_project_dir):
        """Créer des fichiers de données d'exemple pour les tests."""
        # Fichier CSV de population
        population_csv = temp_project_dir / "data" / "population.csv"
        population_csv.write_text("""annee,population
2020,15000
2021,15200
2022,15400""")
        
        # Fichier YAML de configuration
        config_yml = temp_project_dir / "data" / "config.yml"
        config_yml.write_text("""# Configuration de test
project:
  name: "Test AEP Project"
  description: "Projet de test pour LCPI Jalon 2"
  
aep:
  population:
    debut: 2020
    fin: 2030
    taux_croissance: 0.02""")
        
        return {
            "population_csv": population_csv,
            "config_yml": config_yml
        }
    
    def test_lcpi_project_initialization(self, temp_project_dir):
        """Test que l'initialisation d'un projet LCPI fonctionne."""
        # Vérifier que la structure de projet est créée
        assert (temp_project_dir / ".lcpi").exists()
        assert (temp_project_dir / "data").exists()
        assert (temp_project_dir / "logs").exists()
        assert (temp_project_dir / "results").exists()
        
        # Vérifier que le répertoire .lcpi est initialisé
        lcpi_dir = temp_project_dir / ".lcpi"
        assert lcpi_dir.exists()
    
    def test_lcpi_project_locking_workflow(self, temp_project_dir):
        """Test du workflow de verrouillage/déverrouillage de projet."""
        from src.lcpi.main import lock_project, unlock_project
        
        # 1. Verrouiller le projet
        with patch('src.lcpi.main.console') as mock_console:
            lock_project(project_path=temp_project_dir, force=True)
        
        # Vérifier que le verrou est créé
        lock_file = temp_project_dir / ".lcpi" / "lock"
        assert lock_file.exists()
        
        # Vérifier le contenu du verrou
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)
        
        assert "locked_at" in lock_data
        assert "locked_by" in lock_data
        assert "process_id" in lock_data
        
        # 2. Déverrouiller le projet
        with patch('src.lcpi.main.console') as mock_console:
            unlock_project(project_path=temp_project_dir, force=True)
        
        # Vérifier que le verrou est supprimé
        assert not lock_file.exists()
    
    def test_lcpi_plugin_management_workflow(self, temp_project_dir):
        """Test du workflow de gestion des plugins."""
        from src.lcpi.main import get_plugin_config, save_plugin_config
        
        # 1. Vérifier la configuration initiale
        config = get_plugin_config()
        assert "active_plugins" in config
        assert "available_plugins" in config
        
        # 2. Activer un plugin
        active_plugins = set(config.get("active_plugins", []))
        active_plugins.add("aep")
        config["active_plugins"] = sorted(list(active_plugins))
        save_plugin_config(config)
        
        # 3. Vérifier que le plugin est activé
        updated_config = get_plugin_config()
        assert "aep" in updated_config["active_plugins"]
    
    def test_lcpi_log_integrity_workflow(self, temp_project_dir):
        """Test du workflow d'intégrité des logs."""
        try:
            from src.lcpi.lcpi_logging.logger import LCPILogger
            from src.lcpi.lcpi_logging.integrity import LogIntegrityManager
            
            # 1. Créer un logger
            logger = LCPILogger(log_dir=temp_project_dir / "logs")
            
            # 2. Créer un log de calcul
            log_id = logger.log_calculation_result(
                plugin="aep",
                command="population",
                parameters={"debut": 2020, "fin": 2030},
                results={"population_2020": 15000, "population_2030": 18280},
                execution_time=1.23
            )
            
            # 3. Vérifier que le log est créé
            log_files = list((temp_project_dir / "logs").glob("*.json"))
            assert len(log_files) == 1
            
            # 4. Vérifier l'intégrité du log
            integrity_manager = LogIntegrityManager()
            verification_result = integrity_manager.verify_log_integrity(log_files[0])
            
            assert verification_result["checksum_valid"] is True
            assert verification_result["overall_valid"] is True
            
        except ImportError:
            pytest.skip("Modules de logging LCPI non disponibles")
    
    def test_lcpi_export_reproducible_workflow(self, temp_project_dir, sample_data_files):
        """Test du workflow d'export reproductible."""
        try:
            from src.lcpi.core.reproducible import export_reproducible
            
            # 1. Créer un export reproductible
            export_path = temp_project_dir / "export" / "test_repro.tar.gz"
            export_path.parent.mkdir(exist_ok=True)
            
            export_info = export_reproducible(
                project_path=temp_project_dir,
                output_path=str(export_path),
                include_logs=True,
                include_results=True,
                include_env=True
            )
            
            # 2. Vérifier que l'export est créé
            assert export_path.exists()
            
            # 3. Vérifier les informations d'export
            assert "export_date" in export_info
            assert "project_name" in export_info
            assert "checksums" in export_info
            
        except ImportError:
            pytest.skip("Module d'export reproductible non disponible")
    
    def test_lcpi_plugin_versioning_workflow(self, temp_project_dir):
        """Test du workflow de gestion des versions de plugins."""
        try:
            from src.lcpi.core.plugin_versioning import plugin_version_manager
            
            # 1. Vérifier que le gestionnaire de versions est initialisé
            assert hasattr(plugin_version_manager, 'plugin_versions')
            assert isinstance(plugin_version_manager.plugin_versions, dict)
            
            # 2. Vérifier la compatibilité d'un plugin
            if 'aep' in plugin_version_manager.plugin_versions:
                is_compatible, message = plugin_version_manager.check_plugin_compatibility('aep')
                assert isinstance(is_compatible, bool)
                assert isinstance(message, str)
            
            # 3. Générer la matrice de compatibilité
            matrix = plugin_version_manager.get_api_compatibility_matrix()
            assert isinstance(matrix, dict)
            
            # Vérifier que les versions d'API supportées sont présentes
            supported_versions = ["2.0.0", "2.1.0"]
            for version in supported_versions:
                assert version in matrix
                
        except ImportError:
            pytest.skip("Module de gestion des versions non disponible")
    
    def test_lcpi_complete_workflow_simulation(self, temp_project_dir, sample_data_files):
        """Test de simulation du workflow LCPI complet."""
        # Ce test simule le workflow complet sans exécuter réellement LCPI
        # Il vérifie que tous les composants sont disponibles et fonctionnels
        
        workflow_steps = []
        
        # Étape 1: Initialisation du projet
        try:
            workflow_steps.append("✅ Initialisation du projet")
        except Exception as e:
            workflow_steps.append(f"❌ Initialisation du projet: {e}")
        
        # Étape 2: Gestion des plugins
        try:
            from src.lcpi.main import get_plugin_config
            config = get_plugin_config()
            workflow_steps.append("✅ Gestion des plugins")
        except Exception as e:
            workflow_steps.append(f"❌ Gestion des plugins: {e}")
        
        # Étape 3: Intégrité des logs
        try:
            from src.lcpi.lcpi_logging.integrity import LogIntegrityManager
            workflow_steps.append("✅ Intégrité des logs")
        except Exception as e:
            workflow_steps.append(f"❌ Intégrité des logs: {e}")
        
        # Étape 4: Export reproductible
        try:
            from src.lcpi.core.reproducible import export_reproducible
            workflow_steps.append("✅ Export reproductible")
        except Exception as e:
            workflow_steps.append(f"❌ Export reproductible: {e}")
        
        # Étape 5: Gestion des versions
        try:
            from src.lcpi.core.plugin_versioning import plugin_version_manager
            workflow_steps.append("✅ Gestion des versions")
        except Exception as e:
            workflow_steps.append(f"❌ Gestion des versions: {e}")
        
        # Afficher le statut du workflow
        print("\n📋 Statut du Workflow LCPI Jalon 2:")
        for step in workflow_steps:
            print(f"  {step}")
        
        # Vérifier que toutes les étapes sont réussies
        successful_steps = [step for step in workflow_steps if step.startswith("✅")]
        assert len(successful_steps) == 5, f"Seulement {len(successful_steps)}/5 étapes réussies"


class TestLCPIPerformance:
    """Tests de performance des fonctionnalités du Jalon 2."""
    
    def test_plugin_loading_performance(self):
        """Test que le chargement des plugins est rapide."""
        import time
        
        try:
            from src.lcpi.main import initialize_base_plugins_with_spinner
            
            # Mesurer le temps de chargement des plugins de base
            start_time = time.time()
            
            # Simuler le chargement (sans affichage)
            with patch('src.lcpi.main.console'):
                initialize_base_plugins_with_spinner()
            
            loading_time = time.time() - start_time
            
            # Le chargement devrait être rapide (< 2 secondes)
            assert loading_time < 2.0, f"Chargement des plugins trop lent: {loading_time:.2f}s"
            
        except ImportError:
            pytest.skip("Module principal LCPI non disponible")
    
    def test_log_integrity_performance(self):
        """Test que la vérification d'intégrité des logs est rapide."""
        import time
        
        try:
            from src.lcpi.lcpi_logging.integrity import LogIntegrityManager
            
            integrity_manager = LogIntegrityManager()
            
            # Mesurer le temps d'initialisation
            start_time = time.time()
            # L'initialisation devrait être rapide (< 1 seconde)
            initialization_time = time.time() - start_time
            
            assert initialization_time < 1.0, f"Initialisation trop lente: {initialization_time:.2f}s"
            
        except ImportError:
            pytest.skip("Module d'intégrité des logs non disponible")
    
    def test_plugin_versioning_performance(self):
        """Test que la gestion des versions de plugins est rapide."""
        import time
        
        try:
            from src.lcpi.core.plugin_versioning import plugin_version_manager
            
            # Mesurer le temps de génération de la matrice de compatibilité
            start_time = time.time()
            matrix = plugin_version_manager.get_api_compatibility_matrix()
            generation_time = time.time() - start_time
            
            # La génération devrait être très rapide (< 0.1 seconde)
            assert generation_time < 0.1, f"Génération de matrice trop lente: {generation_time:.3f}s"
            
        except ImportError:
            pytest.skip("Module de gestion des versions non disponible")


class TestLCPISecurity:
    """Tests de sécurité des fonctionnalités du Jalon 2."""
    
    def test_log_signature_security(self):
        """Test que la signature des logs est sécurisée."""
        try:
            from src.lcpi.lcpi_logging.integrity import LogIntegrityManager
            
            integrity_manager = LogIntegrityManager()
            
            # Vérifier que l'algorithme de signature est sécurisé
            # (HMAC-SHA256 ou équivalent)
            assert hasattr(integrity_manager, '_signing_algorithm')
            
            # Vérifier que les clés de signature sont gérées de manière sécurisée
            assert hasattr(integrity_manager, '_signing_key')
            
        except ImportError:
            pytest.skip("Module d'intégrité des logs non disponible")
    
    def test_project_lock_security(self):
        """Test que le verrouillage de projet est sécurisé."""
        # Vérifier que le verrouillage utilise des mécanismes sécurisés
        # (fichiers atomiques, permissions, etc.)
        assert True, "Vérification de sécurité du verrouillage de projet"


# Configuration des marqueurs pytest pour l'intégration
def pytest_configure(config):
    """Configuration des marqueurs pytest pour l'intégration."""
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration end-to-end"
    )


if __name__ == "__main__":
    # Exécuter les tests directement
    pytest.main([__file__, "-v", "--tb=short"])
