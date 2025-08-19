
# 🧠 Mémoire — Projet **LCPI** (version 2.0) — pour Cursor AI

**Dernière mise à jour :** 2025-08-19 (Africa/Lome)

> Utilisation : quand tu aides l’utilisateur, consulte d’abord cette mémoire. Réponds en **français** par défaut, avec un ton professionnel, pratique et orienté ingénierie. Priorise les commandes CLI, la reproductibilité et l’auditabilité.

---

## 1) Qui est l’utilisateur / Contexte (ce que je sais)

* Langue préférée : **français** (réponses en français par défaut).
* Fuseau horaire : **Africa/Lome**.
* Rôle / profil : ingénieur / développeur travaillant sur un outil métier AEP (adduction d’eau potable) — responsable d’implémenter et d’auditer l’optimiseur “tank” dans le projet `lcpi-cli`.
* Priorités : rigueur d’ingénierie, traçabilité, auditabilité, transparence mathematique (logs signés), intégration EPANET, optimisation H_tank + diamètres, optimisation coût (CAPEX + OPEX).
* Préfère : CLI robuste (Typer + Rich), aides complètes, tests automatisés, exports de rapports (Jinja2 → PDF/DOCX), DB SQLite pour prix.
* Préférences d’affichage : éviter caractères Unicode problématiques sur Windows dans les help strings (ex : remplacer `λ` par `lambda`).

---

## 2) Règles & préférences générales (à respecter systématiquement)

* Répondre en **français**.
* Ton : pragmatique, concret, orienté ingénierie — proposer code/pseudocode précis si demandé.
* Toujours favoriser **reproductibilité** (seed, versions, meta dans résultats).
* Toujours proposer **critères d’acceptation** et commandes de test concrets.
* Ne jamais laisser de résultats non signés — intégrer `integrity_manager.sign_log` pour chaque optimisation.
* Pour l’aide CLI, remplacer les caractères Unicode risqués par des équivalents ASCII (ex: `lambda`).
* Lorsque tu fournis des scripts, inclure les commandes pour les lancer, vérifier et rollback (backups).

---

## 3) Conventions de projet (à appliquer dans tout code/documentation)

### Nommage & style

* Python files / modules : `snake_case.py`
* Classes : `PascalCase`
* Config/data files : `snake_case.yml / .csv`
* Templates Jinja2 : `optimisation_tank.jinja2` etc.
* Semantic Versioning : `X.Y.Z` (current: LCPI v2.1.0 in memory)

### Structure repo standard (à céder comme canonical)

```
repo-root/
├── docs/
├── tests/
├── examples/
├── src/lcpi/
│   ├── aep/
│   │   ├── optimizer/
│   │   ├── solvers/
│   │   ├── cli.py
│   │   └── optimizer/cli_commands.py  # Typer app exportée
├── project/
├── output/
└── reports/
```

---

## 4) Ce qui est implémenté / état (résumé rapide)

* **CLI** : `lcpi aep tank {verify, simulate, optimize, auto-optimize, price-optimize, diameters-manage, report}` — **disponible**. `optimizer` exposé via `typer.Typer()` (fix appliqué).
* **Algorithmes** : `binary`, `nested`, `global` (wrapper minimal), `surrogate` (squelette) — **implémentés**.
* **Hardy-Cross** : `_identify_loops_robust()` implémenté (support >24 boucles).
* **Price DB** : base SQLite **aep_prices.db** générée (diameters = 140, accessories = 1260). Exemple path conventionnel : `~/.lcpi/data/aep_prices.db`.
* **Scoring CAPEX** : implémenté, utilise `PriceDB`.
* **OPEX** : implémentation recommandée (`compute_opex`) — **à valider** (dev précédent a planifié, vérifier tests).
* **EPANET wrapper** : `EPANETOptimizer` existant; la gestion des erreurs de solveur a été améliorée; simulation fonctionnelle sous `wntr` (si installé).
* **Cache** : persistant + LRU/TTL — présent.
* **Reporting** : intégration `lcpi rapport` ok ; template `optimisation_tank.jinja2` présent ; HTML report generation ok.
* **Auditabilité** : logs signés via `integrity_manager` (`lcpi.lcpi_logging`) prévu — vérifier signature automatique intégrée dans controller.
* **Tests** : Unitaires passés (16/16), integration & e2e en cours.

---

## 5) Données critiques (à garder accessibles)

### Liste DN supportés (28 DN)

`[20,25,32,40,50,65,75,80,90,110,125,140,160,180,200,225,250,280,315,350,400,450,500,560,630,710,800,900]`

### Table baseline fournie (total fourn.+pose F CFA/ml)

(associée au DN list ci-dessus — utilisée pour construire CSV et DB)

* 20 → 1750
* 25 → 1980
* 32 → 2300
* 40 → 2710
* 50 → 3170
* 65 → 3800
* 75 → 4260
* 80 → 4490
* 90 → 4947
* 110 → 6739
* 125 → 8285
* 140 → 9830
* 160 → 11890
* 180 → 15090
* 200 → 18293
* 225 → 23364
* 250 → 28760
* 280 → 35360
* 315 → 44760
* 350 → 55950
* 400 → 73000
* 450 → 92300
* 500 → 113900
* 560 → 142200
* 630 → 179600
* 710 → 227800
* 800 → 291100
* 900 → 369000



---

## 6) Intégration DB → Optimiseur (règles à appliquer)

* DAO central : `PriceDB` (fichier `src/lcpi/aep/optimizer/db.py`) — doit exposer :

  * `get_price_total(dn, material)`, `get_supply_and_pose(dn, material)`, `get_closest_dn(dn, material)`, `get_accessory_price(code,dn,material)`.
* `CostScorer.compute_capex` doit **utiliser PriceDB** et renvoyer un `CAPEX_breakdown` (link/length/unit_price/cost/source).
* Fallback strategy configurable : `nearest_higher` | `nearest_any` | `error`.
* Le résultat final doit inclure `price_db_info` (path, checksum, version) dans `meta`.

---

## 7) Contrôles d’audit prioritaires (checklist rapide)

* [ ] `lcpi aep tank optimize --method nested` renvoie JSON contenant `proposals.capex_min` et `proposals.compromise`.
* [ ] Chaque run écrit log signé (`integrity.signature`) et `integrity.verify` passe.
* [ ] `PriceDB` répond pour chaque DN listé ; si manquant, `get_closest_dn` trouve un fallback et logge `price_source`.
* [ ] EPANET wrapper : `simulate_with_tank_height` retourne `pressures_m`, `velocities_m_s`, `min_pressure_m`.
* [ ] GA global : checkpointing, parallel workers, `pareto.json` exportable.
* [ ] OPEX : `compute_opex` présent et testé (formula: P = ρ g Q H / η, energy -> annualization -> NPV).
* [ ] CLI help cross-platform : **aucun caractère Unicode problématique** (ex: `λ` remplacé par `lambda`).

---

## 8) Plan d’action / Roadmap (priorités immédiates)

1. **Sprint 1 (4–5j)**

   * EPANET robuste : finalize wrapper, timeouts/retries, tests e2e.
   * OPEX : implement & unit test `compute_opex`.
   * Signatures logs & index runs.
   * Tests e2e simple (project/network example).
2. **Sprint 2 (5j)**

   * GA Global (NSGA-II via `pymoo`) : `H_tank` in chromosome, parallel eval, checkpoints.
   * Pareto export + knee selector + auto proposals.
   * Multi-tanks validation.
3. **V11 → V12** : Surrogate warmstarts, Dask/GPU scaling, SWMM integration (phase 4).

---

## 9) Commandes usuelles & snippets (à coller directement)

* Vérifier CLI help (après fix Unicode) :
  `lcpi aep optimizer --help`
* Run nested (mock solver) :
  `lcpi aep tank optimize project/network.yml --config project/config.yml --method nested --solver mock --price-db ~/.lcpi/data/aep_prices.db --out results/opt.json`
* Run GA short (pareto) :
  `lcpi aep tank optimize project/network.yml --method global --pareto --gens 20 --pop 40 --workers 4 --export results/pareto.json`
* Vérifier signature log :
  ```python
  from pathlib import Path
  from lcpi.lcpi_logging import integrity_manager
  print(integrity_manager.verify_log_integrity(Path('results/opt.json')))
  ```

---

## 10) Bugs connus / Résolutions appliquées

* **Typer app binding** : corrigé — `app = typer.Typer(name="optimizer")` est exporté depuis `src/lcpi/aep/optimizer/cli_commands.py` et ajouté à l'application principale dans `src/lcpi/aep/cli.py` via `app.add_typer(optimizer_cli, name="optimizer")`.
* **Unicode help bug (Windows)** : `λ` → remplacer par `lambda` dans les help strings (script automatisé disponible).
* **EPANET TypeError 'method'** : Recommandation — centraliser la logique de détection du solveur pour éviter les erreurs de type (e.g. `if 'method' in solver` sans test de type).

---

## 11) Comment Cursor AI doit utiliser cette mémoire

* **Priorité** : quand l’utilisateur demande du code/patch/PR, vérifier d’abord ce document pour respecter conventions et chemins.
* **Langue** : français par défaut ; si l’utilisateur écrit en anglais, suivre la langue demandée.
* **Templates** : utiliser les snippets CLI / DAO / JSON meta pour générer réponses/patches conformes.
* **Safety** : ne pas inventer données d’utilisateur (seuls éléments personnels permis sont ceux listés dans la section 1).
* **Actualisation** : préciser la date de last update (2025-08-19) et proposer de rafraîchir la mémoire si de nouvelles décisions/progrès sont faits.

---

## 12) Métadonnées de la mémoire (utiles pour indexing)

* `project_name`: `lcpi`
* `module_focus`: `aep` (optimiseur tank)
* `preferred_language`: `fr`
* `last_update`: `2025-08-19`
* `user_timezone`: `Africa/Lome`
* `user_role`: `ingénieur/développeur`
* `price_db_path_example`: `~/.lcpi/data/aep_prices.db`
* `DN_list_count`: 28

---
