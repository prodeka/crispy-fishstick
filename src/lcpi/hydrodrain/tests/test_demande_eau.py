import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.demande_eau import estimer_demande_eau

class TestDemandeEau(unittest.TestCase):
    def test_estimation_nominale(self):
        donnees = {"population": 125000, "dotation_domestique_l_j_hab": 150}
        resultats = estimer_demande_eau(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertAlmostEqual(resultats["production_requise_m3_jour"], 23437.5, places=2) 