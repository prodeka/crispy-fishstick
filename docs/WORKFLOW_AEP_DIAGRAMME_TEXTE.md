# 📊 Diagramme de Workflow AEP - Format Texte

## 🔄 Workflow Principal

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WORKFLOW AEP LCPI v2.1.0                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐
│ 📁 DONNÉES  │
│   D'ENTRÉE  │
│ YAML/CSV    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 🔍 DIAGNOSTIC│
│ PRÉLIMINAIRE│
│ NetworkUtils│
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ ✅ RÉSEAU   │
│   VALIDE ?  │
└─────┬───────┘
      │
      ├─❌ NON──┐
      │         ▼
      │   ┌─────────────┐
      │   │ 🚨 RAPPORT  │
      │   │   D'ERREUR  │
      │   │Recommandations│
      │   └─────┬───────┘
      │         │
      │         ▼
      │   ┌─────────────┐
      │   │ 🔄 RETOUR   │
      │   │  UTILISATEUR│
      │   │Correction   │
      │   └─────┬───────┘
      │         │
      │         ▼
      │   ┌─────────────┐
      │   │ 📁 DONNÉES  │
      │   │   D'ENTRÉE  │
      │   │ YAML/CSV    │
      │   └─────────────┘
      │
      ▼
┌─────────────┐
│ ⚡ SIMULATION│
│ HARDY-CROSS │
│Enhanced     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 🌐 SIMULATION│
│   EPANET    │
│Simulator    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ ✅ EPANET   │
│  RÉUSSI ?   │
└─────┬───────┘
      │
      ├─❌ NON──┐
      │         ▼
      │   ┌─────────────┐
      │   │ ⚠️ RAPPORT  │
      │   │  ERREUR     │
      │   │EPANET       │
      │   └─────┬───────┘
      │         │
      │         ▼
      │   ┌─────────────┐
      │   │ 🔄 RETOUR   │
      │   │  UTILISATEUR│
      │   │Correction   │
      │   └─────┬───────┘
      │         │
      │         ▼
      │   ┌─────────────┐
      │   │ 📁 DONNÉES  │
      │   │   D'ENTRÉE  │
      │   │ YAML/CSV    │
      │   └─────────────┘
      │
      ▼
┌─────────────┐
│ 🔄 VALIDATION│
│   CROISÉE   │
│HC vs EPANET │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 📋 GÉNÉRATION│
│   RAPPORTS  │
│Markdown/JSON│
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 🎯 RAPPORTS │
│    FINAUX   │
│Résultats    │
└─────────────┘
```

## 🔍 Points de Contrôle Détaillés

### Point de Contrôle 1 : Validation du Réseau
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        POINT DE CONTRÔLE 1: RÉSEAU VALIDE                   │
└─────────────────────────────────────────────────────────────────────────────┘

Vérifications Effectuées:
├─ ✅ Présence de sources d'eau (réservoirs/tanks)
├─ ✅ Connectivité du réseau (composantes connexes)
├─ ✅ Validité des dimensions des conduites
├─ ✅ Cohérence des demandes
└─ ✅ Compatibilité EPANET

Décision:
├─ VALIDE → Continuer vers Hardy-Cross
└─ INVALIDE → Arrêt avec recommandations
```

### Point de Contrôle 2 : Succès EPANET
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      POINT DE CONTRÔLE 2: EPANET RÉUSSI                     │
└─────────────────────────────────────────────────────────────────────────────┘

Vérifications Effectuées:
├─ ✅ Ouverture du fichier .inp
├─ ✅ Résolution des équations hydrauliques
├─ ✅ Extraction des résultats
└─ ✅ Fermeture propre du projet

Erreurs Possibles:
├─ Erreur 110: Équations insolubles → Diagnostic automatique
├─ Erreur 6: Pressions négatives → Avertissement
└─ Autres erreurs → Messages détaillés

Décision:
├─ RÉUSSI → Continuer vers validation croisée
└─ ÉCHEC → Arrêt avec diagnostic
```

## 📊 Flux de Données

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INPUT     │    │  PROCESSING │    │   OUTPUT    │
│             │    │             │    │             │
│ network.yml │───▶│ Diagnostic  │───▶│ Rapport     │
│ network.csv │    │ Hardy-Cross │    │ Markdown    │
│             │    │ EPANET      │    │ JSON        │
│             │    │ Comparaison │    │ HTML        │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Validation  │    │ Résultats   │    │ Rapports    │
│ Structure   │    │ Intermédiaires│   │ Finaux      │
│ Données     │    │ Convergence │    │ Comparaisons│
│ Format      │    │ Statistiques│    │ Recommandations│
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🔄 Boucles de Retour

### Boucle 1 : Correction des Données
```
┌─────────────┐
│ ❌ ERREUR   │
│ DIAGNOSTIC  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 💡 RECOMMAN-│
│   DATIONS   │
│ Correction  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 🔄 RETOUR   │
│ UTILISATEUR │
│ Modifier    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 📁 NOUVELLES│
│   DONNÉES   │
│ YAML/CSV    │
└─────────────┘
```

### Boucle 2 : Correction EPANET
```
┌─────────────┐
│ ❌ ERREUR   │
│   EPANET    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 🔍 DIAGNOSTIC│
│   DÉTAILLÉ  │
│ Causes      │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 💡 RECOMMAN-│
│   DATIONS   │
│ Correction  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 🔄 RETOUR   │
│ UTILISATEUR │
│ Modifier    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 📁 NOUVELLES│
│   DONNÉES   │
│ YAML/CSV    │
└─────────────┘
```

## ⏱️ Timeline Typique

```
Temps: 0s    1s    2s    5s    10s   15s   20s   25s   30s
      │     │     │     │     │     │     │     │     │
      ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│Charg│ │Diag │ │Hardy│ │EPAN │ │Comp │ │Rapp │ │Fin  │ │Done │
│ement│ │nost │ │Cross│ │ET   │ │arai │ │orts │ │al   │ │     │
└─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
```

## 🎯 Métriques de Performance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MÉTRIQUES DE PERFORMANCE                          │
└─────────────────────────────────────────────────────────────────────────────┘

Temps par Étape (réseau moyen 100-500 nœuds):
├─ Chargement des données:     0.1 - 1.0 secondes
├─ Diagnostic préliminaire:    0.5 - 2.0 secondes
├─ Simulation Hardy-Cross:     1.0 - 30.0 secondes
├─ Simulation EPANET:          0.5 - 10.0 secondes
├─ Validation croisée:         0.1 - 1.0 secondes
└─ Génération rapports:        0.5 - 2.0 secondes

Temps Total Typique:
├─ Réseau petit (<100 nœuds):  2-5 secondes
├─ Réseau moyen (100-1000):    5-45 secondes
├─ Réseau grand (1000-10000):  45-300 secondes
└─ Très grand (>10000):        300+ secondes

Mémoire Utilisée:
├─ Données réseau:             1-10 MB
├─ Résultats intermédiaires:   5-50 MB
├─ Rapports finaux:            1-5 MB
└─ Total typique:              10-100 MB
```

## 🔧 Points d'Extension

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           POINTS D'EXTENSION                                │
└─────────────────────────────────────────────────────────────────────────────┘

Extensions Possibles:
├─ 🔗 Interface Graphique (GUI)
│   ├─ Visualisation du réseau
│   ├─ Édition interactive
│   └─ Résultats graphiques
│
├─ 📊 Analyse Avancée
│   ├─ Analyse de sensibilité
│   ├─ Optimisation automatique
│   └─ Scénarios multiples
│
├─ 🌐 Intégration Web
│   ├─ API REST
│   ├─ Interface web
│   └─ Collaboration en ligne
│
├─ 📈 Machine Learning
│   ├─ Prédiction de convergence
│   ├─ Optimisation automatique
│   └─ Détection d'anomalies
│
└─ 🔄 Workflow Avancé
    ├─ Pipeline de traitement
    ├─ Intégration continue
    └─ Déploiement automatique
``` 