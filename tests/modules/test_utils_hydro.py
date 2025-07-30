import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from lcpi.hydrodrain.utils import utils
from lcpi.hydrodrain.calculs.demande_eau import estimer_demande_eau

def test_initialize_colors():
    utils.initialize_colors()
    print("initialize_colors: OK (pas d'erreur)")

def test_check_and_install_packages():
    # Simulation : on ne va pas vraiment installer, juste vérifier l'appel
    utils.check_and_install_packages(["typer", "yaml"])
    print("check_and_install_packages: OK (simulation)")

def test_print_colored():
    utils.print_colored("Texte jaune", color_name="yellow", bold=True)
    utils.print_colored("Texte vert", color_name="green")
    print("print_colored: OK (affichage console)")

def test_setup_logging():
    utils.setup_logging()
    import logging
    logging.info("Test log info")
    print("setup_logging: OK (voir dimensionnement.log)")

def test_estimer_demande_eau():
    donnees = {
        "population": 10000,
        "dotation_domestique_l_j_hab": 80,
        "besoins_publics_m3_j": 50,
        "rendement_reseau": 0.85
    }
    result = estimer_demande_eau(donnees)
    print("estimer_demande_eau:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_initialize_colors()
    test_check_and_install_packages()
    test_print_colored()
    test_setup_logging()
    test_estimer_demande_eau() 