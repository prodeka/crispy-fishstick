# plotting.py
import matplotlib.pyplot as plt
import pandas as pd
import os # ***** IMPORTATION AJOUTÉE *****
from utils import print_colored

# ***** SIGNATURE DE LA FONCTION MISE À JOUR *****
def generer_graphiques(df_results: pd.DataFrame, df_input: pd.DataFrame):
    """Génère et sauvegarde des graphiques à partir des résultats."""
    
    # Création des dossiers de sortie
    repports_dir = 'repports'
    graphics_dir = os.path.join(repports_dir, 'graphics')
    os.makedirs(graphics_dir, exist_ok=True)
    
    print_colored("\n--- Génération des graphiques ---", "cyan")
    try:
        df_ok = df_results[df_results['statut'] == 'OK'].copy()
        if df_ok.empty:
            print("Aucun tronçon n'a pu être dimensionné, impossible de générer les graphiques.")
            return

        # S'assurer que les colonnes sont numériques
        for col in ['diametre_retenu_mm', 'hauteur_retenue_m', 'surface_cumulee', 'q_max_m3s', 'tc_final_min']:
            if col in df_ok.columns:
                df_ok[col] = pd.to_numeric(df_ok[col], errors='coerce')

        # --- Graphique 1 : Distribution des dimensions ---
        plt.figure(figsize=(18, 6))
        plt.suptitle('Distribution des Dimensions par Type de Section', fontsize=16, y=1.02)

        ax1 = plt.subplot(1, 3, 1)
        df_circ = df_ok[df_ok['diametre_retenu_mm'] > 0]
        if not df_circ.empty:
            df_circ['diametre_retenu_mm'].value_counts().sort_index().plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
        ax1.set_title('Circulaire'); ax1.set_xlabel('Diamètre (mm)'); ax1.set_ylabel('Nombre de Tronçons')
        ax1.tick_params(axis='x', rotation=45); ax1.grid(axis='y', linestyle='--', alpha=0.7)
        
        ax2 = plt.subplot(1, 3, 2)
        df_trap = df_ok[(df_ok['hauteur_retenue_m'] > 0) & (df_ok['type_section'] == 'trapezoidal')]
        if not df_trap.empty:
            df_trap['hauteur_retenue_m'].value_counts().sort_index().plot(kind='bar', ax=ax2, color='lightgreen', edgecolor='black')
        ax2.set_title('Trapézoïdal'); ax2.set_xlabel('Hauteur (m)'); ax2.set_ylabel('')
        ax2.tick_params(axis='x', rotation=45); ax2.grid(axis='y', linestyle='--', alpha=0.7)

        ax3 = plt.subplot(1, 3, 3)
        df_rect = df_ok[(df_ok['hauteur_retenue_m'] > 0) & (df_ok['type_section'] == 'rectangulaire')]
        if not df_rect.empty:
            df_rect['hauteur_retenue_m'].value_counts().sort_index().plot(kind='bar', ax=ax3, color='salmon', edgecolor='black')
        ax3.set_title('Rectangulaire'); ax3.set_xlabel('Hauteur (m)'); ax3.set_ylabel('')
        ax3.tick_params(axis='x', rotation=45); ax3.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(os.path.join(graphics_dir, 'resultats_dimensions.png'))
        print("  - Graphique 'resultats_dimensions.png' sauvegardé.")

        # --- Graphique 2 : Surface vs. Débit ---
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(df_ok['surface_cumulee'], df_ok['q_max_m3s'], c=df_ok['diametre_retenu_mm'] + df_ok['hauteur_retenue_m']*1000, cmap='viridis', s=100, alpha=0.8, edgecolors='black')
        plt.title('Débit de Pointe vs. Surface Cumulée', fontsize=16)
        plt.xlabel('Surface Cumulée (ha)'); plt.ylabel('Débit de Pointe (m³/s)')
        cbar = plt.colorbar(scatter); cbar.set_label('Dimension (mm ou m*1000)')
        plt.grid(True); plt.tight_layout()
        plt.savefig(os.path.join(graphics_dir, 'resultats_surface_debit.png'))
        print("  - Graphique 'resultats_surface_debit.png' sauvegardé.")

        # --- Graphique 3 : Tc vs. Qmax ---
        plt.figure(figsize=(10, 6))
        scatter_tc = plt.scatter(df_ok['tc_final_min'], df_ok['q_max_m3s'], c=df_ok['surface_cumulee'], cmap='plasma', s=100, alpha=0.8, edgecolors='black')
        plt.title('Débit de Pointe vs. Temps de Concentration', fontsize=16)
        plt.xlabel('Temps de Concentration Final (min)'); plt.ylabel('Débit de Pointe (m³/s)')
        cbar_tc = plt.colorbar(scatter_tc); cbar_tc.set_label('Surface Cumulée (ha)')
        plt.grid(True); plt.tight_layout()
        plt.savefig(os.path.join(graphics_dir, 'resultats_tc_qmax.png'))
        print("  - Graphique 'resultats_tc_qmax.png' sauvegardé.")

        # --- Graphique 4 : Profil en Long ---
        df_full = pd.merge(df_ok, df_input[['id_troncon', 'z_start', 'z_end', 'longueur_troncon_m']], on='id_troncon', how='left')
        if not df_full[['z_start', 'z_end']].isnull().values.any():
            plt.figure(figsize=(12, 6))
            distances_cumulees, altitudes = 0, [df_full.iloc[0]['z_start']]
            distances = [0]
            for _, row in df_full.iterrows():
                distances_cumulees += row['longueur_troncon_m']
                distances.append(distances_cumulees)
                altitudes.append(row['z_end'])
            plt.plot(distances, altitudes, marker='o', linestyle='-', color='b')
            plt.title('Profil en Long (Simplifié - Ordre de traitement)'); plt.xlabel('Distance Cumulée (m)'); plt.ylabel('Altitude Radier (m)')
            plt.grid(True); plt.tight_layout()
            plt.savefig(os.path.join(graphics_dir, 'resultats_profil_long.png'))
            print("  - Graphique 'resultats_profil_long.png' sauvegardé.")
        
        plt.show() # Affiche tous les graphiques
    except Exception as e:
        print_colored(f"Erreur lors de la génération des graphiques : {e}", "red")