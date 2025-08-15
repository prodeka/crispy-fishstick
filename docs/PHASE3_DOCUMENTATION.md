# Documentation Phase 3 : Analyse Avancée et Optimisation

## Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture des Modules](#architecture-des-modules)
3. [Module d'Optimisation](#module-doptimisation)
4. [Module d'Analyse de Sensibilité](#module-danalyse-de-sensibilité)
5. [Module de Comparaison](#module-de-comparaison)
6. [Utilisation Pratique](#utilisation-pratique)
7. [Exemples d'Usage](#exemples-dusage)
8. [Troubleshooting](#troubleshooting)
9. [API Reference](#api-reference)

## Vue d'ensemble

La Phase 3 introduit trois modules principaux pour l'analyse avancée et l'optimisation des réseaux d'eau potable (AEP) :

- **Optimisation** : Algorithmes génétiques pour trouver les meilleures configurations de diamètres
- **Sensibilité** : Analyse Monte Carlo et indices de Sobol pour évaluer la robustesse
- **Comparaison** : Métriques et outils de visualisation pour comparer différentes variantes

### Fonctionnalités Clés

- ✅ Optimisation multi-critères (coût, énergie, performance hydraulique)
- ✅ Gestion des contraintes budgétaires et techniques
- ✅ Analyse de sensibilité avec échantillonnage Monte Carlo
- ✅ Comparaison quantitative des variantes de réseaux
- ✅ Intégration complète en FCFA (Francs CFA)
- ✅ Architecture modulaire et extensible

## Architecture des Modules

```
src/lcpi/aep/
├── optimization/           # Module d'optimisation
│   ├── __init__.py
│   ├── models.py          # Modèles Pydantic
│   ├── individual.py      # Classe Individu
│   ├── genetic_algorithm.py # Algorithme génétique
│   └── constraints.py     # Gestionnaire de contraintes
├── sensitivity/           # Module d'analyse de sensibilité
│   ├── __init__.py
│   ├── monte_carlo.py    # Analyse Monte Carlo
│   ├── sobol_indices.py  # Indices de Sobol
│   └── robustness.py     # Analyse de robustesse
└── comparison/           # Module de comparaison
    ├── __init__.py
    ├── metrics.py        # Métriques de comparaison
    ├── visualizer.py     # Visualisation des réseaux
    └── reporter.py       # Génération de rapports
```

## Module d'Optimisation

### Concepts Fondamentaux

#### Individu
Représente une solution candidate avec ses diamètres et performances :

```python
from lcpi.aep.optimization import Individu

individu = Individu(
    diametres=[110, 125, 90],  # Diamètres en mm
    fitness=0.85,               # Score de fitness
    cout_total=45000,           # Coût total en FCFA
    energie_totale=1200,        # Énergie en Wh
    performance_hydraulique=0.92
)
```

#### Configuration d'Optimisation
Définit tous les paramètres de l'optimisation :

```python
from lcpi.aep.optimization import (
    ConfigurationOptimisation, CriteresOptimisation,
    ContraintesBudget, ContraintesTechniques,
    ParametresAlgorithme, DiametreCommercial
)

# Critères d'optimisation
criteres = CriteresOptimisation(
    principal="cout",
    secondaires=["energie", "performance"],
    poids=[0.5, 0.3, 0.2]
)

# Contraintes budgétaires
contraintes_budget = ContraintesBudget(
    cout_max_fcfa=100000,      # Budget maximum en FCFA
    cout_par_metre_max=150     # Coût max par mètre
)

# Contraintes techniques
contraintes_tech = ContraintesTechniques(
    pression_min_mce=20.0,     # Pression minimale
    pression_max_mce=80.0,     # Pression maximale
    vitesse_min_m_s=0.5,       # Vitesse minimale
    vitesse_max_m_s=2.5        # Vitesse maximale
)

# Paramètres de l'algorithme
algorithme = ParametresAlgorithme(
    type="genetique",
    population_size=100,
    generations=50,
    mutation_rate=0.1,
    crossover_rate=0.8
)

# Diamètres candidats
diametres = [
    DiametreCommercial(diametre_mm=90, cout_fcfa_m=35),
    DiametreCommercial(diametre_mm=110, cout_fcfa_m=45),
    DiametreCommercial(diametre_mm=125, cout_fcfa_m=60)
]

# Configuration complète
config = ConfigurationOptimisation(
    criteres=criteres,
    contraintes_budget=contraintes_budget,
    contraintes_techniques=contraintes_tech,
    algorithme=algorithme,
    diametres_candidats=diametres
)
```

### Algorithme Génétique

#### Optimiseur Principal

```python
from lcpi.aep.optimization import GeneticOptimizer

# Création de l'optimiseur
optimizer = GeneticOptimizer(config)

# Lancement de l'optimisation
resultats = optimizer.optimiser()

# Structure des résultats
{
    "statut": "succes",
    "iterations": 50,
    "meilleure_solution": {
        "diametres": {"C1": 110, "C2": 125, "C3": 90},
        "performance": {
            "cout_total_fcfa": 45000,
            "energie_totale_kwh": 0.33,
            "performance_hydraulique": 0.92
        }
    },
    "historique": [...]
}
```

#### Gestionnaire de Contraintes

```python
from lcpi.aep.optimization import ConstraintManager

# Création du gestionnaire
manager = ConstraintManager(config.contraintes_budget, config.contraintes_techniques)

# Vérification des contraintes
if manager.verifier_contraintes(individu):
    print("Individu valide")
else:
    print("Individu invalide")

# Calcul des pénalités
penalites = manager.calculer_penalites(individu)
```

## Module d'Analyse de Sensibilité

### Analyse Monte Carlo

```python
from lcpi.aep.sensitivity import MonteCarloAnalyzer

# Création de l'analyseur
analyzer = MonteCarloAnalyzer(
    parametres_initiaux=config,
    nombre_simulations=1000
)

# Lancement de l'analyse
resultats = analyzer.analyser_sensibilite()

# Structure des résultats
{
    "statut": "succes",
    "resultats_valides": 950,
    "parametres_critiques": ["cout_max_fcfa", "pression_min_mce"],
    "indices_sobol": {...},
    "statistiques": {...},
    "robustesse": {
        "score_global": 0.78,
        "zones_critiques": ["conduite_principale"]
    }
}
```

### Paramètres d'Analyse

```python
# Définition des distributions de paramètres
distributions = {
    "cout_max_fcfa": {
        "type": "normal",
        "moyenne": 100000,
        "ecart_type": 10000
    },
    "pression_min_mce": {
        "type": "uniforme",
        "min": 15.0,
        "max": 25.0
    }
}

# Configuration de l'analyse
config_analyse = {
    "nombre_simulations": 1000,
    "seuil_robustesse": 0.7,
    "parametres_etudies": ["cout_max_fcfa", "pression_min_mce"]
}
```

## Module de Comparaison

### Métriques de Comparaison

```python
from lcpi.aep.comparison import ComparisonMetrics

# Création du comparateur
comparateur = ComparisonMetrics()

# Comparaison de deux variantes
variante1 = {
    "cout_total_fcfa": 45000,
    "performance_hydraulique": 0.92,
    "energie_totale": 1200
}

variante2 = {
    "cout_total_fcfa": 52000,
    "performance_hydraulique": 0.95,
    "energie_totale": 1100
}

# Comparaison
resultats = comparateur.comparer_variantes(
    "Variante_Optimisee", variante1,
    "Variante_Reference", variante2
)

# Structure des résultats
{
    "variante_gagnante": "Variante_Optimisee",
    "score_global": 0.78,
    "metriques": {
        "cout_total_fcfa": {
            "difference": -7000,
            "pourcentage": -13.5,
            "favorise": "Variante_Optimisee"
        },
        "performance_hydraulique": {
            "difference": -0.03,
            "pourcentage": -3.2,
            "favorise": "Variante_Reference"
        }
    }
}
```

### Visualisation

```python
from lcpi.aep.comparison import NetworkVisualizer

# Création du visualiseur
visualiseur = NetworkVisualizer()

# Génération des graphiques
visualiseur.generer_comparaison_radar(resultats)
visualiseur.generer_comparaison_barres(resultats)
visualiseur.generer_carte_thermique(resultats)
```

## Utilisation Pratique

### 1. Configuration via Fichier YAML

```yaml
# optimise_reseau.yml
criteres:
  principal: "cout"
  secondaires: ["energie", "performance"]
  poids: [0.5, 0.3, 0.2]

contraintes_budget:
  cout_max_fcfa: 100000
  cout_par_metre_max: 150

contraintes_techniques:
  pression_min_mce: 20.0
  pression_max_mce: 80.0
  vitesse_min_m_s: 0.5
  vitesse_max_m_s: 2.5

algorithme:
  type: "genetique"
  population_size: 100
  generations: 50
  mutation_rate: 0.1
  crossover_rate: 0.8

diametres_candidats:
  - diametre_mm: 90
    cout_fcfa_m: 35
    materiau: "pvc"
  - diametre_mm: 110
    cout_fcfa_m: 45
    materiau: "pvc"
  - diametre_mm: 125
    cout_fcfa_m: 60
    materiau: "pvc"
```

### 2. Utilisation en Ligne de Commande

```bash
# Optimisation d'un réseau
python -m lcpi.aep.commands.network_optimize optimise \
    --config optimise_reseau.yml \
    --output resultats_optimisation.json

# Analyse de sensibilité
python -m lcpi.aep.commands.network_optimize sensibilite \
    --config optimise_reseau.yml \
    --simulations 1000 \
    --output analyse_sensibilite.json

# Comparaison de variantes
python -m lcpi.aep.commands.network_optimize compare \
    --variante1 variante1.json \
    --variante2 variante2.json \
    --output comparaison.json
```

### 3. Utilisation en Python

```python
import json
from lcpi.aep.optimization import GeneticOptimizer
from lcpi.aep.sensitivity import MonteCarloAnalyzer
from lcpi.aep.comparison import ComparisonMetrics

# Chargement de la configuration
with open('optimise_reseau.yml', 'r') as f:
    config = yaml.safe_load(f)

# 1. Optimisation
optimizer = GeneticOptimizer(config)
resultats_opt = optimizer.optimiser()

# 2. Analyse de sensibilité
analyzer = MonteCarloAnalyzer(config)
resultats_sens = analyzer.analyser_sensibilite()

# 3. Comparaison
comparateur = ComparisonMetrics()
resultats_comp = comparateur.comparer_variantes(
    "Optimisee", resultats_opt['meilleure_solution'],
    "Reference", config_reference
)

# Sauvegarde des résultats
with open('resultats_complets.json', 'w') as f:
    json.dump({
        'optimisation': resultats_opt,
        'sensibilite': resultats_sens,
        'comparaison': resultats_comp
    }, f, indent=2)
```

## Exemples d'Usage

### Exemple 1 : Optimisation Simple

```python
# Configuration minimale
config_simple = {
    "criteres": {"principal": "cout"},
    "contraintes_budget": {"cout_max_fcfa": 50000},
    "contraintes_techniques": {},
    "algorithme": {"type": "genetique"},
    "diametres_candidats": [
        {"diametre_mm": 90, "cout_fcfa_m": 35},
        {"diametre_mm": 110, "cout_fcfa_m": 45}
    ]
}

optimizer = GeneticOptimizer(config_simple)
resultats = optimizer.optimiser()
print(f"Meilleur coût: {resultats['meilleure_solution']['performance']['cout_total_fcfa']} FCFA")
```

### Exemple 2 : Analyse de Sensibilité

```python
# Analyse de la sensibilité au budget
config_sensibilite = {
    "parametres_etudies": ["cout_max_fcfa"],
    "distributions": {
        "cout_max_fcfa": {
            "type": "normal",
            "moyenne": 100000,
            "ecart_type": 15000
        }
    },
    "nombre_simulations": 500
}

analyzer = MonteCarloAnalyzer(config, config_sensibilite)
resultats = analyzer.analyser_sensibilite()

# Identification des paramètres critiques
parametres_critiques = resultats['parametres_critiques']
print(f"Paramètres critiques: {parametres_critiques}")
```

### Exemple 3 : Comparaison Multi-Critères

```python
# Comparaison avec pondération personnalisée
poids_personnalises = {
    'cout_total_fcfa': 0.6,      # Priorité au coût
    'performance_hydraulique': 0.3,
    'energie_totale': 0.1
}

resultats = comparateur.comparer_variantes(
    "Variante_A", variante_a,
    "Variante_B", variante_b,
    poids=poids_personnalises
)

print(f"Variante gagnante: {resultats['variante_gagnante']}")
print(f"Score global: {resultats['score_global']:.2f}")
```

## Troubleshooting

### Problèmes Courants

#### 1. Erreur de Validation Pydantic

```python
# Erreur: ValidationError pour les contraintes
try:
    config = ConfigurationOptimisation(**donnees)
except ValidationError as e:
    print("Erreur de validation:", e)
    # Vérifier les types et contraintes
```

#### 2. Convergence de l'Algorithme Génétique

```python
# Si l'optimisation ne converge pas
config['algorithme'].update({
    'population_size': 200,      # Augmenter la population
    'generations': 100,          # Plus de générations
    'mutation_rate': 0.15        # Plus de mutation
})
```

#### 3. Mémoire Insuffisante

```python
# Pour les gros réseaux
config['algorithme'].update({
    'population_size': 50,       # Réduire la population
    'generations': 30            # Moins de générations
})

# Ou utiliser le streaming des données
```

### Solutions Recommandées

1. **Validation des données** : Toujours valider les entrées avec Pydantic
2. **Tests unitaires** : Exécuter les tests avant déploiement
3. **Logging** : Activer les logs pour le débogage
4. **Profiling** : Utiliser cProfile pour identifier les goulots d'étranglement

## API Reference

### Classes Principales

#### GeneticOptimizer

```python
class GeneticOptimizer:
    def __init__(self, config: ConfigurationOptimisation)
    def optimiser(self) -> Dict[str, Any]
    def _initialiser_population(self) -> None
    def _calculer_fitness(self, individu: Individu) -> float
    def _selection_tournoi(self) -> Individu
    def _croisement(self, parent1: Individu, parent2: Individu) -> Tuple[Individu, Individu]
    def _mutation(self, individu: Individu) -> None
```

#### MonteCarloAnalyzer

```python
class MonteCarloAnalyzer:
    def __init__(self, config: ConfigurationOptimisation, **kwargs)
    def analyser_sensibilite(self) -> Dict[str, Any]
    def _generer_echantillons(self) -> List[Dict[str, Any]]
    def _evaluer_robustesse(self, resultats: List[Dict]) -> Dict[str, Any]
    def _calculer_indices_sobol(self) -> Dict[str, float]
```

#### ComparisonMetrics

```python
class ComparisonMetrics:
    def __init__(self)
    def comparer_variantes(self, nom1: str, variante1: Dict, 
                          nom2: str, variante2: Dict, 
                          poids: Optional[Dict] = None) -> Dict[str, Any]
    def _calculer_score_global(self, metriques: Dict, poids: Dict) -> float
    def _ajouter_metrique(self, nom: str, val1: float, val2: float, 
                         nom1: str, nom2: str, inverser: bool = False) -> None
```

### Types de Données

#### Individu

```python
@dataclass
class Individu:
    diametres: List[int]
    fitness: float = 0.0
    cout_total: float = 0.0
    energie_totale: float = 0.0
    performance_hydraulique: float = 0.0
```

#### ConfigurationOptimisation

```python
class ConfigurationOptimisation(BaseModel):
    criteres: CriteresOptimisation
    contraintes_budget: ContraintesBudget
    contraintes_techniques: ContraintesTechniques
    algorithme: ParametresAlgorithme
    diametres_candidats: List[DiametreCommercial]
```

---

*Document généré le : $(date)*  
*Version : 1.0*  
*Module : Phase 3 - Analyse Avancée et Optimisation*
