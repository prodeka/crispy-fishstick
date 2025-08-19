**Contexte**  
Cet audit couvre l’implémentation de la **V1** (Unification Optimisation Réseau) et la marque en **V16**. Il vérifie que la commande `network-optimize-unified` accepte `.inp` et `.yml`, expose les contraintes hydrodynamiques, supporte le choix de méthode (`genetic|nested|surrogate|global|multi-tank`), et fournit l’hybridation (raffinage local) tout en restant compatible avec le format de sortie V11 et le système de rapports `lcpi report`.

**Date audit** : `2025-08-19` (même date mémoire)  
**Auteur** : Audit automatique / manuel produit pour l’équipe LCPI

---

# 1 — Synthèse rapide (1-ligne)

La V15 est **implémentable et à faible risque** ; la base (conversion INP, API d’optimiseurs et CLI) a été fournie ; l’audit V16 confirme l’intégration de la commande unifiée mais identifie 7 points critiques à corriger/valider avant mise en production.

---

# 2 — Portée de l’audit

Vérifie les éléments suivants end-to-end :

- prise en charge `.inp` → conversion en modèle unifié en mémoire
    
- nouvelles options CLI (`--method`, `--pression-min`, `--vitesse-min/max`, `--hybrid-refiner`)
    
- API commune `BaseOptimizer` et adaptateur `SimpleAdapter`
    
- contrôleur/factory `OptimizationController` + hybrid wrapper
    
- intégration PriceDB & `CostScorer` (CAPEX)
    
- journalisation/signature (auditabilité) compatible V11
    
- compatibilité report (template `optimisation_tank.jinja2`)
    
- tests unitaires & e2e de base
    
- performance / cache / comportement par défaut
    

---

# 3 — Résumé des constatations (haut niveau)

## ✅ Fonctionnalités correctement implémentées / livrables fournis

- Commande Typer `network-optimize-unified` (squelette) — fichier CLI fourni.
    
- Interface `BaseOptimizer` et `SimpleAdapter` — standardisation d’API prête.
    
- `OptimizationController` : INP→modèle (via WNTR si présent), instanciation des optimisateurs, hybrid wrapper minimal — fourni.
    
- Hybrid wrapper : top-K refine flow implémenté côté controller.
    
- Signing : controller appelle `integrity_manager.sign_log` si présent.
    
- Fallbacks : `wntr` absent → conversion minimale (graceful fallback).
    
- `SimpleAdapter` sécurisé pour englober optimiseurs existants.
    

## ⚠️ Points à valider / risques à corriger (priorité)

1. **Contrainte de vitesse** : certaines implémentations d’optimiseurs ne prennent pas `velocity_constraints` — actuellement gérées en post-check (soft). _Priorité élevée_ si cas d’usage demande hard constraints.
    
2. **Penalties & constraint handling** : pas d’implémentation centralisée de pénalité; chaque optimiseur peut appliquer sa propre méthode → risque d’incohérence des résultats. _Priorité élevée_.
    
3. **GA hybrid hook** : le raffinage est fait côté controller (wrapper) — OK, mais idealement il faut un hook dans `GeneticOptimizer` pour éviter perte d’état/population. _Priorité moyenne_.
    
4. **Versioning PriceDB** : vérifier que `price_db_info` (checksum/version) est systématiquement enregistré. _Priorité moyenne_.
    
5. **Tests e2e** : tests d’intégration/CI manquants ou incomplets (EPANET+hybrid+report). _Priorité élevée_.
    
6. **Performance/Cache** : cache global existe mais doit être vérifié pour collisions de hash/network-model. _Priorité moyenne_.
    
7. **Help / Unicode** : remplacer tous les caractères Unicode problématiques (ex: `λ`) dans les help strings. _Priorité faible mais nécessaire pour cross-platform_.
    

---

# 4 — Vérifications détaillées (comment tester / commandes / critères attendus)

> Tous les tests ci-dessous doivent être automatisés dans CI (voir section CI).

## 4.1 Vérification CLI & parsing

### Commandes

```bash
# aide
lcpi aep network-optimize-unified --help

# run minimal nested (mock solver recommended pour CI)
lcpi aep network-optimize-unified examples/simple_net.inp --method nested --solver mock --pression-min 12 --vitesse-max 2.0 --output /tmp/out.json
```

### Critères

- `--help` s’affiche sans erreur (Windows OK — pas de `λ`).
    
- La commande retourne code 0 et écrit `/tmp/out.json`.
    
- `/tmp/out.json` contient `meta.method == "nested"` et clé `proposals` (non vide).
    

## 4.2 INP → modèle unifié

### Test

- Utiliser un INP d’exemple (simple) et appeler `convert_inp_to_unified_model(inp)`.
    

### Attendu

- Résultat dict contient `meta.file`, `nodes` (≥1), `links` (≥1), `tanks` (même vide si absent).
    
- Les liens ont `length_m` et `diameter_m` (ou null si absent).
    
- En absence de WNTR, conversion ne provoque pas d’exception et retourne fallback minimal.
    

## 4.3 Optimizer factory & API uniforme

### Test

- Pour chaque méthode supportée (nested, global, genetic, surrogate, multi-tank) : appeler `get_optimizer_instance(method, model, solver, price_db)` et vérifier que l’objet retourné a `optimize()` fonctionnel (ou adapté par `SimpleAdapter`).
    

### Attendu

- `optimize()` exécute et renvoie dict structure standard avec `meta`, `proposals`.
    
- Si implémentation manquante, `ImportError` clair.
    

## 4.4 Contraintes hydrodynamiques

### Test

- Run nested & genetic with flags `--pression-min 16 --vitesse-max 2.0` and check proposals.
    
- Vérifier in JSON `constraints_ok` pour chaque proposal and list of violations if any.
    

### Attendu

- Solutions qui violent `pression_min` sont marquées `constraints_ok: false` (fail) or filtered by optimizer if implemented hard constraint.
    
- Velocities violations either penalized or marked.
    

## 4.5 Hybridation (genetic + nested)

### Test

- Run genetic with `--hybrid-refiner nested --hybrid-topk 2 --hybrid-steps 1 --generations 40 --population 40`.
    
- Compare best before/after hybrid step (controller metrics).
    

### Attendu

- `result.metrics.hybrid_improved_count >= 0`
    
- If improved, the best CAPEX in proposals is <= pre-refinement CAPEX.
    

## 4.6 PriceDB integration & CAPEX

### Test

- Run with `--price-db ~/.lcpi/data/aep_prices.db` and check `result.costs.CAPEX` and `result.meta.price_db_info`.
    
- SQL spot-check:
    

```sql
SELECT dn_mm, COUNT(*) FROM diameters GROUP BY dn_mm ORDER BY dn_mm;
SELECT COUNT(*) FROM accessories;
```

### Attendu

- CAPEX numeric > 0, `price_db_info.path` present, `price_db_info.checksum` present.
    
- For links where DN exact match missing, `price_source` indicates `fallback`.
    

## 4.7 Signing & auditabilité

### Test

- After run, call `integrity_manager.verify_log_integrity(result_path)` and expect `signature_valid: True`.
    

### Attendu

- Signed log present; verification OK.
    

## 4.8 Report compatibility

### Test

- `lcpi aep optimizer report result.json --template optimisation_tank.jinja2` (or call ReportGenerator).
    

### Attendu

- HTML/PDF generated successfully containing BOM table with unit prices and totals.
    

## 4.9 Performance & cache

### Test

- Run same candidate twice (same network+constraints+diametres) and verify cache hit in log and significantly lower time on second run.
    

### Attendu

- log: `cache_hit: true`, time second run << first run.
    

---

# 5 — Tests automatiques à ajouter (pytest snippets)

Inclure dans `tests/integration/` :

- `test_inp_conversion.py` — verify convert_inp_to_unified_model outputs keys.
    
- `test_optimizer_api.py` — for each method instantiate via factory and call optimize on a toy network (mock solver).
    
- `test_hybrid_refiner.py` — run genetic in mock and assert `hybrid_improved_count` key exists.
    
- `test_price_db_integration.py` — verify CAPEX_breakdown populated and price_db_info present.
    
- `test_signing.py` — run controller and verify integrity signature.
    

---

# 6 — Écarts détectés & recommandations (priorité + actions correctives)

## Écart 1 — Constraint handling centralisé (Criticité : Élevée)

**Issue** : pas de gestion centralisée des pénalités/hard constraints.  
**Action** : implémenter un module `constraints_handler.py` avec :

- fonction `apply_constraints(solution, constraints, mode='soft'|'hard', penalty_weight=...)`
    
- API exposée aux optimiseurs (ou utilisée par wrapper lors du scoring).  
    **Effort** : 0.5 j.
    

## Écart 2 — Hook within GeneticOptimizer (Criticité : Moyenne)

**Issue** : hybrid refinement est extérieur → perte d’état/population.  
**Action** : ajouter hook `on_generation_callback(population, gen)` dans `GeneticOptimizer` pour exécuter raffinage proprement.  
**Effort** : 1 j.

## Écart 3 — Tests CI / e2e (Criticité : Élevée)

**Action** : ajouter pipelines CI qui : run unit tests, run quick e2e with mock solver, run integration with small INP + WNTR (optional, conditional).  
**Effort** : 0.5–1 j.

## Écart 4 — PriceDB versioning & provenance (Criticité : Moyenne)

**Action** : systématiquement include `price_db_info` : path, sha256(file), imported_at, source. Ajouter test qui vérifie presence.  
**Effort** : 0.25 j.

## Écart 5 — Documentation & CLI help (Criticité : Faible)

**Action** : ensure no special Unicode chars in help. Run replacer script. Update README examples.  
**Effort** : 0.1 j.

---

# 7 — Plan d’action recommandé (Sprint / tâches)

## Sprint A (2.5 jours) — Stabilisation & constraints

1. Implémenter `constraints_handler.py` + unit tests — 0.5 j
    
2. Add penalties as default strategy and `--hard-vel` flag — 0.5 j
    
3. PriceDB provenance & tests — 0.25 j
    
4. CI: add pytest job + quick e2e (mock) — 0.75 j
    
5. Replace Unicode in help (apply script) — 0.1 j
    

## Sprint B (2.5 jours) — Hybrid & Optimizer hooks

1. Add `on_generation_callback` hook in `GeneticOptimizer` and modify controller to use it — 1.0 j
    
2. Add targeted tests for hybrid refiner hook (mock) — 0.5 j
    
3. Performance: validate cache correctness & add cache metrics in logs — 0.5 j
    
4. Run full e2e (with WNTR if CI supports) and fix issues — 0.5 j
    

**Total** ≈ **5 jours ouvrés** pour rendre V15 production-ready (V16). Estimation prudente.

---

# 8 — Critères d’acceptation (release V16)

Avant merge en `main` / release V16, confirmer :

-  `lcpi aep network-optimize-unified` prend `.inp` et `.yml` sans erreurs.
    
-  Flags `--pression-min`, `--vitesse-min`, `--vitesse-max`, `--method`, `--hybrid-refiner` fonctionnels et documentés.
    
-  `constraints_handler` existe et est utilisé par au moins `nested` et `genetic` (soft by default).
    
-  `GeneticOptimizer` supporte `on_generation_callback` et hybrid wrapper améliore solutions (testé).
    
-  PriceDB provenance (path + checksum) inclus dans result.meta.
    
-  Logs signés et `integrity.verify_log_integrity` retourne `signature_valid: True`.
    
-  Tests CI (unit + quick e2e) passent sur PR.
    
-  Report template `optimisation_tank.jinja2` accepte la JSON V16 et génère HTML/PDF.
    

---

# 9 — Artefacts d’audit fournis

- Checklist exécutable (shell snippets) — voir section 4.
    
- Pytest snippets (section 5) à committer.
    
- Scripts de remplacement Unicode (si besoin).
    
- Recommandations de configuration CI (jobs unit, e2e-mock, e2e-wntr conditional).
    

---

# 10 — Conclusion & recommandation finale

La V15 est bien conçue — l’API, le controller et le wrapper hybrid sont en place. Pour livrer V16 (production), il faut prioriser **gestion centralisée des contraintes / pénalités**, **tests CI e2e**, et **un petit refactor pour hook dans GeneticOptimizer** afin d’exécuter le raffinage de façon non intrusive et reproductible. Avec les actions listées ci-dessus (≈5 j), l’équipe pourra livrer V16 robuste, auditée et intégrée au workflow `lcpi report`.


