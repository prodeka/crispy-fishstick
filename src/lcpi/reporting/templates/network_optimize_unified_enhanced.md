# 🏗️ LCPI Engineering
## Analyse et Dimensionnement Hydraulique

**Date de génération :** {{ generation_date }}  
**Version :** {{ version }}  
**Fichier source :** {{ input_file }}

---

# 📊 Rapport d'Optimisation Réseau - {{ meta.method|default('Méthode') }}

---

## 🎯 Informations Générales

| Paramètre | Valeur |
|-----------|---------|
| **Méthode d'optimisation** | {{ meta.method|default('N/A') }} |
| **Solveur** | {{ meta.solver|default('N/A') }} |
| **Générations** | {{ meta.generations|default('N/A') }} |
| **Population** | {{ meta.population|default('N/A') }} |
| **Durée d'exécution** | {{ meta.duration_seconds|default(0)|round(1) }} secondes |
| **Appels simulateur** | {{ meta.solver_calls|default(0) }} |

---

## 🏆 Résultats de l'Optimisation

{% if proposals %}
{% for proposal in proposals %}
### Proposition {{ loop.index }}

| Paramètre | Valeur |
|-----------|---------|
| **ID** | {{ proposal.id|default('N/A') }} |
| **CAPEX** | **{{ proposal.CAPEX|default(0)|round(0)|int }} FCFA** |
| **Hauteur réservoir** | {% if proposal.H_tank_m %}{{ proposal.H_tank_m|round(2) }}{% else %}N/A{% endif %} m |
| **Contraintes respectées** | {% if proposal.constraints_ok %}✅ Oui{% else %}❌ Non{% endif %} |
| **Indice de performance** | {% if proposal.performance_index %}{{ proposal.performance_index|round(3) }}{% else %}N/A{% endif %} |

{% if proposal.diameters_mm %}
#### 📏 Diamètres des Conduites

| Conduite | Diamètre (mm) |
|----------|----------------|
{% for pipe, diameter in proposal.diameters_mm.items() %}
| {{ pipe }} | {{ diameter }} |
{% endfor %}
{% endif %}

{% if proposal.constraints_violations %}
#### ⚠️ Violations de Contraintes

{% for violation in proposal.constraints_violations %}
- {{ violation }}
{% endfor %}
{% endif %}

---
{% endfor %}
{% else %}
*Aucune proposition d'optimisation disponible.*
{% endif %}

---

## 📊 Statistiques Hydrauliques

{% if hydraulics and hydraulics.statistics %}
{% set stats = hydraulics.statistics %}

### 📊 Pressions

| Paramètre | Valeur |
|-----------|---------|
| **Nombre de nœuds** | {{ stats.pressures.count|default(0) }} |
| **Pression minimale** | {{ stats.pressures.min|default(0)|round(3) }} m |
| **Pression maximale** | {{ stats.pressures.max|default(0)|round(3) }} m |
| **Pression moyenne** | {{ stats.pressures.mean|default(0)|round(3) }} m |
| **Pression médiane** | {{ stats.pressures.median|default(0)|round(3) }} m |
| **Écart-type** | {{ stats.pressures.std|default(0)|round(3) }} m |
| **Q25** | {{ stats.pressures.q25|default(0)|round(3) }} m |
| **Q75** | {{ stats.pressures.q75|default(0)|round(3) }} m |
| **% < 10m** | {{ stats.pressures.pct_lt_10m|default(0)|round(1) }}% |
| **% < 15m** | {{ stats.pressures.pct_lt_15m|default(0)|round(1) }}% |
| **% < 20m** | {{ stats.pressures.pct_lt_20m|default(0)|round(1) }}% |

### 🌊 Vitesses

| Paramètre | Valeur |
|-----------|---------|
| **Nombre de conduites** | {{ stats.velocities.count|default(0) }} |
| **Vitesse minimale** | {{ stats.velocities.min|default(0)|round(3) }} m/s |
| **Vitesse maximale** | {{ stats.velocities.max|default(0)|round(3) }} m/s |
| **Vitesse moyenne** | {{ stats.velocities.mean|default(0)|round(3) }} m/s |
| **Vitesse médiane** | {{ stats.velocities.median|default(0)|round(3) }} m/s |
| **Écart-type** | {{ stats.velocities.std|default(0)|round(3) }} m/s |

### 💧 Débits

| Paramètre | Valeur |
|-----------|---------|
| **Nombre de conduites** | {{ stats.flows.count|default(0) }} |
| **Débit minimal** | {{ stats.flows.min|default(0)|round(3) }} m³/s |
| **Débit maximal** | {{ stats.flows.max|default(0)|round(3) }} m³/s |
| **Débit moyen** | {{ stats.flows.mean|default(0)|round(3) }} m³/s |
| **Débit médian** | {{ stats.flows.median|default(0)|round(3) }} m³/s |
| **Débit minimal (absolu)** | {{ stats.flows.min_abs|default(0)|round(3) }} m³/s |
| **Débit maximal (absolu)** | {{ stats.flows.max_abs|default(0)|round(3) }} m³/s |
| **Débit moyen (absolu)** | {{ stats.flows.mean_abs|default(0)|round(3) }} m³/s |
| **Débit médian (absolu)** | {{ stats.flows.median_abs|default(0)|round(3) }} m³/s |
| **Conduites en sens normal** | {{ stats.flows.positive_flows|default(0) }} |
| **Conduites en sens inverse** | {{ stats.flows.negative_flows|default(0) }} |
| **Conduites sans débit** | {{ stats.flows.zero_flows|default(0) }} |

> **ℹ️ Note sur les débits :** Un débit négatif indique que le sens réel de l'écoulement est opposé à la direction définie dans le fichier d'entrée. Par exemple, si la conduite N21_N22 a un débit de -0.23 m³/s, cela signifie que l'eau circule réellement de N22 vers N21.

### 📏 Diamètres

| Paramètre | Valeur |
|-----------|---------|
| **Nombre de conduites** | {{ stats.diameters.count|default(0) }} |
| **Diamètre minimal** | {{ stats.diameters.min|default(0) }} mm |
| **Diamètre maximal** | {{ stats.diameters.max|default(0) }} mm |
| **Diamètre moyen** | {{ stats.diameters.mean|default(0)|round(1) }} mm |
| **Diamètre médian** | {{ stats.diameters.median|default(0)|round(1) }} mm |
| **Écart-type** | {{ stats.diameters.std|default(0)|round(1) }} mm |

### 📉 Pertes de Charge

| Paramètre | Valeur |
|-----------|---------|
| **Nombre de conduites** | {{ stats.headlosses.count|default(0) }} |
| **Perte minimale** | {{ stats.headlosses.min|default(0)|round(3) }} m |
| **Perte maximale** | {{ stats.headlosses.max|default(0)|round(3) }} m |
| **Perte moyenne** | {{ stats.headlosses.mean|default(0)|round(3) }} m |
| **Perte médiane** | {{ stats.headlosses.median|default(0)|round(3) }} m |
| **Écart-type** | {{ stats.headlosses.std|default(0)|round(3) }} m |

### 📈 Indice de Performance

| Paramètre | Valeur |
|-----------|---------|
| **Indice global** | **{{ stats.performance_index|default('N/A')|round(3) }}** |

{% else %}
*Aucune statistique hydraulique disponible.*
{% endif %}

---

## 🏗️ Structure du Réseau

### 📋 Énumération des Tronçons

| DC_ID | Longueur (m) | NODE1 | NODE2 |
|-------|---------------|-------|-------|
{% if proposals and proposals[0].diameters_mm %}
{% for pipe, diameter in proposals[0].diameters_mm.items() %}
| {{ pipe }} | -- | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- | -- |
{% endif %}

### 📐 Dimensionnement des Tronçons

| DC_ID | Longueur (m) | Qd (m³/s) | DN (mm) | V (m/s) | ΔH (m) |
|-------|---------------|------------|---------|---------|---------|
{% if proposals and proposals[0].diameters_mm %}
{% for pipe, diameter in proposals[0].diameters_mm.items() %}
| {{ pipe }} | -- | -- | {{ diameter }} | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- | -- | -- | -- |
{% endif %}

### 🎯 Dimensionnement des Nœuds

| JUNCTIONS | X | Y | Z (m) | P_réel (m) |
|------------|---|----|--------|-------------|
{% if hydraulics and hydraulics.statistics and hydraulics.statistics.pressures %}
{% for i in range(hydraulics.statistics.pressures.count|default(0)) %}
| N{{ i + 1 }} | -- | -- | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- | -- | -- |
{% endif %}

### 🗼 Récapitulatif du Réservoir

| Paramètre | Valeur | Description |
|-----------|---------|-------------|
| **Type** | Réservoir surélevé | Type de réservoir |
| **Hauteur (m)** | {% if proposals and proposals[0].H_tank_m %}{{ proposals[0].H_tank_m|round(2) }}{% else %}--{% endif %} | Hauteur du réservoir |
| **Volume utile (m³)** | -- | Volume utile calculé |
| **Volume max (m³)** | -- | Volume maximum |
| **Volume min (m³)** | -- | Volume minimum |
| **Hauteur min (m)** | -- | Hauteur minimale |
| **Hauteur max (m)** | -- | Hauteur maximale |
| **Pression min (m)** | -- | Pression minimale |
| **Pression max (m)** | -- | Pression maximale |
| **Capacité (m³)** | -- | Capacité totale |
| **Réserve (m³)** | -- | Volume de réserve |
| **Autonomie (h)** | -- | Autonomie en heures |
| **Débit d'entrée (m³/s)** | -- | Débit d'alimentation |
| **Débit de sortie (m³/s)** | -- | Débit de distribution |

---

## 🔄 Comparaisons et Validation

### 📊 Comparatif Diamètres et Débits

| TRONCONS | D_CALCULE (mm) | D_EPANET (mm) | DN_CALCULE (mm) | DN_EPANET (mm) | Q_CALCULER (m³/s) | Q_EPANET (m³/s) |
|----------|-----------------|---------------|-----------------|-----------------|-------------------|------------------|
{% if proposals and proposals[0].diameters_mm %}
{% for pipe, diameter in proposals[0].diameters_mm.items() %}
| {{ pipe }} | {{ diameter }} | {{ diameter }} | {{ diameter }} | {{ diameter }} | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- | -- | -- | -- | -- |
{% endif %}

### 🚀 Comparatif Vitesses et Pertes de Charges

| TRONCONS | V_CALCULE (m/s) | V_EPANET (m/s) | ΔH_i_CALCULER (m) | ΔH_i_EPANET (m) |
|----------|------------------|-----------------|-------------------|------------------|
{% if proposals and proposals[0].diameters_mm %}
{% for pipe, diameter in proposals[0].diameters_mm.items() %}
| {{ pipe }} | -- | -- | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- | -- | -- |
{% endif %}

### 📏 Comparatif des Pressions

| JUNCTIONS | P_CALCULE (m) | P_EPANET (m) |
|------------|----------------|---------------|
{% if hydraulics and hydraulics.statistics and hydraulics.statistics.pressures %}
{% for i in range(hydraulics.statistics.pressures.count|default(0)) %}
| N{{ i + 1 }} | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- |
{% endif %}

### 📈 Récapitulatif des Diamètres des Conduites

| Diamètre nominal (mm) | Longueur Distribution | Longueur refoulement | Longueurs totales |
|------------------------|------------------------|----------------------|-------------------|
{% if proposals and proposals[0].diameters_mm %}
{% set diameters = proposals[0].diameters_mm.values()|list %}
{% for diameter in diameters|unique %}
| {{ diameter }} | -- | -- | -- |
{% endfor %}
{% else %}
| *Aucune donnée disponible* | -- | -- | -- |
{% endif %}

---

## 💰 Analyse Financière

### 📋 Devis Estimatif et Quantitatif

| N° | Désignations | Unité | Quantité | Prix Unitaire | MONTANT |
|----|--------------|-------|----------|----------------|----------|
| 1 | Conduites principales | ml | -- | -- | -- |
| 2 | Réservoir surélevé | u | 1 | -- | -- |
| 3 | Vannes et robinets | u | -- | -- | -- |
| 4 | Installation électrique | lot | 1 | -- | -- |
| **TOTAL** | | | | | **{% if proposals %}{{ proposals[0].CAPEX|default(0)|round(0)|int }} FCFA{% else %}--{% endif %}** |

---

## 📋 Contraintes d'Optimisation

{% if constraints %}
| Contrainte | Valeur |
|------------|---------|
{% if constraints.pressure_min_m %}
| **Pression minimale** | {{ constraints.pressure_min_m }} m |
{% endif %}
{% if constraints.velocity_min_m_s %}
| **Vitesse minimale** | {{ constraints.velocity_min_m_s }} m/s |
{% endif %}
{% if constraints.velocity_max_m_s %}
| **Vitesse maximale** | {{ constraints.velocity_max_m_s }} m/s |
{% endif %}
{% if constraints.hmax %}
| **Hauteur maximale** | {{ constraints.hmax }} m |
{% endif %}
{% else %}
*Aucune contrainte spécifiée.*
{% endif %}

---

## 📊 Métriques de Performance

| Métrique | Valeur |
|----------|---------|
| **Durée totale** | {{ meta.duration_seconds|default(0)|round(1) }} secondes |
| **Appels simulateur** | {{ meta.solver_calls|default(0) }} |
| **Efficacité** | {% if meta.duration_seconds and meta.solver_calls %}
{% set efficiency = (meta.solver_calls / meta.duration_seconds)|round(2) %}
{{ efficiency }} simulations/seconde
{% else %}
N/A
{% endif %} |
| **Taux de succès** | {% if proposals and proposals|length > 0 %}
{% set success_count = proposals|selectattr('constraints_ok')|list|length %}
{% set success_rate = (success_count / proposals|length * 100) %}
{{ success_rate|round(1) }}%
{% else %}
N/A
{% endif %} |

---

## 🔍 Détails Techniques

### 📊 Distribution des Diamètres

{% if proposals and proposals[0].diameters_mm %}
{% set diameters = proposals[0].diameters_mm.values()|list %}
{% set unique_diameters = diameters|unique|sort %}

**Répartition des diamètres :**

{% for diameter in unique_diameters %}
- **{{ diameter }} mm** : {{ diameters|select('equalto', diameter)|list|length }} conduite(s)
{% endfor %}

**Total des conduites :** {{ diameters|length }}
{% else %}
*Aucune donnée de diamètre disponible pour l'analyse.*
{% endif %}

### 📈 Analyse des Contraintes

{% if proposals %}
{% set total_proposals = proposals|length %}
{% set valid_proposals = proposals|selectattr('constraints_ok')|list|length %}
{% set invalid_proposals = total_proposals - valid_proposals %}

- **Propositions totales :** {{ total_proposals }}
- **Contraintes respectées :** {{ valid_proposals }} ({{ (valid_proposals / total_proposals * 100)|round(1) if total_proposals > 0 else 0 }}%)
- **Contraintes violées :** {{ invalid_proposals }} ({{ (invalid_proposals / total_proposals * 100)|round(1) if total_proposals > 0 else 0 }}%)

{% if invalid_proposals > 0 %}
**Violations identifiées :**
{% for proposal in proposals %}
{% if not proposal.constraints_ok %}
- **Proposition {{ loop.index }}** : 
  {% if proposal.constraints_violations %}
    {% for violation in proposal.constraints_violations %}
      - {{ violation }}
    {% endfor %}
  {% else %}
    - Contraintes non respectées (détails non disponibles)
  {% endif %}
{% endif %}
{% endfor %}
{% endif %}
{% else %}
*Aucune proposition disponible pour l'analyse des contraintes.*
{% endif %}

---

## 📋 Résumé Exécutif

### 🎯 Objectifs Atteints

{% if proposals and proposals[0].constraints_ok %}
✅ **Optimisation réussie** : La solution optimale respecte toutes les contraintes définies
✅ **Coût minimisé** : CAPEX optimal de {{ proposals[0].CAPEX|default(0)|round(0)|int }} FCFA
{% if proposals[0].H_tank_m %}
✅ **Hauteur de réservoir optimisée** : {{ proposals[0].H_tank_m|round(2) }} m
{% endif %}
{% else %}
⚠️ **Optimisation partielle** : Certaines contraintes ne sont pas respectées
{% if proposals %}
💰 **Coût de la meilleure solution** : {{ proposals[0].CAPEX|default(0)|round(0)|int }} FCFA
{% endif %}
{% endif %}

### 📊 Indicateurs de Performance

- **Efficacité de l'algorithme** : {{ meta.solver_calls|default(0) }} simulations en {{ meta.duration_seconds|default(0)|round(1) }} secondes
- **Qualité des solutions** : {% if proposals %}{{ proposals|length }} proposition(s) générée(s){% else %}Aucune proposition{% endif %}
- **Convergence** : {% if meta.generations and meta.population %}Génération {{ meta.generations }} avec population {{ meta.population }}{% else %}Paramètres non spécifiés{% endif %}

---

## 🔧 Recommandations

### 📈 Améliorations Suggérées

1. **Analyse des contraintes violées** : Examiner les violations pour ajuster les paramètres d'optimisation
2. **Validation hydraulique** : Vérifier la cohérence des résultats avec EPANET
3. **Optimisation des paramètres** : Ajuster le nombre de générations et la taille de population si nécessaire
4. **Analyse de sensibilité** : Étudier l'impact des variations des contraintes sur la solution optimale

### 📊 Validation des Résultats

- **Comparaison EPANET** : Valider les résultats avec le simulateur de référence
- **Analyse des écarts** : Identifier les différences entre calculs et simulations
- **Tests de robustesse** : Vérifier la stabilité des solutions optimales

---

## 📚 Annexes

### 📋 Glossaire

- **CAPEX** : Capital Expenditure (Dépenses d'investissement)
- **DN** : Diamètre Nominal
- **ΔH** : Perte de charge
- **Qd** : Débit de dimensionnement
- **V** : Vitesse d'écoulement

### 🔗 Références

- **EPANET** : Logiciel de simulation hydraulique de l'EPA
- **Algorithme génétique** : Méthode d'optimisation basée sur l'évolution
- **Contraintes hydrauliques** : Limites physiques du réseau

---

## 📄 Informations de Génération

- **Généré par** : LCPI (Logiciel de Calcul et Planification d'Infrastructure)
- **Version** : {{ version }}
- **Date** : {{ generation_date }}
- **Fichier source** : {{ input_file }}
- **Méthode** : {{ meta.method|default('N/A') }}
- **Solveur** : {{ meta.solver|default('N/A') }}

---

*Rapport généré automatiquement par LCPI - Tous droits réservés*