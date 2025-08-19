## Plan d’implémentation AMELIORATION V15 — 3 sprints

Objectif global: unifier l’optimisation réseau (INP/YML) via une commande unique, normaliser l’API des optimiseurs, exposer les contraintes (pression/vitesse), ajouter un wrapper d’hybridation, garantir la journalisation/signature V11 et des tests e2e.

Durée cible totale: ≈ 3 jours (répartis en 3 sprints courts). Livrables et critères d’acceptation inclus à chaque sprint.

---

### Sprint 1 — Fondation (modèle unifié + API + CLI minimal)

- **Portée**
  - Conversion INP → modèle unifié en mémoire.
  - Interface `BaseOptimizer` + adaptateur `SimpleAdapter`.
  - CLI Typer « network-optimize-unified » (support minimal: méthode `nested`, parse contraintes, IO basique).

- **Tâches**
  - Implémenter `convert_inp_to_unified_model(inp_path: Path) -> Dict` dans `src/lcpi/aep/optimizer/controllers.py` (fallback si `wntr` absent).
  - Créer `src/lcpi/aep/optimizer/base.py` avec `BaseOptimizer` et `SimpleAdapter`.
  - Créer `src/lcpi/aep/commands/network_optimize_unified.py` avec la commande Typer (options: `--method`, `--solver`, `--pression-min`, `--vitesse-min`, `--vitesse-max`, `--output`, `--verbose`).
  - Intégrer la commande dans `src/lcpi/aep/cli.py` via `app.add_typer(...)`.
  - Wiring minimal du contrôleur: chargement input (.inp/.yml), instanciation de l’optimiseur pour `nested`, appel `optimize()`.

- **Livrables**
  - Fichiers: `src/lcpi/aep/commands/network_optimize_unified.py`, `src/lcpi/aep/optimizer/base.py`, `src/lcpi/aep/optimizer/controllers.py` complété.
  - Aide CLI accessible: `python -m lcpi aep network-optimize-unified --help`.

- **Tests / critères d’acceptation**
  - Unit: `test_convert_inp_minimal` (INP minimal → dict avec `meta`).
  - Unit: `test_cmd_help` (la fonction/commande existe et charge).
  - Exécution locale rapide (mock/solver simple): lecture d’un `.inp` et d’un `.yml` retourne un dict `result` contenant `meta.method`, même si `proposals` est vide au début.

---

### Sprint 2 — Routage méthodes + contraintes/pénalités + hybridation (top-k)

- **Portée**
  - Mappage `method -> optimizer` (nested|genetic|surrogate|global|multi-tank) via factory.
  - Gestion des contraintes: `pression-min` (hard), `vitesse-min`/`vitesse-max` (soft par défaut, option hard).
  - Stratégie de pénalisation configurable: `penalty = alpha * max(0, violation)^beta`.
  - Wrapper d’hybridation: raffinement local sur top-K solutions (ex: `genetic + nested`).

- **Tâches**
  - Étendre `_import_optimizer_class` et `get_optimizer_instance` dans `controllers.py`.
  - Propager `constraints` et `algo_params` dans `optimize()` (population, generations, objective, seed).
  - Implémenter `_apply_hybrid_refinement` (tri par CAPEX, remplacement si amélioré) + flags CLI: `--hybrid-refiner`, `--hybrid-topk`, `--hybrid-steps`, `--hybrid-frequency`.
  - Ajouter options par défaut: `--pression-min=10`, `--vitesse-min=0.3`, `--vitesse-max=2.0` (ou lire YAML si présent).

- **Livrables**
  - Routage complet des méthodes dans le contrôleur.
  - Hybridation fonctionnelle post-run, métrique `hybrid_improved_count` dans `result.metrics`.

- **Tests / critères d’acceptation**
  - Unit: `test_optimizer_api_uniform` (instanciation + `optimize(constraints)` pour chaque optimiseur sur un réseau mock).
  - Unit: `test_hybrid_refiner_integration` (raffinement améliore ou égale le coût meilleur).
  - e2e: `network-optimize-unified network.inp --method nested --pression-min 15` → JSON avec `proposals` non vide ou solutions marquées `constraints_ok`.

---

### Sprint 3 — Journalisation/signature V11 + reporting + CI/perf

- **Portée**
  - Journalisation/audit: signature des résultats via `integrity_manager.sign_log(result)`.
  - Adapter la sortie pour compatibilité V11 (`report_payload`, `price_db_info`).
  - CI basique: exécuter tests unitaires et scénarios e2e.
  - Perf & robustesse: cache (hash des runs), gestion timeouts/checkpoints, logging DEBUG.

- **Tâches**
  - Intégrer `integrity_manager` dans `OptimizationController` (champ `result.integrity`).
  - Ajouter `price_db_info` (path + checksum + version) et `meta` enrichi (method, solver, constraints).
  - Mettre en place `results/<runid>.json` et `results/<runid>.log.json` (signés) par défaut.
  - Pipeline CI (`.github/workflows/ci.yml`) exécutant tests et linters.
  - Activer cache persistant des simulations coûteuses, journaliser `cache_hit`/`cache_miss`.

- **Livrables**
  - Résultats signés et stockés, rapport compatible V11.
  - CI qui passe vert sur la matrice minimale (Windows, Python ciblé du projet).

- **Tests / critères d’acceptation**
  - e2e: `simulate-inp` simple réseau → pressions/vitesses OK (smoke test).
  - e2e: `network-optimize-unified net.yml --method genetic --hybrid-refiner nested` → `meta.method` inclut `+nested_local_search` ou équivalent, sortie JSON complète.
  - CI: l’ensemble des tests ajoutés aux Sprints 1–2 passent; artefacts de rapport générés.

---

### Risques & mitigations (transversal)

- **Temps de GA**: defaults conservateurs, `--timeout`, checkpoints, possibilité `--solver mock`.
- **Divergence EPANET/WNTR**: pinner versions; valider via INP exemple en CI.
- **Mismatch contraintes**: defaults documentés + flags `--hard-*`.
- **Mémoire gros réseaux**: conseiller voie surrogate + décomposition (futur).

---

### Checklist de fin

- CLI dispo et documentée; `--help` clair.
- Optimiseurs accessibles via factory; API homogène.
- Hybridation opérante avec métriques d’amélioration.
- Résultats signés, rapport V11, CI verte.


