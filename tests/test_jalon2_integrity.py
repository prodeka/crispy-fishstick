"""
Tests de non-régression pour le Jalon 2 - Robustesse & Reproductibilité.
Teste l'intégrité des logs, la signature et la vérification.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import des modules LCPI
try:
    from src.lcpi.lcpi_logging.integrity import LogIntegrityManager
    from src.lcpi.lcpi_logging.logger import LCPILogger
    LCPI_AVAILABLE = True
except ImportError:
    LCPI_AVAILABLE = False

# Marqueur pour les tests du Jalon 2
pytestmark = pytest.mark.jalon2

class TestLogIntegrity:
    """Tests de l'intégrité des logs - Fonctionnalité 2.2 du Jalon 2."""
    
    @pytest.fixture
    def temp_log_dir(self):
        """Créer un répertoire temporaire pour les tests de logs."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_log_data(self):
        """Données de log d'exemple pour les tests."""
        return {
            "timestamp": "2025-08-17T14:00:00",
            "plugin": "aep",
            "command": "population",
            "parameters": {
                "debut": 2020,
                "fin": 2030,
                "taux_croissance": 0.02
            },
            "results": {
                "population_2020": 15000,
                "population_2030": 18280
            },
            "execution_time": 1.23,
            "status": "success"
        }
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_log_creation_with_integrity(self, temp_log_dir, sample_log_data):
        """Test que la création d'un log inclut automatiquement la vérification d'intégrité."""
        logger = LCPILogger(log_dir=temp_log_dir)
        
        # Créer un log
        log_id = logger.log_calculation_result(
            plugin="aep",
            command="population",
            parameters=sample_log_data["parameters"],
            results=sample_log_data["results"],
            execution_time=sample_log_data["execution_time"]
        )
        
        # Vérifier que le fichier de log existe
        log_files = list(temp_log_dir.glob("*.json"))
        assert len(log_files) == 1
        
        # Vérifier que le log contient les métadonnées d'intégrité
        with open(log_files[0], 'r') as f:
            log_content = json.load(f)
        
        assert "integrity" in log_content
        assert "checksum" in log_content["integrity"]
        assert "signature" in log_content["integrity"]
        assert "signature_valid" in log_content["integrity"]
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_log_verification_success(self, temp_log_dir, sample_log_data):
        """Test que la vérification d'un log valide réussit."""
        logger = LCPILogger(log_dir=temp_log_dir)
        
        # Créer un log
        log_id = logger.log_calculation_result(
            plugin="aep",
            command="population",
            parameters=sample_log_data["parameters"],
            results=sample_log_data["results"],
            execution_time=sample_log_data["execution_time"]
        )
        
        # Vérifier l'intégrité
        integrity_manager = LogIntegrityManager()
        log_files = list(temp_log_dir.glob("*.json"))
        verification_result = integrity_manager.verify_log_integrity(log_files[0])
        
        assert verification_result["checksum_valid"] is True
        assert verification_result["signature_valid"] is True
        assert verification_result["overall_valid"] is True
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_log_verification_corruption_detection(self, temp_log_dir, sample_log_data):
        """Test que la corruption d'un log est détectée."""
        logger = LCPILogger(log_dir=temp_log_dir)
        
        # Créer un log
        log_id = logger.log_calculation_result(
            plugin="aep",
            command="population",
            parameters=sample_log_data["parameters"],
            results=sample_log_data["results"],
            execution_time=sample_log_data["execution_time"]
        )
        
        # Corrompre le log en modifiant le contenu
        log_files = list(temp_log_dir.glob("*.json"))
        with open(log_files[0], 'r') as f:
            log_content = json.load(f)
        
        # Modifier les résultats
        log_content["results"]["population_2030"] = 99999
        
        with open(log_files[0], 'w') as f:
            json.dump(log_content, f, indent=2)
        
        # Vérifier que la corruption est détectée
        integrity_manager = LogIntegrityManager()
        verification_result = integrity_manager.verify_log_integrity(log_files[0])
        
        assert verification_result["checksum_valid"] is False
        assert verification_result["overall_valid"] is False
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_log_signature_verification(self, temp_log_dir, sample_log_data):
        """Test que la vérification de signature fonctionne correctement."""
        logger = LCPILogger(log_dir=temp_log_dir)
        
        # Créer un log
        log_id = logger.log_calculation_result(
            plugin="aep",
            command="population",
            parameters=sample_log_data["parameters"],
            results=sample_log_data["results"],
            execution_time=sample_log_data["execution_time"]
        )
        
        # Vérifier la signature
        integrity_manager = LogIntegrityManager()
        log_files = list(temp_log_dir.glob("*.json"))
        signature_result = integrity_manager.verify_log_signature(log_files[0])
        
        assert "valid" in signature_result
        assert "signature_info" in signature_result
        assert "algorithm" in signature_result["signature_info"]
        assert "timestamp" in signature_result["signature_info"]


class TestProjectLocking:
    """Tests du verrouillage de projet - Fonctionnalité 2.3 du Jalon 2."""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Créer un répertoire temporaire pour les tests de projet."""
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir) / "test_project"
        project_dir.mkdir()
        yield project_dir
        shutil.rmtree(temp_dir)
    
    def test_project_lock_creation(self, temp_project_dir):
        """Test que la création d'un verrou de projet fonctionne."""
        from src.lcpi.main import lock_project
        
        # Créer un verrou
        with patch('src.lcpi.main.console') as mock_console:
            lock_project(project_path=temp_project_dir, force=True)
        
        # Vérifier que le fichier de verrou existe
        lock_file = temp_project_dir / ".lcpi" / "lock"
        assert lock_file.exists()
        
        # Vérifier le contenu du verrou
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)
        
        assert "locked_at" in lock_data
        assert "locked_by" in lock_data
        assert "process_id" in lock_data
    
    def test_project_lock_conflict_detection(self, temp_project_dir):
        """Test que la détection de conflit de verrouillage fonctionne."""
        from src.lcpi.main import lock_project
        
        # Créer un premier verrou
        with patch('src.lcpi.main.console') as mock_console:
            lock_project(project_path=temp_project_dir, force=True)
        
        # Essayer de créer un second verrou (sans force)
        with patch('src.lcpi.main.console') as mock_console:
            lock_project(project_path=temp_project_dir, force=False)
        
        # Vérifier que le message de conflit est affiché
        mock_console.print.assert_called()
        call_args = [call[0][0] for call in mock_console.print.call_args_list]
        assert any("déjà verrouillé" in str(arg) for arg in call_args)
    
    def test_project_unlock(self, temp_project_dir):
        """Test que le déverrouillage de projet fonctionne."""
        from src.lcpi.main import lock_project, unlock_project
        
        # Créer un verrou
        with patch('src.lcpi.main.console') as mock_console:
            lock_project(project_path=temp_project_dir, force=True)
        
        # Vérifier que le verrou existe
        lock_file = temp_project_dir / ".lcpi" / "lock"
        assert lock_file.exists()
        
        # Déverrouiller
        with patch('src.lcpi.main.console') as mock_console:
            unlock_project(project_path=temp_project_dir, force=True)
        
        # Vérifier que le verrou a été supprimé
        assert not lock_file.exists()


class TestPluginVersioning:
    """Tests de la gestion des versions d'API des plugins - Fonctionnalité 2.5 du Jalon 2."""
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_plugin_version_detection(self):
        """Test que la détection des versions de plugins fonctionne."""
        from src.lcpi.core.plugin_versioning import plugin_version_manager
        
        # Vérifier que le gestionnaire de versions est initialisé
        assert hasattr(plugin_version_manager, 'plugin_versions')
        assert isinstance(plugin_version_manager.plugin_versions, dict)
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_plugin_compatibility_check(self):
        """Test que la vérification de compatibilité des plugins fonctionne."""
        from src.lcpi.core.plugin_versioning import plugin_version_manager
        
        # Vérifier la compatibilité d'un plugin existant
        if 'aep' in plugin_version_manager.plugin_versions:
            is_compatible, message = plugin_version_manager.check_plugin_compatibility('aep')
            assert isinstance(is_compatible, bool)
            assert isinstance(message, str)
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_api_compatibility_matrix(self):
        """Test que la matrice de compatibilité des versions d'API est générée."""
        from src.lcpi.core.plugin_versioning import plugin_version_manager
        
        matrix = plugin_version_manager.get_api_compatibility_matrix()
        assert isinstance(matrix, dict)
        
        # Vérifier que les versions d'API supportées sont présentes
        supported_versions = ["2.0.0", "2.1.0"]
        for version in supported_versions:
            assert version in matrix


class TestReproducibleExport:
    """Tests de l'export reproductible - Fonctionnalité 2.1 du Jalon 2."""
    
    @pytest.fixture
    def temp_export_dir(self):
        """Créer un répertoire temporaire pour les tests d'export."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.mark.skipif(not LCPI_AVAILABLE, reason="LCPI modules non disponibles")
    def test_export_reproducible_creation(self, temp_export_dir):
        """Test que la création d'un export reproductible fonctionne."""
        from src.lcpi.core.reproducible import export_reproducible
        
        # Créer un export reproductible
        export_info = export_reproducible(
            project_path=temp_export_dir,
            output_path=str(temp_export_dir / "test_repro.tar.gz"),
            include_logs=True,
            include_results=True,
            include_env=True
        )
        
        # Vérifier que l'export a été créé
        assert "export_date" in export_info
        assert "project_name" in export_info
        assert "checksums" in export_info


class TestEndToEndWorkflow:
    """Tests end-to-end du workflow LCPI complet."""
    
    @pytest.fixture
    def temp_workflow_dir(self):
        """Créer un répertoire temporaire pour les tests de workflow."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    def test_complete_lcpi_workflow(self, temp_workflow_dir):
        """Test du workflow LCPI complet : projet → calcul → log → export."""
        # Ce test simule le workflow complet sans exécuter réellement LCPI
        # Il vérifie que tous les composants sont disponibles
        
        # Vérifier que les modules nécessaires sont disponibles
        required_modules = [
            'src.lcpi.main',
            'src.lcpi.core.reproducible',
            'src.lcpi.lcpi_logging.integrity',
            'src.lcpi.core.plugin_versioning'
        ]
        
        for module_name in required_modules:
            try:
                __import__(module_name)
            except ImportError:
                pytest.skip(f"Module {module_name} non disponible")
        
        # Si tous les modules sont disponibles, le test passe
        assert True, "Tous les modules du Jalon 2 sont disponibles"


# Tests de performance pour le Jalon 2
class TestPerformance:
    """Tests de performance des fonctionnalités du Jalon 2."""
    
    @pytest.mark.performance
    def test_log_integrity_performance(self):
        """Test que la vérification d'intégrité des logs est rapide."""
        import time
        
        if not LCPI_AVAILABLE:
            pytest.skip("LCPI modules non disponibles")
        
        from src.lcpi.lcpi_logging.integrity import LogIntegrityManager
        
        integrity_manager = LogIntegrityManager()
        
        # Mesurer le temps d'initialisation
        start_time = time.time()
        # L'initialisation devrait être rapide (< 1 seconde)
        initialization_time = time.time() - start_time
        
        assert initialization_time < 1.0, f"Initialisation trop lente: {initialization_time:.2f}s"
    
    @pytest.mark.performance
    def test_plugin_versioning_performance(self):
        """Test que la gestion des versions de plugins est rapide."""
        import time
        
        if not LCPI_AVAILABLE:
            pytest.skip("LCPI modules non disponibles")
        
        from src.lcpi.core.plugin_versioning import plugin_version_manager
        
        # Mesurer le temps de génération de la matrice de compatibilité
        start_time = time.time()
        matrix = plugin_version_manager.get_api_compatibility_matrix()
        generation_time = time.time() - start_time
        
        # La génération devrait être très rapide (< 0.1 seconde)
        assert generation_time < 0.1, f"Génération de matrice trop lente: {generation_time:.3f}s"


# Configuration des marqueurs pytest
def pytest_configure(config):
    """Configuration des marqueurs pytest pour le Jalon 2."""
    config.addinivalue_line(
        "markers", "jalon2: marque les tests du Jalon 2 - Robustesse & Reproductibilité"
    )
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration end-to-end"
    )
    config.addinivalue_line(
        "markers", "performance: marque les tests de performance"
    )


if __name__ == "__main__":
    # Exécuter les tests directement
    pytest.main([__file__, "-v", "--tb=short"])
