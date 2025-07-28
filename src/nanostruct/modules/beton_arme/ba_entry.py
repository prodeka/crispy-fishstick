# PROJET_DIMENTIONEMENT/BA/ba_entry.py
# Version "Expert" finale, refactorisée, complète et avec toutes les fonctionnalités intégrées.

# --- Imports ---
import pandas as pd
import math
from nanostruct.utils import settings
from nanostruct.utils.ui_helpers import get_user_input, v_print
from nanostruct.modules.beton_arme.core.materials import Beton, Acier
from nanostruct.modules.beton_arme.core.sections import SectionRectangulaire
from nanostruct.modules.beton_arme.core.design.column_design import design_rectangular_column, design_column_compression_bael
from nanostruct.modules.beton_arme.core.rebar_selector import get_rebar_proposals
from nanostruct.modules.beton_arme.reports.plotting import plot_column_section
from nanostruct.modules.beton_arme.core.analysis.continuous_beam import analyze_by_forfaitaire
from nanostruct.modules.beton_arme.core.analysis.moment_calculator import calculate_beam_end_moment
from nanostruct.modules.beton_arme.core.checks.service_limit_states import check_soil_bearing_pressure, check_concrete_compression_stress

# ==============================================================================
# SECTION 1 : FONCTIONS DE SAISIE UTILISATEUR
# ==============================================================================

def define_materials():
    """Interface utilisateur pour définir les matériaux (Béton et Acier)."""
    print("\n" + "="*50); print("=== ÉTAPE 1: DÉFINITION DES MATÉRIAUX ==="); print("="*50)
    print("\n--- 1.1. Choix du Béton ---"); print("[1] C25/30 (Courant)"); print("[2] C30/37"); print("[3] Personnalisé")
    beton_choice = get_user_input("Votre choix pour le béton", 1, int)
    if beton_choice == 1: fc28 = 25.0
    elif beton_choice == 2: fc28 = 30.0
    else: fc28 = get_user_input("Résistance fc28 (MPa)", 25.0)
    gamma_b = get_user_input("Coeff. sécurité béton γb", 1.5); beton = Beton(fc28=fc28, gamma_b=gamma_b); print(f"-> Béton défini : {beton}")
    
    print("\n--- 1.2. Choix de l'Acier ---"); print("[1] S500 (Courant)"); print("[2] S400"); print("[3] Personnalisé")
    acier_choice = get_user_input("Votre choix pour l'acier", 1, int)
    if acier_choice == 1: fe = 500.0
    elif acier_choice == 2: fe = 400.0
    else: fe = get_user_input("Limite élastique fe (MPa)", 500.0)
    gamma_s = get_user_input("Coeff. sécurité acier γs", 1.15); acier = Acier(fe=fe, gamma_s=gamma_s); print(f"-> Acier défini : {acier}")
    return beton, acier

def get_column_moment_from_user():
    """Menu interactif pour aider l'utilisateur à déterminer Mu pour un poteau."""
    print("\n" + "-"*40); print("--- Détermination du Moment Ultime Mu ---"); print("Choisissez le cas de figure :"); print("[1] Poteau de Rive"); print("[2] Poteau Intermédiaire"); print("[3] Charge Excentrée"); print("[4] Entrée manuelle")
    case_choice = get_user_input("Votre choix", 4, int)
    if case_choice == 1: print("\n--- Cas 1 : Poteau de Rive ---"); q = get_user_input("Charge q (kN/m)", 25.0); L = get_user_input("Portée L (m)", 5.0); return calculate_beam_end_moment(q, L, is_end_span=True)
    elif case_choice == 2: print("\n--- Cas 2 : Poteau Intermédiaire ---"); print("Poutre de GAUCHE :"); q_gauche = get_user_input("Charge q (kN/m)", 25.0); L_gauche = get_user_input("Portée L (m)", 5.0); M_gauche = calculate_beam_end_moment(q_gauche, L_gauche, is_end_span=False); print("\nPoutre de DROITE :"); q_droite = get_user_input("Charge q (kN/m)", 22.0); L_droite = get_user_input("Portée L (m)", 4.5); M_droite = calculate_beam_end_moment(q_droite, L_droite, is_end_span=False); Mu = abs(M_gauche - M_droite); v_print("Moment de continuité final", "Mu = |Mg - Md|", f"|{M_gauche:.4f} - {M_droite:.4f}|", Mu, "MN.m"); return Mu
    elif case_choice == 3: print("\n--- Cas 3 : Charge Excentrée ---"); Nu_load = get_user_input("Charge ponctuelle Nu (MN)", 0.1); e = get_user_input("Excentricité e (m)", 0.15); Mu = Nu_load * e; v_print("Moment d'excentricité", "Mu = Nu * e", f"{Nu_load:.2f} * {e:.2f}", Mu, "MN.m"); return Mu
    else: return get_user_input("Entrez la valeur de Mu (MN.m)", 0.05)

def get_radier_inputs():
    """Fonction interactive et pédagogique pour collecter les données du radier."""
    print("\n" + "-"*50); print("--- Étape 1 : Données d'Entrée et Prédimensionnement ---"); print("-" * 50); print("Concept : On détermine d'abord les charges totales et les dimensions globales du radier.")
    print("Comment souhaitez-vous définir les charges des poteaux ?"); print("[1] Par charges brutes (G et Q)"); print("[2] Par sollicitations (Nser et Nu)")
    input_type = get_user_input("Votre choix", 1, int)
    poteaux = []; num_poteaux = get_user_input("\nCombien de poteaux reposent sur le radier ?", 4, int)
    if num_poteaux <= 0: print("Nombre de poteaux invalide. Opération annulée."); return None
    print("\nEntrez les données pour chaque poteau :");
    for i in range(num_poteaux):
        print(f"\n--- Poteau n°{i+1} ---"); p_id = input(f"ID du poteau (ex: P1) [défaut: P{i+1}]: ") or f"P{i+1}"
        if input_type == 1:
            charge_g = get_user_input(f"  Charge permanente G (Tonnes)", 50.0); charge_q = get_user_input(f"  Charge d'exploitation Q (Tonnes)", 20.0)
            p_ser_kn = (charge_g + charge_q) * 9.81; p_u_kn = (1.35 * charge_g + 1.5 * charge_q) * 9.81
        else:
            p_ser_kn = get_user_input(f"  Sollicitation de service N_ser (kN)", 686.7); p_u_kn = get_user_input(f"  Sollicitation ultime N_u (kN)", 971.4)
        poteaux.append({'ID': p_id, 'P_ser_kN': p_ser_kn, 'P_u_kN': p_u_kn})
    df_poteaux = pd.DataFrame(poteaux)
    print("\n" + "-"*30); print("Calcul des charges totales :"); print("-" * 30); total_p_ser_kN = df_poteaux['P_ser_kN'].sum(); total_p_u_kN = df_poteaux['P_u_kN'].sum()
    v_print("Charge de service totale", "ΣP_ser", f"{total_p_ser_kN/9.81:.1f} T", total_p_ser_kN, "kN"); v_print("Charge ultime totale", "ΣP_u", f"{total_p_u_kN/9.81:.1f} T", total_p_u_kN, "kN")
    print("\n" + "-"*30); print("Dimensions du radier en plan :"); print("-" * 30); sigma_sol_adm = get_user_input("Contrainte admissible du sol σ_sol,adm (kPa)", 150.0)
    surface_requise = total_p_ser_kN / sigma_sol_adm; v_print("Surface minimale requise", "S_req = ΣP_ser / σ_sol,adm", f"{total_p_ser_kN:.1f} / {sigma_sol_adm:.1f}", surface_requise, "m²")
    dim_A = get_user_input("Dimension A du radier (m)", round(math.sqrt(surface_requise), 1)); dim_B = get_user_input("Dimension B du radier (m)", round(surface_requise / dim_A, 1) if dim_A > 0 else 0)
    print("\n" + "-"*30); print("Épaisseur du radier :"); print("-" * 30); portee_max = get_user_input("Plus grande portée entre poteaux L_max (m) ?", 6.0); h_estime = portee_max / 10; v_print("Épaisseur estimée", "h ≈ L_max / 10", f"{portee_max:.1f} / 10", h_estime, "m"); h_radier = get_user_input("Choisissez l'épaisseur finale h du radier (m)", math.ceil(h_estime * 20) / 20)
    d_radier = h_radier - 0.07; print(f"\n" + "="*50); print("--- RÉCAPITULATIF DU PRÉDIMENSIONNEMENT ---"); print("="*50); print(f"  - Dimensions : {dim_A:.2f}m x {dim_B:.2f}m (Surface = {dim_A * dim_B:.2f} m²)"); print(f"  - Épaisseur : {h_radier:.2f}m (Hauteur utile d ≈ {d_radier:.2f}m)")
    return {"poteaux_df": df_poteaux, "dimensions_plan": (dim_A, dim_B), "epaisseur_h": h_radier, "hauteur_utile_d": d_radier, "sigma_sol_adm": sigma_sol_adm}

# ==============================================================================
# SECTION 2 : LOGIQUE DE CONCEPTION ET FLUX DE TRAVAIL
# ==============================================================================

### --- Logique Commune et pour Poteaux --- ###
def run_single_column_design_process(design_function, design_args):
    initial_results = design_function(**design_args)
    if initial_results.get("status") == "ERREUR": print(f"\nERREUR: {initial_results['message']}"); return None
    v_print("\n--- Vérification ELS : Contrainte Béton ---", "", "", "")
    Nser_estimé_kN = design_args.get('Nu', 0) * 1000 / 1.4 # Estimation grossière G+Q / 1.35G+1.5Q ≈ 1/1.4
    check_concrete_compression_stress(Nser_estimé_kN, design_args['section'], design_args['beton'])
    proposals = initial_results.get('proposals', [])
    if not proposals: print("\nAVERTISSEMENT: Aucune combinaison d'armatures n'a pu être trouvée."); return None
    selected_proposal = handle_rebar_selection(proposals, initial_results['required_longitudinal_steel_cm2'])
    final_results = initial_results.copy(); final_results.update(selected_proposal)
    bar_groups = []; rep_counter = 1
    if final_results['type'] == 'single': bar_groups.append({'rep': rep_counter, 'qty': final_results['num_bars'], 'diam': final_results['diameter']})
    elif final_results['type'] == 'mixed':
        c_count, c_diam = final_results['corner_config']; f_count, f_diam = final_results['face_config']
        bar_groups.append({'rep': rep_counter, 'qty': c_count, 'diam': c_diam}); rep_counter += 1
        if f_count > 0: bar_groups.append({'rep': rep_counter, 'qty': f_count, 'diam': f_diam})
    final_results['bar_groups'] = bar_groups
    bar_diameter = bar_groups[0]['diam']
    final_results['transversal_rebar_diameter'] = max(6, math.ceil(bar_diameter / 3)); final_results['max_transversal_spacing_cm'] = min(15 * (bar_diameter / 10), 40, (min(final_results['section'].b, final_results['section'].h) * 100) + 10)
    display_and_plot_results(final_results)
    return final_results

def handle_rebar_selection(proposals, required_area):
    print("\n" + "="*50); print(f"=== CHOIX DES ACIERS (Besoin: {required_area:.2f} cm²) ==="); print("="*50)
    for i, p in enumerate(proposals): print(f"[{i+1}] {p['text']} (Fourni: {p['provided_area']:.2f} cm²)")
    while True:
        user_choice = get_user_input(f"Choisissez une combinaison [1-{len(proposals)}]", 1, int)
        if 1 <= user_choice <= len(proposals): break
        else: print(f"Erreur : Veuillez entrer un nombre entre 1 et {len(proposals)}.")
    return proposals[user_choice - 1]

def display_and_plot_results(final_results):
    print("\n" + "="*50); print("=== RÉSULTATS FINAUX DU DIMENSIONNEMENT ==="); print("="*50)
    print(f"STATUT: OK"); print(f"Section d'acier requise: {final_results['required_longitudinal_steel_cm2']:.2f} cm²")
    print(f"Combinaison retenue: {final_results['text']}"); print(f"Section d'acier fournie: {final_results['provided_area']:.2f} cm²")
    print(f"Cadres: Φ{final_results['transversal_rebar_diameter']}mm, Espacement max {final_results['max_transversal_spacing_cm']:.1f} cm")
    output_filename = f"plan_ferraillage_{final_results.get('ID_Poteau', 'interactif')}.png"
    plot_column_section(final_results, output_folder="output/rapports_beton_arme", filename=output_filename)

### --- Flux de Travail pour Poteaux --- ###
def calculate_column_interactive():
    print("\n" + "="*50); print("=== MODE INTERACTIF: CALCUL D'UN POTEAU ==="); print("="*50)
    print("Quelle méthode de calcul ?"); print("[1] Flexion Composée (Générale)"); print("[2] Compression Centrée (BAEL 91)")
    method_choice = get_user_input("Choix de la méthode", 1, int)
    beton, acier = define_materials()
    print("\n" + "="*50); print("=== GÉOMÉTRIE ET SOLLICITATIONS ==="); print("="*50)
    Nu = get_user_input("Effort normal ultime Nu (MN)", 0.5); b = get_user_input("Largeur b (m)", 0.3); h = get_user_input("Hauteur h (m)", 0.3); height = get_user_input("Hauteur libre L (m)", 3.0); section = SectionRectangulaire(b, h)
    design_args = {"section": section, "beton": beton, "acier": acier, "height": height}
    if method_choice == 1:
        Mu = get_column_moment_from_user(); k_factor = get_user_input("Coefficient de flambement k", 1.0, float)
        design_args.update({"Nu": Nu, "Mu": Mu, "k_factor": k_factor}); design_function = design_rectangular_column
    else:
        k_factor = get_user_input("Coefficient de flambement k", 0.7, float); design_args.update({"Nu": Nu, "k_factor": k_factor})
        design_function = design_column_compression_bael
    run_single_column_design_process(design_function, design_args)
    input("\nCalcul interactif terminé. Appuyez sur Entrée pour retourner au menu...")

def calculate_columns_batch():
    print("\n" + "="*50); print("=== MODE: CONCEPTION ASSISTÉE PAR LOT ==="); print("="*50)
    default_path = "data/poteaux_a_calculer.csv"; df = None
    while df is None:
        csv_path = get_user_input(prompt=f"Chemin du fichier CSV", default_value=default_path, data_type=str)
        if csv_path.lower() in ['quitter', 'annuler', 'exit']: print("Opération annulée."); return
        try: df = pd.read_csv(csv_path); df.fillna(0, inplace=True); print(f"-> Fichier '{csv_path}' chargé. {len(df)} poteaux à traiter.")
        except Exception as e: print(f"\nERREUR: Impossible de lire le fichier '{csv_path}'.\nDétail: {e}"); df = None
    beton, acier = define_materials(); all_final_results_for_summary = []
    for index, row in df.iterrows():
        print("\n" + "#"*60); print(f"### TRAITEMENT DU POTEAU : {row['ID_Poteau']} ({index + 1}/{len(df)}) ###"); print("#"*60)
        settings.VERBOSE = True
        Mu = 0.0; cas = str(row['cas_poteau']).lower()
        if cas == 'rive': Mu = calculate_beam_end_moment(row['q_gauche'], row['L_gauche'], is_end_span=True)
        elif cas == 'intermediaire': M_gauche = calculate_beam_end_moment(row['q_gauche'], row['L_gauche'], is_end_span=False); M_droite = calculate_beam_end_moment(row['q_droite'], row['L_droite'], is_end_span=False); Mu = abs(M_gauche - M_droite)
        elif cas == 'excentre': Mu = row['Nu_MN'] * row['e_m']
        section = SectionRectangulaire(b=row['largeur_b_m'], h=row['hauteur_h_m'])
        design_args = {"Nu": row['Nu_MN'], "Mu": Mu, "height": row['longueur_L_m'], "k_factor": row['k_flambement'], "section": section, "beton": beton, "acier": acier}
        final_results = run_single_column_design_process(design_args, is_interactive=False)
        if final_results:
            final_results['ID_Poteau'] = row['ID_Poteau']; final_results['Mu_calc_MNm'] = Mu
            all_final_results_for_summary.append(final_results)
        if index < len(df) - 1: input(f"\nTraitement pour {row['ID_Poteau']} terminé. Appuyez sur Entrée pour passer au suivant...")
    if all_final_results_for_summary:
        summary_data = [{"ID": res['ID_Poteau'], "Mu (MN.m)": f"{res['Mu_calc_MNm']:.4f}", "As req (cm²)": f"{res['required_longitudinal_steel_cm2']:.2f}", "Proposition": res['text'], "As fournie (cm²)": f"{res['provided_area']:.2f}"} for res in all_final_results_for_summary]
        summary_df = pd.DataFrame(summary_data); print("\n" + "="*50); print("=== TABLEAU RÉCAPITULATIF FINAL ==="); print("="*50); print(summary_df.to_string(index=False))
    settings.VERBOSE = False; input("\nTraitement par lot terminé. Appuyez sur Entrée pour retourner au menu...")

### --- Flux de Travail pour Radier --- ###
def analyze_strips_interactively(radier_data):
    print("\n" + "="*50); print("--- Étape 2 : Analyse Structurale par Bandes ---"); print("="*50); print("Concept : On découpe le radier en 'bandes'. Chaque bande est analysée comme une poutre continue inversée.")
    poteaux_df = radier_data["poteaux_df"]; dim_A, dim_B = radier_data["dimensions_plan"]
    total_p_u = poteaux_df['P_u_kN'].sum()
    q_u = total_p_u / (dim_A * dim_B) if (dim_A * dim_B) > 0 else 0
    v_print("\nPression du sol (ELU)", "q_u = ΣP_u / S", f"{total_p_u:.1f} / {dim_A*dim_B:.2f}", q_u, "kPa")
    all_moments = {}
    for direction in ['X', 'Y']:
        print(f"\n" + "-"*40); print(f"--- Analyse des bandes dans la direction {direction} ---"); print("-" * 40)
        num_bandes = get_user_input(f"Combien de bandes de calcul dans cette direction ?", 1, int)
        for i in range(num_bandes):
            print(f"\n-- Bande {direction}{i+1} --"); largeur_bande = get_user_input("Largeur de cette bande (m)", dim_B if direction == 'X' else dim_A)
            w_u = q_u * largeur_bande; v_print(f"Charge sur bande {direction}{i+1}", "w_u = q_u * larg.", f"{q_u:.2f} * {largeur_bande:.2f}", w_u, "kN/m")
            num_appuis = get_user_input("Nombre de poteaux (appuis) sur cette bande", 2, int)
            positions = sorted([get_user_input(f"  Position du poteau {j+1} (m)", j * 5.0) for j in range(num_appuis)])
            spans = [positions[k+1] - positions[k] for k in range(len(positions)-1)]
            print(f"\nAnalyse de la bande {direction}{i+1} (travées: {spans} m)...")
            moments = analyze_by_forfaitaire(spans, w_u)
            all_moments[f"Bande_{direction}{i+1}"] = {"max_moment_pos_kNm": max(moments['travees'], default=0), "max_moment_neg_kNm": abs(min(moments['appuis'], default=0))}
    return all_moments

def calculate_radier_interactive():
    """Orchestre le dimensionnement et les vérifications d'un radier."""
    print("\n" + "="*60); print("=== MODULE: DIMENSIONNEMENT D'UN RADIER GÉNÉRAL ==="); print("="*60)
    radier_data = get_radier_inputs()
    if not radier_data: return
    beton, acier = define_materials(); radier_data['beton'] = beton; radier_data['acier'] = acier
    print("\n" + "-"*50); print("--- Vérification ELS : Tassements ---"); print("-" * 50)
    sigma_sol_ser = check_soil_bearing_pressure(radier_data["poteaux_df"]['P_ser_kN'].sum(), radier_data["dimensions_plan"])
    sigma_sol_adm = radier_data.get("sigma_sol_adm", 150.0)
    if sigma_sol_ser <= sigma_sol_adm: print(f"-> VÉRIFICATION OK ({sigma_sol_ser:.2f} kPa <= {sigma_sol_adm:.2f} kPa)")
    else:
        print(f"-> AVERTISSEMENT : NON CONFORME ({sigma_sol_ser:.2f} kPa > {sigma_sol_adm:.2f} kPa). Augmentez les dimensions.")
        cont = input("Continuer malgré tout ? (o/n): ").lower()
        if cont != 'o': return
    all_moments = analyze_strips_interactively(radier_data)
    if all_moments:
        print("\n--- Récapitulatif des Moments Maximaux Calculés ---")
        for bande, results in all_moments.items(): print(f"  - {bande}: M_pos = {results['max_moment_pos_kNm']:.2f} kNm, M_neg = {results['max_moment_neg_kNm']:.2f} kNm")
    print("\n" + "-"*50); print("--- Étape 3 : Calcul du Ferraillage ---"); print("-" * 50); print("(Fonctionnalité en cours de développement)")
    print("\n" + "-"*50); print("--- Étape 4 : Vérification au Poinçonnement ---"); print("-" * 50); print("(Fonctionnalité en cours de développement)")
    input("\nCalcul du radier terminé. Appuyez sur Entrée...")

# ==============================================================================
# SECTION 4 : MENUS DE NAVIGATION
# ==============================================================================
def calculate_beam():
    print("\n--- Module poutre (en développement) ---"); input("Appuyez sur Entrée...")

def menu_poteau():
    while True:
        print("\n--- Menu : Calcul des Poteaux ---"); print("[1] Mode Interactif"); print("[2] Mode par Lot (CSV)"); print("[0] Retour")
        choice = input("Votre choix : ").strip()
        if choice == '1': calculate_column_interactive()
        elif choice == '2': calculate_columns_batch()
        elif choice == '0': break
        else: print("Choix invalide.")

def start_ba_module():
    """Gère le menu principal du module Béton Armé."""
    while True:
        print("\n--- Domaine : Béton Armé ---"); print("Quel ouvrage souhaitez-vous dimensionner ?"); print("[1] Poteau Rectangulaire"); print("[2] Radier Général"); print("[3] Poutre (à venir)"); print("[0] Retour au menu principal")
        choice = input("Votre choix : ").strip()
        if choice == '1': menu_poteau()
        elif choice == '2': calculate_radier_interactive()
        elif choice == '3': calculate_beam()
        elif choice == '0': break
        else: print("Choix invalide.")