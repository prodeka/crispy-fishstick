from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint

from ..optimizer.controllers import OptimizationController  # type: ignore
from ..utils.inp_validator import validate_inp_file


app = typer.Typer(name="network-optimize-unified", help="Optimisation réseau unifiée (INP/YML)")
_controller = OptimizationController()


@app.command("run")
def network_optimize_unified(
    input_file: Path = typer.Argument(..., help="Fichier réseau (.inp ou .yml)"),
    method: str = typer.Option("nested", "--method", "-m", help="genetic|nested|surrogate|global|multi-tank"),
    solver: str = typer.Option("epanet", "--solver", help="epanet|lcpi|mock"),
    solvers: Optional[str] = typer.Option(None, "--solvers", help="Exécuter la commande pour plusieurs solveurs, séparés par des virgules (ex: epanet,lcpi)"),
    pression_min: Optional[float] = typer.Option(None, "--pression-min", help="Pression minimale (m)"),
    vitesse_min: Optional[float] = typer.Option(None, "--vitesse-min", help="Vitesse minimale (m/s)"),
    vitesse_max: Optional[float] = typer.Option(None, "--vitesse-max", help="Vitesse maximale (m/s)"),
    hard_vel: bool = typer.Option(False, "--hard-vel", help="Traiter la contrainte de vitesse max comme hard (rejet)"),
    price_db: Optional[Path] = typer.Option(None, "--price-db", help="Base de prix à utiliser (provenance incluse dans meta)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier JSON de sortie"),
    report: Optional[str] = typer.Option(None, "--report", help="Générer un rapport: html|md|pdf"),
    report_output: Optional[Path] = typer.Option(None, "--report-output", help="Dossier de sortie pour les rapports (défaut: même dossier que --output)"),
    show_stats: bool = typer.Option(False, "--show-stats", help="Afficher les statistiques hydrauliques après l'optimisation"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose"),
):
    """Commande d'optimisation unifiée acceptant .inp et .yml avec support des rapports HTML, Markdown et PDF."""
            # Processing input file
    
    if not input_file.exists():
        rprint(f"[red]Fichier introuvable:[/red] {input_file}")
        raise typer.Exit(code=2)
    
    # Validation et nettoyage automatique du fichier INP
    if input_file.suffix.lower() == '.inp':
        rprint("[yellow]🔍 Validation du fichier INP...[/yellow]")
        success, message = validate_inp_file(input_file)
        if success:
            rprint(f"[green]✅ {message}[/green]")
        else:
            rprint(f"[red]❌ {message}[/red]")
            if typer.confirm("Continuer malgré les problèmes ?"):
                rprint("[yellow]⚠️ Continuation avec le fichier non validé[/yellow]")
            else:
                raise typer.Exit(1)

    constraints = {
        "pressure_min_m": pression_min,
        "velocity_min_m_s": vitesse_min,
        "velocity_max_m_s": vitesse_max,
    }

    # Mode multi-solveurs
    multi_solver_list = None
    if solvers:
        multi_solver_list = [s.strip() for s in str(solvers).split(",") if s.strip()]

    if multi_solver_list:
        rprint(f"[blue]🚀 Démarrage de l'optimisation multi-solveurs: {', '.join(multi_solver_list)}[/blue]")
        rprint(f"[blue]📋 Méthode: {method}, Contraintes: pression_min={pression_min}m, vitesse_max={vitesse_max}m/s[/blue]")
        
        # Exécuter pour chaque solveur et produire un bundle d'outputs
        outputs = {}
        for i, sname in enumerate(multi_solver_list, 1):
            rprint(f"[yellow]⏳ Optimisation {i}/{len(multi_solver_list)} avec {sname}...[/yellow]")
            try:
                result = _controller.run_optimization(
                    input_path=input_file,
                    method=method,
                    solver=sname,
                    constraints=constraints,
                    hybrid_refiner=None,
                    hybrid_params=None,
                    algo_params={"hard_velocity": bool(hard_vel)},
                    price_db=str(price_db) if price_db else None,
                    verbose=verbose,
                )
                outputs[sname] = result
            except Exception as exc:
                outputs[sname] = {"error": str(exc), "meta": {"solver": sname, "method": method}}

        # Sauvegarde multi-json et un index
        if output:
            import json
            base = output
            base.parent.mkdir(parents=True, exist_ok=True)
            index = {"meta": {"solvers": multi_solver_list}, "results": {}}
            for sname, res in outputs.items():
                path_s = base.with_name(f"{base.stem}_{sname}{base.suffix}")
                with open(path_s, "w", encoding="utf-8") as f:
                    json.dump(res, f, indent=2, ensure_ascii=False)
                index["results"][sname] = str(path_s)
            # fichier index
            idx_path = base.with_name(f"{base.stem}_multi{base.suffix}")
            with open(idx_path, "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            rprint(f"[green]Résultats multi-solveurs écrits (index):[/green] {idx_path}")
            
            # Affichage des statistiques hydrauliques si demandé
            if show_stats:
                rprint("[yellow]📊 Affichage des statistiques hydrauliques pour chaque solveur...[/yellow]")
                for sname, res in outputs.items():
                    if "error" not in res:
                        rprint(f"\n[bold blue]=== Statistiques pour {sname} ===[/bold blue]")
                        _display_hydraulic_statistics(res)
            
            # Génération des rapports si demandé
            if report:
                # Déterminer le dossier de sortie des rapports
                report_dir = report_output if report_output else base.parent
                rprint(f"[yellow]📊 Génération du rapport {report.upper()}...[/yellow]")
                _generate_reports(index, outputs, report, report_dir, verbose)
        else:
            rprint("[green]Optimisation multi-solveurs terminée — résumé :[/green]")
            for sname, res in outputs.items():
                meta = res.get("meta", {})
                best = res.get("proposals", [{}])[0] if res.get("proposals") else {}
                rprint(f" {sname}: best CAPEX={best.get('CAPEX')} ok={best.get('constraints_ok')}")
        return

    # Mode mono-solveur
    rprint(f"[blue]🚀 Démarrage de l'optimisation avec {method} et {solver}...[/blue]")
    rprint(f"[blue]📋 Contraintes: pression_min={pression_min}m, vitesse_max={vitesse_max}m/s[/blue]")
    
    try:
        result = _controller.run_optimization(
            input_path=input_file,
            method=method,
            solver=solver,
            constraints=constraints,
            hybrid_refiner=None,
            hybrid_params=None,
            algo_params={"hard_velocity": bool(hard_vel)},
            price_db=str(price_db) if price_db else None,
            verbose=verbose,
        )
    except Exception as exc:
        rprint(f"[red]Erreur lors de l'optimisation:[/red] {exc}")
        raise typer.Exit(code=3)

    if output:
        import json
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        rprint(f"[green]Résultat écrit dans[/green] {output}")
        
        # Affichage des statistiques hydrauliques si demandé
        if show_stats:
            rprint("[yellow]📊 Affichage des statistiques hydrauliques...[/yellow]")
            _display_hydraulic_statistics(result)
        
        # Génération des rapports si demandé
        if report:
            # Generating report
            # Déterminer le dossier de sortie des rapports
            report_dir = report_output if report_output else output.parent
            rprint(f"[yellow]📊 Génération du rapport {report.upper()} dans {report_dir}...[/yellow]")
            try:
                _generate_reports({"meta": {"solvers": [solver]}, "results": {solver: str(output)}}, 
                               {solver: result}, report, report_dir, verbose)
                rprint(f"[green]✅ Génération du rapport terminée[/green]")
            except Exception as e:
                rprint(f"[red]❌ Erreur lors de la génération du rapport: {e}[/red]")
                if verbose:
                    import traceback
                    traceback.print_exc()
    else:
        meta = result.get("meta", {})
        best = result.get("proposals", [{}])[0] if result.get("proposals") else {}
        rprint("[green]Optimisation terminée — résumé :[/green]")
        rprint(f" method: {meta.get('method')} solver: {meta.get('solver')}")
        rprint(f" best CAPEX: {best.get('CAPEX')} constraints_ok: {best.get('constraints_ok')}")
        
        # Affichage des statistiques hydrauliques si demandé
        if show_stats:
            rprint("[yellow]📊 Affichage des statistiques hydrauliques...[/yellow]")
            _display_hydraulic_statistics(result)


def _display_hydraulic_statistics(result_data: dict):
    """Affiche les statistiques hydrauliques de manière structurée."""
    
    # Chercher les statistiques hydrauliques
    stats = None
    
    # Chercher dans la section hydraulics
    if "hydraulics" in result_data:
        hydraulics = result_data["hydraulics"]
        if "statistics" in hydraulics:
            stats = hydraulics["statistics"]
    
    # Si pas trouvé, chercher dans les propositions
    if not stats:
        proposals = result_data.get("proposals", [])
        for proposal in proposals:
            if "statistics" in proposal:
                stats = proposal["statistics"]
                break
    
    # Si pas trouvé, chercher à la racine
    if not stats and "statistics" in result_data:
        stats = result_data["statistics"]
    
    if not stats:
        rprint("[yellow]⚠️ Aucune statistique hydraulique trouvée dans les résultats[/yellow]")
        return
    
    # Affichage des statistiques
    rprint("\n" + "="*80)
    rprint("[bold green]📊 Statistiques Hydrauliques[/bold green]")
    rprint("="*80)
    
    # Pressions
    pressures = stats.get("pressures", {})
    if pressures:
        rprint(f"[bold magenta]📊 Pressions:[/bold magenta]")
        rprint(f"  • Nœuds: {pressures.get('count', 0)}")
        rprint(f"  • Min: {pressures.get('min', 0):.3f} m, Max: {pressures.get('max', 0):.3f} m")
        rprint(f"  • Moyenne: {pressures.get('mean', 0):.3f} m, Médiane: {pressures.get('median', 0):.3f} m")
        rprint(f"  • % < 10m: {pressures.get('percent_under_10m', 0):.1f}%")
    
    # Vitesses
    velocities = stats.get("velocities", {})
    if velocities:
        rprint(f"[bold blue]⚡ Vitesses:[/bold blue]")
        rprint(f"  • Conduites: {velocities.get('count', 0)}")
        rprint(f"  • Min: {velocities.get('min', 0):.3f} m/s, Max: {velocities.get('max', 0):.3f} m/s")
        rprint(f"  • Moyenne: {velocities.get('mean', 0):.3f} m/s, Médiane: {velocities.get('median', 0):.3f} m/s")
        rprint(f"  • % > 2 m/s: {velocities.get('percent_over_2ms', 0):.1f}%")
    
    # Diamètres
    diameters = stats.get("diameters", {})
    if diameters:
        rprint(f"[bold yellow]🔧 Diamètres:[/bold yellow]")
        rprint(f"  • Conduites: {diameters.get('count', 0)}")
        rprint(f"  • Min: {diameters.get('min', 0):.0f} mm, Max: {diameters.get('max', 0):.0f} mm")
        rprint(f"  • Moyenne: {diameters.get('mean', 0):.0f} mm, Médiane: {diameters.get('median', 0):.0f} mm")
    
    # Pertes de charge
    headlosses = stats.get("headlosses", {})
    if headlosses:
        rprint(f"[bold red]💧 Pertes de charge:[/bold red]")
        rprint(f"  • Conduites: {headlosses.get('count', 0)}")
        rprint(f"  • Min: {headlosses.get('min', 0):.3f} m, Max: {headlosses.get('max', 0):.3f} m")
        rprint(f"  • Moyenne: {headlosses.get('mean', 0):.3f} m, Total: {headlosses.get('total', 0):.3f} m")
    
    # Débits
    flows = stats.get("flows", {})
    if flows:
        rprint(f"[bold green]🌊 Débits:[/bold green]")
        rprint(f"  • Conduites: {flows.get('count', 0)}")
        rprint(f"  • Magnitude (absolue): Min: {flows.get('min_abs', 0):.3f} m³/s, Max: {flows.get('max_abs', 0):.3f} m³/s")
        rprint(f"  • Moyenne (absolue): {flows.get('mean_abs', 0):.3f} m³/s")
        rprint(f"  • Sens normal: {flows.get('positive_flows', 0)} conduites, Sens inverse: {flows.get('negative_flows', 0)} conduites")
        rprint(f"  • Total (conservation): {flows.get('total', 0):.3f} m³/s")
        rprint(f"  [dim]💡 Note: Débit négatif = écoulement inverse au sens défini[/dim]")
    
    # Indice de performance
    performance_index = stats.get("performance_index")
    if performance_index is not None:
        rprint(f"[bold]Indice de Performance Hydraulique:[/bold] {performance_index:.3f}")
    
    rprint("="*80)


def _generate_reports(index_data: dict, outputs: dict, report_format: str, output_dir: Path, verbose: bool):
    """Génère les rapports dans le format demandé."""
    try:
        from ...reporting.report_generator import ReportGenerator
        from ...reporting.markdown_generator import MarkdownGenerator
        from ...reporting.pdf_generator import PDFGenerator
        
        # Créer le dossier de sortie si nécessaire
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Chemin vers les templates
        template_dir = Path(__file__).parent.parent.parent.parent / "lcpi" / "reporting" / "templates"
        
        if report_format.lower() == "html":
            rprint("[yellow]📝 Génération du rapport HTML...[/yellow]")
            # Rapport HTML avec onglet détaillé des résultats
            generator = ReportGenerator(template_dir)
            html_content = generator._generate_multi_solver_report(
                index_data, 
                {"nom_projet": "Optimisation Réseau"}, 
                "1.0.0"
            )
            
            # Sauvegarder le rapport HTML
            html_path = output_dir / f"rapport_optimisation_{index_data['meta']['solvers'][0]}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            rprint(f"[green]✅ Rapport HTML généré:[/green] {html_path}")
            
        elif report_format.lower() == "md":
            rprint("[yellow]📝 Génération du rapport Markdown...[/yellow]")
            # Rapport Markdown
            md_generator = MarkdownGenerator()
            md_content = md_generator.generate_optimization_report(index_data, outputs)
            
            md_path = output_dir / f"rapport_optimisation_{index_data['meta']['solvers'][0]}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            rprint(f"[green]✅ Rapport Markdown généré:[/green] {md_path}")
            
        elif report_format.lower() == "pdf":
            rprint("[yellow]📝 Génération du rapport PDF...[/yellow]")
            # Rapport PDF
            pdf_generator = PDFGenerator()
            pdf_content = pdf_generator.generate_optimization_report(index_data, outputs)
            
            pdf_path = output_dir / f"rapport_optimisation_{index_data['meta']['solvers'][0]}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(pdf_content)
            rprint(f"[green]✅ Rapport PDF généré:[/green] {pdf_path}")
            
        else:
            rprint(f"[yellow]⚠️ Format de rapport non reconnu:[/yellow] {report_format}")
            rprint("[yellow]Formats supportés: html, md, pdf[/yellow]")
            
    except ImportError as e:
        rprint(f"[red]❌ Erreur: Module de rapport non disponible:[/red] {e}")
        rprint("[yellow]Les rapports ne peuvent pas être générés[/yellow]")
    except Exception as e:
        rprint(f"[red]❌ Erreur lors de la génération du rapport:[/red] {e}")
        if verbose:
            import traceback
            traceback.print_exc()


