from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console
from rich.text import Text
import time
import subprocess
import json
import pathlib
import sys

console = Console()

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

    with console.status("[bold green]Génération du rapport PDF...", spinner="dots") as status:
        doc.build(story)
        time.sleep(1) # Simuler le temps de génération
    console.print(f"\n[bold green]✓[/bold green] Rapport PDF généré : {output_filename}")


def run_analysis_and_generate_report(project_dir: str, output_format: str = "pdf"):
    """
    Fonction principale pour scanner le projet, exécuter les calculs
    et générer le rapport final avec une barre de progression.
    """
    project_path = pathlib.Path(project_dir).resolve()
    results = []
    
    plugin_commands = {
        "cm": "calc", 
        "bois": "check", 
        "beton": "calc", 
        "hydrodrain": "calc"
    }

    # Supprimer les messages rich si la sortie JSON est activée
    if output_format != "json":
        console.print(f"[bold cyan]--- Démarrage de l'analyse du projet ({project_path}) ---[/bold cyan]")
    
    files_to_process = []
    for plugin in plugin_commands.keys():
        plugin_dir = pathlib.Path(__file__).parent.parent / plugin
        if plugin_dir.is_dir():
            files_to_process.extend(list(plugin_dir.glob("**/*.yml")))

    if not files_to_process:
        if output_format != "json":
            console.print("[yellow]Aucun fichier .yml à analyser n'a été trouvé dans les plugins.[/yellow]")
        return

    # Utiliser Progress uniquement si la sortie n'est pas JSON
    if output_format != "json":
        progress_context = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            SpinnerColumn(),
            console=console,
            transient=True
        )
    else:
        progress_context = type("NoProgress", (object,), {"__enter__": lambda s: s, "__exit__": lambda s, *a: None, "add_task": lambda s, *a, **kw: None, "update": lambda s, *a, **kw: None, "advance": lambda s, *a: None})()

    with progress_context as progress:
        task = progress.add_task("[green]Analyse des éléments...", total=len(files_to_process))

        for yml_file in files_to_process:
            try:
                plugin_name = yml_file.relative_to(pathlib.Path(__file__).parent.parent).parts[0]
            except ValueError:
                if output_format != "json":
                    console.print(f"[red]Impossible de déterminer le plugin pour {yml_file}[/red]")
                continue

            command = plugin_commands.get(plugin_name)
            if not command:
                continue

            if output_format != "json":
                progress.update(task, description=f"Analyse de [bold]{yml_file.name}[/bold] ([cyan]{plugin_name}[/cyan])")
            
            script_path = pathlib.Path(__file__).parent.parent / "main.py"
            cmd = [sys.executable, str(script_path), plugin_name, command, str(yml_file), "--json"]
            
            try:
                process = subprocess.run(
                    cmd, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore'
                )
                
                if process.returncode != 0:
                    raise subprocess.CalledProcessError(
                        returncode=process.returncode,
                        cmd=cmd,
                        stderr=process.stderr
                    )

                output = process.stdout
                start = output.find('{')
                end = output.rfind('}') + 1
                if start != -1 and end != 0:
                    json_output = output[start:end]
                    data = json.loads(json_output)
                    results.append(data)
                else:
                    if output_format != "json":
                        console.log(f"[yellow]Avertissement[/yellow]: Pas de sortie JSON pour {yml_file.name}.")

            except subprocess.CalledProcessError as e:
                if output_format != "json":
                    console.print(f"[bold red]Erreur lors de l'analyse de {yml_file.name}[/bold red]")
                    console.print(f"[red]  CMD: {' '.join(e.cmd)}[/red]")
                    console.print(f"[red]  Code de sortie: {e.returncode}[/red]")
                    error_output = e.stderr or e.stdout or ""
                    console.print(f"[red]  Erreur: {error_output.strip()}[/red]")
            except json.JSONDecodeError:
                if output_format != "json":
                    console.print(f"[bold red]Erreur de décodage JSON pour {yml_file.name}[/bold red]")
                    console.print(f"[red]  Sortie reçue: {output.strip()}[/red]")
            except Exception as e:
                if output_format != "json":
                    console.print(f"[bold red]Une erreur inattendue est survenue avec {yml_file.name}: {e}[/bold red]")

            if output_format != "json":
                progress.advance(task)

    if results:
        if output_format == "json":
            # Imprimer directement le JSON sur stdout
            json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n") # Ajouter une nouvelle ligne à la fin
        else:
            output_filename = project_path / f"rapport_lcpi.{output_format}"
            console.print(f"\n[bold cyan]--- Génération du rapport ---[/bold cyan]")
            if output_format == "pdf":
                generate_pdf_report(results, str(output_filename))
            else:
                json_output_path = str(output_filename).replace('.pdf', '.json')
                with console.status("[bold green]Génération du rapport JSON...", spinner="dots"):
                    with open(json_output_path, "w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    time.sleep(0.5)
                console.print(f"[bold green]✓[/bold green] Rapport JSON généré : {json_output_path}")
    else:
        if output_format != "json":
            console.print("\n[yellow]Aucune donnée d'analyse valide n'a été collectée. Le rapport n'a pas été généré.[/yellow]")