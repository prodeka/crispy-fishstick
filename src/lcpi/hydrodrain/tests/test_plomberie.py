import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.plomberie import dimensionner_troncon_plomberie

class TestPlomberie(unittest.TestCase):
    def test_troncon_appartement(self):
        donnees = {"nombre_appareils": 5, "somme_debits_base_ls": 0.75}
        resultats = dimensionner_troncon_plomberie(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertEqual(resultats["diametre_normalise_choisi_mm"], 16.0) 