Parfait — voici un **plan d’action détaillé, opérationnel et prêt à implémenter** pour intégrer dans `lcpi-cli` (plugin `aep`) la fonctionnalité d’**optimisation intelligente** de la _hauteur sous radier d’un réservoir surélevé_ (H_tank) + choix de diamètres, choix de méthode (binary / nested / global / surrogate), vérification d’intégrité des entrées `.inp` / `.yml`, optimisation par prix, intégration aux rapports et à la logique existante.

Je donne : architecture logique, emplacement des modules, noms de commandes CLI proposés (avec alternatives si conflits), flux détaillé d’exécution, points d’intégration (solver LCPI / EPANET), tests, CI, et enfin ce que doit contenir au minimum l’`inp` ou le `yaml`.

---

# 1 — Objectifs fonctionnels (rappel rapide)

- L’utilisateur fournit réseau `.inp` (EPANET) **ou** `.yml`.
    
- Il peut fixer H_tank (ou son intervalle), pression minimale, vitesses acceptables, base de diamètres.
    
- L’outil propose : H_tank retenue, pressions à tous les nœuds, vitesses dans chaque tuyau, diamètres choisis, métrés & coût estimé, fichiers de simulation, et rapport.
    
- L’utilisateur choisit la méthode d’optimisation via CLI (`binary`, `nested`, `global`, `surrogate`).
    
- Le CLI vérifie l’intégrité du `.inp` / `.yml` avant toute simulation (checksum/signature).
    
- Résultats signés/journalisés et compatibles avec le moteur `lcpi` ou `epanet`.
    
- Une commande « magique » exécute tout le pipeline automatiquement.
    

---

# 2 — Architecture & organisation du code (emplacement proposé)

```
src/lcpi/plugins/aep/
├─ cli.py                         # déclaration des commandes Typer
├─ optimizer/
│  ├─ __init__.py
│  ├─ controllers.py              # orchestration des méthodes et du pipeline
│  ├─ binary.py                   # implémentation recherche binaire
│  ├─ nested.py                   # nested greedy / heuristique
│  ├─ global_opt.py               # GA / DE / NSGA-II wrapper
│  ├─ surrogate.py                # construction et usage du surrogate model
│  ├─ scoring.py                  # objectifs, pénalités, coût CAPEX/OPEX
│  ├─ io.py                       # lecture YAML/INP -> internal model (Pydantic)
│  ├─ cache.py                    # cache & hashing des simulations
│  └─ validators.py               # checks business rules + integrity checks
├─ solvers/
│  ├─ __init__.py
│  ├─ lcpi_solver.py              # solveur interne pluggable (mock/tests)
│  └─ epanet_solver.py            # wrapper autour d’EPANET (calls epanet or wntr)
├─ data/
│  ├─ diameters.yml               # DB initiale (ou upgrade SQLite)
│  └─ model_store/                # stockage des modèles surrogate
└─ tests/
   ├─ test_binary.py
   ├─ test_nested.py
   └─ test_integration.yml
```

---

# 3 — Noms de commandes proposées (Typer) & usages

> **Important** : au démarrage, vérifier dans `lcpi-core` / `plugins` que ces noms ne sont pas déjà pris — si un nom existe, suffixer par `-aep` (ex: `tank-optimize-aep`).

1. `lcpi aep tank-optimize`
    
    - Usage principal. Arguments / options : `--network`, `--config`, `--method [binary|nested|global|surrogate]`, `--solver [lcpi|epanet]`, `--out`.
        
    - Comportement : lance optimisation selon `method`.
        
    - Exemple :
        
        ```
        lcpi aep tank-optimize --network project/network.inp --config cfg.yml --method nested --solver epanet --out results/opt.json
        ```
        
2. `lcpi aep tank-verify`
    
    - Usage : vérifie intégrité du `.inp` / `.yml` (checksum/signature + schéma), renvoie `ok`/`errors`.
        
    - Exemple : `lcpi aep tank-verify --network project/network.inp`
        
3. `lcpi aep tank-simulate`
    
    - Usage : lance une simulation unique (H_tank donné, diamètres donnés) sans optimiser. Utile pour debug et validation.
        
    - Exemple :
        
        ```
        lcpi aep tank-simulate --network project/network.yml --H 63.2 --diameters diam.yml --solver lcpi --out sim.json
        ```
        
4. `lcpi aep diameters-manage`
    
    - CRUD pour base diamètres (add/list/update) — utile pour la BD AEP.
        
    - Exemple : `lcpi aep diameters-manage add --file new_diam.yml`
        
5. **La commande magique** : `lcpi aep auto-optimize` (alias `tank-auto`)
    
    - Comporte tout : integrity check → prévalidation → optimisation choisie (ou automatique: starter binary then nested) → post-validation → journalisation/signature → génération de résultat adapté au template et push vers `lcpi rapport`.
        
    - Exemple :
        
        ```
        lcpi aep auto-optimize --network network.inp --config cfg.yml --solver epanet --out results/auto_opt.json
        ```
        
6. `lcpi aep price-optimize` (optionnel)
    
    - Optimisation priorisant coût (CAPEX) ; peut être une option `--objective price` dans `tank-optimize`.
        

---

# 4 — Flux d’exécution détaillé d’une commande (pipeline `auto-optimize`)

1. **Entrée & parsing** : `io.py` charge soit `.inp` soit `.yml` et convertit en _internal model_ (Pydantic) : nodes, links, pumps, tanks, demands, elevations.
    
2. **Vérification d’intégrité** (`validators.py`) :
    
    - calcul SHA256 du fichier ; si signature attendue (fichier d’intégrité adjacent ou champ metadata), comparer ; sinon reporter warning.
        
    - validation schéma Pydantic (champs manquants, types, units).
        
3. **Pré-checks métier** : s’assurer que `H_max` permet d’atteindre `pressure_min` (test rapide : simulate H_max once). Sinon : `unfeasible` → message conseillé (augmenter H_max ou revoir contraintes).
    
4. **Choix du solver** : wrapper `solvers/epanet_solver` ou `solvers/lcpi_solver`. Les deux exposent la même API :
    
    ```py
    solve(network_model, H_tank=None, diameters=None, duration_h=24) -> SimulationResult
    ```
    
5. **Algorithme d’optimisation** : route vers binary / nested / global / surrogate. Tous écrivent leurs essais dans `cache` et `logs/` (utiliser `integrity_manager` pour signer logs JSON).
    
6. **Scoring** : `scoring.py` calcule CAPEX (via diameters DB × length), OPEX estimé (énergie), pénalités de violation, score total.
    
7. **Sélection & post-check** : prendre meilleure solution (ou Pareto), exécuter une simulation finale pour valider.
    
8. **Génération de sortie** : JSON résumé (H_tank, diameters, pressures, velocities, costs, violations, sim_files), fichiers de simulation EPANET si demandé.
    
9. **Intégration rapport** : déposer résultat dans emplacement connu pour `lcpi rapport` (ex: `project/logs/optimizations/*.json`) et générer tag/template placeholders utilisables par `Jinja` templates.
    
10. **Journalisation & signature** : signer les logs (avec `integrity_manager`) et stocker index SQLite.
    
11. **Retour** : message CLI avec chemin des fichiers et résumé (rich table).
    

---

# 5 — API & contrats (fonctions clés à implémenter)

- `io.load_network(path: Path) -> NetworkModel` (Pydantic)
    
- `validators.check_integrity(path: Path) -> IntegrityReport` (utiliser le module d’intégrité existant pour logs; pour INP: calcul SHA256 + compare signature store)
    
- `solvers.solve(network: NetworkModel, H_tank: float, diameters: Dict[str,int], solver: str) -> SimulationResult`
    
- `binary.search_H(...) -> OptResult`
    
- `nested.optimize(H_bounds, diameters_db, ...) -> OptResult`
    
- `global_opt.optimize(...) -> OptResult` (support parallel workers)
    
- `surrogate.build_and_optimize(...) -> OptResult`
    
- `scoring.compute_cost(network, diam_choice) -> cost_dict`
    
- `results.save_as_template(result: OptResult, template_name: str) -> ReportPayload` (map result -> placeholders pour `lcpi rapport`)
    

---

# 6 — Intégration avec EPANET & LCPI solver

- `epanet_solver` : wrapper qui prend le `NetworkModel`, écrit / modifie un `.inp` temporaire (positionne niveau du réservoir `H_tank` en `[TANKS]` ou `[RESERVOIRS]`), remplace diamètres, lance EPANET engine (via `wntr.epanet` ou `epanet2` binding) et récupère pressions/flows/time-series.
    
- `lcpi_solver` : API identique pour unité tests / dev sans dépendance EPANET. Utile pour CI et tests rapides (mock).
    
- Exposer option `--solver` pour l’utilisateur. Les résultats doivent être identiques en forme (structure JSON) pour faciliter templates.
    

---

# 7 — Intégration aux rapports & templates

- **Format de sortie** standardisé (`results/opt_YYYYMMDD_HHMM.json`) contenant :
    
    - `meta`: method, solver, timestamp, seed
        
    - `H_tank_m`, `diameters_mm{link_id: d}`, `pressures_m{node: p}`, `velocities_m_s{link: v}`
        
    - `CAPEX`, `OPEX_annual`, `violations`, `sim_file`
        
- `lcpi rapport` doit accepter `--include-optimizations results/*.json` et remplacer placeholders dans `note_calcul_aep` templates :
    
    - tableau diamètres, carte (GeoJSON) pressions, graphiques (pressure vs node), section texte `Méthode utilisée : X`, `Contrainte pression min : Y`.
        
- Ajouter dans `templates/` un template `optimisation_tank.jinja2` que `rapport.generate` peut appeler.
    

---

# 8 — Vérifications & tests (indispensables)

- **Unitaires** :
    
    - parser INP → Pydantic model (cas valide / invalide).
        
    - `validators.check_integrity` (faux fichier signé vs corrompu).
        
    - `binary.search_H` sur réseau analytique (1 tuyau) → converge au résultat attendu.
        
    - `nested` : vérifier diamètres choisis dans DB et contraintes respectées.
        
- **Intégration** :
    
    - pipeline `tank-optimize` sur petit réseau EPANET (3–10 nodes).
        
    - `auto-optimize` end-to-end.
        
- **Performance** :
    
    - nombre de simulations / seconde, caching effectif.
        
- **Regression** : garde historique des runs pour comparaison.
    
- **CI** : GitHub Actions qui : lint, unit tests, integration tests (mock EPANET or wntr), et runner pour un petit example.
    

---

# 9 — Cache, parallélisme et robustesse

- **Cache** : clé = hash(network_model + H_tank + diam_vector + demands) → si exists reuse SimulationResult.
    
- **Parallélisme** : pour `global` et entraînement surrogate, jobs indépendants en `concurrent.futures.ProcessPoolExecutor`.
    
- **Timeouts & retries** : wrapper solveur doit gérer timeout et marquer l’essai comme `failed_sim`.
    
- **Reproducibility** : seed control pour algos stochastiques ; journaliser seed.
    

---

# 10 — Scoring & optimisation par prix (CAPEX-aware)

- **CAPEX** : somme( length_link * cost_per_m(diameter) ). Cost per m depuis `diameters.yml` ou DB.
    
- **OPEX** : estimation énergie = Σ (puissance pompe @Q * heures * tarif_kWh). Simple modèle annualisé.
    
- **Objective examples** :
    
    - minimize `CAPEX + λ * OPEX`
        
    - multi-objective → produire Pareto front (coût vs min_pressure_margin).
        
- **Commandes** : `--objective price` ou `--weights capex:0.7,opex:0.3`.
    

---

# 11 — IA / Surrogate : implémentation, entraînement, usage (niveau opérationnel)

**But** : réduire nombre de sims lourdes en remplaçant temporairement solveur par un modèle rapide.

## a) Données & features

- Entrées (features) :
    
    - `H_tank` (float)
        
    - vecteur diamètres par lien (encode integer or one-hot)
        
    - résumé demande (Q_total, Q_peak)
        
    - caractéristiques réseau simplifiées : link lengths, elevations differences, roughness means, pump head baseline
        
- Sorties (labels) :
    
    - `min_pressure` (m),
        
    - `pressures` (optionnel : on peut prédire résumé ou nodal),
        
    - `max_velocity`,
        
    - `feasible_flag` (bool).
        

## b) Génération dataset (offline)

- Sampling strategy : Latin Hypercube / uniform + include edge cases (H_min, H_max, smallest/largest diameters).
    
- N initial simulations : 200–1000 selon taille réseau (pour petit réseau 200 suffisent).
    
- Stocker chaque sample `X->Y` avec meta (solver used, runtime).
    

## c) Modèles / libs proposées

- **XGBoost** ou `RandomForest` : rapides, robustes, gèrent non-lin.
    
- **Gaussian Process (GP)** : si on veut estimation d’incertitude (coûteux pour large dims).
    
- **Neural Net** : si features large et besoin generaliser nodal pressures (plus complexe).
    

## d) Training pipeline

1. prepare dataset → train/val/test split (80/10/10).
    
2. grid search / CV pour hyperparam.
    
3. metrics : MAE, RMSE for continuous; accuracy/recall for feasibility.
    
4. calibrate uncertainty (if GP).
    
5. save model artifact (versioned) in `data/model_store/` and sign it (integrity).
    

## e) Usage en production

- `surrogate.build_and_optimize` :
    
    1. Si model existant & applicable (same network topology) → use it for fast scoring of many candidates.
        
    2. Else : run small LHS sample to build local surrogate; then optimize on it; finally validate top-K candidates on real solver.
        
- **Active learning** : après optimisation sur surrogate, valider top candidates et ajouter résultats au dataset ; réentraîner itérativement pour améliorer performance.
    

## f) Monitoring & validité

- Surrogate doit être _topology-aware_ — si réseau change structure (nouveaux links), retrain.
    
- Toujours **final-validate** best candidates sur EPANET.
    

---

# 12 — Sécurité, intégrité & audit

- **Integrity check** pour `.inp` / `.yml` : SHA256 and optional signature file `network.inp.sig` (format simple JSON with checksum and signer). `tank-verify` vérifie.
    
- **Signer** tous les logs d’optimisation (utiliser `integrity_manager.sign_log`).
    
- **Model artifacts** (surrogate) signés et versionnés.
    
- **Index des runs** : sqlite index des résultats pour recherche et génération de rapports.
    

---

# 13 — Tests & scénarios recommandés (liste courte)

- **Scénario A** : réseau 1 tuyau analytique → vérifier binary.
    
- **Scénario B** : petit réseau EPANET 5 nodes → nested greedy.
    
- **Scénario C** : budget contraint → objective price.
    
- **Scénario D** : surrogate warmstart → validate top 5.
    

---

# 14 — Roadmap de livraison (sprints)

- **Sprint 1** (1–2 semaines) :
    
    - structure code + CLI commands + IO Pydantic + validators + epanet solver wrapper (mock ok).
        
    - implémentation `binary` + tests unitaires.
        
    - `tank-verify` integrity.
        
- **Sprint 2** (2 semaines) :
    
    - `nested` heuristic + diameters DB + scoring CAPEX.
        
    - `tank-simulate` + result JSON + integration with `lcpi rapport` minimal.
        
- **Sprint 3** (2–3 semaines) :
    
    - `global` GA/DE (parallel), caching, CI integration, more tests.
        
- **Sprint 4** (3–4 semaines) :
    
    - `surrogate` : dataset sampling, model training flow, active learning loop, UI options.
        
    - finalize `auto-optimize` command and full integration with reports.
        

---

# 15 — Ce que le fichier INP (EPANET) ou YAML doit contenir _au minimum_ (obligatoire)

> On sépare INP (EPANET) et YAML (internal schema) — mais ces champs sont nécessaires pour que l’optimisation soit possible.

## Minimum pour `.inp` (EPANET) — éléments EPANET classiques :

- **[JUNCTIONS]** : ID, Elevation (Z), BaseDemand (L/s ou m3/h), Pattern (optionnel)
    
- **[PIPES]** : ID, Node1, Node2, Length (m), Diameter (mm), Roughness/Coeff, MinorLoss (optional)
    
- **[RESERVOIRS] / [TANKS]** : pour le réservoir existant (ou placeholder) → ID, Elevation (radier), InitLevel/MinLevel/MaxLevel etc. (_Si on veut ajuster H_tank on modifiera la section TANK/RESERVOIR level definitions_)
    
- **[PUMPS]** : si pompes présentes : ID, Node1, Node2, Curve ID (ou simple head)
    
- **[CURVES]** : si pompes with curves
    
- **[OPTIONS] / [TIMES]** : simulation duration / time step (optionnel mais utile)
    
- **Commentaires / Metadata** : idéalement un bloc `[LABELS]` ou `COMMENT` pour indiquer unité & coordinate system.
    

## Minimum pour `.yml` (schéma internal) :

```yaml
nodes:
  - id: node_001
    x: 123.45
    y: 67.89
    elevation_m: 45.2
    base_demand_m3_s: 0.01
links:
  - id: pipe_1
    from: node_001
    to: node_002
    length_m: 150.0
    diameter_mm: 110
    roughness: 130
tanks:
  - id: tank_A
    radier_elevation_m: 70.0   # cote radier
    init_level_m: 2.0          # niveau initial au dessus radier
    min_level_m: 0.0
    max_level_m: 5.0
pumps:
  - id: pump_1
    from: node_003
    to: tank_A
    curve_id: curve_1
demands:
  patterns: { optional patterns }
metadata:
  coordinate_system: "EPSG:4326"   # optional
```

---

# 16 — Notes pratiques & conseils d’implémentation

- Toujours **final-validate** les meilleures solutions avec le solver réel EPANET (jamais s’appuyer uniquement sur surrogate).
    
- Stocker la liste des diamètres dans une **DB SQLite** (permet filtres par matériau, coût, stock). YAML ok pour début.
    
- Gérer units de façon explicite (m, mm, m3/s). Utiliser Pydantic avec custom types/validators.
    
- Prévoir un `--dry-run` et `--verbose` pour debug.
    
- Documenter chaque commande dans `docs/` et ajouter exemples templates pour `lcpi rapport`.
    

---

# 17 — Output attendu du pipeline (exemple résumé)

```json
{
  "meta": {"method":"nested","solver":"epanet","timestamp":"2025-08-17T..."},
  "H_tank_m": 63.2,
  "diameters_mm": {"pipe_1":110,...},
  "pressures_m": {"node_001":15.2,...},
  "velocities_m_s": {"pipe_1":1.1,...},
  "CAPEX": 123450.0,
  "OPEX_annual": 3456.0,
  "constraints_ok": true,
  "violations": [],
  "sim_file": "results/opt_sim.inp",
  "report_payload": "templates/optimisation_tank.jinja2 placeholders..."
}
```

---
