### **Prompt pour Cursor AI : Implémentation de la Phase 2**

"Salut. Je démarre une nouvelle session de travail sur mon projet LCPI.

**Contexte :**
Nous avons terminé la Phase 1. La classe `PriceDB` est maintenant la source de vérité unique pour les diamètres et les prix, et elle est correctement intégrée dans tout le pipeline d'optimisation (contrôleur, algorithmes, scoring).

**Ta mission :**
Tu vas maintenant implémenter la **Phase 2 : Pénalité adaptative non linéaire et normalisation des violations**. L'objectif est de remplacer le système de pénalité actuel, probablement trop simple, par un mécanisme plus sophistiqué qui punit les solutions en fonction de la *sévérité* de leurs violations et de l'avancement de l'optimisation.

---

### **Étape 1 : Créer le Module de Gestion des Contraintes**

**Explication :** Nous allons centraliser toute la logique liée aux contraintes dans un nouveau fichier. Cela inclut la normalisation des violations (pour avoir un score de "violation" comparable entre pression et vitesse) et la fonction de pénalité adaptative elle-même.

**Action :** Crée un nouveau fichier `src/lcpi/aep/optimization/constraints_handler.py` et insère-y le contenu suivant.

```python
# --- Contenu du nouveau fichier src/lcpi/aep/optimization/constraints_handler.py ---

from typing import Dict, Any

def normalize_violations(sim_metrics: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcule un score de violation normalisé pour la pression et la vitesse.
    Un ratio > 0 indique une violation.
    
    Retourne un dictionnaire détaillé avec les ratios de violation et un total pondéré.
    """
    # Pression
    pressure_req_m = float(constraints.get("pressure_min_m", 10.0))
    min_pressure_obs_m = float(sim_metrics.get("min_pressure_m", 0.0) or 0.0)
    
    # Ratio = (Requis - Observé) / Requis. Uniquement si violation.
    pressure_violation_ratio = max(0.0, (pressure_req_m - min_pressure_obs_m) / max(1.0, pressure_req_m))

    # Vitesse
    velocity_max_ms = float(constraints.get("velocity_max_m_s", 2.0))
    max_velocity_obs_ms = float(sim_metrics.get("max_velocity_m_s", 0.0) or 0.0)
    
    # Ratio = (Observé - Max) / Max. Uniquement si violation.
    velocity_violation_ratio = max(0.0, (max_velocity_obs_ms - velocity_max_ms) / max(1.0, velocity_max_ms))
    
    # Score total pondéré (plus de poids sur la pression, qui est souvent plus critique)
    total_violation = (pressure_violation_ratio * 0.6) + (velocity_violation_ratio * 0.4)
    
    return {
        "pressure_ratio": pressure_violation_ratio,
        "velocity_ratio": velocity_violation_ratio,
        "total": total_violation
    }

def adaptive_penalty(
    violation_total: float,
    generation: int,
    total_generations: int,
    alpha_start: float = 1e5,
    alpha_max: float = 1e8,
    beta: float = 1.8
) -> Dict[str, float]:
    """
    Calcule une pénalité non linéaire et adaptative.
    
    - 'alpha' est le poids de la pénalité, il augmente avec les générations.
    - 'beta' (>1) est l'exposant non linéaire, qui punit sévèrement les grosses violations.
    """
    if violation_total <= 1e-6:  # Tolérance pour les erreurs de virgule flottante
        return {"penalty": 0.0, "alpha": 0.0, "beta": beta}
    
    # Progression de l'optimisation (de 0.0 à 1.0)
    progress_t = float(generation) / max(1, total_generations - 1)
    
    # Alpha augmente de manière linéaire au cours des générations
    alpha = min(alpha_start * (1 + 9 * progress_t), alpha_max)
    
    penalty = alpha * (violation_total ** beta)
    
    return {"value": penalty, "alpha": alpha, "beta": beta}
```

---

### **Étape 2 : Intégrer la Nouvelle Logique dans l'Algorithme Génétique**

**Explication :** Maintenant, nous allons modifier la classe `GeneticOptimizer` pour qu'elle utilise ces nouvelles fonctions. La méthode qui évalue chaque solution (`evaluer_fitness`) va être mise à jour pour :
1.  Appeler `normalize_violations`.
2.  Appeler `adaptive_penalty` avec le score de violation total.
3.  Calculer le score final en combinant le CAPEX et la pénalité.
4.  Stocker les informations détaillées sur la violation et la pénalité dans l'objet "individu" pour un meilleur logging et reporting.

**Action :** Ouvre le fichier `src/lcpi/aep/optimization/genetic_algorithm.py` et modifie la méthode d'évaluation (elle peut s'appeler `_evaluate_individual`, `evaluer_fitness` ou similaire).

```python
# --- Imports à ajouter en haut de genetic_algorithm.py ---
from .constraints_handler import normalize_violations, adaptive_penalty

# --- Logique à intégrer dans la méthode d'évaluation de la classe GeneticOptimizer ---

# Supposons que la méthode ressemble à ceci :
# def _evaluate_individual(self, individual, generation, total_generations):

    # ... (le code qui simule le réseau et calcule le CAPEX existe déjà)
    # simulation_metrics = self.simulator.run(individual.diameters)
    # capex = self.scorer.compute_capex(individual.diameters)

    # 1. Normaliser les violations
    violation_info = normalize_violations(simulation_metrics, self.constraints)
    
    # 2. Calculer la pénalité adaptative
    penalty_info = adaptive_penalty(
        violation_total=violation_info["total"],
        generation=generation,
        total_generations=total_generations,
        # Ces paramètres devraient venir de la configuration de l'AG
        alpha_start=self.algo_params.get("penalty_alpha_start", 1e5),
        alpha_max=self.algo_params.get("penalty_alpha_max", 1e8),
        beta=self.algo_params.get("penalty_beta", 1.8)
    )
    
    # 3. Calculer le score final et la fitness
    final_score = capex + penalty_info["value"]
    # La fitness est souvent l'inverse du score pour les problèmes de minimisation
    fitness = 1.0 / (1.0 + final_score) 

    # 4. Stocker les métriques détaillées pour l'analyse
    individual.capex = capex
    individual.fitness = fitness
    individual.score = final_score
    individual.is_feasible = violation_info["total"] <= 1e-6
    individual.metrics["violations"] = violation_info
    individual.metrics["penalty"] = penalty_info
    
    # return individual (ou ce que la méthode est censée retourner)
```

---

### **Étape 3 : Créer les Tests Unitaires**

**Explication :** Nous devons valider que nos nouvelles fonctions se comportent comme attendu.

**Action :** Crée un nouveau fichier de test `tests/optimizer/test_constraints_handler.py`.

```python
# --- Contenu du nouveau fichier tests/optimizer/test_constraints_handler.py ---
import pytest
from src.lcpi.aep.optimization.constraints_handler import normalize_violations, adaptive_penalty

def test_normalize_violations_no_violation():
    metrics = {"min_pressure_m": 15.0, "max_velocity_m_s": 1.5}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    assert violations["total"] == 0.0
    assert violations["pressure_ratio"] == 0.0
    assert violations["velocity_ratio"] == 0.0

def test_normalize_violations_pressure_violation():
    metrics = {"min_pressure_m": 8.0, "max_velocity_m_s": 1.5}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    # (10 - 8) / 10 = 0.2. Pondéré par 0.6 -> 0.12
    assert violations["pressure_ratio"] == pytest.approx(0.2)
    assert violations["velocity_ratio"] == 0.0
    assert violations["total"] == pytest.approx(0.12)

def test_adaptive_penalty_increases_with_generation():
    violation = 0.1
    total_gen = 100
    penalty_start = adaptive_penalty(violation, 0, total_gen)
    penalty_mid = adaptive_penalty(violation, 50, total_gen)
    penalty_end = adaptive_penalty(violation, 99, total_gen)
    
    assert penalty_start["value"] < penalty_mid["value"] < penalty_end["value"]
    assert penalty_start["alpha"] < penalty_mid["alpha"]

def test_adaptive_penalty_is_nonlinear():
    violation_small = 0.1
    violation_large = 0.2 # 2x plus grande
    penalty_small = adaptive_penalty(violation_small, 10, 100)
    penalty_large = adaptive_penalty(violation_large, 10, 100)
    
    # La pénalité doit être plus que 2x plus grande car beta > 1
    assert penalty_large["value"] > penalty_small["value"] * 2
```

---

**Instruction Finale :**
Une fois que tu as créé le nouveau fichier `constraints_handler.py`, modifié `genetic_algorithm.py` et créé le nouveau fichier de test, confirme que tout est en place. Nous lancerons ensuite la suite de tests pour valider cette phase.