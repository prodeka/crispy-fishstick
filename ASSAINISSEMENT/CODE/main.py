# main.py
import pandas as pd
import os
import sys
import logging
import json
import getpass

# Imports des modules du projet
from utils.ui import check_and_install_packages, print_colored, initialize_colors, get_input_with_default, get_menu_choice
from utils.security import authenticate, display_disclaimer_and_get_agreement
from utils.logging_config import setup_logging
from core.engine import run_dimensioning_workflow
from core.models import Reseau
from config.idf_models import DEFAULT_IDF_DATA
from plotting import generer_graphiques
from reporting import creer_rapport_pdf

# --- Constantes ---
USER_PLUVIO_FILE = os.path.join('config', 'pluviometrie_user.json')
PLUVIO_PASSWORD = "pluvio2024"
SUPPORTED_FORMULAS = {'1': 'montana', '2': 'talbot', '3': 'kiefer-chu'}

# --- Fonctions de gestion des données de pluie (IDF) ---

def load_idf_data(include_default=True):
    """Charge les données IDF (celles des sources et celles de l'utilisateur)."""
    params = DEFAULT_IDF_DATA.copy() if include_default else {}
    if os.path.exists(USER_PLUVIO_FILE):
        try:
            with open(USER_PLUVIO_FILE, 'r', encoding='utf-8') as f:
                user_params = json.load(f)
                params.update(user_params)
        except (json.JSONDecodeError, IOError):
            print_colored(f"Attention: Le fichier '{USER_PLUVIO_FILE}' est corrompu.", "red")
    return params

def save_user_idf_data(data):
    """Sauvegarde les données IDF de l'utilisateur dans le fichier JSON."""
    os.makedirs('config', exist_ok=True)
    with open(USER_PLUVIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def _get_params_for_formula(formula_name):
    """Demande à l'utilisateur les paramètres spécifiques à une formule IDF."""
    params = {}
    if formula_name == 'montana':
        params['a'] = get_input_with_default("      Coefficient 'a'", 100.0, float)
        if params['a'] is None: return None
        params['b'] = get_input_with_default("      Coefficient 'b' (doit être négatif)", -0.5, float)
        if params['b'] is None: return None
    elif formula_name == 'talbot':
        params['a'] = get_input_with_default("      Coefficient 'a'", 70.0, float)
        if params['a'] is None: return None
        params['b'] = get_input_with_default("      Coefficient 'b'", 15.0, float)
        if params['b'] is None: return None
    elif formula_name == 'kiefer-chu':
        params['a'] = get_input_with_default("      Coefficient 'a'", 700.0, float)
        if params['a'] is None: return None
        params['b'] = get_input_with_default("      Coefficient 'b'", 30.0, float)
        if params['b'] is None: return None
        params['c'] = get_input_with_default("      Coefficient 'c'", 1.2, float)
        if params['c'] is None: return None
    
    if any(p is None for p in params.values()): return None
    return params

def _handle_add_location(user_data):
    """Gère la logique d'ajout d'une nouvelle localité et de ses paramètres IDF."""
    while True:
        location = input("\nEntrez le nom de la nouvelle localité (ex: 'Cotonou - Benin') ou '<' pour retour : ").strip()
        if location == '<': break
        if not location: continue

        formula_choice = get_menu_choice("\nChoisissez la formule IDF pour cette localité :", SUPPORTED_FORMULAS)
        if formula_choice is None: continue
        formula_name = SUPPORTED_FORMULAS[formula_choice]
        
        location_data = {"formula": formula_name, "parameters": {}}
        
        while True:
            t = get_input_with_default(f"   Période de retour (T en années) pour '{location}' (ou 'fin' pour valider)", 'fin', str)
            if t is None or t.lower() == 'fin': break

            params = _get_params_for_formula(formula_name)
            if params is None: continue
            
            params['nom'] = f'Pluie T={t} ans'
            location_data["parameters"][t] = params
        
        if location_data["parameters"]:
            user_data[location] = location_data
            save_user_idf_data(user_data)
            print_colored(f"Données pour '{location}' sauvegardées avec succès.", "green")

def run_manage_idf_mode():
    """Menu principal pour la gestion des données de pluie."""
    print_colored("\n--- Mode Gestionnaire de Pluviométrie ---", "cyan", bold=True)
    if getpass.getpass("Veuillez entrer le mot de passe administrateur : ") != PLUVIO_PASSWORD:
        print_colored("Mot de passe incorrect.", "red"); return
    
    print_colored("Accès autorisé.", "green")
    
    # NOTE: Pour garder le code gérable, seule l'ajout est implémenté ici.
    # La logique de modification/suppression suivrait un schéma similaire.
    print_colored("\nSeul l'ajout de nouvelles données est disponible dans cette version.", "yellow")
    user_data = load_idf_data(include_default=False)
    _handle_add_location(user_data)
    input("\nAppuyez sur Entrée pour retourner au menu principal...")

# --- Fonctions de workflow de dimensionnement ---

def get_validation_params():
    """Gère la saisie des critères de vitesse pour la validation."""
    print_colored("\n--- Paramètres de Validation du Projet ---", "bold")
    v_min_prompt = "   Vitesse minimale (auto-curage pour éviter les dépôts) [m/s]"
    v_min = get_input_with_default(v_min_prompt, 0.6)
    if v_min is None: return None

    v_max_prompt = "   Vitesse maximale (pour éviter l'érosion des canaux) [m/s]"
    v_max = get_input_with_default(v_max_prompt, 2.0)
    if v_max is None: return None
    
    return {'v_min': v_min, 'v_max': v_max}

def get_idf_params():
    """Gère le menu de sélection des modèles et paramètres IDF."""
    all_idf_data = load_idf_data()
    if not all_idf_data:
        print_colored("Aucune donnée de pluviométrie n'est disponible.", "red")
        return None

    while True:
        locations_map = {str(i+1): loc for i, loc in enumerate(sorted(all_idf_data.keys()))}
        choix_loc_key = get_menu_choice("\nChoisissez un jeu de données pluviométriques :", locations_map)
        if choix_loc_key is None: return None

        selected_location_name = locations_map[choix_loc_key]
        params_locaux = all_idf_data[selected_location_name]
        
        formula_name = params_locaux.get("formula", "montana")
        print_colored(f"   Modèle sélectionné : {formula_name.capitalize()}", "cyan")
        
        # ***** CETTE SECTION CONSTRUIT LE MENU DÉTAILLÉ QUE VOUS SOUHAITEZ *****
        # Elle parcourt les paramètres et les formate pour un affichage clair.
        options_locales = {}
        for t, params in params_locaux["parameters"].items():
            # Crée une chaîne comme "a=100, b=-0.5"
            param_str = ", ".join([f"{k}={v}" for k, v in params.items() if k != 'nom'])
            # Crée l'entrée de menu complète
            options_locales[t] = f"{params['nom']} ({param_str})"
            
        choix_t_key = get_menu_choice("Choisissez une période de retour :", options_locales)
        if choix_t_key is None: continue
        
        final_params = {
            'formula': formula_name, 'periode_retour': int(choix_t_key),
            **params_locaux["parameters"][choix_t_key]
        }
        print_colored(f"Jeu de données pour T={choix_t_key} ans sélectionné.", "green")
        return final_params

def run_batch_mode(idf_params: dict, validation_params: dict):
    """Lance le dimensionnement pour un réseau complet depuis un fichier CSV."""
    print_colored("\n--- MODE BATCH - TRAITEMENT D'UN FICHIER CSV DE RÉSEAU ---", "cyan", bold=True)
    
    csv_path, methode_calcul, tc_formule_name = "", "", "kirpich"
    
    while True:
        csv_path_input = input(f"Entrez le chemin du fichier CSV (utilisez '/') (ou '<' pour retour) : ").strip()
        if csv_path_input == '<': return
        if os.path.exists(csv_path_input):
            csv_path = csv_path_input
            break
        else:
            print_colored("Fichier non trouvé. Vérifiez le chemin et réessayez.", "red")

    methode_calcul_map = {'1': 'Rationnelle', '2': 'Caquot'}
    choix_methode_key = get_menu_choice("\nChoisissez la méthode de calcul pour le lot :", methode_calcul_map)
    if choix_methode_key is None: return
    methode_calcul = methode_calcul_map[choix_methode_key].lower()
    
    if methode_calcul == 'rationnelle':
        tc_formule_map = {'1': 'Kirpich', '2': 'Californienne'}
        choix_tc_key = get_menu_choice("Choisissez la formule de tc de surface :", tc_formule_map)
        if choix_tc_key is None: return
        tc_formule_name = tc_formule_map[choix_tc_key].lower()
    
    try:
        df_input = pd.read_csv(csv_path, dtype={'id_troncon': str, 'troncon_amont': str})
        required_cols = {'id_troncon','type_section', 'surface_ha', 'coeff_ruissellement', 'longueur_troncon_m', 'pente_troncon'}
        if not required_cols.issubset(df_input.columns):
            raise ValueError(f"CSV doit contenir au moins : {required_cols - set(df_input.columns)}")
        
        project_info = {
            'nom_projet': os.path.basename(csv_path), 'methode_calcul': methode_calcul,
            'tc_formule_name': tc_formule_name, 'idf_formula': idf_params.get('formula', 'N/A'),
            **validation_params, **idf_params
        }
        
        reseau = Reseau(df_input)
        reseau_calcule, verbose_log = run_dimensioning_workflow(reseau, methode_calcul, tc_formule_name, idf_params, validation_params['v_min'], validation_params['v_max'])
        df_results = pd.DataFrame([t.to_dict() for t in reseau_calcule.troncons.values()])

        print_colored("\n================ TABLEAU DE RÉSULTATS ================", "cyan", bold=True)
        if df_results.empty: 
            print("Aucun tronçon n'a été traité.")
        else:
            pd.set_option('display.width', 130); print(df_results.to_string(index=False))
            generer_graphiques(df_results, df_input)
            creer_rapport_pdf(df_results, project_info, verbose_log)
        
        repports_dir = 'repports'
        os.makedirs(repports_dir, exist_ok=True)
        nom_fichier_csv = os.path.join(repports_dir, f"resultats_{project_info['nom_projet'].replace('.csv', '.csv')}")
        df_results.to_csv(nom_fichier_csv, index=False, sep=';', decimal='.')
        print_colored(f"\nRésultats également exportés vers '{nom_fichier_csv}'", "green", bold=True)

    except Exception as e:
        logging.error(f"Erreur critique: {e}", exc_info=True)
        print_colored(f"\nERREUR CRITIQUE : {e}", "red", bold=True)

# --- Point d'Entrée Principal ---
def main():
    """Le chef d'orchestre principal du programme."""
    check_and_install_packages(['pandas', 'matplotlib', 'colorama', 'reportlab'])
    initialize_colors(); setup_logging()
    
    copyright_header = """
# ==============================================================================
# Outil de Dimensionnement de Réseau d'Assainissement Pluvial
# Copyright (c) 2024 TABE DJATO Serge / intrepidcore
# Auteur : TABE DJATO Serge - Dépôt GitHub : https://github.com/prodeka
# ==============================================================================
    """
    print_colored(copyright_header, "cyan", bold=True)
    
    if not display_disclaimer_and_get_agreement(): sys.exit()
    if not authenticate(): sys.exit()

    while True:
        print_colored("\n BIENVENUE DANS LA PLATEFORME DE CALCUL D'INGÉNIERIE", "cyan", bold=True)
        main_menu_options = {'1': 'Lancer un dimensionnement', '2': 'Gérer les données de pluie', '0': 'Quitter'}
        choix_app = get_menu_choice("\nChoisissez une action :", main_menu_options)

        if choix_app == '0' or choix_app is None: break
        
        if choix_app == '2':
            run_manage_idf_mode()
            continue

        if choix_app == '1':
            while True:
                validation_params = get_validation_params()
                if validation_params is None: break

                idf_params = get_idf_params()
                if idf_params is None: continue

                mode_menu_options = {'1': 'Par Lot (Batch)', '2': 'Interactif (Simplifié)'}
                choix_mode_key = get_menu_choice("\nChoisissez un mode de fonctionnement :", mode_menu_options)
                if choix_mode_key is None: continue
                
                if choix_mode_key == '1':
                    run_batch_mode(idf_params, validation_params)
                elif choix_mode_key == '2':
                    print_colored("Mode interactif non disponible dans cette version.", "yellow")
                
                print_colored("\nOpération de dimensionnement terminée.", "cyan")
                break
    
    print_colored("\nMerci d'avoir utilisé le programme. À bientôt !", "green")
    
if __name__ == "__main__":
    main()