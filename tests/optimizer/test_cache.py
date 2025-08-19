import time
from pathlib import Path
from src.lcpi.aep.optimizer.cache import OptimizationCache


def test_cache_persistence(tmp_path):
    """Vérifie que le cache écrit et lit correctement sur le disque."""
    cache = OptimizationCache(persist_dir=tmp_path)
    
    network_model = {"nodes": {"N1": {"elevation": 0}}}
    h_tanks = {"T1": 50.0}
    diameters = {"P1": 100}
    result = {"min_pressure_m": 15.0}

    # 1. Écrire dans le cache
    cache.set(network_model, h_tanks, diameters, result)

    # Vérifier que le fichier a été créé
    cache_key = cache._key(network_model, h_tanks, diameters)
    cache_file = tmp_path / f"{cache_key}.json"
    assert cache_file.exists()

    # 2. Lire depuis un nouvel objet cache pour forcer la lecture disque
    cache2 = OptimizationCache(persist_dir=tmp_path)
    retrieved_result = cache2.get(network_model, h_tanks, diameters)

    assert retrieved_result is not None
    assert retrieved_result["min_pressure_m"] == 15.0

def test_cache_multi_tank_key():
    """Vérifie que la clé de cache est différente pour des hauteurs différentes."""
    cache = OptimizationCache()
    network_model = {"nodes": {}}
    diameters = {}

    h_tanks1 = {"T1": 50.0, "T2": 70.0}
    h_tanks2 = {"T1": 50.1, "T2": 70.0} # Hauteur légèrement différente
    h_tanks3 = {"T2": 70.0, "T1": 50.0} # Ordre différent

    key1 = cache._key(network_model, h_tanks1, diameters)
    key2 = cache._key(network_model, h_tanks2, diameters)
    key3 = cache._key(network_model, h_tanks3, diameters)

    assert key1 != key2
    # Le tri des clés dans le JSON stable doit garantir que l'ordre n'importe pas
    assert key1 == key3

def test_cache_expiration(tmp_path):
    """Vérifie que le cache expire après le TTL."""
    cache = OptimizationCache(persist_dir=tmp_path, ttl_s=1) # TTL de 1 seconde
    
    network_model = {"nodes": {}}
    h_tanks = {"T1": 50.0}
    diameters = {}
    result = {"data": "some_data"}

    cache.set(network_model, h_tanks, diameters, result)
    
    # Doit être lisible immédiatement
    assert cache.get(network_model, h_tanks, diameters) is not None

    time.sleep(1.5)

    # Doit être expiré maintenant
    assert cache.get(network_model, h_tanks, diameters) is None
