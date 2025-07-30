import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from lcpi.hydrodrain.calculs.bassin_versant import caracteriser_bassin

def test_caracteriser_bassin():
    donnees = {
        'superficie_km2': 50.0,
        'perimetre_km': 35.0,
        'pente_globale_m_km': 12.0
    }
    result = caracteriser_bassin(donnees)
    print("caracteriser_bassin:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_caracteriser_bassin() 