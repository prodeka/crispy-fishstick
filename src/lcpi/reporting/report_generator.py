# src/lcpi/reporting/report_generator.py

import json
import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class ReportGenerator:
    """Génère un rapport HTML à partir de données de log et de templates Jinja2."""

    def __init__(self, template_dir: Path):
        """
        Initialise le générateur de rapport.

        Args:
            template_dir: Le chemin vers le dossier contenant les templates Jinja2.
        """
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        # On pourrait ajouter des filtres personnalisés ici si nécessaire

    def generate_html_report(
        self, 
        selected_logs_paths: list[Path],
        project_metadata: dict,
        lcpi_version: str = "1.0.0" # Pourrait être récupéré dynamiquement
    ) -> str:
        """
        Génère le contenu HTML complet du rapport.

        Args:
            selected_logs_paths: Liste des chemins vers les fichiers de log JSON à inclure.
            project_metadata: Dictionnaire des métadonnées du projet (nom, client, etc.).
            lcpi_version: Version de l'outil LCPI.

        Returns:
            Le contenu HTML du rapport sous forme de chaîne de caractères.
        """
        
        # 1. Charger les données des logs
        logs_data = []
        for log_path in selected_logs_paths:
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs_data.append(json.load(f))
            except (IOError, json.JSONDecodeError) as e:
                print(f"Avertissement : Impossible de charger ou parser le fichier de log {log_path}. Erreur: {e}")
                continue

        # 2. Préparer le contexte pour Jinja2
        context = {
            "projet_metadata": project_metadata,
            "auteurs": project_metadata.get("auteurs", [{"nom": "Non spécifié", "role": ""}]),
            "generation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "logs_selectionnes": logs_data,
            "version_lcpi": lcpi_version
        }

        # 3. Charger le template de base et le rendre
        try:
            template = self.env.get_template("base.html")
            html_output = template.render(context)
            return html_output
        except Exception as e:
            print(f"Erreur critique lors de la génération du template HTML : {e}")
            return f"<h1>Erreur de génération de rapport</h1><p>{e}</p>"
