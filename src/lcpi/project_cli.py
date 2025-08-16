"""
Commandes CLI pour la gestion des projets et du sandbox.
"""
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import shutil
import zipfile
from datetime import datetime

from .core.global_config import global_config
from .core.context import get_project_context
from .core.template_manager import get_available_templates, get_template_description, get_template_type
from .core.example_manager import get_available_examples, get_example_description, get_example_files

console = Console()

app = typer.Typer(name="project", help="Gestion des projets et du contexte de travail")

def show_next_steps(template: str, project_path: Path):
    """Affiche les prochaines étapes après la création d'un projet."""
    console.print("\n🎯 **Prochaines étapes :**")
    
    if template.startswith("aep"):
        console.print("1. 📊 **Configurer votre réseau :**")
        console.print("   - Modifiez le fichier `data/network.yml`")
        console.print("   - Ajoutez vos nœuds et tronçons")
        console.print("2. 🚀 **Exécuter les calculs :**")
        console.print("   ```bash")
        console.print("   lcpi aep run data/network.yml")
        console.print("   ```")
        console.print("3. 📋 **Générer le rapport :**")
        console.print("   ```bash")
        console.print("   lcpi report generate")
        console.print("   ```")
    
    elif template in ["canal-simple", "dalot", "deversoir"]:
        console.print("1. 📏 **Configurer vos paramètres :**")
        console.print("   - Modifiez le fichier de configuration")
        console.print("   - Ajustez les dimensions et caractéristiques")
        console.print("2. 🧮 **Lancer le calcul :**")
        console.print("   ```bash")
        console.print("   lcpi hydro run data/canal.yml")
        console.print("   ```")
    
    elif template in ["beton-arme", "bois"]:
        console.print("1. 🏗️ **Configurer vos éléments :**")
        console.print("   - Modifiez les fichiers dans `data/`")
        console.print("   - Ajustez les charges et matériaux")
        console.print("2. 🔨 **Exécuter les calculs :**")
        console.print("   ```bash")
        console.print("   lcpi beton run data/")
        console.print("   # ou")
        console.print("   lcpi bois run data/")
        console.print("   ```")
    
    else:
        console.print("1. 📁 **Explorer la structure :**")
        console.print("   - Vérifiez le fichier `lcpi.yml`")
        console.print("   - Consultez le `README.md`")
        console.print("2. 🚀 **Commencer à travailler :**")
        console.print("   - Ajoutez vos données dans `data/`")
        console.print("   - Consultez la documentation LCPI")
    
    console.print(f"\n📁 **Projet créé dans :** {project_path.resolve()}")
    console.print("💡 **Aide :** Utilisez `lcpi --help` pour voir toutes les commandes disponibles")

@app.command("init")
def init_project(
    nom_projet: str = typer.Argument(..., help="Nom du projet à créer"),
    template: str = typer.Option(None, "--template", "-t", help="Template spécifique (cm, bois, beton, hydro, complet)"),
    plugins: str = typer.Option(None, "--plugins", "-p", help="Plugins à inclure (séparés par des virgules)"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer la création même si le dossier existe"),
    git_init: bool = typer.Option(False, "--git", "-g", help="Initialiser un dépôt Git"),
    remote_url: str = typer.Option(None, "--remote", "-r", help="URL du remote Git")
):
    """Initialise un nouveau projet LCPI dans le répertoire actuel."""
    try:
        # Créer l'arborescence du projet
        from .core.project_manager import create_project
        project_path = Path.cwd() / nom_projet
        
        if project_path.exists() and not force:
            typer.secho(f"❌ Le projet '{nom_projet}' existe déjà. Utilisez --force pour écraser.", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        # Créer le projet
        create_project(
            nom_projet=nom_projet,
            template=template,
            plugins=plugins,
            force=force,
            git_init=git_init,
            remote_url=remote_url
        )
        
        # Ajouter le projet à la configuration globale
        global_config.add_project(nom_projet, str(project_path.resolve()))
        
        # Définir comme projet actif
        global_config.set_active_project(nom_projet)
        
        console.print(f"✅ Projet '{nom_projet}' créé et activé.")
        console.print(f"📁 Chemin: {project_path.resolve()}")
        
    except Exception as e:
        typer.secho(f"❌ Erreur lors de la création du projet: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("create")
def create_project_from_template(
    nom_projet: str = typer.Argument(..., help="Nom du projet à créer"),
    template: str = typer.Option("aep-village", "--template", "-t", help="Template à utiliser"),
    output_dir: str = typer.Option(".", "--output", "-o", help="Répertoire de sortie"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer la création même si le dossier existe"),
    git_init: bool = typer.Option(False, "--git", "-g", help="Initialiser un dépôt Git"),
    remote_url: str = typer.Option(None, "--remote", "-r", help="URL du remote Git")
):
    """Crée un nouveau projet à partir d'un template prédéfini."""
    try:
        from .core.project_manager import create_project_from_template
        
        # Vérifier que le template existe
        available_templates = get_available_templates()
        if template not in available_templates:
            typer.secho(f"❌ Template '{template}' non trouvé.", fg=typer.colors.RED)
            typer.secho(f"📋 Templates disponibles: {', '.join(available_templates)}", fg=typer.colors.YELLOW)
            raise typer.Exit(1)
        
        # Créer le projet
        project_path = create_project_from_template(
            nom_projet=nom_projet,
            template=template,
            output_dir=output_dir,
            force=force,
            git_init=git_init,
            remote_url=remote_url
        )
        
        # Ajouter le projet à la configuration globale
        global_config.add_project(nom_projet, str(project_path.resolve()))
        
        # Définir comme projet actif
        global_config.set_active_project(nom_projet)
        
        console.print(f"✅ Projet '{nom_projet}' créé à partir du template '{template}'.")
        console.print(f"📁 Chemin: {project_path.resolve()}")
        
        # Afficher les prochaines étapes
        show_next_steps(template, project_path)
        
    except Exception as e:
        typer.secho(f"❌ Erreur lors de la création du projet: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("templates")
def list_templates():
    """Affiche la liste des templates disponibles."""
    templates = get_available_templates()
    
    if not templates:
        console.print("📋 Aucun template disponible.")
        return
    
    # Créer une table Rich
    table = Table(title="Templates LCPI Disponibles")
    table.add_column("Nom", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Type", style="yellow")
    
    for template in templates:
        description = get_template_description(template)
        template_type = get_template_type(template)
        table.add_row(template, description, template_type)
    
    console.print(table)
    console.print("\n💡 Utilisez 'lcpi project create <nom> --template <template>' pour créer un projet.")

@app.command("examples")
def list_examples():
    """Affiche la liste des exemples disponibles."""
    examples = get_available_examples()
    
    if not examples:
        console.print("📋 Aucun exemple disponible.")
        return
    
    # Créer une table Rich
    table = Table(title="Exemples LCPI Disponibles")
    table.add_column("Nom", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Fichiers", style="yellow")
    
    for example in examples:
        description = get_example_description(example)
        files = get_example_files(example)
        table.add_row(example, description, ", ".join(files))
    
    console.print(table)
    console.print("\n💡 Utilisez 'lcpi project create <nom> --template <template>' pour créer un projet.")

@app.command("list")
def list_projects():
    """Affiche la liste des projets connus."""
    projects = global_config.list_projects()
    active_project = global_config.get_active_project()
    
    if not projects:
        console.print("📋 Aucun projet connu.")
        return
    
    # Créer une table Rich
    table = Table(title="Projets LCPI Connus")
    table.add_column("Nom du Projet", style="cyan", no_wrap=True)
    table.add_column("Chemin", style="green")
    table.add_column("Statut", style="yellow")
    
    for name, path in projects.items():
        status = "🟢 Actif" if active_project and active_project['name'] == name else ""
        table.add_row(name, str(Path(path)), status)
    
    console.print(table)
    
    # Afficher le contexte actuel
    context = get_project_context()
    if context['type'] == 'sandbox':
        console.print("🟡 Mode sandbox actif")

@app.command("switch")
def switch_project(
    nom_projet: str = typer.Argument(None, help="Nom du projet à activer")
):
    """Change le projet actif."""
    projects = global_config.list_projects()
    
    if not projects:
        typer.secho("❌ Aucun projet connu. Créez d'abord un projet avec 'lcpi project init'.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    if not nom_projet:
        # Mode interactif
        console.print("📋 Projets disponibles :")
        project_names = list(projects.keys())
        
        for i, name in enumerate(project_names, 1):
            active_marker = "🟢 " if global_config.get_active_project() and global_config.get_active_project()['name'] == name else "  "
            console.print(f"  {i}. {active_marker}{name}")
        
        try:
            choice = typer.prompt("Sélectionnez le numéro du projet", type=int)
            if 1 <= choice <= len(project_names):
                nom_projet = project_names[choice - 1]
            else:
                typer.secho("❌ Sélection invalide", fg=typer.colors.RED)
                raise typer.Exit(1)
        except ValueError:
            typer.secho("❌ Sélection invalide", fg=typer.colors.RED)
            raise typer.Exit(1)
    
    try:
        global_config.set_active_project(nom_projet)
        console.print(f"✅ Projet '{nom_projet}' est maintenant actif.")
    except ValueError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("cd")
def cd_project():
    """Change le répertoire courant vers le projet actif."""
    active_project = global_config.get_active_project()
    
    if not active_project:
        typer.secho("❌ Aucun projet actif. Utilisez 'lcpi project switch' pour activer un projet.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    project_path = Path(active_project['path'])
    console.print(f"📁 Changement vers: {project_path}")
    
    # Note: Dans un vrai environnement, on changerait le répertoire
    # Mais ici on affiche juste le chemin
    console.print(f"💡 Pour naviguer vers ce dossier, utilisez: cd {project_path}")

@app.command("remove")
def remove_project(
    nom_projet: str = typer.Argument(..., help="Nom du projet à supprimer"),
    force: bool = typer.Option(False, "--force", "-f", help="Supprimer sans confirmation")
):
    """Supprime un projet de la liste des projets connus."""
    projects = global_config.list_projects()
    
    if nom_projet not in projects:
        typer.secho(f"❌ Projet '{nom_projet}' non trouvé.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    if not force:
        confirm = typer.confirm(f"Voulez-vous vraiment supprimer le projet '{nom_projet}' de la liste ?")
        if not confirm:
            console.print("❌ Suppression annulée.")
            return
    
    global_config.remove_project(nom_projet)
    console.print(f"✅ Projet '{nom_projet}' supprimé de la liste.")

@app.command("archive")
def archive_project(
    nom_projet: str = typer.Argument(..., help="Nom du projet à archiver"),
    output_dir: Path = typer.Option(Path.cwd(), "--output", "-o", help="Répertoire de sortie pour l'archive")
):
    """Crée une archive zip du projet."""
    projects = global_config.list_projects()
    
    if nom_projet not in projects:
        typer.secho(f"❌ Projet '{nom_projet}' non trouvé.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    project_path = Path(projects[nom_projet])
    if not project_path.exists():
        typer.secho(f"❌ Le dossier du projet '{nom_projet}' n'existe plus.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Créer le nom de l'archive
    timestamp = datetime.now().strftime("%Y-%m-%d")
    archive_name = f"{nom_projet.replace(' ', '_')}_{timestamp}.zip"
    archive_path = output_dir / archive_name
    
    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in project_path.rglob('*'):
                if file_path.is_file():
                    # Ajouter le fichier à l'archive avec un chemin relatif
                    arcname = file_path.relative_to(project_path)
                    zipf.write(file_path, arcname)
        
        console.print(f"✅ Archive créée: {archive_path}")
        console.print(f"📦 Taille: {archive_path.stat().st_size / 1024 / 1024:.1f} MB")
        
    except Exception as e:
        typer.secho(f"❌ Erreur lors de la création de l'archive: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("sandbox")
def sandbox_commands(
    clean: bool = typer.Option(False, "--clean", help="Nettoyer le contenu du sandbox"),
    status: bool = typer.Option(False, "--status", help="Afficher le statut du sandbox")
):
    """Gestion du sandbox."""
    if status:
        if global_config.is_sandbox_active():
            console.print("🟡 Sandbox actif")
            sandbox_path = global_config.get_sandbox_path()
            console.print(f"📁 Chemin: {sandbox_path}")
            
            # Afficher le contenu du sandbox
            if sandbox_path.exists():
                files = list(sandbox_path.iterdir())
                if files:
                    console.print("📋 Contenu du sandbox:")
                    for file in files:
                        if file.is_file():
                            console.print(f"  📄 {file.name}")
                        elif file.is_dir():
                            console.print(f"  📁 {file.name}/")
                else:
                    console.print("📋 Sandbox vide")
        else:
            console.print("⚪ Sandbox inactif")
    
    elif clean:
        if not global_config.is_sandbox_active():
            typer.secho("❌ Le sandbox n'est pas actif.", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        confirm = typer.confirm(
            "Voulez-vous supprimer tout le contenu du sandbox ? Cette action est irréversible."
        )
        
        if confirm:
            global_config.clean_sandbox()
            console.print("✅ Sandbox nettoyé.")
        else:
            console.print("❌ Nettoyage annulé.")
    
    else:
        # Afficher l'aide du sandbox
        console.print(Panel(
            "🟡 **Gestion du Sandbox**\n\n"
            "Le sandbox est un environnement d'expérimentation temporaire.\n\n"
            "**Commandes disponibles:**\n"
            "• lcpi project sandbox --status    - Afficher le statut\n"
            "• lcpi project sandbox --clean     - Nettoyer le contenu\n\n"
            "**Utilisation:**\n"
            "Le sandbox s'active automatiquement quand aucun projet n'est actif\n"
            "et que vous exécutez une commande métier.",
            title="Sandbox LCPI",
            border_style="yellow"
        ))

@app.command("status")
def project_status():
    """Affiche le statut du contexte actuel."""
    context = get_project_context()
    
    if context['type'] == 'project':
        console.print(Panel(
            f"🟢 **Projet Actif: {context['name']}**\n\n"
            f"📁 Chemin: {context['path']}\n"
            f"📊 Type: Projet LCPI\n\n"
            f"**Commandes utiles:**\n"
            f"• lcpi project cd              - Naviguer vers le projet\n"
            f"• lcpi project archive {context['name']}  - Archiver le projet",
            title="Contexte Actuel",
            border_style="green"
        ))
    
    elif context['type'] == 'sandbox':
        console.print(Panel(
            "🟡 **Mode Sandbox Actif**\n\n"
            f"📁 Chemin: {context['path']}\n"
            f"📊 Type: Environnement d'expérimentation\n\n"
            f"**Commandes utiles:**\n"
            f"• lcpi project sandbox --clean  - Nettoyer le sandbox\n"
            f"• lcpi project switch           - Activer un projet",
            title="Contexte Actuel",
            border_style="yellow"
        ))
    
    else:
        console.print(Panel(
            "⚪ **Aucun Contexte Actif**\n\n"
            "Aucun projet n'est actuellement actif.\n\n"
            f"**Commandes utiles:**\n"
            f"• lcpi project init <nom>       - Créer un nouveau projet\n"
            f"• lcpi project switch           - Activer un projet existant\n"
            f"• lcpi project list             - Voir les projets disponibles",
            title="Contexte Actuel",
            border_style="white"
        ))


@app.command("export-repro")
def export_reproducible(
    output: str = typer.Option("repro.tar.gz", "--output", "-o", help="Chemin du fichier d'export"),
    include_logs: bool = typer.Option(True, "--logs/--no-logs", help="Inclure les logs de calcul"),
    include_results: bool = typer.Option(True, "--results/--no-results", help="Inclure les résultats"),
    include_env: bool = typer.Option(True, "--env/--no-env", help="Inclure l'environnement Python"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails de l'export")
):
    """Exporte un environnement reproductible complet du projet."""
    try:
        from .core.reproducible import export_reproducible
        
        console.print("🚀 Export de l'environnement reproductible...")
        
        # Vérifier qu'un projet est actif
        if not project_context.is_project_active():
            console.print("❌ Aucun projet actif. Utilisez 'lcpi project switch <nom>' ou 'lcpi project init'")
            raise typer.Exit(1)
        
        # Effectuer l'export
        export_info = export_reproducible(
            output_path=output,
            include_logs=include_logs,
            include_results=include_results,
            include_env=include_env
        )
        
        # Afficher le résumé
        console.print(Panel("✅ Export réussi !", style="green"))
        console.print(f"📁 Fichier créé: {output}")
        console.print(f"📅 Date d'export: {export_info['export_date']}")
        console.print(f"🏗️  Projet: {export_info['project_name']}")
        
        if verbose:
            console.print("\n📋 Détails de l'export:")
            console.print(f"   • Logs inclus: {'✅' if include_logs else '❌'}")
            console.print(f"   • Résultats inclus: {'✅' if include_results else '❌'}")
            console.print(f"   • Environnement inclus: {'✅' if include_env else '❌'}")
        
        console.print(f"\n💡 Pour reproduire l'environnement:")
        console.print(f"   tar -xzf {output}")
        console.print(f"   cd lcpi_reproducible/environment")
        console.print(f"   pip install -r requirements.txt")
        console.print(f"   docker build -t lcpi-repro .")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'export: {e}")
        raise typer.Exit(1)
