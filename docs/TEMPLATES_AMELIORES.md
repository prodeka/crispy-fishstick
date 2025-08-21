# 🎨 Templates Améliorés pour network-optimize-unified

Ce document décrit les templates améliorés créés pour la commande `network-optimize-unified` de LCPI, offrant des rapports riches en style CSS, JavaScript et HTML avec une intégration complète des tableaux de données.

## 📋 Vue d'ensemble

Les templates améliorés offrent trois formats de sortie :

1. **HTML Interactif** (`network_optimize_unified_enhanced.html`) - Interface web moderne avec onglets et animations
2. **Markdown Structuré** (`network_optimize_unified_enhanced.md`) - Documentation technique complète
3. **PDF Professionnel** (`network_optimize_unified_pdf_enhanced.jinja2`) - Rapport imprimable avec mise en page optimisée

## 🚀 Fonctionnalités

### ✨ Interface HTML Moderne
- **Design responsive** avec CSS Grid et Flexbox
- **Navigation par onglets** pour organiser l'information
- **Animations CSS** et transitions fluides
- **Icônes FontAwesome** pour une meilleure lisibilité
- **Thème coloré** avec variables CSS personnalisables
- **Export PDF/CSV** intégré (JavaScript)

### 📊 Intégration Complète des Tableaux
Tous les templates incluent les tableaux suivants :

#### 🏗️ Structure du Réseau
- **Énumération des Tronçons** : DC_ID, longueur, NODE1, NODE2
- **Dimensionnement des Tronçons** : DC_ID, longueur, Qd, DN, V, ΔH
- **Dimensionnement des Nœuds** : JUNCTIONS, X, Y, Z, P_réel
- **Récapitulatif du Réservoir** : 14 paramètres complets

#### 🔄 Comparaisons et Validation
- **Comparatif Diamètres et Débits** : Calculé vs EPANET
- **Comparatif Vitesses et Pertes** : Calculé vs EPANET
- **Comparatif des Pressions** : Calculé vs EPANET
- **Récapitulatif des Diamètres** : Distribution par type

#### 💰 Analyse Financière
- **Devis Estimatif et Quantitatif** : Nomenclature complète avec prix

#### 📈 Statistiques Hydrauliques
- **Pressions** : min, max, moyenne, médiane, quartiles, pourcentages
- **Vitesses** : statistiques complètes des écoulements
- **Débits** : analyse des sens d'écoulement (normal/inverse)
- **Diamètres** : distribution et analyse des conduites
- **Pertes de charge** : analyse des pertes hydrauliques
- **Indice de performance** : métrique globale d'optimisation

## 🛠️ Installation et Utilisation

### Prérequis
```bash
pip install jinja2 weasyprint
```

### Utilisation Directe
```python
from lcpi.reporting.network_optimize_unified_pdf_generator import NetworkOptimizeUnifiedPDFGenerator

# Créer le générateur
generator = NetworkOptimizeUnifiedPDFGenerator()

# Générer un rapport PDF
pdf_content = generator.generate_pdf_report(
    result_data=your_data,
    input_file="network.inp",
    version="1.0.0"
)
```

### Intégration CLI
```bash
# Générer un rapport HTML
python -m lcpi.aep.cli network-optimize-unified input.inp --report html

# Générer un rapport Markdown
python -m lcpi.aep.cli network-optimize-unified input.inp --report md

# Générer un rapport PDF
python -m lcpi.aep.cli network-optimize-unified input.inp --report pdf
```

## 📁 Structure des Fichiers

```
src/lcpi/reporting/
├── templates/
│   ├── network_optimize_unified_enhanced.html          # Template HTML interactif
│   ├── network_optimize_unified_enhanced.md            # Template Markdown
│   └── network_optimize_unified_pdf_enhanced.jinja2   # Template PDF
├── network_optimize_unified_pdf_generator.py           # Générateur PDF
└── table_templates.py                                  # Définitions des tableaux

tools/
├── test_enhanced_templates.py                          # Tests des templates
└── demo_enhanced_templates.py                          # Démonstration complète
```

## 🧪 Tests et Validation

### Test des Templates
```bash
cd tools
python test_enhanced_templates.py
```

### Démonstration Complète
```bash
cd tools
python demo_enhanced_templates.py
```

## 🎨 Personnalisation

### Variables CSS
Les templates utilisent des variables CSS pour faciliter la personnalisation :

```css
:root {
    --primary-color: #2563eb;      /* Couleur principale */
    --secondary-color: #7c3aed;    /* Couleur secondaire */
    --success-color: #059669;      /* Couleur de succès */
    --warning-color: #d97706;      /* Couleur d'avertissement */
    --error-color: #dc2626;        /* Couleur d'erreur */
    --dark-color: #1f2937;         /* Couleur sombre */
    --light-color: #f8fafc;        /* Couleur claire */
}
```

### Ajout de Nouveaux Tableaux
Pour ajouter un nouveau tableau, modifiez `table_templates.py` :

```python
"nouveau_tableau": {
    "titre_defaut": "Titre du Nouveau Tableau",
    "type_tableau": "liste_enregistrements",
    "colonnes": ["Colonne1", "Colonne2", "Colonne3"],
},
```

Puis ajoutez la section correspondante dans les templates.

## 📊 Format des Données

### Structure Attendue
```python
{
    "meta": {
        "method": "Algorithme Génétique",
        "solver": "EPANET",
        "generations": 15,
        "population": 25,
        "duration_seconds": 45.7,
        "solver_calls": 375
    },
    "proposals": [
        {
            "id": "OPT_001",
            "CAPEX": 12500000,
            "H_tank_m": 28.5,
            "constraints_ok": True,
            "performance_index": 0.892,
            "diameters_mm": {"N1_N2": 200, "N2_N3": 150}
        }
    ],
    "hydraulics": {
        "statistics": {
            "pressures": {"count": 10, "min": 12.5, "max": 45.2},
            "flows": {"count": 9, "positive_flows": 7, "negative_flows": 2},
            "diameters": {"count": 9, "min": 40, "max": 200}
        }
    },
    "constraints": {
        "pressure_min_m": 10,
        "velocity_max_m_s": 3.0
    }
}
```

## 🔧 Dépannage

### Erreurs Courantes

#### Template non trouvé
```
jinja2.exceptions.TemplateNotFound: network_optimize_unified_enhanced.html
```
**Solution** : Vérifiez que le fichier existe dans `src/lcpi/reporting/templates/`

#### Erreur de rendu
```
jinja2.exceptions.UndefinedError: 'meta' is undefined
```
**Solution** : Assurez-vous que toutes les clés requises sont présentes dans vos données

#### Erreur PDF
```
weasyprint.errors.HTMLParsingError: Invalid HTML
```
**Solution** : Vérifiez que le HTML généré est valide (balises fermées, attributs corrects)

### Logs et Debug
Activez le mode verbose pour plus de détails :
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Améliorations Futures

### Fonctionnalités Planifiées
- [ ] **Graphiques interactifs** avec Chart.js ou D3.js
- [ ] **Export Excel** des tableaux de données
- [ ] **Thèmes multiples** (clair/sombre, couleurs personnalisées)
- [ ] **Internationalisation** (français/anglais)
- [ ] **Comparaison de rapports** (différences entre optimisations)

### Optimisations Techniques
- [ ] **Lazy loading** des sections pour les gros rapports
- [ ] **Compression CSS/JS** pour réduire la taille des fichiers
- [ ] **Cache des templates** pour améliorer les performances
- [ ] **Validation des données** avec Pydantic

## 📚 Références

- **Jinja2** : [Documentation officielle](https://jinja.palletsprojects.com/)
- **WeasyPrint** : [Documentation officielle](https://weasyprint.org/)
- **CSS Grid** : [Guide MDN](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_Grid_Layout)
- **FontAwesome** : [Icônes disponibles](https://fontawesome.com/icons)

## 🤝 Contribution

Pour contribuer aux templates améliorés :

1. **Fork** le repository
2. **Créez une branche** pour votre fonctionnalité
3. **Testez** vos modifications avec `test_enhanced_templates.py`
4. **Soumettez** une pull request

### Standards de Code
- **HTML** : HTML5 valide, accessibilité WCAG 2.1
- **CSS** : Variables CSS, responsive design, préfixes navigateurs
- **JavaScript** : ES6+, gestion d'erreurs, documentation JSDoc
- **Python** : PEP 8, type hints, docstrings

---

*Documentation générée automatiquement - LCPI v1.0.0*
