
# 1 — Verdict global

Ton plan est réaliste et de faible risque si on limite la portée comme indiqué. L’essentiel est de :

* centraliser la conversion INP→modèle en mémoire,
* normaliser l’API d’appel des optimiseurs (inputs/outputs),
* ajouter les flags de contraintes et un wrapper de raffinage (hybrid-refiner) côté commande,
* garantir journalisation/format V11 et tests e2e.

Je propose d’implémenter V14 en **3 étapes simples** : *ingest INP*, *routing/mapping contraintes → optimiser*, *post-traitement + journaux/rapports*.

# 2 — Améliorations et précisions à intégrer (prioritaires)

### 2.1 Validation d’entrée & priorité des contraintes

* Valider en premier les inputs (fichier, suffixe) et rejeter tôt les combinaisons impossibles (ex: `--method surrogate` sans `--diameter-candidates`).
* Priorité des contraintes :

  * **Hard constraints** : `pression-min` doit être traitée en contrainte dure (rejet d’une solution si violée).
  * **Soft constraints** : `vitesse-min` / `vitesse-max` peuvent être soit hard (option `--force-hard-vel`) soit soft avec pénalité dans la fonction coût. Par défaut je recommande **soft** avec forte pénalité mais proposer `--hard-vel` pour cas stricts.

### 2.2 Stratégies de pénalisation

* Penalty function recommandée : penalty = α × max(0, violation\_amount)^β, avec α configurable (ex: `--penalty-weight`) et β = 1 ou 2.
* Pour GA/Global, add constraint handling via `pymoo` constraints or augment fitness by penalty.

### 2.3 Defaults plausibles et sécurité

* `--pression-min` par défaut = 10 m (ou lu depuis YAML si présent).
* `--vitesse-min` = 0.3 m/s, `--vitesse-max` = 2.0 m/s par défauts recommandés.
* `--method` par défaut = `nested` pour runs rapides, `genetic` pour recherche globale (documenter).

### 2.4 API unifiée interne (critique)

Crée une interface commune que chaque optimiseur implémente :

```py
class BaseOptimizer:
    def __init__(self, network_model: Dict, solver: str, price_db: Optional[PriceDB]=None, config: Dict=None):
        ...
    def optimize(self, constraints: Dict, objective: str='price', seed: Optional[int]=None) -> Dict:
        """
        Retourne: {
           'proposals': [ ... ],
           'best': {...},
           'pareto': [...],  # si multi-objective
           'logs': {...},
           'metrics': {...}
        }
        """
```

Ainsi le CLI fait : `opt = get_optimizer(method)(network, solver, price_db, cfg); result = opt.optimize(constraints, objective)`.

### 2.5 Conversion INP → modèle unifié

* Implémenter `convert_inp_to_unified_model(inp_path: Path) -> network_model: Dict`.
* Utiliser WNTR pour parser INP en mémoire.
* **Important** : inclure métadonnées (elevations, pump-curves, initial-levels, link lengths, diameters, nodes types) et `source='inp'` dans model.meta.
* Option verbose `--dump-model` pour écrire YAML pour debug.

### 2.6 Hybridation (mémétique) : détails pratiques

* Hook minimal côté CLI :

  * Exécuter l’algorithme primaire (ex: GA).
  * À chaque N génération ou à la fin, prendre `top_k` solutions et lancer le `refiner` (ex: `NestedGreedyOptimizer.refine(solution)`).
  * Si résultat amélioré, remplacer dans la population/retour.
* Paramètres exposés :

  * `--hybrid-refiner nested`
  * `--hybrid-topk 3`
  * `--hybrid-steps 2`
  * `--hybrid-frequency 10` (toutes les N générations)
* Par défaut : `topk=2`, `steps=1`, `frequency=20`.

### 2.7 Cache et idempotence

* Générer hash clé : `sha256(network_schema + constraints + H_bounds + diam_vector + price_db_version + solver_version)`.
* Utiliser cache persistant pour simulations coûteuses (WNTR/EPANET runs).
* Log `cache_hit`/`cache_miss`.

# 3 — Spécifications techniques concrètes (fichiers / signatures)

### CLI : signature Typer recommandée (extrait)

```py
@app.command("network-optimize-unified")
def network_optimize_unified(
    input_file: Path,
    method: str = typer.Option("nested", "--method", "-m", help="genetic|nested|surrogate|global|multi-tank"),
    solver: str = typer.Option("epanet", "--solver", help="epanet|lcpi"),
    pression_min: Optional[float] = typer.Option(None, "--pression-min"),
    vitesse_min: Optional[float] = typer.Option(None, "--vitesse-min"),
    vitesse_max: Optional[float] = typer.Option(None, "--vitesse-max"),
    hybrid_refiner: Optional[str] = typer.Option(None, "--hybrid-refiner"),
    hybrid_topk: int = typer.Option(3, "--hybrid-topk"),
    hybrid_steps: int = typer.Option(1, "--hybrid-steps"),
    generations: int = typer.Option(50, "--generations"),
    population: int = typer.Option(60, "--population"),
    objective: str = typer.Option("price", "--objective"),
    output: Optional[Path] = typer.Option(None, "--output"),
    verbose: bool = typer.Option(False, "--verbose"),
):
    ...
```

### Helper convert\_inp\_to\_unified\_model

```py
def convert_inp_to_unified_model(inp_path: Path) -> Dict:
    import wntr
    model = wntr.network.WaterNetworkModel(str(inp_path))
    # build dict with nodes, links, pumps, tanks, elevations, lengths, diameters, material if exist
    return unified_model
```

### Hook hybrid refiner (squelette)

```py
def genetic_with_hybrid(genetic_opt, hybrid_refiner, topk, steps, freq):
    for gen in range(generations):
        genetic_opt.step()
        if gen % freq == 0:
            topk_sols = genetic_opt.get_topk(topk)
            for sol in topk_sols:
                refined = hybrid_refiner.refine(sol, steps=steps)
                genetic_opt.replace_if_better(sol, refined)
```

### JSON de sortie standard (extrait)

```json
{
  "meta": {"method":"genetic+nested_local_search","solver":"epanet","timestamp":"...","price_db_version":"..."},
  "proposals": [
    {"id":"p1","H_tank_m":63.2,"diameters_mm": {...},"CAPEX":12345,"OPEX_NPV":345,"constraints_ok":true}
  ],
  "pareto": [...],
  "cache_info": {"hits":3,"misses":12},
  "logs": {"signed":true, "signature":"..."},
  "report_payload": {...}
}
```

# 4 — Tests d’acceptation (automatique & manuels)

### Tests unitaires à ajouter/imposer

* `test_convert_inp_to_unified_model`: INP minimal → dict with nodes/links/pumps.
* `test_optimizer_api_uniform`: instantiate each optimizer, call `opt.optimize(constraints)` with small network mock.
* `test_hybrid_refiner_integration`: run GA wrapper with mock solver; assert refined best.cost <= pre-refine best.cost.

### Scénarios e2e (CI)

1. `simulate-inp` simple network → must return pressures and velocities.
2. `network-optimize-unified network.inp --method nested --pression-min 15` → output JSON, `proposals` not empty, all proposals have `constraints_ok=True` or flagged failing with proper message.
3. `network-optimize-unified network.yml --method genetic --hybrid-refiner nested` → run completes and output shows `meta.method` includes `+nested_local_search`.

# 5 — Journalisation & reporting

* Toujours appeler `integrity_manager.sign_log(result)` avant sauvegarde.
* Stocker `price_db_info` (path + checksum + version).
* Produire `report_payload` compatible V11 (placeholders).
* Par défaut écriture en `results/<runid>.json` et `results/<runid>.log.json` (signed).

# 6 — Risques / mitigations (récap)

* **Time-consuming GA** → set conservative defaults; enable `--timeout` and checkpointing.
* **EPANET WNTR divergence** → pin package version in CI; validate via example INP.
* **Constraint mismatch** → choose penalty default + offer `--hard-*` flags.
* **Memory for large networks** → recommend surrogate path + decomposition (future).

# 7 — Estimation affinée (en jours-homme)

* INP ingestion & model unifié + tests : 0.5 j
* Flags contraintes & mapping + validation : 0.5 j
* Routing méthode → appels aux optimiseurs + adapter outputs V11 : 0.5–1 j
* Hybridation wrapper (minimal) + tests : 1 j
* Journaux/signature + report adapter + e2e tests : 0.5–1 j
  **Total** ≈ 3 jours (confirmes ton estimation).

# 8 — Priorité d’implémentation (ordre conseillé)

1. INP → modèle unifié (fondation)
2. Normalize optimizer API (BaseOptimizer)
3. CLI flags + routing simple `method->optimizer`
4. Hybridation wrapper (top-k)
5. Tests e2e + journaux/signature + report adapter
6. Perf: cache, parallel, surrogate warmstart

# 9 — Commandes de vérification rapides (à exécuter après implémentation)

```bash
# help
lcpi aep network-optimize-unified --help

# INP nested quick run (mock solver to be fast)
lcpi aep network-optimize-unified examples/simple_net.inp --method nested --solver mock --pression-min 12 --output /tmp/out.json

# YAML genetic + hybrid
lcpi aep network-optimize-unified examples/net.yml --method genetic --hybrid-refiner nested --generations 40 --population 50 --output /tmp/gen_out.json
```

trois modules prêts à coller dans ton repo.
Ils fournissent :

* un wrapper **Typer** pour la commande `network-optimize-unified` (A),
* une **interface `BaseOptimizer`** et des adaptateurs (B),
* un **wrapper d’hybridation (genetic + refiner)** et un contrôleur/factory (C).

Chaque fichier contient des commentaires, des points d’extension et des comportements sûrs (fallbacks / messages clairs). Colle-les exactement aux chemins indiqués, puis exécute les tests rapides proposés.

---

## 1) Fichier A — CLI : `src/lcpi/aep/commands/network_optimize_unified.py`

Place ce fichier ici : `src/lcpi/aep/commands/network_optimize_unified.py`

```python
# src/lcpi/aep/commands/network_optimize_unified.py
"""
Commande Typer: network-optimize-unified
Entrée: .inp ou .yml -> optimisation via method choisi (genetic|nested|surrogate|global|multi-tank)
"""

from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint

# Import controller / helpers
from ...optimizer.controllers import OptimizationController
from ...optimizer.db import PriceDB  # assume existing or keep None if absent

app = typer.Typer(name="network-optimize-unified", help="Optimisation unifiée réseau (INP/YML)")

# Controller singleton (stateless)
_controller = OptimizationController()


@app.command("run")
def network_optimize_unified(
    input_file: Path = typer.Argument(..., help="Fichier réseau (.inp ou .yml)"),
    method: str = typer.Option("nested", "--method", "-m", help="genetic|nested|surrogate|global|multi-tank"),
    solver: str = typer.Option("epanet", "--solver", help="epanet|lcpi|mock"),
    pression_min: Optional[float] = typer.Option(None, "--pression-min", help="Pression minimale (m)"),
    vitesse_min: Optional[float] = typer.Option(None, "--vitesse-min", help="Vitesse minimale (m/s)"),
    vitesse_max: Optional[float] = typer.Option(None, "--vitesse-max", help="Vitesse maximale (m/s)"),
    hybrid_refiner: Optional[str] = typer.Option(None, "--hybrid-refiner", help="nested|global|... (ex: genetic+nested)"),
    hybrid_topk: int = typer.Option(2, "--hybrid-topk", help="Top-K solutions to refine"),
    hybrid_steps: int = typer.Option(1, "--hybrid-steps", help="Local steps for refiner"),
    hybrid_frequency: int = typer.Option(20, "--hybrid-frequency", help="Frequency (generations) to run hybrid refiner (if applicable)"),
    generations: int = typer.Option(50, "--generations", help="Generations (if method supports)"),
    population: int = typer.Option(60, "--population", help="Population size (if method supports)"),
    objective: str = typer.Option("price", "--objective", help="Objective: price|multi"),
    price_db: Optional[Path] = typer.Option(None, "--price-db", help="Chemin vers la DB SQLite des prix"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier JSON de sortie"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose"),
):
    """
    Commande d'optimisation unifiée acceptant .inp et .yml
    """
    # Validate input
    if not input_file.exists():
        rprint(f"[red]Fichier introuvable:[/red] {input_file}")
        raise typer.Exit(code=2)

    # Build constraints dict
    constraints = {
        "pressure_min_m": pression_min,
        "velocity_min_m_s": vitesse_min,
        "velocity_max_m_s": vitesse_max,
    }

    # Price DB
    price_db_obj = None
    if price_db:
        try:
            price_db_obj = PriceDB(str(price_db))
        except Exception as e:
            rprint(f"[yellow]Warning: impossible d'ouvrir price DB: {e}[/yellow] -- continue sans DB")

    # Run controller
    try:
        result = _controller.run_optimization(
            input_path=input_file,
            method=method,
            solver=solver,
            constraints=constraints,
            hybrid_refiner=hybrid_refiner,
            hybrid_params={"topk": hybrid_topk, "steps": hybrid_steps, "frequency": hybrid_frequency},
            algo_params={"generations": generations, "population": population, "objective": objective},
            price_db=price_db_obj,
            verbose=verbose
        )
    except Exception as exc:
        rprint(f"[red]Erreur lors de l'optimisation:[/red] {exc}")
        raise typer.Exit(code=3)

    # Save result
    if output:
        import json
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        rprint(f"[green]Résultat écrit dans[/green] {output}")
    else:
        rprint("[green]Optimisation terminée — résumé :[/green]")
        # print small summary
        meta = result.get("meta", {})
        best = result.get("proposals", [{}])[0] if result.get("proposals") else {}
        rprint(f" method: {meta.get('method')} solver: {meta.get('solver')}")
        rprint(f" best CAPEX: {best.get('CAPEX')} constraints_ok: {best.get('constraints_ok')}")

```

**À faire** : dans ton `src/lcpi/aep/cli.py` ajoute (ou vérifie) l’import et l’ajout du Typer :

```python
from .commands.network_optimize_unified import app as network_optimize_app
app.add_typer(network_optimize_app, name="network-optimize-unified")
```

---

## 2) Fichier B — Interface `BaseOptimizer` + Adaptateur : `src/lcpi/aep/optimizer/base.py`

Place ce fichier ici : `src/lcpi/aep/optimizer/base.py`

```python
# src/lcpi/aep/optimizer/base.py
"""
Interface de base pour les optimiseurs AEP.
Les optimiseurs existants (NestedGreedyOptimizer, GlobalOptimizer, SurrogateOptimizer, GeneticOptimizer)
devraient implémenter cette interface (ou être adaptés via un adaptateur).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class BaseOptimizer(ABC):
    def __init__(self, network_model: Dict[str, Any], solver: str = "epanet",
                 price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None):
        """
        network_model : modèle unifié (nodes, links, pumps, tanks, metadata)
        solver : 'epanet'|'lcpi'|'mock'
        price_db : objet DAO pour les prix (optionnel)
        config : paramètres additionnels (generations, population, etc.)
        """
        self.network_model = network_model
        self.solver = solver
        self.price_db = price_db
        self.config = config or {}

    @abstractmethod
    def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Lance l'optimisation et retourne un dictionnaire standardisé :
        {
            'meta': {...},
            'proposals': [ { 'id': 'p1', 'H_tank_m':.., 'diameters_mm': {...}, 'CAPEX':.., 'OPEX_NPV':.., 'constraints_ok': bool }, ...],
            'pareto': [...],  # optional
            'metrics': {...}
        }
        """
        raise NotImplementedError()

    def refine_solution(self, solution: Dict[str, Any], steps: int = 1) -> Dict[str, Any]:
        """
        Optionnel : si l'optimiseur sait raffiner une solution donnée (local search),
        renvoie une solution améliorée (ou la même). Peut être surchargé.
        """
        # Par défaut, pas de raffinage : renvoyer la solution inchangée
        return solution

# Adaptateur simple (si optimizer existant n'implémente pas BaseOptimizer)
class SimpleAdapter(BaseOptimizer):
    """
    Permet d'encapsuler un optimiseur existant (non-BaseOptimizer) en fournissant optimize().
    L'objet 'impl' doit exposer une méthode 'optimize' ou 'run' qui retourne un dict compatible.
    """
    def __init__(self, impl: Any, network_model: Dict[str, Any], solver: str = "epanet", price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(network_model, solver, price_db, config)
        self.impl = impl

    def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
        # Attempt common method names
        if hasattr(self.impl, "optimize"):
            return self.impl.optimize(constraints=constraints, objective=objective, seed=seed)
        if hasattr(self.impl, "run"):
            return self.impl.run(constraints=constraints, objective=objective, seed=seed)
        # As last resort, try call without args
        try:
            res = self.impl()
            if isinstance(res, dict):
                return res
        except Exception as e:
            raise RuntimeError("Adapter unable to call underlying optimizer: " + str(e))
        raise RuntimeError("Underlying optimizer does not expose a known entry point (optimize/run)")

    def refine_solution(self, solution: Dict[str, Any], steps: int = 1) -> Dict[str, Any]:
        if hasattr(self.impl, "refine_solution"):
            return self.impl.refine_solution(solution, steps=steps)
        if hasattr(self.impl, "refine"):
            return self.impl.refine(solution, steps=steps)
        return solution
```

---

## 3) Fichier C — Controller / Factory / Hybrid wrapper : `src/lcpi/aep/optimizer/controllers.py`

Place ce file here: `src/lcpi/aep/optimizer/controllers.py`

```python
# src/lcpi/aep/optimizer/controllers.py
"""
OptimizationController: factory, INP->model conversion, hybrid wrapper (genetic+nested)
"""

from pathlib import Path
from typing import Dict, Any, Optional
import hashlib
import json
import time
import logging

logger = logging.getLogger("lcpi.optimizer.controllers")

# BaseOptimizer and SimpleAdapter
from .base import BaseOptimizer, SimpleAdapter

# Try importing known optimizers (adapt names to your project)
def _import_optimizer_class(name: str):
    """
    Retourne la classe implémentant l'optimiseur pour 'name'.
    Lève ImportError si introuvable, avec message utile.
    """
    name = name.lower()
    if name == "nested":
        from .algorithms.nested import NestedGreedyOptimizer as C
        return C
    if name == "global":
        from .algorithms.global_opt import GlobalOptimizer as C
        return C
    if name == "surrogate":
        from .algorithms.surrogate import SurrogateOptimizer as C
        return C
    if name == "genetic":
        # genetic optimizer may live in optimization/genetic_algorithm.py
        try:
            from ..optimization.genetic_algorithm import GeneticOptimizer as C
            return C
        except Exception:
            # fallback: try in algorithms
            from .algorithms.global_opt import GlobalOptimizer as C
            return C
    if name == "multi-tank" or name == "multitank":
        from .algorithms.multi_tank import MultiTankOptimizer as C
        return C
    raise ImportError(f"Optimiseur inconnu: {name}")

# Try import wntr for INP parsing
def convert_inp_to_unified_model(inp_path: Path) -> Dict[str, Any]:
    """
    Convertit un .inp en modèle unifié (nodes, links, pumps, tanks, metadata).
    Essaie WNTR si disponible. Si WNTR absente, renvoie une structure minimale.
    """
    inp_path = Path(inp_path)
    try:
        import wntr
    except Exception:
        logger.warning("WNTR non disponible — conversion INP limitée.")
        # Minimal fallback: return file path and mark for upstream parsing
        return {"meta": {"source": "inp", "path": str(inp_path)}, "nodes": {}, "links": {}}

    wn = wntr.network.WaterNetworkModel(str(inp_path))
    # Build a compact unified model
    nodes = {}
    for node_name, node in wn.junctions():
        nodes[node_name] = {
            "elevation": node.elevation,
            "demand": node.base_demand,
            "pattern": getattr(node, "demand_pattern_name", None)
        }
    links = {}
    for link_name, link in wn.links():
        links[link_name] = {
            "link_type": type(link).__name__,
            "length_m": getattr(link, "length", None),
            "diameter_m": getattr(link, "diameter", None),
            "start_node": getattr(link, "start_node_name", None),
            "end_node": getattr(link, "end_node_name", None),
            "roughness": getattr(link, "roughness", None),
        }
    tanks = {}
    for tname, t in wn.tanks():
        tanks[tname] = {"elevation": t.elevation, "init_level": t.init_level, "min_level": t.min_level, "max_level": t.max_level}
    pumps = {}
    for pname, p in wn.pumps():
        pumps[pname] = {"pump_curve": getattr(p, "pump_curve", None)}

    model = {
        "meta": {"source": "inp", "file": str(inp_path), "converted_at": time.time()},
        "nodes": nodes,
        "links": links,
        "tanks": tanks,
        "pumps": pumps
    }
    return model

class OptimizationController:
    """
    Controller orchestrant: lecture input (.inp/.yml), factory optimizers, hybrid wrapper,
    signature/logging via integrity manager.
    """
    def __init__(self, cache=None):
        # cache can be an object implementing get/cache
        self.cache = cache
        try:
            from ...integrity import integrity_manager
            self.integrity_manager = integrity_manager
        except Exception:
            self.integrity_manager = None

    def _load_input(self, input_path: Path) -> Dict[str, Any]:
        s = str(input_path)
        if s.lower().endswith(".inp"):
            model = convert_inp_to_unified_model(input_path)
            return model
        else:
            # assume YAML/JSON
            import yaml
            with open(input_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data

    def _hash_run(self, network_model: Dict[str, Any], constraints: Dict[str, Any], meta: Dict[str, Any]) -> str:
        payload = json.dumps({"network": network_model.get("meta", {}).get("file", "") , "constraints": constraints, "meta": meta}, sort_keys=True, default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get_optimizer_instance(self, method: str, network_model: Dict[str, Any], solver: str, price_db: Optional[Any], config: Optional[Dict[str, Any]] = None) -> BaseOptimizer:
        """
        Instancie un optimiseur basé sur 'method' et retourne un objet conforme à BaseOptimizer.
        """
        method_l = method.lower()
        OptimClass = _import_optimizer_class(method_l)
        try:
            # Try constructing with common signature
            inst = OptimClass(network_model=network_model, solver=solver, price_db=price_db, config=config)
            if isinstance(inst, BaseOptimizer):
                return inst
            # else adapt
            return SimpleAdapter(inst, network_model=network_model, solver=solver, price_db=price_db, config=config)
        except TypeError:
            # fallback: instantiate without kwargs
            inst = OptimClass()
            return SimpleAdapter(inst, network_model=network_model, solver=solver, price_db=price_db, config=config)

    def run_optimization(self,
                         input_path: Path,
                         method: str = "nested",
                         solver: str = "epanet",
                         constraints: Optional[Dict[str, Any]] = None,
                         hybrid_refiner: Optional[str] = None,
                         hybrid_params: Optional[Dict[str, Any]] = None,
                         algo_params: Optional[Dict[str, Any]] = None,
                         price_db: Optional[Any] = None,
                         verbose: bool = False) -> Dict[str, Any]:
        """
        Orchestrates the run: load input -> make optimizer -> run -> optionally hybrid refine -> sign log -> return dict
        """
        constraints = constraints or {}
        algo_params = algo_params or {}
        hybrid_params = hybrid_params or {}

        # Load network model
        network_model = self._load_input(Path(input_path))

        # Create optimizer instance
        optimizer = self.get_optimizer_instance(method, network_model, solver, price_db, config=algo_params)

        # Run optimizer
        result = optimizer.optimize(constraints=constraints, objective=algo_params.get("objective", "price"), seed=algo_params.get("seed"))

        # If hybrid requested and method is genetic (or any), run hybrid post-process/refine
        if hybrid_refiner:
            try:
                # instantiate refiner
                refiner = self.get_optimizer_instance(hybrid_refiner, network_model, solver, price_db, config=algo_params)
                result = self._apply_hybrid_refinement(result, optimizer, refiner, hybrid_params, verbose)
            except Exception as e:
                logger.warning(f"Hybrid refinement failed: {e}")

        # Add meta info
        meta = result.get("meta", {})
        meta.update({"method": method, "solver": solver, "hybrid_refiner": hybrid_refiner, "constraints": constraints})
        result["meta"] = meta

        # Sign the result (auditability)
        if self.integrity_manager:
            try:
                signed = self.integrity_manager.sign_log(result)
                result["integrity"] = signed.get("integrity", result.get("integrity", {}))
            except Exception as e:
                logger.warning(f"Signing failed: {e}")

        return result

    def _apply_hybrid_refinement(self, result: Dict[str, Any], primary_optimizer: BaseOptimizer, refiner: BaseOptimizer, hybrid_params: Dict[str, Any], verbose: bool=False) -> Dict[str, Any]:
        """
        Applique un raffinement local aux top-K solutions du résultat.
        Méthode non intrusive : si optimizer.returned proposals, on raffine ces éléments.
        """
        topk = int(hybrid_params.get("topk", 2))
        steps = int(hybrid_params.get("steps", 1))
        improved = 0
        proposals = result.get("proposals", [])
        if not proposals:
            logger.debug("No proposals found to refine.")
            return result

        # Sort proposals by objective (assume CAPEX exists)
        sorted_props = sorted(proposals, key=lambda p: p.get("CAPEX", float("inf")))
        for sol in sorted_props[:topk]:
            try:
                refined = refiner.refine_solution(sol, steps=steps)
                # If refined has lower CAPEX, replace in proposals
                if refined and refined.get("CAPEX", float("inf")) < sol.get("CAPEX", float("inf")):
                    idx = proposals.index(sol)
                    proposals[idx] = refined
                    improved += 1
                    if verbose:
                        logger.info(f"Hybrid refiner improved solution {sol.get('id')} -> new CAPEX {refined.get('CAPEX')}")
            except Exception as e:
                logger.warning(f"Refinement on solution failed: {e}")
        result["proposals"] = proposals
        result.setdefault("metrics", {})["hybrid_improved_count"] = improved
        return result
```

---

## 4) Notes d’intégration & checklist pour toi

1. **Installer/coler** les trois fichiers aux emplacements indiqués.
2. **Importer la commande** dans le CLI principal (cf. plus haut) : `app.add_typer(network_optimize_app, name="network-optimize-unified")`.
3. **Adapter les imports** des optimiseurs si leurs chemins/nom de classe diffèrent (ex: GeneticOptimizer dans `src/lcpi/aep/optimization/genetic_algorithm.py`). Les `_import_optimizer_class` contient les points d’extension — ajoute d’autres chemins si nécessaire.
4. **Vérifier** que les optimiseurs exposent au minimum `optimize(constraints, objective, seed)` ou sinon, `SimpleAdapter` fera le pont.
5. **Signer les logs** : controller utilise `integrity_manager` si disponible. Assure-toi que `from ...integrity import integrity_manager` correspond au vrai chemin.
6. **WNTR** : si tu veux la conversion INP complète, pin `wntr` dans ton environnement CI ; le code essaie d’importer `wntr` et retourne un fallback minimal s’il est absent.
7. **Tests rapides** :

   * `python -m lcpi aep network-optimize-unified.run examples/simple_net.inp --method nested --solver mock --output /tmp/out.json`
   * `python -m lcpi aep network-optimize-unified.run examples/simple_net.yml --method genetic --hybrid-refiner nested --output /tmp/gen.json`

---

## 5) Snippets de tests unitaires (à ajouter)

`tests/unit/test_network_optimize_cmd.py`

```py
from pathlib import Path
from lcpi.aep.commands.network_optimize_unified import network_optimize_unified
def test_cmd_help():
    # just ensure function exists and signature works
    assert callable(network_optimize_unified)
```

`tests/unit/test_convert_inp.py`

```py
from lcpi.aep.optimizer.controllers import convert_inp_to_unified_model
def test_convert_inp_minimal(tmp_path):
    dummy = tmp_path / "dummy.inp"
    dummy.write_text("[JUNCTIONS]\n; none\n")
    out = convert_inp_to_unified_model(dummy)
    assert "meta" in out
```

---

## 6) Remarques finales / conseils pratiques

* **Adaptation progressive** : commence par brancher `network-optimize-unified` sur `nested` (plus simple), puis ajoute genetic/hybrid et tests.
* **Logging** : augmente le logging dans `OptimizationController` pour debuggage (niveau DEBUG).
* **Fallbacks** : `SimpleAdapter` garantit que les anciens optimiseurs non conformes continuent de fonctionner.
* **Performance** : pour GA + hybrid, recommande exécuter d’abord en `--solver mock`/`--dry-run` pour valider wiring, puis en `epanet`/`lcpi` réels.
