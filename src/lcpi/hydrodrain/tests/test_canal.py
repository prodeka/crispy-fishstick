import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.canal import dimensionner_canal

class TestCanal(unittest.TestCase):
    def test_dimensionnement_nominal(self):
        donnees = {"debit_projet_m3s": 10.0, "pente_m_m": 0.001, "k_strickler": 30, "fruit_talus_m_m": 1.5, "vitesse_imposee_ms": 1.2}
        resultats = dimensionner_canal(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertAlmostEqual(resultats["hauteur_eau_h_m"], 1.989, places=3) 