import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.lcpi.hydrodrain.calculs.population import prevoir_population

class TestPopulation(unittest.TestCase):
    def test_prevision_arithmetique(self):
        donnees = {"pop_annee_1": (50000, 2010), "pop_annee_2": (85000, 2020), "annee_projet": 2030, "methode": "arithmetique"}
        resultats = prevoir_population(donnees)
        self.assertEqual(resultats["statut"], "OK")
        self.assertEqual(resultats["population_estimee"], 120000) 