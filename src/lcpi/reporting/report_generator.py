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
        # Conserver le chemin des templates pour charger le CSS
        self.template_dir = Path(template_dir)
        # On pourrait ajouter des filtres personnalisés ici si nécessaire

    def _detect_multi_solver_data(self, logs_data: list) -> tuple[bool, dict]:
        """
        Détecte si les données contiennent des résultats multi-solveurs.
        
        Args:
            logs_data: Liste des données de logs
            
        Returns:
            Tuple (is_multi_solver, solver_data)
        """
        if len(logs_data) == 1:
            data = logs_data[0]
            # Vérifier si c'est un fichier de métadonnées multi-solveurs
            if isinstance(data, dict) and "meta" in data and "results" in data:
                meta = data.get("meta", {})
                results = data.get("results", {})
                
                if "solvers" in meta and isinstance(results, dict):
                    solvers = meta["solvers"]
                    if len(solvers) > 1 and all(solver in results for solver in solvers):
                        # C'est un fichier multi-solveurs, charger les données de chaque solveur
                        solver_data = {}
                        for solver in solvers:
                            result_path = results.get(solver)
                            if result_path and Path(result_path).exists():
                                try:
                                    with open(result_path, 'r', encoding='utf-8') as f:
                                        solver_data[solver] = json.load(f)
                                except (IOError, json.JSONDecodeError):
                                    print(f"Avertissement : Impossible de charger les données pour {solver}")
                                    solver_data[solver] = {}
                            else:
                                solver_data[solver] = {}
                        
                        return True, {
                            "solvers": solvers,
                            "solver_data": solver_data,
                            "meta": meta
                        }
        
        return False, {}

    def _detect_multi_solver_data(self, logs_data: list) -> tuple[bool, dict]:
        """
        Détecte si les données contiennent des résultats multi-solveurs.
        
        Args:
            logs_data: Liste des données de logs
            
        Returns:
            Tuple (is_multi_solver, solver_data)
        """
        if len(logs_data) == 1:
            data = logs_data[0]
            # Vérifier si c'est un fichier de métadonnées multi-solveurs
            if isinstance(data, dict) and "meta" in data and "results" in data:
                meta = data.get("meta", {})
                results = data.get("results", {})
                
                if "solvers" in meta and isinstance(results, dict):
                    solvers = meta["solvers"]
                    if len(solvers) > 1 and all(solver in results for solver in solvers):
                        # C'est un fichier multi-solveurs, charger les données de chaque solveur
                        solver_data = {}
                        for solver in solvers:
                            result_path = results.get(solver)
                            if result_path and Path(result_path).exists():
                                try:
                                    with open(result_path, 'r', encoding='utf-8') as f:
                                        solver_data[solver] = json.load(f)
                                except (IOError, json.JSONDecodeError):
                                    print(f"Avertissement : Impossible de charger les données pour {solver}")
                                    solver_data[solver] = {}
                            else:
                                solver_data[solver] = {}
                        
                        return True, {
                            "solvers": solvers,
                            "solver_data": solver_data,
                            "meta": meta
                        }
        
        return False, {}

    def generate_html_report(
        self,
        selected_logs_paths: list[Path],
        project_metadata: dict,
        lcpi_version: str = "1.0.0"  # Pourrait être récupéré dynamiquement
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

        # 2. Vérifier si c'est un rapport multi-solveurs
        is_multi_solver, multi_solver_data = self._detect_multi_solver_data(logs_data)
        
        if is_multi_solver:
            # Utiliser le template multi-solveurs
            return self._generate_multi_solver_report(multi_solver_data, project_metadata, lcpi_version)
        
        # 3. Normaliser les logs pour le template simple
        normalized_logs = []
        now_iso = datetime.datetime.now().isoformat()
        for item in logs_data:
            if isinstance(item, dict) and ("meta" in item or "proposals" in item):
                meta = item.get("meta", {})
                integrity = item.get("integrity", {})
                proposals = item.get("proposals", []) or []
                first_prop = proposals[0] if proposals else {}
                hyd = item.get("hydraulics", {})
                resume = {
                    "constraints": meta.get("constraints", {}),
                    "constraints_ok": first_prop.get("constraints_ok"),
                    "min_pressure_m": (first_prop.get("metrics", {}) or {}).get("min_pressure_m") or first_prop.get("min_pressure_m"),
                    "max_velocity_m_s": (first_prop.get("metrics", {}) or {}).get("max_velocity_m_s") or first_prop.get("max_velocity_m_s"),
                    "capex": first_prop.get("CAPEX"),
                    "nodes_count": len(hyd.get("pressures", {}) or hyd.get("pressures_m", {}) or {}),
                    "links_count": len(hyd.get("velocities", {}) or hyd.get("velocities_m_s", {}) or hyd.get("flows_m3_s", {}) or {}),
                }
                normalized_logs.append({
                    "titre_calcul": meta.get("method", "Optimisation Réseau"),
                    "id": integrity.get("checksum") or integrity.get("signature") or meta.get("source", "log"),
                    "timestamp": integrity.get("signed_at") or now_iso,
                    "commande_executee": meta.get("command") or "lcpi aep network-optimize-unified",
                    "donnees_resultat": item,
                    "resume": resume,
                    "transparence_mathematique": [],
                })
            elif isinstance(item, dict):
                # Supposer déjà au bon format ou format inconnu
                normalized_logs.append({
                    "titre_calcul": item.get("titre_calcul", "Calcul LCPI"),
                    "id": item.get("id", "log"),
                    "timestamp": item.get("timestamp", now_iso),
                    "commande_executee": item.get("commande_executee", "lcpi"),
                    "donnees_resultat": item,
                    "resume": item.get("resume"),
                    "transparence_mathematique": item.get("transparence_mathematique", []),
                })
            else:
                normalized_logs.append({
                    "titre_calcul": "Calcul LCPI",
                    "id": "log",
                    "timestamp": now_iso,
                    "commande_executee": "lcpi",
                    "donnees_resultat": item,
                    "resume": None,
                    "transparence_mathematique": [],
                })

        # 4. Préparer le contexte pour Jinja2
        # S'assurer que le nom du projet est renseigné
        if project_metadata is None:
            project_metadata = {}
        if "nom_projet" not in project_metadata:
            name_val = project_metadata.get("name") or project_metadata.get("nom") or "Projet LCPI"
            project_metadata["nom_projet"] = name_val

        # Charger le CSS et l'injecter inline
        inline_css = ""
        try:
            css_path = self.template_dir / "style.css"
            if css_path.exists():
                inline_css = css_path.read_text(encoding="utf-8")
        except Exception:
            inline_css = ""

        context = {
            "projet_metadata": project_metadata,
            "auteurs": project_metadata.get("auteurs", [{"nom": "Non spécifié", "role": ""}]),
            "generation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "logs_selectionnes": normalized_logs,
            "version_lcpi": lcpi_version,
            "inline_css": inline_css,
        }

        # 5. Choisir le template selon le nombre de logs
        try:
            preferred_candidates = []
            if len(normalized_logs) > 1:
                preferred_candidates = ["optimisation_tabs.jinja2", "optimisation_unified.jinja2", "optimisation_tank.jinja2"]
            else:
                preferred_candidates = ["optimisation_unified.jinja2", "optimisation_tank.jinja2"]
            template = None
            for preferred in preferred_candidates:
                try:
                    template = self.env.get_template(preferred)
                    break
                except Exception:
                    template = None
            if template is None:
                template = self.env.get_template("base_simple.html")
        except Exception:
            template = self.env.get_template("base_simple.html")
        try:
            html_output = template.render(context)
            return html_output
        except Exception as e:
            print(f"Erreur critique lors de la génération du template HTML : {e}")
            return f"<h1>Erreur de génération de rapport</h1><p>{e}</p>"

    def _generate_multi_solver_report(
        self,
        multi_solver_data: dict,
        project_metadata: dict,
        lcpi_version: str
    ) -> str:
        """
        Génère un rapport multi-solveurs.
        
        Args:
            multi_solver_data: Données multi-solveurs
            project_metadata: Métadonnées du projet
            lcpi_version: Version de LCPI
            
        Returns:
            Contenu HTML du rapport
        """
        # Préparer le contexte pour le template multi-solveurs
        if project_metadata is None:
            project_metadata = {}
        if "nom_projet" not in project_metadata:
            name_val = project_metadata.get("name") or project_metadata.get("nom") or "Projet LCPI"
            project_metadata["nom_projet"] = name_val

        # Charger le CSS et l'injecter inline
        inline_css = ""
        try:
            css_path = self.template_dir / "style.css"
            if css_path.exists():
                inline_css = css_path.read_text(encoding="utf-8")
        except Exception:
            inline_css = ""

        context = {
            "projet_metadata": project_metadata,
            "generation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "version_lcpi": lcpi_version,
            "inline_css": inline_css,
            "solvers": multi_solver_data.get("meta", {}).get("solvers", []),
            "solver_data": multi_solver_data.get("results", {}),
            "meta": multi_solver_data.get("meta", {})
        }

        # Utiliser le template multi-solveurs avec onglets
        try:
            # Essayer d'abord le template avec onglets
            try:
                template = self.env.get_template("optimisation_with_tabs.jinja2")
            except:
                # Fallback vers le template standard
                template = self.env.get_template("multi_solver_comparison.jinja2")
            
            html_output = template.render(context)
            return html_output
        except Exception as e:
            print(f"Erreur critique lors de la génération du rapport multi-solveurs : {e}")
            return f"<h1>Erreur de génération de rapport multi-solveurs</h1><p>{e}</p>"
