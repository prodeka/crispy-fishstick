# Diagnostic Conservation de Masse - Bismark Network

**Date**: 21 Août 2025  
**Réseau**: `bismark-Administrator.inp`  
**Méthode**: Comparaison EPANET brut vs Optimisation

## 📊 Résultats de Comparaison

### Simulation EPANET Brute (check_flows.py)
- **Total Flow**: -2.881 m³/s
- **Conservation OK**: ❌ (violation majeure)
- **Conduites**: 205
- **Timesteps**: 1 (simulation statique)

### Optimisation LCPI
- **Total Flow**: -1.202 m³/s  
- **Conservation OK**: ❌ (violation majeure)
- **Conduites**: 205
- **Diamètres uniques**: [315] (tous identiques !)
- **PriceDB**: external_file (C:\PROJET_DIMENTIONEMENT_2\src\lcpi\db\aep_prices.db)

## 🔍 Diagnostic

### 1. Conservation de Masse Violée
**Problème**: Les deux simulations montrent une violation de conservation de masse
- EPANET brut: -2.881 m³/s
- Optimisation: -1.202 m³/s

**Interprétation**: 
- ✅ **Le problème ne vient PAS de l'optimisation** (l'optimisation améliore même légèrement la conservation)
- ❌ **Le problème vient du parsing initial de l'INP** ou de la configuration du réseau

### 2. Diamètres Uniformes
**Problème**: Toutes les conduites ont le même diamètre (315mm)
- **Cause probable**: PriceDB externe chargée mais diamètres non diversifiés
- **Impact**: Optimisation inefficace, coûts non optimaux

### 3. Contraintes Non Respectées
**Problème**: `constraints_ok: True` malgré vitesse max > 5 m/s
- **Cause**: Logique de validation des contraintes défaillante

## 🎯 Causes Probables

### 1. Configuration du Réseau
- **Demandes non équilibrées**: La somme des demandes ≠ somme des entrées
- **Réservoirs/Tanks mal configurés**: Niveaux ou débits incorrects
- **Valves ou éléments spéciaux**: Comportement non standard

### 2. Parsing WNTR/EPANET
- **Orientation des conduites**: Sens défini arbitraire dans l'INP
- **Unités**: Problème de conversion ou d'interprétation
- **Agrégation des résultats**: Erreur dans le calcul des sommes

### 3. PriceDB Externe
- **Diamètres limités**: Base de données avec peu de diamètres disponibles
- **Fallback défaillant**: Logique de repli vers diamètres standards

## 🛠️ Actions Correctives Recommandées

### Priorité 1: Vérifier la Configuration du Réseau
```bash
# Analyser le fichier INP
python tools/check_flows.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --simulator wntr --links "P1,P2,P3" --no-json-series
```

**Actions**:
1. Vérifier les sections `[RESERVOIRS]` et `[TANKS]`
2. Contrôler les `[DEMANDS]` aux nœuds
3. S'assurer que la somme des entrées = somme des sorties

### Priorité 2: Corriger la Logique des Contraintes
**Fichier**: `src/lcpi/aep/optimizer/controllers.py`
**Problème**: `constraints_ok` reste `True` malgré les violations

**Solution**:
```python
# Dans _apply_constraints_and_penalties
if max_velocity > velocity_max_m_s:
    constraints_ok = False  # Forcer à False si violation
```

### Priorité 3: Diversifier les Diamètres
**Fichier**: `src/lcpi/aep/optimizer/controllers.py`
**Problème**: Tous les diamètres identiques

**Solution**:
```python
# Ajouter un fallback avec diamètres standards
STANDARD_DIAMETERS = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]
```

### Priorité 4: Améliorer le Diagnostic
**Script**: `tools/diagnose_flow_conservation.py`
**Problème**: Échec avec simulation EPANET vide

**Solution**: Gérer les cas où la simulation retourne des données vides

## 📈 Métriques de Suivi

### Conservation de Masse
- **Seuil acceptable**: |sum(flows)| < 1e-3 m³/s
- **Actuel**: -2.881 m³/s (violation majeure)
- **Objectif**: < 1e-3 m³/s

### Diversité des Diamètres
- **Actuel**: 1 diamètre unique (315mm)
- **Objectif**: 5-10 diamètres différents
- **Métrique**: `len(set(diameters))`

### Respect des Contraintes
- **Actuel**: `constraints_ok: True` (incorrect)
- **Objectif**: `constraints_ok` reflète la réalité
- **Métrique**: Cohérence entre `constraints_ok` et les violations

## 🔄 Prochaines Étapes

1. **Analyser le fichier INP** pour identifier les problèmes de configuration
2. **Corriger la logique des contraintes** pour une validation correcte
3. **Implémenter un fallback de diamètres** pour la diversité
4. **Tester avec un réseau simple** pour valider les corrections
5. **Relancer l'optimisation** et vérifier les améliorations

## 📝 Notes Techniques

### Fichiers de Diagnostic Générés
- `src/lcpi/aep/PROTOTYPE/INP/results/bismark-Administrator_sumflows_epanet.csv`
- `src/lcpi/aep/PROTOTYPE/INP/results/bismark-Administrator_sumflows_epanet.json`
- `src/lcpi/aep/PROTOTYPE/INP/results/bismark-Administrator_sumflows_plot.png`
- `src/lcpi/aep/PROTOTYPE/INP/results/bismark-Administrator_sumflows_report.md`

### Commandes de Diagnostic
```bash
# Diagnostic complet
python tools/check_flows.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --simulator epanet --save-plot

# Inspection rapide
python tools/quick_inspect.py .\results\test_integrated_stats.json

# Diagnostic avec sous-ensemble
python tools/check_flows.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --simulator wntr --links "P1,P2,P3" --no-json-series
```

---

**Conclusion**: Le problème principal vient de la configuration du réseau (conservation de masse violée dès le départ), pas de l'optimisation. Les corrections doivent se concentrer sur la validation des contraintes et la diversité des diamètres.
