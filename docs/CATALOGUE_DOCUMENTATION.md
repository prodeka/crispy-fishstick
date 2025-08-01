# 📚 Catalogue de Documentation LCPI-CLI

## Vue d'ensemble

LCPI-CLI (Plateforme de Calcul Polyvalent pour l'Ingénierie) est une suite logicielle complète pour les calculs d'ingénierie dans les domaines de la construction métallique, bois, béton armé et hydrologie.

## 📖 Documentation Technique

### 🏗️ Modules de Calcul

#### Construction Métallique (CM)
- **Eurocode 3** - Calculs selon les normes européennes
- **Vérifications** : Poteaux, poutres, assemblages
- **Optimisation** : Sections, assemblages
- **Fichiers** : `src/lcpi/cm/`

#### Construction Bois
- **Eurocode 5** - Calculs selon les normes européennes
- **Vérifications** : Poteaux, poutres, assemblages
- **Types d'assemblages** : Pointes, embrevement
- **Fichiers** : `src/lcpi/bois/`

#### Béton Armé
- **Eurocode 2** - Calculs selon les normes européennes
- **Vérifications** : Poteaux, radiers
- **Armatures** : Longitudinales et transversales
- **Fichiers** : `src/lcpi/beton/`

#### Hydrologie et Assainissement
- **Dimensionnement** : Canaux, réservoirs
- **Analyse pluviométrique** : Courbes IDF
- **Assainissement** : Réseaux gravitaires
- **Fichiers** : `src/lcpi/hydrodrain/`

### 🔧 Architecture Technique

#### Structure du Projet
```
src/lcpi/
├── main.py              # Application principale Typer
├── cli.py               # Point d'entrée CLI
├── cm/                  # Module Construction Métallique
├── bois/                # Module Construction Bois
├── beton/               # Module Béton Armé
├── hydrodrain/          # Module Hydrologie
├── utils/               # Utilitaires communs
├── templates/           # Templates de rapports
└── templates_project/   # Templates de projets
```

#### Système de Plugins
- **Chargement dynamique** des modules
- **Configuration** via `.plugins.json`
- **Extensibilité** pour nouveaux modules

#### Gestion des Licences
- **Système de licence** intégré
- **Validation** automatique au démarrage
- **Types** : Standard, Premium, Enterprise

## 📋 Guides Utilisateur

### 🚀 Démarrage Rapide
1. **Installation** : `pip install -e .`
2. **Vérification** : `lcpi doctor`
3. **Premier projet** : `lcpi init mon_projet`
4. **Calculs** : `lcpi cm check-poteau data.yml`

### 📁 Gestion des Projets
- **Initialisation** : `lcpi init [nom] [options]`
- **Templates** : cm, bois, beton, hydro, complet
- **Plugins** : Sélection personnalisée
- **Structure** : Arborescence automatique

### 🔌 Commandes Principales

#### Commandes Générales
```bash
lcpi --help              # Aide générale
lcpi doctor              # Diagnostic système
lcpi init projet         # Nouveau projet
lcpi plugins list        # Plugins disponibles
lcpi examples            # Exemples d'utilisation
```

#### Commandes de Calcul
```bash
# Construction Métallique
lcpi cm check-poteau fichier.yml
lcpi cm check-poutre fichier.yml
lcpi cm optimize-section

# Construction Bois
lcpi bois check-poteau fichier.yml
lcpi bois check-poutre fichier.yml

# Béton Armé
lcpi beton calc-poteau fichier.yml
lcpi beton calc-radier fichier.yml

# Hydrologie
lcpi hydro ouvrage canal fichier.yml
lcpi hydro reservoir equilibrage
```

## 📊 Formats de Données

### Format YAML
Tous les fichiers de données utilisent le format YAML :

```yaml
# Exemple de fichier de données
element_id: P1
description: "Description de l'élément"
parametres:
  valeur1: 10.0
  valeur2: "texte"
```

### Structure des Données
- **Métadonnées** : ID, description, version
- **Géométrie** : Dimensions, sections
- **Matériaux** : Caractéristiques mécaniques
- **Efforts** : Charges, moments, efforts
- **Paramètres** : Coefficients, limites

## 🎨 Interface Utilisateur

### Console Rich
- **Couleurs** : Sortie colorée et structurée
- **Panels** : Informations encadrées
- **Tables** : Données tabulaires
- **Barres de progression** : Avancement des calculs

### Mode Interactif
- **Shell intégré** : `lcpi shell`
- **Aide contextuelle** : `lcpi tips`
- **Guides interactifs** : `lcpi guide`

## 📈 Rapports et Sorties

### Formats Supportés
- **PDF** : Rapports détaillés
- **HTML** : Rapports web
- **JSON** : Données structurées
- **Console** : Affichage direct

### Templates de Rapports
- **Default** : Rapport standard
- **Enhanced** : Rapport amélioré
- **Technical** : Rapport technique
- **Custom** : Templates personnalisés

## 🔒 Sécurité et Licences

### Système de Licence
- **Validation** : Vérification automatique
- **Types** : Standard, Premium, Enterprise
- **Durée** : Licences temporaires et permanentes
- **Utilisateurs** : Gestion multi-utilisateurs

### Sécurité des Données
- **Validation** : Vérification des entrées
- **Encodage** : UTF-8 obligatoire
- **Erreurs** : Gestion robuste des exceptions

## 🛠️ Développement

### Architecture
- **Modulaire** : Plugins indépendants
- **Extensible** : Ajout facile de modules
- **Maintenable** : Code structuré et documenté
- **Testable** : Tests unitaires et d'intégration

### Standards de Code
- **PEP 8** : Style Python
- **Type Hints** : Annotations de types
- **Docstrings** : Documentation inline
- **Tests** : Couverture de code

### Contribution
- **Git** : Gestion de versions
- **Issues** : Suivi des problèmes
- **Pull Requests** : Contributions
- **Documentation** : Mise à jour continue

## 📚 Références

### Normes et Standards
- **Eurocode 3** : Construction métallique
- **Eurocode 5** : Construction bois
- **Eurocode 2** : Béton armé
- **Standards hydrauliques** : Dimensionnement

### Bibliothèques Utilisées
- **Typer** : Interface CLI
- **Rich** : Affichage console
- **PyYAML** : Gestion YAML
- **Pandas** : Manipulation données
- **NumPy** : Calculs numériques

## 🔗 Liens Utiles

### Documentation
- [Guide de démarrage](QUICK_START.md)
- [Documentation technique](DOCUMENTATION_TECHNIQUE.md)
- [API Reference](API_DOCUMENTATION.md)
- [Exemples d'utilisation](examples/)

### Support
- [Issues GitHub](https://github.com/lcpi/issues)
- [Discussions](https://github.com/lcpi/discussions)
- [Wiki](https://github.com/lcpi/wiki)

### Licence
- [LICENSE.md](LICENSE.md)
- [DISCLAIMER.md](DISCLAIMER.md)
- [PRIVACY.md](PRIVACY.md)

---

**Version** : 2.0.0  
**Dernière mise à jour** : 2025-08-01  
**Auteur** : Équipe LCPI-CLI 