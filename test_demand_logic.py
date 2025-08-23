from __future__ import annotations

import os
from pathlib import Path
import shutil
import typer
from rich import print as rprint

# Assurez-vous que le chemin du projet est dans le sys.path pour trouver lcpi
import sys
# Obtenez le répertoire du script actuel et remontez pour trouver la racine du projet
script_dir = Path(__file__).parent
project_root = script_dir.parent  # Ajustez si nécessaire
sys.path.insert(0, str(project_root))

from src.lcpi.aep.utils.inp_demand_manager import handle_demand_logic

app = typer.Typer()

@app.command()
def test_demand(
    input_file: Path = typer.Argument(..., help="Fichier INP à tester", exists=True),
    demand: float = typer.Option(..., "--demand", help="Valeur de demande à appliquer"),
    no_log: bool = typer.Option(False, "--no-log", help="Désactiver les confirmations interactives (simule --yes)"),
):
    """
    Script de test pour valider la fonction handle_demand_logic de manière isolée.
    """
    rprint(f"▶️  Test de handle_demand_logic sur '{input_file}' avec une demande de {demand}")
    
    # Créer un répertoire de sortie temporaire pour les résultats
    output_dir = Path("./test_demand_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    
    # Copier le fichier d'entrée original pour comparaison
    original_copy_path = output_dir / "original.inp"
    shutil.copy(input_file, original_copy_path)
    rprint(f"📋 Copie de l'original dans '{original_copy_path}'")

    try:
        # Appeler la fonction à tester
        # Le paramètre 'yes' dans la fonction est mappé à 'no_log' ici
        processed_file_path = handle_demand_logic(input_file, demand, yes=no_log)
        
        rprint(f"[green]✅ handle_demand_logic a terminé avec succès.[/green]")
        rprint(f"📄 Fichier traité (temporaire): '{processed_file_path}'")

        # Copier le fichier traité dans notre répertoire de sortie pour inspection
        final_copy_path = output_dir / "processed.inp"
        shutil.copy(processed_file_path, final_copy_path)
        rprint(f"✨ Copie du fichier traité dans '{final_copy_path}' pour inspection.")
        
        # Afficher les différences
        rprint("\n--- [bold]Comparaison des fichiers[/bold] ---")
        os.system(f'diff "{original_copy_path}" "{final_copy_path}"')
        
    except Exception as e:
        rprint(f"[red]❌ Erreur pendant l'exécution de handle_demand_logic:[/red]")
        rprint(e)
    finally:
        # Le nettoyage des fichiers temporaires est géré par atexit dans inp_demand_manager
        rprint("\n[info]Le nettoyage des fichiers temporaires est géré automatiquement à la fin du script.[/info]")


if __name__ == "__main__":
    app()
