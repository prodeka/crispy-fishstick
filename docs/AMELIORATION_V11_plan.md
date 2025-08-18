# 🚀 AMÉLIORATION V11 — Optimisation des Réservoirs surélevés (intégration avancée, multi-objets, multi-réservoirs)

---

## 🎯 Vision et objectifs

- **But**: étendre l’Amélioration V10 vers une solution robuste de production, couvrant multi-réservoirs, optimisation multi‑objectifs (CAPEX/OPEX/robustesse), intégrations EPANET/LCPI complètes, pipelines IA (surrogate + active learning), reporting avancé et compatibilité totale avec l’écosystème AEP.
- **Principes**: réutilisation maximale de l’existant, non‑régression, interfaces stables, performances, auditabilité et sécurité.

---

## 🔗 Intégration harmonieuse avec l’existant

- **Réutiliser**: `GeneticOptimizer`, `ConstraintManager`, `SolverFactory`, base AEP (projets/données), système de rapports, validation YAML/INP, logging, intégrité.
- **Isoler les nouveautés** dans `src/lcpi/aep/optimizer/` pour éviter les régressions sur `src/lcpi/aep/optimization/`.
- **Compatibilité**: commandes existantes inchangées; ajout d’un sous‑espace `lcpi aep tank` étendu.

---

## 🏗️ Architecture et organisation du code (V11)

```
src/lcpi/aep/
├─ optimization/                      # ✅ EXISTANT (ne pas modifier)
│  ├─ genetic_algorithm.py
│  ├─ models.py
│  ├─ constraints.py
│  └─ individual.py
├─ optimizer/                         # 🆕 Extension V10 → V11
│  ├─ __init__.py
│  ├─ controllers.py                  # Orchestrateur principal (multi‑réservoirs)
│  ├─ algorithms/
│  │  ├─ __init__.py
│  │  ├─ binary.py                    # Binary H_tank (réutilisé, stabilisé)
│  │  ├─ nested.py                    # Nested greedy (H puis DN)
│  │  ├─ global_opt.py                # Wrapper GA (H + DN)
│  │  ├─ surrogate.py                 # IA (XGBoost/RandomForest)
│  │  └─ multi_tank.py                # 🆕 Optimisation multi‑réservoirs
│  ├─ solvers/
│  │  ├─ __init__.py
│  │  ├─ epanet_optimizer.py          # Wrapper EPANET complet (INP dyn.)
│  │  └─ lcpi_optimizer.py            # Wrapper LCPI (HardyCross, etc.)
│  ├─ scoring.py                      # CAPEX/OPEX/penalités, Pareto
│  ├─ cache.py                        # Cache LRU + persistance (SHA256)
│  ├─ validators.py                   # Intégrité + règles métier
│  ├─ io.py                           # Loader YAML/INP → modèle interne
│  ├─ models.py                       # Modèles Pydantic étendus (V11)
│  └─ db.py                           # 🆕 DAO diamètres (SQLite/YAML)
├─ data/
│  ├─ diameters.yml                   # DB initiale diamètres
│  └─ model_store/                    # Modèles surrogate (persistés)
└─ tests/
   ├─ test_binary.py
   ├─ test_nested.py
   ├─ test_global.py
   ├─ test_surrogate.py
   ├─ test_multi_tank.py              # 🆕 Nouvelles capacités
   └─ test_integration.py             # E2E V11
```

---

## 🧩 Modèles de données (Pydantic, V11)

```python
# src/lcpi/aep/optimizer/models.py
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class PressureConstraints(BaseModel):
    min_pressure_m: float = Field(..., gt=0)
    max_pressure_m: Optional[float] = None

class VelocityConstraints(BaseModel):
    min_m_s: float = 0.6
    max_m_s: float = 2.0

class CostConstraints(BaseModel):
    budget_capex: Optional[float] = None
    lambda_opex: float = 0.0  # pondération J = CAPEX + λ·OPEX

class TankDecision(BaseModel):
    tank_id: str
    height_m: float

class OptimizationObjectives(BaseModel):
    objective: str = Field("multi", description="price|multi|robust")
    export_pareto: bool = True

class OptimizationConfig(BaseModel):
    method: str = Field("nested", description="binary|nested|global|surrogate|multi_tank")
    H_bounds_m: Optional[Tuple[float, float]] = None
    multi_tank: Optional[Dict[str, Tuple[float, float]]] = None  # tank_id -> (Hmin, Hmax)
    tolerance_m: float = 0.1
    max_iterations: int = 100
    parallel_workers: int = 4
    cache_persist_path: Optional[str] = None
    seed: int = 42

class NetworkModel(BaseModel):
    nodes: Dict[str, Dict]
    links: Dict[str, Dict]
    tanks: Dict[str, Dict]
    pumps: Optional[Dict[str, Dict]] = None
```

---

## 🧠 Méthodes d’optimisation (V11)

### 1) Binary (stabilisation)
- Monotonicité vérifiée; bornes dynamiques par simulation rapide de `H_max`.
- Supporte vérifications vitesse et pénalités légères.

### 2) Nested Greedy (amélioré)
- Étape 1: binary sur H.
- Étape 2: tri des conduites par criticité (longueur × sensibilité pression) et sélection DN minimal respectant contraintes; backtracking local si violation.

### 3) Global (Wrapper GA)
- Inclure `H_tank` comme gène; contraintes gérées par pénalités fortes.
- Parallelisation via `ProcessPoolExecutor`; checkpoints périodiques.

### 4) Surrogate (IA)
- Dataset initial par LHS (200–1000); modèles XGBoost/RandomForest.
- Optimisation sur surrogate → validation top‑K sur solveur réel.
- Boucle d’active learning jusqu’à convergence.

### 5) Multi‑réservoirs (Nouveau)
- Décision: vecteur `H = [H_tank_1, …, H_tank_k]` + DN par tronçon.
- Stratégie: nested multi‑d; coordinate descent (itérations par réservoir), puis GA court.
- Validation conjointe sur contraintes réseau complètes.

---

## 🔧 Solveurs et I/O (EPANET/LCPI)

### EPANETOptimizer (complet)
- Modification dynamique des sections `[TANKS]`, `[RESERVOIRS]`, `[PIPES]` sur fichier `.inp` temporaire.
- Exécution EPANET via `wntr.epanet` ou binaire; extraction pressions/vitesses/énergie.
- Gestion timeouts, retries, logs détaillés; artefacts `.inp/.out` archivés.

### LCPIOptimizer
- Adaptation HardyCross/solveurs internes; mêmes métriques retournées.
- Alignement des unités et conventions avec EPANET pour comparabilité.

### Cache (persistant)
- Clé: SHA256(network_hash, H_vector, diam_vector, solver, timestep).
- LRU en mémoire + persistance sur disque (JSON msgpack/parquet léger).

---

## 💰 Scoring et multi‑objectifs

- CAPEX = Σ longueur × coût_mètre(diamètre) (DB diamètres SQLite/YAML).
- OPEX_annual: dérivé de l’énergie de pompage et des pertes de charge.
- Pénalités: violations pression/vitesse/budget; contraintes dures si requis.
- Pareto front: extraction non‑dominés; détection du knee‑point; score `J = CAPEX + λ·OPEX_NPV` optionnel.

```python
# src/lcpi/aep/optimizer/scoring.py
class CostScorer:
    def compute_capex(self, network, diameters_mm) -> float: ...
    def compute_opex_annual(self, network, H_vector) -> float: ...
    def compute_total(self, capex, opex_npv, lambda_):
        return capex + lambda_ * opex_npv

def compute_pareto(points): ...
def knee_point(pareto_points): ...
```

---

## 🗄️ Base de données diamètres (DAO)

```sql
-- Table diameters (SQLite)
CREATE TABLE IF NOT EXISTS diameters (
  id INTEGER PRIMARY KEY,
  d_mm INTEGER NOT NULL,
  material TEXT,
  cost_per_m REAL NOT NULL,
  roughness REAL,
  available BOOLEAN DEFAULT 1,
  stock INTEGER DEFAULT NULL
);
CREATE INDEX IF NOT EXISTS idx_diam_dmm ON diameters(d_mm);
CREATE INDEX IF NOT EXISTS idx_diam_available ON diameters(available);
```

```python
# src/lcpi/aep/optimizer/db.py
def get_candidate_diameters(min_d: int, max_d: int, material: str | None = None) -> list[dict]: ...
```

---

## 🧪 Tests et validation (V11)

- Unitaires: binary convergence, greedy criticité, scoring CAPEX/OPEX, knee‑point, DAO diamètres, cache persisté.
- Intégration: EPANET small/medium networks; multi‑réservoirs 2–3 tanks; GA wrapper.
- Performance: temps moyen/sim, taux cache‑hit, accélération surrogate (≥×3).
- Compatibilité: `network-optimize-unified` inchangé; anciens projets chargés.

---

## 🖥️ CLI et API (V11)

```python
# src/lcpi/aep/commands/main.py
from .tank_optimization import app as tank_optimization_app
app.add_typer(tank_optimization_app, name="tank", help="🏗️ Optimisation des réservoirs surélevés")
```

### Nouvelles commandes

```bash
lcpi aep tank optimize            # optimize (binary|nested|global|surrogate|multi_tank)
lcpi aep tank verify              # intégrité + validation
lcpi aep tank simulate            # simulation unique
lcpi aep tank auto-optimize       # pipeline complet
lcpi aep tank pareto              # export du front Pareto
lcpi aep tank price-optimize      # objectif coût (budget/capex)
lcpi aep tank report              # génère rapport depuis JSON
lcpi aep tank diameters-manage    # gestion DB diamètres
```

### Exemples d’utilisation

```bash
# Multi-objectif avec Pareto export
lcpi aep tank optimize network.inp --method global --objective multi --solver epanet \
  --export results/pareto.json --workers 6 --seed 123

# Multi-réservoirs
lcpi aep tank optimize network.yml --method multi_tank --solver epanet \
  --config config_v11.yml --out results/multitank.json

# Reporting
lcpi aep tank report results/multitank.json --template optimisation_tank.jinja2 --pdf out/report.pdf
```

---

## 📦 Formats de sortie (JSON standardisé V11)

```json
{
  "meta": {
    "method": "global",
    "solver": "epanet",
    "timestamp": "2025-09-01T...",
    "seed": 42,
    "version": "2.2.0"
  },
  "proposals": [
    {
      "id": "capex_min",
      "label": "Budget max",
      "H_tank_m": {"tank_A": 63.2},
      "diameters_mm": {"pipe_1": 110, "pipe_2": 160},
      "costs": {"CAPEX": 123450.0, "OPEX_annual": 3456.0, "total_cost": 126906.0},
      "constraints": {"pressure_min_ok": true, "velocity_limits_ok": true, "violations": []}
    },
    {
      "id": "knee",
      "label": "Robuste / Économe",
      "H_tank_m": {"tank_A": 66.0},
      "diameters_mm": {"pipe_1": 125, "pipe_2": 160},
      "costs": {"CAPEX": 130000.0, "OPEX_annual": 2900.0, "total_cost": 132900.0}
    }
  ],
  "pareto": [{"CAPEX": 1.2e5, "OPEX": 3.4e3}, {"CAPEX": 1.3e5, "OPEX": 2.9e3}],
  "simulation_files": {"epanet_inp": "results/opt_sim.inp", "epanet_out": "results/opt_sim.out"},
  "report_payload": {
    "template": "optimisation_tank.jinja2",
    "placeholders": {"methode_utilisee": "global", "contrainte_pression_min": "10.0 m", "cout_total": "132,900 FCFA"}
  }
}
```

---

## 🔒 Sécurité, intégrité et audit

- Vérifications **SHA256** sur fichiers `.inp/.yml` et artefacts résultats.
- Journalisation structurée; signature optionnelle des résultats.
- Timeouts, retries, fallback solver; gestion d’erreurs explicites.

---

## 📈 Monitoring et performance

- Métriques: temps de simulation, taux de cache hit, convergence (ΔPareto), écart surrogate → solveur réel, taux de faisabilité.
- Optimisations: Dask (optionnel) pour parallélisme avancé; pooling EPANET.

---

## 🔄 Migration et compatibilité

- Commandes historiques inchangées; ajout non‑intrusif des sous‑commandes `tank`.
- Fichiers de projets existants acceptés; YAML enrichi recommandé pour V11.
- Gabarits `rapport` mis à jour mais compatibles (placeholders conservés).

---

## 🧭 Roadmap V11 (Sprints)

### Sprint 1 — Stabilisation V10 → V11 (Semaine 1)
- Durcir `binary`, finaliser `nested` et scoring CAPEX/OPEX.
- EPANETOptimizer complet (INP dyn., extraction fiable); cache LRU mémoire.
- Tests unitaires élargis; E2E simple.

### Sprint 2 — Global + Multi‑réservoirs (Semaines 2–3)
- GA wrapper (H + DN), checkpoints et parallélisation.
- `multi_tank.py` (coordinate descent + GA court); validations croisées.
- DB diamètres (DAO SQLite), gestion CLI diameters‑manage.

### Sprint 3 — Surrogate + Active Learning (Semaines 4–5)
- LHS, entraînement XGBoost/RandomForest, optimisation surrogate.
- Validation top‑K sur EPANET, boucle active learning; cache persistant disque.
- Benchmarks et critères qualité (écart ≤ 5%).

### Sprint 4 — Reporting/QA/Docs (Semaine 6)
- Template `optimisation_tank.jinja2`, commande `report`.
- Tests d’intégration complets, non‑régression, documentation utilisateur + README archi.
- Indicateurs performance publiés (tableau comparatif V10 vs V11).

---

## ✅ Critères d’acceptation V11

- Commandes `lcpi aep tank` opérationnelles: optimize (toutes méthodes), pareto, report, diameters‑manage.
- Multi‑réservoirs supporté et testé (≥2 tanks) avec EPANET.
- Accélération surrogate ≥ ×3 sur cas de référence; écart moyen ≤ 5%.
- Rapport généré à partir du JSON V11; compatibilité confirmée avec V10.
- Suite de tests verte (unitaires, intégration, compatibilité) et logs/audit complets.

---

## 📚 Exemples de configuration V11

```yaml
# project/config_v11.yml
optimization:
  method: "global"
  H_bounds_m: [50.0, 80.0]
  tolerance_m: 0.1
  max_iterations: 80
  parallel_workers: 6
  cache_persist_path: ".cache/opt_v11"
  seed: 123
  multi_tank:
    tank_A: [55.0, 75.0]
    tank_B: [45.0, 70.0]

pressure_constraints:
  min_pressure_m: 12.0

velocity_constraints:
  min_m_s: 0.6
  max_m_s: 2.0

cost_constraints:
  budget_capex: 1500000
  lambda_opex: 0.2

solver:
  type: "epanet"
  duration_h: 24
  time_step_min: 5
```

---

## 📝 Notes de mise en œuvre

- Conserver les interfaces publiques; isoler les changements dans `optimizer/`.
- Toujours valider les meilleures solutions surrogate sur EPANET.
- Activer logs détaillés et sauvegarde des artefacts pour auditabilité.

---

## Vision générale
Objectif: ajouter l’optimisation des réservoirs surélevés en réutilisant l’existant, sans régression, avec une intégration CLI/rapports propre et des algorithmes progressifs (binary → nested → global → surrogate).

### Jalon 1 — Architecture minimale opérationnelle (MVP Binary)
- **Cibles**
  - Structure `optimizer/` ajoutée sans toucher à `optimization/` existant.
  - CLI dédiée `lcpi aep tank` (verify, simulate, optimize, auto-optimize).
  - Implémentation fonctionnelle `BinarySearchOptimizer` avec `MockSolver`.
  - I/O minimal YAML/INP + validateurs d’intégrité.
  - Base diamètres en YAML et format JSON de sortie standardisé.
- **Livrables**
  - Dossiers: `src/lcpi/aep/optimizer/{controllers.py, algorithms/binary.py, validators.py, io.py, scoring.py(stub)}`.
  - CLI: `lcpi aep tank verify|simulate|optimize|auto-optimize`.
  - Fichiers d’exemple: `project/config.yml`, `project/data/diameters.yml`, `project/network.yml`.
  - Tests: unitaires binary (convergence, bornes).
- **Critères d’acceptation**
  - `lcpi aep tank verify` et `optimize --method binary` passent sur réseau de test.
  - Sortie JSON conforme (meta, résultats hydro, placeholders rapport).
  - Aucune régression sur `lcpi aep network-optimize-unified`.
- **Risques/Dépendances**
  - INP non parsé finement (placeholder accepté). Remplacé à Jalon 2 via EPANET wrapper.

### Jalon 2 — Algorithmes étendus + Wrappers solveurs
- **Cibles**
  - `NestedGreedyOptimizer` (H_tank via binary, puis diamètres glouton).
  - `GlobalOptimizer` (wrapper `GeneticOptimizer`) avec gène `H_tank`.
  - Wrappers solveurs: `EPANETOptimizer` (modif .inp, extraction résultats) et `LCPIOptimizer`.
  - Scoring CAPEX/OPEX et cache simple (en mémoire).
- **Livrables**
  - `src/lcpi/aep/optimizer/algorithms/{nested.py, global_opt.py}`.
  - `src/lcpi/aep/optimizer/solvers/{epanet_optimizer.py, lcpi_optimizer.py}`.
  - `src/lcpi/aep/optimizer/scoring.py` (CAPEX, OPEX basique).
  - `src/lcpi/aep/optimizer/cache.py` (LRU simple).
  - Tests: nested (faisabilité/coût), global wrapper (intégration petite instance).
- **Critères d’acceptation**
  - `--method nested` et `--method global` opérationnels avec EPANET.
  - Respect contraintes pression/vitesse; calcul CAPEX cohérent avec DB diamètres.
  - Backward compatibility confirmée (anciens projets/commandes).
- **Risques/Dépendances**
  - Stabilité EPANET/wntr et temps de simulation; prévoir timeouts/logging.

### Jalon 3 — Surrogate/IA + Performance et Fiabilité
- **Cibles**
  - `SurrogateOptimizer` (LHS, XGBoost/RandomForest, optimisation sur modèle, validation top‑K).
  - Cache intelligent (hash paramètres, persistance disque).
  - Parallélisation (ProcessPool) + checkpointing simple.
  - Métriques: temps/simulation, taux de cache-hit, convergence.
- **Livrables**
  - `src/lcpi/aep/optimizer/algorithms/surrogate.py`.
  - Cache persistant dans `optimizer/cache.py` (hash SHA256 de network+H+diam).
  - Benchmarks et tests de performance/qualité (écart surrogate vs solveur réel).
- **Critères d’acceptation**
  - Accélération mesurée vs nested/global (x≥3 sur cas test).
  - Écart max admis sur pressions/couts validés (p.ex. ≤5% sur top‑K).
  - Robustesse: reprise après interruption, logs détaillés, retries.
- **Risques/Dépendances**
  - Qualité des features/dataset; calibrage du n_samples et du top‑K.

### Jalon 4 — Intégration complète CLI/Rapports + QA et Docs
- **Cibles**
  - Intégration aux sous-commandes existantes: `lcpi aep tank` ajouté proprement.
  - Gabarit rapport `optimisation_tank.jinja2` + payload prêt pour `lcpi rapport`.
  - Sécurité/intégrité: SHA256, journalisation, non-régression complète.
  - Documentation et exemples; gestion d’erreurs UX (messages clairs).
- **Livrables**
  - `src/lcpi/aep/commands/main.py` mis à jour (ajout sous‑commande `tank`).
  - Template rapport + exemples d’exports JSON/CSV diamètres.
  - Suite de tests d’intégration E2E, tests de compatibilité.
  - Documentation utilisateur et README d’architecture.
- **Critères d’acceptation**
  - Toutes les commandes `lcpi aep tank` fonctionnent avec EPANET/LCPI.
  - Génération de rapport à partir de la sortie JSON.
  - Tests verts (unitaires, intégration, compatibilité) sur CI locale.
- **Risques/Dépendances**
  - Collisions CLI; veiller au nommage cohérent et à la rétro‑compatibilité.

Notes d’organisation
- Prioriser la réutilisation: `GeneticOptimizer`, `ConstraintManager`, `SolverFactory`, système de rapports et validation existants.
- Garder les interfaces stables; encapsuler nouveautés dans `optimizer/`.
- Mesurer en continu: temps de simulation, taux de cache, respect contraintes, régressions.

Fin du document V11.




