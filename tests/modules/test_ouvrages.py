import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from lcpi.hydrodrain.calculs.canal import dimensionner_canal
from lcpi.hydrodrain.calculs.dalot import verifier_dalot
from lcpi.hydrodrain.calculs.deversoir import dimensionner_deversoir

def test_dimensionner_canal():
    donnees = {
        'debit_projet_m3s': 10.0,
        'pente_m_m': 0.001,
        'k_strickler': 30.0,
        'fruit_talus_m_m': 1.5,
        'vitesse_imposee_ms': 1.2
    }
    result = dimensionner_canal(donnees)
    print("dimensionner_canal:", json.dumps(result, indent=2, ensure_ascii=False))

def test_verifier_dalot():
    donnees = {
        'largeur_m': 2.5,
        'hauteur_m': 2.0,
        'nombre_cellules': 2,
        'longueur_m': 18.0,
        'pente_m_m': 0.005,
        'debit_projet_m3s': 35.0,
        'manning': 0.013
    }
    result = verifier_dalot(donnees)
    print("verifier_dalot:", json.dumps(result, indent=2, ensure_ascii=False))

def test_dimensionner_deversoir():
    donnees = {
        'debit_projet_m3s': 600,
        'cote_crete_barrage_m': 150.0,
        'revanche_m': 1.0,
        'cote_crete_deversoir_m': 148.0,
        'profil_crete': 'creager'
    }
    result = dimensionner_deversoir(donnees)
    print("dimensionner_deversoir:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_dimensionner_canal()
    test_verifier_dalot()
    test_dimensionner_deversoir() 