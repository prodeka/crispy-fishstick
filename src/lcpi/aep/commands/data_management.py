"""
Commandes CLI pour la gestion des données (import/export/validation).
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.import_automatique import AEPImportAutomatique
from ..core.validation_donnees import AEPDataValidator
from ..core.recalcul_automatique import AEPRecalculEngine
from ..utils.exporters import export_content

app = typer.Typer(help="Gestion des données (import/export/validation)")
console = Console()

@app.command("import")
def import_data(
    source: Path = typer.Argument(..., help="Fichier source à importer"),
    format: str = typer.Option("auto", "--format", "-f", help="Format du fichier (auto, csv, yaml, json, excel)"),
    validate: bool = typer.Option(True, "--validate", help="Valider les données après import"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les données validées")
):
    """Importer des données depuis différents formats."""
    
    console.print(Panel.fit("📥 [bold blue]Import de Données[/bold blue]"))
    
    try:
        # 1. Import automatique
        with console.status("[bold green]Import des données..."):
            importer = ImportAutomatique()
            data = importer.importer_fichier(source, format_force=format if format != "auto" else None)
        
        console.print(f"✅ Données importées avec succès depuis {source}")
        console.print(f"📊 {len(data)} éléments importés")
        
        # 2. Validation des données si demandé
        if validate:
            with console.status("[bold blue]Validation des données..."):
                validator = ValidationDonnees()
                validation_results = validator.valider_donnees(data)
            
            # Affichage des résultats de validation
            validation_table = Table(title="Résultats de Validation")
            validation_table.add_column("Critère", style="cyan")
            validation_table.add_column("Statut", style="bold")
            validation_table.add_column("Détails", style="white")
            
            for critere, result in validation_results.items():
                status = "✅ OK" if result["valide"] else "❌ Erreur"
                status_style = "green" if result["valide"] else "red"
                
                validation_table.add_row(
                    critere,
                    f"[{status_style}]{status}[/{status_style}]",
                    result.get("message", "")
                )
            
            console.print(validation_table)
            
            # Sauvegarde des données validées si demandé
            if output and validation_results.get("global", {}).get("valide", False):
                exporter = DataExporter()
                exporter.exporter_json(data, output)
                console.print(f"💾 Données validées sauvegardées dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'import: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("export")
def export_data(
    source: Path = typer.Argument(..., help="Fichier source à exporter"),
    format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, yaml, csv, excel, html)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie")
):
    """Exporter des données vers différents formats."""
    
    console.print(Panel.fit("📤 [bold blue]Export de Données[/bold blue]"))
    
    try:
        # 1. Import des données source
        with console.status("[bold green]Chargement des données..."):
            importer = ImportAutomatique()
            data = importer.importer_fichier(source)
        
        # 2. Export vers le format demandé
        with console.status(f"[bold blue]Export vers {format.upper()}..."):
            exporter = DataExporter()
            
            if not output:
                output = source.with_suffix(f".{format}")
            
            if format == "json":
                exporter.exporter_json(data, output)
            elif format == "yaml":
                exporter.exporter_yaml(data, output)
            elif format == "csv":
                exporter.exporter_csv(data, output)
            elif format == "excel":
                exporter.exporter_excel(data, output)
            elif format == "html":
                exporter.exporter_html(data, output)
            else:
                raise ValueError(f"Format non supporté: {format}")
        
        console.print(f"✅ Données exportées avec succès vers {output}")
        console.print(f"📊 {len(data)} éléments exportés")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'export: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("validate")
def validate_data(
    source: Path = typer.Argument(..., help="Fichier à valider"),
    rules: Optional[Path] = typer.Option(None, "--rules", "-r", help="Fichier de règles de validation"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Rapport de validation")
):
    """Valider des données selon des règles définies."""
    
    console.print(Panel.fit("🔍 [bold blue]Validation de Données[/bold blue]"))
    
    try:
        # 1. Import des données
        with console.status("[bold green]Chargement des données..."):
            importer = ImportAutomatique()
            data = importer.importer_fichier(source)
        
        # 2. Validation
        with console.status("[bold blue]Validation en cours..."):
            validator = ValidationDonnees()
            
            if rules:
                # Charger des règles personnalisées
                validation_results = validator.valider_avec_regles(data, rules)
            else:
                # Validation par défaut
                validation_results = validator.valider_donnees(data)
        
        # 3. Affichage des résultats
        console.print(f"✅ Validation terminée pour {len(data)} éléments")
        
        # Résumé de validation
        summary_table = Table(title="Résumé de Validation")
        summary_table.add_column("Critère", style="cyan")
        summary_table.add_column("Statut", style="bold")
        summary_table.add_column("Erreurs", style="white")
        summary_table.add_column("Avertissements", style="yellow")
        
        for critere, result in validation_results.items():
            if critere == "global":
                continue
                
            status = "✅ OK" if result["valide"] else "❌ Erreur"
            status_style = "green" if result["valide"] else "red"
            
            errors = len(result.get("erreurs", []))
            warnings = len(result.get("avertissements", []))
            
            summary_table.add_row(
                critere,
                f"[{status_style}]{status}[/{status_style}]",
                str(errors),
                str(warnings)
            )
        
        console.print(summary_table)
        
        # 4. Sauvegarde du rapport si demandé
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(validation_results, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Rapport de validation sauvegardé dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la validation: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("recalculate")
def recalculate_data(
    source: Path = typer.Argument(..., help="Fichier source pour le recalcul"),
    mode: str = typer.Option("auto", "--mode", "-m", help="Mode de recalcul (auto, force, incremental)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les résultats")
):
    """Recalculer automatiquement les données selon les dépendances."""
    
    console.print(Panel.fit("🔄 [bold blue]Recalcul Automatique[/bold blue]"))
    
    try:
        # 1. Import des données
        with console.status("[bold green]Chargement des données..."):
            importer = ImportAutomatique()
            data = importer.importer_fichier(source)
        
        # 2. Recalcul automatique
        with console.status("[bold blue]Recalcul en cours..."):
            recalculator = RecalculAutomatique()
            
            if mode == "force":
                results = recalculator.recalcul_complet(data)
            elif mode == "incremental":
                results = recalculator.recalcul_incremental(data)
            else:  # auto
                results = recalculator.recalcul_intelligent(data)
        
        # 3. Affichage des résultats
        console.print(f"✅ Recalcul terminé")
        
        # Résumé du recalcul
        summary_table = Table(title="Résumé du Recalcul")
        summary_table.add_column("Métrique", style="cyan")
        summary_table.add_column("Valeur", style="white")
        
        summary_table.add_row("Mode", mode)
        summary_table.add_row("Éléments traités", str(len(results.get("traites", []))))
        summary_table.add_row("Éléments mis à jour", str(len(results.get("mis_a_jour", []))))
        summary_table.add_row("Éléments inchangés", str(len(results.get("inchanges", []))))
        summary_table.add_row("Erreurs", str(len(results.get("erreurs", []))))
        
        console.print(summary_table)
        
        # 4. Sauvegarde des résultats si demandé
        if output:
            exporter = DataExporter()
            exporter.exporter_json(results, output)
            console.print(f"💾 Résultats du recalcul sauvegardés dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du recalcul: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("convert")
def convert_format(
    source: Path = typer.Argument(..., help="Fichier source"),
    source_format: str = typer.Option("auto", "--source-format", "-sf", help="Format source (auto, csv, yaml, json, excel)"),
    target_format: str = typer.Option("json", "--target-format", "-tf", help="Format cible (json, yaml, csv, excel, html)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie")
):
    """Convertir des données d'un format vers un autre."""
    
    console.print(Panel.fit("🔄 [bold blue]Conversion de Format[/bold blue]"))
    
    try:
        # 1. Import depuis le format source
        with console.status(f"[bold green]Import depuis {source_format.upper()}..."):
            importer = ImportAutomatique()
            data = importer.importer_fichier(source, format_force=source_format if source_format != "auto" else None)
        
        # 2. Export vers le format cible
        with console.status(f"[bold blue]Export vers {target_format.upper()}..."):
            exporter = DataExporter()
            
            if not output:
                output = source.with_suffix(f".{target_format}")
            
            if target_format == "json":
                exporter.exporter_json(data, output)
            elif target_format == "yaml":
                exporter.exporter_yaml(data, output)
            elif target_format == "csv":
                exporter.exporter_csv(data, output)
            elif target_format == "excel":
                exporter.exporter_excel(data, output)
            elif target_format == "html":
                exporter.exporter_html(data, output)
            else:
                raise ValueError(f"Format cible non supporté: {target_format}")
        
        console.print(f"✅ Conversion réussie: {source} → {output}")
        console.print(f"📊 {len(data)} éléments convertis")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la conversion: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("batch")
def batch_process(
    input_dir: Path = typer.Argument(..., help="Répertoire contenant les fichiers à traiter"),
    pattern: str = typer.Option("*.yml", "--pattern", "-p", help="Pattern de fichiers à traiter"),
    operation: str = typer.Option("validate", "--operation", "-op", help="Opération à effectuer (validate, convert, recalculate)"),
    target_format: Optional[str] = typer.Option(None, "--target-format", "-tf", help="Format cible pour la conversion"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-od", help="Répertoire de sortie")
):
    """Traiter un lot de fichiers en mode batch."""
    
    console.print(Panel.fit("📁 [bold blue]Traitement en Lot[/bold blue]"))
    
    try:
        # 1. Recherche des fichiers
        files = list(input_dir.glob(pattern))
        if not files:
            console.print(f"❌ Aucun fichier trouvé avec le pattern: {pattern}")
            return
        
        console.print(f"📋 {len(files)} fichiers trouvés")
        
        # 2. Traitement en lot
        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for file_path in files:
                task = progress.add_task(f"Traitement de {file_path.name}...", total=None)
                
                try:
                    if operation == "validate":
                        # Validation
                        importer = ImportAutomatique()
                        data = importer.importer_fichier(file_path)
                        validator = ValidationDonnees()
                        result = validator.valider_donnees(data)
                        result["fichier"] = file_path.name
                        result["statut"] = "valide" if result.get("global", {}).get("valide", False) else "invalide"
                        
                    elif operation == "convert":
                        # Conversion
                        if not target_format:
                            raise ValueError("Format cible requis pour la conversion")
                            
                        importer = ImportAutomatique()
                        data = importer.importer_fichier(file_path)
                        exporter = DataExporter()
                        
                        if output_dir:
                            output_file = output_dir / f"{file_path.stem}.{target_format}"
                        else:
                            output_file = file_path.with_suffix(f".{target_format}")
                        
                        if target_format == "json":
                            exporter.exporter_json(data, output_file)
                        elif target_format == "yaml":
                            exporter.exporter_yaml(data, output_file)
                        elif target_format == "csv":
                            exporter.exporter_csv(data, output_file)
                        elif target_format == "excel":
                            exporter.exporter_excel(data, output_file)
                        elif target_format == "html":
                            exporter.exporter_html(data, output_file)
                        
                        result = {
                            "fichier": file_path.name,
                            "statut": "converti",
                            "sortie": str(output_file)
                        }
                        
                    elif operation == "recalculate":
                        # Recalcul
                        importer = ImportAutomatique()
                        data = importer.importer_fichier(file_path)
                        recalculator = RecalculAutomatique()
                        result = recalculator.recalcul_intelligent(data)
                        result["fichier"] = file_path.name
                        result["statut"] = "recalculé"
                    
                    else:
                        raise ValueError(f"Opération non supportée: {operation}")
                    
                    results.append(result)
                    progress.update(task, description=f"✅ {file_path.name} traité")
                    
                except Exception as e:
                    result = {
                        "fichier": file_path.name,
                        "statut": "erreur",
                        "erreur": str(e)
                    }
                    results.append(result)
                    progress.update(task, description=f"❌ {file_path.name} échoué")
        
        # 3. Résumé du traitement
        console.print(f"\n✅ Traitement terminé")
        
        summary_table = Table(title="Résumé du Traitement en Lot")
        summary_table.add_column("Statut", style="bold")
        summary_table.add_column("Nombre", style="white")
        
        status_counts = {}
        for result in results:
            status = result["statut"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            status_emoji = "✅" if status in ["valide", "converti", "recalculé"] else "❌"
            summary_table.add_row(f"{status_emoji} {status}", str(count))
        
        console.print(summary_table)
        
        # 4. Sauvegarde du rapport si demandé
        if output_dir:
            import json
            report_file = output_dir / "rapport_traitement.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Rapport de traitement sauvegardé dans: {report_file}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du traitement en lot: {e}", style="red")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
