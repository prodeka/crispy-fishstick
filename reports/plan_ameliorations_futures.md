# Plan d'Améliorations Futures - LCPI Hardy-Cross

**Date :** 28 Août 2025  
**Auteur :** Assistant IA  
**Basé sur :** Évaluation détaillée de l'implémentation  

---

## 🎯 **Objectif Principal**

Améliorer la capacité de LCPI à trouver des **solutions faisables** tout en maintenant son efficacité économique, afin de permettre une comparaison équitable avec EPANET.

---

## 📋 **Priorités d'Amélioration**

### 🔥 **Priorité Haute : Amélioration de la Faisabilité**

#### 1. **Renforcement de la Fonction d'Évaluation (Fitness)**
- **Problème** : LCPI trouve des solutions économiques mais non faisables
- **Solution** : Renforcer les pénalités pour violations de contraintes
- **Actions** :
  - Augmenter les poids de pénalité pour pression insuffisante
  - Implémenter des pénalités progressives (plus fortes avec les générations)
  - Ajouter des pénalités spécifiques pour solutions non faisables
- **Fichiers à modifier** : `src/lcpi/aep/optimization/genetic_algorithm.py`

#### 2. **Paramètres d'Optimisation Optimisés**
- **Problème** : Paramètres actuels insuffisants pour explorer l'espace de solutions
- **Solution** : Augmenter les paramètres d'exploration
- **Actions** :
  - Générations : 30-50 (au lieu de 15)
  - Population : 50-100 (au lieu de 25)
  - Ajuster les taux de mutation et croisement
- **Fichiers à modifier** : Scripts de test et CLI

#### 3. **Harmonisation Précise des Contraintes**
- **Problème** : Différences dans l'application des contraintes
- **Solution** : Alignement parfait des contraintes avec EPANET
- **Actions** :
  - Vérifier les unités (m vs mCE)
  - Harmoniser les seuils de pression et vitesse
  - Implémenter la même logique de tolérance
- **Fichiers à modifier** : `src/lcpi/aep/optimizer/constraints_handler.py`

### 🔶 **Priorité Moyenne : Exploration de l'Espace de Solutions**

#### 4. **Gestion des Grands Diamètres**
- **Problème** : LCPI évite les grands diamètres coûteux
- **Question** : Est-ce optimal ou manque d'exploration ?
- **Actions** :
  - Analyser si l'évitement est justifié
  - Forcer l'exploration des grands diamètres si nécessaire
  - Vérifier les prix dans la base de données
- **Fichiers à modifier** : Algorithme génétique et base de données

#### 5. **Opérateurs Génétiques Spécialisés**
- **Problème** : Opérateurs génériques peu adaptés au problème
- **Solution** : Opérateurs spécialisés pour les réseaux hydrauliques
- **Actions** :
  - Mutation intelligente préservant la faisabilité
  - Croisement adapté aux contraintes hydrauliques
  - Mécanismes de diversification
- **Fichiers à modifier** : `src/lcpi/aep/optimization/genetic_algorithm.py`

### 🔵 **Priorité Basse : Documentation et Validation**

#### 6. **Transparence Mathématique**
- **Problème** : Manque de visibilité sur la convergence Hardy-Cross
- **Solution** : Améliorer la traçabilité
- **Actions** :
  - Afficher les détails itératifs avec `--verbose`
  - Tracer la convergence des débits
  - Logger les ajustements de pression
- **Fichiers à modifier** : `src/lcpi/aep/solver/hardy_cross.py`

#### 7. **Documentation Complète**
- **Problème** : Manque de documentation des améliorations
- **Solution** : Documentation détaillée
- **Actions** :
  - Documenter les scripts d'analyse
  - Expliquer les changements apportés
  - Guide d'utilisation des nouveaux outils
- **Fichiers à créer** : Documentation dans `/docs/`

---

## 🛠️ **Outils Créés pour les Améliorations**

### Scripts d'Analyse
1. **`tools/analyze_fitness_function.py`** - Analyse de la fonction d'évaluation
2. **`tools/harmonize_hydraulic_constraints.py`** - Harmonisation des contraintes
3. **`tools/cleanup_test_files.py`** - Nettoyage des fichiers temporaires

### Scripts de Test
1. **`tests/test_harmonized_constraints.py`** - Tests avec contraintes harmonisées

### Rapports
1. **`reports/rapport_final_analyse_ecart_cout.md`** - Analyse complète
2. **`reports/synthese_travail_effectue.md`** - Synthèse du travail
3. **`reports/plan_ameliorations_futures.md`** - Ce plan

---

## 📊 **Métriques de Succès**

### Objectifs Quantitatifs
- **Faisabilité LCPI** : ≥90% de solutions faisables
- **Écart de coût** : Réduction à <20% (solutions faisables)
- **Temps d'exécution** : Maintenir <5 minutes par optimisation

### Objectifs Qualitatifs
- **Cohérence** : Même logique de contraintes qu'EPANET
- **Robustesse** : Solutions stables et reproductibles
- **Transparence** : Visibilité complète sur le processus

---

## 🚀 **Plan d'Exécution**

### Phase 1 : Amélioration de la Faisabilité (1-2 semaines)
1. **Semaine 1** :
   - Renforcer les pénalités dans la fonction d'évaluation
   - Tester avec paramètres optimisés
   - Analyser les résultats

2. **Semaine 2** :
   - Harmoniser les contraintes avec EPANET
   - Valider la cohérence des résultats
   - Documenter les améliorations

### Phase 2 : Optimisation Avancée (2-3 semaines)
3. **Semaine 3** :
   - Implémenter des opérateurs génétiques spécialisés
   - Analyser l'utilisation des grands diamètres
   - Optimiser les paramètres d'exploration

4. **Semaine 4-5** :
   - Améliorer la transparence mathématique
   - Finaliser la documentation
   - Tests de validation complets

### Phase 3 : Validation et Documentation (1 semaine)
5. **Semaine 6** :
   - Tests sur plusieurs réseaux
   - Comparaison finale avec EPANET
   - Documentation complète

---

## 🔧 **Modifications Techniques Détaillées**

### 1. **Renforcement des Pénalités**
```python
# Dans genetic_algorithm.py
def _calculate_adaptive_penalties(self, individu, sim_result):
    # Pénalité plus forte pour échec de simulation
    if not sim_result.get("success"):
        return 1e8  # Augmenter de 1e6 à 1e8
    
    # Pénalité pression plus forte
    if p_min < p_req:
        deficit = p_req - p_min
        penal += weight * 0.2 * deficit * 1000  # Augmenter de 0.1 à 0.2
    
    # Pénalité vitesse plus forte
    if vmax_obs > v_max_req:
        excess = vmax_obs - v_max_req
        penal += weight * 0.1 * excess * 1000  # Augmenter de 0.05 à 0.1
```

### 2. **Paramètres d'Optimisation Optimisés**
```python
# Paramètres recommandés
generations = 40  # Au lieu de 15
population = 75   # Au lieu de 25
mutation_rate = 0.15  # Augmenter l'exploration
crossover_rate = 0.8  # Maintenir la diversité
```

### 3. **Harmonisation des Contraintes**
```python
# Dans constraints_handler.py
def apply_constraints(solution, constraints, mode="soft"):
    # Utiliser exactement les mêmes seuils qu'EPANET
    pmin_req = constraints.get("pressure_min_m", 15.0)
    vmax_req = constraints.get("velocity_max_m_s", 2.0)
    vmin_req = constraints.get("velocity_min_m_s", 0.5)
    
    # Même logique de tolérance
    tolerance_ratio = 0.05  # 5% de tolérance
```

---

## 📈 **Suivi et Évaluation**

### Métriques de Suivi
- **Taux de faisabilité** : % de solutions respectant les contraintes
- **Écart de coût** : Différence relative avec EPANET
- **Temps d'exécution** : Durée des optimisations
- **Convergence** : Nombre de générations nécessaires

### Points de Contrôle
- **Fin Semaine 1** : Vérifier l'amélioration de la faisabilité
- **Fin Semaine 2** : Valider l'harmonisation des contraintes
- **Fin Semaine 3** : Évaluer l'impact des opérateurs spécialisés
- **Fin Semaine 6** : Validation finale et documentation

---

## 🎯 **Conclusion**

Ce plan d'améliorations vise à transformer LCPI en un solveur robuste et fiable, capable de générer systématiquement des solutions faisables tout en maintenant son avantage économique. L'objectif final est d'obtenir une comparaison équitable et significative avec EPANET.

**Prochaine étape immédiate** : Exécuter `tools/analyze_fitness_function.py` pour analyser la fonction d'évaluation actuelle et identifier les points d'amélioration prioritaires.

---

**Document généré le 28/08/2025**  
**Basé sur l'évaluation détaillée de l'implémentation**  
**Encodage UTF-8 pour compatibilité complète**
