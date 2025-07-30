import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.deversoir import dimensionner_deversoir

class TestDeversoir(unittest.TestCase):
    def test_dimensionnement_nominal(self):
        donnees = {"debit_projet_m3s": 800, "cote_crete_barrage_m": 212.5, "revanche_m": 1.2, "cote_crete_deversoir_m": 210.0, "profil_crete": "creager"}
        resultats = dimensionner_deversoir(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertAlmostEqual(resultats["longueur_crete_calculee_m"], 248.67, places=2) 