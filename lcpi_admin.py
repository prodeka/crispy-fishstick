import json
from pathlib import Path

import typer
from rich.console import Console

from src.lcpi.core.integrity import generate_keys, verify_signature

app = typer.Typer(help="Outils d'administration pour la plateforme LCPI.")
console = Console()

@app.command("generate-keys")
def cmd_generate_keys(
    force: bool = typer.Option(False, "--force", help="Forcer la création de nouvelles clés si elles existent déjà.")
):
    """Génère une nouvelle paire de clés de signature ECDSA."""
    try:
        generate_keys(force=force)
        console.print("[green]Opération terminée.[/green]")
    except Exception as e:
        console.print(f"[bold red]Erreur : {e}[/bold red]")
        raise typer.Exit(code=1)

@app.command("verify-log")
def cmd_verify_log(
    log_file: Path = typer.Argument(..., help="Chemin vers le fichier de résultat JSON à vérifier.", exists=True)
):
    """Vérifie l'intégrité et la signature d'un fichier de résultat."""
    console.print(f"Vérification de [cyan]{log_file}[/cyan]...")
    try:
        data = json.loads(log_file.read_text(encoding="utf-8"))
        result = verify_signature(data)
        
        if result["valid"]:
            console.print(f"[bold green]✔ Succès:[/bold green] {result['reason']}")
        else:
            console.print(f"[bold red]❌ Échec:[/bold red] {result['reason']}")
            raise typer.Exit(code=1)
            
    except json.JSONDecodeError:
        console.print("[bold red]Erreur: Le fichier n'est pas un JSON valide.[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Erreur inattendue : {e}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
