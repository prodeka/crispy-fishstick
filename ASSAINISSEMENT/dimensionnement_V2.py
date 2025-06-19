import sys
import subprocess
import importlib.util

# ==============================================================================
# SECTION 0 : BOOTSTRAP - VÉRIFICATION ET INSTALLATION DES DÉPENDANCES
# ==============================================================================
def check_and_install_packages(packages):
    print("Vérification des dépendances requises...")
    all_installed = True
    for package in packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            print(f"La bibliothèque '{package}' est manquante.")
            all_installed = False
            
    if not all_installed:
        print("Tentative d'installation des paquets manquants avec pip...")
        for package in packages:
            if importlib.util.find_spec(package) is None:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                except subprocess.CalledProcessError:
                    print(f"\nERREUR CRITIQUE : Impossible d'installer '{package}'.")
                    print(f"Veuillez l'installer manuellement avec la commande : pip install {package}")
                    sys.exit(1)
        print("Toutes les dépendances sont maintenant installées.")
    else:
        print("Toutes les dépendances sont déjà présentes.")

required_packages = ['pandas', 'matplotlib']
check_and_install_packages(required_packages)

# Les importations sont faites APRÈS la vérification
import math
import pandas as pd
import os
import matplotlib.pyplot as plt

# ==============================================================================
# PROGRAMME AVANCÉ DE DIMENSIONNEMENT DE RÉSEAU PLUVIAL
# Version : CORRIGÉE - Barre de progression remplacée
# ==============================================================================

# --- Constantes et Paramètres Globaux ---
DIAMETRES_COMMERCIAUX_m = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 1.20, 1.50]
MAX_ITERATIONS = 10
TOLERANCE_TC_min = 0.1
MONTANA_A = 40.0
MONTANA_B = -0.85

# --- Fonctions Utilitaires et de Calcul (inchangées) ---
def print_colored(text, color="yellow"):
    colors = {"yellow": "\033[93m", "green": "\033[92m", "cyan": "\033[96m", "red": "\033[91m", "bold": "\033[1m", "end": "\033[0m"}
    if 'NO_COLOR' in os.environ or sys.platform == 'win32' and 'TERM' not in os.environ:
        print(text)
    else:
        print(f"{colors.get(color, '')}{text}{colors['end']}")

def tc_kirpich(longueur_m, pente):
    H = longueur_m * pente
    if H <= 0: return 5.0
    return 0.01947 * (longueur_m**0.77) * ((H/longueur_m)**-0.385)

def tc_californienne(longueur_m, pente):
    longueur_km = longueur_m / 1000
    if pente <= 0: return 5.0
    return 0.0663 * ((longueur_km / math.sqrt(pente))**0.77) * 60

def calculer_intensite_montana(tc_min, a, b):
    return a * (tc_min ** b)

def calculer_q_max(c, i_mmh, a_ha):
    return (c * i_mmh * a_ha) / 360

def dimensionner_conduite(q_max_m3s, pente, ks):
    for diametre in DIAMETRES_COMMERCIAUX_m:
        section_pleine = math.pi * (diametre / 2) ** 2
        rayon_hydraulique_plein = diametre / 4
        q_capacite = ks * section_pleine * (rayon_hydraulique_plein ** (2/3)) * (pente ** 0.5)
        if q_capacite >= q_max_m3s:
            vitesse_pleine_section = q_capacite / section_pleine
            return diametre, q_capacite, vitesse_pleine_section
    raise ValueError(f"Débit trop élevé ({q_max_m3s:.3f} m³/s).")

# --- Coeur de la logique de calcul ---
def dimensionner_reseau(df_input: pd.DataFrame, tc_formule_name: str) -> pd.DataFrame:
    sorted_troncons = []
    processed_ids = set()
    df_input['troncon_amont'] = df_input['troncon_amont'].fillna('NONE')

    while len(sorted_troncons) < len(df_input):
        found_new = False
        for index, row in df_input.iterrows():
            if row['id_troncon'] in processed_ids:
                continue
            
            amont_ids = str(row['troncon_amont']).split(';')
            if amont_ids == ['NONE'] or all(am_id in processed_ids for am_id in amont_ids):
                sorted_troncons.append(row)
                processed_ids.add(row['id_troncon'])
                found_new = True
        
        if not found_new:
            raise Exception("Erreur de topologie dans le CSV : boucle détectée ou tronçon amont non défini.")

    df_sorted = pd.DataFrame(sorted_troncons)
    results_data = {}

    print_colored(f"\n--- Lancement du dimensionnement du réseau ({len(df_sorted)} tronçons) ---", "bold")
    
    # ******** LA CORRECTION EST ICI : Remplacement de la barre de progression 'click' ********
    total_troncons = len(df_sorted)
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        params_troncon = row.to_dict()
        print_colored(f"\n({i+1}/{total_troncons}) Traitement du tronçon : {params_troncon['id_troncon']}", "bold")
            
        if tc_formule_name == 'kirpich':
            tc_surface = tc_kirpich(params_troncon['longueur_parcours_surface_m'], params_troncon['pente_parcours_surface'])
        else:
            tc_surface = tc_californienne(params_troncon['longueur_parcours_surface_m'], params_troncon['pente_parcours_surface'])
            
        amont_ids = str(params_troncon['troncon_amont']).split(';')
        if amont_ids == ['NONE']:
            surface_totale = params_troncon['surface_ha']
            coeff_c_moyen = params_troncon['coeff_ruissellement']
            tc_amont_max = 0
        else:
            try:
                surfaces_amont = [results_data[am_id]['surface_cumulee'] for am_id in amont_ids]
                c_pondere_amont = [results_data[am_id]['c_moyen_cumule'] * results_data[am_id]['surface_cumulee'] for am_id in amont_ids]
                surface_totale = params_troncon['surface_ha'] + sum(surfaces_amont)
                c_pondere_total = (params_troncon['coeff_ruissellement'] * params_troncon['surface_ha']) + sum(c_pondere_amont)
                coeff_c_moyen = c_pondere_total / surface_totale
                tc_amont_max = max(results_data[am_id]['tc_final_min'] for am_id in amont_ids)
            except KeyError as e:
                raise Exception(f"Erreur de topologie : le tronçon amont {e} n'a pas été trouvé ou traité avant son dépendant.")


        tc_courant_min = max(tc_surface, tc_amont_max)
        
        # Initialisation des variables pour le cas où la boucle ne s'exécute pas
        q_max, diametre, vitesse = 0, 0, 0 
        
        for it_num in range(MAX_ITERATIONS):
            try:
                intensite = calculer_intensite_montana(tc_courant_min, MONTANA_A, MONTANA_B)
                q_max = calculer_q_max(coeff_c_moyen, intensite, surface_totale)
                diametre, q_capacite, vitesse = dimensionner_conduite(q_max, params_troncon['pente_troncon'], params_troncon['ks_manning_strickler'])
            except ValueError as e:
                results_data[params_troncon['id_troncon']] = {'statut': f"Erreur: {e}"}
                break

            temps_parcours_min = (params_troncon['longueur_troncon_m'] / vitesse) / 60
            tc_nouveau_min = tc_amont_max + temps_parcours_min
            
            if abs(tc_nouveau_min - tc_courant_min) < TOLERANCE_TC_min:
                break
            tc_courant_min = tc_nouveau_min
        
        # Assurer que les résultats sont stockés même en cas d'erreur dans la boucle
        if 'statut' not in results_data.get(params_troncon['id_troncon'], {}):
            results_data[params_troncon['id_troncon']] = {
                'id_troncon': params_troncon['id_troncon'],
                'surface_cumulee': round(surface_totale, 2),
                'c_moyen_cumule': round(coeff_c_moyen, 2),
                'tc_final_min': round(tc_courant_min, 2),
                'q_max_m3s': round(q_max, 3),
                'diametre_retenu_mm': int(diametre * 1000),
                'vitesse_ms': round(vitesse, 2),
                'statut': 'OK'
            }

    return pd.DataFrame(list(results_data.values()))


# --- Fonctions graphiques ---
def generer_graphiques(df_results: pd.DataFrame):
    print_colored("\n--- Génération des graphiques ---", "cyan")
    try:
        df_ok = df_results[df_results['statut'] == 'OK'].copy()
        if df_ok.empty:
            print("Aucun tronçon n'a pu être dimensionné, impossible de générer les graphiques.")
            return

        df_ok['diametre_retenu_mm'] = pd.to_numeric(df_ok['diametre_retenu_mm'])
        df_ok['surface_cumulee'] = pd.to_numeric(df_ok['surface_cumulee'])
        df_ok['q_max_m3s'] = pd.to_numeric(df_ok['q_max_m3s'])

        plt.figure(figsize=(10, 6))
        df_ok['diametre_retenu_mm'].value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title('Distribution des Diamètres de Conduites Retenus', fontsize=16)
        plt.xlabel('Diamètre (mm)', fontsize=12)
        plt.ylabel('Nombre de Tronçons', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('resultats_diametres.png')
        print("  - Graphique 'resultats_diametres.png' sauvegardé.")

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(df_ok['surface_cumulee'], df_ok['q_max_m3s'], c=df_ok['diametre_retenu_mm'], cmap='viridis', s=100, alpha=0.8, edgecolors='black')
        plt.title('Débit de Pointe en fonction de la Surface Cumulée', fontsize=16)
        plt.xlabel('Surface Cumulée (ha)', fontsize=12)
        plt.ylabel('Débit de Pointe (m³/s)', fontsize=12)
        cbar = plt.colorbar(scatter)
        cbar.set_label('Diamètre Retenu (mm)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig('resultats_surface_debit.png')
        print("  - Graphique 'resultats_surface_debit.png' sauvegardé.")
        
        plt.show()
    except Exception as e:
        print_colored(f"Une erreur est survenue lors de la génération des graphiques : {e}", "red")

# --- Chef d'orchestre ---
def main():
    print_colored("==========================================================", "cyan")
    print_colored(" BIENVENUE DANS L'OUTIL DE DIMENSIONNEMENT AVANCÉ", "cyan")
    print_colored("==========================================================", "cyan")

    while True:
        csv_path = input("Entrez le chemin relatif de votre fichier CSV de réseau (ex: projet_reseau.csv) : ")
        if os.path.exists(csv_path): break
        else: print_colored("Fichier non trouvé.", "red")
    
    while True:
        tc_formule_name = input("Choisissez la formule pour le tc de surface [kirpich / californienne] : ").lower().strip()
        if tc_formule_name in ["kirpich", "californienne"]: break
        else: print_colored("Choix non valide.", "red")
        
    try:
        df_input = pd.read_csv(csv_path)
        required_cols = {'id_troncon', 'surface_ha', 'coeff_ruissellement', 'longueur_parcours_surface_m', 'pente_parcours_surface', 'longueur_troncon_m', 'pente_troncon', 'ks_manning_strickler', 'troncon_amont'}
        if not required_cols.issubset(df_input.columns):
            print_colored(f"Erreur: Le CSV doit contenir les colonnes : {required_cols}", "red")
            return
        
        df_results = dimensionner_reseau(df_input, tc_formule_name)

        print_colored("\n================ TABLEAU DE RÉSULTATS ================", "cyan")
        if df_results.empty:
            print("Aucun tronçon n'a été traité.")
        else:
            pd.set_option('display.width', 120)
            print(df_results.to_string(index=False))
            generer_graphiques(df_results)
        print_colored("=======================================================", "cyan")

    except Exception as e:
        print_colored(f"\nUne erreur critique est survenue : {e}", "red")

if __name__ == "__main__":
    main()