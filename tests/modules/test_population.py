import sys
import os
import json

# Pour permettre l'import du module depuis src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from lcpi.hydrodrain.calculs.population import prevoir_population

def test_cases():
    cases = [
        {
            'desc': 'Logistique - croissance forte (K > populations)',
            'input': {
                'methode': 'logistique',
                'annee_projet': 2050,
                'pop_annee_0': (1000, 2000),
                'pop_annee_1': (2000, 2010),
                'pop_annee_2': (4000, 2020),
            }
        },
        {
            'desc': 'Logistique - K <= max(y0, y1, y2) (erreur attendue)',
            'input': {
                'methode': 'logistique',
                'annee_projet': 2050,
                'pop_annee_0': (1000, 2000),
                'pop_annee_1': (1200, 2010),
                'pop_annee_2': (1500, 2020),
            }
        },
        {
            'desc': 'Arithmétique',
            'input': {
                'methode': 'arithmetique',
                'annee_projet': 2030,
                'pop_annee_1': (1000, 2000),
                'pop_annee_2': (1500, 2020),
            }
        },
        {
            'desc': 'Géométrique',
            'input': {
                'methode': 'geometrique',
                'annee_projet': 2030,
                'pop_annee_1': (1000, 2000),
                'pop_annee_2': (1500, 2020),
            }
        },
        {
            'desc': 'Logistique - intervalle non constant (erreur attendue)',
            'input': {
                'methode': 'logistique',
                'annee_projet': 2050,
                'pop_annee_0': (1000, 2000),
                'pop_annee_1': (2000, 2012),
                'pop_annee_2': (4000, 2020),
            }
        },
        {
            'desc': 'Méthode inconnue (erreur attendue)',
            'input': {
                'methode': 'bidon',
                'annee_projet': 2030,
                'pop_annee_1': (1000, 2000),
                'pop_annee_2': (1500, 2020),
            }
        },
    ]

    for i, case in enumerate(cases, 1):
        print(f"\n--- Cas {i}: {case['desc']} ---")
        result = prevoir_population(case['input'])
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_cases() 