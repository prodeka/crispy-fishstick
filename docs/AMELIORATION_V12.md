
## Action A — EPANET robuste (Sprint 1, 2 jours)

**Objectif :** fiabiliser la lecture/écriture et l’exécution des `.inp` pour les optimisations (modifier TANK/RESERVOIR, PIPES), prendre en charge commentaires, unités, timeouts, erreurs, et garantir résultats exploitables (pressions/vitesses).

### Livrables

- `optimizer/solvers/epanet_optimizer.py` complet et testé (wntr-based).
    
- Helpers: `io/inp_utils.py` pour lecture/écriture robustes.
    
- Tests e2e minimal (.inp → simulate → extract pressures/velocities).
    
- Documentation d’utilisation et exemples.
    

### Tâches (pas à pas)

1. **Choix lib** : utiliser `wntr` (Python, support EPANET format). Installer `pip install wntr`.
    
2. **Écrire wrapper** `EPANETOptimizer` :
    
    - API :
        
        ```py
        class EPANETOptimizer(BaseSolver):
            def simulate(self, network_path: Path, H_tank_map: Dict[node_id,float], diameters_map: Dict[link_id,int], duration_h:int, timestep_min:int, timeout_s:int) -> SimulationResult
        ```
        
    - Comportement :
        
        - Charger `.inp` via `wntr.network.WaterNetworkModel(inp_path)`.
            
        - Appliquer modifications : pour chaque tank/reservoir node, set head or initlevel:
            
            - **If RESERVOIR**: set `model.get_reservoir(node).head = H_tank` (or `elevation`) — wntr uses `base_head`? Use `Reservoir.head` attribute.
                
            - **If TANK**: compute `init_level = H_tank - radier_elevation` and set `tank.init_level = max(min_level, init_level)`. For fixed head behavior prefer RESERVOIR nodes for deterministic head; but keep both supported.
                
        - Replace diameters: `pipe.diameter = d_mm / 1000.0` (m).
            
        - Save temp `.inp` (`tmp_inp = tmpdir / 'tmp_opt.inp'`) with full metadata preserved (`wntr` writes comments? it tries to preserve topology).
            
        - Run simulation using `wntr.sim.EPANETSimulator(model)` with timeout wrapper (subprocess/thread).
            
        - Extract: nodal pressures (use `results.node['pressure']`), link velocities (`results.link['velocity']` or compute from Q & area).
            
        - Return `SimulationResult` with time-series or summary stats (min_pressure, max_velocity) and path to `tmp_inp` and raw output.
            
3. **Timeout & retries** : wrap simulator call with `concurrent.futures.ThreadPoolExecutor().submit(...).result(timeout=timeout_s)`; on TimeoutError retry N times with backoff then mark simulation failed.
    
4. **Validation & sanitation** :
    
    - Validate pump curves exist; if missing return clear error with suggestions.
        
    - Unit conversions: ensure diameters in meters, elevations in meters, flows in m3/s.
        
5. **Edge-cases** :
    
    - If network uses patterns/time series larger than duration, ensure simulation configured to requested duration.
        
    - Multi-tank support: accept `H_tank_map` for multiple nodes.
        
6. **Tests** :
    
    - Unit: modify simple example `.inp` and check that temp INP contains modified diameter and tank head.
        
    - Integration: run simulate on sample .inp and check that pressures and velocities are numeric and reasonable.
        
7. **Docs** : add `docs/epanet_optimizer.md` with examples and troubleshooting.
    

### Extrait pseudocode (wntr)

```py
import wntr
model = wntr.network.WaterNetworkModel(inp_path)
# set diameters
for lid, d_mm in diam_map.items():
    link = model.get_link(lid)
    link.diameter = float(d_mm)/1000.0
# set tank/reservoir heads
for nid, H in H_tank_map.items():
    if nid in model.reservoir_name_list:
        model.get_reservoir(nid).base_head = float(H)
    elif nid in model.tank_name_list:
        tank = model.get_tank(nid)
        tank.init_level = max(tank.min_level, min(tank.max_level, float(H) - tank.elevation))
# write & simulate
tmp_inp = tmpdir/'opt.inp'
model.write_inpfile(str(tmp_inp))
sim = wntr.sim.EPANETSimulator(model)
res = sim.run_sim()
pressures = res.node['pressure'].loc[:, :]  # DataFrame time x node
```

### Tests d’acceptation

- `python -c "from optimizer.solvers.epanet_optimizer import EPANETOptimizer; ..."` runs and returns `min_pressure_m` and `max_velocity_m_s`.
    
- Timeout test: corrupt solver call to ensure graceful failure message.
    

### Durée estimée

~2 jours de dev + 0.5 jour tests.

---

## Action B — GA global complet (Sprint 2, 3 jours)

**Objectif :** implémenter un GA/NSGA-II capable d’optimiser conjointement `H_tank` et vecteur diamètres, parallélisé, checkpointable, et produisant un front de Pareto.

### Livrables

- `optimizer/algorithms/global_opt.py` NSGA-II via **DEAP** (recommandé) or **pymoo**. DEAP is flexible; pymoo has NSGA-II built-in.
    
- Parallel evaluation with `ProcessPoolExecutor`.
    
- Checkpointing (pickle population) & resume CLI flags `--resume`.
    
- Tests unitaires + example run.
    
- Exports pareto JSON.
    

### Tâches (pas à pas)

1. **Choix lib** : utiliser `pymoo` for NSGA-II (multi-objective) or `DEAP` (manual). I recommend **pymoo** for built-in NSGA-II and easy extensions (`pip install pymoo`).
    
2. **Design du chromosome** :
    
    - Represent `H_tank` as continuous gene (bounded H_min,H_max).
        
    - Represent each link diameter as integer index into sorted `D_list` (discrete). For `pymoo` you can use mixed integer representation or encode everything continuous then map to nearest DN index during evaluation.
        
3. **Fitness / Objectives**:
    
    - Obj1 = CAPEX (minimize)
        
    - Obj2 = OPEX_NPV (minimize)
        
    - Use heavy penalty for infeasible (pressure violation) by returning large objective values or adding indicator in selection step. Better: set feasibility indicator and use constrained optimization features (pymoo supports constraints).
        
4. **Population init** : seed population with:
    
    - current network diameters,
        
    - nested greedy result,
        
    - random samples.
        
5. **Parallel Evaluation**:
    
    - Evaluate candidate using `ProcessPoolExecutor.map(evaluate_candidate, population)`.
        
    - `evaluate_candidate` runs: map genes → diam_map & H, build modified INP (via EPANETOptimizer), run simulate, compute CAPEX via DAO, compute OPEX (empty if not implemented yet or estimate), return objectives + feasibility + metrics.
        
6. **Checkpointing**:
    
    - Every N gens save population (pickle) + best archive to disk.
        
    - Add `--resume path/to/chkpt.pkl` CLI option.
        
7. **Pareto export**: after termination export `pareto.json` with list of solutions + metrics.
    
8. **Postprocessing**:
    
    - Knee detection (see section later).
        
    - refine best candidates by local search.
        
9. **Tests**:
    
    - Small network (<10 links) run with `--gens 20` and verify pareto JSON non-empty and feasibility counts.
        

### Pseudocode (pymoo)

```py
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem

class TankProblem(Problem):
    def __init__(self, ...):
        super().__init__(n_var=num_vars, n_obj=2, n_constr=num_constraints, xl=..., xu=...)
    def _evaluate(self, X, out, *args, **kwargs):
        objs = []
        cons = []
        for x in X:
            H, diam_indices = decode_x(x)
            res = evaluate_candidate(H, diam_indices)
            objs.append([res.capex, res.opex])
            cons.append(res.constraint_violations) 
        out["F"] = np.array(objs)
        out["G"] = np.array(cons)
```

### Tests d’acceptation

- `lcpi aep tank optimize net.yml --method global --pareto --workers 4 --gens 40 --pop 80` → `pareto.json` written and includes >1 point, at least one feasible.
    

### Durée estimée

~3 jours dev + 1 jour tests.

---

## Action C — OPEX : calcul énergie & NPV (Sprint 1, 1 jour)

**Objectif :** implémenter `CostScorer.compute_opex` : calcule l’énergie consommée par les pompes depuis les résultats de simulation et retombe en OPEX annualisé et actualisé (NPV).

### Livrables

- `optimizer/scoring.py` method `compute_opex(network, sim_result, horizon_years, discount_rate, energy_price)` implemented.
    
- Tests unitaires with synthetic simulation result.
    

### Algorithme & Formules

- Instantaneous pump power (W): Pt=ρgQtHt/ηP_t = \rho g Q_t H_t / \eta
    
    - ρ = 1000 kg/m³, g = 9.81 m/s², Q_t in m³/s, H_t in m (head), η pump efficiency (use per-pump or default 0.65).
        
- Energy per timestep (Wh): Et(Wh)=Pt(W)∗Δt(s)/3600E_t (Wh) = P_t (W) * \Delta t (s) / 3600
    
- Annual energy E_y = sum over simulation year (if sim shorter, scale up or use multiple-year sim).
    
- OPEX_NPV over horizon T: OPEXNPV=∑y=1TTarifkWh⋅Ey(1+r)yOPEX_{NPV} = \sum_{y=1}^{T} \dfrac{Tarif_{kWh} \cdot E_y}{(1+r)^y}
    

### Implémentation (snippet)

```py
RHO = 1000.0
G = 9.81

def compute_opex(sim_result, horizon_years=10, discount_rate=0.05, price_kwh=0.15, pump_efficiency=0.65):
    # sim_result contains pump_flow[time, pump], pump_head[time, pump], dt (s)
    # compute energy per timestep
    P_t = (RHO * G * Q_t * H_t) / pump_efficiency  # W
    E_kwh = (P_t * dt).sum() / 3600.0
    # assume this E_kwh is annual (if sim is 24h, compute for full year by scaling)
    annual_energy = E_kwh * (365.0 / sim_days)
    # NPV
    opex_npv = sum((price_kwh * annual_energy) / ((1+discount_rate)**y) for y in range(1,horizon_years+1))
    return opex_npv
```

### Tests d’acceptation

- Given a mock sim where pump Q=0.01 m3/s at H=20m for 24h, with η=0.5, price=0.1 XOF/kWh, horizon=1, check computed OPEX matches expected.
    

### Durée

~1 jour dev + tests.

---

## Action D — Auditabilité : logs signés, CI et tests e2e (Sprint 1 S1-S2, 1+1 day)

**Objectif :** rendre toutes les runs auditables (logs signés), ajouter CI (unit + integration) et tests e2e `.inp`.

### Livrables

- Integration of `integrity_manager.sign_log` into optimizer controller.
    
- `results/index.db` (SQLite) that indexes runs: id, timestamp, method, solver, file_path, checksum, signature.
    
- `GitHub Actions` workflow: `python-app.yml` with matrix run and `integration` job (skips EPANET tests if wntr not installed).
    
- Example e2e tests: small .inp test.
    

### Tâches (pas à pas)

1. **Sign logs** : after any optimization run, call:
    
    ```py
    signed = integrity_manager.sign_log(result_dict)
    # store JSON with signed integrity block
    ```
    
    - Ensure key file exists (`~/.lcpi/signing_key`) with `chmod 600`.
        
2. **Index runs** : write into `~/.lcpi/runs/index.db` a row for each run and include path to signed JSON and INP.
    
3. **Signature verification util** : CLI `tank verify-log <log.json>` that validates signature and returns human-readable result.
    
4. **GitHub Actions** :
    
    - `jobs.test` : installs deps, runs `pytest` (unit).
        
    - `jobs.integration` : runs with `wntr` installed when env var `RUN_EPANET=true`, else is skipped or uses mock. Use `matrix` if needed.
        
    - Add caching for pip / venv.
        
5. **e2e tests**:
    
    - Create `tests/e2e/test_inp_pipeline.py` that:
        
        - Copies example INP,
            
        - Runs `lcpi aep tank auto-optimize example.inp --config cfg.yml --solver epanet` (could use mock or wntr),
            
        - Verifies `results/opt.json` exists and signature is valid.
            
6. **CI gating** : require passing integration (or skip marker) before merge to `main`.
    

### GitHub Actions sample snippet

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with: python-version: '3.10'
      - name: Install deps
        run: pip install -r requirements-dev.txt
      - name: Run unit tests
        run: pytest -q tests/unit

  integration:
    runs-on: ubuntu-latest
    if: ${{ github.event.pull_request || github.event_name == 'push' }}
    env:
      RUN_EPANET: ${{ secrets.RUN_EPANET || 'false' }}
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with: python-version: '3.10'
      - name: Install deps (including wntr if requested)
        run: |
          pip install -r requirements-dev.txt
          if [ "${{ env.RUN_EPANET }}" = "true" ] ; then pip install wntr ; fi
      - name: Run integration tests
        run: |
          if [ "${{ env.RUN_EPANET }}" = "true" ] ; then pytest -q tests/integration ; else pytest -q tests/integration -k "not epanet" ; fi
```

### Tests d’acceptation

- After an optimize run, the output JSON (`results/opt.json`) contains `integrity` with `signature` and `checksum` — and `lcpi aep tank verify-log results/opt.json` returns `signature_valid: true`.
    
- CI passes unit tests; integration job runs or skips with clear logs.
    

### Durée

~1 jour for signing & indexing + ~1 day to setup CI & e2e tests.

---

## Priorisation & Planning proposé (récapitulatif)

|Action|Sprint|Estimation|
|---|--:|--:|
|EPANET robuste|S1|2j|
|OPEX (NPV)|S1|1j|
|Logs signés + index + e2e|S1|1-2j|
|GA global (NSGA-II)|S2|3j|
|Auto-proposals + pareto export|S2|1j|
|Multi-réservoirs testing|S2|1j|

(Le total S1 ≈ 4–5 jours ; S2 ≈ 5 jours — aligné avec ton plan.)

---

## Commandes & checks rapides (après implémentation)

- Vérifier EPANET wrapper:
    
    ```bash
    python -c "from optimizer.solvers.epanet_optimizer import EPANETOptimizer; e=EPANETOptimizer(); r=e.simulate(Path('examples/net.inp'), {'TANK1':63.2}, {}, 24,5,timeout_s=60); print(r.min_pressure_m, r.max_velocity_m_s)"
    ```
    
- Lancer GA (petit run):
    
    ```bash
    lcpi aep tank optimize examples/net.yml --method global --pareto --workers 4 --gens 40 --pop 60 --out /tmp/pareto.json
    jq . /tmp/pareto.json | less
    ```
    
- Vérifier signature:
    
    ```bash
    lcpi aep tank verify-log results/opt.json
    ```
    

---

## Risques & mitigations

- **EPANET mismatch** : different versions of EPANET/wntr produce slight differences. Mitigate by pinning wntr version in CI and documenting engine used.
    
- **Long GA time** : mitigate with surrogate + nested seeding + parallel eval + checkpointing.
    
- **Data gaps in DB** : enforce fallback (choose next larger DN) and log warnings.
    

---

Si tu veux, je code immédiatement (ce que tu préfères en premier) :

1. `epanet_optimizer.py` (wntr wrapper) — prêt à brancher sur Binary/Nested.
    
2. `compute_opex` function in `scoring.py` + unit tests.
    
3. `global_opt.py` NSGA-II skeleton using `pymoo` + parallel evaluator + checkpointing.
    
4. CI workflow + `verify_log` CLI tool + run indexing.
    

Dis `1`, `2`, `3`, `4` (ou une combinaison) et je fournis le code/pseudocode/fichiers nécessaires.