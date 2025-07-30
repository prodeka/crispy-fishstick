# Tests Unitaires - Plugin Hydro

Ce document décrit les tests unitaires automatisés pour les nouvelles fonctionnalités du plugin hydro.

## 📋 Vue d'Ensemble

### Modules Testés

1. **Collecteur d'Assainissement** (`test_collector_assainissement.py`)
   - 20 tests allant du simple au complexe
   - Tests des réseaux d'eaux usées et d'eaux pluviales
   - Tests des algorithmes de dimensionnement

2. **Réservoirs d'Eau Potable** (`test_reservoir_aep.py`)
   - 20 tests allant du simple au complexe
   - Tests des différents types de réservoirs
   - Tests des calculs de pression et de renouvellement

3. **Calculs Hydrauliques** (`test_hydraulique.py`)
   - 20 tests allant du simple au complexe
   - Tests des pertes de charge et courbes de remous
   - Tests de stabilité des talus

## 🚀 Exécution des Tests

### Prérequis

```bash
# Installer pytest et les dépendances
pip install pytest pytest-cov

# Vérifier l'installation
pytest --version
```

### Commandes de Base

```bash
# Exécuter tous les tests
python run_tests.py

# Exécuter avec couverture
python run_tests.py --coverage

# Exécuter en mode verbeux
python run_tests.py --verbose

# Exécuter seulement les tests rapides
python run_tests.py --fast
```

### Tests par Module

```bash
# Tests du collecteur d'assainissement
python run_tests.py --module collector

# Tests des réservoirs
python run_tests.py --module reservoir

# Tests hydrauliques
python run_tests.py --module hydraulique
```

### Tests par Difficulté

```bash
# Tests faciles seulement
python run_tests.py --difficulty easy

# Tests moyens
python run_tests.py --difficulty medium

# Tests difficiles
python run_tests.py --difficulty hard
```

### Commandes Pytest Directes

```bash
# Tous les tests
pytest tests/

# Tests avec couverture
pytest --cov=src/lcpi/hydrodrain tests/

# Tests d'un fichier spécifique
pytest tests/test_collector_assainissement.py

# Tests avec marqueurs
pytest -m "collector and easy" tests/
```

## 📊 Structure des Tests

### Niveaux de Difficulté

#### **Facile (Tests 1-5)**
- Création d'objets simples
- Tests de base des fonctions
- Vérifications élémentaires

#### **Moyen (Tests 6-15)**
- Calculs avec paramètres réels
- Tests de cas limites
- Vérifications de cohérence

#### **Complexe (Tests 16-20)**
- Tests d'intégration
- Cas d'usage complexes
- Validation d'algorithmes complets

### Marqueurs Pytest

```python
@pytest.mark.collector      # Tests du module collecteur
@pytest.mark.reservoir      # Tests du module réservoir
@pytest.mark.hydraulique    # Tests du module hydraulique
@pytest.mark.easy          # Tests faciles
@pytest.mark.medium        # Tests moyens
@pytest.mark.hard          # Tests difficiles
@pytest.mark.slow          # Tests lents
@pytest.mark.integration   # Tests d'intégration
@pytest.mark.unit          # Tests unitaires
```

## 🧪 Détail des Tests

### Collecteur d'Assainissement

#### Tests Faciles (1-5)
1. **Création d'un tronçon simple**
   - Vérification des attributs de base
   - Test des valeurs par défaut

2. **Création d'un réseau vide**
   - Test de l'initialisation
   - Vérification de la structure

3. **Ajout d'un tronçon au réseau**
   - Test de l'ajout d'éléments
   - Vérification de l'intégrité

4. **Tri topologique simple**
   - Test avec 2 tronçons
   - Vérification de l'ordre

5. **Calcul du débit propre**
   - Test avec données réelles
   - Vérification des formules

#### Tests Moyens (6-15)
6. **Calcul du débit amont**
   - Test de l'agrégation
   - Vérification des cumuls

7. **Dimensionnement circulaire**
   - Test avec débit réel
   - Vérification des contraintes

8. **Calcul du temps de concentration**
   - Test de la formule Kirpich
   - Vérification des unités

9. **Calcul de l'intensité de pluie**
   - Test de la formule Talbot
   - Vérification des coefficients

10. **Réseau d'eaux usées complet**
    - Test d'intégration
    - Vérification des résultats

#### Tests Complexes (16-20)
16. **Gestion d'erreurs**
    - Test des cas limites
    - Vérification des messages

17. **Paramètres extrêmes**
    - Test avec valeurs limites
    - Vérification de la robustesse

18. **Agrégation complexe**
    - Test avec plusieurs tronçons
    - Vérification des calculs

19. **Convergence itérative**
    - Test des algorithmes
    - Vérification de la stabilité

20. **Réseau complexe**
    - Test d'intégration complète
    - Vérification de la cohérence

### Réservoirs d'Eau Potable

#### Tests Faciles (1-5)
1. **Dimensionnement d'équilibrage**
   - Test des calculs de base
   - Vérification des volumes

2. **Réservoir d'incendie urbain**
   - Test des normes
   - Vérification des débits

3. **Réservoir d'incendie rural**
   - Test des paramètres ruraux
   - Vérification des différences

4. **Réservoir d'incendie industriel**
   - Test des paramètres industriels
   - Vérification des volumes

5. **Gestion d'erreurs**
   - Test des types invalides
   - Vérification des messages

#### Tests Moyens (6-15)
6. **Vérification de pression**
   - Test des calculs de pression
   - Vérification des niveaux

7. **Pression insuffisante**
   - Test des cas limites
   - Vérification des alertes

8. **Calcul de renouvellement**
   - Test des temps de renouvellement
   - Vérification de la qualité

9. **Renouvellement problématique**
   - Test des cas critiques
   - Vérification des recommandations

10. **Volume optimal simple**
    - Test des courbes cumulées
    - Vérification des calculs

#### Tests Complexes (16-20)
16. **Niveaux de sécurité**
    - Test des différents niveaux
    - Vérification des seuils

17. **Qualités de renouvellement**
    - Test des différentes qualités
    - Vérification des critères

18. **Pointe extrême**
    - Test avec demande variable
    - Vérification des volumes

19. **Paramètres extrêmes**
    - Test avec grandes populations
    - Vérification de la robustesse

20. **Intégration complète**
    - Test d'intégration
    - Vérification de la cohérence

### Calculs Hydrauliques

#### Tests Faciles (1-5)
1. **Pertes de charge linéaires**
   - Test des calculs de base
   - Vérification des formules

2. **Pertes de charge singulières**
   - Test des coefficients
   - Vérification des calculs

3. **Calcul du débit critique**
   - Test de la formule
   - Vérification des paramètres

4. **Stabilité des talus**
   - Test de la méthode Bishop
   - Vérification des coefficients

5. **Courbe de remous**
   - Test de base
   - Vérification de la structure

#### Tests Moyens (6-15)
6. **Écoulement turbulent**
   - Test des régimes
   - Vérification des nombres de Reynolds

7. **Pertes singulières complexes**
   - Test avec multiples éléments
   - Vérification des cumuls

8. **Débit critique variable**
   - Test avec différentes profondeurs
   - Vérification des tendances

9. **Stabilité variable**
   - Test avec différentes conditions
   - Vérification des comparaisons

10. **Écoulement rapide**
    - Test des courbes de remous
    - Vérification des profils

#### Tests Complexes (16-20)
16. **Paramètres extrêmes**
    - Test avec valeurs limites
    - Vérification de la robustesse

17. **Pentes variables**
    - Test avec différentes pentes
    - Vérification des tendances

18. **Matériaux différents**
    - Test avec différents sols
    - Vérification des comportements

19. **Écoulement lent**
    - Test des courbes de remous
    - Vérification des profils

20. **Intégration complète**
    - Test d'intégration
    - Vérification de la cohérence

## 📈 Couverture de Code

### Génération des Rapports

```bash
# Rapport de couverture en terminal
python run_tests.py --coverage

# Rapport HTML
python run_tests.py --html

# Rapport XML (pour CI/CD)
pytest --cov=src/lcpi/hydrodrain --cov-report=xml tests/
```

### Objectifs de Couverture

- **Lignes de code**: > 90%
- **Branches**: > 85%
- **Fonctions**: > 95%
- **Modules**: 100%

## 🔧 Maintenance des Tests

### Ajout de Nouveaux Tests

1. **Créer le test** dans le fichier approprié
2. **Ajouter les marqueurs** appropriés
3. **Documenter** le test avec une docstring claire
4. **Vérifier** que le test passe

### Exemple de Test

```python
@pytest.mark.collector
@pytest.mark.medium
def test_nouveau_calcul():
    """Test du nouveau calcul (niveau: moyen)"""
    # Arrange
    donnees = {...}
    
    # Act
    resultat = fonction_testee(donnees)
    
    # Assert
    assert resultat["statut"] == "OK"
    assert resultat["valeur"] > 0
```

### Bonnes Pratiques

1. **Nommage clair** des tests
2. **Documentation** des cas de test
3. **Isolation** des tests
4. **Données de test** réalistes
5. **Assertions** spécifiques
6. **Gestion d'erreurs** testée

## 🚨 Dépannage

### Problèmes Courants

#### Import Errors
```bash
# Vérifier le PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Ou utiliser le script
python run_tests.py
```

#### Tests qui Échouent
```bash
# Mode verbeux pour plus de détails
python run_tests.py --verbose

# Tests spécifiques
pytest tests/test_collector_assainissement.py::TestCollecteurAssainissement::test_1_creation_troncon_simple -v
```

#### Couverture Manquante
```bash
# Vérifier les fichiers manqués
python run_tests.py --coverage

# Générer un rapport détaillé
pytest --cov=src/lcpi/hydrodrain --cov-report=html tests/
```

## 📚 Ressources

- [Documentation Pytest](https://docs.pytest.org/)
- [Pytest-cov](https://pytest-cov.readthedocs.io/)
- [Bonnes pratiques de test](https://realpython.com/python-testing/) 