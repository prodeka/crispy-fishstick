#!/usr/bin/env python3
"""
Script Python pour Exécuter et Comparer Plusieurs Runs d'Optimisation LCPI AEP

Ce script automatise l'exécution de la commande lcpi.aep.cli network-optimize-unified
avec différentes combinaisons de paramètres, stocke les résultats et fournit une analyse comparative.

Auteur: Assistant IA
Date: 25 août 2025
"""

import subprocess
import json
import os
import datetime
import time
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Forcer l'encodage UTF-8 pour le terminal Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    # Définir la variable d'environnement pour les sous-processus
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'

# Configuration des couleurs pour l'affichage
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class TestRun:
    """Représente un test d'optimisation avec ses paramètres et résultats"""
    run_name: str
    parameters: Dict[str, Any]
    output_file: str
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    status: str = "pending"
    error_message: Optional[str] = None
    results: Optional[Dict[str, Any]] = None

class ProgressTracker:
    """Gestionnaire de progression pour les tests"""
    
    def __init__(self, total_runs: int):
        self.total_runs = total_runs
        self.completed_runs = 0
        self.failed_runs = 0
        self.current_run = None
        self.lock = threading.Lock()
        
    def start_run(self, run_name: str):
        """Démarre un nouveau run"""
        with self.lock:
            self.current_run = run_name
            print(f"\n{Colors.OKCYAN}🚀 Démarrage du run: {run_name}{Colors.ENDC}")
            
    def complete_run(self, success: bool = True):
        """Marque un run comme terminé"""
        with self.lock:
            self.completed_runs += 1
            if success:
                print(f"{Colors.OKGREEN}✅ Run terminé avec succès ({self.completed_runs}/{self.total_runs}){Colors.ENDC}")
            else:
                self.failed_runs += 1
                print(f"{Colors.FAIL}❌ Run échoué ({self.completed_runs}/{self.total_runs}){Colors.ENDC}")
            
            self.current_run = None
            
    def get_progress(self) -> float:
        """Retourne le pourcentage de progression"""
        return (self.completed_runs / self.total_runs) * 100 if self.total_runs > 0 else 0

class OptimizationTestRunner:
    """Classe principale pour exécuter les tests d'optimisation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get("output_dir", "test_runs"))
        self.cli_script = config.get("cli_script", ["python", "-m", "lcpi.aep.cli"])
        self.input_network_file = config.get("input_network_file", "bismark_inp.inp")
        self.param_combinations = config.get("param_combinations", [])
        self.max_workers = config.get("max_workers", 1)  # Par défaut séquentiel pour éviter les conflits
        self.results: List[TestRun] = []
        
        # Créer le répertoire de sortie
        self.output_dir.mkdir(exist_ok=True)
        
    def build_command(self, params: Dict[str, Any], output_file: str) -> List[str]:
        """Construit la commande CLI pour un run donné"""
        base_command = [
            *self.cli_script,
            "network-optimize-unified",
            self.input_network_file,
            "--method", "genetic",
            "--solver", "epanet",
            "--verbose",
            "--show-stats",
            "--output", output_file,
            "--generations", str(params["generations"]),
            "--population", str(params["population"]),
            "--hmax", str(params["hmax"]),
            "--no-log",  # Désactiver la journalisation automatiquement
        ]
        
        # Ajouter des paramètres optionnels
        if "demand" in params:
            base_command.extend(["--demand", str(params["demand"])])
        if "mutation_rate" in params:
            base_command.extend(["--mutation-rate", str(params["mutation_rate"])])
        if "crossover_rate" in params:
            base_command.extend(["--crossover-rate", str(params["crossover_rate"])])
        if "elite_size" in params:
            base_command.extend(["--elite-size", str(params["elite_size"])])
            
        return base_command
    
    def execute_single_run(self, test_run: TestRun, progress_tracker: ProgressTracker) -> TestRun:
        """Exécute un seul run d'optimisation"""
        try:
            progress_tracker.start_run(test_run.run_name)
            test_run.start_time = datetime.datetime.now()
            test_run.status = "running"
            
            # Construire la commande
            command = self.build_command(test_run.parameters, test_run.output_file)
            
            print(f"{Colors.OKBLUE}Commande: {' '.join(command)}{Colors.ENDC}")
            
            # Exécuter la commande avec encodage UTF-8 forcé
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env,
                check=True,
                timeout=1800  # Timeout de 30 minutes
            )
            
            # Marquer comme terminé avec succès
            test_run.end_time = datetime.datetime.now()
            test_run.status = "completed"
            
            # Charger et analyser les résultats
            if os.path.exists(test_run.output_file):
                with open(test_run.output_file, 'r', encoding='utf-8') as f:
                    test_run.results = json.load(f)
            
            progress_tracker.complete_run(success=True)
            return test_run
            
        except subprocess.TimeoutExpired:
            test_run.status = "timeout"
            test_run.error_message = "Timeout après 30 minutes"
            progress_tracker.complete_run(success=False)
            return test_run
            
        except subprocess.CalledProcessError as e:
            test_run.status = "failed"
            test_run.error_message = f"Erreur d'exécution: {e.stderr}"
            progress_tracker.complete_run(success=False)
            return test_run
            
        except Exception as e:
            test_run.status = "error"
            test_run.error_message = f"Erreur inattendue: {str(e)}"
            progress_tracker.complete_run(success=False)
            return test_run
    
    def run_all_tests(self) -> List[TestRun]:
        """Exécute tous les tests d'optimisation"""
        print(f"{Colors.HEADER}{Colors.BOLD}🚀 Démarrage des tests d'optimisation LCPI AEP{Colors.ENDC}")
        print(f"📁 Répertoire de sortie: {self.output_dir}")
        print(f"🔧 Nombre total de tests: {len(self.param_combinations)}")
        print(f"⚙️  Workers maximum: {self.max_workers}")
        print(f"⏰ Début: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Créer les objets TestRun
        for i, params in enumerate(self.param_combinations):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.output_dir / f"{params['run_name']}_{timestamp}.json"
            
            test_run = TestRun(
                run_name=params['run_name'],
                parameters=params,
                output_file=str(output_file)
            )
            self.results.append(test_run)
        
        # Initialiser le tracker de progression
        progress_tracker = ProgressTracker(len(self.results))
        
        # Exécuter les tests
        if self.max_workers == 1:
            # Exécution séquentielle
            for test_run in self.results:
                self.execute_single_run(test_run, progress_tracker)
        else:
            # Exécution parallèle
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_run = {
                    executor.submit(self.execute_single_run, test_run, progress_tracker): test_run
                    for test_run in self.results
                }
                
                for future in as_completed(future_to_run):
                    test_run = future_to_run[future]
                    try:
                        future.result()
                    except Exception as e:
                        test_run.status = "error"
                        test_run.error_message = f"Erreur d'exécution: {str(e)}"
                        progress_tracker.complete_run(success=False)
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}🎯 Tous les tests sont terminés !{Colors.ENDC}")
        print(f"✅ Succès: {progress_tracker.completed_runs - progress_tracker.failed_runs}")
        print(f"❌ Échecs: {progress_tracker.failed_runs}")
        print(f"📊 Progression: {progress_tracker.get_progress():.1f}%")
        
        return self.results
    
    def generate_summary_report(self) -> str:
        """Génère un rapport sommaire des résultats"""
        if not self.results:
            return "Aucun résultat à analyser."
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}📊 Génération du rapport de synthèse...{Colors.ENDC}")
        
        summary_data = []
        
        for test_run in self.results:
            if test_run.status == "completed" and test_run.results:
                try:
                    data = test_run.results
                    meta = data.get("meta", {})
                    best_proposal = data.get("proposals", [{}])[0] if data.get("proposals") else {}
                    stats = data.get("metrics", {}).get("stats", {})
                    
                    summary_data.append({
                        "Run": test_run.run_name,
                        "Status": test_run.status,
                        "Constraints OK": best_proposal.get("constraints_ok", False),
                        "CAPEX": best_proposal.get("CAPEX", "N/A"),
                        "Max Speed (m/s)": stats.get("vitesse_max", "N/A"),
                        "Min Pressure (m)": stats.get("pression_min", "N/A"),
                        "Generations": meta.get("generations", "N/A"),
                        "Population": meta.get("population", "N/A"),
                        "Hmax": meta.get("hmax", "N/A"),
                        "Duration": str(test_run.end_time - test_run.start_time) if test_run.end_time and test_run.start_time else "N/A"
                    })
                except Exception as e:
                    print(f"⚠️  Erreur lors de l'analyse de {test_run.run_name}: {e}")
            else:
                summary_data.append({
                    "Run": test_run.run_name,
                    "Status": test_run.status,
                    "Constraints OK": "N/A",
                    "CAPEX": "N/A",
                    "Max Speed (m/s)": "N/A",
                    "Min Pressure (m)": "N/A",
                    "Generations": "N/A",
                    "Population": "N/A",
                    "Hmax": "N/A",
                    "Duration": "N/A"
                })
        
        # Générer le rapport
        report_file = self.output_dir / f"test_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Rapport de Synthèse des Tests d'Optimisation LCPI AEP\n\n")
            f.write(f"**Date de génération:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Nombre total de tests:** {len(self.results)}\n")
            f.write(f"**Tests réussis:** {len([r for r in self.results if r.status == 'completed'])}\n")
            f.write(f"**Tests échoués:** {len([r for r in self.results if r.status != 'completed'])}\n\n")
            
            # Tableau des résultats
            f.write("## Résultats des Tests\n\n")
            f.write("| Run | Status | Constraints OK | CAPEX | Max Speed | Min Pressure | Generations | Population | Hmax | Duration |\n")
            f.write("|-----|--------|----------------|-------|-----------|--------------|-------------|------------|------|----------|\n")
            
            for row in summary_data:
                f.write(f"| {row['Run']} | {row['Status']} | {row['Constraints OK']} | {row['CAPEX']} | {row['Max Speed (m/s)']} | {row['Min Pressure (m)']} | {row['Generations']} | {row['Population']} | {row['Hmax']} | {row['Duration']} |\n")
            
            f.write("\n## Détails des Tests\n\n")
            
            for test_run in self.results:
                f.write(f"### {test_run.run_name}\n")
                f.write(f"- **Status:** {test_run.status}\n")
                f.write(f"- **Paramètres:** {test_run.parameters}\n")
                f.write(f"- **Fichier de sortie:** {test_run.output_file}\n")
                
                if test_run.start_time:
                    f.write(f"- **Début:** {test_run.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                if test_run.end_time:
                    f.write(f"- **Fin:** {test_run.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                if test_run.error_message:
                    f.write(f"- **Erreur:** {test_run.error_message}\n")
                f.write("\n")
        
        print(f"{Colors.OKGREEN}📄 Rapport généré: {report_file}{Colors.ENDC}")
        return str(report_file)
    
    def print_summary_table(self):
        """Affiche un tableau résumé dans la console"""
        if not self.results:
            print("Aucun résultat à afficher.")
            return
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}📊 Résumé des Tests{Colors.ENDC}")
        print("=" * 120)
        
        # En-têtes
        headers = ["Run", "Status", "Constraints", "CAPEX", "Max Speed", "Min Pressure", "Generations", "Population", "Hmax", "Duration"]
        header_line = " | ".join(f"{h:15}" for h in headers)
        print(header_line)
        print("-" * len(header_line))
        
        # Données
        for test_run in self.results:
            if test_run.status == "completed" and test_run.results:
                try:
                    data = test_run.results
                    best_proposal = data.get("proposals", [{}])[0] if data.get("proposals") else {}
                    stats = data.get("metrics", {}).get("stats", {})
                    meta = data.get("meta", {})
                    
                    row_data = [
                        test_run.run_name[:15],
                        test_run.status[:15],
                        str(best_proposal.get("constraints_ok", False))[:15],
                        str(best_proposal.get("CAPEX", "N/A"))[:15],
                        str(stats.get("vitesse_max", "N/A"))[:15],
                        str(stats.get("pression_min", "N/A"))[:15],
                        str(meta.get("generations", "N/A"))[:15],
                        str(meta.get("population", "N/A"))[:15],
                        str(meta.get("hmax", "N/A"))[:15],
                        str(test_run.end_time - test_run.start_time)[:15] if test_run.end_time and test_run.start_time else "N/A"
                    ]
                except Exception as e:
                    row_data = [test_run.run_name[:15], test_run.status[:15]] + ["N/A"] * 8
            else:
                row_data = [test_run.run_name[:15], test_run.status[:15]] + ["N/A"] * 8
            
            print(" | ".join(f"{d:15}" for d in row_data))

def load_config(config_file: str = "optimization_test_config.json") -> Dict[str, Any]:
    """Charge la configuration depuis un fichier JSON"""
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Configuration par défaut
        return {
            "output_dir": "test_runs",
            "cli_script": ["python", "-m", "lcpi.aep.cli"],
            "input_network_file": "bismark_inp.inp",
            "max_workers": 1,
            "param_combinations": [
                # Tests pour hmax à 50m
                {"generations": 30, "population": 40, "hmax": 50, "demand": 500, "run_name": "gen30_pop40_hmax50"},
                {"generations": 50, "population": 50, "hmax": 50, "demand": 500, "run_name": "gen50_pop50_hmax50"},
                
                # Tests pour hmax à 100m
                {"generations": 30, "population": 40, "hmax": 100, "demand": 500, "run_name": "gen30_pop40_hmax100"},
                {"generations": 50, "population": 50, "hmax": 100, "demand": 500, "run_name": "gen50_pop50_hmax100"},
                {"generations": 80, "population": 80, "hmax": 100, "demand": 500, "run_name": "gen80_pop80_hmax100"},
                
                # Tests pour hmax à 150m
                {"generations": 50, "population": 50, "hmax": 150, "demand": 500, "run_name": "gen50_pop50_hmax150"},
                {"generations": 100, "population": 100, "hmax": 150, "demand": 500, "run_name": "gen100_pop100_hmax150"},
                
                # Tests pour hmax à 200m
                {"generations": 50, "population": 50, "hmax": 200, "demand": 500, "run_name": "gen50_pop50_hmax200"},
            ]
        }

def save_config(config: Dict[str, Any], config_file: str = "optimization_test_config.json"):
    """Sauvegarde la configuration dans un fichier JSON"""
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Script de test d'optimisation LCPI AEP")
    parser.add_argument("--config", "-c", default="optimization_test_config.json", 
                       help="Fichier de configuration JSON")
    parser.add_argument("--input", "-i", help="Fichier réseau d'entrée")
    parser.add_argument("--output", "-o", help="Répertoire de sortie")
    parser.add_argument("--workers", "-w", type=int, help="Nombre de workers parallèles")
    parser.add_argument("--generate-config", action="store_true", 
                       help="Générer un fichier de configuration par défaut")
    
    args = parser.parse_args()
    
    if args.generate_config:
        config = load_config()
        save_config(config, "optimization_test_config.json")
        print(f"{Colors.OKGREEN}✅ Fichier de configuration généré: optimization_test_config.json{Colors.ENDC}")
        return
    
    # Charger la configuration
    config = load_config(args.config)
    
    # Remplacer les paramètres de ligne de commande si fournis
    if args.input:
        config["input_network_file"] = args.input
    if args.output:
        config["output_dir"] = args.output
    if args.workers:
        config["max_workers"] = args.workers
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(config["input_network_file"]):
        print(f"{Colors.FAIL}❌ Erreur: Le fichier réseau {config['input_network_file']} n'existe pas.{Colors.ENDC}")
        sys.exit(1)
    
    try:
        # Créer et exécuter le runner
        runner = OptimizationTestRunner(config)
        results = runner.run_all_tests()
        
        # Générer le rapport
        report_file = runner.generate_summary_report()
        
        # Afficher le résumé dans la console
        runner.print_summary_table()
        
        print(f"\n{Colors.OKGREEN}🎉 Tests terminés avec succès !{Colors.ENDC}")
        print(f"📄 Rapport détaillé: {report_file}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Tests interrompus par l'utilisateur.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Erreur fatale: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()