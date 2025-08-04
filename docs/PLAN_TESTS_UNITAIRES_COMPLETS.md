# 📊 **PLAN D'ACTION - TESTS UNITAIRES COMPLETS**

## 🎯 **Objectif Global**
Créer une suite de tests unitaires complète pour tous les modules de calcul métier, plugins, rapports et fonctionnalités de licence en mode CLI et REPL.

## 📋 **Phase 1 : Correction et Préparation**

### ✅ **1.1 Correction Base CM-Bois**
- **Problème** : `Extra data: line 280 column 1 (char 16658)`
- **Action** : Réparer le fichier JSON corrompu
- **Fichier** : `src/lcpi/db/cm_bois.json`
- **Priorité** : 🔴 URGENT

### ✅ **1.2 Structure des Tests**
- **Dossier** : `tests/unit/`
- **Organisation** : Par module et fonctionnalité
- **Framework** : `pytest`
- **Couvrance** : 100% des fonctions critiques

## 🧪 **Phase 2 : Tests des Modules de Calcul Métier**

### **2.1 Tests AEP (Adduction Eau Potable)**

#### **2.1.1 Calculs de Population**
```python
# tests/unit/aep/test_population.py
- test_projection_malthus()
- test_projection_arithmetique()
- test_projection_geometrique()
- test_projection_logistique()
- test_comparaison_methodes()
```

#### **2.1.2 Calculs de Demande**
```python
# tests/unit/aep/test_demand.py
- test_calcul_demande_globale()
- test_calcul_demande_par_type()
- test_coefficient_pointe()
- test_profil_consommation()
```

#### **2.1.3 Calculs de Réseau**
```python
# tests/unit/aep/test_network.py
- test_dimensionnement_conduite()
- test_perte_charge_hazen_williams()
- test_perte_charge_manning()
- test_perte_charge_darcy_weisbach()
```

#### **2.1.4 Méthode Hardy-Cross**
```python
# tests/unit/aep/test_hardy_cross.py
- test_chargement_csv()
- test_chargement_yaml()
- test_identification_boucles()
- test_iteration_hardy_cross()
- test_convergence()
- test_export_resultats()
```

#### **2.1.5 Calculs de Réservoir**
```python
# tests/unit/aep/test_reservoir.py
- test_volume_cylindrique()
- test_volume_parallelepipedique()
- test_capacite_regulation()
- test_dimensionnement()
```

#### **2.1.6 Calculs de Pompage**
```python
# tests/unit/aep/test_pumping.py
- test_puissance_electrique()
- test_hauteur_manometrique()
- test_rendement_pompe()
- test_selection_pompe()
```

### **2.2 Tests CM (Construction Métallique)**

#### **2.2.1 Calculs de Sections**
```python
# tests/unit/cm/test_sections.py
- test_proprietes_geometriques()
- test_moment_inertie()
- test_module_resistance()
- test_rayon_giration()
```

#### **2.2.2 Calculs de Résistance**
```python
# tests/unit/cm/test_resistance.py
- test_resistance_traction()
- test_resistance_compression()
- test_resistance_flexion()
- test_resistance_cisaillement()
```

#### **2.2.3 Calculs d'Assemblages**
```python
# tests/unit/cm/test_assemblages.py
- test_assemblage_boulonne()
- test_assemblage_soude()
- test_resistance_assemblage()
- test_verification_assemblage()
```

### **2.3 Tests Bois**

#### **2.3.1 Propriétés du Bois**
```python
# tests/unit/bois/test_properties.py
- test_proprietes_espece()
- test_resistance_compression()
- test_resistance_flexion()
- test_resistance_traction()
```

#### **2.3.2 Calculs d'Éléments**
```python
# tests/unit/bois/test_elements.py
- test_dimensionnement_poteau()
- test_dimensionnement_poutre()
- test_verification_stabilite()
- test_calcul_flambement()
```

#### **2.3.3 Calculs d'Assemblages**
```python
# tests/unit/bois/test_assemblages.py
- test_assemblage_embrevement()
- test_assemblage_pointe()
- test_resistance_assemblage()
- test_verification_assemblage()
```

### **2.4 Tests Béton**

#### **2.4.1 Calculs de Béton Armé**
```python
# tests/unit/beton/test_ba.py
- test_dimensionnement_poteau()
- test_dimensionnement_poutre()
- test_calcul_ferraillage()
- test_verification_bael()
```

#### **2.4.2 Calculs de Fondations**
```python
# tests/unit/beton/test_foundations.py
- test_dimensionnement_semelle()
- test_dimensionnement_radier()
- test_capacite_portante()
- test_verification_geotechnique()
```

### **2.5 Tests Hydrodrain**

#### **2.5.1 Calculs Hydrauliques**
```python
# tests/unit/hydrodrain/test_hydraulics.py
- test_dimensionnement_canal()
- test_calcul_debit()
- test_verification_pente()
- test_calcul_rugosite()
```

#### **2.5.2 Calculs de Bassin Versant**
```python
# tests/unit/hydrodrain/test_watershed.py
- test_calcul_surface()
- test_calcul_pente_moyenne()
- test_calcul_temps_concentration()
- test_calcul_debit_pointe()
```

## 🔌 **Phase 3 : Tests des Plugins**

### **3.1 Tests Plugin AEP**
```python
# tests/unit/plugins/test_aep_plugin.py
- test_chargement_plugin()
- test_commandes_cli()
- test_fonctions_calcul()
- test_export_resultats()
```

### **3.2 Tests Plugin CM**
```python
# tests/unit/plugins/test_cm_plugin.py
- test_chargement_plugin()
- test_commandes_cli()
- test_fonctions_calcul()
- test_export_resultats()
```

### **3.3 Tests Plugin Bois**
```python
# tests/unit/plugins/test_bois_plugin.py
- test_chargement_plugin()
- test_commandes_cli()
- test_fonctions_calcul()
- test_export_resultats()
```

### **3.4 Tests Plugin Béton**
```python
# tests/unit/plugins/test_beton_plugin.py
- test_chargement_plugin()
- test_commandes_cli()
- test_fonctions_calcul()
- test_export_resultats()
```

### **3.5 Tests Plugin Hydrodrain**
```python
# tests/unit/plugins/test_hydrodrain_plugin.py
- test_chargement_plugin()
- test_commandes_cli()
- test_fonctions_calcul()
- test_export_resultats()
```

## 📊 **Phase 4 : Tests des Rapports**

### **4.1 Tests Génération Rapports**
```python
# tests/unit/reports/test_report_generation.py
- test_generation_markdown()
- test_generation_html()
- test_generation_pdf()
- test_generation_excel()
```

### **4.2 Tests Templates**
```python
# tests/unit/reports/test_templates.py
- test_template_default()
- test_template_enhanced()
- test_template_custom()
- test_inclusion_formules()
```

### **4.3 Tests Export**
```python
# tests/unit/reports/test_export.py
- test_export_json()
- test_export_csv()
- test_export_markdown()
- test_export_html()
```

## 🔐 **Phase 5 : Tests Licence**

### **5.1 Tests Système Licence**
```python
# tests/unit/license/test_license_system.py
- test_verification_licence()
- test_activation_licence()
- test_expiration_licence()
- test_renouvellement_licence()
```

### **5.2 Tests CLI Licence**
```python
# tests/unit/license/test_license_cli.py
- test_commande_license_check()
- test_commande_license_activate()
- test_commande_license_status()
- test_commande_license_renew()
```

### **5.3 Tests REPL Licence**
```python
# tests/unit/license/test_license_repl.py
- test_repl_license_commands()
- test_repl_license_help()
- test_repl_license_status()
```

## 🖥️ **Phase 6 : Tests CLI et REPL**

### **6.1 Tests CLI Global**
```python
# tests/unit/cli/test_cli_global.py
- test_commande_help()
- test_commande_version()
- test_commande_doctor()
- test_commande_plugins()
```

### **6.2 Tests CLI par Plugin**
```python
# tests/unit/cli/test_cli_plugins.py
- test_cli_aep()
- test_cli_cm()
- test_cli_bois()
- test_cli_beton()
- test_cli_hydrodrain()
```

### **6.3 Tests REPL**
```python
# tests/unit/repl/test_repl.py
- test_repl_initialisation()
- test_repl_commandes()
- test_repl_autocompletion()
- test_repl_historique()
```

## 🗄️ **Phase 7 : Tests Base de Données**

### **7.1 Tests Gestionnaire Global**
```python
# tests/unit/db/test_global_manager.py
- test_chargement_bases()
- test_recherche_globale()
- test_requetes_par_plugin()
- test_autocompletion()
- test_export_resultats()
```

### **7.2 Tests Base AEP**
```python
# tests/unit/db/test_aep_database.py
- test_chargement_aep()
- test_recherche_coefficients()
- test_recherche_materiaux()
- test_recherche_formules()
```

### **7.3 Tests Base CM-Bois**
```python
# tests/unit/db/test_cm_bois_database.py
- test_chargement_cm_bois()
- test_recherche_sections()
- test_recherche_materiaux()
- test_recherche_proprietes()
```

### **7.4 Tests Base Bois**
```python
# tests/unit/db/test_bois_database.py
- test_chargement_bois()
- test_recherche_especes()
- test_recherche_proprietes()
- test_recherche_resistances()
```

## 🧪 **Phase 8 : Tests d'Intégration**

### **8.1 Tests Intégration Complète**
```python
# tests/integration/test_integration_complete.py
- test_workflow_complet_aep()
- test_workflow_complet_cm()
- test_workflow_complet_bois()
- test_workflow_complet_beton()
```

### **8.2 Tests Performance**
```python
# tests/performance/test_performance.py
- test_performance_calculs()
- test_performance_recherche()
- test_performance_export()
- test_performance_cli()
```

## 📁 **Structure des Tests**

```
tests/
├── unit/
│   ├── aep/
│   │   ├── test_population.py
│   │   ├── test_demand.py
│   │   ├── test_network.py
│   │   ├── test_hardy_cross.py
│   │   ├── test_reservoir.py
│   │   └── test_pumping.py
│   ├── cm/
│   │   ├── test_sections.py
│   │   ├── test_resistance.py
│   │   └── test_assemblages.py
│   ├── bois/
│   │   ├── test_properties.py
│   │   ├── test_elements.py
│   │   └── test_assemblages.py
│   ├── beton/
│   │   ├── test_ba.py
│   │   └── test_foundations.py
│   ├── hydrodrain/
│   │   ├── test_hydraulics.py
│   │   └── test_watershed.py
│   ├── plugins/
│   │   ├── test_aep_plugin.py
│   │   ├── test_cm_plugin.py
│   │   ├── test_bois_plugin.py
│   │   ├── test_beton_plugin.py
│   │   └── test_hydrodrain_plugin.py
│   ├── reports/
│   │   ├── test_report_generation.py
│   │   ├── test_templates.py
│   │   └── test_export.py
│   ├── license/
│   │   ├── test_license_system.py
│   │   ├── test_license_cli.py
│   │   └── test_license_repl.py
│   ├── cli/
│   │   ├── test_cli_global.py
│   │   └── test_cli_plugins.py
│   ├── repl/
│   │   └── test_repl.py
│   └── db/
│       ├── test_global_manager.py
│       ├── test_aep_database.py
│       ├── test_cm_bois_database.py
│       └── test_bois_database.py
├── integration/
│   ├── test_integration_complete.py
│   └── test_performance.py
├── conftest.py
└── pytest.ini
```

## 🚀 **Plan d'Exécution**

### **Semaine 1 : Correction et Base**
- [ ] Corriger le fichier CM-Bois JSON
- [ ] Créer la structure des tests
- [ ] Configurer pytest
- [ ] Tests des modules AEP

### **Semaine 2 : Tests Métier**
- [ ] Tests des modules CM
- [ ] Tests des modules Bois
- [ ] Tests des modules Béton
- [ ] Tests des modules Hydrodrain

### **Semaine 3 : Tests Plugins et CLI**
- [ ] Tests des plugins
- [ ] Tests CLI global
- [ ] Tests CLI par plugin
- [ ] Tests REPL

### **Semaine 4 : Tests Avancés**
- [ ] Tests des rapports
- [ ] Tests de licence
- [ ] Tests d'intégration
- [ ] Tests de performance

## 📊 **Métriques de Succès**

### **Couvrance de Code**
- **Objectif** : 95% minimum
- **Modules critiques** : 100%
- **Fonctions publiques** : 100%

### **Tests par Module**
- **AEP** : 50+ tests
- **CM** : 30+ tests
- **Bois** : 25+ tests
- **Béton** : 20+ tests
- **Hydrodrain** : 15+ tests
- **Plugins** : 20+ tests
- **CLI/REPL** : 30+ tests
- **Base de données** : 25+ tests

### **Performance**
- **Temps d'exécution** : < 30 secondes
- **Mémoire** : < 500MB
- **Tests parallèles** : Support complet

## 🎯 **Priorités**

### **🔴 URGENT**
1. Corriger le fichier CM-Bois JSON
2. Tests des modules critiques (AEP, CM)
3. Tests CLI de base

### **🟡 IMPORTANT**
1. Tests des plugins
2. Tests de licence
3. Tests d'intégration

### **🟢 NORMAL**
1. Tests de performance
2. Tests avancés REPL
3. Documentation des tests

---

**📅 Date de début : Immédiat**
**📅 Date de fin estimée : 4 semaines**
**👥 Responsable : Équipe de développement**
**📊 Suivi : Rapport hebdomadaire** 