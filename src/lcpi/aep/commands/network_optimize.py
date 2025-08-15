"""
Commande CLI pour l'optimisation des réseaux AEP.
"""

import click
import yaml
import json
from pathlib import Path
from typing import Dict, Any
from ..optimization.models import ConfigurationOptimisation
from ..optimization.genetic_algorithm import GeneticOptimizer
from ..optimization.constraints import ConstraintManager

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Fichier de sortie JSON')
@click.option('--mode', type=click.Choice(['simple', 'enhanced']), default='enhanced', help='Mode d\'exécution')
@click.option('--verbose', '-v', is_flag=True, help='Affichage détaillé')
@click.option('--iterations', type=int, default=50, help='Nombre de générations')
@click.option('--population', type=int, default=100, help='Taille de la population')
def network_optimize(input_file: str, output: str, mode: str, verbose: bool, iterations: int, population: int):
    """
    Optimise les diamètres de conduites d'un réseau AEP.
    
    INPUT_FILE: Fichier YAML contenant la configuration d'optimisation
    """
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
            click.echo(f"🔧 Configuration chargée:")
            click.echo(f"   Critère principal: {config.criteres.principal}")
            click.echo(f"   Budget max: {config.contraintes_budget.cout_max_fcfa} FCFA")
            click.echo(f"   Diamètres candidats: {len(config.diametres_candidats)}")
        
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
            click.echo("❌ Aucune conduite trouvée dans le fichier de configuration")
            return
        
        # Lancer l'optimisation
        resultats = optimizer.optimiser(reseau_data, nb_conduites)
        
        # Sauvegarder les résultats
        if output:
            output_path = Path(output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(resultats, f, indent=2, ensure_ascii=False)
            click.echo(f"💾 Résultats sauvegardés dans: {output_path}")
        else:
            # Affichage des résultats
            click.echo("\n📊 RÉSULTATS DE L'OPTIMISATION")
            click.echo("=" * 50)
            
            opt = resultats['optimisation']
            click.echo(f"Algorithme: {opt['algorithme']}")
            click.echo(f"Convergence: {opt['convergence']['iterations']} générations")
            click.echo(f"Fitness finale: {opt['convergence']['fitness_finale']:.4f}")
            
            solution = opt['meilleure_solution']
            click.echo(f"\n🏆 MEILLEURE SOLUTION")
            click.echo(f"Coût total: {solution['performance']['cout_total_fcfa']:.0f} FCFA")
            click.echo(f"Performance: {solution['performance']['performance_hydraulique']:.3f}")
            click.echo(f"Énergie: {solution['performance']['energie_totale_kwh']:.1f} kWh")
            
            click.echo(f"\n📏 DIAMÈTRES OPTIMISÉS")
            for conduite, diametre in solution['diametres'].items():
                click.echo(f"  {conduite}: {diametre} mm")
        
        click.echo("\n✅ Optimisation terminée avec succès!")
        
    except Exception as e:
        click.echo(f"❌ Erreur lors de l'optimisation: {e}")
        if verbose:
            import traceback
            click.echo(traceback.format_exc())
        raise click.Abort()

if __name__ == '__main__':
    network_optimize()
