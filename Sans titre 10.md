
### **Prompt pour Cursor AI : Implémentation de la Phase 3**

"Salut. Je démarre une nouvelle session de travail sur mon projet LCPI.

**Contexte :**
Nous avons terminé la Phase 2 avec succès. L'algorithme génétique utilise maintenant un système de pénalité adaptative et non linéaire pour évaluer les solutions, basé sur une classe `ConstraintPenaltyCalculator`.

**Ta mission :**
Tu vas maintenant implémenter la **Phase 3 : Réparation Douce (Soft Repair)**. L'objectif est d'ajouter un mécanisme qui tente de corriger intelligemment un petit nombre des meilleures solutions infaisables à chaque génération, sans appliquer de changements brutaux.

---

### **Étape 1 : Créer le Module de Réparation**

**Explication :** Nous allons isoler la logique de réparation dans un nouveau fichier dédié. La fonction principale identifiera les conduites les plus problématiques et n'augmentera leur diamètre que d'un seul cran.

**Action :** Crée un nouveau fichier `src/lcpi/aep/optimization/repairs.py` et insère-y le contenu suivant.

```python
# --- Contenu du nouveau fichier src/lcpi/aep/optimization/repairs.py ---

from typing import Dict, List, Tuple, Optional
import random
import logging

logger = logging.getLogger(__name__)

def soft_repair_solution(
    diameters_map: Dict[str, int],
    simulation_metrics: Dict,
    candidate_diameters: List[int],
    max_changes_fraction: float = 0.10,
    constraints: Optional[Dict] = None
) -> Tuple[Dict[str, int], Dict]:
    """
    Tente une réparation "douce" d'une solution infaisable.

    Identifie les N conduites les plus problématiques (basé sur la perte de charge)
    et augmente leur diamètre d'un seul cran dans la liste des candidats.

    Retourne le nouveau dictionnaire de diamètres et un dictionnaire de diagnostic.
    """
    changes_made = {"repaired_pipes": [], "total_changes": 0}
    
    # On a besoin des pertes de charge par conduite pour une réparation intelligente
    headlosses = simulation_metrics.get("headlosses_m")
    if not headlosses or not isinstance(headlosses, dict):
        logger.debug("Réparation impossible : métriques de perte de charge par conduite non disponibles.")
        return diameters_map, changes_made
        
    # Trier les conduites par perte de charge, de la plus élevée à la plus basse
    problematic_pipes_sorted = sorted(headlosses.items(), key=lambda item: item[1], reverse=True)
    
    # Calculer le nombre de conduites à modifier (au moins 1)
    num_pipes_to_change = max(1, int(len(diameters_map) * max_changes_fraction))
    
    # Sélectionner les N conduites les plus problématiques
    pipes_to_repair = [pipe_id for pipe_id, _ in problematic_pipes_sorted[:num_pipes_to_change]]
    
    new_diameters_map = dict(diameters_map)
    sorted_candidates = sorted(candidate_diameters)

    for pipe_id in pipes_to_repair:
        current_diameter = new_diameters_map.get(pipe_id)
        if current_diameter is None:
            continue
            
        try:
            current_index = sorted_candidates.index(current_diameter)
            # Augmenter d'un seul cran, sans dépasser la fin de la liste
            new_index = min(current_index + 1, len(sorted_candidates) - 1)
            
            new_diameter = sorted_candidates[new_index]

            if new_diameter != current_diameter:
                new_diameters_map[pipe_id] = new_diameter
                changes_made["repaired_pipes"].append({
                    "pipe_id": pipe_id,
                    "from_dn_mm": current_diameter,
                    "to_dn_mm": new_diameter
                })
        except ValueError:
            # Le diamètre actuel n'est pas dans la liste des candidats, on ne peut rien faire
            logger.warning(f"Impossible de réparer la conduite {pipe_id}: son diamètre {current_diameter} n'est pas dans la liste des candidats.")
            continue
            
    changes_made["total_changes"] = len(changes_made["repaired_pipes"])
    return new_diameters_map, changes_made
```

---

### **Étape 2 : Intégrer ("Hook") la Logique de Réparation dans l'Algorithme Génétique**

**Explication :** Nous allons maintenant modifier la classe `GeneticOptimizer` pour qu'elle utilise cette nouvelle fonction de réparation. L'idée est, à la fin de chaque génération, de :
1.  Identifier les quelques meilleures solutions qui sont encore infaisables.
2.  Tenter de les réparer.
3.  Simuler à nouveau la solution réparée (c'est un coût supplémentaire, donc il faut le faire avec parcimonie).
4.  N'accepter la solution réparée que si elle est "meilleure" (moins de violation) et pas "beaucoup plus chère".

**Action :** Ouvre le fichier `src/lcpi/aep/optimization/genetic_algorithm.py` et ajoute une nouvelle méthode privée `_apply_soft_repair` et modifie la boucle principale de l'algorithme.

```python
# --- Imports à ajouter en haut de genetic_algorithm.py ---
from .repairs import soft_repair_solution

# --- Logique à ajouter/modifier dans la classe GeneticOptimizer ---

# 1. Ajouter cette nouvelle méthode privée à la classe
def _apply_soft_repair(self, population: List, candidate_diameters: List[int]):
    """
    Applique la réparation douce aux meilleurs individus infaisables de la population.
    """
    # Paramètres de la réparation (à rendre configurables)
    repair_top_k = self.algo_params.get("repair_top_k", 3)
    repair_max_cost_increase_ratio = self.algo_params.get("repair_max_cost_increase_ratio", 1.10) # 10% de surcoût max

    # 1. Identifier les candidats à la réparation
    infeasible_individuals = [ind for ind in population if not ind.is_feasible]
    if not infeasible_individuals:
        return # Rien à faire

    # Trier les infaisables par leur score (le moins mauvais d'abord)
    infeasible_individuals.sort(key=lambda ind: ind.score)
    
    # Ne garder que les K meilleurs
    candidates_for_repair = infeasible_individuals[:repair_top_k]

    for individual in candidates_for_repair:
        self.logger.debug(f"Tentative de réparation douce sur l'individu avec score={individual.score:.2f}...")
        
        # 2. Tenter la réparation
        repaired_diam_map, changes = soft_repair_solution(
            individual.diameters,
            individual.metrics,
            candidate_diameters
        )

        if changes["total_changes"] == 0:
            continue # La réparation n'a rien pu faire

        # 3. Évaluer la solution réparée
        repaired_capex = self.scorer.compute_capex(repaired_diam_map)
        
        # Condition d'acceptation de coût
        if repaired_capex > individual.capex * repair_max_cost_increase_ratio:
            self.logger.debug(f"Réparation rejetée: le coût a trop augmenté ({individual.capex:.0f} -> {repaired_capex:.0f}).")
            continue
            
        # Resimuler la solution réparée pour voir si elle est meilleure
        repaired_metrics = self.simulator.run(repaired_diam_map)
        repaired_violations = normalize_violations(repaired_metrics, self.constraints)
        
        # Condition d'acceptation de performance
        if repaired_violations["total"] < individual.metrics["violations"]["total"]:
            self.logger.info(
                f"Réparation ACCEPTÉE sur individu. Violation réduite: "
                f"{individual.metrics['violations']['total']:.4f} -> {repaired_violations['total']:.4f}. "
                f"Coût: {repaired_capex:,.0f} FCFA."
            )
            # Remplacer l'individu original par sa version réparée
            individual.diameters = repaired_diam_map
            # (Optionnel mais recommandé : ré-évaluer complètement l'individu réparé)
            # self._evaluate_individual(individual, ...)
        else:
            self.logger.debug("Réparation rejetée: la violation n'a pas diminué.")

# 2. Modifier la boucle principale de l'AG (dans la méthode run())
# Après la boucle d'évaluation de la population et avant la sélection/croisement :

    # ... (boucle `for individual in population: self._evaluate_individual(...)`)
    
    # --- HOOK DE RÉPARATION DOUCE ---
    self._apply_soft_repair(population, candidate_diameters)
    
    # ... (suite de l'algorithme : sélection, croisement, mutation)
```

---

### **Étape 3 : Créer le Test Unitaire**

**Explication :** Nous devons valider que notre fonction de réparation se comporte comme prévu sur un cas simple.

**Action :** Crée un nouveau fichier de test `tests/optimizer/test_repairs.py`.

```python
# --- Contenu du nouveau fichier tests/optimizer/test_repairs.py ---
import pytest
from src.lcpi.aep.optimization.repairs import soft_repair_solution

def test_soft_repair_increases_most_problematic_pipe():
    # Arrange
    diameters_map = {"P1": 110, "P2": 90, "P3": 110}
    # P2 a la plus grosse perte de charge, P3 la deuxième
    sim_metrics = {"headlosses_m": {"P1": 5.2, "P2": 15.8, "P3": 10.1}}
    candidate_diameters = [75, 90, 110, 125, 160]
    
    # Act: réparer 20% des conduites (donc la plus problématique, 1 conduite)
    repaired_map, changes = soft_repair_solution(
        diameters_map, sim_metrics, candidate_diameters, max_changes_fraction=0.20
    )
    
    # Assert
    assert changes["total_changes"] == 1
    assert changes["repaired_pipes"][0]["pipe_id"] == "P2"
    assert changes["repaired_pipes"][0]["from_dn_mm"] == 90
    assert changes["repaired_pipes"][0]["to_dn_mm"] == 110 # 1 cran de plus
    
    # Vérifier que les autres conduites n'ont pas changé
    assert repaired_map["P1"] == 110
    assert repaired_map["P3"] == 110
```

---

**Instruction Finale :**
Une fois que tu as créé le nouveau fichier `repairs.py`, modifié `genetic_algorithm.py` et créé le nouveau fichier de test, confirme que tout est en place. Nous lancerons ensuite la suite de tests pour valider cette phase.