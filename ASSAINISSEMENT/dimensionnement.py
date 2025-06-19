import math
import pandas as pd
import os

# ==============================================================================
# PROGRAMME PÉDAGOGIQUE DE DIMENSIONNEMENT PLUVIAL (AVEC CHEF D'ORCHESTRE)
# Version : CORRIGÉE - Gestion des paramètres globaux en mode batch
# ==============================================================================

# --- Constantes de conception ---
DIAMETRES_COMMERCIAUX_m = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 1.20, 1.50]
MAX_ITERATIONS = 10
TOLERANCE_TC_min = 0.1

# --- Fonctions de calcul (inchangées) ---
def print_colored(text, color="yellow"):
    colors = {"yellow": "\033[93m", "green": "\033[92m", "cyan": "\033[96m", "red": "\033[91m", "bold": "\033[1m", "end": "\033[0m"}
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def calculer_intensite_montana(tc_min: float, a: float, b: float, verbose: bool):
    if verbose:
        print_colored("\n   -> Calcul de l'intensité de pluie (i) :")
        print("      Formule de Montana : i = a * tc^b")
        print(f"      Application numérique : i = {a} * {tc_min:.2f}^{b}")
    if tc_min <= 0: raise ValueError("Le temps de concentration doit être positif.")
    intensite = a * (tc_min ** b)
    if verbose: print(f"      Résultat : i = {intensite:.2f} mm/h")
    return intensite

def calculer_q_max(c: float, i_mmh: float, a_ha: float, verbose: bool):
    if verbose:
        print_colored("\n   -> Calcul du débit de pointe (Qmax) :")
        print("      Formule Rationnelle : Qmax = (C * i * A) / 360")
        print(f"      Application numérique : Qmax = ({c:.2f} * {i_mmh:.2f} * {a_ha:.2f}) / 360")
    q_max = (c * i_mmh * a_ha) / 360
    if verbose: print(f"      Résultat : Qmax = {q_max:.3f} m³/s")
    return q_max

def dimensionner_conduite(q_max_m3s: float, pente: float, ks: float, verbose: bool):
    if verbose:
        print_colored("\n   -> Dimensionnement hydraulique de la conduite :")
        print("      Objectif : Trouver le plus petit diamètre commercial (D) tel que Q_capacité >= Qmax.")
        print(f"      Qmax à évacuer = {q_max_m3s:.3f} m³/s")
    
    for diametre in DIAMETRES_COMMERCIAUX_m:
        section_pleine = math.pi * (diametre / 2) ** 2
        rayon_hydraulique_plein = diametre / 4
        if verbose:
            print(f"\n      Test du diamètre D = {int(diametre*1000)} mm...")
            print("      Formule de Manning-Strickler : Q_capacité = Ks * S * Rh^(2/3) * I^(1/2)")
            print(f"      Application numérique : Q_capacité = {ks} * {section_pleine:.3f} * {rayon_hydraulique_plein:.3f}^(2/3) * {pente}^(1/2)")
        
        q_capacite = ks * section_pleine * (rayon_hydraulique_plein ** (2/3)) * (pente ** 0.5)
        if verbose: print(f"      Résultat : Q_capacité = {q_capacite:.3f} m³/s")
        
        if q_capacite >= q_max_m3s:
            if verbose: print_colored("      Conclusion : Ce diamètre est suffisant.", "green")
            vitesse_pleine_section = q_capacite / section_pleine
            return diametre, q_capacite, vitesse_pleine_section
        elif verbose:
            print_colored("      Conclusion : Ce diamètre est insuffisant.", "red")
            
    raise ValueError(f"Débit trop élevé ({q_max_m3s:.3f} m³/s).")


# --- Coeur de la logique de calcul pour un tronçon ---
# ******** MODIFICATION 1 : La fonction accepte maintenant les paramètres globaux séparément ********
def dimensionner_un_troncon(params_troncon: dict, params_globaux: dict, verbose: bool = False) -> dict:
    tc_courant_min = params_troncon['tc_initial_min']
    
    for i in range(MAX_ITERATIONS):
        if verbose: print_colored(f"\n--- Itération n°{i + 1} (tc = {tc_courant_min:.2f} min) ---", "bold")
        
        try:
            # ******** MODIFICATION 2 : Utilisation des paramètres globaux pour Montana ********
            intensite = calculer_intensite_montana(
                tc_courant_min, 
                params_globaux['montana_a'], 
                params_globaux['montana_b'], 
                verbose
            )
            q_max = calculer_q_max(
                params_troncon['coeff_ruissellement'], 
                intensite, 
                params_troncon['surface_ha'], 
                verbose
            )
            diametre, q_capacite, vitesse = dimensionner_conduite(
                q_max, 
                params_troncon['pente_troncon'], 
                params_troncon['ks_manning_strickler'], 
                verbose
            )
        except ValueError as e:
            return {'id_troncon': params_troncon.get('id_troncon', 'N/A'), 'statut': f"Erreur: {e}"}

        temps_parcours_min = (params_troncon['longueur_troncon_m'] / vitesse) / 60
        tc_nouveau_min = params_troncon['tc_initial_min'] + temps_parcours_min
        
        if verbose: print_colored(f"\n   -> Recalcul du tc: nouveau tc = {tc_nouveau_min:.2f} min", "yellow")
        
        if abs(tc_nouveau_min - tc_courant_min) < TOLERANCE_TC_min:
            if verbose: print_colored("\n>>> CONVERGENCE ATTEINTE !", "green")
            break
        tc_courant_min = tc_nouveau_min
    else:
        if verbose: print_colored("\n>>> ATTENTION : Convergence non atteinte.", "red")

    return {
        'id_troncon': params_troncon.get('id_troncon', 'N/A'),
        'tc_final_min': round(tc_courant_min, 2),
        'q_max_m3s': round(q_max, 3),
        'diametre_retenu_mm': int(diametre * 1000),
        'vitesse_ms': round(vitesse, 2),
        'statut': 'OK'
    }

# --- Fonctions pour les modes de fonctionnement ---
def get_input_with_default(prompt, default, type_converter=float):
    user_input = input(f"{prompt} [défaut: {default}] : ").strip().replace(',', '.')
    if user_input == "": return default
    try: return type_converter(user_input)
    except ValueError:
        print_colored(f"Entrée invalide. Utilisation de la valeur par défaut : {default}", "red")
        return default

def run_interactive_mode():
    params_troncon = {}
    params_globaux = {}
    print_colored("\n--- MODE INTERACTIF - DIMENSIONNEMENT D'UN TRONÇON ---", "cyan")
    
    # ... Saisie des données du tronçon ...
    print("\n--- 1. Caractéristiques du Sous-Bassin Versant ---")
    params_troncon['id_troncon'] = 'TR-INTERACTIF'
    params_troncon['surface_ha'] = get_input_with_default("Entrez la Surface (A) en hectares [ha]", 5.0)
    params_troncon['coeff_ruissellement'] = get_input_with_default("Entrez le Coefficient de ruissellement (C)", 0.6)
    params_troncon['tc_initial_min'] = get_input_with_default("Entrez le Temps de concentration de surface [min]", 10.0)
    
    print("\n--- 2. Caractéristiques du Tronçon à Dimensionner ---")
    params_troncon['longueur_troncon_m'] = get_input_with_default("Entrez la Longueur de la conduite [m]", 150.0)
    params_troncon['pente_troncon'] = get_input_with_default("Entrez la Pente de la conduite (ex: 0.02 pour 2%)", 0.02)
    params_troncon['ks_manning_strickler'] = get_input_with_default("Entrez le Coefficient (Ks) [Béton par défaut]", 67.0)

    # ... Saisie des données globales ...
    print("\n--- 3. Données Pluviométriques (Formule de Montana) ---")
    params_globaux['montana_a'] = get_input_with_default("Entrez le coefficient 'a'", 40.0)
    params_globaux['montana_b'] = get_input_with_default("Entrez le coefficient 'b' (négatif)", -0.85)

    resultats = dimensionner_un_troncon(params_troncon, params_globaux, verbose=True)
    
    print_colored("\n================ RAPPORT FINAL ================", "cyan")
    # ... Affichage des résultats ...
    if resultats.get('statut') == 'OK':
        for key, value in resultats.items():
            print(f"  - {key.replace('_', ' ').capitalize():<25} : {value}")
    else:
        print_colored(f"Le calcul a échoué : {resultats.get('statut', 'Erreur inconnue')}", "red")
    print_colored("===============================================", "cyan")

def run_batch_mode():
    print_colored("\n--- MODE BATCH - TRAITEMENT D'UN FICHIER CSV ---", "cyan")
    
    while True:
        csv_path = input("Entrez le chemin relatif de votre fichier CSV (ex: projet.csv) : ")
        if os.path.exists(csv_path): break
        else: print_colored("Fichier non trouvé.", "red")
    
    try:
        df_input = pd.read_csv(csv_path)
        required_cols = {'id_troncon', 'surface_ha', 'coeff_ruissellement', 'tc_initial_min', 'longueur_troncon_m', 'pente_troncon', 'ks_manning_strickler'}
        if not required_cols.issubset(df_input.columns):
            print_colored(f"Erreur: Le CSV doit contenir les colonnes : {required_cols}", "red")
            return
    except Exception as e:
        print_colored(f"Erreur de lecture du fichier CSV : {e}", "red")
        return
    
    params_globaux = {}
    print_colored("\n--- Paramètres Globaux pour le Traitement par Lot ---", "cyan")
    params_globaux['montana_a'] = get_input_with_default("Entrez le coefficient 'a' de Montana pour ce projet", 40.0)
    params_globaux['montana_b'] = get_input_with_default("Entrez le coefficient 'b' de Montana pour ce projet", -0.85)
    
    results_list = []
    
    if not df_input.empty:
        print_colored(f"\n--- Traitement détaillé du premier tronçon ({df_input.iloc[0]['id_troncon']}) ---", "bold")
        first_row_params = df_input.iloc[0].to_dict()
        # ******** MODIFICATION 3 : On passe les deux dictionnaires à la fonction ********
        results_list.append(dimensionner_un_troncon(first_row_params, params_globaux, verbose=True))
    
    if len(df_input) > 1:
        print_colored(f"\n--- Traitement rapide des {len(df_input) - 1} tronçons restants ---", "bold")
        for _, row in df_input.iloc[1:].iterrows():
            params_troncon = row.to_dict()
            result = dimensionner_un_troncon(params_troncon, params_globaux, verbose=False)
            results_list.append(result)
            print(f"  - Tronçon {params_troncon['id_troncon']}... traité.")

    print_colored("\n================ TABLEAU DE RÉSULTATS ================", "cyan")
    if not results_list: print("Aucun tronçon n'a été traité.")
    else:
        df_results = pd.DataFrame(results_list)
        pd.set_option('display.width', 120)
        print(df_results.to_string(index=False))
    print_colored("=======================================================", "cyan")

# --- Chef d'orchestre ---
def main():
    print_colored("==========================================================", "cyan")
    print_colored(" BIENVENUE DANS L'OUTIL DE DIMENSIONNEMENT PLUVIAL", "cyan")
    print_colored("==========================================================", "cyan")
    
    while True:
        mode = input("Choisissez un mode de fonctionnement [interactif / lot] : ").lower().strip()
        if mode in ["interactif", "i"]: run_interactive_mode(); break
        elif mode in ["lot", "l"]: run_batch_mode(); break
        else: print_colored("Mode non reconnu. Veuillez choisir 'interactif' ou 'lot'.", "red")

if __name__ == "__main__":
    main()