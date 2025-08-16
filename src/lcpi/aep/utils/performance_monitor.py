"""
Module de monitoring et profiling des performances pour les algorithmes AEP.

Ce module implémente :
- Profiling des algorithmes avec métriques détaillées
- Monitoring en temps réel des performances
- Benchmark des solveurs et optimisations
- Rapports de performance détaillés
"""

import time
import psutil
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Représente une métrique de performance."""
    name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""


@dataclass
class AlgorithmProfile:
    """Profil de performance d'un algorithme."""
    algorithm_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None
    memory_usage_mb: List[float] = field(default_factory=list)
    cpu_usage_percent: List[float] = field(default_factory=list)
    metrics: List[PerformanceMetric] = field(default_factory=list)
    iterations: int = 0
    convergence: bool = False
    error: Optional[str] = None
    
    def add_metric(self, name: str, value: float, unit: str, description: str = ""):
        """Ajoute une métrique au profil."""
        metric = PerformanceMetric(name, value, unit, description)
        self.metrics.append(metric)
    
    def finalize(self):
        """Finalise le profil en calculant les métriques finales."""
        if self.end_time is None:
            self.end_time = datetime.now()
        
        if self.start_time and self.end_time:
            self.execution_time = (self.end_time - self.start_time).total_seconds()
        
        # Calculer les métriques moyennes
        if self.memory_usage_mb:
            self.add_metric("memory_avg", sum(self.memory_usage_mb) / len(self.memory_usage_mb), "MB", "Mémoire moyenne utilisée")
            self.add_metric("memory_max", max(self.memory_usage_mb), "MB", "Pic de mémoire")
        
        if self.cpu_usage_percent:
            self.add_metric("cpu_avg", sum(self.cpu_usage_percent) / len(self.cpu_usage_percent), "%", "CPU moyen utilisé")
            self.add_metric("cpu_max", max(self.cpu_usage_percent), "%", "Pic CPU")


class PerformanceMonitor:
    """Moniteur de performance pour les algorithmes AEP."""
    
    def __init__(self, 
                 monitor_interval: float = 1.0,
                 enable_memory_monitoring: bool = True,
                 enable_cpu_monitoring: bool = True):
        """
        Initialise le moniteur de performance.
        
        Args:
            monitor_interval: Intervalle de monitoring en secondes
            enable_memory_monitoring: Activer le monitoring mémoire
            enable_cpu_monitoring: Activer le monitoring CPU
        """
        self.monitor_interval = monitor_interval
        self.enable_memory_monitoring = enable_memory_monitoring
        self.enable_cpu_monitoring = enable_cpu_monitoring
        
        self.active_profiles: Dict[str, AlgorithmProfile] = {}
        self.completed_profiles: List[AlgorithmProfile] = []
        self.monitoring_thread: Optional[threading.Thread] = None
        self.stop_monitoring = False
        
        # Statistiques globales
        self.global_stats = {
            "total_algorithms": 0,
            "total_execution_time": 0.0,
            "total_memory_peak": 0.0,
            "total_cpu_peak": 0.0,
            "successful_runs": 0,
            "failed_runs": 0
        }
    
    def start_profile(self, algorithm_name: str) -> str:
        """
        Démarre le profiling d'un algorithme.
        
        Args:
            algorithm_name: Nom de l'algorithme
            
        Returns:
            ID du profil
        """
        profile_id = f"{algorithm_name}_{int(time.time())}"
        
        profile = AlgorithmProfile(
            algorithm_name=algorithm_name,
            start_time=datetime.now()
        )
        
        self.active_profiles[profile_id] = profile
        self.global_stats["total_algorithms"] += 1
        
        logger.info(f"Profil démarré: {profile_id}")
        return profile_id
    
    def stop_profile(self, profile_id: str, convergence: bool = True, error: Optional[str] = None):
        """
        Arrête le profiling d'un algorithme.
        
        Args:
            profile_id: ID du profil
            convergence: L'algorithme a-t-il convergé ?
            error: Erreur éventuelle
        """
        if profile_id not in self.active_profiles:
            logger.warning(f"Profil non trouvé: {profile_id}")
            return
        
        profile = self.active_profiles[profile_id]
        profile.convergence = convergence
        profile.error = error
        profile.finalize()
        
        # Mettre à jour les statistiques globales
        if profile.execution_time:
            self.global_stats["total_execution_time"] += profile.execution_time
        
        if profile.memory_usage_mb:
            memory_peak = max(profile.memory_usage_mb)
            self.global_stats["total_memory_peak"] = max(self.global_stats["total_memory_peak"], memory_peak)
        
        if profile.cpu_usage_percent:
            cpu_peak = max(profile.cpu_usage_percent)
            self.global_stats["total_cpu_peak"] = max(self.global_stats["total_cpu_peak"], cpu_peak)
        
        if error:
            self.global_stats["failed_runs"] += 1
        else:
            self.global_stats["successful_runs"] += 1
        
        # Déplacer vers les profils complétés
        self.completed_profiles.append(profile)
        del self.active_profiles[profile_id]
        
        logger.info(f"Profil arrêté: {profile_id}")
    
    def add_iteration(self, profile_id: str):
        """Ajoute une itération au profil."""
        if profile_id in self.active_profiles:
            self.active_profiles[profile_id].iterations += 1
    
    def add_metric(self, profile_id: str, name: str, value: float, unit: str, description: str = ""):
        """Ajoute une métrique au profil."""
        if profile_id in self.active_profiles:
            self.active_profiles[profile_id].add_metric(name, value, unit, description)
    
    def start_monitoring(self):
        """Démarre le monitoring en arrière-plan."""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            logger.warning("Monitoring déjà en cours")
            return
        
        self.stop_monitoring = False
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Monitoring démarré")
    
    def stop_monitoring(self):
        """Arrête le monitoring."""
        self.stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("Monitoring arrêté")
    
    def _monitoring_loop(self):
        """Boucle principale de monitoring."""
        while not self.stop_monitoring:
            try:
                # Mettre à jour les profils actifs
                for profile_id, profile in self.active_profiles.items():
                    if self.enable_memory_monitoring:
                        memory_mb = psutil.Process().memory_info().rss / (1024 * 1024)
                        profile.memory_usage_mb.append(memory_mb)
                    
                    if self.enable_cpu_monitoring:
                        cpu_percent = psutil.cpu_percent(interval=0.1)
                        profile.cpu_usage_percent.append(cpu_percent)
                
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                logger.error(f"Erreur dans la boucle de monitoring: {e}")
                time.sleep(self.monitor_interval)
    
    def get_profile(self, profile_id: str) -> Optional[AlgorithmProfile]:
        """Récupère un profil par son ID."""
        # Chercher dans les profils actifs
        if profile_id in self.active_profiles:
            return self.active_profiles[profile_id]
        
        # Chercher dans les profils complétés
        for profile in self.completed_profiles:
            if profile.algorithm_name in profile_id:
                return profile
        
        return None
    
    def get_algorithm_stats(self, algorithm_name: str) -> Dict[str, Any]:
        """Récupère les statistiques pour un algorithme spécifique."""
        algorithm_profiles = [p for p in self.completed_profiles if p.algorithm_name == algorithm_name]
        
        if not algorithm_profiles:
            return {"error": f"Aucun profil trouvé pour {algorithm_name}"}
        
        execution_times = [p.execution_time for p in algorithm_profiles if p.execution_time]
        memory_peaks = [max(p.memory_usage_mb) for p in algorithm_profiles if p.memory_usage_mb]
        cpu_peaks = [max(p.cpu_usage_percent) for p in algorithm_profiles if p.cpu_usage_percent]
        
        stats = {
            "algorithm_name": algorithm_name,
            "total_runs": len(algorithm_profiles),
            "successful_runs": len([p for p in algorithm_profiles if not p.error]),
            "failed_runs": len([p for p in algorithm_profiles if p.error]),
            "success_rate": len([p for p in algorithm_profiles if not p.error]) / len(algorithm_profiles)
        }
        
        if execution_times:
            stats.update({
                "avg_execution_time": sum(execution_times) / len(execution_times),
                "min_execution_time": min(execution_times),
                "max_execution_time": max(execution_times),
                "total_execution_time": sum(execution_times)
            })
        
        if memory_peaks:
            stats.update({
                "avg_memory_peak": sum(memory_peaks) / len(memory_peaks),
                "min_memory_peak": min(memory_peaks),
                "max_memory_peak": max(memory_peaks)
            })
        
        if cpu_peaks:
            stats.update({
                "avg_cpu_peak": sum(cpu_peaks) / len(cpu_peaks),
                "min_cpu_peak": min(cpu_peaks),
                "max_cpu_peak": max(cpu_peaks)
            })
        
        return stats
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques globales."""
        return self.global_stats.copy()
    
    def export_profile(self, profile_id: str, output_file: Path) -> bool:
        """Exporte un profil vers un fichier JSON."""
        profile = self.get_profile(profile_id)
        if not profile:
            return False
        
        try:
            # Convertir le profil en dictionnaire
            profile_dict = {
                "algorithm_name": profile.algorithm_name,
                "start_time": profile.start_time.isoformat(),
                "end_time": profile.end_time.isoformat() if profile.end_time else None,
                "execution_time": profile.execution_time,
                "iterations": profile.iterations,
                "convergence": profile.convergence,
                "error": profile.error,
                "metrics": [
                    {
                        "name": m.name,
                        "value": m.value,
                        "unit": m.unit,
                        "timestamp": m.timestamp.isoformat(),
                        "description": m.description
                    }
                    for m in profile.metrics
                ],
                "memory_usage_mb": profile.memory_usage_mb,
                "cpu_usage_percent": profile.cpu_usage_percent
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profile_dict, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export: {e}")
            return False
    
    def clear_profiles(self):
        """Efface tous les profils."""
        self.active_profiles.clear()
        self.completed_profiles.clear()
        self.global_stats = {
            "total_algorithms": 0,
            "total_execution_time": 0.0,
            "total_memory_peak": 0.0,
            "total_cpu_peak": 0.0,
            "successful_runs": 0,
            "failed_runs": 0
        }
        logger.info("Tous les profils ont été effacés")


class PerformanceProfiler:
    """Profiler de performance avec contexte manager."""
    
    def __init__(self, monitor: PerformanceMonitor, algorithm_name: str):
        """
        Initialise le profiler.
        
        Args:
            monitor: Instance du moniteur de performance
            algorithm_name: Nom de l'algorithme à profiler
        """
        self.monitor = monitor
        self.algorithm_name = algorithm_name
        self.profile_id = None
    
    def __enter__(self):
        """Démarre le profiling."""
        self.profile_id = self.monitor.start_profile(self.algorithm_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Arrête le profiling."""
        if self.profile_id:
            error = str(exc_val) if exc_val else None
            self.monitor.stop_profile(self.profile_id, error=error)
    
    def add_metric(self, name: str, value: float, unit: str, description: str = ""):
        """Ajoute une métrique au profil actuel."""
        if self.profile_id:
            self.monitor.add_metric(self.profile_id, name, value, unit, description)
    
    def add_iteration(self):
        """Ajoute une itération au profil actuel."""
        if self.profile_id:
            self.monitor.add_iteration(self.profile_id)


class PerformanceReporter:
    """Générateur de rapports de performance."""
    
    def __init__(self, monitor: PerformanceMonitor):
        """
        Initialise le générateur de rapports.
        
        Args:
            monitor: Instance du moniteur de performance
        """
        self.monitor = monitor
        self.console = Console()
    
    def generate_summary_report(self) -> str:
        """Génère un rapport de résumé des performances."""
        global_stats = self.monitor.get_global_stats()
        
        report = f"""
# 📊 RAPPORT DE PERFORMANCE - RÉSUMÉ

## 🎯 Statistiques Globales
- **Total d'algorithmes exécutés** : {global_stats['total_algorithms']}
- **Temps d'exécution total** : {global_stats['total_execution_time']:.2f} secondes
- **Pic de mémoire global** : {global_stats['total_memory_peak']:.2f} MB
- **Pic CPU global** : {global_stats['total_cpu_peak']:.2f} %
- **Exécutions réussies** : {global_stats['successful_runs']}
- **Exécutions échouées** : {global_stats['failed_runs']}

## 📈 Taux de Succès
- **Taux global** : {global_stats['successful_runs'] / max(global_stats['total_algorithms'], 1) * 100:.1f}%

## 🔍 Détails par Algorithme
"""
        
        # Ajouter les détails par algorithme
        algorithm_names = set(p.algorithm_name for p in self.monitor.completed_profiles)
        
        for alg_name in sorted(algorithm_names):
            stats = self.monitor.get_algorithm_stats(alg_name)
            if "error" not in stats:
                report += f"""
### {alg_name}
- **Exécutions** : {stats['total_runs']}
- **Taux de succès** : {stats['success_rate'] * 100:.1f}%
- **Temps moyen** : {stats.get('avg_execution_time', 0):.2f} secondes
- **Mémoire moyenne** : {stats.get('avg_memory_peak', 0):.2f} MB
"""
        
        return report
    
    def display_live_monitoring(self, refresh_interval: float = 1.0):
        """Affiche le monitoring en temps réel."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="active_profiles", size=10),
            Layout(name="global_stats", size=8)
        )
        
        try:
            with Live(layout, refresh_per_second=1/refresh_interval, screen=True):
                while True:
                    # Header
                    layout["header"].update(Panel(
                        f"🔍 Monitoring Performance AEP - {datetime.now().strftime('%H:%M:%S')}",
                        style="bold blue"
                    ))
                    
                    # Profils actifs
                    active_table = Table(title="📊 Algorithmes Actifs")
                    active_table.add_column("Algorithme", style="cyan")
                    active_table.add_column("Temps", style="green")
                    active_table.add_column("Mémoire", style="yellow")
                    active_table.add_column("CPU", style="magenta")
                    active_table.add_column("Itérations", style="blue")
                    
                    for profile_id, profile in self.monitor.active_profiles.items():
                        elapsed = (datetime.now() - profile.start_time).total_seconds()
                        memory = profile.memory_usage_mb[-1] if profile.memory_usage_mb else 0
                        cpu = profile.cpu_usage_percent[-1] if profile.cpu_usage_percent else 0
                        
                        active_table.add_row(
                            profile.algorithm_name,
                            f"{elapsed:.1f}s",
                            f"{memory:.1f} MB",
                            f"{cpu:.1f}%",
                            str(profile.iterations)
                        )
                    
                    layout["active_profiles"].update(active_table)
                    
                    # Statistiques globales
                    global_stats = self.monitor.get_global_stats()
                    stats_table = Table(title="📈 Statistiques Globales")
                    stats_table.add_column("Métrique", style="cyan")
                    stats_table.add_column("Valeur", style="white")
                    
                    stats_table.add_row("Total algorithmes", str(global_stats["total_algorithms"]))
                    stats_table.add_row("Temps total", f"{global_stats['total_execution_time']:.1f}s")
                    stats_table.add_row("Pic mémoire", f"{global_stats['total_memory_peak']:.1f} MB")
                    stats_table.add_row("Pic CPU", f"{global_stats['total_cpu_peak']:.1f}%")
                    stats_table.add_row("Succès", str(global_stats["successful_runs"]))
                    stats_table.add_row("Échecs", str(global_stats["failed_runs"]))
                    
                    layout["global_stats"].update(stats_table)
                    
                    time.sleep(refresh_interval)
                    
        except KeyboardInterrupt:
            self.console.print("\n🛑 Monitoring arrêté par l'utilisateur")


# Instance globale du moniteur de performance
_default_monitor = None

def get_performance_monitor(**kwargs) -> PerformanceMonitor:
    """Retourne l'instance globale du moniteur de performance."""
    global _default_monitor
    
    if _default_monitor is None:
        _default_monitor = PerformanceMonitor(**kwargs)
    
    return _default_monitor


@contextmanager
def profile_algorithm(algorithm_name: str, **monitor_kwargs):
    """
    Contexte manager pour profiler un algorithme.
    
    Usage:
        with profile_algorithm("hardy_cross") as profiler:
            # Votre algorithme ici
            result = run_hardy_cross(network_data)
            profiler.add_metric("convergence_iterations", 15, "iterations")
    """
    monitor = get_performance_monitor(**monitor_kwargs)
    
    with PerformanceProfiler(monitor, algorithm_name) as profiler:
        yield profiler


def benchmark_solvers(network_data: Dict[str, Any], 
                     solvers: List[str] = None,
                     iterations: int = 5) -> Dict[str, Any]:
    """
    Benchmark des solveurs disponibles.
    
    Args:
        network_data: Données du réseau à tester
        solvers: Liste des solveurs à tester (None = tous)
        iterations: Nombre d'itérations par solveur
        
    Returns:
        Résultats du benchmark
    """
    if solvers is None:
        solvers = ["lcpi", "epanet"]
    
    monitor = get_performance_monitor()
    results = {}
    
    for solver_name in solvers:
        try:
            solver_results = []
            
            for i in range(iterations):
                with profile_algorithm(f"benchmark_{solver_name}_{i}") as profiler:
                    # Obtenir le solveur
                    solver = SolverFactory.get_solver(solver_name)
                    
                    # Exécuter la simulation
                    start_time = time.time()
                    result = solver.run_simulation(network_data)
                    execution_time = time.time() - start_time
                    
                    profiler.add_metric("execution_time", execution_time, "seconds")
                    profiler.add_metric("success", 1 if result else 0, "boolean")
                    
                    solver_results.append({
                        "iteration": i,
                        "execution_time": execution_time,
                        "success": bool(result)
                    })
            
            # Calculer les statistiques
            execution_times = [r["execution_time"] for r in solver_results if r["success"]]
            
            results[solver_name] = {
                "iterations": len(solver_results),
                "successful_runs": len(execution_times),
                "success_rate": len(execution_times) / len(solver_results),
                "avg_execution_time": sum(execution_times) / len(execution_times) if execution_times else 0,
                "min_execution_time": min(execution_times) if execution_times else 0,
                "max_execution_time": max(execution_times) if execution_times else 0,
                "total_execution_time": sum(execution_times)
            }
            
        except Exception as e:
            results[solver_name] = {"error": str(e)}
    
    return results


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de profiling
    with profile_algorithm("test_algorithm") as profiler:
        # Simuler un algorithme
        time.sleep(2)
        profiler.add_metric("test_value", 42.0, "units", "Valeur de test")
        profiler.add_iteration()
    
    # Afficher les statistiques
    monitor = get_performance_monitor()
    stats = monitor.get_global_stats()
    print(f"Algorithmes exécutés: {stats['total_algorithms']}")
    print(f"Temps total: {stats['total_execution_time']:.2f}s")
