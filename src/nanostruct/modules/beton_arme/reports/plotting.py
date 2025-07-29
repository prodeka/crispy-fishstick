# PROJET_DIMENTIONEMENT/BA/reports/plotting.py
# Version "Expert" finale avec une structure de fonctions corrigée et robuste.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import math
import numpy as np

# ==============================================================================
# SECTION 1 : FONCTIONS AUXILIAIRES DE DESSIN ET DE POSITIONNEMENT
# ==============================================================================


def _get_bar_positions(b, h, enrobage, num_bars):
    """
    Calcule des positions symétriques et réalistes pour les barres.
    """
    if num_bars < 4:
        return [], []

    positions = set()
    # 1. Placer les 4 barres de coin
    positions.add((enrobage, enrobage))
    positions.add((b - enrobage, enrobage))
    positions.add((enrobage, h - enrobage))
    positions.add((b - enrobage, h - enrobage))

    bars_to_place = num_bars - 4
    if bars_to_place == 0:
        return sorted(list(positions)), []

    # 2. Répartir les barres restantes sur les faces
    if b >= h:
        num_top_bottom = math.ceil(bars_to_place / 2)
        num_left_right = bars_to_place - num_top_bottom
    else:
        num_left_right = math.ceil(bars_to_place / 2)
        num_top_bottom = bars_to_place - num_left_right

    intermediate_positions = set()
    for i in range(1, num_top_bottom + 1):
        x = enrobage + (b - 2 * enrobage) * i / (num_top_bottom + 1)
        intermediate_positions.add((x, enrobage))
        intermediate_positions.add((x, h - enrobage))

    for i in range(1, num_left_right + 1):
        y = enrobage + (h - 2 * enrobage) * i / (num_left_right + 1)
        intermediate_positions.add((enrobage, y))
        intermediate_positions.add((b - enrobage, y))

    positions.update(intermediate_positions)
    return sorted(list(positions)), sorted(list(intermediate_positions))


def _draw_callout(ax, target_pos, label_pos, label_text):
    """Dessine un repère (ligne, cercle, numéro)."""
    ax.plot(
        [target_pos[0], label_pos[0]],
        [target_pos[1], label_pos[1]],
        "k-",
        lw=0.8,
        zorder=40,
    )
    circle = patches.Circle(
        label_pos, radius=2.5, facecolor="white", edgecolor="black", lw=1, zorder=50
    )
    ax.add_patch(circle)
    ax.text(
        label_pos[0],
        label_pos[1],
        label_text,
        ha="center",
        va="center",
        fontsize=8,
        weight="bold",
        zorder=51,
    )


def _draw_section_view(ax, results):
    """Dessine la vue en coupe technique avec repères."""
    b = results["section"].b * 100
    h = results["section"].h * 100
    enrobage = results.get("enrobage_cm", 3)
    ax.set_title("Coupe A-A", fontsize=10, weight="bold")
    ax.set_aspect("equal")

    ax.add_patch(patches.Rectangle((0, 0), b, h, lw=1.5, ec="black", fc="#F0F0F0"))
    ax.add_patch(
        patches.Rectangle(
            (enrobage, enrobage),
            b - 2 * enrobage,
            h - 2 * enrobage,
            fill=False,
            ec="black",
            lw=1,
            zorder=2,
        )
    )

    bar_groups = results.get("bar_groups", [])
    total_bars = sum(g["qty"] for g in bar_groups)
    all_positions, _ = _get_bar_positions(b, h, enrobage, total_bars)

    pos_idx = 0
    for group in bar_groups:
        diam_cm = group["diam"] / 10
        for _ in range(group["qty"]):
            if pos_idx < len(all_positions):
                x, y = all_positions[pos_idx]
                ax.add_patch(
                    patches.Circle((x, y), radius=diam_cm / 2, fc="black", zorder=3)
                )
                pos_idx += 1
        ref_pos = all_positions[pos_idx - group["qty"]]
        _draw_callout(ax, ref_pos, (ref_pos[0] - 5, ref_pos[1] + 5), str(group["rep"]))

    ax.plot([0, b], [-5, -5], color="black", lw=0.8)
    ax.text(b / 2, -7, f"{b:.0f}", ha="center", va="top")
    ax.plot([-5, -5], [0, h], color="black", lw=0.8)
    ax.text(-7, h / 2, f"{h:.0f}", ha="right", va="center", rotation=90)

    ax.set_xlim(-15, b + 15)
    ax.set_ylim(-15, h + 15)
    ax.axis("off")


def _draw_elevation_view(ax, results):
    """Dessine la vue en élévation du poteau."""
    h_poteau = results["height_L_m"] * 100
    b_poteau = results["section"].b * 100
    enrobage = results.get("enrobage_cm", 3)
    espacement_cadres = results.get("max_transversal_spacing_cm", 20)
    num_cadres = int((h_poteau - 2 * enrobage) / espacement_cadres) + 1

    ax.add_patch(
        patches.Rectangle((0, 0), b_poteau, h_poteau, lw=1.5, ec="black", fc="none")
    )
    ax.vlines(
        x=[enrobage, b_poteau - enrobage],
        ymin=enrobage,
        ymax=h_poteau - enrobage,
        color="black",
        lw=0.8,
        ls="--",
    )
    y_stirrups = np.linspace(enrobage, h_poteau - enrobage, num_cadres)
    ax.hlines(
        y=y_stirrups, xmin=enrobage, xmax=b_poteau - enrobage, color="black", lw=0.8
    )

    ax.plot([b_poteau + 10, b_poteau + 10], [0, h_poteau], "gray", lw=0.7)
    ax.text(
        b_poteau + 12,
        h_poteau / 2,
        f"{h_poteau / 100:.2f}",
        ha="left",
        va="center",
        rotation=90,
        fontsize=9,
    )
    ax.text(
        b_poteau - 20,
        h_poteau / 2,
        f"{num_cadres - 1}x{espacement_cadres:.0f}",
        ha="center",
        va="center",
        rotation=90,
        fontsize=8,
    )

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_ylim(-10, h_poteau + 10)


def _draw_nomenclature_table(ax, results):
    """Dessine le tableau de nomenclature des aciers."""
    ax.axis("off")
    cell_text = [["Pos.", "Armature", "Code", "Forme"]]
    for group in results.get("bar_groups", []):
        cell_text.append(
            [str(group["rep"]), f"{group['qty']}xΦ{group['diam']}", "00", "Droite"]
        )
    cadre_diam = results.get("transversal_rebar_diameter", "N/A")
    cell_text.append(
        [
            str(len(results.get("bar_groups", [])) + 1),
            f"Cadres Φ{cadre_diam}",
            "31",
            "Cadre",
        ]
    )
    table = ax.table(
        cellText=cell_text,
        loc="center",
        cellLoc="center",
        colLabels=["Pos.", "Armature", "Code", "Forme"],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(weight="bold")


# ==============================================================================
# SECTION 2 : FONCTION PRINCIPALE DE DESSIN
# ==============================================================================


def plot_column_section(
    results, output_folder="output", filename="plan_ferraillage.png"
):
    """Génère une planche de ferraillage complète."""
    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.5], height_ratios=[1.5, 1])
    ax_elevation = fig.add_subplot(gs[:, 0])
    ax_section = fig.add_subplot(gs[0, 1])
    ax_table = fig.add_subplot(gs[1, 1])

    _draw_section_view(ax_section, results)
    _draw_elevation_view(ax_elevation, results)
    _draw_nomenclature_table(ax_table, results)

    fig.suptitle(
        f"Plan de Ferraillage - Poteau : {results.get('ID_Poteau', '')}",
        fontsize=16,
        weight="bold",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filepath = os.path.join(output_folder, filename)
    plt.savefig(filepath, dpi=200)
    plt.close()

    print(
        f"\n{'-' * 20}\nPlan de ferraillage complet sauvegardé dans : {filepath}\n{'-' * 20}"
    )
