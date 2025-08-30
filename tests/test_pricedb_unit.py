#!/usr/bin/env python3
"""
Tests unitaires complets pour la classe PriceDB.
Utilise pytest pour une structure claire et des assertions robustes.
"""

import sys
import os
import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour pouvoir importer src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.lcpi.aep.optimizer.db import PriceDB, PipeData, ValidationError


class TestPipeData:
    """Tests unitaires pour la classe PipeData (validation Pydantic)."""
    
    def test_valid_pipe_data(self):
        """Test de création d'un objet PipeData valide."""
        data = {
            "dn_mm": 100,
            "material": "PVC-U",
            "supply_fcfa_per_m": 5000.0,
            "pose_fcfa_per_m": 1000.0,
            "total_fcfa_per_m": 6000.0,
            "source_method": "test"
        }
        pipe = PipeData(**data)
        assert pipe.dn_mm == 100
        assert pipe.material == "PVC-U"
        assert pipe.total_fcfa_per_m == 6000.0
    
    def test_invalid_diameter(self):
        """Test de validation du diamètre (doit être > 0)."""
        data = {
            "dn_mm": 0,  # Diamètre invalide
            "material": "PVC-U",
            "total_fcfa_per_m": 6000.0,
            "source_method": "test"
        }
        with pytest.raises(ValidationError):
            PipeData(**data)
    
    def test_invalid_material_empty(self):
        """Test de validation du matériau (ne peut pas être vide)."""
        data = {
            "dn_mm": 100,
            "material": "",  # Matériau vide
            "total_fcfa_per_m": 6000.0,
            "source_method": "test"
        }
        with pytest.raises(ValidationError):
            PipeData(**data)
    
    def test_invalid_material_whitespace(self):
        """Test de validation du matériau (ne peut pas être que des espaces)."""
        data = {
            "dn_mm": 100,
            "material": "   ",  # Matériau avec espaces
            "total_fcfa_per_m": 6000.0,
            "source_method": "test"
        }
        with pytest.raises(ValidationError):
            PipeData(**data)
    
    def test_invalid_negative_price(self):
        """Test de validation du prix (ne peut pas être négatif)."""
        data = {
            "dn_mm": 100,
            "material": "PVC-U",
            "total_fcfa_per_m": -100.0,  # Prix négatif
            "source_method": "test"
        }
        with pytest.raises(ValidationError):
            PipeData(**data)
    
    def test_optional_fields(self):
        """Test des champs optionnels."""
        data = {
            "dn_mm": 100,
            "material": "PVC-U",
            "total_fcfa_per_m": 6000.0,
            "source_method": "test"
            # supply_fcfa_per_m et pose_fcfa_per_m sont optionnels
        }
        pipe = PipeData(**data)
        assert pipe.supply_fcfa_per_m is None
        assert pipe.pose_fcfa_per_m is None


class TestPriceDBInitialization:
    """Tests unitaires pour l'initialisation de PriceDB."""
    
    def test_init_without_path(self):
        """Test d'initialisation sans chemin spécifié."""
        with patch('src.lcpi.aep.optimizer.db.PriceDB._resolve_db_path') as mock_resolve:
            mock_resolve.return_value = None
            db = PriceDB()
            assert db.db_path is None
            assert len(db._candidate_diameters) > 0  # Doit charger le fallback
    
    def test_init_with_valid_path(self):
        """Test d'initialisation avec un chemin valide."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('src.lcpi.aep.optimizer.db.PriceDB._load_from_sqlite') as mock_load:
                mock_load.return_value = [
                    {
                        "dn_mm": 100,
                        "material": "PVC-U",
                        "supply_fcfa_per_m": 5000.0,
                        "pose_fcfa_per_m": 1000.0,
                        "total_fcfa_per_m": 6000.0,
                        "source_method": "sqlite"
                    }
                ]
                db = PriceDB("/fake/path.db")
                # Le chemin est converti en chemin absolu par _resolve_db_path
                assert db.db_path is not None
                assert len(db._candidate_diameters) == 1
    
    def test_init_with_invalid_path(self):
        """Test d'initialisation avec un chemin invalide."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            db = PriceDB("/invalid/path.db")
            # Le chemin invalide est rejeté et db_path devient None
            assert db.db_path is None
            # Doit utiliser le fallback
            assert len(db._candidate_diameters) > 0


class TestPriceDBMethods:
    """Tests unitaires pour les méthodes de PriceDB."""
    
    @pytest.fixture
    def sample_db(self):
        """Fixture pour créer une base de données de test."""
        db = PriceDB()
        # Simuler des données de test
        db._candidate_diameters = [
            PipeData(
                dn_mm=100,
                material="PVC-U",
                supply_fcfa_per_m=5000.0,
                pose_fcfa_per_m=1000.0,
                total_fcfa_per_m=6000.0,
                source_method="test"
            ),
            PipeData(
                dn_mm=150,
                material="PVC-U",
                supply_fcfa_per_m=7500.0,
                pose_fcfa_per_m=1500.0,
                total_fcfa_per_m=9000.0,
                source_method="test"
            ),
            PipeData(
                dn_mm=200,
                material="PEHD",
                supply_fcfa_per_m=10000.0,
                pose_fcfa_per_m=2000.0,
                total_fcfa_per_m=12000.0,
                source_method="test"
            )
        ]
        return db
    
    def test_get_database_info(self, sample_db):
        """Test de la méthode get_database_info."""
        info = sample_db.get_database_info()
        assert 'type' in info
        assert 'diameter_count' in info
        assert 'fallback_used' in info
        assert 'timestamp_utc' in info
        assert info['diameter_count'] == 3
    
    def test_get_candidate_diameters_all(self, sample_db):
        """Test de get_candidate_diameters sans filtre."""
        diameters = sample_db.get_candidate_diameters()
        assert len(diameters) == 3
        assert all(isinstance(d, dict) for d in diameters)
        assert diameters[0]['dn_mm'] == 100
        assert diameters[1]['dn_mm'] == 150
        assert diameters[2]['dn_mm'] == 200
    
    def test_get_candidate_diameters_filtered(self, sample_db):
        """Test de get_candidate_diameters avec filtre matériau."""
        pvc_diameters = sample_db.get_candidate_diameters("PVC-U")
        assert len(pvc_diameters) == 2
        assert all(d['material'] == "PVC-U" for d in pvc_diameters)
        
        pehd_diameters = sample_db.get_candidate_diameters("PEHD")
        assert len(pehd_diameters) == 1
        assert pehd_diameters[0]['material'] == "PEHD"
    
    def test_get_diameter_price_found(self, sample_db):
        """Test de get_diameter_price avec diamètre trouvé."""
        price = sample_db.get_diameter_price(100, "PVC-U")
        assert price == 6000.0
    
    def test_get_diameter_price_not_found(self, sample_db):
        """Test de get_diameter_price avec diamètre non trouvé."""
        price = sample_db.get_diameter_price(999, "PVC-U")
        assert price is None
    
    def test_get_diameter_price_wrong_material(self, sample_db):
        """Test de get_diameter_price avec mauvais matériau."""
        price = sample_db.get_diameter_price(100, "PEHD")
        assert price is None
    
    def test_get_closest_diameter_exact_match(self, sample_db):
        """Test de get_closest_diameter avec correspondance exacte."""
        closest = sample_db.get_closest_diameter(100)
        assert closest['dn_mm'] == 100
        assert closest['material'] == "PVC-U"
    
    def test_get_closest_diameter_approximate(self, sample_db):
        """Test de get_closest_diameter avec correspondance approximative."""
        closest = sample_db.get_closest_diameter(120)
        assert closest['dn_mm'] == 100  # Plus proche de 100 que de 150
        assert closest['material'] == "PVC-U"
    
    def test_get_closest_diameter_with_material(self, sample_db):
        """Test de get_closest_diameter avec filtre matériau."""
        closest = sample_db.get_closest_diameter(120, "PVC-U")
        assert closest['dn_mm'] == 100
        assert closest['material'] == "PVC-U"
    
    def test_get_closest_diameter_prefer_larger(self, sample_db):
        """Test de get_closest_diameter avec prefer_larger=True."""
        # Ajouter un diamètre pour tester l'égalité
        sample_db._candidate_diameters.append(PipeData(
            dn_mm=110,
            material="PVC-U",
            total_fcfa_per_m=7000.0,
            source_method="test"
        ))
        
        closest = sample_db.get_closest_diameter(105, prefer_larger=True)
        assert closest['dn_mm'] == 110  # Préfère le plus grand
    
    def test_get_closest_diameter_prefer_smaller(self, sample_db):
        """Test de get_closest_diameter avec prefer_larger=False."""
        # Ajouter un diamètre pour tester l'égalité
        sample_db._candidate_diameters.append(PipeData(
            dn_mm=110,
            material="PVC-U",
            total_fcfa_per_m=7000.0,
            source_method="test"
        ))
        
        closest = sample_db.get_closest_diameter(105, prefer_larger=False)
        assert closest['dn_mm'] == 100  # Préfère le plus petit
    
    def test_get_closest_diameter_no_candidates(self, sample_db):
        """Test de get_closest_diameter sans candidats."""
        sample_db._candidate_diameters = []
        closest = sample_db.get_closest_diameter(100)
        assert closest is None


class TestPriceDBReload:
    """Tests unitaires pour la méthode reload."""
    
    def test_reload_with_sqlite(self):
        """Test de reload avec base SQLite."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('src.lcpi.aep.optimizer.db.PriceDB._load_from_sqlite') as mock_load:
                mock_load.return_value = [
                    {
                        "dn_mm": 100,
                        "material": "PVC-U",
                        "total_fcfa_per_m": 6000.0,
                        "source_method": "sqlite"
                    }
                ]
                db = PriceDB("/fake/path.db")
                initial_timestamp = db.get_database_info()['timestamp_utc']
                
                # Simuler un délai
                import time
                time.sleep(0.1)
                
                db.reload()
                new_timestamp = db.get_database_info()['timestamp_utc']
                
                assert initial_timestamp != new_timestamp
                assert len(db._candidate_diameters) == 1
    
    def test_reload_with_fallback(self):
        """Test de reload avec fallback."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            db = PriceDB("/invalid/path.db")
            initial_count = len(db._candidate_diameters)
            initial_timestamp = db.get_database_info()['timestamp_utc']
            
            # Simuler un délai
            import time
            time.sleep(0.1)
            
            db.reload()
            new_count = len(db._candidate_diameters)
            new_timestamp = db.get_database_info()['timestamp_utc']
            
            assert initial_timestamp != new_timestamp
            assert initial_count == new_count  # Même nombre de diamètres fallback


class TestPriceDBFallback:
    """Tests unitaires pour le système de fallback."""
    
    def test_fallback_data_structure(self):
        """Test de la structure des données de fallback."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            db = PriceDB("/invalid/path.db")
            
            diameters = db.get_candidate_diameters()
            assert len(diameters) > 0
            
            # Vérifier la structure
            for diameter in diameters:
                assert 'dn_mm' in diameter
                assert 'material' in diameter
                assert 'total_fcfa_per_m' in diameter
                assert 'source_method' in diameter
                assert diameter['source_method'] == 'fallback_realistic_model'
    
    def test_fallback_material_filtering(self):
        """Test du filtrage par matériau avec fallback."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            db = PriceDB("/invalid/path.db")
            
            pvc_diameters = db.get_candidate_diameters("PVC")
            assert len(pvc_diameters) > 0
            assert all(d['material'] == 'PVC' for d in pvc_diameters)
            
            pehd_diameters = db.get_candidate_diameters("PEHD")
            assert len(pehd_diameters) > 0
            assert all(d['material'] == 'PEHD' for d in pehd_diameters)


if __name__ == "__main__":
    # Exécuter les tests avec pytest
    pytest.main([__file__, "-v"])
