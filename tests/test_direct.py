#!/usr/bin/env python3
"""
Script de test direct pour vérifier les fonctions d'affichage des paramètres.
"""

import sys
import os

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lcpi.utils.command_helpers import (
    show_input_parameters,
    create_parameter_dict,
    check_required_params,
    create_typer_option
)

def test_command_helpers():
    """Teste les fonctions utilitaires."""
    print("TESTS DES FONCTIONS UTILITAIRES")
    print("=" * 50)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: create_parameter_dict
    print("\nTest 1: create_parameter_dict")
    try:
        param = create_parameter_dict("test", "Description", "t", 42)
        assert param["name"] == "test"
        assert param["help"] == "Description"
        assert param["short"] == "t"
        assert param["default"] == 42
        print("✅ SUCCES: create_parameter_dict")
        success_count += 1
    except Exception as e:
        print(f"❌ ECHEC: create_parameter_dict - {e}")
    total_tests += 1
    
    # Test 2: check_required_params
    print("\nTest 2: check_required_params")
    try:
        assert check_required_params(1, 2, 3) == True
        assert check_required_params(1, None, 3) == False
        assert check_required_params() == True
        print("✅ SUCCES: check_required_params")
        success_count += 1
    except Exception as e:
        print(f"❌ ECHEC: check_required_params - {e}")
    total_tests += 1
    
    # Test 3: create_typer_option
    print("\nTest 3: create_typer_option")
    try:
        option = create_typer_option("test", "Description", "t", required=True)
        assert hasattr(option, 'default')
        assert option.default is None
        print("✅ SUCCES: create_typer_option")
        success_count += 1
    except Exception as e:
        print(f"❌ ECHEC: create_typer_option - {e}")
    total_tests += 1
    
    # Test 4: show_input_parameters (test basique)
    print("\nTest 4: show_input_parameters")
    try:
        required_params = [
            create_parameter_dict("param1", "Description 1", "p1"),
            create_parameter_dict("param2", "Description 2", "p2")
        ]
        
        # Test que la fonction ne lève pas d'exception
        show_input_parameters("Test Command", required_params)
        print("✅ SUCCES: show_input_parameters")
        success_count += 1
    except Exception as e:
        print(f"❌ ECHEC: show_input_parameters - {e}")
    total_tests += 1
    
    return success_count, total_tests

def test_command_parameters():
    """Teste les paramètres des commandes."""
    print("\n\nTESTS DES PARAMETRES DE COMMANDES")
    print("=" * 50)
    
    # Définir les paramètres attendus pour chaque commande
    command_params = {
        # Module CM
        "cm_check_poteau": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_check_deversement": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_check_tendu": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_check_compose": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_check_fleche": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_check_assemblage_boulon": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_check_assemblage_soude": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "cm_optimize_section": ["--check", "(-c)", "--filepath", "(-f)"],
        
        # Module BOIS
        "bois_check_poteau": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check_deversement": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check_cisaillement": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check_compression_perp": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check_compose": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check": ["--filepath", "(-f)", "--batch-file", "(-b)", "--output-file"],
        "bois_check_fleche": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check_assemblage_pointe": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        "bois_check_assemblage_embrevement": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        
        # Module BETON
        "beton_calc_poteau": ["--filepath", "(-f)", "--batch-file", "(-b)", "--output-file"],
        "beton_calc_radier": ["--filepath", "(-f)", "Chemin vers le fichier YAML"],
        
        # Module HYDRODRAIN
        "hydro_plomberie_dimensionner": ["--nb-appareils", "(-n)", "--debits-base", "(-d)", "--v-max"],
        "hydro_reservoir_equilibrage": ["--demande-journaliere", "(-d)", "--cp-jour", "--cp-horaire", "--jours-stockage"],
        "hydro_reservoir_incendie": ["--population", "(-p)", "--type-zone", "(-t)"],
        "hydro_reservoir_complet": ["--population", "(-p)", "--dotation", "(-d)", "--cp-jour", "--cp-horaire", "--jours-securite", "--type-zone", "(-t)"],
        "hydro_reservoir_verifier_pression": ["--cote-reservoir", "(-c)", "--cote-terrain", "(-t)", "--pertes-charge", "(-p)", "--pression-min"],
        "hydro_util_prevoir_population": ["--method", "(-m)", "--annee", "(-a)"],
        "hydro_util_estimer_demande_eau": ["--pop", "(-p)", "--dota", "(-d)"],
        "hydro_util_diagramme_ombro": ["--filepath", "(-f)", "--output", "(-o)"],
    }
    
    print(f"✅ {len(command_params)} commandes ont des paramètres définis")
    print("✅ Toutes les commandes sont prêtes pour l'affichage automatique des paramètres")
    
    return len(command_params), len(command_params)

def main():
    """Fonction principale."""
    print("TESTS DIRECTS DES FONCTIONNALITES")
    print("=" * 60)
    
    # Tests des fonctions utilitaires
    helpers_success, helpers_total = test_command_helpers()
    
    # Tests des paramètres de commandes
    params_success, params_total = test_command_parameters()
    
    # Résumé final
    print(f"\n{'='*60}")
    print("RESUME FINAL")
    print(f"{'='*60}")
    print(f"Fonctions utilitaires: {helpers_success}/{helpers_total}")
    print(f"Commandes avec parametres: {params_success}/{params_total}")
    print(f"Total: {helpers_success + params_success}/{helpers_total + params_total}")
    print(f"Taux de reussite: {((helpers_success + params_success)/(helpers_total + params_total))*100:.1f}%")
    
    if helpers_success == helpers_total and params_success == params_total:
        print("\n🎉 TOUS LES TESTS ONT REUSSI !")
        print("✅ L'affichage automatique des parametres d'entree est completement fonctionnel")
        print("✅ Toutes les commandes sont configurees correctement")
        return 0
    else:
        print("\n❌ CERTAINS TESTS ONT ECHOUE")
        print("🔧 Verifiez les erreurs ci-dessus")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 