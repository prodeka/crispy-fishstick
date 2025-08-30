#!/usr/bin/env python3
"""
Tests d'intégration pour la classe PriceDB.
Teste le comportement complet avec des bases de données réelles.
"""

import sys
import os
import tempfile
import sqlite3
import pytest
from pathlib import Path

# Ajouter le répertoire parent au path pour pouvoir importer src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.lcpi.aep.optimizer.db import PriceDB, PipeData


class TestPriceDBIntegration:
    """Tests d'intégration pour PriceDB avec bases de données réelles."""
    
    def create_test_sqlite_db(self, db_path: str) -> None:
        """Crée une base de données SQLite de test."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Créer la table metadata
        cursor.execute("""
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("INSERT INTO metadata (key, value) VALUES (?, ?)", 
                      ("db_version", "1.0.0"))
        
        # Créer la table diameters
        cursor.execute("""
            CREATE TABLE diameters (
                dn_mm INTEGER,
                material TEXT,
                supply_fcfa_per_m REAL,
                pose_fcfa_per_m REAL,
                total_fcfa_per_m REAL,
                source_method TEXT
            )
        """)
        
        # Insérer des données de test
        test_data = [
            (100, "PVC-U", 5000.0, 1000.0, 6000.0, "sqlite"),
            (150, "PVC-U", 7500.0, 1500.0, 9000.0, "sqlite"),
            (200, "PEHD", 10000.0, 2000.0, 12000.0, "sqlite"),
            (250, "PEHD", 12500.0, 2500.0, 15000.0, "sqlite"),
            (300, "Fonte", 20000.0, 4000.0, 24000.0, "sqlite")
        ]
        
        cursor.executemany("""
            INSERT INTO diameters 
            (dn_mm, material, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m, source_method)
            VALUES (?, ?, ?, ?, ?, ?)
        """, test_data)
        
        conn.commit()
        conn.close()
    
    def test_integration_with_real_sqlite(self):
        """Test d'intégration avec une vraie base SQLite."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        try:
            # Créer la base de données de test
            self.create_test_sqlite_db(db_path)
            
            # Tester PriceDB avec cette base
            db = PriceDB(db_path)
            
            # Vérifier les informations de base
            info = db.get_database_info()
            assert info['type'] == 'sqlite'
            assert info['diameter_count'] == 5
            assert info['fallback_used'] == False
            assert info['db_version'] == '1.0.0'
            assert 'timestamp_utc' in info
            
            # Vérifier les diamètres
            diameters = db.get_candidate_diameters()
            assert len(diameters) == 5
            
            # Vérifier le filtrage par matériau
            pvc_diameters = db.get_candidate_diameters("PVC-U")
            assert len(pvc_diameters) == 2
            assert all(d['material'] == 'PVC-U' for d in pvc_diameters)
            
            pehd_diameters = db.get_candidate_diameters("PEHD")
            assert len(pehd_diameters) == 2
            assert all(d['material'] == 'PEHD' for d in pehd_diameters)
            
            # Tester get_diameter_price
            price = db.get_diameter_price(100, "PVC-U")
            assert price == 6000.0
            
            # Tester get_closest_diameter
            closest = db.get_closest_diameter(120)
            assert closest['dn_mm'] == 100  # Plus proche de 100 que de 150
            
            # Tester reload
            initial_timestamp = info['timestamp_utc']
            db.reload()
            new_info = db.get_database_info()
            assert new_info['timestamp_utc'] != initial_timestamp
            
            # Fermer explicitement la connexion
            if hasattr(db, '_conn') and db._conn:
                db._conn.close()
                db._conn = None
            
        finally:
            # Nettoyer
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # Ignorer l'erreur si le fichier est encore utilisé
                pass
    
    def test_integration_fallback_behavior(self):
        """Test d'intégration du comportement de fallback."""
        # Créer une instance avec un chemin inexistant
        db = PriceDB("/chemin/inexistant/vers/db.db")
        
        # Vérifier que le fallback est utilisé
        info = db.get_database_info()
        assert info['type'] == 'fallback'
        assert info['fallback_used'] == True
        assert info['path'] == 'N/A'
        
        # Vérifier que les données de fallback sont présentes
        diameters = db.get_candidate_diameters()
        assert len(diameters) > 0
        
        # Vérifier la structure des données de fallback
        for diameter in diameters:
            assert 'dn_mm' in diameter
            assert 'material' in diameter
            assert 'total_fcfa_per_m' in diameter
            assert 'source_method' in diameter
            assert diameter['source_method'] == 'fallback_realistic_model'
    
    def test_integration_mixed_scenarios(self):
        """Test d'intégration de scénarios mixtes."""
        # Test 1: Base SQLite valide
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        try:
            self.create_test_sqlite_db(db_path)
            db = PriceDB(db_path)
            
            # Vérifier que les données SQLite sont chargées
            assert db.get_database_info()['type'] == 'sqlite'
            assert len(db.get_candidate_diameters()) == 5
            
            # Test 2: Supprimer la base et recharger (doit passer en fallback)
            # Fermer d'abord la connexion
            if hasattr(db, '_conn') and db._conn:
                db._conn.close()
                db._conn = None
            
            os.unlink(db_path)
            db.reload()
            
            # Vérifier que le fallback est maintenant utilisé
            assert db.get_database_info()['type'] == 'fallback'
            assert len(db.get_candidate_diameters()) > 0
            
        finally:
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                pass
    
    def test_integration_data_validation(self):
        """Test d'intégration de la validation des données."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        try:
            # Créer une base avec des données invalides
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE diameters (
                    dn_mm INTEGER,
                    material TEXT,
                    supply_fcfa_per_m REAL,
                    pose_fcfa_per_m REAL,
                    total_fcfa_per_m REAL,
                    source_method TEXT
                )
            """)
            
            # Insérer des données valides et invalides
            test_data = [
                (100, "PVC-U", 5000.0, 1000.0, 6000.0, "sqlite"),  # Valide
                (0, "PVC-U", 5000.0, 1000.0, 6000.0, "sqlite"),    # Diamètre invalide
                (150, "", 7500.0, 1500.0, 9000.0, "sqlite"),       # Matériau vide
                (200, "PEHD", -1000.0, 2000.0, 1000.0, "sqlite"),  # Prix négatif
            ]
            
            cursor.executemany("""
                INSERT INTO diameters 
                (dn_mm, material, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m, source_method)
                VALUES (?, ?, ?, ?, ?, ?)
            """, test_data)
            
            conn.commit()
            conn.close()
            
            # Tester PriceDB - doit ignorer les données invalides
            db = PriceDB(db_path)
            
            # Seule la première donnée devrait être valide
            diameters = db.get_candidate_diameters()
            assert len(diameters) == 1
            assert diameters[0]['dn_mm'] == 100
            assert diameters[0]['material'] == 'PVC-U'
            
            # Fermer explicitement la connexion
            if hasattr(db, '_conn') and db._conn:
                db._conn.close()
                db._conn = None
            
        finally:
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                pass
    
    def test_integration_performance(self):
        """Test d'intégration des performances."""
        # Test de performance avec beaucoup de données
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE diameters (
                    dn_mm INTEGER,
                    material TEXT,
                    supply_fcfa_per_m REAL,
                    pose_fcfa_per_m REAL,
                    total_fcfa_per_m REAL,
                    source_method TEXT
                )
            """)
            
            # Créer 1000 enregistrements de test
            test_data = []
            for i in range(1000):
                dn_mm = 20 + (i * 10)  # Diamètres de 20 à 10020mm
                material = ["PVC-U", "PEHD", "Fonte"][i % 3]
                price = 1000 + (i * 100)
                test_data.append((dn_mm, material, price, price * 0.2, price * 1.2, "sqlite"))
            
            cursor.executemany("""
                INSERT INTO diameters 
                (dn_mm, material, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m, source_method)
                VALUES (?, ?, ?, ?, ?, ?)
            """, test_data)
            
            conn.commit()
            conn.close()
            
            # Tester les performances
            import time
            start_time = time.time()
            
            db = PriceDB(db_path)
            
            # Test de chargement
            load_time = time.time() - start_time
            assert load_time < 1.0  # Doit charger en moins d'1 seconde
            
            # Test de recherche
            start_time = time.time()
            for _ in range(100):
                db.get_closest_diameter(500)
            search_time = time.time() - start_time
            assert search_time < 1.0  # 100 recherches en moins d'1 seconde
            
            # Vérifier les résultats
            assert len(db.get_candidate_diameters()) == 1000
            assert len(db.get_candidate_diameters("PVC-U")) > 300
            
            # Fermer explicitement la connexion
            if hasattr(db, '_conn') and db._conn:
                db._conn.close()
                db._conn = None
            
        finally:
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                pass


if __name__ == "__main__":
    # Exécuter les tests avec pytest
    pytest.main([__file__, "-v"])
