"""
Commande CLI pour l'optimisation des réseaux AEP.
"""

import typer
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import conditionnel des modules d'optimisation
try:
    from ..optimization.models import ConfigurationOptimisation
    from ..optimization.genetic_algorithm import GeneticOptimizer
    from ..optimization.constraints import ConstraintManager
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False

app = typer.Typer(help="Commandes d'analyse et d'optimisation de réseaux")
console = Console()

@app.command()
def optimize(
    input_file: Path = typer.Argument(..., help="Fichier YAML contenant la configuration d'optimisation"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie JSON"),
    mode: str = typer.Option("enhanced", "--mode", "-m", help="Mode d'exécution (simple/enhanced)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Affichage détaillé"),
    iterations: int = typer.Option(50, "--iterations", "-i", help="Nombre de générations"),
    population: int = typer.Option(100, "--population", "-p", help="Taille de la population")
):
    """
    Optimise les diamètres de conduites d'un réseau AEP.
    
    INPUT_FILE: Fichier YAML contenant la configuration d'optimisation
    """
    if not OPTIMIZATION_AVAILABLE:
        console.print("❌ Module d'optimisation non disponible", style="red")
        console.print("💡 Installez les dépendances requises pour l'optimisation", style="yellow")
        raise typer.Exit(code=1)
    
    try:
        # Charger la configuration
        with open(input_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        # Valider la configuration
        config = ConfigurationOptimisation(**config_data['optimisation'])
        
        # Ajuster les paramètres si spécifiés en ligne de commande
        config.algorithme.generations = iterations
        config.algorithme.population_size = population
        
        if verbose:
            console.print(Panel.fit("🔧 Configuration chargée", style="blue"))
            console.print(f"   Critère principal: {config.criteres.principal}")
            console.print(f"   Budget max: {config.contraintes_budget.cout_max_fcfa} FCFA")
            console.print(f"   Diamètres candidats: {len(config.diametres_candidats)}")
        
        # Créer le gestionnaire de contraintes
        constraint_manager = ConstraintManager(
            config.contraintes_budget,
            config.contraintes_techniques
        )
        
        # Créer l'optimiseur
        optimizer = GeneticOptimizer(config, constraint_manager)
        
        # Charger les données du réseau
        reseau_data = config_data.get('reseau_complet', {})
        nb_conduites = len(reseau_data.get('conduites', []))
        
        if nb_conduites == 0:
            console.print("❌ Aucune conduite trouvée dans le fichier de configuration", style="red")
            raise typer.Exit(code=1)
        
        # Lancer l'optimisation
        with console.status("[bold green]Optimisation en cours..."):
            resultats = optimizer.optimiser(reseau_data, nb_conduites)
        
        # Sauvegarder les résultats
        if output:
            output_path = Path(output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(resultats, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Résultats sauvegardés dans: {output_path}", style="green")
        else:
            # Affichage des résultats
            console.print(Panel.fit("📊 RÉSULTATS DE L'OPTIMISATION", style="green"))
            
            opt = resultats['optimisation']
            console.print(f"Algorithme: {opt['algorithme']}")
            console.print(f"Convergence: {opt['convergence']['iterations']} générations")
            console.print(f"Fitness finale: {opt['convergence']['fitness_finale']:.4f}")
            
            solution = opt['meilleure_solution']
            console.print(f"\n🏆 MEILLEURE SOLUTION")
            console.print(f"Coût total: {solution['performance']['cout_total_fcfa']:.0f} FCFA")
            console.print(f"Performance: {solution['performance']['performance_hydraulique']:.3f}")
            console.print(f"Énergie: {solution['performance']['energie_totale_kwh']:.1f} kWh")
            
            console.print(f"\n📏 DIAMÈTRES OPTIMISÉS")
            for conduite, diametre in solution['diametres'].items():
                console.print(f"  {conduite}: {diametre} mm")
        
        console.print("\n✅ Optimisation terminée avec succès!", style="green")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'optimisation: {e}", style="red")
        if verbose:
            import traceback
            console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)

@app.command()
def sensitivity(
    input_file: Path = typer.Argument(..., help="Fichier YAML réseau de base"),
    parametres: str = typer.Option("rugosite,demande", "--parametres", "-p", help="Paramètres à analyser"),
    iterations: int = typer.Option(1000, "--iterations", "-i", help="Nombre d'itérations Monte-Carlo"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie")
):
    """Analyse de sensibilité des paramètres du réseau."""
    console.print("🔍 Analyse de sensibilité - Fonctionnalité en cours de développement", style="yellow")

@app.command()
def compare(
    variante1: Path = typer.Argument(..., help="Première variante de réseau"),
    variante2: Path = typer.Argument(..., help="Deuxième variante de réseau"),
    criteres: str = typer.Option("cout,performance", "--criteres", "-c", help="Critères de comparaison"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie")
):
    """Compare deux variantes de réseau."""
    console.print("⚖️ Comparaison de variantes - Fonctionnalité en cours de développement", style="yellow")

if __name__ == '__main__':
    app()
