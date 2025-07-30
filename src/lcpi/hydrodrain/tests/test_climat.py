import unittest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.climat import generer_diagramme_ombrothermique

class TestClimat(unittest.TestCase):
    def test_generation_diagramme(self):
        donnees_lomé = {
            "station": "Test", "donnees_mensuelles": [
                {"mois": "Jan", "temp_C": 27, "precip_mm": 20}, {"mois": "Juil", "temp_C": 25, "precip_mm": 105}
            ]
        }
        output_file = "test_diagram.png"
        resultats = generer_diagramme_ombrothermique(donnees_lomé, output_file)
        self.assertEqual(resultats["statut"], "OK")
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file) # Nettoie le fichier de test 