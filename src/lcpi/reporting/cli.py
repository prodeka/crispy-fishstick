# src/lcpi/reporting/cli.py

import typer
from pathlib import Path
import json
from typing import List

from .report_generator import ReportGenerator
from .utils.pdf_generator import export_to_pdf
from .utils.docx_generator import export_to_docx

app = typer.Typer(name="reporting", help="Génération de rapports professionnels à partir des logs de calcul.")

@app.command("generate", help="Génère un rapport à partir d'un ou plusieurs fichiers de log JSON.")
def generate_report(
    ctx: typer.Context,
    log_files: List[Path] = typer.Argument(
        ..., 
        help="Le ou les chemins vers les fichiers de log JSON à inclure.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    output_file: Path = typer.Option(
        Path("rapport.html"), 
        "--output", "-o", 
        help="Chemin du fichier de sortie."
    ),
    output_format: str = typer.Option(
        "html", 
        "--format", "-f", 
        help="Format de sortie (html, pdf, docx)."
    ),
    project_file: Path = typer.Option(
        None, 
        "--project", "-p",
        help="Chemin vers le fichier de métadonnées du projet (lcpi.yml ou .json).",
        exists=True
    )
):
    """Génère un rapport complet en HTML, PDF ou DOCX."""
    
    # --- Chargement des métadonnées du projet ---
    project_metadata = {}
    if project_file:
        try:
            with open(project_file, 'r', encoding='utf-8') as f:
                # Simple check for yaml, could be improved with pyyaml
                if project_file.suffix in ['.yml', '.yaml']:
                    import yaml
                    project_metadata = yaml.safe_load(f).get("projet_metadata", {})
                else:
                    project_metadata = json.load(f).get("projet_metadata", {})
        except Exception as e:
            typer.secho(f"Avertissement: Impossible de charger le fichier projet {project_file}. Erreur: {e}", fg=typer.colors.YELLOW)
            project_metadata = {"nom_projet": "Projet LCPI (métadonnées non trouvées)"}
    else:
        project_metadata = {"nom_projet": "Projet LCPI"}

    # --- Logique de génération ---
    template_dir = Path(__file__).parent / "templates"
    report_gen = ReportGenerator(template_dir=template_dir)

    typer.echo(f"Génération du rapport au format {output_format.upper()}...")

    if output_format.lower() == 'docx':
        # Le générateur DOCX a besoin des données brutes, pas du HTML.
        logs_data = []
        for log_path in log_files:
            with open(log_path, 'r', encoding='utf-8') as f:
                logs_data.append(json.load(f))
        export_to_docx(logs_data, project_metadata, output_file)
    else:
        # Génération HTML comme base pour HTML et PDF
        html_content = report_gen.generate_html_report(log_files, project_metadata)
        
        if output_format.lower() == 'html':
            try:
                with open(output_file, "w", encoding='utf-8') as f:
                    f.write(html_content)
                typer.secho(f"✅ Rapport HTML généré avec succès : {output_file}", fg=typer.colors.GREEN)
            except IOError as e:
                typer.secho(f"❌ Erreur lors de l'écriture du fichier HTML : {e}", fg=typer.colors.RED)
                raise typer.Exit(1)

        elif output_format.lower() == 'pdf':
            # Le base_url est le dossier des templates pour que WeasyPrint trouve le CSS
            export_to_pdf(html_content, output_file, base_url=template_dir)
        else:
            typer.secho(f"Format de sortie '{output_format}' non reconnu. Utilisez html, pdf, or docx.", fg=typer.colors.RED)
            raise typer.Exit(1)

if __name__ == "__main__":
    app()
