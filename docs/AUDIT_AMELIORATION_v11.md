# CAHIER DES CHARGES — Audit de l'optimiseur « tank » (résumé exécutif)

**Objet :** Vérifier que la fonctionnalité d’optimisation de la hauteur sous radier et des diamètres est conforme aux exigences métier, robuste, réutilisable et intégrée à `lcpi` (plugin `aep`).  
**Livrables attendus :** spécification validée, tests unitaires & d’intégration, script d’import prix, rapport d’audit signé.

---

## 1. Objectifs fonctionnels (exigences)

1. **Entrées acceptées**
    
    - `.inp` EPANET ou `.yml` réseau (format Pydantic attendu).
        
    - `config.yml` avec paramètres optimisation (méthode, H_bounds / H_fixed, limites vitesse, pressure_min, diameter_db, λ, budget, solver).
        
    - Base de prix `aep_prices.db` (SQLite) ou `diameters.yml`.
        
2. **Fonctionnalités**
    
    - `tank verify` : vérification intégrité fichier + validation schéma.
        
    - `tank simulate` : simulation unique pour H donné (via solver choisi).
        
    - `tank optimize` : optimisation avec méthodes `binary|nested|global|surrogate`.
        
    - `tank auto-optimize` : pipeline complet (verify → optimize → save → report payload).
        
    - CAPEX calculé depuis DB diamètres ; OPEX calculé depuis solveur (énergie).
        
    - Produire deux propositions : `capex_min` et `compromise` (knee / J-min).
        
    - Journalisation auditable (logs signés) et cache des simulations.
        
3. **Contraintes**
    
    - Respect pressure_min et velocity bounds sur toutes les solutions acceptées.
        
    - Les diamètres choisis doivent provenir de la DB (ou arrondis au DN supérieur si nécessaire).
        
    - Les résultats finaux doivent être validés par une simulation EPANET (si solver epanet sélectionné).
        

---

## 2. Exigences non-fonctionnelles (NFR)

- **Robustesse** : gestion des erreurs, timeouts, retries, fallback solver.
    
- **Reproductibilité** : seed contrôlable pour algos stochastiques; logs signés.
    
- **Performance** : cache des simulations sur disque; parallélisme configurable (`--workers`).
    
- **Sécurité** : vérification SHA256 des fichiers d’entrée; permissions fichiers sensibles.
    
- **Extensibilité** : architecture plugin / algorithmes extensible (ajouter nouveaux solveurs/optimiseurs).
    
- **Interopérabilité** : format de sortie JSON compatible `lcpi rapport` avec `report_payload`.
    

---

## 3. Interface(s) attendues (CLI / Files)

- CLI :
    
    - `lcpi aep tank verify <network>`
        
    - `lcpi aep tank simulate <network> --H <float> [--diameters ...]`
        
    - `lcpi aep tank optimize <network> --config <config.yml> [--method nested] [--solver epanet]`
        
    - `lcpi aep tank auto-optimize <network> --config <config.yml>`
        
- Files : `config.yml`, `data/diameters.yml` or `~/.lcpi/data/aep_prices.db`.
    
- Outputs : `results/tank_opt.json`, `results/pareto.json`, `results/opt_sim.inp/out`.
    

---

## 4. Critères d’acceptation / Tests d’acceptation (recette)

Pour être validé, chaque exigence ci-dessous doit retourner **OK** :

### Fonctionnels

1. **Verify** : `lcpi aep tank verify example/network.yml` → status OK, affiche checksum.
    
2. **Simulate** : `lcpi aep tank simulate example/network.yml --H 65` → retourne `min_pressure_m`, `max_velocity_m_s`, pressures list.
    
    - Acceptance : `min_pressure_m` numérique, `pressures_m` contiennent tous les nœuds.
        
3. **Optimize (nested)** : `lcpi aep tank optimize net.yml --config cfg.yml --method nested --solver mock` → `results/tank_opt.json`
    
    - Acceptance : JSON contient `proposals.capex_min` et `proposals.compromise` ou équivalent.
        
    - Chaque proposition : `H_tank_m`, `diameters_mm`, `pressures_m`, `velocities_m_s`, `CAPEX`, `OPEX_NPV`, `constraints_ok: true`.
        
4. **Optimize (global)** : `--method global --pareto --export results/pareto.json` → `pareto.json` non vide, front non-dominé.
    
5. **Auto-optimize** : pipeline complet → génère JSON + inscrit log signé.
    
    - Acceptance : vérifier signature présente dans le JSON log `integrity.signature` et que la signature est vérifiable.
        

### Non-fonctionnels

6. **Cache hit** : rerun optimize with same inputs → runtime réduit, cache hit logged.
    
7. **Timeout** : force a long sim (mock can simulate) → solver times out and fallback used or error gracefully reported.
    
8. **Parallel** : `--workers 4` with global → evaluations ran en parallèle (vérifier temps).
    
9. **Reproducibility** : run GA with `--seed 42` twice → identical best solution metrics (or within allowed nondeterminism threshold).
    

---

## 5. Checklist technique (code review)

Passe sur chaque point et coche OK / NOK :

### Qualité & architecture

-  Modules addés dans `src/lcpi/aep/optimizer` respectent architecture plugin.
    
-  Interfaces solvers (`simulate(network, H, diameters)`) identiques pour EPANET et LCPI.
    
-  `Binary`, `Nested`, `Global`, `Surrogate` implémentés sous `algorithms/` et testés.
    
-  `controllers.py` n’absorbe pas logique métier (sépare orchestration & algos).
    
-  DB access via DAO (`optimizer/db.py`) ; pas de SQL inline dispersé.
    

### Tests & CI

-  Tests unitaires pour scoring, DB lookup, greedy routine et knee selector.
    
-  Tests d’intégration exécutant pipeline sur 2 réseaux exemples.
    
-  GitHub Actions: lint, unit tests, integration tests (mock solver).
    

### Observabilité

-  Logs structurés (JSON) avec meta (method, solver, seed, runtime).
    
-  Chaque run écrit un log dans `project/logs/optimizations/` et est signé.
    
-  Index SQLite des runs disponible.
    

### Sécurité / Data

-  Permissions fichier clé/signing (600).
    
-  Vérification SHA256 pour INP/YML importés.
    
-  Inputs invalides rejettés (clear error messages).
    

### Performance

-  Cache key est SHA256(network_hash + H + diam_vector + demands).
    
-  Parallélisme avec ProcessPoolExecutor correctement géré (safe pickling).
    
-  Long-running jobs support checkpoint/resume.
    

---

## 6. Tests unitaires & assertions (exemples pytest)

1. **Test CAPEX calc**
    

```py
def test_compute_capex(tmp_db, small_network):
    db = PriceDB(tmp_db)
    capex, details = compute_capex(small_network, {'p1':110}, db)
    assert capex == pytest.approx(1100.0)  # valeur attendue selon fixture
```

2. **Test binary convergence**
    

```py
def test_binary_converges(mock_network):
    opt = BinarySearchOptimizer(mock_network, PressureConstraints(min_pressure_m=10), solver=MockSolver())
    res = opt.optimize_tank_height(50, 80, tolerance=0.1, max_iter=50)
    assert res['feasible'] is True
    assert res['min_pressure_m'] >= 10 - 1e-6
```

3. **Test DB lookup fallback**
    

```py
def test_get_cost_per_m_fallback(tmp_db):
    db = PriceDB(tmp_db)
    assert db.get_cost_per_m(999) is None or isinstance(db.get_cost_per_m(999), float)
```

---

## 7. Tests d’intégration à exécuter (commande)

- Préparer `project/network_example1.yml`, `config_nested.yml`, `data/aep_prices.db`.
    
- Lancer :
    

```bash
lcpi aep tank verify project/network_example1.yml
lcpi aep tank simulate project/network_example1.yml --H 65
lcpi aep tank optimize project/network_example1.yml --config project/config_nested.yml --method nested --solver epanet --out results/test_nested.json
lcpi aep tank optimize project/network_example1.yml --config project/config_global.yml --method global --pareto --export results/pareto.json --solver epanet
lcpi aep tank auto-optimize project/network_example1.yml --config project/config_nested.yml --out results/test_auto.json
```

- Vérifier `results/*.json` et `project/logs/` (signatures et contenu).
    

---

## 8. Prompts & commandes pratiques (à exécuter / à copier-coller)

### A. Commandes de vérification rapide

```bash
# Vérifier intégrité du network
lcpi aep tank verify project/network.yml

# Simulation unique (contrôle rapide)
lcpi aep tank simulate project/network.yml --H 65

# Optimisation nested rapide (mock solver si EPANET pas installé)
lcpi aep tank optimize project/network.yml --config project/config.yml --method nested --solver mock --out results/nested.json

# Pipeline complet avec EPANET (si installé)
lcpi aep tank auto-optimize project/network.inp --config project/config.yml --solver epanet --out results/auto.json
```

### B. Prompts pour l’IA / Relecteur

Utilise ces prompts pour demander un audit automatisé / relecture à moi ou à un reviewer :

1. _“Check the code in `src/lcpi/aep/optimizer/algorithms/nested.py` for separation of concerns, list functions that need unit tests and propose tests.”_
    
2. _“Analyse `results/test_auto.json` and report any constraint violations, explain why they occur and propose fixes.”_
    
3. _“Generate pytest cases for binary search edge cases (H_unfeasible, monotonicity fail).”_
    

### C. Prompt d’automatisation QA (script)

Crée un script `qa_run.sh` :

```bash
#!/usr/bin/env bash
set -e
python -m lcpi aep tank verify project/network.yml
python -m lcpi aep tank simulate project/network.yml --H 65 > /tmp/sim.json
python -m lcpi aep tank optimize project/network.yml --config project/config.yml --method nested --solver mock --out /tmp/opt.json
python -m lcpi aep tank auto-optimize project/network.yml --config project/config.yml --out /tmp/auto.json
python - <<'PY'
import json
for f in ['/tmp/sim.json','/tmp/opt.json','/tmp/auto.json']:
    j=json.load(open(f))
    print(f, 'keys=', j.keys())
PY
```

---

## 9. Points d’attention critique — à valider impérativement

-  **Final validation EPANET** : aucune solution finale ne doit être livrée sans validation EPANET (si EPANET est la source de vérité).
    
-  **Diamètres DB coverage** : vérifier que pour chaque lien proposé un DN correspondant existe ou qu’un mécanisme d’arrondi (au DN supérieur) est appliqué et loggé.
    
-  **Signature des logs** : signer chaque sortie d’optimisation et conserver clé privée/fichiers en sécurité.
    
-  **Edge cases** : réseaux sans tank, pompes manquantes, courbes pompe non définies → erreurs gérées et messages clairs.
    
-  **Reproductibilité** : seed, versions des modèles/simulateurs inscrits dans `meta`.
    

---

## 10. Exemples de messages d’erreur attendus (et comment corriger)

- `UNFEASIBLE: No height in bounds satisfies pressure_min` → augmenter H_max ou réduire pressure_min / revoir diamètres.
    
- `DIAM_NOT_FOUND: d=37mm` → vérifier DB diameters ; proposer arrondi à 40/50 etc.
    
- `EPANET_ERROR: unable to run simulation` → vérifier installation wntr/epanet binding & .inp modifications.
    

---

## 11. Livrables attendus après audit (checklist final)

-  `QA_CHECKLIST.md` (ce document) placé au repo root.
    
-  Tests unitaires et integration tests (passing).
    
-  Scripts d’import du bordereau + DB `aep_prices.db` validé (ex: 10 lignes test).
    
-  Exemple de run `results/tank_opt.json` pour un réseau test validé.
    
-  Rapport d’audit signé (log signé) avec recommandations restantes.
    

