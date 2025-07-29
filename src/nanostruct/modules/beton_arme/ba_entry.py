# PROJET_DIMENTIONEMENT/BA/ba_entry.py
# Version "Expert" finale, refactorisée, complète et avec toutes les fonctionnalités intégrées.

# --- Imports ---
import pandas as pd
import math
from nanostruct.utils import settings
from nanostruct.utils.ui_rich import (
    afficher_action,
    afficher_resultat,
    afficher_erreur,
    afficher_menu_et_choisir,
    poser_question,
)
from nanostruct.modules.beton_arme.core.materials import Beton, Acier
from nanostruct.modules.beton_arme.core.sections import SectionRectangulaire
from nanostruct.modules.beton_arme.core.design.column_design import (
    design_rectangular_column,
    design_column_compression_bael,
)
from nanostruct.modules.beton_arme.reports.plotting import plot_column_section
from nanostruct.modules.beton_arme.core.analysis.continuous_beam import (
    analyze_by_forfaitaire,
)
from nanostruct.modules.beton_arme.core.analysis.moment_calculator import (
    calculate_beam_end_moment,
)
from nanostruct.modules.beton_arme.core.checks.service_limit_states import (
    check_soil_bearing_pressure,
    check_concrete_compression_stress,
)

# ==============================================================================
# SECTION 1 : FONCTIONS DE SAISIE UTILISATEUR
# ==============================================================================


def define_materials():
    """Interface utilisateur pour définir les matériaux (Béton et Acier)."""
    afficher_action("=== ÉTAPE 1: DÉFINITION DES MATÉRIAUX ===")
    
    options_beton = {
        "1": "C25/30 (Courant)",
        "2": "C30/37",
        "3": "Personnalisé",
    }
    beton_choice = afficher_menu_et_choisir("--- 1.1. Choix du Béton ---", options_beton, default="1")

    if beton_choice == "1":
        fc28 = 25.0
    elif beton_choice == "2":
        fc28 = 30.0
    else:
        fc28 = poser_question("Résistance fc28 (MPa)", default="25.0", type=float)
    gamma_b = poser_question("Coeff. sécurité béton γb", default=1.5, value_type=float)
    beton = Beton(fc28=fc28, gamma_b=gamma_b)
    afficher_resultat(f"-> Béton défini : {beton}")

    options_acier = {
        "1": "S500 (Courant)",
        "2": "S400",
        "3": "Personnalisé",
    }
    acier_choice = afficher_menu_et_choisir("--- 1.2. Choix de l'Acier ---", options_acier, default="1")

    if acier_choice == "1":
        fe = 500.0
    elif acier_choice == "2":
        fe = 400.0
    else:
        fe = poser_question("Limite élastique fe (MPa)", default="500.0", type=float)
    gamma_s = poser_question("Coeff. sécurité acier γs", default=1.15, value_type=float)
    acier = Acier(fe=fe, gamma_s=gamma_s)
    afficher_resultat(f"-> Acier défini : {acier}")
    return beton, acier


def get_column_moment_from_user():
    """Menu interactif pour aider l'utilisateur à déterminer Mu pour un poteau."""
    options = {
        "1": "Poteau de Rive",
        "2": "Poteau Intermédiaire",
        "3": "Charge Excentrée",
        "4": "Entrée manuelle",
    }
    case_choice = afficher_menu_et_choisir("--- Détermination du Moment Ultime Mu ---", options, default="4")

    if case_choice == "1":
        afficher_action("--- Cas 1 : Poteau de Rive ---")
        q = poser_question("Charge q (kN/m)", default="25.0", type=float)
        L = poser_question("Portée L (m)", default="5.0", type=float)
        return calculate_beam_end_moment(q, L, is_end_span=True)
    elif case_choice == "2":
        afficher_action("--- Cas 2 : Poteau Intermédiaire ---")
        afficher_action("Poutre de GAUCHE :")
        q_gauche = poser_question("Charge q (kN/m)", default="25.0", type=float)
        L_gauche = poser_question("Portée L (m)", default="5.0", type=float)
        M_gauche = calculate_beam_end_moment(q_gauche, L_gauche, is_end_span=False)
        afficher_action("\nPoutre de DROITE :")
        q_droite = poser_question("Charge q (kN/m)", default="22.0", type=float)
        L_droite = poser_question("Portée L (m)", default="4.5", type=float)
        M_droite = calculate_beam_end_moment(q_droite, L_droite, is_end_span=False)
        Mu = abs(M_gauche - M_droite)
        if settings.VERBOSE:
            afficher_resultat(f"Moment de continuité final: Mu = |Mg - Md| = |{M_gauche:.4f} - {M_droite:.4f}| = {Mu:.4f} MN.m")
        return Mu
    elif case_choice == "3":
        afficher_action("--- Cas 3 : Charge Excentrée ---")
        Nu_load = poser_question("Charge ponctuelle Nu (MN)", default="0.1", type=float)
        e = poser_question("Excentricité e (m)", default="0.15", type=float)
        Mu = Nu_load * e
        if settings.VERBOSE:
            afficher_resultat(f"Moment d'excentricité: Mu = Nu * e = {Nu_load:.2f} * {e:.2f} = {Mu:.4f} MN.m")
        return Mu
    else:
        return poser_question("Entrez la valeur de Mu (MN.m)", default="0.05", type=float)


def get_radier_inputs():
    """Fonction interactive et pédagogique pour collecter les données du radier."""
    afficher_action("--- Étape 1 : Données d'Entrée et Prédimensionnement ---")
    afficher_resultat(
        "Concept : On détermine d'abord les charges totales et les dimensions globales du radier."
    )
    options = {
        "1": "Par charges brutes (G et Q)",
        "2": "Par sollicitations (Nser et Nu)",
    }
    input_type = afficher_menu_et_choisir("Comment souhaitez-vous définir les charges des poteaux ?", options, default="1")
    poteaux = []
    num_poteaux = poser_question(
        "\nCombien de poteaux reposent sur le radier ?", default=4, value_type=int
    )
    if num_poteaux <= 0:
        afficher_erreur("Nombre de poteaux invalide. Opération annulée.")
        return None
    afficher_action("\nEntrez les données pour chaque poteau :")
    for i in range(num_poteaux):
        afficher_action(f"--- Poteau n°{i + 1} ---")
        p_id = poser_question(f"ID du poteau (ex: P1) [défaut: P{i + 1}]: ", default=f"P{i + 1}")
        if input_type == "1":
            charge_g = poser_question("  Charge permanente G (Tonnes)", default="50.0", type=float)
            charge_q = poser_question("  Charge d'exploitation Q (Tonnes)", default="20.0", type=float)
            p_ser_kn = (charge_g + charge_q) * 9.81
            p_u_kn = (1.35 * charge_g + 1.5 * charge_q) * 9.81
        else:
            p_ser_kn = poser_question("  Sollicitation de service N_ser (kN)", default="686.7", type=float)
            p_u_kn = poser_question("  Sollicitation ultime N_u (kN)", default="971.4", type=float)
        poteaux.append({"ID": p_id, "P_ser_kN": p_ser_kn, "P_u_kN": p_u_kn})
    df_poteaux = pd.DataFrame(poteaux)
    afficher_action("\n" + "-" * 30)
    afficher_resultat("Calcul des charges totales :")
    afficher_action("-" * 30)
    total_p_ser_kN = df_poteaux["P_ser_kN"].sum()
    total_p_u_kN = df_poteaux["P_u_kN"].sum()
    if settings.VERBOSE:
        afficher_resultat(f"Charge de service totale: ΣP_ser = {total_p_ser_kN / 9.81:.1f} T = {total_p_ser_kN:.1f} kN")
    if settings.VERBOSE:
        afficher_resultat(f"Charge ultime totale: ΣP_u = {total_p_u_kN / 9.81:.1f} T = {total_p_u_kN:.1f} kN")
    afficher_action("\n" + "-" * 30)
    afficher_resultat("Dimensions du radier en plan :")
    afficher_action("-" * 30)
    sigma_sol_adm = poser_question(
        "Contrainte admissible du sol σ_sol,adm (kPa)", default="150.0", type=float
    )
    surface_requise = total_p_ser_kN / sigma_sol_adm
    if settings.VERBOSE:
        afficher_resultat(f"Surface minimale requise: S_req = ΣP_ser / σ_sol,adm = {total_p_ser_kN:.1f} / {sigma_sol_adm:.1f} = {surface_requise:.2f} m²")
    dim_A = poser_question(
        "Dimension A du radier (m)", default=str(round(math.sqrt(surface_requise), 1)), type=float
    )
    dim_B = poser_question(
        "Dimension B du radier (m)",
        default=str(round(surface_requise / dim_A, 1)) if dim_A > 0 else "0",
        type=float
    )
    afficher_action("\n" + "-" * 30)
    afficher_resultat("Épaisseur du radier :")
    afficher_action("-" * 30)
    portee_max = poser_question("Plus grande portée entre poteaux L_max (m) ?", default="6.0", type=float)
    h_estime = portee_max / 10
    if settings.VERBOSE:
        afficher_resultat(f"Épaisseur estimée: h ≈ L_max / 10 = {portee_max:.1f} / 10 = {h_estime:.2f} m")
    h_radier = poser_question(
        "Choisissez l'épaisseur finale h du radier (m)", default=str(math.ceil(h_estime * 20) / 20), type=float
    )
    d_radier = h_radier - 0.07
    afficher_action("\n" + "=" * 50)
    afficher_resultat("--- RÉCAPITULATIF DU PRÉDIMENSIONNEMENT ---")
    afficher_action("=" * 50)
    afficher_resultat(
        f"  - Dimensions : {dim_A:.2f}m x {dim_B:.2f}m (Surface = {dim_A * dim_B:.2f} m²)"
    )
    afficher_resultat(f"  - Épaisseur : {h_radier:.2f}m (Hauteur utile d ≈ {d_radier:.2f}m)")
    return {
        "poteaux_df": df_poteaux,
        "dimensions_plan": (dim_A, dim_B),
        "epaisseur_h": h_radier,
        "hauteur_utile_d": d_radier,
        "sigma_sol_adm": sigma_sol_adm,
    }


# ==============================================================================
# SECTION 2 : LOGIQUE DE CONCEPTION ET FLUX DE TRAVAIL
# ==============================================================================


### --- Logique Commune et pour Poteaux --- ###
def run_single_column_design_process(design_function, design_args):
    initial_results = design_function(**design_args)
    if initial_results.get("status") == "ERREUR":
        afficher_erreur(f"\nERREUR: {initial_results['message']}")
        return None
    if settings.VERBOSE:
        afficher_resultat("\n--- Vérification ELS : Contrainte Béton ---")
    Nser_estimé_kN = (
        design_args.get("Nu", 0) * 1000 / 1.4
    )  # Estimation grossière G+Q / 1.35G+1.5Q ≈ 1/1.4
    check_concrete_compression_stress(
        Nser_estimé_kN, design_args["section"], design_args["beton"]
    )
    proposals = initial_results.get("proposals", [])
    if not proposals:
        afficher_erreur("\nAVERTISSEMENT: Aucune combinaison d'armatures n'a pu être trouvée.")
        return None
    selected_proposal = handle_rebar_selection(
        proposals, initial_results["required_longitudinal_steel_cm2"]
    )
    final_results = initial_results.copy()
    final_results.update(selected_proposal)
    bar_groups = []
    rep_counter = 1
    if final_results["type"] == "single":
        bar_groups.append(
            {
                "rep": rep_counter,
                "qty": final_results["num_bars"],
                "diam": final_results["diameter"],
            }
        )
    elif final_results["type"] == "mixed":
        c_count, c_diam = final_results["corner_config"]
        f_count, f_diam = final_results["face_config"]
        bar_groups.append({"rep": rep_counter, "qty": c_count, "diam": c_diam})
        rep_counter += 1
        if f_count > 0:
            bar_groups.append({"rep": rep_counter, "qty": f_count, "diam": f_diam})
    final_results["bar_groups"] = bar_groups
    bar_diameter = bar_groups[0]["diam"]
    final_results["transversal_rebar_diameter"] = max(6, math.ceil(bar_diameter / 3))
    final_results["max_transversal_spacing_cm"] = min(
        15 * (bar_diameter / 10),
        40,
        (min(final_results["section"].b, final_results["section"].h) * 100) + 10,
    )
    display_and_plot_results(final_results)
    return final_results


def handle_rebar_selection(proposals, required_area):
    afficher_action(f"=== CHOIX DES ACIERS (Besoin: {required_area:.2f} cm²) ===")
    options = {str(i + 1): f"{p['text']} (Fourni: {p['provided_area']:.2f} cm²)" for i, p in enumerate(proposals)}
    
    while True:
        user_choice = afficher_menu_et_choisir("Choisissez une combinaison", options, default="1")
        if user_choice in options:
            break
        else:
            afficher_erreur(f"Erreur : Veuillez entrer un nombre entre 1 et {len(proposals)}.")
    return proposals[int(user_choice) - 1]


def display_and_plot_results(final_results):
    afficher_action("=== RÉSULTATS FINAUX DU DIMENSIONNEMENT ===")
    afficher_resultat("STATUT: OK")
    afficher_resultat(
        f"Section d'acier requise: {final_results['required_longitudinal_steel_cm2']:.2f} cm²"
    )
    afficher_resultat(f"Combinaison retenue: {final_results['text']}")
    afficher_resultat(f"Section d'acier fournie: {final_results['provided_area']:.2f} cm²")
    afficher_resultat(
        f"Cadres: Φ{final_results['transversal_rebar_diameter']}mm, Espacement max {final_results['max_transversal_spacing_cm']:.1f} cm"
    )
    output_filename = (
        f"plan_ferraillage_{final_results.get('ID_Poteau', 'interactif')}.png"
    )
    plot_column_section(
        final_results,
        output_folder="output/rapports_beton_arme",
        filename=output_filename,
    )


### --- Flux de Travail pour Poteaux --- ###
def calculate_column_interactive():
    afficher_action("=== MODE INTERACTIF: CALCUL D'UN POTEAU ===")
    options = {
        "1": "Flexion Composée (Générale)",
        "2": "Compression Centrée (BAEL 91)",
    }
    method_choice = afficher_menu_et_choisir("Quelle méthode de calcul ?", options, default="1")
    beton, acier = define_materials()
    afficher_action("=== GÉOMÉTRIE ET SOLLICITATIONS ===")
    Nu = poser_question("Effort normal ultime Nu (MN)", default=0.5, value_type=float)
    b = poser_question("Largeur b (m)", default=0.3, value_type=float)
    h = poser_question("Hauteur h (m)", default=0.3, value_type=float)
    height = poser_question("Hauteur libre L (m)", default="3.0", type=float)
    section = SectionRectangulaire(b, h)
    design_args = {"section": section, "beton": beton, "acier": acier, "height": height}
    if method_choice == "1":
        Mu = get_column_moment_from_user()
        k_factor = poser_question("Coefficient de flambement k", default="1.0", type=float)
        design_args.update({"Nu": Nu, "Mu": Mu, "k_factor": k_factor})
        design_function = design_rectangular_column
    else:
        k_factor = poser_question("Coefficient de flambement k", default="0.7", type=float)
        design_args.update({"Nu": Nu, "k_factor": k_factor})
        design_function = design_column_compression_bael
    run_single_column_design_process(design_function, design_args)
    poser_question("\nCalcul interactif terminé. Appuyez sur Entrée pour retourner au menu...")


def calculate_columns_batch():
    afficher_action("=== MODE: CONCEPTION ASSISTÉE PAR LOT ===")
    default_path = "data/poteaux_a_calculer.csv"
    df = None
    while df is None:
        csv_path = poser_question("Chemin du fichier CSV", default=default_path)
        if csv_path.lower() in ["quitter", "annuler", "exit"]:
            afficher_resultat("Opération annulée.")
            return
        try:
            df = pd.read_csv(csv_path)
            df.fillna(0, inplace=True)
            afficher_resultat(f"-> Fichier '{csv_path}' chargé. {len(df)} poteaux à traiter.")
        except Exception as e:
            afficher_erreur(f"\nERREUR: Impossible de lire le fichier '{csv_path}'.\nDétail: {e}")
            df = None
    beton, acier = define_materials()
    all_final_results_for_summary = []
    for index, row in df.iterrows():
        afficher_action("\n" + "#" * 60)
        afficher_action(
            f"### TRAITEMENT DU POTEAU : {row['ID_Poteau']} ({index + 1}/{len(df)}) ###"
        )
        afficher_action("#" * 60)
        settings.VERBOSE = True
        Mu = 0.0
        cas = str(row["cas_poteau"]).lower()
        if cas == "rive":
            Mu = calculate_beam_end_moment(
                row["q_gauche"], row["L_gauche"], is_end_span=True
            )
        elif cas == "intermediaire":
            M_gauche = calculate_beam_end_moment(
                row["q_gauche"], row["L_gauche"], is_end_span=False
            )
            M_droite = calculate_beam_end_moment(
                row["q_droite"], row["L_droite"], is_end_span=False
            )
            Mu = abs(M_gauche - M_droite)
        elif cas == "excentre":
            Mu = row["Nu_MN"] * row["e_m"]
        section = SectionRectangulaire(b=row["largeur_b_m"], h=row["hauteur_h_m"])
        design_args = {
            "Nu": row["Nu_MN"],
            "Mu": Mu,
            "height": row["longueur_L_m"],
            "k_factor": row["k_flambement"],
            "section": section,
            "beton": beton,
            "acier": acier,
        }
        final_results = run_single_column_design_process(
            design_rectangular_column, design_args
        )
        if final_results:
            final_results["ID_Poteau"] = row["ID_Poteau"]
            final_results["Mu_calc_MNm"] = Mu
            all_final_results_for_summary.append(final_results)
        if index < len(df) - 1:
            poser_question(
                f"\nTraitement pour {row['ID_Poteau']} terminé. Appuyez sur Entrée pour passer au suivant..."
            )
    if all_final_results_for_summary:
        summary_data = [
            {
                "ID": res["ID_Poteau"],
                "Mu (MN.m)": f"{res['Mu_calc_MNm']:.4f}",
                "As req (cm²)": f"{res['required_longitudinal_steel_cm2']:.2f}",
                "Proposition": res["text"],
                "As fournie (cm²)": f"{res['provided_area']:.2f}",
            }
            for res in all_final_results_for_summary
        ]
        summary_df = pd.DataFrame(summary_data)
        afficher_action("\n" + "=" * 50)
        afficher_resultat("=== TABLEAU RÉCAPITULATIF FINAL ===")
        afficher_action("=" * 50)
        print(summary_df.to_string(index=False))
    settings.VERBOSE = False
    poser_question("\nTraitement par lot terminé. Appuyez sur Entrée pour retourner au menu...")


### --- Flux de Travail pour Radier --- ###
def analyze_strips_interactively(radier_data):
    afficher_action("--- Étape 2 : Analyse Structurale par Bandes ---")
    afficher_resultat(
        "Concept : On découpe le radier en 'bandes'. Chaque bande est analysée comme une poutre continue inversée."
    )
    poteaux_df = radier_data["poteaux_df"]
    dim_A, dim_B = radier_data["dimensions_plan"]
    total_p_u = poteaux_df["P_u_kN"].sum()
    q_u = total_p_u / (dim_A * dim_B) if (dim_A * dim_B) > 0 else 0
    if settings.VERBOSE:
        afficher_resultat(f"\nPression du sol (ELU): q_u = ΣP_u / S = {total_p_u:.1f} / {dim_A * dim_B:.2f} = {q_u:.2f} kPa")
    all_moments = {}
    for direction in ["X", "Y"]:
        afficher_action(f"--- Analyse des bandes dans la direction {direction} ---")
        num_bandes = poser_question(
            "Combien de bandes de calcul dans cette direction ?", default="1", type=int
        )
        for i in range(num_bandes):
            afficher_action(f"-- Bande {direction}{i + 1} --")
            largeur_bande = poser_question(
                "Largeur de cette bande (m)", default=dim_B if direction == "X" else dim_A, type=float
            )
            w_u = q_u * largeur_bande
            if settings.VERBOSE:
                afficher_resultat(f"Charge sur bande {direction}{i + 1}: w_u = q_u * larg. = {q_u:.2f} * {largeur_bande:.2f} = {w_u:.2f} kN/m")
            num_appuis = poser_question(
                "Nombre de poteaux (appuis) sur cette bande", default=2, type=int
            )
            positions = sorted(
                [
                    poser_question(f"  Position du poteau {j + 1} (m)", default=j * 5.0, type=float)
                    for j in range(num_appuis)
                ]
            )
            spans = [positions[k + 1] - positions[k] for k in range(len(positions) - 1)]
            afficher_action(f"\nAnalyse de la bande {direction}{i + 1} (travées: {spans} m)...")
            moments = analyze_by_forfaitaire(spans, w_u)
            all_moments[f"Bande_{direction}{i + 1}"] = {
                "max_moment_pos_kNm": max(moments["travees"], default=0),
                "max_moment_neg_kNm": abs(min(moments["appuis"], default=0)),
            }
    return all_moments


def calculate_radier_interactive():
    """Orchestre le dimensionnement et les vérifications d'un radier."""
    afficher_action("=== MODULE: DIMENSIONNEMENT D'UN RADIER GÉNÉRAL ===")
    radier_data = get_radier_inputs()
    if not radier_data:
        return
    beton, acier = define_materials()
    radier_data["beton"] = beton
    radier_data["acier"] = acier
    afficher_action("--- Vérification ELS : Tassements ---")
    sigma_sol_ser = check_soil_bearing_pressure(
        radier_data["poteaux_df"]["P_ser_kN"].sum(), radier_data["dimensions_plan"]
    )
    sigma_sol_adm = radier_data.get("sigma_sol_adm", 150.0)
    if sigma_sol_ser <= sigma_sol_adm:
        afficher_resultat(
            f"-> VÉRIFICATION OK ({sigma_sol_ser:.2f} kPa <= {sigma_sol_adm:.2f} kPa)"
        )
    else:
        afficher_erreur(
            f"-> AVERTISSEMENT : NON CONFORME ({sigma_sol_ser:.2f} kPa > {sigma_sol_adm:.2f} kPa). Augmentez les dimensions."
        )
        cont = poser_question("Continuer malgré tout ? (o/n)", choices=["o", "n"], default="n")
        if cont != "o":
            return
    all_moments = analyze_strips_interactively(radier_data)
    if all_moments:
        afficher_resultat("--- Récapitulatif des Moments Maximaux Calculés ---")
        for bande, results in all_moments.items():
            afficher_resultat(
                f"  - {bande}: M_pos = {results['max_moment_pos_kNm']:.2f} kNm, M_neg = {results['max_moment_neg_kNm']:.2f} kNm"
            )
    afficher_action("--- Étape 3 : Calcul du Ferraillage ---")
    afficher_resultat("(Fonctionnalité en cours de développement)")
    afficher_action("--- Étape 4 : Vérification au Poinçonnement ---")
    afficher_resultat("(Fonctionnalité en cours de développement)")
    poser_question("\nCalcul du radier terminé. Appuyez sur Entrée...")


# ==============================================================================
# SECTION 4 : MENUS DE NAVIGATION
# ==============================================================================
def calculate_beam():
    afficher_action("--- Module poutre (en développement) ---")
    poser_question("Appuyez sur Entrée...")


def menu_poteau():
    while True:
        options = {
            "1": "Mode Interactif",
            "2": "Mode par Lot (CSV)",
            "0": "Retour",
        }
        choice = afficher_menu_et_choisir("--- Menu : Calcul des Poteaux ---", options)

        if choice == "1":
            calculate_column_interactive()
        elif choice == "2":
            calculate_columns_batch()
        elif choice == "0":
            break
        else:
            afficher_erreur("Choix invalide.")


def start_ba_module():
    """Gère le menu principal du module Béton Armé."""
    while True:
        options = {
            "1": "Poteau Rectangulaire",
            "2": "Radier Général",
            "3": "Poutre (à venir)",
            "0": "Retour au menu principal",
        }
        choice = afficher_menu_et_choisir("--- Domaine : Béton Armé ---", options)

        if choice == "1":
            menu_poteau()
        elif choice == "2":
            calculate_radier_interactive()
        elif choice == "3":
            calculate_beam()
        elif choice == "0":
            break
        else:
            afficher_erreur("Choix invalide.")
