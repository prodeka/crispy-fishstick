# Guide de Diagnostic - Conservation des Débits

## 🎯 Objectif
Diagnostiquer et résoudre les violations de conservation de masse dans les réseaux hydrauliques EPANET/WNTR.

## 📋 Problèmes Identifiés
- **Conservation de masse violée**: `Total (conservation): -1.202 m³/s` ≠ 0
- **Diamètres uniformes**: Toutes les conduites à 200mm (suspect)
- **Contraintes non respectées**: Vitesse max > 5 m/s malgré `constraints_ok: true`

## 🔧 Outils Disponibles

### 1. Script de Diagnostic Automatique
```bash
python tools/diagnose_flow_conservation.py <network.inp> [options]
```

### 2. Script de Vérification des Débits
```bash
python tools/check_flows.py <network.inp> --simulator epanet --save-plot --show
```

### 3. Script d'Inspection Rapide
```bash
python tools/quick_inspect.py results/optimization.json
```

## 📊 Étapes de Diagnostic

### Étape 1: Simulation EPANET Unique
**Objectif**: Vérifier si le problème vient du parsing initial de l'INP

```bash
# Simulation directe avec EPANET
.\venv_new\Scripts\python.exe -m lcpi.aep.cli simulate-inp .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --format json --output .\results\sim_one.json --verbose
```

**Interprétation**:
- Si `sum(flows) ≈ 0` → Le parsing INP est correct
- Si `sum(flows) ≠ 0` → Problème dans l'orientation des conduites

### Étape 2: Diagnostic Automatique Complet
**Objectif**: Analyse complète avec comparaison

```bash
# Diagnostic complet avec comparaison
python tools/diagnose_flow_conservation.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --optimization .\results\test_integrated_stats.json
```

**Résultats attendus**:
- Rapport Markdown avec diagnostic
- Plots d'évolution temporelle
- Comparaison EPANET vs Optimisation

### Étape 3: Vérification avec check_flows.py
**Objectif**: Analyse détaillée avec WNTR/EPANET

```bash
# Diagnostic avec EPANET (recommandé)
python tools/check_flows.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --simulator epanet --save-plot --show

# Diagnostic avec WNTR pour sous-ensemble
python tools/check_flows.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --simulator wntr --links "P1,P2,P3" --sample 10 --no-json-series
```

### Étape 4: Inspection des Résultats d'Optimisation
**Objectif**: Vérifier les métriques clés

```bash
# Inspection rapide
python tools/quick_inspect.py .\results\test_integrated_stats.json
```

**Métriques à vérifier**:
- `total_flow`: Somme des débits
- `diameters_count`: Nombre de diamètres
- `unique_diameters`: Diversité des diamètres
- `price_db.type` et `price_db.source`: Source des diamètres

## 🔍 Causes Possibles

### 1. Sens de Conduite Arbitraire
**Symptôme**: Débits négatifs nombreux
**Cause**: Orientation définie dans l'INP ne correspond pas au sens réel
**Solution**: Vérifier l'ordre des nœuds dans les sections `[PIPES]`

### 2. Exports WNTR Mal Agrégés
**Symptôme**: Somme non nulle même avec EPANET brut
**Cause**: Problème de parsing des résultats WNTR
**Solution**: Comparer avec EPANET GUI ou utiliser `EpanetSimulator`

### 3. Modifications d'Orientations par Optimisation
**Symptôme**: EPANET OK mais optimisation NOK
**Cause**: Réparation/optimisation modifie les diamètres/orientations
**Solution**: Vérifier la logique de réparation dans `_ensure_at_least_one_feasible`

### 4. Demandes Dynamiques Non Équilibrées
**Symptôme**: Somme variable dans le temps
**Cause**: Consommation variable non compensée
**Solution**: Vérifier les patterns de demande dans l'INP

### 5. PriceDB Manquante ou Incohérente
**Symptôme**: Tous les diamètres identiques (200mm)
**Cause**: Base de données des prix non chargée
**Solution**: Vérifier `price_db_info` et le fallback

## 🛠️ Actions Correctives

### Pour les Diamètres Uniformes
1. **Vérifier la PriceDB**:
   ```bash
   python tools/quick_inspect.py results/test_integrated_stats.json | grep price_db
   ```

2. **Forcer l'utilisation de diamètres variés**:
   - Modifier `src/lcpi/aep/optimizer/controllers.py`
   - Ajouter un fallback avec diamètres standards: `[50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]`

### Pour la Conservation de Masse
1. **Vérifier l'orientation des conduites**:
   - Ouvrir l'INP et vérifier l'ordre des nœuds
   - Comparer avec EPANET GUI

2. **Analyser les débits négatifs**:
   - Un débit négatif = écoulement inverse au sens défini
   - Normal pour certaines configurations

3. **Vérifier les demandes**:
   - S'assurer que la somme des demandes = somme des entrées

### Pour les Contraintes Non Respectées
1. **Vérifier l'application des contraintes**:
   - S'assurer que `apply_constraints_to_result` est appelé après simulation
   - Vérifier que `constraints_ok` est mis à `False` si violation

## 📈 Interprétation des Résultats

### Seuils de Tolérance
- **Conservation de masse**: `|sum(flows)| < 1e-3 m³/s`
- **Vitesse max**: `velocity < 5.0 m/s`
- **Pression min**: `pressure > 0.0 m`

### Codes de Statut
- ✅ **OK**: Toutes les contraintes respectées
- ⚠️ **WARNING**: Violation mineure (tolérance)
- ❌ **ERROR**: Violation majeure (non tolérable)

## 🚀 Exécution Recommandée

```bash
# 1. Diagnostic complet automatique
python tools/diagnose_flow_conservation.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --optimization .\results\test_integrated_stats.json

# 2. Vérification avec check_flows
python tools/check_flows.py .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --simulator epanet --save-plot

# 3. Inspection des résultats
python tools/quick_inspect.py .\results\test_integrated_stats.json
```

## 📝 Fichiers de Sortie

### Diagnostic Automatique
- `results/bismark-Administrator_epanet_sim.json`: Simulation EPANET
- `results/bismark-Administrator_flow_conservation_report.md`: Rapport complet
- `results/bismark-Administrator_sumflows_*.json`: Données de diagnostic

### Check_flows
- `results/bismark-Administrator_sumflows_epanet.csv`: Évolution temporelle
- `results/bismark-Administrator_sumflows_epanet.png`: Plot de conservation
- `results/bismark-Administrator_sumflows_epanet_report.md`: Rapport détaillé

## 🔄 Workflow de Correction

1. **Diagnostic initial** → Identifier la cause
2. **Correction ciblée** → Modifier le code source
3. **Test de régression** → Relancer l'optimisation
4. **Validation** → Vérifier que les problèmes sont résolus
5. **Documentation** → Mettre à jour ce guide

## 📞 Support

En cas de problème persistant:
1. Vérifier les logs dans `logs/`
2. Comparer avec EPANET GUI
3. Tester avec un réseau simple
4. Consulter la documentation WNTR/EPANET
