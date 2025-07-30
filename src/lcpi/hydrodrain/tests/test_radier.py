import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.radier import dimensionner_radier_submersible

class TestRadier(unittest.TestCase):
    def test_dimensionnement_crue(self):
        donnees = {"debit_crue_m3s": 50, "largeur_radier_m": 20, "cote_crete_radier_m": 100.0}
        resultats = dimensionner_radier_submersible(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertAlmostEqual(resultats["hauteur_eau_amont_crue_m"], 1.26, places=2) 