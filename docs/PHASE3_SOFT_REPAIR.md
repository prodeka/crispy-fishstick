# Phase 3 : Réparation Douce (Soft Repair) - Documentation

## Vue d'ensemble

La Phase 3 introduit un mécanisme de **réparation douce** dans l'algorithme génétique pour tenter de corriger intelligemment les solutions infaisables sans appliquer de changements brutaux.

## Objectifs

1. **Améliorer la convergence** : Aider l'algorithme à trouver des solutions faisables plus rapidement
2. **Préserver la diversité** : Éviter les changements trop drastiques qui pourraient déstabiliser la population
3. **Optimiser les coûts** : S'assurer que les réparations n'augmentent pas excessivement le coût total
4. **Intelligence ciblée** : Identifier et réparer les conduites les plus problématiques en priorité

## Architecture

### 1. Module de Réparation (`src/lcpi/aep/optimization/repairs.py`)

#### Fonction principale : `soft_repair_solution()`

```python
def soft_repair_solution(
    diameters_map: Dict[str, int],
    simulation_metrics: Dict,
    candidate_diameters: List[int],
    max_changes_fraction: float = 0.10,
    constraints: Optional[Dict] = None
) -> Tuple[Dict[str, int], Dict]:
```

**Paramètres :**
- `diameters_map` : Dictionnaire des diamètres actuels par conduite
- `simulation_metrics` : Résultats de simulation incluant les pertes de charge
- `candidate_diameters` : Liste des diamètres candidats disponibles
- `max_changes_fraction` : Fraction maximale de conduites à modifier (défaut: 10%)
- `constraints` : Contraintes du problème (optionnel)

**Retour :**
- Nouveau dictionnaire de diamètres
- Dictionnaire de diagnostic des changements effectués

#### Logique de réparation

1. **Identification des conduites problématiques** :
   - Trie les conduites par perte de charge (de la plus élevée à la plus basse)
   - Sélectionne les N conduites les plus problématiques

2. **Augmentation progressive** :
   - Augmente le diamètre d'un seul cran dans la liste des candidats
   - Évite les changements trop drastiques

3. **Contrôle des limites** :
   - Ne dépasse jamais le diamètre maximum disponible
   - Gère les cas où le diamètre actuel n'est pas dans la liste des candidats

### 2. Intégration dans l'Algorithme Génétique

#### Méthode : `_apply_soft_repair()`

```python
def _apply_soft_repair(self, population: List[Individu], candidate_diameters: List[int]):
```

**Étapes :**

1. **Sélection des candidats** :
   - Identifie les individus infaisables
   - Trie par fitness (meilleurs d'abord)
   - Sélectionne les K meilleurs infaisables

2. **Tentative de réparation** :
   - Applique `soft_repair_solution()` à chaque candidat
   - Vérifie que des changements ont été effectués

3. **Évaluation de la solution réparée** :
   - Calcule le nouveau coût
   - Vérifie la contrainte de surcoût (max 10% par défaut)
   - Re-simule la solution réparée

4. **Critères d'acceptation** :
   - La simulation doit réussir
   - Les violations doivent diminuer
   - Le coût ne doit pas augmenter excessivement

5. **Application de la réparation** :
   - Remplace l'individu original par sa version réparée
   - Ré-évalue complètement l'individu

#### Hook dans la boucle principale

La réparation douce est appelée après l'évaluation de la population et avant la sélection/croisement :

```python
# Tri par fitness
self.population.sort(key=lambda x: getattr(x, 'fitness', 0.0), reverse=True)

# --- HOOK DE RÉPARATION DOUCE ---
candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
self._apply_soft_repair(self.population, candidate_diams)

# Mise à jour de la meilleure solution
# ...
```

## Paramètres configurables

### Dans la configuration de l'algorithme

```yaml
algorithme:
  repair_top_k: 3                    # Nombre d'individus infaisables à réparer
  repair_max_cost_increase_ratio: 1.10  # Surcoût maximum autorisé (10%)
```

### Dans la fonction de réparation

```python
max_changes_fraction: float = 0.10  # Fraction maximale de conduites à modifier
```

## Tests unitaires

### Fichier : `tests/optimizer/test_repairs.py`

**Tests inclus :**

1. **`test_soft_repair_increases_most_problematic_pipe()`** :
   - Vérifie que la conduite avec la plus grosse perte de charge est réparée en priorité
   - Confirme l'augmentation d'un seul cran

2. **`test_soft_repair_no_headlosses_data()`** :
   - Teste le comportement quand les données de perte de charge sont manquantes
   - Aucune réparation ne doit être effectuée

3. **`test_soft_repair_maximum_diameter_reached()`** :
   - Vérifie le comportement quand tous les diamètres sont déjà au maximum
   - Aucune réparation possible

4. **`test_soft_repair_multiple_pipes()`** :
   - Teste la réparation de plusieurs conduites simultanément
   - Vérifie l'ordre de priorité basé sur les pertes de charge

5. **`test_soft_repair_invalid_diameter()`** :
   - Teste le comportement avec des diamètres invalides
   - Gestion des erreurs appropriée

## Avantages de la Phase 3

### 1. Convergence améliorée
- Aide à échapper aux minima locaux
- Accélère la découverte de solutions faisables
- Réduit le temps d'optimisation

### 2. Robustesse
- Évite les changements trop drastiques
- Préserve la diversité de la population
- Maintient l'équilibre exploration/exploitation

### 3. Intelligence ciblée
- Identifie les vraies causes des violations
- Répare de manière sélective et efficace
- Optimise l'utilisation des ressources

### 4. Contrôle des coûts
- Limite l'augmentation des coûts
- Évite les solutions économiquement irréalistes
- Maintient la faisabilité budgétaire

## Limitations et considérations

### 1. Coût computationnel
- Chaque réparation nécessite une nouvelle simulation
- Limité aux K meilleurs individus infaisables
- Paramètres configurables pour équilibrer coût/bénéfice

### 2. Dépendances
- Nécessite des données de perte de charge par conduite
- Dépend de la qualité des métriques de simulation
- Requiert une liste de diamètres candidats valide

### 3. Heuristique
- Basé sur les pertes de charge comme proxy des problèmes
- Ne garantit pas toujours l'amélioration
- Critères d'acceptation stricts pour éviter la dégradation

## Utilisation

### Activation automatique
La réparation douce est activée automatiquement dans l'algorithme génétique. Aucune configuration supplémentaire n'est nécessaire.

### Configuration optionnelle
Pour personnaliser le comportement :

```python
# Dans la configuration
config.algorithme.repair_top_k = 5  # Réparer 5 individus au lieu de 3
config.algorithme.repair_max_cost_increase_ratio = 1.15  # 15% de surcoût max
```

### Monitoring
Les logs détaillent les tentatives de réparation :

```
[INFO] Tentative de réparation douce sur l'individu avec score=0.85...
[INFO] Réparation ACCEPTÉE sur individu. Violation réduite: 0.0234 -> 0.0187. Coût: 1,234,567 FCFA.
[DEBUG] Réparation rejetée: la violation n'a pas diminué.
```

## Évolution future

### Améliorations potentielles

1. **Réparation multi-critères** :
   - Considérer d'autres métriques que les pertes de charge
   - Pondération adaptative des critères

2. **Réparation adaptative** :
   - Ajuster les paramètres selon la phase d'optimisation
   - Apprentissage des stratégies de réparation efficaces

3. **Réparation collaborative** :
   - Coordonner les réparations entre plusieurs individus
   - Éviter les conflits de réparation

4. **Métriques avancées** :
   - Utiliser des indicateurs de performance hydraulique plus sophistiqués
   - Intégrer des contraintes de fiabilité

## Conclusion

La Phase 3 introduit un mécanisme de réparation douce intelligent qui améliore significativement la convergence de l'algorithme génétique tout en préservant la diversité et en contrôlant les coûts. Cette approche ciblée et progressive représente une évolution importante dans l'optimisation des réseaux d'eau potable.
