#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnose_flow_conservation.py
----------------------------
Script autonome pour diagnostiquer les violations de conservation de masse
dans les réseaux EPANET/WNTR.

Ce script automatise le processus de diagnostic en:
1. Simulant le réseau brut avec EPANET
2. Comparant avec les résultats d'optimisation
3. Isolant les problèmes via sous-ensembles de conduites
4. Générant des rapports détaillés

Usage:
    python tools/diagnose_flow_conservation.py <network.inp> [options]
    python tools/diagnose_flow_conservation.py results/optimization.json [options]

Dépendances:
    - wntr, pandas, matplotlib, numpy
    - check_flows.py (dans le même dossier)
"""

import argparse
import json
import sys
import subprocess
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional, Tuple
import math

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("diagnose_flow_conservation")


class FlowConservationDiagnostic:
    """Diagnostic de conservation des débits pour réseaux hydrauliques."""
    
    def __init__(self, inp_path: Path, results_dir: Path = Path("results")):
        self.inp_path = inp_path
        self.results_dir = results_dir
        self.results_dir.mkdir(exist_ok=True)
        
    def run_epanet_simulation(self) -> Dict[str, Any]:
        """Exécute une simulation EPANET unique via CLI LCPI."""
        logger.info("🚀 Simulation EPANET unique...")
        
        cmd = [
            sys.executable, "-m", "lcpi.aep.cli", "simulate-inp",
            str(self.inp_path), "--format", "json"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            sim_data = json.loads(result.stdout)
            
            # Sauvegarder le résultat
            sim_file = self.results_dir / f"{self.inp_path.stem}_epanet_sim.json"
            with open(sim_file, 'w', encoding='utf-8') as f:
                json.dump(sim_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Simulation sauvegardée: {sim_file}")
            return sim_data
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Erreur simulation EPANET: {e}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur parsing JSON: {e}")
            logger.error(f"STDOUT: {result.stdout[:500]}...")
            raise
    
    def calculate_flow_sum(self, data: Dict[str, Any]) -> float:
        """Calcule la somme des débits depuis les données hydrauliques."""
        hyd = data.get('hydraulics') or data
        flows = hyd.get('flows_m3_s') or hyd.get('flows') or {}
        
        def extract_flow_value(x):
            """Extrait la valeur de débit depuis différents formats."""
            if isinstance(x, dict):
                return float(x.get('value', 0) or 0)
            elif isinstance(x, (int, float)):
                return float(x)
            elif isinstance(x, str):
                try:
                    return float(x)
                except ValueError:
                    return 0.0
            return 0.0
        
        if isinstance(flows, dict):
            total = sum(extract_flow_value(v) for v in flows.values())
        elif isinstance(flows, list):
            total = sum(extract_flow_value(x) for x in flows)
        else:
            total = 0.0
            
        return total
    
    def run_check_flows(self, simulator: str = "epanet", links: Optional[List[str]] = None, 
                       save_plot: bool = True, no_json_series: bool = True) -> Dict[str, Any]:
        """Exécute check_flows.py avec les paramètres donnés."""
        logger.info(f"🔍 Diagnostic conservation avec {simulator.upper()}...")
        
        cmd = [
            sys.executable, "tools/check_flows.py",
            str(self.inp_path),
            "--simulator", simulator,
            "--outdir", str(self.results_dir),
            "--save-plot" if save_plot else "",
            "--no-json-series" if no_json_series else "",
        ]
        
        if links:
            cmd.extend(["--links", ",".join(links)])
        
        # Filtrer les arguments vides
        cmd = [arg for arg in cmd if arg]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("✅ Diagnostic check_flows terminé")
            return {"success": True, "output": result.stdout}
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Erreur check_flows: {e}")
            logger.error(f"STDERR: {e.stderr}")
            return {"success": False, "error": e.stderr}
    
    def compare_simulations(self, epanet_data: Dict[str, Any], 
                          optimization_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Compare les résultats de simulation EPANET vs optimisation."""
        logger.info("📊 Comparaison des simulations...")
        
        # Calculer somme des débits pour simulation EPANET
        epanet_total = self.calculate_flow_sum(epanet_data)
        
        comparison = {
            "epanet_simulation": {
                "total_flow_m3s": epanet_total,
                "conservation_ok": abs(epanet_total) < 1e-3,
                "source": "simulate-inp CLI"
            }
        }
        
        if optimization_data:
            opt_total = self.calculate_flow_sum(optimization_data)
            comparison["optimization"] = {
                "total_flow_m3s": opt_total,
                "conservation_ok": abs(opt_total) < 1e-3,
                "source": "network-optimize-unified"
            }
            
            # Diagnostic
            if abs(epanet_total) < 1e-3 and abs(opt_total) > 1e-3:
                comparison["diagnosis"] = "❌ L'erreur vient de la modification des diamètres par l'optimiseur/réparation"
            elif abs(epanet_total) > 1e-3:
                comparison["diagnosis"] = "❌ Le parsing initial de l'INP (ordre/orientation) est suspect"
            else:
                comparison["diagnosis"] = "✅ Conservation respectée dans les deux cas"
        
        return comparison
    
    def isolate_problem_links(self, num_links: int = 10) -> List[str]:
        """Isole un sous-ensemble de conduites pour diagnostic ciblé."""
        logger.info(f"🎯 Isolation de {num_links} premières conduites...")
        
        # Exécuter check_flows pour obtenir la liste des conduites
        result = self.run_check_flows(simulator="wntr", no_json_series=True)
        
        if not result["success"]:
            logger.warning("⚠️ Impossible d'obtenir la liste des conduites")
            return []
        
        # Lire le JSON généré pour extraire les noms de conduites
        json_files = list(self.results_dir.glob(f"{self.inp_path.stem}_sumflows_wntr.json"))
        if not json_files:
            logger.warning("⚠️ Fichier JSON de diagnostic non trouvé")
            return []
        
        try:
            with open(json_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            link_stats = data.get("link_stats_sample", [])
            links = [stat["link"] for stat in link_stats[:num_links]]
            
            logger.info(f"✅ Conduites isolées: {links}")
            return links
            
        except Exception as e:
            logger.error(f"❌ Erreur lecture JSON: {e}")
            return []
    
    def generate_report(self, comparison: Dict[str, Any]) -> Path:
        """Génère un rapport de diagnostic complet."""
        logger.info("📝 Génération du rapport...")
        
        report_file = self.results_dir / f"{self.inp_path.stem}_flow_conservation_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Diagnostic Conservation des Débits - {self.inp_path.name}\n\n")
            f.write(f"**Date:** {Path(__file__).stat().st_mtime}\n\n")
            
            f.write("## Résumé\n\n")
            f.write("| Simulation | Total Flow (m³/s) | Conservation OK |\n")
            f.write("|------------|-------------------|-----------------|\n")
            
            for sim_name, data in comparison.items():
                if sim_name != "diagnosis":
                    total = data["total_flow_m3s"]
                    ok = "✅" if data["conservation_ok"] else "❌"
                    f.write(f"| {sim_name} | {total:.6f} | {ok} |\n")
            
            f.write("\n## Diagnostic\n\n")
            if "diagnosis" in comparison:
                f.write(f"{comparison['diagnosis']}\n\n")
            
            f.write("## Causes Possibles\n\n")
            f.write("- **Sens de conduite arbitraire**: Orientation définie dans l'INP\n")
            f.write("- **Exports WNTR mal agrégés**: Problème de parsing des résultats\n")
            f.write("- **Unités signées**: Interprétation des débits négatifs\n")
            f.write("- **Modifications d'orientations**: Réparation/optimisation\n")
            f.write("- **Demandes dynamiques**: Consommation variable non équilibrée\n")
            f.write("- **Valves/éléments spéciaux**: Comportement non standard\n\n")
            
            f.write("## Actions Recommandées\n\n")
            f.write("1. **Vérifier l'orientation des conduites** dans l'INP\n")
            f.write("2. **Analyser les débits négatifs** (sens inverse)\n")
            f.write("3. **Tester avec un sous-ensemble** de conduites\n")
            f.write("4. **Comparer avec EPANET GUI** si disponible\n")
            f.write("5. **Vérifier les demandes** aux nœuds\n\n")
            
            f.write("## Fichiers Générés\n\n")
            for file_path in self.results_dir.glob(f"{self.inp_path.stem}_*"):
                f.write(f"- `{file_path.name}`\n")
        
        logger.info(f"✅ Rapport généré: {report_file}")
        return report_file
    
    def run_full_diagnostic(self, optimization_file: Optional[Path] = None) -> Dict[str, Any]:
        """Exécute le diagnostic complet."""
        logger.info("🔬 Démarrage du diagnostic complet...")
        
        # 1. Simulation EPANET unique
        epanet_data = self.run_epanet_simulation()
        
        # 2. Charger les données d'optimisation si fournies
        optimization_data = None
        if optimization_file and optimization_file.exists():
            logger.info(f"📂 Chargement des données d'optimisation: {optimization_file}")
            with open(optimization_file, 'r', encoding='utf-8') as f:
                optimization_data = json.load(f)
        
        # 3. Comparaison des simulations
        comparison = self.compare_simulations(epanet_data, optimization_data)
        
        # 4. Diagnostic check_flows avec EPANET
        self.run_check_flows(simulator="epanet", save_plot=True, no_json_series=True)
        
        # 5. Isolation de problèmes (sous-ensemble de conduites)
        problem_links = self.isolate_problem_links(num_links=10)
        if problem_links:
            self.run_check_flows(simulator="wntr", links=problem_links, 
                               save_plot=True, no_json_series=True)
        
        # 6. Génération du rapport
        report_file = self.generate_report(comparison)
        
        return {
            "comparison": comparison,
            "problem_links": problem_links,
            "report_file": report_file,
            "epanet_total": comparison["epanet_simulation"]["total_flow_m3s"]
        }


def main():
    parser = argparse.ArgumentParser(
        description="Diagnostic automatique de conservation des débits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Diagnostic complet d'un fichier INP
  python tools/diagnose_flow_conservation.py network.inp
  
  # Comparaison avec résultats d'optimisation
  python tools/diagnose_flow_conservation.py network.inp --optimization results/opt.json
  
  # Diagnostic rapide (sans plots)
  python tools/diagnose_flow_conservation.py network.inp --quick
        """
    )
    
    parser.add_argument("input", help="Fichier INP ou JSON d'optimisation")
    parser.add_argument("--optimization", help="Fichier JSON d'optimisation pour comparaison")
    parser.add_argument("--results-dir", default="results", help="Dossier de sortie")
    parser.add_argument("--quick", action="store_true", help="Mode rapide (sans plots)")
    parser.add_argument("--num-links", type=int, default=10, help="Nombre de conduites à isoler")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"❌ Fichier introuvable: {input_path}")
        sys.exit(1)
    
    # Déterminer le type d'entrée
    if input_path.suffix.lower() == '.inp':
        # Mode diagnostic complet
        diagnostic = FlowConservationDiagnostic(
            inp_path=input_path,
            results_dir=Path(args.results_dir)
        )
        
        optimization_file = Path(args.optimization) if args.optimization else None
        result = diagnostic.run_full_diagnostic(optimization_file)
        
        # Affichage des résultats
        print("\n" + "="*60)
        print("📊 RÉSULTATS DU DIAGNOSTIC")
        print("="*60)
        
        epanet_total = result["epanet_total"]
        print(f"Simulation EPANET: {epanet_total:.6f} m³/s")
        print(f"Conservation OK: {'✅' if abs(epanet_total) < 1e-3 else '❌'}")
        
        if "optimization" in result["comparison"]:
            opt_total = result["comparison"]["optimization"]["total_flow_m3s"]
            print(f"Optimisation: {opt_total:.6f} m³/s")
            print(f"Conservation OK: {'✅' if abs(opt_total) < 1e-3 else '❌'}")
        
        print(f"\nDiagnostic: {result['comparison'].get('diagnosis', 'N/A')}")
        print(f"Rapport: {result['report_file']}")
        
    else:
        # Mode analyse de résultats existants
        logger.info(f"📂 Analyse du fichier de résultats: {input_path}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Calculer la somme des débits
        hyd = data.get('hydraulics') or data
        flows = hyd.get('flows_m3_s') or hyd.get('flows') or {}
        
        def sum_flows(flows_data):
            if isinstance(flows_data, dict):
                return sum(float(v or 0.0) for v in flows_data.values())
            elif isinstance(flows_data, list):
                return sum(float(x.get('value', 0) or 0) if isinstance(x, dict) else float(x or 0) for x in flows_data)
            return 0.0
        
        total = sum_flows(flows)
        print(f"\nTotal flow: {total:.6f} m³/s")
        print(f"Conservation OK: {'✅' if abs(total) < 1e-3 else '❌'}")


if __name__ == "__main__":
    main()
