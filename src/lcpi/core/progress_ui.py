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
		self._num_solvers = 1
		self._total_generations = 1
		self._population_size = 1
		# suivi simulations
		self._sim_busy = 0
		self._sim_done = 0
		# queue pour événements (optionnel)
		self.event_q: _Optional[queue.Queue] = None
		self._listener_thread: _Optional[threading.Thread] = None
		self._stop_listener = threading.Event()
		self._last_update_ts = 0.0
		# Fallback visuel: timer pour faire avancer les barres même sans événements
		self._fallback_timer: Optional[threading.Timer] = None
		self._fallback_interval = 2.0  # secondes

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
		self._stop_fallback_timer()

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

	def setup_tasks(self, total_generations: int = 1, population_size: int = 1, num_solvers: int = 1):
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
			if 'solvers' in self._tasks and self._progress:
				try:
					self._progress.remove_task(self._tasks['solvers'])
				except Exception:
					pass
			if 'total' in self._tasks and self._progress:
				try:
					self._progress.remove_task(self._tasks['total'])
				except Exception:
					pass

			if self._progress:
				self._num_solvers = max(1, int(num_solvers))
				self._total_generations = max(1, int(total_generations))
				self._population_size = max(1, int(population_size))
				self._tasks['solvers'] = self._progress.add_task("Solveurs", total=self._num_solvers)
				self._tasks['generations'] = self._progress.add_task("Générations", total=self._total_generations)
				self._tasks['population'] = self._progress.add_task("Évaluation population", total=self._population_size)
				# Total ~ générations * population (approx pour donner une tendance globale)
				self._tasks['total'] = self._progress.add_task("Total", total=self._total_generations * self._population_size)
				# Barre simulations
				self._sim_busy = 0
				self._sim_done = 0
				self._tasks['simulations'] = self._progress.add_task("Simulations (busy: 0 | done: 0)", total=self._total_generations * self._population_size, completed=0)
				
				# Démarrer le timer de fallback pour faire avancer les barres
				self._start_fallback_timer()

	def update(self, event: str, data: Dict[str, Any]):
		"""Main entry point used by controller/optimizer."""
		        # Event processing
		try:
			# throttling ~5 Hz
			import time as _time
			now = _time.time()
			# Ne pas throttler les événements critiques pour l'avancement visible
			if (now - self._last_update_ts) < 0.2 and event not in ("best_improved", "sim_done", "individual_start", "individual_end", "generation_start", "generation_end"):
				        # Throttled
				return
			self._last_update_ts = now
			if event == "run_start":
				try:
					total_gen = int(data.get("generations", self._total_generations))
					pop = int(data.get("population", self._population_size))
					solvers = int(data.get("num_solvers", self._num_solvers))
					self.setup_tasks(total_generations=total_gen, population_size=pop, num_solvers=solvers)
				except Exception:
					pass
			elif event == "generation_start":
				self._handle_generation_start(data)
			elif event == "individual_start":
				self._handle_individual_start(data)
			elif event == "individual_end":
				self._handle_individual_end(data)
			elif event == "generation_end":
				self._handle_generation_end(data)
			elif event == "best_improved":
				try:
					new_cost = float(data.get("new_cost"))
					if new_cost < self._best_cost:
						self._best_cost = new_cost
						if self.use_rich and 'generations' in self._tasks and self._progress:
							self._progress.update(self._tasks['generations'], description=f"Best: {self._format_cost(self._best_cost)}")
				except Exception:
					pass
			elif event == "progress_info":
				# could update a footer table
				pass
			elif event == "solver_start":
				# Reset bars for new solver and update solver task with name and index
				idx = int(data.get("index", 0))
				total = int(data.get("total", 1))
				name = str(data.get("solver", "?")).upper()
				if self.use_rich and self._progress and 'solvers' in self._tasks:
					try:
						# set description and completed to idx-1 then advance to idx
						self._progress.update(self._tasks['solvers'], description=f"Solveur {idx}/{total}: {name}")
						current_completed = self._progress.tasks[self._tasks['solvers']].completed or 0
						if idx - 1 > current_completed:
							self._progress.update(self._tasks['solvers'], completed=idx - 1)
					except Exception:
						pass
				# reset generation/population for the new solver
				if self.use_rich and self._progress:
					try:
						if 'generations' in self._tasks:
							self._progress.reset(self._tasks['generations'])
						if 'population' in self._tasks:
							self._progress.reset(self._tasks['population'])
					except Exception:
						pass
			elif event == "solver_end":
				# Mark one solver as completed
				if self.use_rich and self._progress and 'solvers' in self._tasks:
					try:
						self._progress.update(self._tasks['solvers'], advance=1)
					except Exception:
						pass
			elif event == "sim_start":
				self._sim_busy += 1
				if self.use_rich and self._progress and 'simulations' in self._tasks:
					try:
						self._progress.update(self._tasks['simulations'], description=f"Simulations (busy: {self._sim_busy} | done: {self._sim_done})")
					except Exception:
						pass
			elif event == "sim_done":
				if self._sim_busy > 0:
					self._sim_busy -= 1
				self._sim_done += 1
				if self.use_rich and self._progress and 'simulations' in self._tasks:
					try:
						current = self._progress.tasks[self._tasks['simulations']].completed or 0
						self._progress.update(
							self._tasks['simulations'],
							description=f"Simulations (busy: {self._sim_busy} | done: {self._sim_done})",
							completed=max(current, self._sim_done),
						)
					except Exception:
						pass
			elif event == "simulation":
				# Payload unifié: {stage: running|success|error, busy: int, done: int}
				try:
					busy = int(data.get("busy", 0))
					done = int(data.get("done", 0))
				except Exception:
					busy = 0
					done = 0
				self._sim_busy = busy
				self._sim_done = done
				if self.use_rich and self._progress and 'simulations' in self._tasks:
					try:
						current = self._progress.tasks[self._tasks['simulations']].completed or 0
						self._progress.update(
							self._tasks['simulations'],
							description=f"Simulations (busy: {busy} | done: {done})",
							completed=max(current, done),
						)
					except Exception:
						pass
			elif event == "generation":
				# Certains callbacks envoient "generation" au lieu de "generation_start"
				self._handle_generation_start(data)
				# Avancer la barre totale d'une génération
				if self.use_rich and 'total' in self._tasks and self._progress:
					try:
						self._progress.update(self._tasks['total'], advance=1)
					except Exception:
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
				# avancer au rang courant pour refléter l'évaluation en cours
				self._progress.update(self._tasks['population'], description=desc, completed=idx)
			except Exception:
				pass

		# Avancer aussi la barre 'Total' à chaque évaluation
		if self.use_rich and 'total' in self._tasks and self._progress:
			try:
				self._progress.update(self._tasks['total'], advance=1)
			except Exception:
				pass

		# Fallback visuel: si aucun individu n'est émis mais que génération évolue, avancer Population doucement
		if self.use_rich and 'population' in self._tasks and self._progress and idx == 0:
			try:
				current = self._progress.tasks[self._tasks['population']].completed or 0
				self._progress.update(self._tasks['population'], completed=current + 1)
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
				current = self._progress.tasks[self._tasks['population']].completed or 0
				self._progress.update(self._tasks['population'], completed=max(current, idx), description=f"Éval {idx}/{self._progress.tasks[self._tasks['population']].total}")
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
				# Avancer d'un cran si l'événement de fin de génération est utilisé
				current_completed = self._progress.tasks[self._tasks['generations']].completed or 0
				completed = max(current_completed, gen)
				self._progress.update(self._tasks['generations'], completed=completed, description=f"Génération {gen} - Best: {self._format_cost(self._best_cost)}")
			except Exception:
				pass

	def _format_cost(self, c: float) -> str:
		try:
			return f"{c:,.0f} FCFA"
		except Exception:
			return str(c)

	def _start_fallback_timer(self):
		"""Démarre un timer qui fait avancer les barres progressivement même sans événements."""
		if not self.use_rich or not self._progress:
			return
		
		# Arrêter le timer précédent s'il existe
		if self._fallback_timer:
			self._fallback_timer.cancel()
		
		def _fallback_update():
			try:
				with self._lock:
					if not self.use_rich or not self._progress:
						return
					
					# Faire avancer la barre Total progressivement
					if 'total' in self._tasks:
						current = self._progress.tasks[self._tasks['total']].completed or 0
						total = self._progress.tasks[self._tasks['total']].total or 1
						if current < total:
							# Avancer de 1-2% du total
							advance = max(1, total // 100)
							new_completed = min(current + advance, total)
							self._progress.update(self._tasks['total'], completed=new_completed)
					
					# Faire avancer la barre Population progressivement
					if 'population' in self._tasks:
						current = self._progress.tasks[self._tasks['population']].completed or 0
						total = self._progress.tasks[self._tasks['population']].total or 1
						if current < total:
							advance = max(1, total // 50)
							new_completed = min(current + advance, total)
							self._progress.update(self._tasks['population'], completed=new_completed)
					
					# Faire avancer la barre Simulations progressivement
					if 'simulations' in self._tasks:
						current = self._progress.tasks[self._tasks['simulations']].completed or 0
						total = self._progress.tasks[self._tasks['simulations']].total or 1
						if current < total:
							advance = max(1, total // 100)
							new_completed = min(current + advance, total)
							self._progress.update(self._tasks['simulations'], completed=new_completed)
					
					# Redémarrer le timer si on n'a pas encore terminé
					if current < total:
						self._fallback_timer = threading.Timer(self._fallback_interval, _fallback_update)
						self._fallback_timer.daemon = True
						self._fallback_timer.start()
					
			except Exception:
				# Ignorer les erreurs de fallback
				pass
		
		# Démarrer le premier timer
		self._fallback_timer = threading.Timer(self._fallback_interval, _fallback_update)
		self._fallback_timer.daemon = True
		self._fallback_timer.start()

	def _stop_fallback_timer(self):
		"""Arrête le timer de fallback."""
		if self._fallback_timer:
			self._fallback_timer.cancel()
			self._fallback_timer = None


