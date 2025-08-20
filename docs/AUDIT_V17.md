
1. **Pourquoi ça peut paraître si rapide (causes possibles)**
2. **Check-list et tests concrets pour diagnostiquer** (commande + scripts prêts à lancer)
3. **Instrumentation / correctifs à ajouter** (où logger, quoi mesurer)
4. **Signes d’implémentation erronée et remèdes**

---

## 1) Pourquoi la commande peut être très rapide (explications plausibles)

* **Résultats mis en cache** — l’optimiseur retrouve une exécution antérieure identique (même réseau, mêmes contraintes, même DB de prix) et renvoie le résultat du cache sans refaire les simulations.
* **Surrogate / modèle de substitution** — l’optimisation tourne sur un modèle ML (XGBoost/RF) rapide et **ne valide** que peu ou pas de candidats sur EPANET réel.
* **Mock / stub en CI / dev** — la pipeline utilise un *mock solver* (ou une option `--solver mock`) pour tests qui renvoie des résultats factices instantanément.
* **Optimisation incomplète** — l’algorithme fait un *early-exit* (p.ex. trouve une solution triviale qui satisfait les contraintes) ou retourne la première solution viable sans itérer.
* **Évaluations légères** — l’optimiseur n’évalue pas la fitness via un solveur hydraulique complet (il utilise des heuristiques analytiques rapides).
* **Parallélisme + RAM cache** — beaucoup d’évaluations en parallèle et cache mémoire font paraître tout court, mais réalistiquement les simulations lourdes prennent plus de temps global.
* **Erreur logique** — bug : le code ne lance tout simplement pas le solveur (oubli d’appel, `return` prématuré, exception swallowée).
* **Génération de rapport asynchrone** — la commande peut lancer un job en arrière-plan et retourner immédiatement (mais tu as dit que tu n'as pas d'asynchronicité — à vérifier).

---

## 2) Comment vérifier — checklist pratique + commandes/scripts

### A — Tests rapides en ligne de commande

1. **Forcer solveur EPANET + verbose**

```bash
# hypothèse : options existantes
lcpi aep network-optimize-unified mon_reseau.inp --solver epanet --method genetic --generations 80 --population 100 --hybrid-refiner nested --verbose --output /tmp/out.json
time lcpi aep network-optimize-unified mon_reseau.inp --solver epanet --method genetic --generations 80 --population 100 --hybrid-refiner nested --verbose --output /tmp/out.json
```

* `time` (Linux/macOS) indique durée réelle. Sur Windows, utilise PowerShell `Measure-Command`.

2. **Comparer avec un run forcé « long »**

   * augmente `--generations` à 200, `--population` à 200. Si le runtime reste \~1–5s, c’est suspect.

3. **Désactiver cache / surrogate (si flags)**

```bash
# si l'option existe ; sinon ajouter une option --no-cache/--no-surrogate pour tester
lcpi aep network-optimize-unified mon_reseau.inp --solver epanet --method genetic --no-cache --no-surrogate --verbose --output /tmp/out.json
```

Si la commande devient longuement exécutée, tu as trouvé la cause.

4. **Vérifier les métadonnées du JSON de sortie**

```bash
jq .meta /tmp/out.json
```

Cherche : `meta.cache_hit`, `meta.surrogate_used`, `meta.eval_count`, `meta.duration_seconds`, `meta.method`, `meta.price_db_info`. S’il n’y a pas d’indicateurs d’exécution (compteurs, durée), ajoute-les (cf. instrumentation).

---

### B — Vérifier que EPANET est réellement appelé

1. **Rechercher appels système (Linux)** : si LCPI lance `epanet2` binaire, utilise `ps` / `pgrep` ou `strace`. Exemple rapide (pendant l’exécution) :

```bash
# lancer dans une console :
time lcpi aep network-optimize-unified mon_reseau.inp --solver epanet ...
# dans une autre console, pendant l'exécution :
pgrep -a epanet || pgrep -a python    # chercher processus epanet ou wntr
```

2. **Sur Windows** : ouvrir le gestionnaire de tâches pendant l’exécution, chercher `epanet2.exe` ou `python` occupant CPU.

3. **Vérifier génération de fichiers .out ou logs EPANET** — le wrapper EPANET doit créer `.out` ou `results/opt_sim.out`. Si inexistants, le solveur n'a pas tourné réellement.

---

### C — Test de comparaison EPANET vs LCPI (script Python)

Ce script exécute un solveur EPANET via `wntr` (si installé) et compare les pressions nodales au meilleur résultat LCPI. Il te permet de vérifier si les pressions proviennent bien d’une simulation EPANET réelle.

```python
# test_epanet_vs_lcpi.py
import json, subprocess, time, sys
from pathlib import Path

OUT_JSON = Path("/tmp/out.json")  # sortie lcpi
INP = Path("mon_reseau.inp")
WNTR_AVAILABLE = True
try:
    import wntr
except Exception:
    WNTR_AVAILABLE = False

def run_lcpi():
    cmd = [
        "lcpi","aep","network-optimize-unified",
        str(INP),
        "--solver","epanet",
        "--method","nested",
        "--verbose",
        "--output", str(OUT_JSON)
    ]
    start = time.time()
    rc = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start
    return rc.returncode, duration, rc.stdout + "\n" + rc.stderr

def run_epanet_in_wntr(inp_path):
    if not WNTR_AVAILABLE:
        raise RuntimeError("wntr not installed")
    wn = wntr.network.WaterNetworkModel(inp_path)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    # pressures at final timestep
    press = results.node['pressure'].iloc[-1].to_dict()
    return press

if __name__ == "__main__":
    rc, dur, output = run_lcpi()
    print("LCPI rc, duration:", rc, dur)
    print(output[:2000])
    if not OUT_JSON.exists():
        print("ERROR: LCPI did not produce output JSON at", OUT_JSON)
        sys.exit(2)
    data = json.loads(OUT_JSON.read_text())
    print("LCPI meta:", data.get("meta", {}))

    # if LCPI contains 'solver_data' best proposal with pressures:
    solver_data = data.get("solver_data", {})
    for s, d in (solver_data.items() if solver_data else []):
        props = d.get("proposals") or []
        if props:
            best = props[0]
            if best.get("pressures_m"):
                print("LCPI provides pressures for", s, "sample node:", list(best["pressures_m"].items())[:3])
            else:
                print("LCPI best proposal has no 'pressures_m' field")

    # run EPANET direct if possible and compare pressures for a few nodes
    if WNTR_AVAILABLE:
        print("Running EPANET via WNTR for comparison (this may take seconds)...")
        t0 = time.time()
        pressures = run_epanet_in_wntr(str(INP))
        print("EPANET run time:", time.time() - t0)
        sample = dict(list(pressures.items())[:5])
        print("Sample EPANET pressures:", sample)
    else:
        print("WNTR not available; install 'wntr' to perform verification.")
```

* Exécute : `python test_epanet_vs_lcpi.py`.
* Si LCPI est ultra-rapide mais EPANET prend 3–5s avec WNTR, il y a une différence : LCPI n’a peut-être pas appelé EPANET.

---

## 3) Instrumentation à ajouter (log, compteur, timings) — *fortement recommandé*

Ajoute ces métriques dans le contrôleur / wrappers des solveurs et dans les optimiseurs :

* `meta.duration_seconds` — temps total de la commande.
* `meta.solver_calls` — nombre d’appels réels au solveur hydraulique.
* `meta.solver_time_seconds` — somme des temps passés dans EPANET/LCPI solver.
* `meta.eval_count` — nombre d’évaluations de fitness (combien de fois la solution a été simulée).
* `meta.cache_hit` / `meta.cache_key` — si résultat provient du cache.
* `meta.surrogate_used` (bool) et `meta.n_surrogate_evals`.
* `metrics.genetic_generations_run` et `metrics.population_size` si GA.

### Exemple : décorateur Python pour logguer temps d'appel du solver

```python
import time, logging
def timed_solver_call(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        dt = time.time() - t0
        logging.getLogger("lcpi.optimizer").info("Solver %s executed in %.3fs", func.__name__, dt)
        # increment global counters (pseudo)
        # stats['solver_calls'] += 1
        # stats['solver_time'] += dt
        return res
    return wrapper
```

* Place ce décorateur sur `EPANETOptimizer.simulate_with_tank_height` et sur `LCPI` wrapper.

### Compteur d’évaluations dans GeneticOptimizer

Ajoute dans la boucle d’évaluation :

```python
self.eval_count = 0
# lors de chaque évaluation:
self.eval_count += 1
# à la fin, expose self.eval_count into result.meta
```

---

## 4) Signes que quelque chose est mal implémenté (et comment corriger)

### Symptôme A — Très rapide + pas de fichiers `.out` EPANET / pas de process

**Cause probable** : EPANET n’est pas lancé.
**Vérif** : chercher `.out` ou `epanet` process, vérifier `meta.solver_calls == 0`.
**Remède** : corriger wrapper EPANET pour exécuter réellement WNTR/epanet, ou s’assurer que la config du chemin exécutable est correcte.

### Symptôme B — `meta.cache_hit==true` tout le temps

**Cause** : cache trop permissif (mauvais hash) ou clés incomplètes (ne pas prendre en compte constraints, price DB, solveur version).
**Vérif** : afficher la clé de cache.
**Remède** : inclure `price_db_checksum`, `solver_version`, `seed`, `meta.constraints` dans le hash.

### Symptôme C — `meta.surrogate_used==true` mais `n_validation==0`

**Cause** : surrogate non validé, optimisation purement sur ML (risque).
**Remède** : exiger K validations réelles par défaut (p.ex. `n_validation=10`), ou au moins valider le top-1 sur EPANET.

### Symptôme D — GeneticOptimizer n’incrémente pas generation counter

**Cause** : code renvoie une solution triviale, population vide, ou wrapper court-circuite.
**Remède** : instrumenter, ajouter `assert` sur `pop_size > 0`, logging de gen index.

---

## 5) Tests à automatiser pour la CI (exemples)

* **test\_solver\_invocation** : lancer `network-optimize-unified` sur petit INP avec `--solver epanet` et assert `meta.solver_calls >= N` (pour GA doit être >100 pour modestes pop/gens).
* **test\_cache\_behavior** : run twice identical request; second run must have `meta.cache_hit==true` and time << first.
* **test\_surrogate\_validation** : when surrogate used, check `meta.n_validations >= K`.
* **test\_results\_consistency** : if EPANET run, pressures in `result` match direct WNTR simulation within tolerance (e.g. ±0.05 m).

---

## 6) Actions concrètes recommandées maintenant (ordre de priorité)

1. **Exécuter les tests rapides ci-dessus** (shell + Python). Ça te montrera s’il y a un vrai solveur.
2. **Vérifier le `meta` du JSON de sortie** — s’il manque `eval_count` / `solver_calls`, ajoute cette instrumentation (déjà décrite).
3. **Forcer un long run** (grand nombre de générations / désactiver cache et surrogate) ; mesurer avec `time`. Si ça reste rapide → bug probable qui évite l’évaluation.
4. **Chercher des "mocks" / conditions de dev** dans le code : grep pour `mock`, `if settings.env == 'test'`, `surrogate`, `return sample`, `TODO`.
   Exemple grep :

   ```bash
   grep -R "mock\|surrogate\|fast_return\|early_exit" src | sed -n '1,200p'
   ```
5. **Instrumenter `EPANETOptimizer.simulate_with_tank_height`** avec le décorateur `timed_solver_call` et relancer; vérifier logs.
6. **Ajouter une sanity-check post-run** : comparer un nœud au hasard en appelant WNTR et comparer aux valeurs retournées par LCPI (voir script Python ci-dessus).

---

## 7) Exemple rapide : comment ajouter `--no-cache` et `--no-surrogate` (si pas présents)

Si le CLI n’expose pas ces flags, ajoute-les dans la commande Typer :

```python
@app.command()
def network_optimize_unified(input_file: Path, no_cache: bool = False, no_surrogate: bool = False, ...):
    config.use_cache = not no_cache
    config.use_surrogate = not no_surrogate
    ...
```

Puis réitère les tests.

---

## 8) Conclusion — est-ce normal ?

* **Ce n’est pas normal** qu’une vraie optimisation GA + EPANET prenne 1–5s pour un réseau non trivial.
* **Mais** ce comportement **peut** être normal si : la commande sert un résultat mis en cache, utilise un surrogate non validé, ou exécute un mock/test-mode.
* **Objectif immédiat** : vérifier s’il y a un appel EPANET réel et combien d’évaluations sont faites. Les étapes et scripts ci-dessus te permettent d’en être sûr rapidement.

--