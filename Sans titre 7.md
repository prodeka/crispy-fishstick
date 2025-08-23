
---

````
Contexte : dépôt lcpi (module AEP). Objectif : appliquer et vérifier les améliorations décrites dans la TODO pour la commande `lcpi aep network-optimize-unified`. Ne pusher QUE si toutes les tâches listées sont implémentées et vérifiées (critères de validation ci-dessous).

Instruction générale :
1. Crée une branche de travail `feature/unify-optimizer` (local).
2. Mets à jour le fichier TODO (ou crée `TODO.md` à la racine si absent) : marquer chaque tâche comme **à faire / en cours / fait**, avec qui (auto), date et commit SHA quand fini.
3. Pour chaque item de priorité (1 → 3) vérifier l’implémentation, corriger si nécessaire, ajouter/mettre à jour tests, et committer les changements. N’effectue un `git push` qu’à la toute fin et seulement si tous les tests passent et les critères d’acceptation sont remplis.

Fichiers clés à auditer / modifier :
- `src/lcpi/aep/optimizer/controllers.py`
- `src/lcpi/aep/optimization/genetic_algorithm.py`
- `src/lcpi/core/progress_ui.py`
- `tools/simulate_wntr_sumflows.py` (ou `src/lcpi/aep/tools/...`)
- `reporting/enable-wkhtmltopdf.ps1`
- `tools/test_progress_adapter.py` et ajouter `tools/test_optimization_streaming.py`
- `tests/fixtures/mini_network.inp`

## Priorité 1 — Améliorations UI & events (ACCEPTANCE)
- Vérifier que le progress adapter normalise et relaie ces événements : `individual_start`, `individual_end`, `simulation` (busy/done), `best_updated`.
  - Test unitaire : `tools/test_progress_adapter.py` doit produire les logs "progress adapter received" et vérifier émission des événements.
- Dans `progress_ui.py` : 
  - Sur `generation_start` initialiser `completed=0` et description "Éval 0/total".
  - Sur `individual_end`, si index absent ou 0, incrémenter d’au moins 1.
- Supporter streaming de snapshots `simulation.snapshot` si le simulateur peut émettre pas-à-pas.
  - Si simulateur émet `simulation.snapshot` avec `{time_h, flows: {pipe: value}}`, collecter et sauvegarder (voir Priorité 2).

Critères d’acceptation (Priorité 1) :
- Tests unitaires liés passent.
- `progress_callback` est correctement branché (vérifier `set_progress_callback` existant).
- Adapter logge un événement `best_updated` lorsque le meilleur solution change.

## Priorité 2 — Observabilité, artefacts, rapports (ACCEPTANCE)
- Implémenter export post-sim : `artifacts/<run_id>/flows_timeseries.json`, `.csv`, `.png`.
  - Ajouter/valider `tools/simulate_wntr_sumflows.py` et appeler depuis `controllers.py` après une simulation.
- Logger `REPAIR_DIAMETERS_APPLIED` (before/after, count) et `FLOW_CONSERVATION_BREACH` (valeur + seuil).
- Après chaque simulation finale, exécuter `wntr_sum_flows_check(inp)` (ou `run_wntr_sumflows_and_save`) et attacher artefacts à `meta.artifacts.flows`.

Critères d’acceptation (Priorité 2) :
- Les fichiers JSON/CSV/PNG sont créés dans `artifacts/run_<YYYYMMDD_HHMMSS>/`.
- `meta` du résultat contient `artifacts.flows` avec chemins valides.
- Logs trouvables contenant `REPAIR_DIAMETERS_APPLIED` et `FLOW_CONSERVATION_BREACH` si applicable.

## Priorité 3 — Robustesse & packaging (ACCEPTANCE)
- Placer `vendor/wkhtmltopdf/bin/wkhtmltopdf.exe` (ou vérifier présence) et maintenir script `reporting/enable-wkhtmltopdf.ps1`.
- Ajouter jobs CI qui exécutent `tools/test_progress_adapter.py` et `tools/test_optimization_streaming.py` (mini INP) et valident `meta.best_cost` et `proposals[0].CAPEX`.
- Par défaut `H_tank = 50.0`. Remplacer occurrences `10.0` dans code de création `network_data` par `50.0` (rechercher usages exacts et remplacer).

Critères d’acceptation (Priorité 3) :
- CI local : les jobs ajoutés s’exécutent et passent (sur runner local ou container).
- Tous les changements sont documentés dans `TODO.md`.
- Binaire wkhtmltopdf accessible via `reporting/enable-wkhtmltopdf.ps1` (test `wkhtmltopdf --version` retourne version).

## Réparation diamètres (_ensure_at_least_one_feasible)
Remplacer heuristique agressive par :
- Sélectionner jusqu’à **5** tronçons les plus critiques (plus petites diamètres).
- Augmenter **1 cran** par itération.
- Re-simuler et sortir si OK.
- Logger `REPAIR_DIAMETERS_APPLIED` (liste before/after, count).
Critère : code doit appliquer la nouvelle logique et les tests d’intégration doivent vérifier qu’on ne monte pas plus d’un cran par itération et que l’algorithme termine quand constraints ok.

## Opérations / commandes à exécuter pour vérification (exécutentelles maintenant)
Lancer dans l’ordre suivant (doit être automatisé dans le script d’intégration local) :

1) Créer branche :
```bash
git checkout -b feature/unify-optimizer
````

2. Lancer tests unitaires :
    

```bash
pytest -q || { echo "Unit tests failed"; exit 1; }
```

3. Test progress adapter :
    

```bash
python tools/test_progress_adapter.py
# Attendu: logs "progress adapter received" et émission events.
```

4. Mini optimisation de vérification :
    

```bash
python -m lcpi.aep.cli network-optimize-unified examples/bismark-Administrator.inp \
  --method genetic --solver epanet --generations 2 --population 20 \
  --no-cache --no-surrogate --verbose --output /tmp/out.json
python -c "import json; d=json.load(open('/tmp/out.json')); print('meta.best_cost', d.get('meta',{}).get('best_cost')); print('proposal capex', d.get('proposals',[])[0].get('CAPEX'))"
# Attendu: meta.best_cost présent et égal (ou cohérent) avec proposals[0].CAPEX
```

5. Test post-sim export flows :
    

```bash
python tools/simulate_wntr_sumflows.py --inp examples/bismark-Administrator.inp --out artifacts/sim_one.json --csv artifacts/sim_one_flows.csv
# Attendu: JSON + CSV + sim_one_flow.png créés
```

6. Rechercher et remplacer usages `10.0` → `50.0` seulement dans le contexte H_tank / create network_data :
    

```bash
# rechercher occurrences potentiellement sensibles
git grep -n "10.0" | grep -E "h_tank|H_tank|create_network|network_data" || true
# remplacer manuellement via editor ou sed si confirmé
```

7. Exécution finale des tests d’intégration (si présents) :
    

```bash
pytest tests/integration -q || { echo "Integration tests failed"; exit 1; }
```


## Push & merge (conditionnel)

- Si et seulement si toutes les étapes ci-dessous sont OK :
    
    - Tous les tests unitaires et d’intégration passent.
        
    - Les fichiers d’artefacts attendus existent pour la mini-run.
        
    - La TODO est mise à jour et chaque item marqué **fait**.
        
    - Les logs attendus sont présents (`REPAIR_DIAMETERS_APPLIED`, `FLOW_CONSERVATION_BREACH` si déclenchés).
        
- Alors :
    

```bash
git add -A
git commit -m "feature: unify optimizer events, safer repairs, flows diagnostics, wkhtmltopdf vendor script"
git push origin feature/unify-optimizer
# préparer PR via hub/gh or UI, inclure checklist et artifacts
```

- Si une erreur survient à tout moment : annuler les changements non validés (`git restore --staged .; git checkout -- .`) et documenter le blocage dans `TODO.md`.
    

## Reporting attendu  (format exigé)

Au retour, fournir :

1. Un résumé en Markdown listant chaque sous tâche + statut (fait/en cours/à faire).
    
2. Pour chaque test lancé : commande exécutée, sortie (stdout/stderr), exit status, chemins des artefacts générés.
    
3. Diffs / patchs (via `git format-patch -1 HEAD --stdout` ou `git diff`) attachés.
    
4. Si push effectué, indiquer le nom de la branche et SHA du commit.
    
5. Un verdict global (OK / NOK) avec liste des éléments restants si NOK.
    

---

Règle cruciale : **ne pusher que si tout est terminé et validé**. Si tu détectes un risque élevé (multiprocessing, dépendances manquantes, wkhtmltopdf absent), n’effectue pas le push ; documente précisément le blocage et propose une solution corrective.
