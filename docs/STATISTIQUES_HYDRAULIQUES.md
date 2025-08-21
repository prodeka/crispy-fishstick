# 📊 Statistiques Hydrauliques Détaillées

## Vue d'ensemble

Les statistiques hydrauliques détaillées ont été ajoutées aux résultats d'optimisation pour fournir une analyse complète des performances hydrauliques du réseau. Ces statistiques sont automatiquement calculées à partir des résultats de simulation EPANET et incluses dans les fichiers de sortie JSON.

## 🎯 Fonctionnalités Ajoutées

### 1. Calcul Automatique des Statistiques

- **Intégration transparente** : Les statistiques sont calculées automatiquement lors de chaque simulation
- **Gestion d'erreurs robuste** : Les erreurs de calcul sont capturées et signalées
- **Performance optimisée** : Calculs vectorisés pour de grandes quantités de données

### 2. Statistiques Calculées

#### 💧 Pressions (m)
- **Statistiques descriptives** : min, max, moyenne, médiane, écart-type
- **Quartiles** : Q25, Q75
- **Pourcentages sous seuils** : % sous 10m, 15m, 20m
- **Nombre de nœuds** analysés

#### ⚡ Vitesses (m/s)
- **Statistiques descriptives** : min, max, moyenne, médiane, écart-type
- **Quartiles** : Q25, Q75
- **Pourcentages au-dessus des seuils** : % au-dessus 1m/s, 2m/s, 3m/s
- **Nombre de conduites** analysées

#### 🌊 Charges Hydrauliques (m)
- **Statistiques descriptives** : min, max, moyenne, médiane, écart-type
- **Nombre de nœuds** analysés

#### 📉 Pertes de Charge (m)
- **Statistiques descriptives** : min, max, moyenne, médiane, écart-type
- **Pertes totales** : somme des pertes de charge
- **Nombre de conduites** analysées

#### 🌊 Débits (m³/s)
- **Statistiques descriptives** : min, max, moyenne, médiane, écart-type
- **Débit total** : somme des débits
- **Nombre de conduites** analysées

#### 🔧 Diamètres Réels DN (mm)
- **Statistiques descriptives** : min, max, moyenne, médiane, écart-type
- **Distribution par gammes DN** :
  - DN20-50
  - DN63-100
  - DN125-200
  - DN250-400
  - DN450+
- **Nombre de conduites** analysées

#### 📈 Indice de Performance Hydraulique
- **Score normalisé** basé sur les pressions et vitesses
- **Valeurs typiques** : 0.0 (mauvais) à 2.0 (excellent)

### 3. Résumé Global

Un résumé global est fourni avec :
- **Nombre total de nœuds et conduites**
- **Plages de valeurs** pour chaque paramètre
- **Totaux** pour les pertes de charge et débits

## 🔧 Implémentation Technique

### Fichiers Modifiés

1. **`src/lcpi/aep/optimizer/controllers.py`**
   - Ajout de la fonction `_calculate_hydraulic_statistics()`
   - Intégration dans le traitement des résultats hydrauliques

2. **`src/lcpi/aep/optimization/genetic_algorithm.py`**
   - Ajout des statistiques détaillées dans les résultats d'optimisation

### Fonction Principale

```python
def _calculate_hydraulic_statistics(hydraulics_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les statistiques hydrauliques détaillées à partir des résultats de simulation.
    
    Args:
        hydraulics_data: Données hydrauliques de la simulation
        
    Returns:
        Dict contenant toutes les statistiques hydrauliques
    """
```

### Structure des Données

Les statistiques sont stockées dans :
```json
{
  "hydraulics": {
    "statistics": {
      "pressures": { ... },
      "velocities": { ... },
      "heads": { ... },
      "headlosses": { ... },
      "flows": { ... },
      "diameters": { ... },
      "performance_index": 1.596,
      "summary": { ... }
    }
  }
}
```

## 📊 Exemples d'Utilisation

### 1. Test des Statistiques

```bash
python tools/test_hydraulic_statistics.py
```

### 2. Démonstration des Résultats

```bash
python tools/demo_hydraulic_statistics.py
```

### 3. Optimisation avec Statistiques

```bash
python -m lcpi.aep.cli network-optimize-unified \
  --method genetic \
  --solver epanet \
  --generations 10 \
  --population 20 \
  --output results/optimization_with_stats.json
```

## 📈 Interprétation des Résultats

### Indicateurs de Performance

1. **Pressions** :
   - **Bon** : Moyenne > 20m, % sous 10m < 5%
   - **Acceptable** : Moyenne 15-20m, % sous 10m < 10%
   - **Problématique** : Moyenne < 15m, % sous 10m > 10%

2. **Vitesses** :
   - **Optimal** : 0.5-1.5 m/s
   - **Acceptable** : 0.3-2.0 m/s
   - **Problématique** : < 0.3 m/s ou > 3.0 m/s

3. **Pertes de Charge** :
   - **Faibles** : < 1% de la hauteur disponible
   - **Modérées** : 1-5% de la hauteur disponible
   - **Élevées** : > 5% de la hauteur disponible

### Distribution des Diamètres

La distribution par gammes DN aide à :
- **Identifier les gammes prédominantes**
- **Optimiser les coûts** en standardisant les diamètres
- **Planifier les approvisionnements**

## 🚀 Avantages

1. **Analyse Complète** : Tous les paramètres hydrauliques sont analysés
2. **Transparence** : Calculs détaillés et traçables
3. **Comparaison** : Facilité de comparaison entre différentes solutions
4. **Optimisation** : Aide à l'identification des points d'amélioration
5. **Reporting** : Données structurées pour les rapports techniques

## 🔮 Évolutions Futures

1. **Graphiques automatiques** : Génération de graphiques de distribution
2. **Seuils configurables** : Paramétrage des seuils d'alerte
3. **Analyse temporelle** : Statistiques sur plusieurs pas de temps
4. **Export Excel** : Export des statistiques en format tabulaire
5. **Comparaison multi-scénarios** : Analyse comparative entre solutions

## 📝 Notes Techniques

- **Gestion des NaN** : Les valeurs NaN sont automatiquement filtrées
- **Performance** : Calculs optimisés pour de grands réseaux
- **Mémoire** : Gestion efficace de la mémoire pour les gros datasets
- **Compatibilité** : Fonctionne avec tous les solveurs hydrauliques

---

*Documentation générée le 20/08/2025*
