# 📋 TODO AMELIORATION_V13 - TÂCHES RESTANTES

## **📊 ÉTAT GLOBAL DU PROJET**

**Progression actuelle : 67% (10/15 tâches complétées)**
- ✅ **Sprint 1** : 100% (5/5 tâches)
- ⚠️ **Sprint 2** : 75% (3/4 tâches) 
- ❌ **Sprint 3** : 0% (0/3 tâches)
- ⚠️ **Sprint 4** : 33% (1/3 tâches)

---

## **🚨 SPRINT 3 : CLI, REPORTING & EXPÉRIENCE UTILISATEUR**

### **1. Format de Sortie JSON V11** 🔴 **BLOQUANT**
**Priorité : CRITIQUE** - Bloque la mise en production

#### **Fichiers à créer/modifier :**
- `src/lcpi/aep/optimizer/output.py` (nouveau)
- `src/lcpi/aep/optimizer/formatters.py` (nouveau)
- Mettre à jour tous les algorithmes d'optimisation

#### **Fonctionnalités à implémenter :**
```python
# Format JSON V11 standard
{
    "proposals": [
        {
            "name": "min_capex",
            "is_feasible": true,
            "tanks": [{"id": "TANK1", "H_m": 65.0}],
            "diameters_mm": {"PIPE1": 200, "PIPE2": 150},
            "costs": {
                "CAPEX": 150000.0,
                "OPEX_annual": 5000.0,
                "OPEX_npv": 45000.0
            },
            "metrics": {
                "min_pressure_m": 12.5,
                "max_velocity_m_s": 1.8
            }
        }
    ],
    "pareto": [...],  # Front de Pareto
    "metadata": {
        "algorithm": "nested_greedy",
        "execution_time": "00:05:23",
        "iterations": 150
    }
}
```

#### **Tâches détaillées :**
- [ ] Créer la classe `OutputFormatter` avec méthode `format_v11()`
- [ ] Implémenter la sérialisation des `Proposal` et `OptimizationResult`
- [ ] Ajouter la gestion des résultats multi-réservoirs
- [ ] Créer des tests unitaires pour le formatage
- [ ] Mettre à jour tous les algorithmes pour utiliser le nouveau format

---

### **2. Commandes CLI Manquantes** 🔴 **BLOQUANT**
**Priorité : CRITIQUE** - Interface utilisateur essentielle

#### **Fichiers à modifier :**
- `src/lcpi/aep/cli.py`
- `src/lcpi/aep/optimizer/cli_commands.py` (nouveau)

#### **Commandes à implémenter :**

##### **`price-optimize` (optimisation avec score pondéré)**
```python
@cli.command()
def price_optimize(
    network: Path,
    lambda_opex: float = 10.0,
    method: str = "nested",
    output: Path = None
):
    """
    Optimise avec score pondéré J = CAPEX + λ·OPEX_NPV
    """
    # Implémentation à faire
    pass
```

##### **`report` (régénération d'un rapport)**
```python
@cli.command()
def report(
    results_file: Path,
    template: str = "default",
    output: Path = None
):
    """
    Régénère un rapport d'optimisation
    """
    # Implémentation à faire
    pass
```

##### **`diameters-manage` (gestion de la DB de diamètres)**
```python
@cli.command()
def diameters_manage(
    action: str,  # "list", "add", "remove", "update"
    diameter_mm: int = None,
    price_fcfa: float = None
):
    """
    Gère la base de données des diamètres disponibles
    """
    # Implémentation à faire
    pass
```

#### **Tâches détaillées :**
- [ ] Créer le module `cli_commands.py` pour organiser les commandes
- [ ] Implémenter la logique de `price-optimize` avec score pondéré
- [ ] Créer le système de régénération de rapports
- [ ] Implémenter la gestion CRUD des diamètres
- [ ] Ajouter la validation des paramètres CLI
- [ ] Créer des tests pour chaque commande
- [ ] Mettre à jour la documentation CLI

---

### **3. Rapport d'Optimisation V11** 🔴 **BLOQUANT**
**Priorité : CRITIQUE** - Visualisation des résultats

#### **Fichiers à créer/modifier :**
- `src/lcpi/aep/templates/optimisation_tank_v11.jinja2` (nouveau)
- `src/lcpi/aep/reporting/report_generator.py` (nouveau)
- `src/lcpi/aep/reporting/charts.py` (nouveau)

#### **Fonctionnalités à implémenter :**

##### **Template Jinja2 V11**
```html
<!-- Tableau comparatif des solutions -->
<table class="solutions-comparison">
    <thead>
        <tr>
            <th>Solution</th>
            <th>CAPEX (FCFA)</th>
            <th>OPEX Annuel (FCFA)</th>
            <th>OPEX NPV (FCFA)</th>
            <th>Pression Min (m)</th>
            <th>Vitesse Max (m/s)</th>
        </tr>
    </thead>
    <tbody>
        {% for proposal in proposals %}
        <tr>
            <td>{{ proposal.name }}</td>
            <td>{{ proposal.costs.CAPEX | format_currency }}</td>
            <td>{{ proposal.costs.OPEX_annual | format_currency }}</td>
            <td>{{ proposal.costs.OPEX_npv | format_currency }}</td>
            <td>{{ proposal.metrics.min_pressure_m | round(2) }}</td>
            <td>{{ proposal.metrics.max_velocity_m_s | round(2) }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- Graphique du front de Pareto -->
<div class="pareto-chart">
    <canvas id="paretoChart"></canvas>
</div>
```

##### **Générateur de rapports**
```python
class ReportGenerator:
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.jinja_env = self._setup_jinja()
    
    def generate_report(self, results: Dict, template: str = "default") -> str:
        """Génère un rapport HTML à partir des résultats"""
        # Implémentation à faire
        pass
    
    def generate_pareto_chart(self, pareto_front: List[Proposal]) -> str:
        """Génère un graphique du front de Pareto en HTML/JS"""
        # Implémentation à faire
        pass
```

#### **Tâches détaillées :**
- [ ] Créer le template Jinja2 V11 avec tableau comparatif
- [ ] Implémenter la génération de graphiques Pareto
- [ ] Créer le système de génération de rapports
- [ ] Ajouter la gestion des thèmes et styles CSS
- [ ] Implémenter l'export en PDF (optionnel)
- [ ] Créer des tests pour la génération de rapports
- [ ] Intégrer avec les commandes CLI

---

## **⚡ SPRINT 2 : ALGORITHMES D'OPTIMISATION AVANCÉS**

### **1. GlobalOptimizer (NSGA-II) - Parallélisation** 🟡 **PRIORITÉ MOYENNE**

#### **Fichiers à modifier :**
- `src/lcpi/aep/optimizer/algorithms/global_opt.py`

#### **Fonctionnalités à implémenter :**
```python
class GlobalOptimizer:
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.executor = ProcessPoolExecutor(
            max_workers=config.global_config.parallel_workers
        )
    
    def optimize_with_parallelization(self) -> OptimizationResult:
        """Exécute l'optimisation NSGA-II en parallèle"""
        # Implémentation à faire
        pass
    
    def _evaluate_population_parallel(self, population: List) -> List[float]:
        """Évalue une population en parallèle"""
        # Implémentation à faire
        pass
```

#### **Tâches détaillées :**
- [ ] Implémenter `ProcessPoolExecutor` pour la parallélisation
- [ ] Diviser la population en chunks pour traitement parallèle
- [ ] Gérer la synchronisation des résultats
- [ ] Ajouter la configuration du nombre de workers
- [ ] Créer des tests de performance parallèle
- [ ] Optimiser la gestion mémoire pour grandes populations

---

### **2. GlobalOptimizer (NSGA-II) - Checkpoints** 🟡 **PRIORITÉ MOYENNE**

#### **Fonctionnalités à implémenter :**
```python
class GlobalOptimizer:
    def save_checkpoint(self, generation: int, population: List, filename: str):
        """Sauvegarde l'état de l'optimisation"""
        checkpoint_data = {
            "generation": generation,
            "population": population,
            "best_fitness": self.best_fitness_history,
            "timestamp": datetime.now().isoformat()
        }
        with open(filename, 'w') as f:
            json.dump(checkpoint_data, f)
    
    def load_checkpoint(self, filename: str) -> Tuple[int, List]:
        """Charge un checkpoint pour reprendre l'optimisation"""
        # Implémentation à faire
        pass
    
    def resume_from_checkpoint(self, checkpoint_file: str) -> OptimizationResult:
        """Reprend l'optimisation depuis un checkpoint"""
        # Implémentation à faire
        pass
```

#### **Tâches détaillées :**
- [ ] Implémenter la sauvegarde de checkpoints
- [ ] Créer le système de reprise depuis checkpoint
- [ ] Gérer la compatibilité des versions de checkpoints
- [ ] Ajouter la validation des données de checkpoint
- [ ] Créer des tests pour la sauvegarde/reprise
- [ ] Intégrer avec la CLI pour `--resume-from-checkpoint`

---

### **3. SurrogateOptimizer - Persistance des modèles** 🟡 **PRIORITÉ MOYENNE**

#### **Fichiers à modifier :**
- `src/lcpi/aep/optimizer/algorithms/surrogate.py`
- `src/lcpi/aep/optimizer/model_store/` (nouveau dossier)

#### **Fonctionnalités à implémenter :**
```python
class SurrogateOptimizer:
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.model_store_path = Path("data/model_store")
        self.model_store_path.mkdir(parents=True, exist_ok=True)
    
    def save_model(self, model: RandomForestRegressor, name: str):
        """Sauvegarde un modèle entraîné"""
        model_path = self.model_store_path / f"{name}.joblib"
        joblib.dump(model, model_path)
        
        # Sauvegarder les métadonnées
        metadata = {
            "name": name,
            "type": "RandomForestRegressor",
            "features": self.feature_names,
            "training_date": datetime.now().isoformat(),
            "performance": self.model_performance
        }
        metadata_path = self.model_store_path / f"{name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
    
    def load_model(self, name: str) -> RandomForestRegressor:
        """Charge un modèle sauvegardé"""
        model_path = self.model_store_path / f"{name}.joblib"
        if not model_path.exists():
            raise FileNotFoundError(f"Modèle {name} non trouvé")
        
        model = joblib.load(model_path)
        return model
    
    def list_available_models(self) -> List[str]:
        """Liste tous les modèles disponibles"""
        # Implémentation à faire
        pass
```

#### **Tâches détaillées :**
- [ ] Créer le dossier `model_store/` pour la persistance
- [ ] Implémenter la sauvegarde avec `joblib`
- [ ] Ajouter la sauvegarde des métadonnées
- [ ] Implémenter le chargement des modèles
- [ ] Créer la liste des modèles disponibles
- [ ] Ajouter la validation des modèles chargés
- [ ] Créer des tests pour la persistance
- [ ] Intégrer avec la CLI pour la gestion des modèles

---

## **🔧 SPRINT 4 : AUDITABILITÉ, TESTS ET INTÉGRATION CONTINUE**

### **1. Auditabilité des Résultats** 🟡 **PRIORITÉ BASSE**

#### **Fichiers à créer :**
- `src/lcpi/aep/audit/signature.py` (nouveau)
- `src/lcpi/aep/audit/database.py` (nouveau)
- `data/results/index.db` (nouveau)

#### **Fonctionnalités à implémenter :**
```python
class ResultAuditor:
    def __init__(self, db_path: Path = Path("data/results/index.db")):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def sign_result(self, result_data: Dict, private_key: str = None) -> str:
        """Signe cryptographiquement un résultat"""
        # Implémentation à faire
        pass
    
    def verify_signature(self, result_data: Dict, signature: str) -> bool:
        """Vérifie la signature d'un résultat"""
        # Implémentation à faire
        pass
    
    def index_execution(self, execution_id: str, metadata: Dict):
        """Indexe une exécution dans la base SQLite"""
        # Implémentation à faire
        pass
    
    def verify_log(self, log_file: Path) -> Dict:
        """Valide une signature de log"""
        # Implémentation à faire
        pass
```

#### **Tâches détaillées :**
- [ ] Implémenter la signature cryptographique (HMAC/SHA256)
- [ ] Créer la base SQLite pour indexer les exécutions
- [ ] Implémenter la vérification des signatures
- [ ] Créer la commande CLI `verify-log`
- [ ] Ajouter la gestion des clés de signature
- [ ] Créer des tests pour l'auditabilité
- [ ] Documenter le processus de vérification

---

### **2. Intégration Continue (CI)** 🟡 **PRIORITÉ BASSE**

#### **Fichiers à créer :**
- `.github/workflows/ci.yml` (nouveau)
- `.github/workflows/test.yml` (nouveau)

#### **Fonctionnalités à implémenter :**
```yaml
# .github/workflows/ci.yml
name: CI - Tests et Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src/lcpi --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

#### **Tâches détaillées :**
- [ ] Créer le workflow GitHub Actions principal
- [ ] Configurer le cache des dépendances
- [ ] Ajouter la couverture de code avec pytest-cov
- [ ] Configurer l'intégration avec Codecov
- [ ] Ajouter les tests sur plusieurs versions Python
- [ ] Configurer les notifications d'échec
- [ ] Ajouter la validation des types avec mypy (optionnel)
- [ ] Documenter le processus CI/CD

---

## **📋 PLAN D'EXÉCUTION RECOMMANDÉ**

### **Phase 1 : Sprint 3 (2-3 semaines) - CRITIQUE**
1. **Format JSON V11** (1 semaine)
2. **Commandes CLI** (1 semaine)
3. **Rapports V11** (1 semaine)

### **Phase 2 : Sprint 2 - Complétion (1-2 semaines)**
1. **Parallélisation GlobalOptimizer** (3-4 jours)
2. **Checkpoints** (2-3 jours)
3. **Persistance des modèles** (3-4 jours)

### **Phase 3 : Sprint 4 - Production (1-2 semaines)**
1. **Auditabilité** (1 semaine)
2. **CI/CD** (1 semaine)

## **🎯 OBJECTIFS DE QUALITÉ**

### **Tests**
- [ ] Couverture de code > 90%
- [ ] Tests unitaires pour toutes les nouvelles fonctionnalités
- [ ] Tests d'intégration pour les workflows complets
- [ ] Tests de performance pour les algorithmes parallèles

### **Documentation**
- [ ] Documentation utilisateur pour toutes les commandes CLI
- [ ] Documentation technique pour les développeurs
- [ ] Exemples d'utilisation et tutoriels
- [ ] Guide de déploiement et configuration

### **Code**
- [ ] Respect des standards PEP 8
- [ ] Type hints pour toutes les fonctions
- [ ] Docstrings complètes
- [ ] Gestion d'erreurs robuste

---

## **📊 MÉTRIQUES DE SUCCÈS**

- **Fonctionnalités** : 100% des tâches V13 implémentées
- **Tests** : Couverture > 90%
- **Performance** : Optimisations parallèles fonctionnelles
- **Interface** : CLI complète et intuitive
- **Production** : Système auditable et déployable

---

*Document généré le : 2025-01-16*  
*Statut : 📋 TODO COMPLET*  
*Priorité : SPRINT 3 CRITIQUE*  
*Estimation : 6-8 semaines*
