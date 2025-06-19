# reporting.py
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.lib import colors
import pandas as pd
from datetime import datetime
import os
import re
from utils.ui import print_colored

# Classe pour gérer le changement d'orientation de la page en mode paysage
class LandscapeFlowable(Flowable):
    """
    Flowable qui force le passage en mode paysage pour son contenu.
    Utile pour les grands tableaux.
    """
    def __init__(self, content):
        Flowable.__init__(self)
        self.content = content

    def draw(self):
        """La méthode draw est appelée par reportlab pour dessiner l'objet."""
        self.canv.setPageSize(landscape(letter))
        self.content.wrapOn(self.canv, self.canv._pagesize[0] - 2*cm, self.canv._pagesize[1] - 2*cm)
        self.content.drawOn(self.canv, cm, cm)

def clean_ansi_codes(text):
    """Supprime les séquences d'échappement ANSI (codes couleur) d'une chaîne."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def creer_rapport_pdf(df_results: pd.DataFrame, project_info: dict, verbose_log: str):
    """Génère un rapport de calcul complet et stylisé en format PDF."""
    
    repports_dir = 'repports'
    calcul_notes_dir = os.path.join(repports_dir, 'calcul_notes')
    os.makedirs(calcul_notes_dir, exist_ok=True)

    file_path = os.path.join(calcul_notes_dir, f"Rapport_{project_info.get('nom_projet', 'Projet').replace('.csv', '')}.pdf")
    
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(name='Title', fontSize=18, alignment=TA_CENTER, spaceAfter=20, fontName='Helvetica-Bold')
    h1_style = ParagraphStyle(name='H1', fontSize=14, alignment=TA_LEFT, spaceBefore=12, spaceAfter=12, fontName='Helvetica-Bold')
    code_style = ParagraphStyle(name='Code', fontName='Courier', fontSize=8, leading=10, leftIndent=10, backColor=colors.whitesmoke, borderPadding=5, borderRadius=2, textColor=colors.darkblue)

    # --- Page de Garde ---
    story.append(Paragraph("Rapport de Dimensionnement de Réseau Pluvial", title_style))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"<b>Projet :</b> {project_info.get('nom_projet', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Date :</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("<b>Auteur du programme :</b> TABE DJATO Serge / intrepidcore", styles['Normal']))
    story.append(Paragraph("<b>Dépôt GitHub :</b> https://github.com/prodeka", styles['Normal']))
    story.append(PageBreak())
    
    # --- Résumé et Calcul Détaillé ---
    story.append(Paragraph("1. Paramètres de Simulation", h1_style))
    story.append(Paragraph(f"   - <b>Méthode de Calcul :</b> {project_info['methode_calcul'].capitalize()}", styles['Normal']))
    if project_info['methode_calcul'] == 'rationnelle':
        story.append(Paragraph(f"   - <b>Formule de Tc Surface :</b> {project_info['tc_formule_name'].capitalize()}", styles['Normal']))
    story.append(Paragraph(f"   - <b>Modèle IDF :</b> {project_info.get('idf_formula', 'N/A').capitalize()}", styles['Normal']))
    story.append(Paragraph(f"   - <b>Paramètres de pluie :</b> a={project_info.get('a')}, b={project_info.get('b')}" + (f", c={project_info.get('c')}" if 'c' in project_info else ""), styles['Normal']))
    story.append(Paragraph(f"   - <b>Critères de vitesse :</b> Min = {project_info.get('v_min')} m/s, Max = {project_info.get('v_max')} m/s", styles['Normal']))

    story.append(Paragraph("2. Calcul Détaillé du Premier Tronçon", h1_style))
    if verbose_log:
        clean_log = clean_ansi_codes(verbose_log)
        verbose_text = clean_log.replace('\n', '<br/>').replace(' ', ' ')
        story.append(Paragraph(verbose_text, code_style))
    else:
        story.append(Paragraph("Aucun calcul détaillé n'a été enregistré.", styles['Italic']))

    # --- Tableau de Résultats (en mode paysage et découpable) ---
    story.append(PageBreak())
    story.append(Paragraph("3. Tableau des Résultats Complets", h1_style))
    story.append(Spacer(1, 0.5*cm))

    df_display = df_results.round(2)
    df_display['statut'] = df_display['statut'].apply(lambda x: "Erreur Débit" if "Débit trop élevé" in x else x)
    data = [df_display.columns.to_list()] + df_display.values.tolist()
    
    # ***** CORRECTION CLÉ : Ajout de splitByRow=1 *****
    # Cela autorise reportlab à découper le tableau entre les lignes.
    # colWidths permet d'ajuster la largeur des colonnes pour qu'elles tiennent sur la page.
    col_widths = [2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 4*cm]
    table = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    
    style_commandes = [
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,0), 10), ('TOPPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,-1), colors.aliceblue), ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]

    statut_col_index = df_display.columns.get_loc('statut')
    for row_idx, row in df_display.iterrows():
        statut = row['statut']
        if 'Vitesse faible' in statut:
            style_commandes.append(('BACKGROUND', (0, row_idx + 1), (-1, row_idx + 1), colors.lightblue))
        elif 'Vitesse forte' in statut:
            style_commandes.append(('BACKGROUND', (0, row_idx + 1), (-1, row_idx + 1), colors.orange))
        elif 'Erreur' in statut or 'Non-convergence' in statut:
            style_commandes.append(('BACKGROUND', (0, row_idx + 1), (-1, row_idx + 1), colors.lightpink))
            
    table.setStyle(TableStyle(style_commandes))
    
    story.append(LandscapeFlowable(table))
    story.append(PageBreak())

    # --- Graphiques ---
    story.append(Paragraph("4. Analyse Graphique", h1_style))
    
    graphics_dir = os.path.join('repports', 'graphics')
    images_a_afficher = ['resultats_dimensions.png', 'resultats_surface_debit.png', 'resultats_tc_qmax.png', 'resultats_profil_long.png']
    
    for i, img_name in enumerate(images_a_afficher):
        img_path = os.path.join(graphics_dir, img_name)
        if os.path.exists(img_path):
            # On ajoute un espace avant l'image pour un meilleur centrage
            story.append(Spacer(1, 1*cm))
            
            img = Image(img_path, width=18*cm, height=12*cm, kind='proportional')
            story.append(img)
            
            # ***** CORRECTION CLÉ : Ajout d'un saut de page après chaque image *****
            # Sauf pour la toute dernière image, pour éviter une page blanche à la fin.
            if i < len(images_a_afficher) - 1:
                story.append(PageBreak())

    try:
        doc.build(story)
        print_colored(f"\nRapport PDF généré avec succès : {file_path}", "green", bold=True)
    except Exception as e:
        print_colored(f"\nErreur critique lors de la création du PDF : {e}", "red", bold=True)