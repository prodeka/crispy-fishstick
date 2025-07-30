import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.pompage import predimensionner_pompe

class TestPompage(unittest.TestCase):
    def test_predimensionnement_nominal(self):
        donnees = {"debit_pompage_m3s": 0.1, "cote_refoulement_m": 50.0, "cote_arret_pompe_m": 20.0, "longueur_conduite_m": 500, "diametre_conduite_m": 0.2}
        resultats = predimensionner_pompe(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertAlmostEqual(resultats["point_fonctionnement"]["hmt_m"], 55.82, places=2) 