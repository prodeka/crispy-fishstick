
# 0 — Préambule : hypothèses & emplacement du code

J’assume que le projet suit la structure vue précédemment et que les éléments sont sous :

```
repo-root/
  src/lcpi/aep/
    optimizer/
    optimizer/algorithms/
    optimizer/solvers/
    optimizer/scoring.py
    optimizer/db.py
    commands/
  src/lcpi/core/
    solvers.py
  project/
    config.yml
    network.yml (ou .inp)
  ~/.lcpi/data/aep_prices.db  (ou project/data/aep_prices.db)
  project/logs/
  results/
```

Adapte les chemins dans les scripts si nécessaire.

---

# 1 — Checklist de vérification (haute priorité)

Chaque ligne indique : **quoi vérifier**, **comment le vérifier** (commande / test), et **résultat attendu**.

### 1.1 Interface CLI & options

- **But** : les commandes existent et acceptent options (`--method`, `--price-db`, `--solver`, `--pareto`, `--export`, `--select`, `--workers`, `--seed`).
    
- **Test manuel** :
    
    ```bash
    lcpi aep tank optimize --help
    lcpi aep tank optimize project/network.yml --method nested --price-db ~/.lcpi/data/aep_prices.db --solver epanet --pareto --export /tmp/pareto.json
    ```
    
- **Attendu** : l’aide liste les options; la commande retourne code 0 (sans exécuter long run) ou lance optimisation si paramètres complets.
    
- **Automatique (pytest/snippet)** : test de parsing Typer/Click.
    

### 1.2 Présence des algorithmes (binary/nested/global/surrogate)

- **But** : les modules/classes existent et s’importent.
    
- **Test** (Python REPL / pytest) :
    
    ```py
    from lcpi.aep.optimizer.algorithms.binary import BinarySearchOptimizer
    from lcpi.aep.optimizer.algorithms.nested import NestedGreedyOptimizer
    from lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer
    from lcpi.aep.optimizer.algorithms.surrogate import SurrogateOptimizer
    ```
    
- **Attendu** : import sans exception ; classes exposent méthodes `optimize_*`/`build_and_optimize`.
    

### 1.3 EPANET wrapper (epanet_optimizer)

- **But** : wrapper utilise `wntr` (si installé), modifie `.inp`, exécute simulation, extrait pressions & vitesses, supporte timeouts/retries.
    
- **Test** :
    
    ```python
    from lcpi.aep.optimizer.solvers.epanet_optimizer import EPANETOptimizer
    e = EPANETOptimizer()
    res = e.simulate_with_tank_height(network_model, H_tank=63.2, diameters={})
    ```
    
    ou shell :
    
    ```bash
    python - <<'PY'
    from lcpi.aep.optimizer.solvers.epanet_optimizer import EPANETOptimizer
    from pathlib import Path
    e=EPANETOptimizer()
    print(e.simulate_with_tank_height(Path("project/network.inp"),63.2,{}))
    PY
    ```
    
- **Attendu** : `res` contient keys `pressures_m`, `velocities_m_s`, `min_pressure_m`, `max_velocity_m_s`, and `epanet_inp` path. Si `wntr` absent, wrapper doit échouer proprement ou retourner message d’indisponibilité.
    

### 1.4 BinarySearchOptimizer correcte

- **But** : recherche binaire sur H fonctionne et garantit `pressure_min`.
    
- **Test** (pytest snippet) :
    
    ```py
    def test_binary_feasible(mock_network):
        opt = BinarySearchOptimizer(mock_network, PressureConstraints(min_pressure_m=10), solver=MockSolver())
        r = opt.optimize_tank_height(50,80,tolerance=0.1)
        assert r['feasible'] is True
        assert r['min_pressure_m'] >= 10 - 1e-6
    ```
    
- **Attendu** : résultat faisable ou message d’impossibilité clair.
    

### 1.5 NestedGreedyOptimizer (H then diameters)

- **But** : nested exécute binary puis diam selection gloutonne.
    
- **Test** : run small example and check that result contains `H_tank_m` and `diameters_mm` mapping, constraints ok.
    
- **Attendu** : `constraints_ok: True` and `CAPEX` present.
    

### 1.6 Global (GA/NSGA-II) completeness

- **But** : NSGA-II wrapper fonctionne, supporte `H_tank` in chromosome, parallel eval, checkpoints, pareto export.
    
- **Checks**:
    
    - Presence of `run_nsga` or usage of `pymoo`/`deap`.
        
    - Existence of checkpoint file writing (pickle) in temp dir during run.
        
    - `pareto.json` export implemented.
        
- **Test** (small run):
    
    ```bash
    lcpi aep tank optimize project/network.yml --method global --pareto --gens 10 --pop 20 --workers 2 --export /tmp/pareto.json
    ```
    
- **Attendu** : `/tmp/pareto.json` exists and contains list of solutions with `CAPEX` & `OPEX_NPV`.
    

### 1.7 Surrogate pipeline

- **But** : model training + candidate generation + validate top-K.
    
- **Test** : presence of `Latin Hypercube` sampling, `XGBoost`/`RandomForest` training code, `validate_topk` stage.
    
- **Attendu** : training callable and validation step that runs EPANET/Mock solver.
    

### 1.8 Price DB integration

- **But** : `optimizer/db.py` exists; `CostScorer` uses it to compute CAPEX; CLI supports `--price-db`.
    
- **Tests** :
    
    - SQL quick check: list DN present:
        
        ```sql
        SELECT dn_mm, COUNT(*) FROM diameters GROUP BY dn_mm ORDER BY dn_mm;
        ```
        
    - Python:
        
        ```py
        from lcpi.aep.optimizer.db import PriceDB
        db=PriceDB("/home/you/.lcpi/data/aep_prices.db")
        assert db.get_price_total(110,"PVC-U") is not None
        ```
        
    - CAPEX compute:
        
        ```py
        from lcpi.aep.optimizer.scoring import CostScorer
        cs = CostScorer(price_db_path)
        cap = cs.compute_total_cost(network, diam_map, H_tank)
        assert 'CAPEX' in cap
        ```
        
- **Attendu** : CAPEX numeric, `price_source` logged for each link when fallback used.
    

### 1.9 OPEX (energy → NPV)

- **But** : `CostScorer.compute_opex` implemented (ρgQH/η, dt, annualize & NPV).
    
- **Test** : unit test with mock simulation results producing known energy → known NPV.
    
- **Attendu** : computed OPEX within acceptable tolerance.
    

### 1.10 Propositions & Pareto selection

- **But** : optimizer returns `proposals` containing `capex_min` and `compromise` (knee or min-J).
    
- **Test** : inspect results JSON (`results/*.json`) for `proposals` keys.
    
- **Attendu** : both proposals present, and `proposals[*].constraints_ok == True`.
    

### 1.11 Cache & performance

- **But** : cache exists, persistent, keyed by hash(network+H+diam).
    
- **Test** :
    
    - Run same candidate twice and check time difference / log `cache_hit`.
        
    - For tests, examine `~/.lcpi/cache/` or `cache.db`.
        
- **Attendu** : second run uses cache (log shows hit), evaluation time significantly lower.
    

### 1.12 Logs & signature auditabilité

- **But** : `integrity_manager.sign_log` called after each run, logs written, `verify_log` works.
    
- **Test** :
    
    ```bash
    jq . results/opt.json | jq '.integrity'
    python - <<'PY'
    from lcpi.aep.optimizer.integrity import integrity_manager
    print(integrity_manager.verify_log_integrity(Path("results/opt.json")))
    PY
    ```
    
- **Attendu** : `signature_valid: True`, presence of `checksum`, `signed_at`.
    

### 1.13 Reporting integration (`lcpi rapport`)

- **But** : result JSON compatible with `lcpi rapport`, `report_payload` present.
    
- **Test** : run `lcpi rapport generate results/opt.json --template optimisation_tank.jinja2` (or `ReportGenerator.generate_optimization_report(result)`).
    
- **Attendu** : PDF/DOCX generated without errors and contains BOM table.
    

---

# 2 — Scripts automatiques d’audit (prêts à lancer)

Colle ces scripts dans `tools/audit_tank.sh`, `tests/test_audit.py`, et un fichier SQL d’inspection.

---

## 2.1 Script shell complet (tools/audit_tank.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel || echo ".")
PRICE_DB="${HOME}/.lcpi/data/aep_prices.db"
NETWORK="project/network.yml"
CONFIG="project/config.yml"
OUT="/tmp/audit_opt.json"
PARETO="/tmp/audit_pareto.json"
LOGS_DIR="project/logs"
PYTEST="pytest -q"

echo "=== 0. Pré-conditions ==="
command -v python >/dev/null || { echo "python not found"; exit 1; }
python -V

echo "=== 1. Vérifier presence price DB ==="
if [ ! -f "${PRICE_DB}" ]; then
  echo "WARNING: Price DB not found at ${PRICE_DB}"
else
  echo "OK: Price DB found"
  sqlite3 "${PRICE_DB}" "SELECT COUNT(*) FROM diameters;" || echo "ERR reading DB"
fi

echo "=== 2. CLI help check ==="
lcpi aep tank optimize --help || echo "CLI help failed"

echo "=== 3. Small nested run (mock solver) ==="
lcpi aep tank optimize "${NETWORK}" --config "${CONFIG}" --method nested --solver mock --price-db "${PRICE_DB}" --out "${OUT}"
jq -e '.proposals' "${OUT}" >/dev/null && echo "OK: proposals present" || echo "FAIL: proposals missing"

echo "=== 4. Global (short) -> pareto ==="
lcpi aep tank optimize "${NETWORK}" --config "${CONFIG}" --method global --pareto --export "${PARETO}" --gens 10 --pop 20 --workers 2 --solver mock
if [ -f "${PARETO}" ]; then echo "OK pareto exported"; else echo "FAIL pareto"; fi

echo "=== 5. Log signature verify ==="
python - <<'PY'
from pathlib import Path
from lcpi.aep.optimizer.integrity import integrity_manager
p=Path("/tmp/audit_opt.json")
if not p.exists(): 
    print("no result file")
    raise SystemExit(1)
print(integrity_manager.verify_log_integrity(p))
PY

echo "=== 6. Run unit tests subset ==="
${PYTEST} tests/unit/test_db.py::test_get_price_total -q || echo "unit test subset failed"

echo "=== 7. DB content spot-check ==="
sqlite3 "${PRICE_DB}" "SELECT dn_mm, COUNT(*) FROM diameters GROUP BY dn_mm ORDER BY dn_mm LIMIT 10;"
echo "=== Audit finished ==="
```

**Attendu** : sortie imprimée avec OK messages. Ajuste chemins.

---

## 2.2 Pytest quick-suite (`tests/test_audit.py`)

```py
import json
import sqlite3
from pathlib import Path
from lcpi.aep.optimizer.db import PriceDB
from lcpi.aep.optimizer.algorithms.binary import BinarySearchOptimizer
from lcpi.aep.optimizer.solvers.epanet_optimizer import EPANETOptimizer
from lcpi.aep.optimizer.scoring import CostScorer

def test_price_db_reads():
    db = PriceDB(Path.home().joinpath(".lcpi/data/aep_prices.db"))
    assert db.get_price_total(110, "PVC-U") is not None

def test_compute_capex_example(sample_network):
    # sample_network fixture returns minimal NetworkModel and diam_map
    from lcpi.aep.optimizer.db import PriceDB
    db = PriceDB("/home/runner/.lcpi/data/aep_prices.db")
    from lcpi.aep.optimizer.scoring import CostScorer
    cs = CostScorer(db_path=db)
    res = cs.compute_total_cost(sample_network, {'p1':110}, 63.2)
    assert "CAPEX" in res and res["CAPEX"] > 0

def test_epanet_wrapper_runs(sample_inp_path):
    e = EPANETOptimizer()
    out = e.simulate_with_tank_height(sample_inp_path, 63.2, {})
    assert "pressures_m" in out and "min_pressure_m" in out
```

Adapte fixtures `sample_network` et `sample_inp_path` selon ton repo.

---

## 2.3 SQL quick checks

- DN coverage (missing DN):
    

```sql
SELECT d.dn_mm, COUNT(*) FROM diameters d GROUP BY d.dn_mm ORDER BY d.dn_mm;
```

- Materials list:
    

```sql
SELECT DISTINCT material FROM diameters;
```

- Accessory price existence for DN 50:
    

```sql
SELECT accessory_code, material, unit_fcfa FROM accessories WHERE dn_mm=50 LIMIT 20;
```

---

# 3 — Critères d’acceptation détaillés (OK / WARN / FAIL)

Pour chaque fonctionnalité, voici les règles de décision automatiques (use in CI):

- **OK** : test renvoie 0 et vérifie valeurs non-nulles attendues.
    
- **WARN** : DB missing some DN but fallback strategy exists; test must output warnings and not fail pipeline.
    
- **FAIL** : optimisation crash, no proposals returned, signatures missing, or CAPEX/OPEX not numeric.
    

Exemples :

- If `lcpi aep tank optimize` returns JSON but `proposals` missing → **FAIL**.
    
- If `price_db` absent and CLI continues using default YAML fallback and logs a warning → **WARN**.
    

---

# 4 — Rapport d’audit automatique (format)

Le script `tools/audit_tank.sh` produit un mini-rapport `/tmp/audit_report.json` (option) avec fields:

```json
{
  "timestamp": "...",
  "cli_help_ok": true,
  "price_db_present": true,
  "nested_run_ok": true,
  "global_run_pareto_ok": true,
  "signature_valid": true,
  "notes":[...]
}
```

Ce JSON peut être signé par `integrity_manager` et ajouté au dossier `project/logs/audit/`.

---

# 5 — Si un test échoue — plan d’action priorisé

1. **Signature missing** → intégrer `integrity_manager.sign_log` dans `controllers.TankOptimizationController` immediately. High priority.
    
2. **Proposals missing** → inspect `optimizer/controllers` output; ensure `compute_results` returns proposals. Medium priority.
    
3. **Price DB missing entries** → run import script or set fallback strategy to `nearest_higher` and log. Low/Medium.
    
4. **EPANET failures** → confirm `wntr` installed; ensure wrapper writes tmp INP correctly; add more error handling and timeouts. High.
    
5. **GA hangs or slow** → reduce pop/gens for CI; enable surrogate seeding. Medium.
    

---

# 6 — Rapport d’audit manuel (template à remplir)

Après exécution automatique, tu voudras un rapport humain. Utilise ce template :

```
RPT_AUDIT_TANK_V11
Date: <...>
Repo hash: <...>
Summary:
- CLI: OK/WARN/FAIL
- Price DB: OK/WARN/FAIL (missing DN list: ...)
- Binary: OK/WARN/FAIL (details)
- Nested: OK/WARN/FAIL
- Global: OK/WARN/FAIL
- Surrogate: OK/WARN/FAIL
- EPANET wrapper: OK/WARN/FAIL (errors)
- OPEX calculation: OK/WARN/FAIL
- Cache: OK/WARN/FAIL (cache hit rate: ...)
- Logging & signature: OK/WARN/FAIL
Recommendations: ...
```

---
