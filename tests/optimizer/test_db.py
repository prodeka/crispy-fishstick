import yaml
from pathlib import Path
from src.lcpi.aep.optimizer.db import get_candidate_diameters

# Utiliser le dossier de test pour créer des fichiers temporaires
TEST_DIR = Path(__file__).parent

def test_get_diameters_from_yaml(tmp_path):
    """Vérifie la lecture des diamètres depuis un fichier YAML."""
    dummy_db_path = tmp_path / "dummy_diameters.yml"
    dummy_data = [
        {"d_mm": 100, "cost_per_m": 15.0, "material": "PVC"},
        {"d_mm": 50, "cost_per_m": 5.0, "material": "PEHD"},
    ]
    dummy_db_path.write_text(yaml.dump(dummy_data), encoding="utf-8")

    candidates = get_candidate_diameters(str(dummy_db_path))
    
    assert len(candidates) == 2
    # Le DAO doit trier par diamètre
    assert candidates[0]["d_mm"] == 50
    assert candidates[1]["d_mm"] == 100
    assert candidates[1]["material"] == "PVC"

def test_get_diameters_fallback():
    """Vérifie que le fallback est utilisé si aucun chemin n'est fourni."""
    candidates = get_candidate_diameters(db_path=None)
    
    assert len(candidates) > 0
    # Vérifier un des diamètres par défaut
    assert any(d["d_mm"] == 110 and d["material"] == "PEHD" for d in candidates)

def test_get_diameters_bad_path():
    """Vérifie que le fallback est utilisé si le chemin est invalide."""
    candidates = get_candidate_diameters(db_path="non_existent_file.yml")
    
    assert len(candidates) > 0
    assert any(d["d_mm"] == 110 for d in candidates)
