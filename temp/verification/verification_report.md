# Vérification automatisée — network-optimize-unified

## Résumé des fichiers générés

- out_opt_500: temp\out_bismark_inp_demand_600.json
- out_opt_600: temp\out_bismark_inp_demand_improved.json
- sim_500: temp\sim_500.json
- sim_600: temp\sim_600.json

## Checks basiques (existence / simulateur)

- opt500: {'simulator_used': 'epanet', 'sim_time_seconds': None}

- opt600: {'simulator_used': 'epanet', 'sim_time_seconds': None}

- sim500: {'simulator_used': 'epanet', 'sim_time_seconds': None}

- sim600: {'simulator_used': 'epanet', 'sim_time_seconds': None}

## Demandes détectées dans INP avant simulation

- INP utilisé pour 500-run: C:\PROJET_DIMENTIONEMENT_2\temp\epanet_archive\sim.inp -> sum_demands = None

- INP utilisé pour 600-run: C:\PROJET_DIMENTIONEMENT_2\temp\epanet_archive\sim.inp -> sum_demands = None

## Diamètres extraits

- diametres (opt500) sample count 0 -> mean: N/A

- diametres (opt600) sample count 0 -> mean: N/A

## Summary simulations

- sim500 summary: {'cost': 3750065.0, 'simulation_time': None, 'n_nodes': 0, 'n_links': 0, 'pressure_min': None, 'pressure_max': None, 'flow_sum': None, 'demand_sum': None}

- sim600 summary: {'cost': 3750065.0, 'simulation_time': None, 'n_nodes': 0, 'n_links': 0, 'pressure_min': None, 'pressure_max': None, 'flow_sum': None, 'demand_sum': None}

## Anomalies détectées

- Impossible de lire les demandes dans au moins un INP avant simulation.

- opt500 semble ne pas contenir de durée de simulation (meta.sim_time_seconds manquant).

- opt600 semble ne pas contenir de durée de simulation (meta.sim_time_seconds manquant).

- sim500 semble ne pas contenir de durée de simulation (meta.sim_time_seconds manquant).

- sim600 semble ne pas contenir de durée de simulation (meta.sim_time_seconds manquant).

- Coût total identique pour les deux scénarios -> vérifier la logique d'évaluation du coût.
