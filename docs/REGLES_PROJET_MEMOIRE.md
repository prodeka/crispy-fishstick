# 📋 RÈGLES ET MÉMOIRE DU PROJET LCPI

## 🎯 **PRÉFÉRENCES ET CONVENTIONS**

### **Structure des Dossiers**
- **Documentation** : Toujours dans `/docs`
- **Tests** : Toujours dans `/tests`
- **Exemples** : Dans `/examples`
- **Templates** : Dans `/src/lcpi/templates_project/`
- **Guides** : Dans `/docs`
- **Rapports** : Dans `/output` ou `/reports`

### **Conventions de Nommage**
- **Fichiers Python** : `snake_case.py`
- **Classes** : `PascalCase`
- **Fonctions** : `snake_case`
- **Variables** : `snake_case`
- **Constantes** : `UPPER_SNAKE_CASE`

### **Versions**
- **Format** : `X.Y.Z` (Semantic Versioning)
- **Majeur** : Changements incompatibles
- **Mineur** : Nouvelles fonctionnalités
- **Patch** : Corrections de bugs

## 🔧 **FONCTIONNALITÉS IDENTIFIÉES**

### **Modules Principaux**
1. **AEP** (Adduction Eau Potable)
   - Hardy-Cross method
   - Population calculations
   - Demand calculations
   - Pumping systems
   - Reservoir design

2. **CM** (Construction Métallique)
   - Steel structures
   - Connections
   - Load calculations

3. **Bois** (Wood Construction)
   - Timber structures
   - Joints
   - Load calculations

4. **Béton** (Concrete)
   - Reinforced concrete
   - Foundations
   - Structural analysis

5. **Hydrodrain** (Hydraulics & Drainage)
   - Canal design
   - Stormwater management
   - Hydraulic calculations

### **Fonctionnalités Globales**
- **Base de données globale** : `db_manager.py`
- **Auto-complétion** : CLI et REPL
- **Rapports globaux** : Pandoc integration
- **Licence système** : Validation et gestion

## 🚨 **PROBLÈMES IDENTIFIÉS**

### **1. Algorithme Hardy-Cross Simplifié**
- **Problème** : `_identify_loops()` limité à 5 boucles
- **Cause** : Algorithme simplifié pour éviter la complexité
- **Solution** : Implémenter un algorithme de recherche de cycles avancé

### **2. Nouveaux Dossiers Détectés**
- **EPANET2.2-master** : Logiciel de simulation hydraulique
- **pyswmm-2.0.1** : Interface Python pour SWMM
- **swmm-python-dev** : Développement SWMM Python

## 📚 **NOUVELLES FONCTIONNALITÉS POTENTIELLES**

### **EPANET Integration**
- **Objectif** : Intégrer EPANET pour la simulation hydraulique
- **Avantages** : Standard industriel, validation des calculs
- **Implémentation** : Wrapper Python, interface CLI

### **SWMM Integration**
- **Objectif** : Gestion des eaux pluviales
- **Avantages** : Modélisation avancée, EPA standard
- **Implémentation** : Via pyswmm, calculs de drainage

## 🔄 **PLAN D'ACTION**

### **Phase 1 : Amélioration Hardy-Cross**
1. Implémenter algorithme de recherche de cycles avancé
2. Supprimer limitation à 5 boucles
3. Ajouter validation des boucles identifiées

### **Phase 2 : Intégration EPANET**
1. Analyser structure EPANET2.2-master
2. Créer wrapper Python
3. Intégrer dans CLI LCPI

### **Phase 3 : Intégration SWMM**
1. Analyser pyswmm et swmm-python-dev
2. Créer module drainage avancé
3. Intégrer calculs eaux pluviales

### **Phase 4 : Vérification Init**
1. Vérifier import des exemples
2. Vérifier import des guides
3. Vérifier import des templates
4. Corriger si nécessaire

## 📝 **NOTES TECHNIQUES**

### **Algorithme de Recherche de Cycles Avancé**
```python
def advanced_cycle_detection(graph):
    """
    Algorithme de recherche de cycles basé sur DFS
    avec détection de tous les cycles simples
    """
    # Implémentation à développer
    pass
```

### **Intégration EPANET**
```python
def epanet_simulation(network_data):
    """
    Utilise EPANET pour valider les calculs Hardy-Cross
    """
    # Implémentation à développer
    pass
```

### **Intégration SWMM**
```python
def swmm_drainage_calculation(rainfall_data):
    """
    Utilise SWMM pour les calculs de drainage
    """
    # Implémentation à développer
    pass
```

## 🎯 **OBJECTIFS PRIORITAIRES**

1. **Améliorer Hardy-Cross** : Supprimer limitation boucles
2. **Analyser nouveaux dossiers** : EPANET, SWMM
3. **Vérifier fonction init** : Exemples, guides, templates
4. **Implémenter intégrations** : EPANET et SWMM dans LCPI

---
*Dernière mise à jour : 2025-08-04*
*Version LCPI : 2.1.0* 