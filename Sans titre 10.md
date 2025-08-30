
### **Prompt pour Cursor AI : Implémentation de la Phase 3**

Absolument. Votre rapport d'implémentation de la Phase 3 est parfait. Vous avez correctement identifié que la prochaine étape n'est pas de se précipiter sur la Phase 4, mais de **consolider, tester et instrumenter** ce qui vient d'être fait. C'est une marque de grande rigueur.

Voici les recommandations transformées en une série de prompts détaillés et actionnables pour une IA de codage. Je les ai regroupés logiquement pour maximiser l'efficacité.

---

### **Prompt 1 : Instrumentation Critique et Logging (La plus haute priorité)**

"Salut. Nous venons de terminer l'implémentation de la Phase 3 (Réparation Douce). Avant de continuer, nous devons ajouter une **instrumentation critique** pour rendre ce nouveau mécanisme observable et fiable.

Ta mission est de modifier la classe `GeneticOptimizer` et le module `repairs.py` pour ajouter un logging atomique et un système de snapshots.

**Fichiers à modifier :** `src/lcpi/aep/optimization/genetic_algorithm.py` et `src/lcpi/aep/optimization/repairs.py`.

---

### **Étape 1 : Améliorer les Retours de la Fonction de Réparation**

**Explication :** La fonction `soft_repair_solution` doit retourner des informations plus riches pour permettre un logging détaillé.

**Action :** Modifie la signature et le retour de la fonction `soft_repair_solution` dans `repairs.py`.

```python
# Dans src/lcpi/aep/optimization/repairs.py

# Modifie la fonction soft_repair_solution pour qu'elle ressemble à ceci :
def soft_repair_solution(
    # ... (arguments existants)
) -> Tuple[Optional[Dict[str, int]], Dict]: # Le premier retour peut être None si rien n'est fait

    # ... (logique existante)

    # Assure-toi que le dictionnaire 'changes_made' contient ces clés
    changes_made = {
        "repaired_pipes": [], # liste des changements détaillés
        "total_changes": 0,
        "selected_problematic_pipes": pipes_to_repair # Ajout : les conduites ciblées
    }
    # ...

    if changes_made["total_changes"] == 0:
        return None, changes_made # Retourne None si aucune réparation n'a été appliquée

    return new_diameters_map, changes_made```

---

### **Étape 2 : Implémenter le Logging Atomique et les Snapshots**

**Explication :** Nous allons modifier la méthode `_apply_soft_repair` pour qu'elle logue chaque étape du processus de réparation et sauvegarde un "snapshot" JSON de la solution avant/après pour un audit détaillé.

**Action :** Remplace la méthode `_apply_soft_repair` dans `genetic_algorithm.py` par cette version améliorée.

```python
# Dans la classe GeneticOptimizer de src/lcpi/aep/optimization/genetic_algorithm.py

def _apply_soft_repair(self, population: List, candidate_diameters: List[int], generation: int):
    # ... (paramètres de réparation existants)
    
    # ... (logique existante pour sélectionner les `candidates_for_repair`)

    for individual in candidates_for_repair:
        
        # --- LOGGING AVANT ---
        log_context = {
            "gen": generation, "ind_id": individual.id,
            "cost_before": individual.capex, 
            "violation_before": individual.metrics.get("violations", {}).get("total", -1)
        }
        self.logger.debug("REPAIR_ATTEMPT", extra=log_context)

        # --- SAUVEGARDE SNAPSHOT AVANT ---
        snapshot_dir = os.path.join(self.artifact_dir, "repairs")
        os.makedirs(snapshot_dir, exist_ok=True)
        snapshot_path_before = os.path.join(snapshot_dir, f"{generation}_{individual.id}_before.json")
        with open(snapshot_path_before, 'w') as f:
            # (Assure-toi d'avoir une méthode .to_dict() ou similaire sur ton objet Individual)
            json.dump(individual.to_dict(), f, indent=2)

        # --- TENTATIVE DE RÉPARATION ---
        repaired_diam_map, changes = soft_repair_solution(
            individual.diameters, individual.metrics, candidate_diameters
        )

        if not repaired_diam_map:
            continue

        repaired_capex = self.scorer.compute_capex(repaired_diam_map)
        
        # --- ÉVALUATION ET ACCEPTATION ---
        repaired_metrics = self.simulator.run(repaired_diam_map)
        repaired_violations = normalize_violations(repaired_metrics, self.constraints)

        # --- Critère d'acceptation strict ---
        violation_decrease = individual.metrics["violations"]["total"] - repaired_violations["total"]
        cost_increase_ratio = repaired_capex / individual.capex if individual.capex > 0 else float('inf')

        if violation_decrease > 1e-4 and cost_increase_ratio <= repair_max_cost_increase_ratio:
            # --- LOGGING APRÈS (SUCCÈS) ---
            log_context.update({
                "cost_after": repaired_capex,
                "violation_after": repaired_violations["total"],
                "pipes_changed": changes["total_changes"],
                "decision": "APPLIED"
            })
            self.logger.info("REPAIR_APPLIED", extra=log_context)
            
            # --- Mise à jour de l'individu et sauvegarde snapshot APRÈS ---
            # (Mettre à jour l'individu avec les nouvelles données)
            snapshot_path_after = os.path.join(snapshot_dir, f"{generation}_{individual.id}_after.json")
            with open(snapshot_path_after, 'w') as f:
                json.dump(individual.to_dict(), f, indent=2)
        else:
            # --- LOGGING APRÈS (ÉCHEC) ---
            log_context.update({
                "cost_after": repaired_capex,
                "violation_after": repaired_violations["total"],
                "decision": "ROLLED_BACK"
            })
            self.logger.debug("REPAIR_ROLLED_BACK", extra=log_context)
```

---

### **Étape 3 : Détection de l'Uniformisation des Diamètres**

**Explication :** Nous ajoutons un garde-fou pour détecter si la réparation rend toutes les conduites identiques, ce qui est un signe de comportement non désiré.

**Action :** Ajoute cette logique à la fin de la méthode `_apply_soft_repair`, juste avant de retourner.

```python
# Dans la méthode _apply_soft_repair de genetic_algorithm.py, à la fin

# --- Détection de l'uniformisation des diamètres ---
# (Cette logique doit être exécutée après la boucle de réparation, sur l'ensemble de la population)
all_repaired_diameters = [d for ind in population for d in ind.diameters.values()]
if len(set(all_repaired_diameters)) == 1:
    self.logger.warning(
        "REPAIR_AGGRESSIVE: La réparation a rendu tous les diamètres de la population uniformes. "
        "La réparation sera désactivée pour la prochaine génération."
    )
    # (Logique pour désactiver la réparation pour la génération n+1 à implémenter)
```

Une fois que tu as appliqué ces modifications, confirme que tout est en place."

---

### **Prompt 2 : Tests et Métriques (Recommandations Fortement Recommandées)**

"Salut. Continuons la consolidation de la Phase 3.

Ta mission est de renforcer nos tests d'intégration et d'ajouter des métriques de suivi pour la nouvelle fonctionnalité de réparation.

---

### **Étape 1 : Créer un Test d'Intégration End-to-End**

**Explication :** Nous allons créer un test qui lance deux petites optimisations complètes, une avec la réparation activée et une sans, puis compare les résultats pour valider son efficacité.

**Action :** Crée un nouveau fichier `tests/integration/test_soft_repair_integration.py`.

```python
# Dans tests/integration/test_soft_repair_integration.py
import pytest

@pytest.mark.slow
def test_ga_with_and_without_soft_repair():
    # --- Configuration ---
    inp_file = "path/to/small_network.inp"
    common_params = {"generations": 10, "population": 20}
    
    # --- Exécution SANS réparation ---
    results_no_repair = run_optimization_pipeline(
        inp_file, **common_params, repair_top_k=0 # Désactive la réparation
    )
    
    # --- Exécution AVEC réparation ---
    results_with_repair = run_optimization_pipeline(
        inp_file, **common_params, repair_top_k=3 # Active la réparation
    )

    # --- Assertions ---
    # 1. Vérifier que la réparation a bien été tentée
    assert results_with_repair["metrics"]["repair_attempts_total"] > 0
    assert results_no_repair["metrics"].get("repair_attempts_total", 0) == 0

    # 2. Vérifier que la faisabilité est meilleure (ou égale) avec la réparation
    feasibility_no_repair = results_no_repair["summary"]["feasible_solutions_ratio"]
    feasibility_with_repair = results_with_repair["summary"]["feasible_solutions_ratio"]
    assert feasibility_with_repair >= feasibility_no_repair

    # 3. Vérifier que le coût n'a pas explosé
    best_cost_no_repair = results_no_repair["best_solution"]["capex"]
    best_cost_with_repair = results_with_repair["best_solution"]["capex"]
    # Le coût peut être un peu plus élevé, c'est normal si la solution est meilleure
    assert best_cost_with_repair < best_cost_no_repair * 1.5 ```

---

### **Étape 2 : Ajouter les Métriques de Suivi**

**Explication :** Nous allons enrichir l'objet de résultat final avec des métriques spécifiques à la réparation pour pouvoir analyser ses performances.

**Action :** Dans `genetic_algorithm.py`, à la fin de la méthode `run()`, juste avant de retourner le résultat, ajoute la logique pour collecter et ajouter ces métriques.

```python
# Dans la méthode run() de GeneticOptimizer, à la fin

def _format_results(self, ...):
    # ... (logique de formatage existante)

    # --- Ajout des métriques de réparation ---
    final_metrics = result.get("metrics", {})
    final_metrics["repair_attempts_total"] = self.repair_stats.get("attempts", 0)
    final_metrics["repair_success_count"] = self.repair_stats.get("success", 0)
    # ... (autres métriques que tu auras collectées dans un dictionnaire self.repair_stats)
    
    result["metrics"] = final_metrics
    return result
```
Confirme lorsque ces modifications sont appliquées."


### **Prompt 3 : Finalisation et Robustification Avancée (Recommandations Fortement Recommandées)**

"Salut. Nous allons maintenant finaliser la consolidation de la Phase 3 en implémentant les dernières recommandations pour rendre notre mécanisme de réparation encore plus intelligent et contrôlable.

Ta mission est de modifier la classe `GeneticOptimizer` et potentiellement `repairs.py` pour ajouter un budget de réparation, un mode "dry-run" et des garde-fous sur la diversité.

---

### **Étape 1 : Ajout des Métriques de Suivi Détaillées**

**Explication :** Nous allons d'abord nous assurer de bien collecter les statistiques de réparation pour pouvoir les afficher.

**Action :** Dans la méthode `__init__` de la classe `GeneticOptimizer` (`genetic_algorithm.py`), initialise un dictionnaire pour les statistiques. Ensuite, modifie `_apply_soft_repair` pour mettre à jour ces statistiques.

```python
# --- Dans la classe GeneticOptimizer ---

# 1. Dans la méthode __init__
def __init__(self, ...):
    # ... (initialisation existante)
    self.repair_stats = {"attempts": 0, "success": 0, "cost_increase": 0.0}

# 2. Dans la méthode _apply_soft_repair, met à jour ce dictionnaire
def _apply_soft_repair(self, ...):
    # ...
    for individual in candidates_for_repair:
        self.repair_stats["attempts"] += 1
        # ...
        if violation_decrease > 1e-4 and cost_increase_ratio <= repair_max_cost_increase_ratio:
            self.repair_stats["success"] += 1
            self.repair_stats["cost_increase"] += (repaired_capex - individual.capex)
            # ... (mise à jour de l'individu)
    # ...

# 3. Dans la méthode _format_results (ou équivalent)
def _format_results(self, ...):
    # ...
    final_metrics = result.get("metrics", {})
    final_metrics["repair_attempts_total"] = self.repair_stats.get("attempts", 0)
    final_metrics["repair_success_count"] = self.repair_stats.get("success", 0)
    avg_cost_increase = (self.repair_stats["cost_increase"] / self.repair_stats["success"]) if self.repair_stats["success"] > 0 else 0
    final_metrics["repair_avg_cost_increase"] = avg_cost_increase
    result["metrics"] = final_metrics
    return result
```

---

### **Étape 2 : Implémentation du Mode "Dry Run"**

**Explication :** Nous allons ajouter un flag qui permet de simuler les réparations et de logger les résultats sans réellement modifier les individus. C'est un outil de débogage très puissant pour régler les paramètres de réparation.

**Action :** Modifie la méthode `_apply_soft_repair` dans `genetic_algorithm.py`.

```python
# --- Dans la classe GeneticOptimizer ---

def _apply_soft_repair(self, population: List, candidate_diameters: List[int], generation: int):
    # --- Ajout du paramètre "dry_run" ---
    is_dry_run = self.algo_params.get("repair_dry_run", False)
    if is_dry_run:
        self.logger.info("Réparation en mode DRY-RUN. Les changements ne seront pas appliqués.")
    
    # ... (logique existante) ...
    
    for individual in candidates_for_repair:
        # ... (logique existante) ...

        if violation_decrease > 1e-4 and cost_increase_ratio <= repair_max_cost_increase_ratio:
            # --- Condition pour appliquer ou non le changement ---
            if not is_dry_run:
                # C'est seulement ici qu'on modifie l'individu
                self.logger.info("Réparation APPLIQUÉE sur individu...")
                # ... (code existant pour mettre à jour l'individu et sauvegarder le snapshot)
            else:
                self.logger.info("Réparation (DRY-RUN) : Le changement aurait été appliqué.")
        else:
            # ... (log existant pour REPAIR_ROLLED_BACK)
```

**Action complémentaire :** Ajoute le flag `--repair-dry-run` à ta CLI pour pouvoir activer ce mode.

---

### **Étape 3 : Implémentation du Budget de Réparation Global**

**Explication :** Pour éviter que le mécanisme de réparation ne fasse dériver le coût total sur l'ensemble du run, nous allons introduire un "budget" total de modifications autorisées.

**Action :** Modifie `__init__` et `_apply_soft_repair` dans `genetic_algorithm.py`.

```python
# --- Dans la classe GeneticOptimizer ---

# 1. Dans la méthode __init__
def __init__(self, ...):
    # ...
    max_total_repairs = self.algo_params.get("repair_budget", -1) # -1 pour infini
    self.repair_stats = {..., "total_pipes_changed": 0, "budget": max_total_repairs}

# 2. Dans la méthode _apply_soft_repair
def _apply_soft_repair(self, ...):
    # ...
    for individual in candidates_for_repair:
        # --- Vérification du budget AVANT la réparation ---
        if self.repair_stats["budget"] != -1 and self.repair_stats["total_pipes_changed"] >= self.repair_stats["budget"]:
            if generation % 10 == 0: # Loguer de temps en temps pour ne pas spammer
                 self.logger.info("Budget de réparation atteint. Aucune nouvelle réparation ne sera tentée.")
            break # Sortir de la boucle et ne plus réparer
            
        # ... (logique de réparation existante) ...

        if violation_decrease > 1e-4 and cost_increase_ratio <= repair_max_cost_increase_ratio:
            # ...
            if not is_dry_run:
                # --- Mettre à jour le compteur du budget ---
                self.repair_stats["total_pipes_changed"] += changes["total_changes"]
                # ... (mettre à jour l'individu)
```

**Action complémentaire :** Ajoute le flag `--repair-budget` à ta CLI.

---

### **Étape 4 : Garde-fou sur la Diversité (Simplifié)**

**Explication :** Implémenter une vraie mesure de diversité est complexe. Nous allons utiliser un proxy simple : on vérifie que le nombre de diamètres uniques dans la population ne chute pas drastiquement après une session de réparation.

**Action :** Ajoute cette vérification à la fin de `_apply_soft_repair`.

```python
# Dans la méthode _apply_soft_repair, à la fin, après la boucle

def _apply_soft_repair(self, ...):
    
    # --- Mesure de la diversité AVANT ---
    diameters_before_repair = [d for ind in population for d in ind.diameters.values()]
    diversity_before = len(set(diameters_before_repair))
    
    # --- Boucle de réparation (déjà existante) ---
    for individual in candidates_for_repair:
        # ...
    
    # --- Mesure de la diversité APRÈS ---
    diameters_after_repair = [d for ind in population for d in ind.diameters.values()]
    diversity_after = len(set(diameters_after_repair))

    # --- Garde-fou ---
    if diversity_after < diversity_before * 0.5: # Si on a perdu plus de 50% de la diversité
        self.logger.warning(
            f"REPAIR_DIVERSITY_LOSS: La réparation a réduit significativement la diversité des diamètres "
            f"(de {diversity_before} à {diversity_after} diamètres uniques). "
            "Il est recommandé de vérifier les paramètres de réparation."
        )
```

---

**Instruction Finale :**
Une fois que tu as appliqué ces modifications, confirme que tout est en place. Ces ajouts rendent notre mécanisme de réparation beaucoup plus contrôlable et robuste, prêt pour des analyses et un tuning fins."