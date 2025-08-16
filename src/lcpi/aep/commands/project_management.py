"""
Commandes CLI pour la gestion des projets (base de données, requêtes, validation).
"""

import typer
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.database import AEPDatabase
from ..core.validators import validate_population_data, validate_population_unified_data
from ..core.dynamic_constants import AEPDynamicConstantsManager

app = typer.Typer(help="Gestion des projets AEP")
console = Console()

@app.command("init")
def init_project(
    project_name: str = typer.Argument(..., help="Nom du projet"),
    project_dir: Optional[Path] = typer.Option(None, "--dir", "-d", help="Répertoire du projet"),
    template: str = typer.Option("default", "--template", "-t", help="Template de projet à utiliser")
):
    """Initialiser un nouveau projet AEP."""
    
    console.print(Panel.fit("🚀 [bold blue]Initialisation de Projet[/bold blue]"))
    
    try:
        # 1. Création du répertoire du projet
        if not project_dir:
            project_dir = Path.cwd() / project_name
        
        project_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"📁 Répertoire du projet: {project_dir}")
        
        # 2. Initialisation de la base de données
        with console.status("[bold green]Initialisation de la base de données..."):
            db_manager = DatabaseManager(project_dir)
            db_manager.initialize_project(project_name)
        
        # 3. Création de la structure du projet
        with console.status("[bold blue]Création de la structure..."):
            # Créer les sous-répertoires
            (project_dir / "data").mkdir(exist_ok=True)
            (project_dir / "config").mkdir(exist_ok=True)
            (project_dir / "results").mkdir(exist_ok=True)
            (project_dir / "reports").mkdir(exist_ok=True)
            
            # Créer le fichier de configuration principal
            config_file = project_dir / "config" / "project.yml"
            config_content = f"""# Configuration du projet {project_name}
project:
  name: {project_name}
  version: "1.0.0"
  description: "Projet AEP {project_name}"
  created_date: "{datetime.now().strftime('%Y-%m-%d')}"

# Paramètres par défaut
defaults:
  units:
    pressure: "mCE"
    flow: "m3/s"
    length: "m"
    diameter: "mm"
  
  materials:
    - name: "PVC"
      roughness: 120
      max_pressure: 6
    - name: "PE"
      roughness: 140
      max_pressure: 10
    - name: "Acier"
      roughness: 100
      max_pressure: 16

# Structure des données
data_structure:
  nodes: "data/nodes.yml"
  pipes: "data/pipes.yml"
  reservoirs: "data/reservoirs.yml"
  demands: "data/demands.yml"
"""
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
        
        # 4. Création des fichiers de données d'exemple
        with console.status("[bold yellow]Création des fichiers d'exemple..."):
            # Fichier des nœuds
            nodes_file = project_dir / "data" / "nodes.yml"
            nodes_content = """# Exemple de nœuds
nodes:
  - id: "N1"
    name: "Réservoir Principal"
    type: "reservoir"
    elevation: 100.0
    coordinates: [0, 0]
    
  - id: "N2"
    name: "Nœud de Distribution 1"
    type: "junction"
    elevation: 95.0
    coordinates: [100, 0]
    demand: 0.001
    
  - id: "N3"
    name: "Nœud de Distribution 2"
    type: "junction"
    elevation: 92.0
    coordinates: [200, 0]
    demand: 0.0008
"""
            
            with open(nodes_file, 'w', encoding='utf-8') as f:
                f.write(nodes_content)
            
            # Fichier des conduites
            pipes_file = project_dir / "data" / "pipes.yml"
            pipes_content = """# Exemple de conduites
pipes:
  - id: "P1"
    name: "Conduite principale"
    from_node: "N1"
    to_node: "N2"
    length: 100.0
    diameter: 150
    material: "PVC"
    roughness: 120
    
  - id: "P2"
    name: "Conduite secondaire"
    from_node: "N2"
    to_node: "N3"
    length: 100.0
    diameter: 110
    material: "PVC"
    roughness: 120
"""
            
            with open(pipes_file, 'w', encoding='utf-8') as f:
                f.write(pipes_content)
        
        console.print(f"✅ Projet '{project_name}' initialisé avec succès")
        console.print(f"📁 Répertoire: {project_dir}")
        console.print(f"🗄️  Base de données: {project_dir / 'project.db'}")
        console.print(f"⚙️  Configuration: {config_file}")
        
        # 5. Instructions d'utilisation
        console.print("\n📋 [bold]Prochaines étapes:[/bold]")
        console.print("1. Modifier les fichiers de données dans le répertoire 'data/'")
        console.print("2. Ajuster la configuration dans 'config/project.yml'")
        console.print("3. Lancer les calculs avec: lcpi network analyze --config config/project.yml")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'initialisation: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("validate")
def validate_project(
    project_dir: Path = typer.Argument(..., help="Répertoire du projet à valider"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de rapport de validation")
):
    """Valider un projet AEP complet."""
    
    console.print(Panel.fit("🔍 [bold blue]Validation de Projet[/bold blue]"))
    
    try:
        # 1. Chargement de la configuration du projet
        with console.status("[bold green]Chargement de la configuration..."):
            config_file = project_dir / "config" / "project.yml"
            if not config_file.exists():
                raise FileNotFoundError(f"Fichier de configuration non trouvé: {config_file}")
            
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        
        # 2. Validation du projet
        with console.status("[bold blue]Validation en cours..."):
            validator = ProjectValidator()
            validation_results = validator.validate_project(project_dir, config)
        
        # 3. Affichage des résultats
        console.print(f"✅ Validation terminée pour le projet: {config.get('project', {}).get('name', 'Inconnu')}")
        
        # Résumé de validation
        summary_table = Table(title="Résumé de Validation du Projet")
        summary_table.add_column("Composant", style="cyan")
        summary_table.add_column("Statut", style="bold")
        summary_table.add_column("Détails", style="white")
        
        for component, result in validation_results.items():
            if component == "global":
                continue
                
            status = "✅ OK" if result["valide"] else "❌ Erreur"
            status_style = "green" if result["valide"] else "red"
            
            details = result.get("message", "")
            if result.get("erreurs"):
                details += f" ({len(result['erreurs'])} erreurs)"
            if result.get("avertissements"):
                details += f" ({len(result['avertissements'])} avertissements)"
            
            summary_table.add_row(
                component,
                f"[{status_style}]{status}[/{status_style}]",
                details
            )
        
        console.print(summary_table)
        
        # 4. Statut global
        global_status = validation_results.get("global", {})
        if global_status.get("valide", False):
            console.print("🎉 [bold green]Projet validé avec succès ![/bold green]")
        else:
            console.print("⚠️  [bold yellow]Projet présente des problèmes à corriger[/bold yellow]")
        
        # 5. Sauvegarde du rapport si demandé
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(validation_results, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Rapport de validation sauvegardé dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la validation: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("info")
def project_info(
    project_dir: Path = typer.Argument(..., help="Répertoire du projet")
):
    """Afficher les informations d'un projet AEP."""
    
    console.print(Panel.fit("ℹ️ [bold blue]Informations du Projet[/bold blue]"))
    
    try:
        # 1. Chargement de la configuration
        config_file = project_dir / "config" / "project.yml"
        if not config_file.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé: {config_file}")
        
        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 2. Informations du projet
        project_info = config.get("project", {})
        
        info_table = Table(title="Informations du Projet")
        info_table.add_column("Propriété", style="cyan")
        info_table.add_column("Valeur", style="white")
        
        info_table.add_row("Nom", project_info.get("name", "N/A"))
        info_table.add_row("Version", project_info.get("version", "N/A"))
        info_table.add_row("Description", project_info.get("description", "N/A"))
        info_table.add_row("Date de création", project_info.get("created_date", "N/A"))
        info_table.add_row("Répertoire", str(project_dir))
        
        console.print(info_table)
        
        # 3. Structure des données
        data_structure = config.get("data_structure", {})
        if data_structure:
            console.print("\n📁 [bold]Structure des Données:[/bold]")
            structure_table = Table()
            structure_table.add_column("Type", style="cyan")
            structure_table.add_column("Fichier", style="white")
            structure_table.add_column("Statut", style="bold")
            
            for data_type, file_path in data_structure.items():
                full_path = project_dir / file_path
                if full_path.exists():
                    status = "✅ Présent"
                    status_style = "green"
                else:
                    status = "❌ Manquant"
                    status_style = "red"
                
                structure_table.add_row(
                    data_type.title(),
                    file_path,
                    f"[{status_style}]{status}[/{status_style}]"
                )
            
            console.print(structure_table)
        
        # 4. Paramètres par défaut
        defaults = config.get("defaults", {})
        if defaults:
            console.print("\n⚙️ [bold]Paramètres par Défaut:[/bold]")
            
            if "units" in defaults:
                units_table = Table(title="Unités")
                units_table.add_column("Mesure", style="cyan")
                units_table.add_column("Unité", style="white")
                
                for measure, unit in defaults["units"].items():
                    units_table.add_row(measure.title(), unit)
                
                console.print(units_table)
            
            if "materials" in defaults:
                materials_table = Table(title="Matériaux")
                materials_table.add_column("Nom", style="cyan")
                materials_table.add_column("Rugosité", style="white")
                materials_table.add_column("Pression Max (bar)", style="white")
                
                for material in defaults["materials"]:
                    materials_table.add_row(
                        material.get("name", "N/A"),
                        str(material.get("roughness", "N/A")),
                        str(material.get("max_pressure", "N/A"))
                    )
                
                console.print(materials_table)
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la récupération des informations: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("query")
def query_project(
    project_dir: Path = typer.Argument(..., help="Répertoire du projet"),
    query: str = typer.Option(..., "--query", "-q", help="Requête SQL à exécuter"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les résultats")
):
    """Exécuter une requête SQL sur la base de données du projet."""
    
    console.print(Panel.fit("🔍 [bold blue]Requête sur le Projet[/bold blue]"))
    
    try:
        # 1. Connexion à la base de données
        with console.status("[bold green]Connexion à la base de données..."):
            db_manager = DatabaseManager(project_dir)
            db_path = project_dir / "project.db"
            
            if not db_path.exists():
                raise FileNotFoundError(f"Base de données non trouvée: {db_path}")
        
        # 2. Exécution de la requête
        with console.status("[bold blue]Exécution de la requête..."):
            results = db_manager.execute_query(query)
        
        # 3. Affichage des résultats
        if results:
            console.print(f"✅ Requête exécutée avec succès")
            console.print(f"📊 {len(results)} lignes retournées")
            
            # Affichage des résultats dans un tableau
            if results and len(results) > 0:
                result_table = Table(title="Résultats de la Requête")
                
                # En-têtes des colonnes
                for column in results[0].keys():
                    result_table.add_column(column, style="cyan")
                
                # Données
                for row in results[:10]:  # Limiter à 10 lignes pour l'affichage
                    result_table.add_row(*[str(value) for value in row.values()])
                
                if len(results) > 10:
                    result_table.add_row("...", "...", "...")
                
                console.print(result_table)
                
                if len(results) > 10:
                    console.print(f"⚠️  Affichage limité à 10 lignes sur {len(results)} totales")
            else:
                console.print("ℹ️  Aucune donnée retournée")
        else:
            console.print("ℹ️  Requête exécutée sans retour de données")
        
        # 4. Sauvegarde des résultats si demandé
        if output and results:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Résultats sauvegardés dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'exécution de la requête: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("constants")
def manage_constants(
    project_dir: Path = typer.Argument(..., help="Répertoire du projet"),
    action: str = typer.Option("list", "--action", "-a", help="Action à effectuer (list, get, set, reset)"),
    constant_name: Optional[str] = typer.Option(None, "--name", "-n", help="Nom de la constante"),
    value: Optional[str] = typer.Option(None, "--value", "-v", help="Nouvelle valeur de la constante")
):
    """Gérer les constantes dynamiques du projet."""
    
    console.print(Panel.fit("🔧 [bold blue]Gestion des Constantes[/bold blue]"))
    
    try:
        # 1. Initialisation du gestionnaire de constantes
        constants_manager = DynamicConstants(project_dir)
        
        if action == "list":
            # Lister toutes les constantes
            constants = constants_manager.get_all_constants()
            
            if constants:
                constants_table = Table(title="Constantes du Projet")
                constants_table.add_column("Nom", style="cyan")
                constants_table.add_column("Valeur", style="white")
                constants_table.add_column("Description", style="white")
                constants_table.add_column("Modifiable", style="bold")
                
                for name, info in constants.items():
                    modifiable = "✅ Oui" if info.get("modifiable", False) else "❌ Non"
                    constants_table.add_row(
                        name,
                        str(info.get("value", "N/A")),
                        info.get("description", "Aucune description"),
                        modifiable
                    )
                
                console.print(constants_table)
            else:
                console.print("ℹ️  Aucune constante définie")
        
        elif action == "get":
            # Obtenir la valeur d'une constante
            if not constant_name:
                raise ValueError("Nom de la constante requis pour l'action 'get'")
            
            constant_value = constants_manager.get_constant(constant_name)
            if constant_value is not None:
                console.print(f"📊 Constante '{constant_name}': {constant_value}")
            else:
                console.print(f"❌ Constante '{constant_name}' non trouvée")
        
        elif action == "set":
            # Définir la valeur d'une constante
            if not constant_name:
                raise ValueError("Nom de la constante requis pour l'action 'set'")
            if not value:
                raise ValueError("Nouvelle valeur requise pour l'action 'set'")
            
            success = constants_manager.set_constant(constant_name, value)
            if success:
                console.print(f"✅ Constante '{constant_name}' mise à jour: {value}")
            else:
                console.print(f"❌ Impossible de modifier la constante '{constant_name}'")
        
        elif action == "reset":
            # Réinitialiser les constantes
            if constant_name:
                # Réinitialiser une constante spécifique
                success = constants_manager.reset_constant(constant_name)
                if success:
                    console.print(f"✅ Constante '{constant_name}' réinitialisée")
                else:
                    console.print(f"❌ Impossible de réinitialiser la constante '{constant_name}'")
            else:
                # Réinitialiser toutes les constantes
                constants_manager.reset_all_constants()
                console.print("✅ Toutes les constantes ont été réinitialisées")
        
        else:
            raise ValueError(f"Action non supportée: {action}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la gestion des constantes: {e}", style="red")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
