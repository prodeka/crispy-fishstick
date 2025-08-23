"""
Module centralisé pour les composants Rich UI.
Fournit une interface cohérente et moderne pour toutes les commandes CLI.
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text

# Console globale pour une utilisation cohérente
console = Console()

class RichUI:
    """Gère un affichage de progression multi-barres pour l'optimiseur."""

    def __init__(self, console: Console):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=False  # Garder les barres visibles après la fin
        )
        self.tasks = {}

    def __enter__(self):
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()

    def setup_tasks(self, total_generations: int, population_size: int):
        """Ajoute les barres de progression pour les générations et la population."""
        self.tasks['generations'] = self.progress.add_task(
            "[green]Générations", total=total_generations
        )
        self.tasks['population'] = self.progress.add_task(
            "[cyan]Évaluation Population", total=population_size
        )

    def update(self, event: str, data: dict):
        """Met à jour les barres de progression en fonction des événements de l'optimiseur."""
        if event == "generation_start":
            # Réinitialiser la barre de la population pour la nouvelle génération
            self.progress.reset(self.tasks['population'])

        elif event == "individual_end":
            self.progress.update(self.tasks['population'], advance=1)

        elif event == "generation_end":
            gen_num = data.get("generation", 0)
            best_cost = data.get("best_cost", float('inf'))
            description = f"[green]Génération {gen_num + 1} - Meilleur Coût: {best_cost:,.0f} FCFA"
            self.progress.update(
                self.tasks['generations'],
                advance=1,
                description=description
            )