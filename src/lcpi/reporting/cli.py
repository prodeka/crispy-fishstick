# src/lcpi/reporting/cli.py

import typer
from pathlib import Path
import json
from typing import List, Optional

from .report_generator import ReportGenerator
from .utils.pdf_generator import export_to_pdf
from .utils.docx_generator import export_to_docx
from ..logging import list_available_logs, load_log_by_id

app = typer.Typer(name="reporting", help="Génération de rapports professionnels à partir des logs de calcul.")

@app.command("generate", help="Génère un rapport à partir d'un ou plusieurs fichiers de log JSON.")
def generate_report(
    ctx: typer.Context,
    log_files: Optional[List[Path]] = typer.Option(
        None, 
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
    ),
    interactive: bool = typer.Option(
        False, 
        "--interactive", "-i",
        help="Mode interactif pour sélectionner les logs disponibles"
    ),
    log_ids: Optional[List[str]] = typer.Option(
        None, 
        "--logs",
        help="IDs des logs à inclure dans le rapport (ex: 20250127_143022)"
    )
):
    """Génère un rapport complet en HTML, PDF ou DOCX."""
    
    # --- Gestion des logs ---
    if interactive or log_ids:
        # Mode interactif ou sélection par IDs
        available_logs = list_available_logs()
        
        if not available_logs:
            typer.secho("❌ Aucun log trouvé dans le répertoire logs/", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        if interactive:
            # Mode interactif : afficher les logs disponibles et demander sélection
            typer.echo("📋 Logs disponibles :")
            for i, log in enumerate(available_logs, 1):
                typer.echo(f"  {i}. [{log['id']}] {log['titre_calcul']} - {log['timestamp'][:19]}")
            
            selected_indices = typer.prompt(
                "Sélectionnez les numéros des logs à inclure (séparés par des virgules)",
                type=str
            )
            
            try:
                indices = [int(x.strip()) - 1 for x in selected_indices.split(",")]
                selected_logs = [available_logs[i] for i in indices if 0 <= i < len(available_logs)]
            except (ValueError, IndexError):
                typer.secho("❌ Sélection invalide", fg=typer.colors.RED)
                raise typer.Exit(1)
        
        elif log_ids:
            # Mode sélection par IDs
            selected_logs = [log for log in available_logs if log['id'] in log_ids]
            if len(selected_logs) != len(log_ids):
                found_ids = [log['id'] for log in selected_logs]
                missing_ids = [log_id for log_id in log_ids if log_id not in found_ids]
                typer.secho(f"⚠️ Logs non trouvés : {missing_ids}", fg=typer.colors.YELLOW)
        
        # Charger les données des logs sélectionnés
        log_files = []
        for log_info in selected_logs:
            log_data = load_log_by_id(log_info['id'])
            if log_data:
                # Créer un fichier temporaire avec les données du log
                temp_file = Path(f"temp_log_{log_info['id']}.json")
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(log_data, f, indent=2, ensure_ascii=False)
                log_files.append(temp_file)
    
    elif not log_files:
        typer.secho("❌ Veuillez spécifier des fichiers de log ou utiliser --interactive", fg=typer.colors.RED)
        raise typer.Exit(1)
    
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
