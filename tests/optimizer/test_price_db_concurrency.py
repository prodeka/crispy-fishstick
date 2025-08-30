import pytest
from threading import Thread
import time

# Assurez-vous que le chemin est correct pour votre structure de projet
from src.lcpi.aep.optimizer.db import PriceDB

@pytest.mark.slow
def test_concurrent_reads_on_single_price_db_instance():
    """
    Vérifie que plusieurs threads peuvent lire depuis LA MÊME instance de PriceDB
    sans provoquer d'erreurs (race conditions). C'est le cas d'usage le plus courant.
    """
    # L'instance est créée une seule fois
    db_instance = PriceDB()
    num_threads = 50
    errors = []

    def read_task():
        try:
            for _ in range(10):
                all_diams = db_instance.get_candidate_diameters()
                pvc_diams = db_instance.get_candidate_diameters("PVC")
                closest = db_instance.get_closest_diameter(115)
                price = db_instance.get_price_for_length(110, 50)
                
                assert all_diams is not None
                assert pvc_diams is not None
                assert closest is not None
                assert price is not None
                time.sleep(0.01) # Petite pause pour encourager le changement de contexte des threads
        except Exception as e:
            errors.append(e)

    threads = [Thread(target=read_task) for _ in range(num_threads)]
    
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()

    assert not errors, f"Des erreurs de concurrence ont été détectées : {errors}"
