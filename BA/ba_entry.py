# PROJET_DIMENTIONEMENT/BA/ba_entry.py
# Version "Expert" finale, améliorée, clarifiée et sans répétition de code.

# --- Imports ---
import pandas as pd
import math
from utils import settings
from utils.ui_helpers import get_user_input, v_print
from BA.core.materials import Beton, Acier
from BA.core.sections import SectionRectangulaire
from BA.core.design.column_design import design_rectangular_column, design_column_compression_bael
from BA.core.rebar_selector import get_rebar_proposals
from BA.reports.plotting import plot_column_section
from BA.core.analysis.moment_calculator import calculate_beam_end_moment
from BA.core.design.raft_foundation_design import design_raft_by_strip_method

# poteau

# ==============================================================================
# SECTION 1 : FONCTIONS DE SAISIE UTILISATEUR
# ==============================================================================

def define_materials():
    """Interface utilisateur pour définir les matériaux (Béton et Acier)."""
    print("\n" + "="*50); print("=== ÉTAPE 1: DÉFINITION DES MATÉRIAUX ==="); print("="*50)
    print("\n--- 1.1. Choix du Béton ---"); print("[1] C25/30 (fc28 = 25 MPa) - Courant"); print("[2] C30/37 (fc28 = 30 MPa)"); print("[3] Personnalisé")
    beton_choice = get_user_input("Votre choix pour le béton", 1, int)
    if beton_choice == 1: fc28 = 25.0
    elif beton_choice == 2: fc28 = 30.0
    else: fc28 = get_user_input("Entrez la résistance du béton fc28 (MPa)", 25.0, float)
    gamma_b = get_user_input("Entrez le coefficient de sécurité du béton γb", 1.5, float)
    beton = Beton(fc28=fc28, gamma_b=gamma_b)
    print(f"-> Béton défini : {beton}")
    
    print("\n--- 1.2. Choix de l'Acier ---"); print("[1] S500 (fe = 500 MPa) - Courant"); print("[2] S400 (fe = 400 MPa) - Ancien"); print("[3] Personnalisé")
    acier_choice = get_user_input("Votre choix pour l'acier", 1, int)
    if acier_choice == 1: fe = 500.0
    elif acier_choice == 2: fe = 400.0
    else: fe = get_user_input("Entrez la limite élastique de l'acier fe (MPa)", 500.0, float)
    gamma_s = get_user_input("Entrez le coefficient de sécurité de l'acier γs", 1.15, float)
    acier = Acier(fe=fe, gamma_s=gamma_s)
    print(f"-> Acier défini : {acier}")
    return beton, acier

def get_column_moment_from_user():
    """Menu interactif pour aider l'utilisateur à déterminer Mu."""
    print("\n" + "-"*40); print("--- Détermination du Moment Ultime Mu ---"); print("Choisissez le cas de figure :"); print("[1] Poteau de Rive"); print("[2] Poteau Intermédiaire"); print("[3] Charge Excentrée"); print("[4] Entrée manuelle")
    case_choice = get_user_input("Votre choix de cas", 4, int)
    if case_choice == 1:
        print("\n--- Cas 1 : Poteau de Rive ---"); q = get_user_input("Charge q (kN/m)", 25.0); L = get_user_input("Portée L (m)", 5.0)
        return calculate_beam_end_moment(q, L, is_end_span=True)
    elif case_choice == 2:
        print("\n--- Cas 2 : Poteau Intermédiaire ---"); print("Poutre de GAUCHE :"); q_gauche = get_user_input("Charge q (kN/m)", 25.0); L_gauche = get_user_input("Portée L (m)", 5.0); M_gauche = calculate_beam_end_moment(q_gauche, L_gauche, is_end_span=False)
        print("\nPoutre de DROITE :"); q_droite = get_user_input("Charge q (kN/m)", 22.0); L_droite = get_user_input("Portée L (m)", 4.5); M_droite = calculate_beam_end_moment(q_droite, L_droite, is_end_span=False)
        Mu = abs(M_gauche - M_droite); v_print("Moment de continuité", "Mu = |Mg - Md|", f"|{M_gauche:.4f} - {M_droite:.4f}|", Mu, "MN.m"); return Mu
    elif case_choice == 3:
        print("\n--- Cas 3 : Charge Excentrée ---"); Nu_load = get_user_input("Valeur de la charge ponctuelle Nu (MN)", 0.1); e = get_user_input("Distance d'excentricité e (m)", 0.15); Mu = Nu_load * e; v_print("Moment d'excentricité", "Mu = Nu * e", f"{Nu_load:.2f} * {e:.2f}", Mu, "MN.m"); return Mu
    else:
        return get_user_input("Entrez la valeur de Mu (MN.m)", 0.05)

# ==============================================================================
# SECTION 2 : LOGIQUE DE CONCEPTION CENTRALE
# ==============================================================================

def run_single_column_design_process(design_function, design_args):
    """Exécute le processus complet de conception pour UN seul poteau."""
    initial_results = design_function(**design_args)
    if initial_results.get("status") == "ERREUR":
        print(f"\nERREUR: {initial_results['message']}")
        return None

    proposals = initial_results.get('proposals', [])
    if not proposals:
        print("\nAVERTISSEMENT: Aucune combinaison d'armatures n'a pu être trouvée.")
        return None
        
    selected_proposal = handle_rebar_selection(proposals, initial_results['required_longitudinal_steel_cm2'])

    # Finalisation des résultats
    final_results = initial_results.copy()
    final_results.update(selected_proposal)
    
    # Construction de la structure 'bar_groups' pour la nomenclature et le dessin
    bar_groups = []
    if final_results['type'] == 'single':
        bar_groups.append({'rep': 1, 'qty': final_results['num_bars'], 'diam': final_results['diameter']})
    elif final_results['type'] == 'mixed':
        c_count, c_diam = final_results['corner_config']
        f_count, f_diam = final_results['face_config']
        bar_groups.append({'rep': 1, 'qty': c_count, 'diam': c_diam})
        if f_count > 0: bar_groups.append({'rep': 2, 'qty': f_count, 'diam': f_diam})
    final_results['bar_groups'] = bar_groups
    
    # Calcul des cadres
    bar_diameter = bar_groups[0]['diam']
    final_results['transversal_rebar_diameter'] = max(6, math.ceil(bar_diameter / 3))
    final_results['max_transversal_spacing_cm'] = min(15 * (bar_diameter / 10), 40, (min(final_results['section'].b, final_results['section'].h) * 100) + 10)

    display_and_plot_results(final_results)
    return final_results

def handle_rebar_selection(proposals, required_area):
    """Affiche les propositions et gère le choix de l'utilisateur de manière robuste."""
    print("\n" + "="*50); print(f"=== ÉTAPE 3: CHOIX DES ACIERS (Besoin: {required_area:.2f} cm²) ==="); print("="*50)
    for i, p in enumerate(proposals): print(f"[{i+1}] {p['text']} (Fourni: {p['provided_area']:.2f} cm²)")
    while True:
        user_choice = get_user_input(f"Choisissez une combinaison [1-{len(proposals)}]", 1, int)
        if 1 <= user_choice <= len(proposals): break
        else: print(f"Erreur : Veuillez entrer un nombre entre 1 et {len(proposals)}.")
    return proposals[user_choice - 1]

def display_and_plot_results(final_results):
    """Affiche le résumé final et génère le plan."""
    print("\n" + "="*50); print("=== RÉSULTATS FINAUX DU DIMENSIONNEMENT ==="); print("="*50)
    print(f"STATUT: OK")
    print(f"Section d'acier requise    : {final_results['required_longitudinal_steel_cm2']:.2f} cm²")
    print(f"Combinaison retenue        : {final_results['text']}")
    print(f"Section d'acier fournie    : {final_results['provided_area']:.2f} cm²")
    print(f"Cadres                     : Φ{final_results['transversal_rebar_diameter']}mm, Espacement max {final_results['max_transversal_spacing_cm']:.1f} cm")
    
    output_filename = f"plan_ferraillage_{final_results.get('ID_Poteau', 'interactif')}.png"
    plot_column_section(final_results, output_folder="BA/output", filename=output_filename)

# ==============================================================================
# SECTION 3 : FLUX DE TRAVAIL PRINCIPAUX
# ==============================================================================

def calculate_column_interactive():
    """Gère le flux de travail pour le mode interactif."""
    print("\n" + "="*50); print("=== MODE INTERACTIF: CALCUL D'UN POTEAU ==="); print("="*50)
    print("Quelle méthode de calcul ?"); print("[1] Flexion Composée (Générale)"); print("[2] Compression Centrée (BAEL 91)")
    method_choice = get_user_input("Choix de la méthode", 1, int)
    
    beton, acier = define_materials()
    print("\n" + "="*50); print("=== GÉOMÉTRIE ET SOLLICITATIONS ==="); print("="*50)
    Nu = get_user_input("Effort normal ultime Nu (MN)", 0.5)
    b = get_user_input("Largeur de la section b (m)", 0.3); h = get_user_input("Hauteur de la section h (m)", 0.3)
    height = get_user_input("Hauteur libre du poteau L (m)", 3.0); section = SectionRectangulaire(b, h)
    
    design_args = {"section": section, "beton": beton, "acier": acier, "height": height}
    
    if method_choice == 1:
        Mu = get_column_moment_from_user(); k_factor = get_user_input("Coefficient de flambement k", 1.0, float)
        design_args.update({"Nu": Nu, "Mu": Mu, "k_factor": k_factor})
        design_function = design_rectangular_column
    else:
        k_factor = get_user_input("Coefficient de flambement k", 0.7, float); design_args.update({"Nu": Nu, "k_factor": k_factor})
        design_function = design_column_compression_bael
        
    run_single_column_design_process(design_function, design_args)
    input("\nCalcul interactif terminé. Appuyez sur Entrée pour retourner au menu...")

def calculate_columns_batch():
    """Gère le flux de travail pour le mode par lot (conception assistée)."""
    print("\n" + "="*50); print("=== MODE: CONCEPTION ASSISTÉE PAR LOT ==="); print("="*50)
    default_path = "BA/data/poteaux_a_calculer.csv"; df = None
    while df is None:
        csv_path = get_user_input(prompt=f"Chemin du fichier CSV", default_value=default_path, data_type=str)
        if csv_path.lower() in ['quitter', 'annuler', 'exit']: print("Opération annulée."); return
        try: df = pd.read_csv(csv_path); df.fillna(0, inplace=True); print(f"-> Fichier '{csv_path}' chargé. {len(df)} poteaux à traiter.")
        except Exception as e: print(f"\nERREUR: Impossible de lire le fichier '{csv_path}'.\nDétail: {e}"); df = None
    
    beton, acier = define_materials()
    all_final_results_for_summary = []
    
    for index, row in df.iterrows():
        print("\n" + "#"*60); print(f"### TRAITEMENT DU POTEAU : {row['ID_Poteau']} ({index + 1}/{len(df)}) ###"); print("#"*60)
        settings.VERBOSE = True
        
        Mu = 0.0; cas = str(row['cas_poteau']).lower()
        if cas == 'rive': Mu = calculate_beam_end_moment(row['q_gauche'], row['L_gauche'], is_end_span=True)
        elif cas == 'intermediaire': M_gauche = calculate_beam_end_moment(row['q_gauche'], row['L_gauche'], is_end_span=False); M_droite = calculate_beam_end_moment(row['q_droite'], row['L_droite'], is_end_span=False); Mu = abs(M_gauche - M_droite)
        elif cas == 'excentre': Mu = row['Nu_MN'] * row['e_m']
        
        section = SectionRectangulaire(b=row['largeur_b_m'], h=row['hauteur_h_m'])
        design_args = {"Nu": row['Nu_MN'], "Mu": Mu, "height": row['longueur_L_m'], "k_factor": row['k_flambement'], "section": section, "beton": beton, "acier": acier}
        
        final_results = run_single_column_design_process(design_rectangular_column, design_args)
        
        if final_results:
            final_results['ID_Poteau'] = row['ID_Poteau']; final_results['Mu_calc_MNm'] = Mu
            all_final_results_for_summary.append(final_results)
        
        if index < len(df) - 1: input(f"\nTraitement pour {row['ID_Poteau']} terminé. Appuyez sur Entrée pour passer au suivant...")

    if all_final_results_for_summary:
        summary_data = [{"ID": res['ID_Poteau'], "Mu_calc (MN.m)": f"{res['Mu_calc_MNm']:.4f}", "As_req (cm²)": f"{res['required_longitudinal_steel_cm2']:.2f}", "Proposition": res['text'], "As_fournie (cm²)": f"{res['provided_area']:.2f}", "Statut": res['status']} for res in all_final_results_for_summary]
        summary_df = pd.DataFrame(summary_data); print("\n" + "="*50); print("=== TABLEAU RÉCAPITULATIF FINAL ==="); print("="*50); print(summary_df.to_string(index=False))
        
    settings.VERBOSE = False
    input("\nTraitement par lot terminé. Appuyez sur Entrée pour retourner au menu...")

# ==============================================================================
# SECTION 4 : MENUS DE NAVIGATION
# ==============================================================================
def calculate_beam():
    print("\n--- Module de calcul de poutre (en développement) ---"); input("Appuyez sur Entrée pour continuer...")

def menu_poteau():
    """Gère le sous-menu dédié au calcul des poteaux."""
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
        print("\n--- Domaine : Béton Armé ---"); print("Quel ouvrage souhaitez-vous dimensionner ?"); print("[1] Poteau Rectangulaire"); print("[2] Poutre (à venir)"); print("[0] Retour au menu principal")
        choice = input("Votre choix : ").strip()
        if choice == '1': menu_poteau()
        elif choice == '2': calculate_beam()
        elif choice == '0': break
        else: print("Choix invalide.")


#######################
#radier
def calculate_raft_foundation_interactive():
    """Interface utilisateur pour le calcul d'un radier général."""
    print("\n" + "="*50)
    print("=== MODE INTERACTIF: CALCUL D'UN RADIER GÉNÉRAL ===")
    print("="*50)
    
    # --- Saisie des données générales ---
    beton, acier = define_materials()
    print("\n" + "="*50)
    print("=== DONNÉES GÉNÉRALES DU PROJET ===")
    print("="*50)
    
    csv_path = get_user_input("Chemin du fichier CSV des poteaux", "BA/data/radier_poteaux.csv", str)
    try:
        df = pd.read_csv(csv_path)
        print(f"-> Fichier '{csv_path}' chargé avec {len(df)} poteaux.")
    except FileNotFoundError:
        print(f"ERREUR: Fichier non trouvé. Le calcul ne peut pas continuer.")
        input("\nAppuyez sur Entrée pour retourner au menu...")
        return

    sigma_sol = get_user_input("Contrainte admissible du sol σ_sol (MPa)", 0.15)
    A = get_user_input("Longueur totale du radier A (m)", 14.0)
    B = get_user_input("Largeur totale du radier B (m)", 12.0)
    h = get_user_input("Épaisseur estimée du radier h (m)", 0.60)
    
    # --- Lancement du calcul ---
    results = design_raft_by_strip_method(df, A, B, h, sigma_sol, beton, acier)
    
    # --- Affichage des résultats ---
    print("\n" + "="*50)
    print("=== RÉSULTATS DU DIMENSIONNEMENT DU RADIER (Bande X) ===")
    print("="*50)
    if results['status'] == 'OK':
        print(f"Aciers supérieurs (chapeaux sur poteaux): {results['As_sup_X_cm2_per_m']:.2f} cm²/m")
        print(f"Aciers inférieurs (nappe en travée)    : {results['As_inf_X_cm2_per_m']:.2f} cm²/m")
        print(f"\nNOTE: {results['message']}")
    else:
        print(f"ERREUR: {results.get('message', 'Calcul non abouti.')}")
        
    input("\nCalcul terminé. Appuyez sur Entrée pour retourner au menu...")