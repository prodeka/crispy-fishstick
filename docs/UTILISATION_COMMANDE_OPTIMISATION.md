# 🚀 Guide d'Utilisation de la Commande d'Optimisation

## 📋 **Commande Principale**

```bash
lcpi aep network-optimize-unified <fichier_reseau> [options]
```

## 🎯 **Paramètres Principaux**

### **Fichier d'Entrée**
- **Obligatoire** : Chemin vers le fichier réseau (.inp ou .yml)
- **Exemple** : `src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp`

### **Méthode d'Optimisation**
- `--method` ou `-m` : `genetic` | `nested` | `surrogate` | `global` | `multi-tank`
- **Défaut** : `nested`
- **Recommandé** : `nested` (plus rapide et fiable)

### **Solveur**
- `--solver` : `epanet` | `lcpi` | `mock`
- **Défaut** : `epanet`
- **Recommandé** : `epanet` (standard de l'industrie)

## 📊 **Génération de Rapports**

### **Nouvelles Options Disponibles**

#### 1. **Format du Rapport**
```bash
--report <format>
```
- **Formats supportés** : `html`, `md`, `pdf`
- **Exemple** : `--report md`

#### 2. **Dossier de Sortie des Rapports**
```bash
--report-output <dossier>
```
- **Défaut** : Même dossier que `--output`
- **Exemple** : `--report-output reports/`

### **Exemples d'Utilisation**

#### **Rapport Markdown dans le dossier par défaut**
```bash
lcpi aep network-optimize-unified bismark.inp \
  --method nested \
  --solver epanet \
  --output results/optimisation.json \
  --report md
```
**Résultat** : Le rapport sera généré dans `results/rapport_optimisation_epanet.md`

#### **Rapport HTML dans un dossier spécifique**
```bash
lcpi aep network-optimize-unified bismark.inp \
  --method nested \
  --solver epanet \
  --output results/optimisation.json \
  --report html \
  --report-output reports/
```
**Résultat** : Le rapport sera généré dans `reports/rapport_optimisation_epanet.html`

#### **Rapport PDF avec dossier personnalisé**
```bash
lcpi aep network-optimize-unified bismark.inp \
  --method nested \
  --solver epanet \
  --output results/optimisation.json \
  --report pdf \
  --report-output docs/rapports/
```
**Résultat** : Le rapport sera généré dans `docs/rapports/rapport_optimisation_epanet.pdf`

## ⚡ **Optimisation des Performances**

### **Contraintes Recommandées**
```bash
--pression-min 12      # Pression minimale en mètres
--vitesse-max 2.0      # Vitesse maximale en m/s
```

### **Paramètres Avancés**
```bash
--hard-vel             # Traiter la contrainte de vitesse comme "hard"
--verbose              # Affichage détaillé
```

## 🔍 **Suivi de la Progression**

### **Indicateurs Visuels**
- 🚀 **Démarrage** : Affichage des paramètres d'optimisation
- ⏳ **Progression** : Suivi des étapes pour les multi-solveurs
- 📊 **Génération** : Feedback sur la création des rapports
- ✅ **Terminé** : Confirmation de la génération

### **Exemple de Sortie**
```
🚀 Démarrage de l'optimisation avec nested et epanet...
📋 Contraintes: pression_min=12m, vitesse_max=2.0m/s
🔍 Validation du fichier INP...
✅ Fichier INP valide - Aucun problème détecté
📊 Génération du rapport MD...
📝 Génération du rapport Markdown...
✅ Rapport Markdown généré: results/rapport_optimisation_epanet.md
```

## 📁 **Structure des Fichiers de Sortie**

### **Fichier Principal**
- **Nom** : Spécifié par `--output`
- **Format** : JSON avec résultats d'optimisation
- **Contenu** : Propositions, métriques, contraintes

### **Rapports Générés**
- **HTML** : `rapport_optimisation_<solver>.html`
- **Markdown** : `rapport_optimisation_<solver>.md`
- **PDF** : `rapport_optimisation_<solver>.pdf`

## 🚨 **Dépannage**

### **Problème : Temps d'exécution long**
**Solutions** :
1. Utiliser `--method nested` (plus rapide)
2. Réduire la complexité des contraintes
3. Vérifier que le fichier INP est valide

### **Problème : Rapport non généré**
**Vérifications** :
1. L'option `--report` est-elle spécifiée ?
2. Le dossier de sortie existe-t-il ?
3. Y a-t-il des erreurs dans la console ?

### **Problème : Fichier INP invalide**
**Solutions** :
1. Le validateur automatique corrige les problèmes
2. Vérifier les sections vides
3. Contrôler la cohérence des unités

## 💡 **Bonnes Pratiques**

### **1. Organisation des Fichiers**
```
projet/
├── input/
│   └── bismark.inp
├── results/
│   └── optimisation.json
└── reports/
    ├── rapport_optimisation_epanet.html
    ├── rapport_optimisation_epanet.md
    └── rapport_optimisation_epanet.pdf
```

### **2. Commandes Recommandées**
```bash
# Optimisation rapide avec rapport Markdown
lcpi aep network-optimize-unified input/bismark.inp \
  --method nested \
  --solver epanet \
  --pression-min 12 \
  --vitesse-max 2.0 \
  --output results/optimisation.json \
  --report md

# Optimisation avec rapport HTML dans un dossier dédié
lcpi aep network-optimize-unified input/bismark.inp \
  --method nested \
  --solver epanet \
  --pression-min 12 \
  --vitesse-max 2.0 \
  --output results/optimisation.json \
  --report html \
  --report-output reports/
```

### **3. Validation Automatique**
- ✅ **INP** : Validation et nettoyage automatiques
- ✅ **Courbes orphelines** : Commentées automatiquement
- ✅ **Sections vides** : Détectées et signalées
- ✅ **Warnings wntr** : Éliminés automatiquement

## 🔮 **Fonctionnalités Futures**

### **Prochaines Améliorations**
- 📊 **Barre de progression** en temps réel
- 🎯 **Estimation du temps** restant
- 📈 **Métriques de performance** détaillées
- 🔄 **Rapports automatiques** après chaque optimisation

### **Intégrations Prévues**
- 📧 **Envoi automatique** des rapports par email
- 🌐 **Interface web** pour visualisation
- 📱 **Notifications** push sur mobile
- 🔗 **Intégration** avec des outils de gestion de projet

## 📝 **Conclusion**

La commande d'optimisation offre maintenant :
- ✅ **Génération de rapports** dans 3 formats (HTML, Markdown, PDF)
- ✅ **Contrôle précis** du dossier de sortie des rapports
- ✅ **Feedback utilisateur** amélioré avec indicateurs visuels
- ✅ **Validation automatique** des fichiers INP
- ✅ **Performance optimisée** avec la méthode `nested`

Utilisez `--report-output` pour organiser vos rapports et profitez du feedback détaillé pour suivre la progression de vos optimisations ! 🎯
