import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from lcpi.hydrodrain.calculs.pompage import predimensionner_pompe

def test_predimensionner_pompe():
    donnees = {
        'debit_pompage_m3s': 0.1,
        'cote_refoulement_m': 120.0,
        'cote_arret_pompe_m': 100.0,
        'longueur_conduite_m': 500.0,
        'diametre_conduite_m': 0.3,
        'pertes_singulieres_k': [0.5, 1.2],
        'rugosite_mm': 0.1
    }
    result = predimensionner_pompe(donnees)
    print("predimensionner_pompe:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_predimensionner_pompe() 