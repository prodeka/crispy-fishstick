from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(results_list: list, output_filename: str):
    """Génère un rapport PDF simple à partir d'une liste de résultats."""
    doc = SimpleDocTemplate(output_filename)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Rapport d'Analyse LCPI-CLI", styles['h1']))
    story.append(Spacer(1, 12))

    for result in results_list:
        element_id = result.get('element_id', 'Inconnu')
        plugin = result.get('plugin', 'Inconnu')
        
        story.append(Paragraph(f"Élément : {element_id} (Plugin: {plugin})", styles['h2']))
        
        result_data = result.get('resultats', {})
        for key, value in result_data.items():
            text = f"<b>{key.replace('_', ' ').title()}:</b> {value}"
            story.append(Paragraph(text, styles['BodyText']))
        
        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"\n[SUCCES] Rapport PDF généré : {output_filename}")
