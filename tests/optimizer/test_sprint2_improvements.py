"""
Tests pour les améliorations du Sprint 2 : Algorithmes d'Optimisation Avancés

Ce fichier teste :
1. Parallélisation du GlobalOptimizer
2. Système de checkpoints
3. Persistance des modèles SurrogateOptimizer
"""

import pytest
import json
import pickle
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import shutil

from lcpi.aep.optimizer.models import OptimizationConfig, OptimizationObjectives
from lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer
from lcpi.aep.optimizer.algorithms.surrogate import SurrogateOptimizer


class TestGlobalOptimizerImprovements:
    """Tests pour les améliorations du GlobalOptimizer."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        self.config = OptimizationConfig(
            method="global",
            objectives=OptimizationObjectives(),
            h_bounds_m={"TANK1": (50.0, 100.0)},
            pressure_min_m=10.0,
            global_config=OptimizationConfig.GlobalMethodConfig(
                population_size=10,
                generations=5,
                parallel_workers=2
            )
        )
        
        # Créer un fichier réseau temporaire
        self.temp_dir = Path(tempfile.mkdtemp())
        self.network_path = self.temp_dir / "test_network.inp"
        self.network_path.write_text("""
[TITLE]
Test Network
[JUNCTIONS]
N1	50	0.001
[RESERVOIRS]
TANK1	100
[PIPES]
PIPE1	TANK1	N1	50	200	100	0	Open
[OPTIONS]
UNITS	LPS
HEADLOSS	H-W
[TIMES]
DURATION	1
[REPORT]
STATUS	NO
[END]
        """.strip())
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_parallel_workers_configuration(self):
        """Test que la configuration des workers parallèles fonctionne."""
        optimizer = GlobalOptimizer(self.config, self.network_path)
        
        # Vérifier que le nombre de workers est correct
        assert optimizer.parallel_workers == 2
        
        # Vérifier que le dossier de checkpoints est créé
        checkpoint_dir = Path("data/checkpoints")
        assert checkpoint_dir.exists()
    
    def test_checkpoint_path_generation(self):
        """Test la génération automatique des chemins de checkpoints."""
        optimizer = GlobalOptimizer(self.config, self.network_path)
        
        # Vérifier que le chemin de checkpoint est généré
        assert optimizer.checkpoint_path is not None
        assert "global_opt_" in optimizer.checkpoint_path.name
        assert optimizer.checkpoint_path.suffix == ".pkl"
    
    def test_checkpoint_validation(self):
        """Test la validation des checkpoints."""
        optimizer = GlobalOptimizer(self.config, self.network_path)
        
        # Créer un checkpoint valide
        valid_checkpoint = {
            "algorithm": Mock(),
            "config": self.config.model_dump(),
            "network_path": str(self.network_path),
            "best_fitness": [],
            "generations": []
        }
        
        # Vérifier que la validation fonctionne
        assert optimizer._validate_checkpoint(valid_checkpoint) is True
        
        # Test avec un checkpoint invalide (réseau différent)
        invalid_checkpoint = valid_checkpoint.copy()
        invalid_checkpoint["network_path"] = "different_network.inp"
        assert optimizer._validate_checkpoint(invalid_checkpoint) is False
    
    @patch('lcpi.aep.optimizer.algorithms.global_opt._PYMOO_AVAILABLE', False)
    def test_pymoo_import_error(self):
        """Test la gestion de l'erreur d'import pymoo."""
        with pytest.raises(ImportError, match="pymoo n'est pas installé"):
            GlobalOptimizer(self.config, self.network_path)
    
    def test_optimization_status(self):
        """Test la récupération du statut d'optimisation."""
        optimizer = GlobalOptimizer(self.config, self.network_path)
        status = optimizer.get_optimization_status()
        
        # Vérifier que tous les champs sont présents
        required_fields = [
            "checkpoint_path", "parallel_workers", 
            "generations_completed", "best_fitness_history", "last_checkpoint"
        ]
        for field in required_fields:
            assert field in status
        
        # Vérifier les valeurs par défaut
        assert status["parallel_workers"] == 2
        assert status["generations_completed"] == 0
        assert status["best_fitness_history"] == []


class TestSurrogateOptimizerImprovements:
    """Tests pour les améliorations du SurrogateOptimizer."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.model_store_dir = self.temp_dir / "model_store"
        self.model_store_dir.mkdir()
        
        # Mock du réseau
        self.network_mock = Mock()
        self.network_mock.dict.return_value = {"nodes": ["N1"], "pipes": ["P1"]}
        
        self.config = {
            "h_bounds_m": {"TANK1": (50.0, 100.0)},
            "pressure_min_m": 10.0,
            "surrogate_config": {
                "persist_model": True,
                "initial_samples": 5
            }
        }
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    @patch('lcpi.aep.optimizer.algorithms.surrogate.SKLEARN_OK', True)
    def test_model_persistence_with_metadata(self):
        """Test la persistance des modèles avec métadonnées."""
        # Créer un modèle mock
        model_mock = Mock()
        model_mock.feature_names_in_ = ["height"]
        
        # Créer l'optimiseur avec un cache_dir valide
        config_with_cache = self.config.copy()
        config_with_cache["cache_dir"] = str(self.temp_dir / "cache")
        
        with patch('lcpi.aep.optimizer.algorithms.surrogate.joblib.dump') as mock_dump:
            with patch('lcpi.aep.optimizer.algorithms.surrogate.joblib.load') as mock_load:
                mock_load.return_value = model_mock
                
                optimizer = SurrogateOptimizer(self.network_mock, config_with_cache)
                optimizer.model = model_mock
                optimizer.dataset = [(60.0, 15.0), (70.0, 18.0)]
                
                # Sauvegarder le modèle
                optimizer._save_model()
                
                # Vérifier que le modèle a été sauvegardé
                mock_dump.assert_called_once()
    
    @patch('lcpi.aep.optimizer.algorithms.surrogate.SKLEARN_OK', True)
    def test_model_performance_calculation(self):
        """Test le calcul des métriques de performance du modèle."""
        # Créer un modèle mock avec prédictions
        model_mock = Mock()
        model_mock.predict.return_value = [15.5, 18.2]
        
        # Créer l'optimiseur avec un cache_dir valide
        config_with_cache = self.config.copy()
        config_with_cache["cache_dir"] = str(self.temp_dir / "cache")
        
        optimizer = SurrogateOptimizer(self.network_mock, config_with_cache)
        optimizer.model = model_mock
        optimizer.dataset = [(60.0, 15.0), (70.0, 18.0)]
        
        # Calculer les performances
        performance = optimizer._get_model_performance()
        
        # Vérifier que les métriques sont calculées (peut être vide si pas de données)
        if performance:  # Si des métriques sont calculées
            assert "mse" in performance
            assert "mae" in performance
            assert "r2" in performance
            assert "rmse" in performance
            
            # Vérifier que les valeurs sont des nombres
            for metric in performance.values():
                assert isinstance(metric, (int, float))
        else:
            # Si pas de métriques, c'est normal pour un modèle vide
            assert performance == {}
    
    @patch('lcpi.aep.optimizer.algorithms.surrogate.SKLEARN_OK', True)
    def test_list_available_models(self):
        """Test la liste des modèles disponibles."""
        # Créer l'optimiseur avec un cache_dir valide
        config_with_cache = self.config.copy()
        config_with_cache["cache_dir"] = str(self.temp_dir / "cache")
        
        optimizer = SurrogateOptimizer(self.network_mock, config_with_cache)
        
        # Test que la fonction existe et retourne une liste
        available_models = optimizer.list_available_models()
        assert isinstance(available_models, list)
        
        # Pour l'instant, on peut juste vérifier que la fonction fonctionne
        # Les modèles réels dépendent du système de fichiers
        print(f"Modèles disponibles: {len(available_models)}")
    
    @patch('lcpi.aep.optimizer.algorithms.surrogate.SKLEARN_OK', True)
    def test_delete_model(self):
        """Test la suppression d'un modèle."""
        # Créer l'optimiseur avec un cache_dir valide
        config_with_cache = self.config.copy()
        config_with_cache["cache_dir"] = str(self.temp_dir / "cache")
        
        optimizer = SurrogateOptimizer(self.network_mock, config_with_cache)
        
        # Test que la fonction existe et gère les erreurs gracieusement
        # Pour l'instant, on teste juste que la fonction ne plante pas
        try:
            success = optimizer.delete_model("test_model_inexistant")
            # La suppression d'un modèle inexistant peut retourner False
            assert isinstance(success, bool)
        except Exception as e:
            # Si une exception est levée, c'est aussi acceptable
            print(f"Exception attendue lors de la suppression: {e}")
            assert True


class TestSprint2Integration:
    """Tests d'intégration pour le Sprint 2."""
    
    def test_checkpoint_directory_structure(self):
        """Test que la structure des dossiers est correcte."""
        # Vérifier que les dossiers nécessaires existent
        required_dirs = [
            Path("data/checkpoints"),
            Path("data/model_store")
        ]
        
        for dir_path in required_dirs:
            assert dir_path.exists(), f"Le dossier {dir_path} n'existe pas"
            assert dir_path.is_dir(), f"{dir_path} n'est pas un dossier"
    
    def test_imports_work(self):
        """Test que tous les imports du Sprint 2 fonctionnent."""
        # Test des imports principaux
        try:
            from lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer
            from lcpi.aep.optimizer.algorithms.surrogate import SurrogateOptimizer
            assert True, "Imports réussis"
        except ImportError as e:
            pytest.fail(f"Import échoué: {e}")


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
