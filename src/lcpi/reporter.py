"""
Module de génération de rapports global avec Pandoc pour tous les plugins LCPI

Ce module fournit une interface unifiée pour générer des rapports
professionnels avec transparence mathématique pour tous les plugins :
- AEP (Alimentation en Eau Potable)
- CM (Construction Métallique)
- Bois (Structures en Bois)
- Béton (Béton Armé)
- Hydrodrain (Hydrologie et Hydraulique)
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None

class GlobalReportBuilder:
    """
    Générateur de rapports global avec Pandoc pour tous les plugins LCPI.
    
    Fonctionnalités :
    - Support multi-format (PDF, DOCX, HTML, LaTeX)
    - Transparence mathématique avec formules LaTeX
    - Templates spécifiques par plugin
    - Graphiques et visualisations
    - Export des calculs détaillés
    """
    
    def __init__(self, project_dir: str = "."):
        """
        Initialise le générateur de rapports.
        
        Args:
            project_dir: Répertoire du projet à analyser
        """
        self.project_dir = Path(project_dir)
        self.templates_dir = Path(__file__).parent / "templates"
        self.output_dir = self.project_dir / "reports"
        self.output_dir.mkdir(exist_ok=True)
        
        # Vérifier la disponibilité de Pandoc
        self.pandoc_available = self._check_pandoc()
        
    def _check_pandoc(self) -> bool:
        """Vérifie si Pandoc est disponible."""
        try:
            result = subprocess.run(
                ["pandoc", "--version"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def analyze_project(self) -> Dict[str, Any]:
        """
        Analyse le projet et collecte les données de tous les plugins.
        
        Returns:
            Dict: Données collectées du projet
        """
        project_data = {
            "metadata": {
                "name": self.project_dir.name,
                "analysis_date": datetime.now().isoformat(),
                "plugins": []
            },
            "results": {}
        }
        
        # Analyser les plugins disponibles
        plugins = self._detect_plugins()
        project_data["metadata"]["plugins"] = plugins
        
        # Collecter les résultats par plugin
        for plugin in plugins:
            plugin_results = self._collect_plugin_results(plugin)
            if plugin_results:
                project_data["results"][plugin] = plugin_results
        
        return project_data
    
    def _detect_plugins(self) -> List[str]:
        """Détecte les plugins utilisés dans le projet."""
        plugins = []
        
        # Vérifier les fichiers de configuration
        config_files = [
            "config.yml", "config.yaml", "project.yml", "project.yaml"
        ]
        
        for config_file in config_files:
            config_path = self.project_dir / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        if config and 'plugins' in config:
                            plugins.extend(config['plugins'])
                except Exception as e:
                    if console:
                        console.print(f"⚠️ Erreur lecture {config_file}: {e}")
        
        # Vérifier les dossiers de données
        data_dirs = ["data", "src", "calculations"]
        for data_dir in data_dirs:
            data_path = self.project_dir / data_dir
            if data_path.exists():
                for subdir in data_path.iterdir():
                    if subdir.is_dir():
                        plugin_name = subdir.name.lower()
                        if plugin_name in ['aep', 'cm', 'bois', 'beton', 'hydro', 'hydrodrain']:
                            if plugin_name not in plugins:
                                plugins.append(plugin_name)
        
        return list(set(plugins))
    
    def _collect_plugin_results(self, plugin: str) -> Optional[Dict[str, Any]]:
        """Collecte les résultats d'un plugin spécifique."""
        try:
            if plugin == "aep":
                return self._collect_aep_results()
            elif plugin == "cm":
                return self._collect_cm_results()
            elif plugin == "bois":
                return self._collect_bois_results()
            elif plugin == "beton":
                return self._collect_beton_results()
            elif plugin == "hydro" or plugin == "hydrodrain":
                return self._collect_hydro_results()
            else:
                return None
        except Exception as e:
            if console:
                console.print(f"⚠️ Erreur collecte {plugin}: {e}")
            return None
    
    def _collect_aep_results(self) -> Dict[str, Any]:
        """Collecte les résultats AEP."""
        results = {
            "plugin": "aep",
            "calculations": {},
            "files": []
        }
        
        # Chercher les fichiers de résultats AEP
        aep_files = list(self.project_dir.rglob("*aep*"))
        aep_files.extend(list(self.project_dir.rglob("*population*")))
        aep_files.extend(list(self.project_dir.rglob("*demand*")))
        aep_files.extend(list(self.project_dir.rglob("*network*")))
        aep_files.extend(list(self.project_dir.rglob("*reservoir*")))
        aep_files.extend(list(self.project_dir.rglob("*pumping*")))
        
        for file_path in aep_files:
            if file_path.is_file():
                results["files"].append(str(file_path.relative_to(self.project_dir)))
        
        return results
    
    def _collect_cm_results(self) -> Dict[str, Any]:
        """Collecte les résultats CM."""
        results = {
            "plugin": "cm",
            "calculations": {},
            "files": []
        }
        
        # Chercher les fichiers de résultats CM
        cm_files = list(self.project_dir.rglob("*cm*"))
        cm_files.extend(list(self.project_dir.rglob("*construction*")))
        cm_files.extend(list(self.project_dir.rglob("*metallique*")))
        
        for file_path in cm_files:
            if file_path.is_file():
                results["files"].append(str(file_path.relative_to(self.project_dir)))
        
        return results
    
    def _collect_bois_results(self) -> Dict[str, Any]:
        """Collecte les résultats Bois."""
        results = {
            "plugin": "bois",
            "calculations": {},
            "files": []
        }
        
        # Chercher les fichiers de résultats Bois
        bois_files = list(self.project_dir.rglob("*bois*"))
        bois_files.extend(list(self.project_dir.rglob("*wood*")))
        
        for file_path in bois_files:
            if file_path.is_file():
                results["files"].append(str(file_path.relative_to(self.project_dir)))
        
        return results
    
    def _collect_beton_results(self) -> Dict[str, Any]:
        """Collecte les résultats Béton."""
        results = {
            "plugin": "beton",
            "calculations": {},
            "files": []
        }
        
        # Chercher les fichiers de résultats Béton
        beton_files = list(self.project_dir.rglob("*beton*"))
        beton_files.extend(list(self.project_dir.rglob("*concrete*")))
        beton_files.extend(list(self.project_dir.rglob("*bael*")))
        
        for file_path in beton_files:
            if file_path.is_file():
                results["files"].append(str(file_path.relative_to(self.project_dir)))
        
        return results
    
    def _collect_hydro_results(self) -> Dict[str, Any]:
        """Collecte les résultats Hydrodrain."""
        results = {
            "plugin": "hydrodrain",
            "calculations": {},
            "files": []
        }
        
        # Chercher les fichiers de résultats Hydrodrain
        hydro_files = list(self.project_dir.rglob("*hydro*"))
        hydro_files.extend(list(self.project_dir.rglob("*drain*")))
        hydro_files.extend(list(self.project_dir.rglob("*hydraulique*")))
        
        for file_path in hydro_files:
            if file_path.is_file():
                results["files"].append(str(file_path.relative_to(self.project_dir)))
        
        return results
    
    def generate_report(self, output_format: str = "pdf") -> str:
        """
        Génère un rapport complet du projet.
        
        Args:
            output_format: Format de sortie (pdf, docx, html, latex)
            
        Returns:
            str: Chemin du fichier de rapport généré
        """
        if not self.pandoc_available:
            raise RuntimeError("Pandoc n'est pas disponible. Veuillez l'installer.")
        
        # Analyser le projet
        project_data = self.analyze_project()
        
        # Générer le contenu Markdown
        markdown_content = self._generate_markdown_content(project_data)
        
        # Créer le fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(markdown_content)
            temp_md_file = f.name
        
        # Générer le rapport avec Pandoc
        output_file = self.output_dir / f"rapport_projet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
        
        pandoc_cmd = [
            "pandoc",
            temp_md_file,
            "-o", str(output_file)
        ]
        
        # Ajouter les options selon le format
        if output_format == "pdf":
            pandoc_cmd.extend(["--pdf-engine=xelatex", "--toc", "--number-sections"])
        elif output_format == "docx":
            pandoc_cmd.extend(["--reference-doc=template.docx"] if (self.templates_dir / "template.docx").exists() else [])
        elif output_format == "html":
            pandoc_cmd.extend(["--standalone", "--css=style.css"] if (self.templates_dir / "style.css").exists() else [])
        
        try:
            subprocess.run(pandoc_cmd, check=True)
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_md_file)
            
            if console:
                console.print(f"✅ Rapport généré: {output_file}")
            
            return str(output_file)
            
        except subprocess.CalledProcessError as e:
            # Nettoyer le fichier temporaire
            os.unlink(temp_md_file)
            raise RuntimeError(f"Erreur lors de la génération du rapport: {e}")
    
    def _generate_markdown_content(self, project_data: Dict[str, Any]) -> str:
        """Génère le contenu Markdown du rapport."""
        content = []
        
        # En-tête
        content.append("# Rapport de Projet LCPI")
        content.append("")
        content.append(f"**Date d'analyse:** {project_data['metadata']['analysis_date']}")
        content.append(f"**Projet:** {project_data['metadata']['name']}")
        content.append("")
        
        # Résumé
        content.append("## Résumé Exécutif")
        content.append("")
        plugins_count = len(project_data['metadata']['plugins'])
        content.append(f"Ce projet utilise **{plugins_count} plugin(s)** LCPI :")
        for plugin in project_data['metadata']['plugins']:
            content.append(f"- {plugin.upper()}")
        content.append("")
        
        # Détails par plugin
        for plugin, results in project_data['results'].items():
            content.append(f"## Plugin {plugin.upper()}")
            content.append("")
            
            if results.get('files'):
                content.append("### Fichiers détectés")
                content.append("")
                for file_path in results['files'][:10]:  # Limiter à 10 fichiers
                    content.append(f"- `{file_path}`")
                if len(results['files']) > 10:
                    content.append(f"- ... et {len(results['files']) - 10} autres fichiers")
                content.append("")
            
            if results.get('calculations'):
                content.append("### Calculs effectués")
                content.append("")
                for calc_name, calc_result in results['calculations'].items():
                    content.append(f"#### {calc_name}")
                    content.append("")
                    if isinstance(calc_result, dict):
                        for key, value in calc_result.items():
                            if isinstance(value, (int, float)):
                                content.append(f"- **{key}:** {value}")
                            else:
                                content.append(f"- **{key}:** {str(value)}")
                    content.append("")
            
            # Ajouter le contenu spécifique au plugin
            try:
                from .templates.plugin_templates import generate_plugin_report_content
                plugin_content = generate_plugin_report_content(plugin, results)
                if plugin_content:
                    content.append("### Formules et Méthodes")
                    content.append("")
                    content.append(plugin_content)
                    content.append("")
            except ImportError:
                content.append("### Formules et Méthodes")
                content.append("")
                content.append("*Templates spécifiques non disponibles pour ce plugin*")
                content.append("")
        
        # Formules mathématiques (exemple)
        content.append("## Formules Mathématiques")
        content.append("")
        content.append("### Calcul de population (Malthus)")
        content.append("")
        content.append("$$P(t) = P_0 \\times (1 + r)^t$$")
        content.append("")
        content.append("Où :")
        content.append("- $P(t)$ : Population à l'année $t$")
        content.append("- $P_0$ : Population initiale")
        content.append("- $r$ : Taux de croissance annuel")
        content.append("- $t$ : Nombre d'années")
        content.append("")
        
        content.append("### Calcul de demande en eau")
        content.append("")
        content.append("$$Q_{brut} = \\frac{P \\times D \\times C_p}{\\eta_t}$$")
        content.append("")
        content.append("Où :")
        content.append("- $Q_{brut}$ : Besoin brut en m³/j")
        content.append("- $P$ : Population")
        content.append("- $D$ : Dotation en L/hab/j")
        content.append("- $C_p$ : Coefficient de pointe")
        content.append("- $\\eta_t$ : Rendement technique")
        content.append("")
        
        # Conclusion
        content.append("## Conclusion")
        content.append("")
        content.append("Ce rapport a été généré automatiquement par LCPI-CLI.")
        content.append("")
        content.append("Pour plus d'informations, consultez la documentation :")
        content.append("- [Documentation LCPI](https://github.com/lcpi-cli/docs)")
        content.append("- [Guide d'utilisation](https://github.com/lcpi-cli/guide)")
        content.append("")
        
        return "\n".join(content)

def run_analysis_and_generate_report(project_dir: str, output_format: str = "pdf") -> str:
    """
    Fonction principale pour analyser un projet et générer un rapport.
    
    Args:
        project_dir: Répertoire du projet à analyser
        output_format: Format de sortie (pdf, docx, html, latex)
        
    Returns:
        str: Chemin du fichier de rapport généré
    """
    try:
        # Initialiser le générateur
        builder = GlobalReportBuilder(project_dir)
        
        # Vérifier Pandoc
        if not builder.pandoc_available:
            if console:
                console.print(Panel(
                    "❌ Pandoc n'est pas disponible.\n\n"
                    "Pour installer Pandoc :\n"
                    "- Windows: https://pandoc.org/installing.html\n"
                    "- Linux: sudo apt-get install pandoc\n"
                    "- macOS: brew install pandoc",
                    title="Erreur Pandoc",
                    border_style="red"
                ))
            raise RuntimeError("Pandoc n'est pas disponible")
        
        # Générer le rapport
        report_file = builder.generate_report(output_format)
        
        if console:
            console.print(Panel(
                f"✅ Rapport généré avec succès !\n\n"
                f"📄 Fichier: {report_file}\n"
                f"📁 Format: {output_format.upper()}\n"
                f"📊 Plugins analysés: {len(builder.analyze_project()['metadata']['plugins'])}",
                title="Génération de Rapport",
                border_style="green"
            ))
        
        return report_file
        
    except Exception as e:
        if console:
            console.print(Panel(
                f"❌ Erreur lors de la génération du rapport:\n{str(e)}",
                title="Erreur",
                border_style="red"
            ))
        raise