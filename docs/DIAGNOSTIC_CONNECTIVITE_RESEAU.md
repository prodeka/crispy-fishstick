# 🔍 Diagnostic de Connectivité Réseau - Guide Complet

## 📋 Vue d'ensemble

Ce module fournit des outils de diagnostic automatique de connectivité réseau pour prévenir l'**erreur EPANET 110** "cannot solve network hydraulic equations". Il analyse la structure du réseau avant l'exécution d'EPANET pour identifier les problèmes de connectivité.

## 🎯 Problème Résolu

### Erreur EPANET 110
- **Symptôme** : EPANET échoue avec l'erreur "cannot solve network hydraulic equations"
- **Cause** : Problèmes de connectivité réseau (composantes orphelines, absence de sources d'eau)
- **Solution** : Diagnostic automatique avant simulation EPANET

## 🚀 Utilisation Rapide

### 1. Diagnostic Simple

```python
from lcpi.aep.core.network_diagnostics import diagnose_network_connectivity

# Votre réseau au format LCPI
network_data = {
    "network": {
        "nodes": {
            "R1": {"type": "reservoir", "cote": 120, "demande": 0},
            "N1": {"type": "junction", "cote": 100, "demande": 10},
            # ... autres nœuds
        },
        "pipes": {
            "P1": {"noeud_amont": "R1", "noeud_aval": "N1", "longueur": 1000, "diametre": 0.3},
            # ... autres conduites
        }
    }
}

# Diagnostic de connectivité
is_connected = diagnose_network_connectivity(network_data)
print(f"Réseau connecté: {'✅' if is_connected else '❌'}")
```

### 2. Intégration EPANET avec Diagnostics

```python
from lcpi.aep.core.epanet_integration import run_epanet_with_diagnostics

# Simulation EPANET avec diagnostic automatique
results = run_epanet_with_diagnostics(network_data)

if results['success']:
    print("✅ Simulation EPANET réussie")
    print(f"Résultats: {results['epanet_results']}")
else:
    print("❌ Échec de la simulation")
    for error in results['errors']:
        print(f"  - {error}")
```

### 3. Diagnostic Complet

```python
from lcpi.aep.core.epanet_integration import quick_diagnostic

# Diagnostic complet sans simulation
diagnostic = quick_diagnostic(network_data)

print(f"Connectivité: {diagnostic['connectivity']}")
print(f"Compatible EPANET: {diagnostic['epanet_compatible']}")
print(f"Erreurs: {diagnostic['errors']}")
print(f"Avertissements: {diagnostic['warnings']}")
```

## 🔧 Fonctionnalités

### 1. Diagnostic de Connectivité (`diagnose_network_connectivity`)

**Fonction** : Analyse la connectivité du réseau et identifie les composantes orphelines.

**Retourne** : `bool` - `True` si le réseau est entièrement alimenté, `False` sinon.

**Détecte** :
- ✅ Sources d'eau (réservoirs, tanks)
- ✅ Composantes connexes
- ❌ Composantes orphelines (sans source d'eau)
- ❌ Réseaux sans source d'eau

**Exemple de sortie** :
```
🔍 DIAGNOSTIC DE CONNECTIVITÉ RÉSEAU
==================================================
📊 Statistiques du réseau:
   • Nœuds: 5
   • Conduites: 4

💧 Identification des sources d'eau...
   • Source d'eau trouvée: R1 (type: reservoir)

🔗 Analyse des composantes connexes...
   • Nombre de composantes connexes: 2
   ✅ Composante 1: 3 nœuds, alimentée par 1 source(s)
   ❌ Composante 2: 2 nœuds, AUCUNE SOURCE D'EAU

🚨 PROBLÈME DÉTECTÉ: 1 composante(s) orpheline(s)
   • Nœuds: ['N4', 'N5']
   • Sources les plus proches: []

💡 RECOMMANDATIONS:
   • Ajouter des réservoirs ou tanks dans les composantes orphelines
   • Vérifier la connectivité des conduites
```

### 2. Validation EPANET (`validate_epanet_compatibility`)

**Fonction** : Valide la compatibilité du réseau avec EPANET.

**Retourne** : `Dict` avec les résultats de validation.

**Vérifie** :
- ✅ Présence de sources d'eau
- ✅ Connectivité du réseau
- ✅ Validité des données de conduites
- ✅ Cohérence des demandes

### 3. Analyse Topologique (`analyze_network_topology`)

**Fonction** : Analyse approfondie de la topologie du réseau.

**Retourne** : `Dict` avec les métriques topologiques.

**Métriques** :
- Densité du réseau
- Degré moyen/min/max des nœuds
- Diamètre et rayon du réseau
- Points d'articulation
- Ponts (conduites critiques)

### 4. Intégration EPANET (`run_epanet_with_diagnostics`)

**Fonction** : Exécute EPANET avec diagnostic automatique.

**Étapes** :
1. 🔍 Diagnostic de connectivité
2. 🔧 Validation EPANET
3. 🔬 Analyse topologique
4. 📝 Génération fichier .inp
5. ⚡ Simulation EPANET
6. 🧹 Nettoyage

## 📊 Format des Données Réseau

### Structure Requise

```yaml
network:
  nodes:
    NODE_ID:
      type: "reservoir" | "junction" | "tank"
      cote: elevation  # en mètres
      demande: demand  # en L/s
      # ... autres propriétés
  
  pipes:
    PIPE_ID:
      noeud_amont: "FROM_NODE_ID"
      noeud_aval: "TO_NODE_ID"
      longueur: length  # en mètres
      diametre: diameter  # en mètres
      coefficient_rugosite: roughness
      # ... autres propriétés
```

### Formats Supportés

Le module supporte deux formats de clés pour les conduites :
- `noeud_amont` / `noeud_aval` (format LCPI standard)
- `from_node` / `to_node` (format alternatif)

## 🚨 Problèmes Détectés

### 1. Composantes Orphelines

**Symptôme** : Certaines parties du réseau ne sont pas connectées à une source d'eau.

**Exemple** :
```
🚨 PROBLÈME DÉTECTÉ: 1 composante(s) orpheline(s)
📋 Composante orpheline #2:
   • Taille: 2 nœuds
   • Nœuds: ['N4', 'N5']
   • Sources les plus proches: []
```

**Solution** :
- Ajouter un réservoir ou tank dans la composante orpheline
- Connecter la composante au réseau principal
- Vérifier la cohérence des IDs de nœuds

### 2. Absence de Source d'Eau

**Symptôme** : Aucun réservoir ou tank dans le réseau.

**Exemple** :
```
❌ ERREUR CRITIQUE: Aucune source d'eau (réservoir/tank) trouvée dans le réseau!
   EPANET nécessite au moins une source d'eau pour résoudre les équations hydrauliques.
```

**Solution** :
- Ajouter au moins un nœud de type "reservoir" ou "tank"
- S'assurer que le type est en minuscules

### 3. Réseau Non Connexe

**Symptôme** : Plusieurs composantes isolées.

**Solution** :
- Vérifier la connectivité des conduites
- S'assurer que tous les nœuds sont accessibles

## 🔧 Intégration dans le Workflow

### Avant (Problématique)

```python
# ❌ Approche risquée
epanet_simulator = EpanetSimulator()
epanet_simulator.open("network.inp")
epanet_simulator.solveH()  # Peut échouer avec erreur 110
```

### Après (Sécurisé)

```python
# ✅ Approche sécurisée
from lcpi.aep.core.epanet_integration import run_epanet_with_diagnostics

results = run_epanet_with_diagnostics(network_data)
if results['success']:
    # Traitement des résultats
    process_results(results['epanet_results'])
else:
    # Gestion des erreurs avec diagnostics détaillés
    handle_errors(results['errors'])
```

## 📁 Fichiers du Module

### Modules Principaux

- `src/lcpi/aep/core/network_diagnostics.py` - Fonctions de diagnostic
- `src/lcpi/aep/core/epanet_integration.py` - Intégration EPANET
- `scripts/test_network_diagnostics.py` - Tests unitaires
- `scripts/demo_epanet_diagnostics.py` - Démonstration complète

### Exemples

- `examples/reseau_test_avec_source.yml` - Réseau valide avec source d'eau
- `examples/hardy_cross_test.yml` - Réseau de test Hardy-Cross

## 🧪 Tests et Validation

### Exécution des Tests

```bash
# Test des fonctions de diagnostic
python scripts/test_network_diagnostics.py

# Démonstration complète
python scripts/demo_epanet_diagnostics.py
```

### Cas de Test

1. **Réseau Valide** : ✅ Devrait passer tous les diagnostics
2. **Réseau Orphelin** : ❌ Devrait détecter les composantes orphelines
3. **Réseau Sans Source** : ❌ Devrait détecter l'absence de source d'eau

## 💡 Bonnes Pratiques

### 1. Validation Précoce

```python
# Valider avant traitement
diagnostic = quick_diagnostic(network_data)
if not diagnostic['connectivity']:
    print("❌ Réseau non connecté - Correction nécessaire")
    return
```

### 2. Gestion d'Erreurs

```python
try:
    results = run_epanet_with_diagnostics(network_data)
    if results['success']:
        # Traitement normal
        pass
    else:
        # Log des erreurs pour analyse
        log_errors(results['errors'])
except Exception as e:
    print(f"Erreur critique: {e}")
```

### 3. Monitoring

```python
# Suivi des métriques de connectivité
topology = analyze_network_topology(network_data)
print(f"Densité réseau: {topology['densite']:.4f}")
print(f"Points critiques: {len(topology['points_articulation'])}")
```

## 🔮 Évolutions Futures

### Fonctionnalités Prévues

1. **Diagnostic Avancé** :
   - Détection de boucles problématiques
   - Analyse de stabilité hydraulique
   - Recommandations automatiques

2. **Interface Graphique** :
   - Visualisation des composantes
   - Carte de connectivité interactive
   - Outils de correction visuels

3. **Intégration CLI** :
   - Commandes de diagnostic dans LCPI CLI
   - Rapports automatiques
   - Export des diagnostics

### Améliorations Techniques

1. **Performance** :
   - Optimisation pour grands réseaux
   - Parallélisation des analyses
   - Cache des diagnostics

2. **Robustesse** :
   - Gestion d'erreurs avancée
   - Validation de données renforcée
   - Récupération automatique

## 📞 Support

### Problèmes Courants

1. **Import Error** : Vérifiez que le module est dans le PYTHONPATH
2. **Format Error** : Vérifiez la structure des données réseau
3. **EPANET Error** : Utilisez les diagnostics pour identifier le problème

### Ressources

- Documentation EPANET : [EPANET User Manual](https://www.epa.gov/water-research/epanet)
- NetworkX : [Documentation officielle](https://networkx.org/)
- LCPI AEP : Documentation du module AEP

---

**Auteur** : Assistant IA Claude  
**Date** : 2025-01-27  
**Version** : 1.0.0  
**Statut** : ✅ Opérationnel 