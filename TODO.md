iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

## Priorité 1 — Améliorations UI & events (ACCEPTANCE)

- **Tâche**: Vérifier que le progress adapter normalise et relaie ces événements : `individual_start`, `individual_end`, `simulation` (busy/done), `best_updated`.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Dans `progress_ui.py` : Sur `generation_start` initialiser `completed=0` et description "Éval 0/total".
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Dans `progress_ui.py` : Sur `individual_end`, si index absent ou 0, incrémenter d’au moins 1.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Supporter streaming de snapshots `simulation.snapshot` si le simulateur peut émettre pas-à-pas.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A

## Priorité 2 — Observabilité, artefacts, rapports (ACCEPTANCE)

- **Tâche**: Implémenter export post-sim : `artifacts/<run_id>/flows_timeseries.json`, `.csv`, `.png`.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Logger `REPAIR_DIAMETERS_APPLIED` (before/after, count) et `FLOW_CONSERVATION_BREACH` (valeur + seuil).
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Après chaque simulation finale, exécuter `wntr_sum_flows_check(inp)` et attacher artefacts à `meta.artifacts.flows`.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A

## Priorité 3 — Robustesse & packaging (ACCEPTANCE)

- **Tâche**: Placer `vendor/wkhtmltopdf/bin/wkhtmltopdf.exe` et maintenir script `reporting/enable-wkhtmltopdf.ps1`.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Ajouter jobs CI qui exécutent `tools/test_progress_adapter.py` et `tools/test_optimization_streaming.py` et valident `meta.best_cost` et `proposals[0].CAPEX`.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Par défaut `H_tank = 50.0`. Remplacer occurrences `10.0` dans code de création `network_data` par `50.0`.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A

## Réparation diamètres (_ensure_at_least_one_feasible)

- **Tâche**: Remplacer heuristique agressive par : sélectionner jusqu’à 5 tronçons les plus critiques, augmenter 1 cran par itération, re-simuler et sortir si OK.
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
- **Tâche**: Logger `REPAIR_DIAMETERS_APPLIED` (liste before/after, count).
  - **Statut**: À faire
  - **Assigné à**: auto
  - **Commit**: N/A
