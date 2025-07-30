# reporting.py
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    Frame,
    PageTemplate,
    NextPageTemplate,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.lib import colors
import pandas as pd
from datetime import datetime
import os
import re
import sys

# Ajout du chemin racine pour permettre l'import de 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from .utils.ui import print_colored


def clean_ansi_codes(text):
    """Supprime les séquences d'échappement ANSI (codes couleur) d'une chaîne de texte."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def build_report_story(
    project_info: dict, df_results: pd.DataFrame, verbose_log: str, is_comparison=False
):
    """Construit la liste des éléments (le "story") pour le rapport PDF."""
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="Title",
        fontSize=20,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    h1_style = ParagraphStyle(
        name="H1",
        fontSize=16,
        fontName="Helvetica-Bold",
        spaceBefore=20,
        spaceAfter=10,
        borderPadding=5,
        backColor=colors.HexColor("#E6E6E6"),
        leftIndent=-10,
        rightIndent=-10,
        paddingLeft=10,
    )
    h2_style = ParagraphStyle(
        name="H2",
        fontSize=12,
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.HexColor("#333333"),
    )
    h3_style = ParagraphStyle(
        name="H3",
        fontSize=10,
        fontName="Helvetica-Bold",
        spaceBefore=8,
        spaceAfter=4,
        leftIndent=10,
    )
    body_style = ParagraphStyle(
        name="Body", alignment=TA_JUSTIFY, spaceAfter=6, leading=14
    )
    code_style = ParagraphStyle(
        name="Code",
        fontName="Courier",
        fontSize=8,
        leading=10,
        leftIndent=10,
        backColor=colors.whitesmoke,
        borderPadding=5,
        borderRadius=2,
        textColor=colors.darkblue,
    )
    formula_style = ParagraphStyle(
        name="Formula",
        fontName="Times-Italic",
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    italic_style = styles["Italic"]
    italic_style.alignment = TA_CENTER

    story = []

    # --- Page de Garde ---
    story.append(Paragraph("Note de Calcul Hydraulique", title_style))
    story.append(Spacer(1, 1 * cm))
    story.append(
        Paragraph("Dimensionnement de Réseau d'Assainissement Pluvial", styles["h2"])
    )
    story.append(Spacer(1, 4 * cm))
    story.append(
        Paragraph(
            f"<b>Projet :</b> {project_info.get('nom_projet', 'Étude Comparative')}",
            body_style,
        )
    )
    story.append(
        Paragraph(
            f"<b>Date de la simulation :</b> {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            body_style,
        )
    )
    story.append(Paragraph("<b>Logiciel :</b> HydroApp v2.0", body_style))
    story.append(
        Paragraph(
            "<b>Auteur du programme :</b> TABE DJATO Serge / intrepidcore", body_style
        )
    )
    story.append(PageBreak())

    # --- Contenu principal du rapport ---
    if not is_comparison:
        # Chapitre 1: Hypothèses et Paramètres
        story.append(Paragraph("1. Hypothèses et Paramètres d'Entrée", h1_style))
        story.append(
            Paragraph(
                "Cette section détaille les choix et paramètres utilisés pour la simulation.",
                body_style,
            )
        )
        story.append(Paragraph("<b>1.1. Méthode de Calcul Hydrologique</b>", h2_style))
        story.append(
            Paragraph(
                f"La méthode retenue est la <b>{project_info['methode_calcul'].capitalize()}</b>.",
                body_style,
            )
        )
        if project_info["methode_calcul"] == "rationnelle":
            story.append(
                Paragraph(
                    f"Le temps de concentration de surface est calculé avec la formule de <b>{project_info['tc_formule_name'].capitalize()}</b>.",
                    body_style,
                )
            )

        story.append(Paragraph("<b>1.2. Pluviométrie de Projet</b>", h2_style))
        story.append(
            Paragraph(
                f"Le modèle d'Intensité-Durée-Fréquence (IDF) utilisé est le modèle de <b>{project_info.get('idf_formula', 'N/A').capitalize()}</b>.",
                body_style,
            )
        )
        story.append(
            Paragraph(
                f"Les paramètres pour la période de retour de <b>{project_info.get('periode_retour')} ans</b> sont :",
                body_style,
            )
        )
        param_str = f"a={project_info.get('a')}, b={project_info.get('b')}" + (
            f", c={project_info.get('c')}" if "c" in project_info else ""
        )
        story.append(Paragraph(param_str, code_style))

        story.append(
            Paragraph("<b>1.3. Formules Hydrauliques Appliquées</b>", h2_style)
        )
        story.append(
            Paragraph("<b>- Débit de pointe (Méthode Rationnelle) :</b>", h3_style)
        )
        story.append(Paragraph("Q = (C × i × A) / 360", formula_style))
        story.append(
            Paragraph(
                "<i>Avec : Q (m³/s), C (coeff. ruissellement), i (mm/h), A (hectares).</i>",
                italic_style,
            )
        )
        story.append(Spacer(1, 0.5 * cm))
        story.append(
            Paragraph("<b>- Capacité hydraulique (Manning-Strickler) :</b>", h3_style)
        )
        story.append(
            Paragraph(
                "Q = K<sub>s</sub> × S × R<sub>h</sub><sup>2/3</sup> × I<sup>1/2</sup>",
                formula_style,
            )
        )
        story.append(
            Paragraph(
                "<i>Avec : K<sub>s</sub> (coeff. Strickler), S (m²), R<sub>h</sub> (m), I (pente).</i>",
                italic_style,
            )
        )

        story.append(Paragraph("<b>1.4. Critères de Validation</b>", h2_style))
        story.append(
            Paragraph(
                f"Vitesse Minimale (auto-curage) : {project_info.get('v_min')} m/s",
                body_style,
            )
        )
        story.append(
            Paragraph(
                f"Vitesse Maximale (anti-érosion) : {project_info.get('v_max')} m/s",
                body_style,
            )
        )
        story.append(PageBreak())

        if verbose_log:
            story.append(
                Paragraph("2. Notes de Calcul Détaillées (Tronçon de Tête)", h1_style)
            )
            clean_log = clean_ansi_codes(verbose_log)
            verbose_text = clean_log.replace("\n", "<br/>").replace(" ", " ")
            story.append(Paragraph(verbose_text, code_style))
            story.append(PageBreak())

    # --- Tableau Récapitulatif ---
    chap_num_prefix = (
        "3. "
        if verbose_log and not is_comparison
        else ("2. " if not is_comparison else "1. ")
    )
    story.append(
        Paragraph(f"{chap_num_prefix}Tableau Récapitulatif des Résultats", h1_style)
    )

    data = [df_results.columns.to_list()] + df_results.values.tolist()

    # Définition des largeurs de colonne "idéales"
    ideal_widths = {
        "id_troncon": 2 * cm,
        "type_section": 2.2 * cm,
        "surface_cumulee": 2.2 * cm,
        "c_moyen_cumule": 2 * cm,
        "tc_final_min": 2 * cm,
        "q_max_m3s": 2 * cm,
        "diametre_retenu_mm": 2.5 * cm,
        "hauteur_retenue_m": 2.5 * cm,
        "largeur_m": 2 * cm,
        "vitesse_ms": 2 * cm,
        "statut": 4 * cm,
    }

    col_headers = df_results.columns
    col_widths = [
        ideal_widths.get(re.sub(r"_Sc\d+.*", "", h), 2.5 * cm) for h in col_headers
    ]
    total_width = sum(col_widths)

    # Décider de l'orientation de la page
    if total_width > (portrait(letter)[0] - 2 * cm):
        story.append(NextPageTemplate("landscape"))
        page_width = landscape(letter)[0] - 2 * cm
        col_widths = [w * (page_width / total_width) for w in col_widths]

    story.append(PageBreak())

    table = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.aliceblue),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]
    )

    if not is_comparison:
        try:
            for row_idx, row in df_results.iterrows():
                statut = str(row["statut"])
                if "Vitesse faible" in statut:
                    style.add(
                        "BACKGROUND",
                        (0, row_idx + 1),
                        (-1, row_idx + 1),
                        colors.lightblue,
                    )
                elif "Vitesse forte" in statut:
                    style.add(
                        "BACKGROUND", (0, row_idx + 1), (-1, row_idx + 1), colors.orange
                    )
                elif "Erreur" in statut or "Non-convergence" in statut:
                    style.add(
                        "BACKGROUND",
                        (0, row_idx + 1),
                        (-1, row_idx + 1),
                        colors.lightpink,
                    )
        except KeyError:
            pass

    table.setStyle(style)
    story.append(table)
    story.append(NextPageTemplate("portrait"))
    story.append(PageBreak())

    # --- Analyse Graphique ---
    if not is_comparison:
        chap_num_prefix = "4. " if verbose_log else "3. "
        story.append(Paragraph(f"{chap_num_prefix}Analyse Graphique", h1_style))
        graphics_dir = os.path.join("repports", "graphics")
        images_a_afficher = [
            "resultats_dimensions.png",
            "resultats_surface_debit.png",
            "resultats_tc_qmax.png",
            "resultats_profil_long.png",
        ]
        for i, img_name in enumerate(images_a_afficher):
            img_path = os.path.join(graphics_dir, img_name)
            if os.path.exists(img_path):
                story.append(Spacer(1, 1 * cm))
                story.append(
                    Image(img_path, width=18 * cm, height=12 * cm, kind="proportional")
                )
                if i < len(images_a_afficher) - 1:
                    story.append(PageBreak())

    return story


def creer_rapport_pdf(
    df_results: pd.DataFrame,
    project_info: dict,
    verbose_log: str,
    is_comparison=False,
    suffix="",
):
    """Génère un rapport de calcul complet et professionnel."""
    repports_dir = "repports"
    calcul_notes_dir = os.path.join(repports_dir, "calcul_notes")
    os.makedirs(calcul_notes_dir, exist_ok=True)

    base_name = project_info.get("nom_projet", "Projet").replace(".csv", "")
    if is_comparison:
        report_name = f"Etude_Comparative_{base_name}.pdf"
    else:
        report_name = (
            f"Rapport_{base_name}_{project_info.get('methode_calcul')}{suffix}.pdf"
        )

    file_path = os.path.join(calcul_notes_dir, report_name)

    doc = SimpleDocTemplate(file_path)

    frame_portrait = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="portrait_frame"
    )
    frame_landscape = Frame(
        doc.leftMargin, doc.bottomMargin, doc.height, doc.width, id="landscape_frame"
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="portrait", frames=frame_portrait),
            PageTemplate(
                id="landscape", frames=frame_landscape, pagesize=landscape(letter)
            ),
        ]
    )

    story = build_report_story(project_info, df_results, verbose_log, is_comparison)

    try:
        doc.build(story)
        print_colored(
            f"\nRapport PDF généré avec succès : {file_path}", "green", bold=True
        )
    except Exception as e:
        print_colored(
            f"\nErreur critique lors de la création du PDF : {e}", "red", bold=True
        )
