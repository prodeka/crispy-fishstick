# AMÉLIORATION V14 — Unification Optimisation Réseau (INP direct, contraintes, méthodes, hybridation)

## Objectif
Offrir une commande unique et complète pour optimiser un réseau AEP à partir d’un fichier `.inp` ou `.yml`, avec:
- Choix du solveur hydraulique (`--solver epanet|lcpi`),
- Contraintes hydrodynamiques en ligne (`--pression-min`, `--vitesse-min`, `--vitesse-max`),
- Sélection du modèle d’optimisation (`--method genetic|nested|surrogate|global|multi-tank`),
- Hybridation (raffinage local) via `--hybrid-refiner` (ex: `nested`).

Commande cible:
```bash
lcpi aep network-optimize-unified mon_reseau.inp \
  --method nested \
  --solver epanet \
  --pression-min 15 \
  --vitesse-max 2.0 \
  --output resultats/mon_optimisation.json
```

## Contexte existant (état du code)
- `lcpi aep simulate-inp <.inp>`: simulation EPANET simple (sans contraintes, sans sélection de solveur par option).
- `lcpi aep optimizer price-optimize <.inp>` (V12): optimisation avec `nested` (EPANET forcé), pression min via YAML; vitesses non exposées.
- `lcpi aep network-optimize-unified <.yml>`: attend un YAML; permet `--solver`; contraintes gérées via YAML; méthodes d’optimisation non unifiées.
- Convertisseur INP→YAML disponible via `lcpi aep convert-inp` (à réutiliser en mémoire).

Références principales:
- `src/lcpi/aep/cli.py` (commandes AEP, `simulate_inp`, `network-optimize-unified`).
- `src/lcpi/aep/optimizer/cli_commands.py` (V11: `price-optimize`, `report`).
- `src/lcpi/aep/core/epanet_wrapper.py` (EPANET/WNTR wrapper et simulation robuste).
- Optimiseurs: `optimizer/algorithms/{nested, global_opt, surrogate, multi_tank}.py`.

## Portée (V14)
- Modifier UNIQUEMENT `network-optimize-unified` pour:
  1) Accepter `.inp` en entrée en plus du `.yml`.
  2) Ajouter des options de contraintes: `--pression-min`, `--vitesse-min`, `--vitesse-max`.
  3) Ajouter `--method` pour sélectionner l’algorithme.
  4) Ajouter `--hybrid-refiner` pour activer l’heuristique mémétique (raffinage local).
  5) Journaliser dans un format standard consommable par `lcpi aep optimizer report` (V11) et par `lcpi report`.

Hors portée immédiate:
- Refonte des optimisateurs internes.
- Ajout d’un solveur tiers.

## Spécification fonctionnelle
- Entrée:
  - `input_file`: `.inp` ou `.yml`. Si `.inp`, conversion en mémoire vers un modèle réseau unifié (sans fichier intermédiaire sur disque).
- Options (nouvelles ou exposées):
  - `--solver [epanet|lcpi]` (déjà présent — à conserver).
  - `--method [genetic|nested|surrogate|global|multi-tank]` (nouveau).
  - `--hybrid-refiner [nested|global|...]` (nouveau, optionnel).
  - `--pression-min <m>` (nouveau).
  - `--vitesse-min <m/s>` (nouveau).
  - `--vitesse-max <m/s>` (nouveau).
  - `--generations`, `--population`, `--verbose`, `--output` (inchangés).
- Sortie: JSON standardisé avec métadonnées comprenant `method` et, si pertinent, `hybrid_refiner` (ex: "method": "genetic+nested_local_search").
- Compatibilité rapport: le JSON est loggé/formaté comme V11 (ou adaptateur minimal) afin que `lcpi aep optimizer report` ou `lcpi report` acceptent la sortie.

## Spécification technique
### 1) Prise en charge `.inp`
- Détection via suffixe `.inp`.
- Conversion en mémoire: réutiliser la logique de `convert-inp` (helper interne) ou `epanet_wrapper.EPANETOptimizer.simulate`/WNTR pour lire la topologie et construire une structure unifiée `{network: {nodes, pipes}}`.
- Pas d’écriture disque (sauf si debug/verbose demandé) — utiliser des objets Python.

### 2) Contraintes hydrodynamiques
- Mapping des flags en structure de contraintes:
  - `pressure_min_m = --pression-min` (float, défaut existant si non fourni).
  - `velocity_min_m_s = --vitesse-min` (float|None).
  - `velocity_max_m_s = --vitesse-max` (float|None).
- Application:
  - Pour `genetic`: passer dans `ConfigurationOptimisation`/`ConstraintManager` (déjà prévus dans `optimization/constraints.py`).
  - Pour `nested`/`global`/`surrogate`/`multi-tank`: passer les valeurs aux appels d’optimisation (ex: `NestedGreedyOptimizer.optimize_nested(H_bounds, pressure_min_m, velocity_constraints)`),
    avec `velocity_constraints=(min,max)` si fournis; à défaut, vérifier a posteriori la faisabilité (post-simulation) et marquer les propositions non conformes.

### 3) Intégration des modèles d’optimisation (routing par `--method`)
- Arbre de décision dans `network-optimize-unified`:
  - `genetic` (défaut): flux actuel basé sur `optimization/genetic_algorithm.py` + `ConstraintManager` (enrichi avec les nouveaux flags).
  - `nested`: utiliser `NestedGreedyOptimizer` avec le chemin réseau (pour EPANET réel) ou modèle unifié si YAML.
  - `surrogate`: `SurrogateOptimizer`.
  - `global`: `GlobalOptimizer`.
  - `multi-tank`: `MultiTankOptimizer`.
- Normaliser la structure de sortie (adapter si nécessaire via un mini-adaptateur) vers V11/JSON unifié.

### 4) Hybridation via `--hybrid-refiner`
- Principe mémétique: à chaque génération (ou toutes N générations), sélectionner le top-K des solutions et exécuter un pas de recherche locale:
  - Ex: `--method genetic --hybrid-refiner nested` → `GeneticOptimizer` conserve son flux; après `evaluate_population`, appliquer pour chaque meilleure solution `NestedGreedyOptimizer` avec contraintes, sur un nombre limité d’itérations/voisinages.
- Implémentation incrémentale (V14):
  - Hook dans `GeneticOptimizer` (si accessible) ou wrapper local côté CLI: boucle externe sur générations, appel interne de l’optimiseur, puis raffinage; réinjection de la solution raffinée si meilleure.
  - Paramètres par défaut raisonnables (ex: `top_k=3`, `local_steps=1`), exposables plus tard via flags.
- Journalisation: setter `result.metadata.method = "genetic+nested_local_search"` et tracer les améliorations (delta fitness/cost) dans le log.

### 5) Journalisation standardisée
- Utiliser les utilitaires V11 existants (`output.formatter`, `report_adapter.v11_adapter`, `save_optimization_result_v11`).
- Ajouter métadonnées:
  - `method`, `hybrid_refiner`, `solver`, `pressure_min_m`, `velocity_min_m_s`, `velocity_max_m_s`.
- Générer un `*.log.json` compatible `lcpi report` si applicable.

## Détails d’implémentation (par fichiers)
- `src/lcpi/aep/cli.py` — fonction/commande `network-optimize-unified`:
  - Signature: ajouter `--method`, `--hybrid-refiner`, `--pression-min`, `--vitesse-min`, `--vitesse-max`.
  - Entrée: si `input_file.suffix == '.inp'`, appeler un helper `convert_inp_to_unified_model(input_file)` (à créer ou à réutiliser du module existant) pour obtenir `network_model` en mémoire.
  - Routing par `--method` vers les optimiseurs (import léger depuis `optimizer.algorithms` et/ou `optimization.*`).
  - Si `--hybrid-refiner` fourni et `--method==genetic`, activer le cycle de raffinage top-K (wrapper minimal si on ne modifie pas `GeneticOptimizer`).
  - Rassembler le résultat, le convertir au format V11 si besoin, écrire `--output`.

- `src/lcpi/aep/core/epanet_wrapper.py` (si besoin):
  - Exposer un utilitaire `read_inp_topology(path) -> unified_model` si le convertisseur existant n’est pas réutilisable proprement.

- `src/lcpi/aep/optimizer/cli_commands.py` (lecture seule):
  - Réutiliser l’adaptation V11 pour la sortie (sans changer ce module si possible).

- `src/lcpi/aep/optimization/*`:
  - `constraints.py`: s’assurer que pression min et vitesses sont pris en compte (sinon, effectuer un check de faisabilité post-simulation côté CLI pour les méthodes non intégrées).
  - `genetic_algorithm.py`: prévoir un hook simple `refine_with(method, ...)` (facultatif V14) ou faire le raffinage dans la commande CLI.

## Compatibilité & rétro-compatibilité
- `network-optimize-unified` accepte toujours les YAML existants sans changement.
- Les nouvelles options sont facultatives.
- Si l’utilisateur fournit un `.inp`, la conversion est implicite en mémoire, sans obligation de changer ses habitudes.

## Performance
- Lecture `.inp` via WNTR/EPANET: coût négligeable vs optimisation.
- Hybridation: surcoût maîtrisé par `top_k` et `local_steps` (défauts conservateurs).

## Tests (plan minimal)
1) INP simple (bismark) → `simulate-inp` OK, puis `network-optimize-unified .inp` avec `--method nested` → sortie JSON non vide, DN variés.
2) YAML unifié existant → `--method genetic --solver lcpi` → JSON et log générés, contraintes respectées.
3) Contraintes:
   - `--pression-min` modifie la faisabilité: solutions sous la limite sont marquées non conformes.
   - `--vitesse-max`: vitesses dépassées détectées et solutions pénalisées/filtrées.
4) Hybridation: `--method genetic --hybrid-refiner nested` → amélioration mesurable de la meilleure fitness/cost dans le log.
5) Rapport: `lcpi aep optimizer report <json> --template optimisation_tank_v11.jinja2` génère un HTML valide.

## Risques & mitigations
- Variabilité des API WNTR entre versions: prévoir accès robuste (déjà présent dans `EpanetWrapper`).
- Manque de support direct des vitesses dans certains optimiseurs: appliquer un check post-simulation et une pénalisation forte/filtrage.
- Temps d’exécution: activer l’hybridation seulement si demandée.

## Estimation
- Parsing INP en mémoire & wiring CLI: 0.5 j
- Flags contraintes & mapping multi-optimiseurs: 0.5–1 j
- Hybridation simple (raffinage top-K): 1 j
- Journalisation unifiée + tests de bout en bout: 0.5–1 j
Total: ~3 jours ouvrés

## Exemple d’utilisation (récapitulatif)
```bash
# INP direct + nested + contraintes + EPANET
lcpi aep network-optimize-unified mon_reseau.inp \
  --method nested --solver epanet \
  --pression-min 15 --vitesse-max 2.0 \
  --output resultats/mon_optimisation.json

# YAML + génétique + hybridation nested
lcpi aep network-optimize-unified reseau.yml \
  --method genetic --hybrid-refiner nested \
  --generations 80 --population 150 --solver lcpi \
  --output resultats/genetic_nested.json
```

## Conclusion
La modification ciblée de `network-optimize-unified` est faisable et à faible risque. Elle unifie l’expérience utilisateur, supporte les `.inp` directement, expose les contraintes et le choix d’algorithme, et permet une hybridation efficace. Le tout en s’appuyant sur l’infrastructure existante (EPANET/WNTR wrapper, optimiseurs V11/unifiés, adaptateurs de rapport).
