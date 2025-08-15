# src/lcpi/reporting/utils/pdf_generator.py

from pathlib import Path

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

def export_to_pdf(html_content: str, output_path: Path, base_url: Path):
    """
    Exporte une chaîne de caractères HTML en fichier PDF.

    Args:
        html_content: Le contenu HTML à convertir.
        output_path: Le chemin du fichier PDF de sortie.
        base_url: Le chemin de base pour résoudre les URLs relatives (ex: pour le CSS).
    """
    if not WEASYPRINT_AVAILABLE:
        print("Erreur : Le package 'WeasyPrint' est requis pour l'export PDF.")
        print("Veuillez l'installer avec : pip install WeasyPrint")
        return

    try:
        # WeasyPrint a besoin d'une URL de base pour trouver les fichiers liés comme le CSS
        html = HTML(string=html_content, base_url=str(base_url))
        html.write_pdf(output_path)
        print(f"✅ Rapport PDF généré avec succès : {output_path}")
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
