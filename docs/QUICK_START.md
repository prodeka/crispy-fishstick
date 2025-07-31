# 🚀 Guide de Démarrage Rapide - LCPI-CLI

## Installation en 5 Minutes

### 1. **Installation Automatique**
```bash
# Windows
python scripts\install_wizard.py

# macOS/Linux
python scripts/install_wizard.py
```

### 2. **Installation Manuelle**
```bash
# Installer les dépendances
pip install -r requirements.txt

# Installer LCPI-CLI
pip install -e .

# Vérifier l'installation
lcpi doctor
```

## Première Utilisation

### 1. **Vérifier l'Installation**
```bash
lcpi --help
lcpi doctor
```

### 2. **Activer les Plugins**
```bash
# Voir les plugins disponibles
lcpi plugins list

# Activer un plugin
lcpi plugins install beton
lcpi plugins install hydro
```

### 3. **Créer votre Premier Projet**
```bash
# Initialiser un projet
lcpi init mon_projet_ingenierie

# Aller dans le projet
cd mon_projet_ingenierie
```

## Exemples Rapides

### **Béton Armé**
```bash
# Calcul de poteau
lcpi beton calc-poteau poteaux.yml

# Mode interactif
lcpi beton interactive
```

### **Hydrologie**
```bash
# Dimensionnement de canal
lcpi hydro ouvrage canal canal.yml

# Analyse pluviométrique
lcpi hydro pluvio analyser pluies.csv
```

### **Construction Métallique**
```bash
# Calcul de poutre
lcpi cm poutre poutre.yml
```

## Commandes Utiles

### **Aide et Guides**
```bash
lcpi tips          # Astuces quotidiennes
lcpi guide         # Guides interactifs
lcpi examples      # Exemples d'utilisation
lcpi welcome       # Message de bienvenue
```

### **Gestion des Projets**
```bash
lcpi init projet   # Nouveau projet
lcpi report        # Générer un rapport
lcpi shell         # Mode interactif
```

### **Diagnostic**
```bash
lcpi doctor        # Vérifier l'installation
lcpi plugins list  # Voir les plugins
```

## Structure de Projet Recommandée

```
mon_projet/
├── data/              # Données d'entrée
│   ├── pluies.csv
│   └── poteaux.yml
├── elements/          # Fichiers YAML
│   ├── canal.yml
│   └── poutre.yml
├── output/            # Résultats
│   ├── rapports/
│   └── graphiques/
└── docs/              # Documentation
    └── README.md
```

## Astuces de Productivité

### **1. Utilisez le Shell Interactif**
```bash
lcpi shell
# Maintenant vous pouvez taper directement:
> beton calc-poteau poteaux.yml
> hydro ouvrage canal canal.yml
> exit
```

### **2. Activez les Plugins selon vos Besoins**
```bash
# Pour le béton armé
lcpi plugins install beton

# Pour l'hydrologie
lcpi plugins install hydro

# Pour la construction métallique
lcpi plugins install cm
```

### **3. Utilisez les Templates**
```bash
# Projet avec template
lcpi init hangar --template hangar-mixte
```

### **4. Générez des Rapports**
```bash
# Rapport PDF
lcpi report --format pdf

# Rapport JSON
lcpi report --format json
```

## Dépannage Rapide

### **Problème: Commande 'lcpi' non reconnue**
```bash
# Réinstaller
pip install -e .
lcpi doctor
```

### **Problème: Plugin non trouvé**
```bash
# Activer le plugin
lcpi plugins install <nom_plugin>
lcpi plugins list
```

### **Problème: Erreur de licence**
```bash
# Vérifier la licence
cat ~/.lcpi/license.key
# Contactez le support si nécessaire
```

### **Problème: Dépendances manquantes**
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
lcpi doctor
```

## Ressources

### **Documentation**
- `docs/GUIDE_UTILISATION.md` - Guide complet
- `docs/NOUVELLES_FONCTIONNALITES.md` - Nouvelles fonctionnalités
- `docs/API_DOCUMENTATION.md` - Documentation technique

### **Exemples**
- `examples/` - Fichiers d'exemple
- `lcpi examples` - Exemples interactifs

### **Support**
- Email: support@lcpi-cli.com
- Téléphone: +33 1 23 45 67 89
- Documentation: `docs/`

## Prochaines Étapes

1. **Explorez les plugins** selon votre domaine
2. **Créez votre premier projet** avec `lcpi init`
3. **Testez les calculs** avec vos données
4. **Générez des rapports** pour présenter vos résultats
5. **Consultez la documentation** pour des fonctionnalités avancées

---

**💡 Conseil:** Utilisez `lcpi tips` chaque jour pour découvrir de nouvelles astuces ! 