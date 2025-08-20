Parfait — je te fournis **(A)** un script d’audit/diagnostic prêt à l’emploi qui exécute les runs LCPI (différentes configurations), mesure temps/compteurs, compare avec EPANET via WNTR si disponible et produit un rapport lisible ; et **(B)** des **patchs/clips de code** à coller dans les fichiers clés pour **instrumenter** l’exécution (timings, compteurs, cache flags, hook GA).

Je donne : où mettre chaque fichier, comment l’exécuter, exemples d’interprétation des résultats, et un petit test CI scriptable.

---

# A — Script d’audit/diagnostic (prêt à exécuter)

Crée un fichier `tools/lcpi_diagnostics.py` à la racine du repo (ou dans `tools/`) et colles-y le code suivant.

```python
#!/usr/bin/env python3
"""
lcpi_diagnostics.py
Script d'audit rapide pour vérifier si `lcpi aep network-optimize-unified`
lance réellement le solveur EPANET / effectue des évaluations, ou si le run est
court-circuité (cache / surrogate / mock).

Usage:
    python tools/lcpi_diagnostics.py --input examples/mon_reseau.inp
"""

import argparse
import json
import shutil
import subprocess
import time
import sys
from pathlib import Path

def run_cmd(cmd, env=None, timeout=None):
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    dt = time.time() - t0
    return proc.returncode, proc.stdout + proc.stderr, dt

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        return None

def print_section(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def main():
    parser = argparse.ArgumentParser(description="Diagnostic LCPI: vérifie solver calls, cache, surrogate, timings")
    parser.add_argument("--input", "-i", required=True, help="Fichier .inp ou .yml")
    parser.add_argument("--out", "-o", default="/tmp/lcpi_diag_out.json", help="Fichier de sortie JSON produit par LCPI")
    parser.add_argument("--runs", type=int, default=1, help="Nombre d'itérations rapide")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_json = Path(args.out)

    if not shutil.which("lcpi"):
        print("ERREUR: la commande `lcpi` n'est pas trouvée dans le PATH. Assure-toi d'activer l'environnement virtuel.")
        sys.exit(2)

    # Baseline: short run with defaults
    cmd_base = [
        "lcpi", "aep", "network-optimize-unified",
        str(input_path),
        "--solver", "epanet",
        "--method", "genetic",
        "--verbose",
        "--output", str(out_json)
    ]

    print_section("RUN 1 - baseline (genetic, solver=epanet)")
    rc, out, dt = run_cmd(cmd_base, timeout=600)
    print(f"Return code: {rc}  | Duration: {dt:.2f}s")
    if args.verbose: print(out[:2000])

    data1 = load_json(out_json)
    if not data1:
        print("⚠️  Aucun JSON produit par LCPI (vérifier logs).")
    else:
        print("Meta fields:", list(data1.get("meta", {}).keys()))
        meta = data1.get("meta", {})
        print("meta.duration_seconds:", meta.get("duration_seconds"))
        print("meta.solver_calls:", meta.get("solver_calls"))
        print("meta.eval_count:", meta.get("eval_count"))
        print("meta.cache_hit:", meta.get("cache_hit"))
        print("meta.surrogate_used:", meta.get("surrogate_used"))

    # Run 2: force no-cache / no-surrogate if flags exist (fallback: pass --no-cache --no-surrogate)
    print_section("RUN 2 - no-cache / no-surrogate (if supported)")
    cmd_nc = cmd_base + ["--no-cache", "--no-surrogate", "--generations", "80", "--population", "60"]
    rc, out, dt = run_cmd(cmd_nc, timeout=1800)
    print(f"Return code: {rc}  | Duration: {dt:.2f}s")
    data2 = load_json(out_json)
    if data2:
        meta = data2.get("meta", {})
        print("meta.duration_seconds:", meta.get("duration_seconds"))
        print("meta.solver_calls:", meta.get("solver_calls"))
        print("meta.eval_count:", meta.get("eval_count"))
        print("meta.cache_hit:", meta.get("cache_hit"))
        print("meta.surrogate_used:", meta.get("surrogate_used"))

    # Run 3: big run to stress GA (should take longer)
    print_section("RUN 3 - stress GA (generations=150, population=100)")
    cmd_big = cmd_base + ["--no-cache", "--no-surrogate", "--generations", "150", "--population", "100"]
    rc, out, dt = run_cmd(cmd_big, timeout=7200)
    print(f"Return code: {rc}  | Duration: {dt:.2f}s")
    data3 = load_json(out_json)
    if data3:
        meta = data3.get("meta", {})
        print("meta.duration_seconds:", meta.get("duration_seconds"))
        print("meta.solver_calls:", meta.get("solver_calls"))
        print("meta.eval_count:", meta.get("eval_count"))
        print("meta.cache_hit:", meta.get("cache_hit"))
        print("meta.surrogate_used:", meta.get("surrogate_used"))

    # Optional: compare LCPI pressures with WNTR if available and out file contains pressures
    try:
        import wntr
        wntr_ok = True
    except Exception:
        wntr_ok = False

    if wntr_ok and data1:
        print_section("Vérification EPANET vs WNTR (si LCPI fournit pressures_m)")
        # run WNTR simulation of the input .inp
        try:
            wn = wntr.network.WaterNetworkModel(str(input_path))
            sim = wntr.sim.EpanetSimulator(wn)
            res = sim.run()
            pressures = res.node['pressure'].iloc[-1].to_dict()
            # sample comparison
            solver_data = data1.get("solver_data", {})
            any_compared = False
            for solver, sd in (solver_data.items() if solver_data else []):
                proposals = sd.get("proposals") or []
                if not proposals: continue
                best = proposals[0]
                p_lcpi = best.get("pressures_m") or {}
                # pick up to 5 nodes present in both
                common = [n for n in list(pressures.keys())[:10] if n in p_lcpi]
                if not common:
                    continue
                print(f"Comparaison pour solver={solver}, noeuds échantillon: {common[:5]}")
                for n in common[:5]:
                    v_epanet = pressures[n]
                    v_lcpi = p_lcpi[n]
                    print(f" node={n}  WNTR={v_epanet:.3f} m   LCPI={v_lcpi:.3f} m   delta={(v_lcpi - v_epanet):+.3f}")
                any_compared = True
            if not any_compared:
                print("Aucune pression comparable trouvée dans la sortie LCPI (champ pressures_m absent).")
        except Exception as e:
            print("Erreur lors de simulation WNTR:", e)
    else:
        if not wntr_ok:
            print("WNTR non présent — installe `pip install wntr` pour vérification hydraulique.")

    # Heuristique d'alerte simple
    print_section("RAPPORT SYNTHÉTIQUE")
    suspect = False
    for idx, d in enumerate((data1, data2, data3), start=1):
        if not d:
            print(f"Run{idx}: PAS DE JSON")
            suspect = True
            continue
        m = d.get("meta", {})
        dur = m.get("duration_seconds") or 0
        sc = m.get("solver_calls") or 0
        ec = m.get("eval_count") or 0
        su = m.get("surrogate_used")
        ch = m.get("cache_hit")
        print(f"Run{idx}: duration={dur}s, solver_calls={sc}, eval_count={ec}, surrogate={su}, cache_hit={ch}")
        # suspicious if duration < 2s and solver_calls == 0 and surrogate_used not true
        if dur < 2 and sc == 0 and not su:
            print(" --> SUSPICION: run très court sans appel solver ni surrogate.")
            suspect = True

    if suspect:
        print("\nWARNING: Il y a des indices qu'un court-circuit (cache/mock/surrogate non validé) est en place. Voir logs et instrumentation.")
    else:
        print("\nOK: Les runs semblent effectuer des évaluations / appels solver.")

if __name__ == "__main__":
    main()
```

### Utilisation

1. Rends le script exécutable et lance-le :

```bash
python tools/lcpi_diagnostics.py --input examples/mon_reseau.inp --verbose
```

2. Observe les trois runs (baseline / no-cache / stress) et regarde les champs `meta.duration_seconds`, `meta.solver_calls`, `meta.eval_count`, `meta.cache_hit`, `meta.surrogate_used` dans la sortie JSON.

---

# B — Patches / snippets à appliquer dans le code LCPI (instrumentation)

Je fournis des **squelettes** sûrs et faciles à coller. L’idée : centraliser des compteurs (stats), minuter les appels solveur, incrémenter les compteurs d’évaluation GA, exposer meta fields à la fin du controller.

## 1) Nouveau module de stats : `src/lcpi/aep/optimizer/stats.py`

Crée ce fichier et colles-y :

```python
# src/lcpi/aep/optimizer/stats.py
import threading
import time

class RunStats:
    def __init__(self):
        self._lock = threading.Lock()
        self.solver_calls = 0
        self.solver_time = 0.0
        self.eval_count = 0
        self.cache_hits = 0
        self.surrogate_evals = 0
        self.start_time = time.time()
        self.extra = {}

    def add_solver_call(self, dt):
        with self._lock:
            self.solver_calls += 1
            self.solver_time += float(dt)

    def incr_eval(self, n=1):
        with self._lock:
            self.eval_count += int(n)

    def incr_cache_hit(self, n=1):
        with self._lock:
            self.cache_hits += int(n)

    def incr_surrogate(self, n=1):
        with self._lock:
            self.surrogate_evals += int(n)

    def snapshot_meta(self):
        now = time.time()
        return {
            "duration_seconds": round(now - self.start_time, 3),
            "solver_calls": self.solver_calls,
            "solver_time_seconds": round(self.solver_time, 3),
            "eval_count": self.eval_count,
            "cache_hits": self.cache_hits,
            "surrogate_evals": self.surrogate_evals,
            **self.extra
        }

# singleton (import from other modules)
GLOBAL_RUN_STATS = RunStats()
```

## 2) Décorateur pour minuter les appels solveur

Ajoute dans `src/lcpi/aep/optimizer/solvers/epanet_optimizer.py` (ou dans un utils) :

```python
# en haut du fichier
import time
import logging
from ...optimizer.stats import GLOBAL_RUN_STATS

logger = logging.getLogger("lcpi.optimizer.epanet")

def timed_solver_call(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        dt = time.time() - t0
        try:
            GLOBAL_RUN_STATS.add_solver_call(dt)
        except Exception:
            pass
        logger.info("EPANET solver call %s took %.3fs", getattr(func, "__name__", str(func)), dt)
        return res
    return wrapper
```

Ensuite **enrobe** la méthode qui lance la simulation (ex : `simulate_with_tank_height`) :

```python
class EPANETOptimizer:
    ...
    @timed_solver_call
    def simulate_with_tank_height(self, network_model: Dict, H_tank: float, diameters: Dict[str, int]) -> Dict:
        # implementation existing
        ...
```

> Si ton wrapper EPANET utilise une autre méthode, applique le décorateur là où le solveur EPANET est réellement lancé.

## 3) Incrémenter `eval_count` dans GeneticOptimizer

Dans `src/lcpi/aep/optimization/genetic_algorithm.py` (ou où l'évaluation est faite) :

* Ajoute import :

```python
from ...optimizer.stats import GLOBAL_RUN_STATS
```

* Au début de la fonction d’évaluation (où tu simules une solution pour obtenir fitness), incrémente :

```python
# inside evaluate_individual or similar
GLOBAL_RUN_STATS.incr_eval(1)
```

* Ajoute un hook facultatif `on_generation_callback` dans la classe `GeneticOptimizer` :

```python
class GeneticOptimizer:
    def __init__(self, config, ...):
        ...
        self.on_generation_callback = None  # callback(population, gen_index)

    def _evolution_loop(self):
        for gen in range(self.config.generations):
            # evaluate population...
            if callable(self.on_generation_callback):
                try:
                    self.on_generation_callback(self.population, gen)
                except Exception:
                    logger.exception("on_generation_callback failed")
```

Le controller pourra fournir un callback qui applique le `nested` refiner au top-K.

## 4) Signaler cache hits dans le cache module

Si tu as un module `optimizer/cache.py`, assure-toi d’appeler `GLOBAL_RUN_STATS.incr_cache_hit()` lorsqu’il retourne une valeur du cache.

Exemple :

```python
from .stats import GLOBAL_RUN_STATS

def get_cached_result(...):
    ...
    if found:
        GLOBAL_RUN_STATS.incr_cache_hit()
        return result
```

## 5) Injecter `meta` final dans le controller

À la fin de `OptimizationController.run()` (ou la méthode qui orchestre l’optim), avant de sauver le JSON, ajoute :

```python
from ..optimizer.stats import GLOBAL_RUN_STATS
# ... after optimization completes
meta_stats = GLOBAL_RUN_STATS.snapshot_meta()
result_payload["meta"] = result_payload.get("meta", {})
result_payload["meta"].update(meta_stats)
# also add price_db provenance if available
if hasattr(self, "price_db_path") and self.price_db_path:
    import hashlib
    p = Path(self.price_db_path)
    if p.exists():
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        result_payload["meta"]["price_db_info"] = {"path": str(p), "sha256": sha}
```

---

## 6) Option CLI pour désactiver cache / surrogate

Dans `src/lcpi/aep/commands/network_optimize_unified.py` (Typer command), expose deux flags:

```python
import typer

@app.command()
def network_optimize_unified(input_file: Path,
                             no_cache: bool = typer.Option(False, "--no-cache", help="Désactive le cache"),
                             no_surrogate: bool = typer.Option(False, "--no-surrogate", help="Désactive surrogate"),
                             ...):
    controller = OptimizationController(...)
    controller.config.use_cache = not no_cache
    controller.config.use_surrogate = not no_surrogate
    ...
```

Assure-toi que le controller / cache module lit `controller.config.use_cache`.

---

# Exemples d’interprétation des résultats (après avoir appliqué A+B)

* **Si `meta.solver_calls >= 1000` et duration >> 5s** → optimisation réelle (GA) en route (normal pour gros paramètres).
* **Si `meta.solver_calls == 0` et `meta.duration_seconds < 3`** → très suspect : probablement mock, cache trop permissif, ou surrogate sans validation.
* **Si `meta.surrogate_evals > 0` mais `meta.solver_calls < 10`** → surrogate est utilisé mais pas validé assez : augmente `n_validation` ou impose `min_validations`.
* **Si `meta.cache_hits` élevé dès run1** → clé de cache erronée (hash trop générique) — corriger hash pour inclure constraints, price\_db checksum, solver version, seed.
* **Si `wntr` comparaison montre deltas importants (>0.1 m)** → attention : LCPI pressures diverge de EPANET; vérifier wrapper extraction mapping node ids.

---

# Tests Pytest rapides (optionnel mais utile pour CI)

Crée `tests/integration/test_instrumentation.py` :

```python
def test_lcpi_instrumentation_runs(tmp_path):
    # run lcpi with small config (mock) and assert meta fields present
    out = tmp_path / "r.json"
    cmd = ["lcpi","aep","network-optimize-unified","examples/simple_net.inp","--solver","epanet","--output",str(out)]
    import subprocess, json
    rc = subprocess.run(cmd).returncode
    assert rc == 0
    data = json.loads(out.read_text())
    assert "meta" in data
    assert "duration_seconds" in data["meta"]
    assert "solver_calls" in data["meta"]
```

---

# Derniers conseils pratiques

* **Applique les patches progressivement** : teste d’abord la stats singleton, puis le décorateur sur le solveur, puis incrément `eval_count` et enfin l’export meta.
* **Commits petits et atomiques** (1 fichier / 1 objectif).
* **Ajoute logs** : `logger.info` dans les endroits clefs (début/fin d’optimisation, nombre d’évaluations, cache hits). Ça simplifie beaucoup le débogage.
* **Ajoute une variable d’environnement `LCPI_INSTRUMENT=1`** pour activer/désactiver instrumentation en prod si besoin.

---