### Audit implémentation flux hybride (GA + raffinement local)

#### Portée
- Fichiers analysés:
  - `src/lcpi/aep/optimizer/controllers.py`
  - `src/lcpi/aep/optimization/genetic_algorithm.py`
  - `src/lcpi/aep/core/epanet_wrapper.py`
  - `src/lcpi/core/progress_ui.py`
  - `src/lcpi/aep/cli.py`
  - `tools/*` (tests/diagnostics progression et streaming)

---

### 1) Checklist vérification (PASS / FAIL)

1. Charger réseau et config
- PASS — La CLI transmet `generations`, `population`, contraintes vers le contrôleur puis l'optimiseur.
  - `src/lcpi/aep/cli.py` (≈ L2875-L2895, L3091-L3101, L3166-L3188)
  - Défauts utilisés: generations=120, population=120, pression_min=10, vitesse_min=0.3, vitesse_max=1.5.
- PASS — Le GA applique les valeurs par défaut attendues.
  - `src/lcpi/aep/optimization/genetic_algorithm.py` (≈ L60-L69)
- FAIL (mineur) — Hauteur réservoir par défaut incohérente lors de l’enrichissement LCPI (10.0 au lieu de 50.0).
  - `src/lcpi/aep/optimizer/controllers.py` (≈ L1281-L1284, L1326-L1329, L1369-L1373)

2. Callback et progression
- PASS — Adaptateur de progression normalisé créé par le contrôleur et transmis à l’optimiseur.
  - `src/lcpi/aep/optimizer/controllers.py` (≈ L23-L110, L880-L895)
- PASS — L’optimiseur transmet le callback au simulateur EPANET.
  - GA: `genetic_algorithm.py` (≈ L92-L103, L183-L191)
  - EPANET: `epanet_wrapper.py` (≈ L915-L973)

3. Émissions d’événements (présence/signature)
- PASS — run start: `genetic_algorithm.py` (≈ L414-L418)
- PASS — generation start: `genetic_algorithm.py` (≈ L429-L433)
- PASS — individual start/end: `genetic_algorithm.py` (≈ L447-L455) — inclut index, cost, fitness
- PASS — generation end: `genetic_algorithm.py` (≈ L493-L497)
- PASS — best updated: contrôleur émet `best_updated` (≈ L1698-L1707). GA émet `best_improved` (≈ L474-L476).
  - Proposition: alias `best_updated` côté GA (diff suggéré ci-dessous).
- PASS — simulation start/done: GA (≈ L271-L277), wrapper EPANET (≈ L922-L971)

4. Simulation et usage EPANET
- PASS — `simulate()` appelé pour chaque individu (INP) et payload contient min pressure / max velocity (+ flows via wrapper).
  - GA: (≈ L171-L191, L267-L281)
  - EPANET wrapper: extraction `flows_m3_s`, agrégats (≈ L1245-L1302)

5. Centralisation best cost
- PASS — `meta.best_cost` mis à jour depuis la meilleure proposition et événement `best_updated` émis.
  - `controllers.py` (≈ L1696-L1713)

6. Hybridation et refiner
- PASS — Refiner périodique sur élites via callback de génération; coûts mis à jour et propagés.
  - `controllers.py` (≈ L989-L1116)
- PASS — Raffinement post-run top-k si configuré (≈ L1511-L1517)

7. Cache et --no-cache
- PASS — Clé de cache inclut SHA réseau, backend, db prix, contraintes, et paramètres algo pertinents. `--no-cache` bypass lecture/écriture.
  - `controllers.py` (≈ L939-L986, L1665-L1678)

8. Multiprocessing
- PASS — Désactivé par défaut (évite objets non picklables).
  - `genetic_algorithm.py` (≈ L421-L423)

9. Sorties artefacts
- PASS — Écritures JSON/plots/artefacts de flux via `FlowEventConsumer` et `inspect_simulation_result`; inclusion statistiques hydrauliques et temps.
  - `controllers.py` (≈ L1231-L1488)

10. UI cohérence
- PASS — UI consomme `meta.best_cost` et la barre Population progresse sur `individual_start`/`end`.
  - `progress_ui.py` (≈ L169-L176, L293-L339)

---

### 2) Propositions de corrections (diffs unifiés)

2.1. Alias best_updated dans le GA pour conformité des événements

```diff
@@
-                try:
-                    self._emit("best_improved", {"generation": generation, "new_cost": current_best_cost})
-                except Exception:
-                    pass
+                try:
+                    self._emit("best_improved", {"generation": generation, "new_cost": current_best_cost})
+                except Exception:
+                    pass
+                # Alias pour compatibilité avec l'UI/contrat d'événements
+                try:
+                    self._emit("best_updated", {"generation": generation, "best_cost": current_best_cost})
+                except Exception:
+                    pass
```

2.2. Harmoniser la hauteur de réservoir par défaut à 50 m lors de l’enrichissement LCPI

```diff
@@
-                        network_data = convert_to_solver_network_data(
-                            lcpi_final._get_network_model_from_path(str(input_path)),
-                            10.0,  # H_tank par défaut
-                            diams
-                        )
+                        network_data = convert_to_solver_network_data(
+                            lcpi_final._get_network_model_from_path(str(input_path)),
+                            50.0,  # H_tank par défaut (aligné avec la règle)
+                            diams
+                        )
@@
-                            network_data = convert_to_solver_network_data(
-                                lcpi_final._get_network_model_from_path(str(input_path)),
-                                10.0,  # H_tank par défaut
-                                diams
-                            )
+                            network_data = convert_to_solver_network_data(
+                                lcpi_final._get_network_model_from_path(str(input_path)),
+                                50.0,  # H_tank par défaut (aligné avec la règle)
+                                diams
+                            )
@@
-                    network_data = convert_to_solver_network_data(
-                        lcpi_final._get_network_model_from_path(str(input_path)),
-                        10.0,  # H_tank par défaut
-                        diams
-                    )
+                    network_data = convert_to_solver_network_data(
+                        lcpi_final._get_network_model_from_path(str(input_path)),
+                        50.0,  # H_tank par défaut (aligné avec la règle)
+                        diams
+                    )
```

---

### 3) Commandes de test rapide (non interactives)

- Vérification CLI Optimizer
```bash
python -m src.lcpi.aep.cli optimizer --help | cat
```

- Test adaptateur de progression et événements
```bash
python tools/test_progress_adapter.py | cat
```

- Test optimisation + streaming/artefacts (petit INP)
```bash
python tools/test_optimization_streaming.py --inp examples/bismark-Administrator.inp --backend wntr --no-cache | cat
```

Attendus: événements `run_start`, `generation_start`, `individual_start/end`, `sim_start/done`, `best_updated`; dossier `temp/epanet_archive` et artefacts de flux si activés.

---

### 4) Test d’intégration complet

Mono-solveur EPANET, UI Rich, sortie JSON:
```bash
python -m src.lcpi.aep.cli optimizer network-optimize-unified \
  --input examples/bismark-Administrator.inp \
  --method auto \
  --solver epanet \
  --generations 5 \
  --population 6 \
  --verbose \
  --output results/test_full.json \
  --no-cache \
  --epanet-backend wntr
```

Résultats attendus:
- UI affiche barres Générations/Population/Simulations (si TTY).
- `results/test_full.json` contient `meta.best_cost`, `meta.sim_time_seconds_total`, `meta.solver_calls`, `hydraulics` avec `pressures_m`, `velocities_m_s`, `flows_m3_s`.
- Événements observables (`best_updated`, etc.).

---

### Conclusion

L’implémentation du flux hybride (génétique + raffinement périodique + raffinement post-run) est conforme au diagramme fonctionnel attendu. Deux ajustements mineurs recommandés: (1) alias `best_updated` dans le GA pour homogénéiser l’UI, (2) H_tank par défaut à 50 m dans les chemins d’enrichissement LCPI.
