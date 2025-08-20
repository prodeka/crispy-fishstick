from typing import Callable, Optional, Dict, Any
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console
from typing import Dict as _Dict
from typing import Any as _Any
from typing import Optional as _Optional
import threading
import math
import queue

console = Console()


class RichProgressManager:
    """
    Manager d'affichage progressif basé sur rich.
    - gère TTY vs non-TTY
    - thread-safe updates via méthode update(event, data)
    - supporte une queue d'événements (utile pour ProcessPool)
    """

    def __init__(self, use_rich: Optional[bool] = None) -> None:
        self.use_rich = (console.is_terminal and (use_rich is not False)) if use_rich is None else bool(use_rich)
        self._progress: Optional[Progress] = None
        self._tasks: _Dict[str, int] = {}
        self._lock = threading.Lock()
        self._best_cost = math.inf
        self._topk = []  # top-k best costs
        # queue pour événements (optionnel)
        self.event_q: _Optional[queue.Queue] = None
        self._listener_thread: _Optional[threading.Thread] = None
        self._stop_listener = threading.Event()

    def __enter__(self):
        if self.use_rich:
            self._progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=None),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                transient=False,
                console=console,
            )
            self._progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.use_rich and self._progress:
            self._progress.stop()
        self.stop_listening()

    def start_listening(self, q: queue.Queue):
        """Start a background thread that consumes events from q and calls update"""
        self.event_q = q
        self._stop_listener.clear()
        t = threading.Thread(target=self._consume_queue, daemon=True)
        self._listener_thread = t
        t.start()

    def stop_listening(self):
        self._stop_listener.set()
        if self._listener_thread:
            self._listener_thread.join(timeout=1.0)

    def _consume_queue(self):
        while not self._stop_listener.is_set():
            try:
                ev = self.event_q.get(timeout=0.2)
            except queue.Empty:
                continue
            try:
                evt, data = ev
                self.update(evt, data)
            except Exception:
                pass

    def setup_tasks(self, total_generations: int = 1, population_size: int = 1):
        with self._lock:
            if not self.use_rich:
                return
            # create or reset
            if 'generations' in self._tasks and self._progress:
                try:
                    self._progress.remove_task(self._tasks['generations'])
                except Exception:
                    pass
            if 'population' in self._tasks and self._progress:
                try:
                    self._progress.remove_task(self._tasks['population'])
                except Exception:
                    pass

            if self._progress:
                self._tasks['generations'] = self._progress.add_task("Générations", total=total_generations)
                self._tasks['population'] = self._progress.add_task("Évaluation population", total=population_size)

    def update(self, event: str, data: Dict[str, Any]):
        """Main entry point used by controller/optimizer."""
        try:
            if event == "generation_start":
                self._handle_generation_start(data)
            elif event == "individual_start":
                self._handle_individual_start(data)
            elif event == "individual_end":
                self._handle_individual_end(data)
            elif event == "generation_end":
                self._handle_generation_end(data)
            elif event == "progress_info":
                # could update a footer table
                pass
            elif event == "done":
                # final cleanup
                pass
        except Exception:
            # UI must never raise to break algo
            pass

    def _handle_generation_start(self, data: Dict[str, Any]):
        gen = int(data.get("generation", 0))
        total = int(data.get("total_generations", 1))
        best = data.get("best_cost")
        if best is not None:
            try:
                self._best_cost = min(self._best_cost, float(best))
            except Exception:
                pass
        if self.use_rich and 'generations' in self._tasks and self._progress:
            try:
                self._progress.update(self._tasks['generations'], completed=gen, description=f"Génération {gen}/{total} - Best: {self._format_cost(self._best_cost)}")
            except Exception:
                pass

        # reset population bar at each generation
        if self.use_rich and 'population' in self._tasks and self._progress:
            try:
                self._progress.reset(self._tasks['population'])
            except Exception:
                pass

    def _handle_individual_start(self, data: Dict[str, Any]):
        idx = int(data.get("index", 0))
        total = int(data.get("population_size", 1))
        worker = data.get("worker", "")
        desc = f"Éval {idx}/{total} {worker}"
        if self.use_rich and 'population' in self._tasks and self._progress:
            try:
                self._progress.update(self._tasks['population'], description=desc)
                self._progress.update(self._tasks['population'], completed=max(0, idx - 1))
            except Exception:
                pass

    def _handle_individual_end(self, data: Dict[str, Any]):
        idx = int(data.get("index", 0))
        cost = data.get("cost")
        if cost is not None:
            try:
                if float(cost) < self._best_cost:
                    self._best_cost = float(cost)
                self._topk.append(float(cost))
                self._topk = sorted(self._topk)[:5]
            except Exception:
                pass
        if self.use_rich and 'population' in self._tasks and self._progress:
            try:
                self._progress.update(self._tasks['population'], completed=idx, description=f"Éval {idx}/{self._progress.tasks[self._tasks['population']].total}")
            except Exception:
                pass

    def _handle_generation_end(self, data: Dict[str, Any]):
        gen = int(data.get("generation", 0))
        best = data.get("best_cost", None)
        if best is not None:
            try:
                self._best_cost = min(self._best_cost, float(best))
            except Exception:
                pass
        if self.use_rich and 'generations' in self._tasks and self._progress:
            try:
                self._progress.update(self._tasks['generations'], completed=gen, description=f"Génération {gen} - Best: {self._format_cost(self._best_cost)}")
            except Exception:
                pass

    def _format_cost(self, c: float) -> str:
        try:
            return f"{c:,.0f} FCFA"
        except Exception:
            return str(c)


