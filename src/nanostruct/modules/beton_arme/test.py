import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


# Votre excellente classe pour structurer les données
class Forme:
    def __init__(self, pos, armature, code, longueur, quantite=1, espacement=0):
        self.pos = pos
        self.armature = armature
        self.code = code
        self.longueur = longueur
        self.quantite = quantite
        self.espacement = espacement


# --- FONCTIONS DE DESSIN (basées sur les vôtres) ---


def dessiner_section(ax, largeur, hauteur, enrobage, aciers):
    """Dessine la section transversale du poteau."""
    ax.set_aspect("equal")
    ax.set_title("Section A-A")

    # Contour du poteau
    contour_poteau = patches.Rectangle(
        (0, 0), largeur, hauteur, linewidth=2, edgecolor="black", facecolor="lightgray"
    )
    ax.add_patch(contour_poteau)

    # Cadre (Pos 2)
    largeur_cadre = largeur - 2 * enrobage
    hauteur_cadre = hauteur - 2 * enrobage
    # <<< MODIFICATION : Utilisation de FancyBboxPatch pour les coins arrondis >>>
    rayon_cintrage = 4
    cadre = patches.FancyBboxPatch(
        (enrobage, enrobage),
        largeur_cadre,
        hauteur_cadre,
        boxstyle=f"round,pad=0,rounding_size={rayon_cintrage}",
        linewidth=1.5,
        edgecolor="black",
        facecolor="none",
    )
    ax.add_patch(cadre)

    # <<< AJOUT : Crochet du cadre à 135 degrés >>>
    longueur_crochet = 6
    ax.plot(
        [
            enrobage + rayon_cintrage,
            enrobage + rayon_cintrage - longueur_crochet * np.cos(np.deg2rad(45)),
        ],
        [
            hauteur - enrobage,
            hauteur - enrobage + longueur_crochet * np.sin(np.deg2rad(45)),
        ],
        color="black",
        linewidth=1.5,
    )

    # Barres longitudinales (Pos 1)
    diametre_barre = 1.2  # HA12
    positions_aciers = [
        (enrobage, enrobage),
        (largeur / 2, enrobage),
        (largeur - enrobage, enrobage),
        (enrobage, hauteur / 2),
        (largeur - enrobage, hauteur / 2),
        (enrobage, hauteur - enrobage),
        (largeur / 2, hauteur - enrobage),
        (largeur - enrobage, hauteur - enrobage),
    ]
    for x, y in positions_aciers:
        cercle = patches.Circle((x, y), radius=diametre_barre / 2, color="black")
        ax.add_patch(cercle)

    # <<< AJOUT : Épingle (Pos 3) >>>
    ax.plot(
        [enrobage, largeur - enrobage],
        [hauteur / 2, hauteur / 2],
        color="black",
        linewidth=1.5,
    )
    # Crochets de l'épingle
    ax.plot(
        [enrobage, enrobage + longueur_crochet / 2],
        [hauteur / 2, hauteur / 2 + longueur_crochet / 2],
        color="black",
        linewidth=1.5,
    )
    ax.plot(
        [largeur - enrobage, largeur - enrobage - longueur_crochet / 2],
        [hauteur / 2, hauteur / 2 + longueur_crochet / 2],
        color="black",
        linewidth=1.5,
    )

    # Dimensions
    ax.plot([-5, largeur + 5], [-10, -10], color="black", lw=0.8)
    ax.text(largeur / 2, -12, str(largeur), ha="center", va="top")
    ax.plot([-10, -10], [-5, hauteur + 5], color="black", lw=0.8)
    ax.text(-12, hauteur / 2, str(hauteur), ha="right", va="center", rotation=90)

    ax.set_xlim(-20, largeur + 20)
    ax.set_ylim(-20, hauteur + 20)
    ax.axis("off")


def dessiner_elevation(ax, largeur, hauteur_totale, forme_cadres):
    """Dessine la vue en élévation du poteau."""
    ax.set_title("Élévation")
    ax.set_aspect("equal")

    # Contours du poteau
    ax.plot([0, 0], [0, hauteur_totale], color="black", lw=2)
    ax.plot([largeur, largeur], [0, hauteur_totale], color="black", lw=2)

    # Cadres (étriers)
    hauteur_aciers = 565  # Hauteur sur laquelle les cadres sont répartis
    y_debut_cadres = (hauteur_totale - hauteur_aciers) / 2
    positions_y = np.linspace(
        y_debut_cadres, y_debut_cadres + hauteur_aciers, forme_cadres.quantite
    )
    for y in positions_y:
        ax.plot([0, largeur], [y, y], color="black", lw=1)

    # <<< AJOUT : Lignes de cote >>>
    # Cote totale
    ax.plot([largeur + 20, largeur + 20], [0, hauteur_totale], color="black", lw=0.8)
    ax.plot([largeur + 18, largeur + 22], [0, 0], color="black", lw=0.8)
    ax.plot(
        [largeur + 18, largeur + 22],
        [hauteur_totale, hauteur_totale],
        color="black",
        lw=0.8,
    )
    ax.text(
        largeur + 25,
        hauteur_totale / 2,
        f"{hauteur_totale / 100:.2f}",
        ha="left",
        va="center",
        rotation=90,
        fontsize=10,
    )

    # Cote répartition cadres
    ax.plot(
        [largeur + 10, largeur + 10],
        [y_debut_cadres, y_debut_cadres + hauteur_aciers],
        color="black",
        lw=0.8,
    )
    ax.plot(
        [largeur + 8, largeur + 12],
        [y_debut_cadres, y_debut_cadres],
        color="black",
        lw=0.8,
    )
    ax.plot(
        [largeur + 8, largeur + 12],
        [y_debut_cadres + hauteur_aciers, y_debut_cadres + hauteur_aciers],
        color="black",
        lw=0.8,
    )
    ax.text(
        largeur + 15,
        hauteur_totale / 2,
        f"{hauteur_aciers / 100:.2f}",
        ha="left",
        va="center",
        rotation=90,
        fontsize=10,
    )
    ax.text(
        largeur + 15,
        hauteur_totale / 2 + 60,
        f"{forme_cadres.quantite}x{forme_cadres.espacement}",
        ha="left",
        va="center",
        rotation=90,
        fontsize=9,
    )

    ax.set_xlim(-10, largeur + 40)
    ax.set_ylim(-20, hauteur_totale + 20)
    ax.axis("off")


def dessiner_tableau(ax, formes):
    """Crée le tableau récapitulatif des armatures."""
    ax.set_title("Tableau d'Armatures")
    cell_text = [["Pos.", "Armature", "Code", "Forme", "L (cm)"]]
    # J'ai ajouté un champ "description" pour plus de clarté dans le tableau final
    forme_descriptions = {"00": "Droite", "31": "Cadre", "custom_pin": "Épingle"}

    for f in formes:
        # On déduit la forme à partir du code, comme sur le plan
        desc = forme_descriptions.get(f.code, "N/A")
        if f.pos == 3:
            desc = "Épingle"  # Cas particulier pour l'épingle
        cell_text.append([f.pos, f.armature, f.code, desc, f"{f.longueur:.2f}"])

    table = ax.table(cellText=cell_text, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    ax.axis("off")


# --- SCRIPT PRINCIPAL ---
if __name__ == "__main__":
    # Définition des dimensions et propriétés
    largeur_poteau = 40
    hauteur_poteau = 40
    hauteur_totale_poteau = 620
    enrobage = 3.0

    # Création des objets pour chaque armature en utilisant votre classe
    forme1 = Forme(pos=1, armature="8 HA 12", code="00", longueur=617)
    forme2 = Forme(
        pos=2, armature="34 HA 8", code="31", longueur=152, quantite=34, espacement=18
    )
    forme3 = Forme(pos=3, armature="34 HA 8", code="00", longueur=48)

    formes = [forme1, forme2, forme3]

    # Création de la figure et des axes
    fig, ((ax_section, ax_elevation), (ax_table, ax_empty)) = plt.subplots(
        2, 2, figsize=(12, 10), gridspec_kw={"width_ratios": [1, 1.5]}
    )
    ax_empty.axis("off")  # On cache l'axe vide

    # Appel des fonctions de dessin
    dessiner_section(ax_section, largeur_poteau, hauteur_poteau, enrobage, formes)
    dessiner_elevation(ax_elevation, largeur_poteau, hauteur_totale_poteau, forme2)
    dessiner_tableau(ax_table, formes)

    # Titre général et affichage
    fig.suptitle("Visualisation d'un Poteau en Béton Armé", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
