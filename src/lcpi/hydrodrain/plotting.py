# plotting.py
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# Ajout du chemin racine pour permettre l'import de 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from .utils.ui import print_colored


def generer_graphiques(df_results: pd.DataFrame, df_input: pd.DataFrame):
    """Génère et sauvegarde un ensemble de graphiques d'analyse à partir des résultats."""

    # Création des dossiers de sortie
    repports_dir = "repports"
    graphics_dir = os.path.join(repports_dir, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    print_colored("\n--- Génération des graphiques d'analyse ---", "cyan")
    try:
        # On ne garde que les tronçons qui ont été calculés avec succès (statut contenant 'OK')
        df_ok = df_results[df_results["statut"].str.contains("OK", na=False)].copy()

        if df_ok.empty:
            print_colored(
                "  ! Aucun tronçon n'a pu être dimensionné. Impossible de générer les graphiques.",
                "yellow",
            )
            return

        # S'assurer que les colonnes numériques sont bien de type numérique
        cols_to_convert = [
            "diametre_retenu_mm",
            "hauteur_retenue_m",
            "surface_cumulee",
            "q_max_m3s",
            "tc_final_min",
        ]
        for col in cols_to_convert:
            if col in df_ok.columns:
                df_ok[col] = pd.to_numeric(df_ok[col], errors="coerce")
        df_ok.dropna(subset=cols_to_convert, inplace=True, how="any")

        # --- Graphique 1 : Distribution des dimensions par type ---
        plt.figure(figsize=(18, 6))
        plt.suptitle(
            "Distribution des Dimensions par Type de Section", fontsize=16, y=1.02
        )

        # Sous-graphique pour les sections circulaires
        ax1 = plt.subplot(1, 3, 1)
        df_circ = df_ok[df_ok["type_section"] == "circulaire"]
        if not df_circ.empty:
            df_circ["diametre_retenu_mm"].value_counts().sort_index().plot(
                kind="bar", ax=ax1, color="skyblue", edgecolor="black"
            )
        ax1.set_title("Circulaire")
        ax1.set_xlabel("Diamètre (mm)")
        ax1.set_ylabel("Nombre de Tronçons")
        ax1.tick_params(axis="x", rotation=45)
        ax1.grid(axis="y", linestyle="--", alpha=0.7)

        # Sous-graphique pour les sections trapézoïdales
        ax2 = plt.subplot(1, 3, 2)
        df_trap = df_ok[df_ok["type_section"] == "trapezoidal"]
        if not df_trap.empty:
            df_trap["hauteur_retenue_m"].value_counts().sort_index().plot(
                kind="bar", ax=ax2, color="lightgreen", edgecolor="black"
            )
        ax2.set_title("Trapézoïdal")
        ax2.set_xlabel("Hauteur (m)")
        ax2.tick_params(axis="x", rotation=45)
        ax2.grid(axis="y", linestyle="--", alpha=0.7)

        # Sous-graphique pour les sections rectangulaires
        ax3 = plt.subplot(1, 3, 3)
        df_rect = df_ok[df_ok["type_section"] == "rectangulaire"]
        if not df_rect.empty:
            df_rect["hauteur_retenue_m"].value_counts().sort_index().plot(
                kind="bar", ax=ax3, color="salmon", edgecolor="black"
            )
        ax3.set_title("Rectangulaire")
        ax3.set_xlabel("Hauteur (m)")
        ax3.tick_params(axis="x", rotation=45)
        ax3.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(os.path.join(graphics_dir, "resultats_dimensions.png"))
        plt.close()
        print_colored("  - Graphique 'resultats_dimensions.png' sauvegardé.", "green")

        # --- Graphique 2 : Débit de Pointe vs. Surface Cumulée ---
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(
            df_ok["surface_cumulee"],
            df_ok["q_max_m3s"],
            c=df_ok["diametre_retenu_mm"].fillna(0)
            + df_ok["hauteur_retenue_m"].fillna(0) * 1000,
            cmap="viridis",
            s=80,
            alpha=0.8,
            edgecolors="black",
        )
        plt.title("Débit de Pointe vs. Surface Cumulée", fontsize=16)
        plt.xlabel("Surface Cumulée (ha)")
        plt.ylabel("Débit de Pointe (m³/s)")
        cbar = plt.colorbar(scatter)
        cbar.set_label("Dimension (mm ou m*1000)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(graphics_dir, "resultats_surface_debit.png"))
        plt.close()
        print_colored(
            "  - Graphique 'resultats_surface_debit.png' sauvegardé.", "green"
        )

        # --- Graphique 3 : Débit de Pointe vs. Temps de Concentration ---
        plt.figure(figsize=(10, 6))
        scatter_tc = plt.scatter(
            df_ok["tc_final_min"],
            df_ok["q_max_m3s"],
            c=df_ok["surface_cumulee"],
            cmap="plasma",
            s=80,
            alpha=0.8,
            edgecolors="black",
        )
        plt.title("Débit de Pointe vs. Temps de Concentration", fontsize=16)
        plt.xlabel("Temps de Concentration Final (min)")
        plt.ylabel("Débit de Pointe (m³/s)")
        cbar_tc = plt.colorbar(scatter_tc)
        cbar_tc.set_label("Surface Cumulée (ha)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(graphics_dir, "resultats_tc_qmax.png"))
        plt.close()
        print_colored("  - Graphique 'resultats_tc_qmax.png' sauvegardé.", "green")

        # --- Graphique 4 : Profil en Long ---
        df_full = pd.merge(
            df_results,
            df_input[["id_troncon", "z_start", "z_end"]],
            on="id_troncon",
            how="left",
        )
        df_full.dropna(subset=["z_start", "z_end"], inplace=True)
        df_full["z_start"] = pd.to_numeric(df_full["z_start"], errors="coerce")
        df_full["z_end"] = pd.to_numeric(df_full["z_end"], errors="coerce")

        if (
            not df_full.empty
            and not (df_full["z_start"] == 0).all()
            and not (df_full["z_end"] == 0).all()
        ):
            plt.figure(figsize=(12, 6))
            # Cette logique simplifiée trace des segments mais ne gère pas les branches multiples.
            # C'est une approximation pour la visualisation.
            distance_cumulee = 0
            for index, row in df_full.iterrows():
                long_troncon = df_input[df_input["id_troncon"] == row["id_troncon"]][
                    "longueur_troncon_m"
                ].iloc[0]
                plt.plot(
                    [distance_cumulee, distance_cumulee + long_troncon],
                    [row["z_start"], row["z_end"]],
                    marker="o",
                    linestyle="-",
                    color="b",
                )
                distance_cumulee += long_troncon

            plt.title("Profil en Long (Simplifié - Ordre de traitement)")
            plt.xlabel("Distance Cumulée (m)")
            plt.ylabel("Altitude Radier (m)")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(graphics_dir, "resultats_profil_long.png"))
            plt.close()
            print_colored(
                "  - Graphique 'resultats_profil_long.png' sauvegardé.", "green"
            )
        else:
            print_colored(
                "  - Données d'altitude insuffisantes pour générer le profil en long.",
                "yellow",
            )

    except Exception as e:
        print_colored(f"Erreur lors de la génération des graphiques : {e}", "red")
