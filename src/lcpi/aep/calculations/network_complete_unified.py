"""
Commande network-complete-unified pour l'analyse complète de réseaux.

Cette commande utilise l'architecture Strategy Pattern pour permettre
l'utilisation de différents solveurs hydrauliques (LCPI Hardy-Cross, EPANET, etc.)
de manière interchangeable.
"""

import typer
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
import json

from ..core.solvers import SolverFactory
from ..core.pydantic_models import ReseauCompletConfig, valider_reseau_seul
from ..utils.rich_ui import RichUI, console
# from ..utils.exporters import export_results  # Commenté car non disponible


app = typer.Typer()


@app.command()
def network_complete_unified(
    input_file: Path = typer.Argument(..., help="Fichier YAML réseau complet à analyser"),
    solver: str = typer.Option("lcpi", "--solver", "-s", help="Solveur hydraulique (lcpi/epanet)"),
    mode: str = typer.Option("auto", "--mode", "-m", help="Mode de calcul (auto/simple/enhanced)"),
    export: str = typer.Option("json", "--export", "-e", help="Format d'export (json/yaml/csv/html)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """
    🌐 Analyse complète de réseau avec choix de solveur hydraulique
    
    Cette commande effectue une analyse complète d'un réseau d'eau potable :
    - Validation de la connectivité et des données
    - Calcul des débits par le solveur choisi
    - Diagnostics et vérifications de contraintes
    - Export des résultats dans le format demandé
    
    L'utilisateur peut choisir le solveur hydraulique :
    - lcpi : Solveur interne rapide (Hardy-Cross)
    - epanet : Solveur EPA plus précis mais plus lent
    """
    try:
        # 1. Charger et valider les données d'entrée
        with console.status("[bold green]Chargement des données..."):
            if not input_file.exists():
                RichUI.print_error(f"❌ Fichier d'entrée introuvable: {input_file}")
                raise typer.Exit(code=1)
            
            with open(input_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Valider avec Pydantic
            try:
                reseau_config = valider_reseau_seul(data)
                RichUI.print_success(f"✅ Réseau validé: {reseau_config.nom}")
            except Exception as e:
                RichUI.print_error(f"❌ Erreur de validation: {e}")
                raise typer.Exit(code=1)
        
        # 2. Sélectionner le solveur
        with console.status("[bold blue]Sélection du solveur..."):
            try:
                hydraulic_solver = SolverFactory.get_solver(solver)
                solver_info = hydraulic_solver.get_solver_info()
                
                if verbose:
                    RichUI.print_info(f"🔧 Solveur sélectionné: {solver_info['name']} v{solver_info['version']}")
                    RichUI.print_info(f"📝 {solver_info['description']}")
                    RichUI.print_info(f"⚡ {solver_info['capabilities']}")
            except ValueError as e:
                RichUI.print_error(f"❌ Erreur de sélection du solveur: {e}")
                raise typer.Exit(code=1)
        
        # 3. Valider la compatibilité du réseau avec le solveur
        with console.status("[bold yellow]Validation de compatibilité..."):
            validation = SolverFactory.validate_solver_choice(solver, data)
            
            if not validation["compatible"]:
                RichUI.print_error("❌ Le réseau n'est pas compatible avec le solveur choisi")
                for error in validation["validation"]["errors"]:
                    RichUI.print_error(f"   - {error}")
                raise typer.Exit(code=1)
            
            RichUI.print_success("✅ Réseau compatible avec le solveur")
        
        # 4. Exécuter la simulation hydraulique
        with console.status("[bold magenta]Simulation hydraulique en cours..."):
            try:
                simulation_results = hydraulic_solver.run_simulation(data)
                
                if simulation_results["status"] == "failure":
                    RichUI.print_error("❌ Échec de la simulation hydraulique")
                    for error in simulation_results.get("errors", []):
                        RichUI.print_error(f"   - {error}")
                    raise typer.Exit(code=1)
                
                RichUI.print_success("✅ Simulation hydraulique terminée")
                
            except Exception as e:
                RichUI.print_error(f"❌ Erreur lors de la simulation: {e}")
                raise typer.Exit(code=1)
        
        # 5. Post-traitement et diagnostics
        with console.status("[bold cyan]Post-traitement et diagnostics..."):
            diagnostics = _perform_post_processing(simulation_results, reseau_config)
            RichUI.print_success("✅ Post-traitement terminé")
        
        # 6. Préparer les résultats finaux
        results = {
            "valeurs": {
                "debit_total_m3_s": sum(simulation_results["flows"].values()),
                "pression_moyenne_mce": sum(simulation_results["pressures"].values()) / len(simulation_results["pressures"]),
                "vitesse_moyenne_m_s": sum(simulation_results["velocities"].values()) / len(simulation_results["velocities"]),
                "longueur_totale_m": sum(conduit.longueur_m for conduit in reseau_config.conduites.values())
            },
            "diagnostics": {
                "connectivite_ok": diagnostics["connectivite_ok"],
                "pression_ok": diagnostics["pression_ok"],
                "vitesse_ok": diagnostics["vitesse_ok"],
                "convergence": simulation_results["convergence"]["converge"],
                "solver_utilise": solver,
                "temps_calcul_s": simulation_results.get("execution_time", 0.0)
            },
            "iterations": {
                "total": simulation_results["convergence"].get("iterations", 0),
                "tolerance_atteinte": simulation_results["convergence"].get("tolerance_atteinte", 0.0),
                "boucles_detectees": simulation_results["diagnostics"].get("boucles_detectees", 0)
            },
            "details": {
                "pressions_par_noeud": simulation_results["pressures"],
                "debits_par_conduite": simulation_results["flows"],
                "vitesses_par_conduite": simulation_results["velocities"],
                "diagnostics_complets": simulation_results["diagnostics"]
            }
        }
        
        
        
        # 8. Export des résultats
        if output:
            export_results(results, export, output, verbose)
            RichUI.print_success(f"✅ Résultats exportés: {output}")
        else:
            # Affichage des résultats principaux
            RichUI.print_success(f"🌐 Analyse terminée pour le réseau: {reseau_config.nom}")
            RichUI.print_info(f"📊 Débit total: {results['valeurs']['debit_total_m3_s']:.3f} m³/s")
            RichUI.print_info(f"📏 Pression moyenne: {results['valeurs']['pression_moyenne_mce']:.1f} mCE")
            RichUI.print_info(f"⚡ Vitesse moyenne: {results['valeurs']['vitesse_moyenne_m_s']:.2f} m/s")
            RichUI.print_info(f"🔄 Convergence: {'✅' if results['diagnostics']['convergence'] else '❌'}")
        
    except Exception as e:
        RichUI.print_error(f"❌ Erreur lors de l'analyse: {e}")
        raise typer.Exit(code=1)


def _perform_post_processing(simulation_results: Dict[str, Any], 
                           reseau_config: ReseauCompletConfig) -> Dict[str, Any]:
    """
    Effectue le post-traitement des résultats de simulation.
    
    Args:
        simulation_results: Résultats de la simulation hydraulique
        reseau_config: Configuration du réseau validée
        
    Returns:
        Dictionnaire des diagnostics post-traitement
    """
    diagnostics = {
        "connectivite_ok": True,  # Déjà validé par Pydantic
        "pression_ok": True,
        "vitesse_ok": True,
        "violations": []
    }
    
    # Vérifier les pressions
    pressions = simulation_results["pressures"]
    for node_id, pression in pressions.items():
        if node_id in reseau_config.noeuds:
            noeud = reseau_config.noeuds[node_id]
            if pression < noeud.pression_min_mce:
                diagnostics["pression_ok"] = False
                diagnostics["violations"].append({
                    "type": "pression_min",
                    "element": node_id,
                    "valeur": pression,
                    "seuil": noeud.pression_min_mce
                })
            elif pression > noeud.pression_max_mce:
                diagnostics["pression_ok"] = False
                diagnostics["violations"].append({
                    "type": "pression_max",
                    "element": node_id,
                    "valeur": pression,
                    "seuil": noeud.pression_max_mce
                })
    
    # Vérifier les vitesses (critères généraux)
    vitesses = simulation_results["velocities"]
    for conduit_id, vitesse in vitesses.items():
        if vitesse < 0.5:  # Vitesse minimale recommandée
            diagnostics["vitesse_ok"] = False
            diagnostics["violations"].append({
                "type": "vitesse_min",
                "element": conduit_id,
                "valeur": vitesse,
                "seuil": 0.5
            })
        elif vitesse > 2.5:  # Vitesse maximale recommandée
            diagnostics["vitesse_ok"] = False
            diagnostics["violations"].append({
                "type": "vitesse_max",
                "element": conduit_id,
                "valeur": vitesse,
                "seuil": 2.5
            })
    
    return diagnostics


if __name__ == "__main__":
    app()


def load_yaml_config(file_path: Path) -> Dict[str, Any]:
    """Charge un fichier YAML."""
    import yaml
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise ValueError(f"Fichier non trouvé: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Erreur de parsing YAML dans {file_path}: {e}")


def export_results(data: Dict[str, Any], format: str, output_path: Path, verbose: bool = False):
    """Exporte les données dans le format spécifié."""
    import json
    import yaml
    
    try:
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif format == "yaml":
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, indent=4, allow_unicode=True)
        elif format == "csv":
            _export_to_csv(data, output_path)
        elif format == "html":
            _export_to_html(data, output_path)
        else:
            raise ValueError(f"Format d'export '{format}' non supporté.")
            
        if verbose:
            RichUI.print_info(f"Export au format {format} vers {output_path}")
            
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'export: {e}")


def _export_to_csv(data: Dict[str, Any], output_path: Path):
    """Exporte les données au format CSV."""
    import csv
    
    # Extraire les données principales
    valeurs = data.get("valeurs", {})
    diagnostics = data.get("diagnostics", {})
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # En-têtes
        writer.writerow(["Section", "Paramètre", "Valeur"])
        
        # Valeurs principales
        for key, value in valeurs.items():
            writer.writerow(["Valeurs", key, value])
        
        # Diagnostics
        for key, value in diagnostics.items():
            writer.writerow(["Diagnostics", key, value])


def _export_to_html(data: Dict[str, Any], output_path: Path):
    """Exporte les données au format HTML."""
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Résultats Analyse Réseau</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin: 20px 0; padding: 10px; border: 1px solid #ccc; }}
        .success {{ color: green; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
    </style>
</head>
<body>
    <h1>Résultats de l'Analyse Réseau</h1>
    
    <div class="section">
        <h2>Valeurs Principales</h2>
        <ul>
"""
    
    # Ajouter les valeurs principales
    for key, value in data.get("valeurs", {}).items():
        html_content += f"            <li><strong>{key}:</strong> {value}</li>\n"
    
    html_content += """
        </ul>
    </div>
    
    <div class="section">
        <h2>Diagnostics</h2>
        <ul>
"""
    
    # Ajouter les diagnostics
    for key, value in data.get("diagnostics", {}).items():
        status_class = "success" if value else "error"
        html_content += f"            <li class='{status_class}'><strong>{key}:</strong> {value}</li>\n"
    
    html_content += """
        </ul>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
