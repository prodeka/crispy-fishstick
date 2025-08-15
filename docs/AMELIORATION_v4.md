# AMELIORATION_v4 - Feuille de Route Phases 2 & 3

## 📋 **Contexte**

Ce document définit la feuille de route pour les **Phases 2 & 3** de l'amélioration du module AEP, en se basant sur les acquis de la **Phase 1** (commandes unifiées) déjà implémentée.

**Note importante** : Les métadonnées (projet, auteur, version, etc.) sont déjà gérées par `lcpi init` et ne sont donc pas incluses dans ce document.

---

## 🎯 **PHASE 2 : INTÉGRATION RÉSEAU COMPLET**

### **Objectif**
Créer des commandes unifiées pour l'analyse de réseaux complets avec intégration EPANET et Hardy-Cross.

### **1) Commandes à Implémenter**

#### **`network-complete-unified`**
```bash
lcpi aep network-complete-unified --input reseau.yml --mode enhanced --export json
```

**Fonctionnalités :**
- Analyse complète du réseau (connectivité, boucles, diamètres)
- Intégration Hardy-Cross pour calcul de débits
- Validation EPANET (génération fichier .inp)
- Post-traitement (vérifications, coup de bélier)

#### **`epanet-unified`**
```bash
lcpi aep epanet-unified --input reseau.yml --duration 24 --timestep 60 --export inp
```

**Fonctionnalités :**
- Génération automatique de fichiers EPANET .inp
- Exécution EPANET via pyswmm
- Analyse des résultats (pressions, vitesses, débits)
- Comparaison avec calculs manuels

### **2) Schéma YAML Réseau Complet**

```yaml
reseau_complet:
  nom: "Réseau Principal"
  type: "maillé"  # ou "ramifié"
  noeuds:
    N1:
      role: "reservoir"
      cote_m: 150.0
      demande_m3_s: 0.0
      pression_min_mce: 20
      pression_max_mce: 80
    N2:
      role: "consommation"
      cote_m: 145.0
      demande_m3_s: 0.02
      profil_consommation: "residential"
    N3:
      role: "consommation"
      cote_m: 140.0
      demande_m3_s: 0.015
      profil_consommation: "commercial"
  
  conduites:
    C1:
      noeud_amont: "N1"
      noeud_aval: "N2"
      longueur_m: 500
      diametre_m: 0.2
      rugosite: 100
      materiau: "acier"
      statut: "existant"
      coefficient_frottement: "hazen_williams"
    C2:
      noeud_amont: "N2"
      noeud_aval: "N3"
      longueur_m: 300
      diametre_m: 0.15
      rugosite: 120
      materiau: "pvc"
      statut: "nouveau"
      coefficient_frottement: "hazen_williams"
  
  boucles:  # optionnel, détection automatique si absent
    L1: ["C1", "C2", "C3", "C4"]

hardy_cross:
  tolerance: 1e-6
  max_iterations: 200
  methode: "hazen_williams"  # ou "darcy_weisbach"
  convergence_criteria: "debit"  # ou "pression"

epanet:
  run_options:
    duration_h: 24
    timestep_min: 60
    start_time: "00:00"
    quality_type: "none"  # ou "chemical", "age", "trace"
  output_options:
    save_hydraulics: true
    save_quality: false
    save_energy: true

post_traitement:
  verifications:
    vitesse_min_m_s: 0.5
    vitesse_max_m_s: 2.5
    pression_min_mce: 20
    pression_max_mce: 80
    diametre_min_mm: 50
    diametre_max_mm: 1000
  
  coup_belier:
    analyse: true
    celerite_m_s: 1200
    temps_fermeture_s: 2.0
    methode: "approximative"  # ou "detaillee"
  
  optimisation:
    diametres_commerciaux_mm: [50, 63, 75, 90, 110, 125, 140, 160, 200, 250, 300, 350, 400]
    critere_optimisation: "cout"  # ou "energie", "performance"
    contraintes:
      cout_max_euros: 100000
      energie_max_kwh: 5000

scenarios:
  base:
    description: "Scénario de référence"
    facteurs:
      population: 1.0
      consommation: 1.0
      fuites: 0.10
  
  urbain_2030:
    description: "Scénario urbain 2030"
    facteurs:
      population: 1.2
      consommation: 1.1
      fuites: 0.08
  
  rural_2050:
    description: "Scénario rural 2050"
    facteurs:
      population: 1.5
      consommation: 0.9
      fuites: 0.15
```

### **3) Formules Clés à Implémenter**

#### **Hardy-Cross (Correction de Boucle)**
```
ΔQ = -Σ(hi/ri) / Σ((2Qi hi')/ri)
```
Où :
- `hi` = perte de charge dans la conduite i
- `ri` = résistance hydraulique de la conduite i
- `Qi` = débit initial dans la conduite i
- `hi'` = dérivée de la perte de charge par rapport au débit

#### **Hazen-Williams**
```
S = 10.67 × (Q^1.852) / (C^1.852 × D^4.87)
hf = S × L
```
Où :
- `S` = pente hydraulique (m/m)
- `Q` = débit (m³/s)
- `C` = coefficient de Hazen-Williams
- `D` = diamètre (m)
- `L` = longueur (m)

#### **Darcy-Weisbach**
```
hf = f × (L/D) × (V²/2g)
```
Où :
- `f` = facteur de frottement (via Colebrook)
- `V` = vitesse (m/s)
- `g` = accélération gravitationnelle (9.81 m/s²)

#### **Coup de Bélier (Approximation)**
```
ΔPmax ≈ ρ × c × ΔV
```
Où :
- `ρ` = masse volumique de l'eau (1000 kg/m³)
- `c` = célérité de l'onde (1200 m/s typique)
- `ΔV` = variation de vitesse (m/s)

### **4) Contrat de Sortie Canonical**

```json
{
  "inputs": {
    "reseau_complet": { /* données d'entrée validées */ },
    "hardy_cross": { /* paramètres Hardy-Cross */ },
    "epanet": { /* paramètres EPANET */ }
  },
  "diagnostics": {
    "connectivite_ok": true,
    "composants_isoles": [],
    "boucles_detectees": 3,
    "epanet_compatible": true,
    "validation_passed": true
  },
  "hardy_cross": {
    "convergence": {
      "converge": true,
      "iterations": 12,
      "tolerance_atteinte": 1e-7,
      "temps_calcul_s": 0.15
    },
    "resultats": {
      "debits_finaux": { /* débits par conduite */ },
      "pertes_charge": { /* pertes par conduite */ },
      "pressions_noeuds": { /* pressions par nœud */ }
    }
  },
  "epanet": {
    "fichier_generer": "reseau.inp",
    "execution": {
      "succes": true,
      "erreurs": [],
      "avertissements": []
    },
    "resultats": {
      "pressions": { /* pressions par nœud et par heure */ },
      "debits": { /* débits par conduite et par heure */ },
      "vitesses": { /* vitesses par conduite et par heure */ },
      "energie": { /* consommation énergétique */ }
    }
  },
  "post_traitement": {
    "verifications": {
      "vitesse_ok": true,
      "pression_ok": true,
      "diametre_ok": true,
      "violations": []
    },
    "coup_belier": {
      "pression_max_mce": 85.2,
      "pression_min_mce": 18.5,
      "risque_elevation": false
    },
    "optimisation": {
      "diametres_recommandes": [
        { "conduite": "C1", "diametre_mm": 200, "cout_euros": 15000 },
        { "conduite": "C2", "diametre_mm": 160, "cout_euros": 12000 }
      ],
      "cout_total_euros": 27000,
      "energie_totale_kwh": 2450
    }
  },
  "scenarios": {
    "base": { /* résultats scénario de référence */ },
    "urbain_2030": { /* résultats scénario urbain */ },
    "rural_2050": { /* résultats scénario rural */ }
  },
  "valeurs": {
    "debit_total_m3_s": 0.035,
    "longueur_totale_m": 800,
    "cout_total_euros": 27000,
    "energie_totale_kwh": 2450,
    "performance_globale": 0.92
  }
}
```

---

## 🚀 **PHASE 3 : OPTIMISATION ET ANALYSE AVANCÉE**

### **Objectif**
Implémenter des fonctionnalités d'optimisation avancée et d'analyse de sensibilité.

### **1) Commandes à Implémenter**

#### **`network-optimize-unified`**
```bash
lcpi aep network-optimize-unified --input reseau.yml --criteria cost --constraints budget.yml --export json
```

**Fonctionnalités :**
- Optimisation multi-critères (coût, énergie, performance)
- Algorithmes génétiques pour sélection de diamètres
- Contraintes techniques et budgétaires
- Analyse de sensibilité

#### **`network-sensitivity-unified`**
```bash
lcpi aep network-sensitivity-unified --input reseau.yml --parameters rugosite,demande --variation 0.2 --export html
```

**Fonctionnalités :**
- Analyse de sensibilité des paramètres clés
- Graphiques interactifs (HTML)
- Identification des paramètres critiques
- Recommandations de robustesse

#### **`network-compare-unified`**
```bash
lcpi aep network-compare-unified --input reseau1.yml reseau2.yml --criteria performance,cost --export xlsx
```

**Fonctionnalités :**
- Comparaison de variantes de réseau
- Tableaux comparatifs détaillés
- Graphiques de comparaison
- Recommandations de choix

### **2) Schéma YAML Optimisation**

```yaml
optimisation:
  criteres:
    principal: "cout"  # ou "energie", "performance", "robustesse"
    secondaires: ["energie", "performance"]
    poids: [0.6, 0.25, 0.15]
  
  contraintes:
    budget:
      cout_max_euros: 100000
      cout_annuel_max_euros: 5000
    techniques:
      pression_min_mce: 20
      pression_max_mce: 80
      vitesse_min_m_s: 0.5
      vitesse_max_m_s: 2.5
    operationnelles:
      maintenance_facilite: true
      extension_future: true
  
  algorithmes:
    type: "genetique"  # ou "gradient", "monte_carlo"
    parametres:
      population_size: 100
      generations: 50
      mutation_rate: 0.1
      crossover_rate: 0.8
  
  diametres_candidats:
    commerciaux: [50, 63, 75, 90, 110, 125, 140, 160, 200, 250, 300, 350, 400]
    couts_euros_m: [15, 20, 25, 35, 45, 60, 80, 100, 150, 250, 350, 500, 700]
    disponibilite: [0.95, 0.95, 0.95, 0.90, 0.90, 0.85, 0.85, 0.80, 0.80, 0.75, 0.70, 0.65, 0.60]

analyse_sensibilite:
  parametres:
    rugosite:
      variation: 0.2  # ±20%
      pas: 0.05
    demande:
      variation: 0.3  # ±30%
      pas: 0.1
    cote_terrain:
      variation: 0.1  # ±10%
      pas: 0.02
  
  sorties:
    pressions: true
    vitesses: true
    couts: true
    energie: true
  
  methodes:
    - "monte_carlo"
    - "one_at_a_time"
    - "sobol_indices"

comparaison:
  variantes:
    reseau_base:
      fichier: "reseau_base.yml"
      description: "Réseau de référence"
    reseau_optimise:
      fichier: "reseau_optimise.yml"
      description: "Réseau optimisé pour coût"
    reseau_robuste:
      fichier: "reseau_robuste.yml"
      description: "Réseau optimisé pour robustesse"
  
  criteres:
    - "performance_hydraulique"
    - "cout_investissement"
    - "cout_exploitation"
    - "robustesse"
    - "maintenabilite"
    - "extensibilite"
  
  horizon_temps:
    - "court_terme"  # 5 ans
    - "moyen_terme"  # 15 ans
    - "long_terme"   # 30 ans
```

### **3) Algorithmes d'Optimisation**

#### **Algorithme Génétique**
```python
def optimize_genetic(network, criteria, constraints, generations=50):
    """
    Optimisation par algorithme génétique
    """
    # 1. Initialisation de la population
    population = generate_initial_population(network, size=100)
    
    # 2. Évaluation de la fitness
    for generation in range(generations):
        fitness_scores = evaluate_population(population, criteria)
        
        # 3. Sélection
        parents = select_parents(population, fitness_scores)
        
        # 4. Croisement
        offspring = crossover(parents)
        
        # 5. Mutation
        offspring = mutate(offspring, rate=0.1)
        
        # 6. Remplacement
        population = replace_population(population, offspring)
    
    return best_solution(population)
```

#### **Analyse de Sensibilité (Indices de Sobol)**
```python
def sobol_analysis(network, parameters, outputs, samples=1000):
    """
    Analyse de sensibilité par indices de Sobol
    """
    # 1. Génération des échantillons
    A = generate_samples(parameters, samples)
    B = generate_samples(parameters, samples)
    
    # 2. Évaluation des modèles
    YA = evaluate_model(network, A)
    YB = evaluate_model(network, B)
    
    # 3. Calcul des indices
    Si = calculate_first_order_indices(YA, YB)
    STi = calculate_total_order_indices(YA, YB)
    
    return {"first_order": Si, "total_order": STi}
```

### **4) Contrat de Sortie Optimisation**

```json
{
  "optimisation": {
    "algorithme": "genetique",
    "convergence": {
      "iterations": 45,
      "fitness_finale": 0.92,
      "temps_calcul_s": 125.3
    },
    "meilleure_solution": {
      "diametres": {
        "C1": 200,
        "C2": 160,
        "C3": 125
      },
      "performance": {
        "cout_total_euros": 85000,
        "energie_totale_kwh": 3200,
        "performance_hydraulique": 0.95
      }
    },
    "pareto_front": [
      /* solutions non-dominées */
    ]
  },
  "analyse_sensibilite": {
    "parametres_critiques": [
      {
        "parametre": "rugosite",
        "indice_sobol": 0.45,
        "impact": "eleve"
      },
      {
        "parametre": "demande",
        "indice_sobol": 0.32,
        "impact": "moyen"
      }
    ],
    "robustesse": {
      "score_global": 0.78,
      "zones_critiques": ["N3", "C2"]
    }
  },
  "comparaison": {
    "tableau_comparatif": {
      "reseau_base": { /* métriques */ },
      "reseau_optimise": { /* métriques */ },
      "reseau_robuste": { /* métriques */ }
    },
    "recommandation": {
      "choix_optimal": "reseau_optimise",
      "justification": "Meilleur compromis coût-performance",
      "risques": ["Sensibilité aux variations de demande"]
    }
  }
}
```

---

## 🧪 **TESTS ET VALIDATION**

### **Tests Unitaires**
```python
def test_network_complete_unified():
    """Test de la commande network-complete-unified"""
    # Test avec réseau simple
    # Test avec réseau complexe (boucles multiples)
    # Test avec données invalides
    # Test des exports (JSON, YAML, HTML)

def test_optimization_algorithms():
    """Test des algorithmes d'optimisation"""
    # Test algorithme génétique
    # Test analyse de sensibilité
    # Test convergence
    # Test contraintes

def test_epanet_integration():
    """Test de l'intégration EPANET"""
    # Test génération fichier .inp
    # Test exécution EPANET
    # Test comparaison résultats
    # Test gestion erreurs
```

### **Tests d'Intégration**
```python
def test_end_to_end_workflow():
    """Test du workflow complet"""
    # 1. Chargement réseau
    # 2. Validation données
    # 3. Analyse Hardy-Cross
    # 4. Génération EPANET
    # 5. Optimisation
    # 6. Analyse sensibilité
    # 7. Comparaison variantes
    # 8. Export résultats
```

---

## 📅 **PLANNING D'IMPLÉMENTATION**

### **Phase 2 (Semaines 1-4)**
- **Semaine 1** : Implémentation `network-complete-unified`
- **Semaine 2** : Intégration Hardy-Cross avancée
- **Semaine 3** : Intégration EPANET
- **Semaine 4** : Post-traitement et validation

### **Phase 3 (Semaines 5-8)**
- **Semaine 5** : Algorithmes d'optimisation
- **Semaine 6** : Analyse de sensibilité
- **Semaine 7** : Comparaison de variantes
- **Semaine 8** : Tests et documentation

### **Livrables**
- Commandes unifiées opérationnelles
- Documentation complète avec exemples
- Tests unitaires et d'intégration
- Templates YAML de référence
- Exemples de projets complets

---

## 🎯 **CRITÈRES DE SUCCÈS**

### **Fonctionnels**
- ✅ Toutes les commandes unifiées opérationnelles
- ✅ Intégration EPANET fonctionnelle
- ✅ Optimisation multi-critères
- ✅ Analyse de sensibilité

### **Performance**
- ⏱️ Temps de calcul < 30s pour réseaux < 100 nœuds
- ⏱️ Convergence Hardy-Cross < 50 itérations
- ⏱️ Optimisation < 5 minutes

### **Qualité**
- 🧪 Couverture de tests > 90%
- 📊 Documentation complète
- 🔍 Validation robuste des données
- 🎨 Interface utilisateur intuitive

---

*Document créé le 2025-01-27 - Version 4.0*
