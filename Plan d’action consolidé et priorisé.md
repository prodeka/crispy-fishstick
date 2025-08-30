# Plan d’action **consolidé et priorisé** (version finale) — intégrant _tout_ ce que vous avez dit

Je vous donne un plan opérationnel, priorisé, avec tâches précises, fichiers à modifier, extraits de code prêts à coller, commandes de test, critères d’acceptation et recommandations de suivi. Il intègre **centralisation diamètres/prix**, **pénalités adaptatives**, **réparation douce**, **mode Pareto**, **instrumentation/UI**, **diagnostics WNTR + artefacts (CSV/JSON/PNG)**, **bundling wkhtmltopdf**, et toutes les corrections d’événements / progression que nous avons parcourues.

---

# Résumé rapide (1 ligne)

Priorité 1 = garantir une **source de vérité pour diamètres & prix**; priorité 2 = rendre l’AG robuste (pénalités adaptatives + réparation douce); priorité 3 = observabilité (progression, best_cost central) + artefacts et distribution PDF.

---

# Phase 0 — Pré-requis immédiats

- Branche git : `feature/optimizer-unify`
    
- Virtualenv propre + tests `pytest`
    
- Localiser `aep_prices.db` (ou prévoir fallback)
    
- Backups des fichiers modifiés
    

---

# Phase 1 — Centralisation diamètres & prix (impératif)

**Objectif :** une seule source (controller → optimiseurs → scoring).

## 1.1 Nouveau module `diameter_manager`

**Fichier** : `src/lcpi/aep/optimizer/diameter_manager.py`

```python
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path
import sqlite3

class PipeType(BaseModel):
    d_mm: int
    price_fcfa_m: float
    material: str = "PVC-U"

def get_standard_diameters_with_prices(price_db_path: Optional[str] = None) -> List[PipeType]:
    # 1 try DB
    if price_db_path:
        p = Path(price_db_path)
        if p.exists():
            try:
                conn = sqlite3.connect(str(p))
                cur = conn.cursor()
                cur.execute("SELECT diameter_mm, price_fcfa_m, material FROM diameters")
                rows = cur.fetchall()
                return [PipeType(d_mm=int(r[0]), price_fcfa_m=float(r[1]), material=r[2] or "PVC") for r in rows]
            except Exception:
                pass
    # 2 fallback realistic list (estimates, not uniform)
    fallback = [
        (50, 1200), (63, 1500), (75, 1800), (90, 2100),
        (110, 2600), (160, 4200), (200, 6200), (250, 9000),
        (315, 14000), (400, 21000)
    ]
    return [PipeType(d_mm=d, price_fcfa_m=p) for d,p in fallback]
```

## 1.2 Utilisation centrale dans `controllers.py`

Remplacer tout `diam_rows = ...` / fallback brut par :

```python
from .optimizer.diameter_manager import get_standard_diameters_with_prices
diam_cands = get_standard_diameters_with_prices(price_db_path=str(db_path_to_use) if db_path_to_use else None)
# Convertir en objets attendus par l'algorithme (p.ex. DiametreCommercial)
```

## 1.3 Unifier calcul CAPEX

**Fichier** : `src/lcpi/aep/optimizer/scoring.py` (ou créer)  
Fonction `compute_capex(diam_map, candidate_list)` -> chercher prix via `PipeType.d_mm`.

## Tests

- `tests/test_diameter_manager.py` : PriceDB présent / absent.
    
- Exécution GA petite pour vérifier CAPEX cohérent.
    

## Critère d’acceptation

- `meta.price_db_info` renseigné et `proposals[0].CAPEX` égal au calcul via `get_standard_diameters_with_prices`.
    

---

# Phase 2 — Pénalité adaptative non linéaire + normalisation des violations

**Objectif :** taux de pénalités proportionnel à la sévérité et à l’étape (génération).

## 2.1 Normalisation des violations

**Fichier** : `src/lcpi/aep/optimization/constraints_handler.py`  
Ajouter :

```python
def normalize_violations(sim_metrics: dict, constraints: dict) -> dict:
    # Retourne dict détaillé: pressure_ratio, velocity_ratio, total
    pressure_req = float(constraints.get("pressure_min_m", 10.0))
    p_min = float(sim_metrics.get("min_pressure_m", 0.0) or 0.0)
    pressure_ratio = max(0.0, (pressure_req - p_min) / max(1.0, pressure_req))
    vmax = float(constraints.get("velocity_max_m_s", 2.0))
    v_max_obs = float(sim_metrics.get("max_velocity_m_s", 0.0) or 0.0)
    velocity_ratio = max(0.0, (v_max_obs - vmax) / max(1.0, vmax))
    total = pressure_ratio * 0.6 + velocity_ratio * 0.4
    return {"pressure": pressure_ratio, "velocity": velocity_ratio, "total": total}
```

## 2.2 adaptive_penalty renvoyant dict détaillé

```python
def adaptive_penalty(violation_total: float, generation: int, total_generations: int,
                     alpha_start=1e5, alpha_max=1e8, beta=1.8) -> dict:
    t = float(generation)/max(1, total_generations)
    alpha = min(alpha_start*(1 + 10*t), alpha_max)
    penalty = alpha * (violation_total ** beta)
    return {"penalty": penalty, "alpha": alpha, "beta": beta}
```

## 2.3 Intégration dans GA

Dans `GeneticOptimizer.evaluer_fitness` (ou équivalent) :

- appeler `normalize_violations`, puis `adaptive_penalty(sim_violation["total"], generation, total_gen)`.
    
- fitness = 1/(1 + capex + penalty)
    
- Enregistrer `individu.metrics["violations"]` détaillé et `individu.metrics["penalty_info"]`.
    

## Tests

- Unit tests pour `normalize_violations` et `adaptive_penalty`.
    
- Vérifier monotonicité.
    

## Critère d’acceptation

- Solutions fortement violantes obtiennent pénalités exponentielles et n’arrivent pas en tête.
    

---

# Phase 3 — Réparation douce (soft repair)

**Objectif :** modifier _peu_ les meilleures solutions infaisables, pas tout le monde.

## 3.1 Nouvelle fonction `soft_repair_solution`

**Fichier** : `src/lcpi/aep/optimization/repairs.py`

```python
def soft_repair_solution(diam_map: dict, sim_metrics: dict, candidate_list: List[int], max_changes_frac=0.05):
    # identify problematic pipe ids via local pressure or headloss (requires sim_metrics per pipe)
    # choose top k = max(1, int(len(diam_map) * max_changes_frac))
    # for each selected pipe, increase 1 cran only (or decrease if beneficial) and return new map
    return new_diam_map, changes_made
```

## 3.2 Hook GA

- Après évaluation génération : sélectionner topK infeasible (par fitness mais infeasible) et tenter `soft_repair`.
    
- Acceptation : only if violation_total decreases AND new_cost <= current_cost * repair_max_ratio (e.g., 1.05).
    

## 3.3 Logging

- `REPAIR_DIAMETERS_APPLIED` with before/after, delta cost, delta violation.
    

## Tests

- run toy network; assert repairs appliqués rarement et valeurs cohérentes.
    

## Critère d’acceptation

- Pas d’uniformisation globale; réparations limitées et utiles.
    

---


# Phase 4 (réécrite) — Mode Pareto avec **pymoo** (NSGA-II / NSGA-III)

Voici une spécification complète, pratique et prête à implémenter pour ajouter un mode Pareto moderne à votre outil. Elle intègre vos recommandations (pymoo, NSGA-III si >2 objectifs), gère contraintes, pénalités adaptatives, réparation douce et exporte le front Pareto en JSON/CSV/PNG.

---

## Objectifs principaux

- Permettre une optimisation multi-objectif (p.ex. **Coût** vs **Performance hydraulique** ± **Énergie**) via **pymoo**.
    
- Supporter NSGA-II pour 2 objectifs et NSGA-III si >2 objectifs.
    
- Respecter les contraintes via pénalités ou en codant `G` (contraintes) pour pymoo.
    
- Produire `result["pareto"]` utilisable par la UI et l’API (JSON + CSV + PNG).
    
- Être reproductible (seed), sûr (option single-process), et compatible avec le reste du contrôleur.
    

---

## 4.0 Ajouts CLI / config

Ajouter flags/options :

- `--mode pareto` (ou `algo_params={"mode":"pareto"}`)
    
- `--pareto-objectives cost,performance[,energy]` (ordre = minimiser)
    
- `--pareto-algo [nsga2|nsga3]` (auto = nsga2 si objectives<=2, nsga3 sinon)
    
- `--pareto-population`, `--pareto-generations`
    
- `--pareto-refdirs` (facultatif: fichier de directions de référence pour NSGA-III)
    

Le contrôleur transmet `algo_params` au constructeur de l’optimizer.

---

## 4.1 Conception technique (high level)

1. **Problem pymoo** : Implémenter une classe `WaterNetworkProblem(pymoo.core.problem.Problem)` encapsulant :
    
    - Le mapping chromosome → diam_map (et h_tank si nécessaire).
        
    - L’évaluation → appel au simulateur (wrapper EPANET) **par individu** (vecteur X → simulation).
        
    - Calcul des objectifs (CAPEX, performance, énergie) et des violations (g).
        
2. **Algorithme** :
    
    - Si n_obj <= 2 : `from pymoo.algorithms.moo.nsga2 import NSGA2`
        
    - Si n_obj >= 3 : `from pymoo.algorithms.moo.nsga3 import NSGA3`
        
3. **Exécution** via `pymoo.optimize.minimize(problem, algorithm, termination=('n_gen', N))`
    
4. **Post-traitement** : convertir `res.X` / `res.F` en `proposals` LCPI, stocker `pareto` dans `result`. Export CSV/PNG.
    
5. **Contraintes** : préférer `out["G"] = violations_array` pour pymoo si facile ; sinon appliquer pénalité dans une composante d’objectif ou via repair (pymoo supporte `n_constr`).
    

---

## 4.2 Exemple d’implémentation (extrait prêt à coller)

> Ce code illustre l’essentiel. Adaptez les appels simulateur / conversion diamètres selon vos objets internes.

```python
# src/lcpi/aep/optimization/pareto_pymoo.py
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.termination import get_termination
import numpy as np
import time
from typing import List, Dict

class WaterNetworkProblem(Problem):
    def __init__(self, n_var:int, candidate_diams: List[int], simulate_fn, constraints: Dict, objectives: List[str], **kwargs):
        # n_var = nombre de conduites
        # candidate_diams = liste de diamètres possibles (valeurs discrètes)
        # On encode X as indices into candidate_diams
        super().__init__(n_var=n_var, n_obj=len(objectives), n_constr=1, xl=0, xu=len(candidate_diams)-1, type_var=int)
        self.candidate_diams = candidate_diams
        self.simulate_fn = simulate_fn
        self.constraints = constraints
        self.objectives = objectives

    def _evaluate(self, X, out, *args, **kwargs):
        # X: shape (pop_size, n_var) (dtype int)
        pop_size = X.shape[0]
        F = np.full((pop_size, self.n_obj), np.inf, dtype=float)
        G = np.zeros((pop_size, self.n_constr), dtype=float)  # G <= 0 is feasible
        for i in range(pop_size):
            try:
                indices = X[i].astype(int).tolist()
                diam_map = {f"pipe_{j}": int(self.candidate_diams[idx]) for j, idx in enumerate(indices)}
                # simulate_fn must be a sync function returning dict with keys: success, CAPEX, performance, energy, min_pressure_m, max_velocity_m_s
                sim = self.simulate_fn(diam_map)
                if not sim.get("success", False):
                    # heavy penalty: set objectives to large values
                    F[i, :] = 1e12
                    G[i, 0] = 1.0  # constraint violated
                    continue
                # map objectives
                vals = []
                for obj in self.objectives:
                    if obj == "cost":
                        vals.append(float(sim.get("CAPEX", 1e9)))
                    elif obj == "performance":
                        # maximize performance -> minimize negative performance
                        vals.append(-float(sim.get("performance_hydraulique", 0.0)))
                    elif obj == "energy":
                        vals.append(float(sim.get("energie_totale_kwh", 0.0)))
                    else:
                        vals.append(float(sim.get(obj, 0.0)))
                F[i, :] = np.array(vals, dtype=float)
                # constraint: pressure_min
                pmin_req = float(self.constraints.get("pressure_min_m", 10.0))
                pmin_obs = float(sim.get("min_pressure_m", 0.0))
                # G <= 0 is feasible: we put positive when violated
                G[i, 0] = max(0.0, pmin_req - pmin_obs)
            except Exception as e:
                F[i, :] = 1e12
                G[i, 0] = 1.0
        out["F"] = F
        out["G"] = G
```

Exécution (dans votre adapter) :

```python
def run_pareto(opt_cfg):
    # build problem
    problem = WaterNetworkProblem(
        n_var = num_pipes,
        candidate_diams = candidate_list,
        simulate_fn = simulate_individual_synchronous,  # wrapper function
        constraints = constraints,
        objectives = objectives_list
    )
    # choose algorithm
    if len(objectives_list) <= 2 and algo_choice != "nsga3":
        alg = NSGA2(pop_size=pop)
    else:
        # NSGA3 needs reference directions; pymoo provides utilities to build them
        alg = NSGA3(pop_size=pop, ref_dirs=ref_dirs)
    termination = get_termination("n_gen", generations)
    res = minimize(problem, alg, termination, seed=seed, verbose=True)
    # res.X, res.F contain pareto set (or final population). Extract nondominated front:
    # pymoo returns res.F pareto approx for NSGA3/2 when using minimize
    # convert to proposals
    pareto_proposals = []
    for x,f in zip(res.X, res.F):
        diam_map = {f"pipe_{j}": int(candidate_list[int(idx)]) for j, idx in enumerate(x)}
        # compute CAPEX/perf again or store f values
        proposal = {
            "id": f"pareto_{len(pareto_proposals)}",
            "diameters_mm": diam_map,
            "objectives": {o: float(v) for o,v in zip(objectives_list, f.tolist())},
        }
        pareto_proposals.append(proposal)
    return pareto_proposals
```

**Remarques pratiques**

- `simulate_fn` doit **être une fonction module-level** (picklable) si vous activez le parallélisme. Pour éviter les soucis de pickling, exécutez en single process par défaut.
    
- Vous pouvez vectoriser l’évaluation (batch simulate) pour accélérer, mais souvent le simulateur EPANET est synchrone et non-vectorisable.
    

---

## 4.3 Contraintes & réparations avec pymoo

- **Option A : G (constraints)** — comme dans l’extrait, renseigner `out["G"]` avec violation magnitude. pymoo gère correctement la dominance en présence de contraintes.
    
- **Option B : pénalités** — si vous préférez garder vos pénalités adaptatives, calculez une pénalité scalar et **ajoutez** à l’objectif coût `F[:,0] += penalty`. Avantage : plus simple si les violations sont complexes.
    
- **Réparation douce** : avant d’évaluer un individu dans `_evaluate`, vous pouvez appliquer `soft_repair_solution` pour les individus dans la population qui sont "presque faisables" (p.ex. violation petite). Attention : cela modifie la diversité ; limiter aux top candidates.
    

---

## 4.4 Export / post-traitement Pareto

- Produire `result["pareto"]` : liste d’objets avec `id, diameters_mm, objectives (dict), constraints_ok, metrics`.
    
- Export CSV : `pareto.csv` with columns `id, CAPEX, performance, ...`.
    
- Plot : scatter cost vs performance (cost en x, performance en y) ; color = constraint_violation. Sauvegarder `pareto.png`.
    
- Log `metrics["pareto_size"] = len(pareto)`.
    

Extrait plot (matplotlib) :

```python
import matplotlib.pyplot as plt
costs = [p["objectives"]["cost"] for p in pareto]
perfs = [-p["objectives"]["performance"] for p in pareto]  # since we used -perf
plt.scatter(costs, perfs, c='tab:blue')
plt.xlabel("CAPEX (FCFA)")
plt.ylabel("Performance hydraulique")
plt.title("Front Pareto approximatif")
plt.savefig("artifacts/pareto_front.png", dpi=150)
```

---

## 4.5 Performance & budgets de calcul

- Les simulations EPANET sont lourdes : **budgeter** population × générations × temps_sim.
    
- Recommandations :
    
    - Surrogate pour pré-filtrer (déjà présent).
        
    - Mode “pareto quick” : réduire `generations` et `population` pour exploration puis refiner top solutions.
        
    - Timeout global : `meta.duration_seconds` et possibilité d’abandonner early si convergence.
        

---

## 4.6 Tests & Critères d’acceptation

- **Unit tests** :
    
    - `tests/test_pareto_problem.py` : small toy network stub simulate_fn returns deterministic values → ensure `minimize` returns expected front.
        
- **Integration test** :
    
    - Run `network-optimize-unified` with `--mode pareto --pareto-objectives cost,performance --generations 20 --population 40` on a small INP; expect: `result["pareto"]` non empty, `pareto.png` and `pareto.csv` generated.
        
- **Acceptance** :
    
    - `result["pareto"]` contient solutions non-dominées (vérification: no proposal in pareto is dominated by another).
        
    - UI can display pareto size and allow selection of a solution for full simulation.
        

---

## 4.7 Sensibilité : NSGA-II vs NSGA-III

- NSGA-II : **très bien** pour 2 objectifs (cost vs perf).
    
- NSGA-III : préférable si vous optimisez 3+ objectifs (cost, perf, energy). NSGA-III nécessite des **directions de référence** (`ref_dirs`) — pymoo fournit utilitaires (see `get_reference_directions("das-dennis", n_obj, n_points)`).
    
- Par défaut : auto-choose (<=2 → NSGA2, otherwise NSGA3).
    

---

## 4.8 Intégration dans `OptimizationController`

- Dans `_import_optimizer_class`, ajouter une branche `if method == "pareto": return ParetoAdapter`
    
- `ParetoAdapter.optimize` appelle `run_pareto(...)` et adapte la structure de sortie en format LCPI :
    

```python
return {
  "meta": {"method":"pareto","solver":self.solver, "pareto_algo": chosen_algo},
  "proposals": [],  # primary best(s) if you want
  "pareto": pareto_proposals,
  "metrics": {"pareto_size": len(pareto_proposals)}
}
```

- Garantir emission `best_updated` avec `meta.best_cost` choisi parmi pareto (min CAPEX) si besoin.
    

---

## 4.9 Bonnes pratiques opérationnelles

- **Seed** : exposez `--seed` pour reproductibilité (pymoo supports `seed`).
    
- **No-multiprocessing par défaut** pour éviter pickling failures. Documenter comment activer (et rendre simulate_fn picklable).
    
- **Surrogate hybrid** : exécuter NSGA rapide sur surrogate puis raffiner topK sur EPANET full-sim.
    
- **Instrumenter** : logger `PARETO_STEP`, `PARETO_FINAL`, tiempos par génération.
    

---

## 4.10 Plan d’implémentation (tâches)

1. Créer `src/lcpi/aep/optimization/pareto_pymoo.py` avec `WaterNetworkProblem` et helpers.
    
2. Ajouter `ParetoAdapter` dans `controllers._import_optimizer_class`.
    
3. Ajouter CLI flags et mapping dans `cli.py`.
    
4. Post-proc : export CSV/PNG/JSON et remplir `result["pareto"]`.
    
5. Tests unitaires + integration smoke.
    
6. Documenter usage (README/CLI help).
    

---

## Résumé final (ce que vous obtenez)

- Mode Pareto basé sur **pymoo** robuste et configurable.
    
- NSGA-II pour 2 objectifs, NSGA-III pour >=3 (avec reference directions).
    
- Contraintes gérées via `G` ou pénalités adaptatives, réparation douce intégrée.
    
- Sorties standardisées (`result["pareto"]`, CSV, PNG) et UI friendly.
    
- Compatible avec vos mécanismes existants (progress adapter, simulateur EPANET, artefacts).
    

---

Si vous le souhaitez je peux maintenant :

- générer le fichier complet `pareto_pymoo.py` (prêt à coller),
    
- fournir le diff pour `controllers.py` ajoutant `ParetoAdapter`,
    
- ou écrire les tests unitaires `tests/test_pareto.py`.
    

Dites lequel vous voulez en premier et je fournis le code exact.

---

# Phase 5 — Observabilité, progression UI et évènements (fix définitif)

**Objectif :** UI correcte, best_cost centralisé, simulate busy/done compte.

## 5.1 Source de vérité best_cost

En fin `OptimizationController.run_optimization` (après tri, apply_hybrid, repair) :

```python
if result.get("proposals"):
    result["proposals"] = self._sort_proposals_by_quality(result["proposals"])
    best_capex = result["proposals"][0].get("CAPEX")
    result.setdefault("meta", {})["best_cost"] = float(best_capex) if best_capex is not None else None
    # metrics duplicate
    result.setdefault("metrics", {})["best_cost"] = result["meta"]["best_cost"]
    # emit event best_updated if progress_callback available
    if callable(progress_callback):
        progress_callback("best_updated", {"best_cost": result["meta"]["best_cost"]})
```

## 5.2 Adapter d’événements (norme)

- `controllers._make_progress_adapter` doit normaliser tous les events et relayer : `run_start`, `generation_start`, `generation_end`, `individual_start`, `individual_end`, `simulation` (busy/done), `best_updated`, `pareto_updated`.
    

Vérifier : **toujours** attacher au GA `set_on_generation_callback` (ou `_progress_cb`) selon disponibilité. **Ne pas** utiliser deux noms différents.

## 5.3 Population bar robust

- `generation_start` : reset completed=0 desc "Éval 0/N".
    
- `individual_end` : if index missing or 0 → increment at least +1.
    

## 5.4 Simulateur

- EPANET wrapper doit émettre `sim_start` et `sim_done` avec payload incluant `flows_m3_s` et `min_pressure_m`, `max_velocity_m_s`.
    
- The progress adapter increments `sim_busy` on sim_start and increments `sim_done` on sim_done.
    

## Tests

- `tools/simulate_progress_events.py` should reproduce UI changes.
    
- Run small GA with `--verbose` to validate.
    

## Critère d’acceptation

- UI bars progressent (Générations, Population, Simulations).
    
- `meta.best_cost` = Best affiché en UI final.
    

---

# Phase 6 — Diagnostics WNTR + artefacts (CSV/JSON/PNG)

**Objectif :** vérifier conservation des flux et produire artefacts stockés dans dossier run.

## 6.1 Script WNTR check

**Fichier** : `tools/wntr_flow_check.py`

```python
import wntr, json, csv
from pathlib import Path
import matplotlib.pyplot as plt

def run(inp_path, out_dir):
    wn = wntr.network.WaterNetworkModel(str(inp_path))
    sim = wntr.sim.EpanetSimulator(wn).run_sim()
    # collect flows per link per time step
    flows_ts = {}
    for link_name in wn.link_name_list:
        flows_ts[link_name] = sim.link['flowrate'].loc[:, link_name].fillna(0.0).tolist()
    # sum over links each timestep
    times = sim.link['flowrate'].index.tolist()
    sum_flows = [sum(abs(sim.link['flowrate'].loc[t])) for t in times]
    # save CSV/JSON
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    csv_p = Path(out_dir)/"flows_time.csv"
    with open(csv_p,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(["time_s","sum_abs_flow_m3_s"])
        for t,v in zip(times,sum_flows):
            w.writerow([t.total_seconds(), v])
    json_p = Path(out_dir)/"flows_time.json"
    json.dump({"times":[t.isoformat() for t in times],"sum_flows": sum_flows}, open(json_p,'w',encoding='utf-8'), indent=2)
    # plot
    plt.plot([t.total_seconds() for t in times], sum_flows)
    plt.xlabel("time_s")
    plt.ylabel("sum_abs_flow_m3_s")
    plt.title("Sum flows over time")
    plt.savefig(Path(out_dir)/"flows_time.png", dpi=150)
    return {"csv": str(csv_p), "json": str(json_p), "png": str(Path(out_dir)/"flows_time.png")}
```

## 6.2 Intégration controller

- Après `simulate()` call `inspect_simulation_result(sim, artifact_dir)` which writes CSV/JSON/PNG into `artifacts/{run_id}/`.
    
- Add `result["meta"]["artifacts"]["flows"] = {...}`.
    

## 6.3 Consumer d’événements live

- If simulate can emit per-step flows, adapter can relay `simulation_step` events to a `FlowEventConsumer` that updates a matplotlib live plot (or stores arrays for later plotting).
    

## Tests

- `python tools/wntr_flow_check.py --inp examples/... --out-dir artifacts/runX`
    
- Check generated CSV/JSON/PNG.
    

## Critère d’acceptation

- Artefacts présents and referenced in result meta.
    

---

# Phase 7 — Bundling wkhtmltopdf + script `enable-wkhtmltopdf.ps1`

**Objectif :** fournir binaire local et script d’activation.

## 7.1 Structure & binaire

- Placez `wkhtmltopdf.exe` dans `vendor/wkhtmltopdf/bin/`
    

## 7.2 Script PowerShell

**Fichier** : `reporting/enable-wkhtmltopdf.ps1`

```powershell
param([string]$RepoRoot = (Get-Location))
$bin = Join-Path $RepoRoot "vendor\wkhtmltopdf\bin"
if(!(Test-Path $bin)) { Write-Error "bin absent: $bin"; exit 1 }
$env:PATH = "$bin;$env:PATH"
Write-Output "WKHTMLTOPDF ajouté au PATH pour la session Powershell"
Write-Output "To persist, add $bin to your user PATH environment variable"
```

## 7.3 Controller detection

- `NetworkOptimizePDFGenerator` : if wkhtmltopdf not found in PATH, look into `vendor/wkhtmltopdf/bin` and use that.
    

## Tests

- Run PS script then `wkhtmltopdf --version`
    

## Critère d’acceptation

- PDF generation works via vendor binary if WeasyPrint missing.
    

---

# Phase 8 — Flags CLI & defaults (UX)

**Objectif :** exposer et harmoniser flags.

- Defaults:
    
    - `generations=120`, `population=120` (comme demandé)
        
    - `hmax=50` par défaut pour la hauteur sous radier
        
    - `pressure_min=10`, `vitesse_min=0.3`, `vitesse_max=1.5`
        
- Flags:
    
    - `--no-cache`, `--no-surrogate` (déjà présents)
        
    - `--penalty-weight`, `--penalty-beta`, `--repair-topk`, `--mode pareto`
        
    - `--epanet-backend [wntr|dll]`
        
    - `--enable-wkhtmltopdf` (optionnel pour auto-activate vendor)
        

Assurez-vous que CLI passe ces params à `OptimizationController.run_optimization` via `algo_params`.

---

# Phase 9 — Tests, CI, et smoke runs

**Tests unitaires** (pytest) + **smoke runs**:

- `pytest tests/ -q`
    
- `python -m lcpi.aep.cli network-optimize-unified <small_inp> --method genetic --generations 10 --population 20 --no-cache --verbose`
    
- Compare JSON outputs, vérifiez `meta.best_cost`, `meta.solver_calls`, `meta.sim_time_seconds_total`, `meta.artifacts.flows`.
    

---

# Phase 10 — Monitoring, logs & documentations

- Add structured logs `BEST_UPDATE`, `REPAIR_DIAMETERS_APPLIED`, `FLOW_CONSERVATION_BREACH`.
    
- Documentation: `docs/optimizer_guide.md` with flags, default behaviour, and how to interpret artifacts.
    
- Issues/PRs: one issue per task; code commits referencing issue numbers.
    

---

# Timeline de travail (estimation) — pour un dev expérimenté

1. Phase 1 : 1–2 jours
    
2. Phase 2 : 1–2 jours
    
3. Phase 3 : 1 jour
    
4. Phase 5 (UI/events) : 0.5–1 jour
    
5. Phase 6 (WNTR scripts) : 0.5 jour
    
6. Phase 7 (wkhtml bundling + script) : 0.5 jour
    
7. Tests & docs : 1 jour  
    Total raisonnable : **6–8 jours** de travail (dépend de disponibilité PriceDB et tests réseau)
    

---

# Risques & mitigations

- **Multiprocessing / pickling** : désactiver pool ou isoler code picklable. _Mitigation_ : par défaut single-process; ajouter opt-in pour multi-process.
    
- **Temps d’exécution EPANET** : utiliser surrogate pour pré-filtre; limit N sims for validation (top 5).
    
- **Réparation agressive** : log + seuils; variable `repair_max_ratio`.
    
- **PDF backend** : vendor binary plus script pour éviter dépendances lourdes.
    

---

# Livrables concrets que je peux fournir tout de suite (dès que vous me dites lesquels)

- `diameter_manager.py` complet (avec tests)
    
- patch pour remplacer hardcodes dans `controllers.py` et GA
    
- `adaptive_penalty` & `normalize_violations` + tests
    
- `repairs.py` (soft repair) + integration hook
    
- `tools/wntr_flow_check.py`
    
- `reporting/enable-wkhtmltopdf.ps1`
    
- Modifs `progress_ui.py`/`controllers.py` pour best_cost/bars
    
- script `tools/simulate_progress_events.py` de test (si vous voulez)
    

Dites-moi **quel(s) livrable(s)** vous voulez en premier (ex: `diameter_manager` + patch controllers + tests), et je vous fournis les fichiers / diffs prêts à appliquer.