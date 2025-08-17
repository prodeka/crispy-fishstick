"""
Interface CLI pour la gestion des logs LCPI.
Gère la signature, l'intégrité et l'indexation des logs.
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .lcpi_logging.logger import logger

app = typer.Typer(name="logs", help="Gestion des logs LCPI avec signature et intégrité")
console = Console()

@app.command()
def list(
    limit: int = typer.Option(50, "--limit", "-l", help="Nombre maximum de logs à afficher"),
    show_details: bool = typer.Option(False, "--details", "-d", help="Afficher les détails complets")
):
    """Liste les logs disponibles."""
    console.print(Panel("📋 Liste des Logs LCPI", style="blue"))
    
    logs = logger.list_available_logs(limit)
    
    if not logs:
        console.print("ℹ️  Aucun log trouvé.")
        return
    
    if show_details:
        # Affichage détaillé
        for log in logs:
            console.print(f"\n📄 {log['filename']}")
            console.print(f"   📁 Chemin: {log['file_path']}")
            console.print(f"   📊 Taille: {log['size_bytes']} octets")
            console.print(f"   🕒 Modifié: {log['modified']}")
            if 'age_hours' in log:
                console.print(f"   ⏰ Âge: {log['age_hours']:.1f} heures")
            if 'error' in log:
                console.print(f"   ❌ Erreur: {log['error']}")
    else:
        # Affichage en tableau
        table = Table(title="Logs LCPI")
        table.add_column("Fichier", style="cyan")
        table.add_column("Taille", style="green")
        table.add_column("Modifié", style="yellow")
        table.add_column("Âge", style="magenta")
        
        for log in logs:
            age_str = f"{log.get('age_hours', 0):.1f}h" if 'age_hours' in log else "N/A"
            size_str = f"{log['size_bytes']} B" if 'size_bytes' in log else "N/A"
            
            table.add_row(
                log['filename'],
                size_str,
                log.get('modified', 'N/A'),
                age_str
            )
        
        console.print(table)

@app.command()
def verify(
    log_file: Optional[Path] = typer.Argument(None, help="Fichier de log à vérifier"),
    all_logs: bool = typer.Option(False, "--all", "-a", help="Vérifier tous les logs")
):
    """Vérifie l'intégrité et la signature des logs."""
    if all_logs:
        console.print(Panel("🔍 Vérification de tous les logs", style="blue"))
        result = logger.verify_all_logs()
        
        if result.get("valid"):
            console.print("✅ Tous les logs sont valides !")
        else:
            console.print(f"⚠️  {result.get('corrupted_logs', 0)} logs corrompus détectés.")
        
        console.print(f"\n📊 Résumé:")
        console.print(f"   Total: {result.get('total_logs', 0)}")
        console.print(f"   Valides: {result.get('valid_logs', 0)}")
        console.print(f"   Corrompus: {result.get('corrupted_logs', 0)}")
        
        if result.get("results"):
            console.print("\n🔍 Détails par fichier:")
            for file_result in result["results"][:10]:  # Limiter l'affichage
                status = "✅" if file_result.get("valid") else "❌"
                console.print(f"   {status} {file_result.get('file_path', 'N/A')}")
                
                if not file_result.get("valid") and "error" in file_result:
                    console.print(f"      Erreur: {file_result['error']}")
        
        return
    
    if not log_file:
        console.print("❌ Veuillez spécifier un fichier de log ou utiliser --all")
        raise typer.Exit(1)
    
    if not log_file.exists():
        console.print(f"❌ Fichier non trouvé: {log_file}")
        raise typer.Exit(1)
    
    console.print(Panel(f"🔍 Vérification du log: {log_file.name}", style="blue"))
    
    # Vérifier l'intégrité
    integrity_result = logger.verify_log_integrity(log_file)
    console.print(f"\n📋 Intégrité:")
    
    if integrity_result.get("valid"):
        console.print("   ✅ Fichier valide")
        console.print(f"   📊 Taille: {integrity_result.get('file_size', 0)} octets")
        console.print(f"   🕒 Modifié: {integrity_result.get('last_modified', 'N/A')}")
    else:
        console.print("   ❌ Fichier corrompu")
        if "error" in integrity_result:
            console.print(f"   Erreur: {integrity_result['error']}")
    
    # Vérifier la signature
    signature_result = logger.verify_log_signature(log_file)
    console.print(f"\n🔐 Signature:")
    
    if signature_result.get("valid"):
        console.print("   ✅ Signature valide")
        signature_info = signature_result.get("signature_info", {})
        console.print(f"   🗝️  Algorithme: {signature_info.get('algorithm', 'N/A')}")
        console.print(f"   🆔 Clé: {signature_info.get('key_id', 'N/A')}")
        console.print(f"   🕒 Signé le: {signature_info.get('timestamp', 'N/A')}")
    else:
        console.print("   ❌ Signature invalide")
        if "error" in signature_result:
            console.print(f"   Erreur: {signature_result['error']}")

@app.command()
def search(
    query: str = typer.Argument(..., help="Requête de recherche"),
    limit: int = typer.Option(50, "--limit", "-l", help="Nombre maximum de résultats"),
    calculation_type: Optional[str] = typer.Option(None, "--type", "-t", help="Type de calcul"),
    solver: Optional[str] = typer.Option(None, "--solver", "-s", help="Solveur utilisé")
):
    """Recherche dans les logs indexés."""
    console.print(Panel(f"🔍 Recherche: {query}", style="blue"))
    
    filters = {}
    if calculation_type:
        filters["calculation_type"] = calculation_type
    if solver:
        filters["solver"] = solver
    
    results = logger.search_logs(query, filters, limit)
    
    if not results:
        console.print("ℹ️  Aucun résultat trouvé.")
        return
    
    console.print(f"📊 {len(results)} résultats trouvés:")
    
    table = Table(title="Résultats de recherche")
    table.add_column("Type", style="cyan")
    table.add_column("Solveur", style="green")
    table.add_column("Timestamp", style="yellow")
    table.add_column("Statut", style="magenta")
    table.add_column("Fichier", style="blue")
    
    for result in results:
        table.add_row(
            result.get("calculation_type", "N/A"),
            result.get("solver", "N/A"),
            result.get("timestamp", "N/A"),
            result.get("status", "N/A"),
            Path(result.get("log_file", "")).name
        )
    
    console.print(table)

@app.command()
def stats():
    """Affiche les statistiques des logs."""
    console.print(Panel("📊 Statistiques des Logs LCPI", style="blue"))
    
    stats = logger.get_log_statistics()
    
    if "error" in stats:
        console.print(f"❌ Erreur: {stats['error']}")
        return
    
    console.print(f"📈 Total des logs: {stats.get('total_logs', 0)}")
    
    if stats.get("by_calculation_type"):
        console.print("\n📋 Par type de calcul:")
        for calc_type, count in stats["by_calculation_type"].items():
            console.print(f"   {calc_type}: {count}")
    
    console.print(f"\n🕒 Indexé le: {stats.get('indexed_at', 'N/A')}")

@app.command()
def index(
    force: bool = typer.Option(False, "--force", "-f", help="Forcer la réindexation")
):
    """Indexe tous les logs du répertoire."""
    console.print(Panel("📚 Indexation des Logs LCPI", style="blue"))
    
    if not logger.enable_indexing:
        console.print("❌ Indexation non activée")
        return
    
    console.print("🔄 Indexation en cours...")
    
    try:
        result = logger.indexer.index_all_logs(force_reindex=force)
        
        if result.get("success"):
            console.print("✅ Indexation terminée !")
            console.print(f"📊 {result.get('indexed_logs', 0)} logs indexés sur {result.get('total_logs', 0)}")
        else:
            console.print(f"❌ Erreur lors de l'indexation: {result.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        console.print(f"❌ Erreur: {e}")

@app.command()
def export_report(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie")
):
    """Exporte un rapport d'intégrité complet."""
    console.print(Panel("📤 Export du Rapport d'Intégrité", style="blue"))
    
    try:
        output_path = logger.export_integrity_report(output)
        console.print(f"✅ Rapport exporté: {output_path}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'export: {e}")

@app.command()
def key_info():
    """Affiche les informations de la clé de signature."""
    console.print(Panel("🗝️  Informations de la Clé de Signature", style="blue"))
    
    key_info = logger.get_public_key_info()
    
    if "error" in key_info:
        console.print(f"❌ {key_info['error']}")
        return
    
    console.print(f"🆔 ID de clé: {key_info.get('key_id', 'N/A')}")
    console.print(f"🔐 Algorithme: {key_info.get('algorithm', 'N/A')}")
    console.print(f"📅 Créée le: {key_info.get('created', 'N/A')}")

@app.command()
def export_key(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour la clé")
):
    """Exporte la clé de signature (à utiliser avec précaution)."""
    console.print(Panel("⚠️  Export de la Clé de Signature", style="red"))
    console.print("⚠️  ATTENTION: Cette opération exporte votre clé secrète !")
    
    if not typer.confirm("Êtes-vous sûr de vouloir continuer ?"):
        console.print("❌ Opération annulée.")
        return
    
    try:
        output_path = logger.export_signing_key(output)
        console.print(f"✅ Clé exportée: {output_path}")
        console.print("⚠️  Conservez cette clé en sécurité et ne la partagez jamais !")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'export: {e}")

@app.command()
def cleanup(
    max_age: int = typer.Option(30, "--max-age", "-m", help="Âge maximum en jours"),
    dry_run: bool = typer.Option(True, "--dry-run", "-d", help="Mode simulation"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer la suppression")
):
    """Nettoie les anciens logs."""
    console.print(Panel("🧹 Nettoyage des Anciens Logs", style="blue"))
    
    if not dry_run and not force:
        console.print("⚠️  ATTENTION: Vous êtes sur le point de supprimer des fichiers !")
        if not typer.confirm("Êtes-vous sûr de vouloir continuer ?"):
            console.print("❌ Opération annulée.")
            return
    
    try:
        result = logger.cleanup_old_logs(max_age, dry_run)
        
        if "error" in result:
            console.print(f"❌ Erreur: {result['error']}")
            return
        
        if dry_run:
            console.print("🔍 Mode simulation - Aucun fichier supprimé")
            console.print(f"📊 {result.get('logs_to_remove', 0)} logs seraient supprimés")
        else:
            console.print(f"✅ Nettoyage terminé: {result.get('logs_removed', 0)} logs supprimés")
        
        console.print(f"📅 Âge maximum: {max_age} jours")
        
    except Exception as e:
        console.print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    app()
