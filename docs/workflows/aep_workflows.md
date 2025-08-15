# 🚀 Workflow AEP Complet - Alimentation en Eau Potable

## 📋 Vue d'Ensemble

Ce document décrit le workflow complet pour l'analyse et le dimensionnement d'un système d'Alimentation en Eau Potable (AEP) dans LCPI. Le workflow est divisé en trois phases principales : **Pré-Calcul**, **Simulation**, et **Post-Calcul**.

## 🔄 **PHASE 1 : PRÉ-CALCUL**

### **1.1 Calcul de Projection de Population**

#### **Objectif**
Déterminer l'évolution démographique de la zone d'étude pour les années à venir.

#### **Méthodes Disponibles**
- **Malthus** : Croissance exponentielle `P(t) = P₀ × e^(rt)`
- **Arithmétique** : Croissance linéaire `P(t) = P₀ + rt`
- **Géométrique** : Croissance géométrique `P(t) = P₀ × (1+r)^t`
- **Logistique** : Croissance logistique avec saturation

#### **Données d'Entrée**
```yaml
population:
  actuelle: 15000
  historique:
    - annee: 2020
      population: 15000
    - annee: 2021
      population: 15200
    - annee: 2022
      population: 15400
  parametres:
    taux_croissance: 0.025  # 2.5% par an
    methode: "malthus"
    horizon: 2050
```

#### **Résultats**
- Population projetée par année
- Taux de croissance effectif
- Analyse de sensibilité

### **1.2 Calcul des Besoins en Eau**

#### **Objectif**
Déterminer la consommation d'eau par type d'usage et par habitant.

#### **Types de Consommation**
- **Domestique** : 150 L/hab/jour (standard français)
- **Industriel** : 50 L/hab/jour
- **Commercial** : 30 L/hab/jour
- **Public** : 20 L/hab/jour

#### **Données d'Entrée**
```yaml
consommation:
  domestique: 150  # litres/habitant/jour
  industriel: 50   # litres/habitant/jour
  commercial: 30   # litres/habitant/jour
  public: 20       # litres/habitant/jour
  
  coefficients:
    pointe_journaliere: 1.3
    pointe_horaire: 1.8
    fuites: 0.15
    pertes_reseau: 0.20
```

#### **Calculs Effectués**
```python
# Demande moyenne journalière
Q_moyen = population × (consommation_totale / 1000)  # m³/jour

# Demande de pointe journalière
Q_pointe_j = Q_moyen × coefficient_pointe_journaliere

# Demande de pointe horaire
Q_pointe_h = Q_pointe_j × coefficient_pointe_horaire

# Demande totale avec fuites
Q_total = Q_pointe_h × (1 + fuites + pertes_reseau)
```

### **1.3 Calcul de la Demande de Pointe**

#### **Objectif**
Déterminer les débits de pointe pour le dimensionnement des infrastructures.

#### **Coefficients de Pointe**
- **Pointe journalière** : 1.3 (variation saisonnière)
- **Pointe horaire** : 1.8 (variation quotidienne)
- **Pointe simultanéité** : 0.7 (usage simultané)

#### **Formules de Calcul**
```python
# Débit de pointe journalier
Q_pj = Q_moyen × K_pj

# Débit de pointe horaire
Q_ph = Q_pj × K_ph

# Débit de pointe simultané
Q_ps = Q_ph × K_simultaneite

# Débit de dimensionnement
Q_dim = Q_ps × (1 + fuites + pertes)
```

### **1.4 Pré-dimensionnement des Conduites**

#### **Objectif**
Estimer les diamètres des conduites principales basés sur les débits calculés.

#### **Méthodes de Calcul**
- **Formule de Hazen-Williams** : `J = 10.67 × (Q/C)^1.85 × L/D^4.87`
- **Formule de Manning** : `J = (n² × Q² × L) / (D^(16/3) × A^(10/3))`
- **Formule de Darcy-Weisbach** : `J = (λ × L × Q²) / (2 × g × D^5 × A²)`

#### **Critères de Dimensionnement**
- **Vitesse maximale** : 2.5 m/s
- **Vitesse minimale** : 0.6 m/s
- **Pression minimale** : 20 m de colonne d'eau
- **Pression maximale** : 80 m de colonne d'eau

#### **Données d'Entrée**
```yaml
reseau:
  conduites:
    C1:
      longueur: 500      # mètres
      debit: 0.05       # m³/s
      rugosite: 100     # coefficient Hazen-Williams
      type: "acier"
    
    C2:
      longueur: 300
      debit: 0.03
      rugosite: 120
      type: "pvc"
  
  parametres:
    vitesse_max: 2.5      # m/s
    pression_min: 20      # m de colonne d'eau
    tolerance: 0.001      # tolérance de convergence
```

## ⚡ **PHASE 2 : SIMULATION (Workflow Défini)**

### **2.1 Diagnostic du Réseau**

#### **Objectif**
Vérifier la connectivité et la cohérence du réseau hydraulique.

#### **Vérifications Effectuées**
- **Connectivité** : Tous les nœuds sont-ils connectés ?
- **Sources d'eau** : Présence de réservoirs ou sources
- **Compatibilité EPANET** : Format compatible avec EPANET
- **Analyse topologique** : Structure du réseau

#### **Résultats du Diagnostic**
```json
{
  "connectivity": true,
  "epanet_compatibility": {
    "compatible": true,
    "erreurs": []
  },
  "topology": {
    "nombre_noeuds": 15,
    "nombre_conduites": 18,
    "nombre_boucles": 4,
    "diametre_moyen": 0.25
  }
}
```

### **2.2 Simulation Hardy-Cross**

#### **Objectif**
Résoudre le système d'équations hydrauliques par méthode itérative.

#### **Principe de la Méthode**
La méthode Hardy-Cross résout le système d'équations :
1. **Équation de continuité** : ΣQ = 0 à chaque nœud
2. **Équation d'énergie** : Σh = 0 sur chaque boucle

#### **Algorithme Itératif**
```python
def hardy_cross_iteration(network_data, tolerance=1e-6, max_iterations=100):
    """
    Méthode Hardy-Cross pour résolution réseau maillé
    """
    iteration = 0
    convergence = False
    
    while iteration < max_iterations and not convergence:
        # 1. Calculer les pertes de charge pour chaque conduite
        for pipe in network_data['pipes']:
            pipe['headloss'] = calculate_headloss(pipe)
        
        # 2. Calculer les corrections de débit pour chaque boucle
        for loop in network_data['loops']:
            correction = calculate_flow_correction(loop)
            
            # 3. Appliquer les corrections
            for pipe in loop['pipes']:
                pipe['flow'] += correction
        
        # 4. Vérifier la convergence
        max_correction = max([abs(correction) for correction in corrections])
        convergence = max_correction < tolerance
        
        iteration += 1
    
    return {
        'iterations': iteration,
        'tolerance_finale': max_correction,
        'flows': extract_flows(network_data),
        'pressures': calculate_pressures(network_data)
    }
```

#### **Formules de Perte de Charge**
```python
# Formule de Hazen-Williams
def hazen_williams_headloss(Q, L, D, C):
    """
    J = 10.67 × (Q/C)^1.85 × L/D^4.87
    """
    return 10.67 * (Q / C)**1.85 * L / (D**4.87)

# Formule de Manning
def manning_headloss(Q, L, D, n):
    """
    J = (n² × Q² × L) / (D^(16/3) × A^(10/3))
    """
    A = math.pi * D**2 / 4
    return (n**2 * Q**2 * L) / (D**(16/3) * A**(10/3))

# Formule de Darcy-Weisbach
def darcy_weisbach_headloss(Q, L, D, lambda_coeff):
    """
    J = (λ × L × Q²) / (2 × g × D^5 × A²)
    """
    A = math.pi * D**2 / 4
    g = 9.81
    return (lambda_coeff * L * Q**2) / (2 * g * D**5 * A**2)
```

#### **Rapport Détaillé Hardy-Cross**
```markdown
# Rapport Hardy-Cross - Itération 1

## Calculs de Perte de Charge

### Conduite C1 (N1 → N2)
- **Débit initial** : 0.05 m³/s
- **Longueur** : 500 m
- **Diamètre** : 0.2 m
- **Rugosité** : 100 (Hazen-Williams)
- **Vitesse** : 1.59 m/s
- **Perte de charge** : 12.45 m

### Conduite C2 (N2 → N3)
- **Débit initial** : 0.03 m³/s
- **Longueur** : 300 m
- **Diamètre** : 0.15 m
- **Rugosité** : 120 (Hazen-Williams)
- **Vitesse** : 1.70 m/s
- **Perte de charge** : 8.92 m

## Corrections de Débit

### Boucle 1 (C1, C2, C3)
- **Σh** : 12.45 + 8.92 - 15.23 = 6.14 m
- **Σ(∂h/∂Q)** : 498.0 + 594.7 + 609.2 = 1701.9
- **Correction** : -6.14 / 1701.9 = -0.0036 m³/s

## Nouveaux Débits
- **C1** : 0.05 - 0.0036 = 0.0464 m³/s
- **C2** : 0.03 - 0.0036 = 0.0264 m³/s
- **C3** : 0.02 + 0.0036 = 0.0236 m³/s
```

### **2.3 Simulation EPANET**

#### **Objectif**
Valider les résultats Hardy-Cross avec le standard industriel EPANET.

#### **Intégration EPANET**
```python
def run_epanet_simulation(network_data):
    """
    Simulation hydraulique avec EPANET
    """
    # 1. Convertir les données LCPI vers format EPANET
    epanet_data = convert_to_epanet_format(network_data)
    
    # 2. Créer le fichier .inp EPANET
    inp_file = create_epanet_inp_file(epanet_data)
    
    # 3. Lancer la simulation EPANET
    epanet = EpanetSimulator()
    epanet.open_project(inp_file)
    epanet.solve_hydraulics()
    
    # 4. Extraire les résultats
    results = extract_epanet_results(epanet)
    epanet.close_project()
    
    return results
```

#### **Format EPANET .inp**
```inp
[TITLE]
Simulation LCPI AEP

[JUNCTIONS]
ID              Elev        Demand       Pattern       Comment
N1              150.0       0.0                         Réservoir
N2              145.0       0.02                        Consommation
N3              140.0       0.015                       Consommation

[RESERVOIRS]
ID              Head        Pattern       Comment
R1              160.0                                    Source d'eau

[PIPES]
ID              Node1       Node2        Length        Diameter      Roughness      Status
C1              R1          N1           500           0.2           100            Open
C2              N1          N2           300           0.15          120            Open
C3              N2          N3           250           0.12          120            Open

[PATTERNS]
ID              Multipliers
Pattern1        1.0         1.2         1.5         1.8         2.0         1.8
```

#### **Résultats EPANET**
```json
{
  "nodes": {
    "N1": {
      "pressure": 45.2,
      "head": 195.2,
      "demand": 0.0
    },
    "N2": {
      "pressure": 38.7,
      "head": 183.7,
      "demand": 0.02
    },
    "N3": {
      "pressure": 32.1,
      "head": 172.1,
      "demand": 0.015
    }
  },
  "pipes": {
    "C1": {
      "flow": 0.0464,
      "velocity": 1.48,
      "headloss": 12.45,
      "status": "Open"
    },
    "C2": {
      "flow": 0.0264,
      "velocity": 1.49,
      "headloss": 8.92,
      "status": "Open"
    },
    "C3": {
      "flow": 0.0236,
      "velocity": 2.09,
      "headloss": 11.6,
      "status": "Open"
    }
  },
  "statistics": {
    "iterations": 8,
    "relative_error": 0.0001,
    "max_head_error": 0.05,
    "max_flow_change": 0.001
  }
}
```

### **2.4 Validation Croisée**

#### **Objectif**
Comparer les résultats Hardy-Cross et EPANET pour valider les calculs.

#### **Métriques de Comparaison**
```python
def compare_results(hardy_results, epanet_results):
    """
    Comparaison Hardy-Cross vs EPANET
    """
    comparison = {
        "flows": {},
        "pressures": {},
        "statistics": {}
    }
    
    # Comparaison des débits
    for pipe_id in hardy_results['flows']:
        hardy_flow = hardy_results['flows'][pipe_id]
        epanet_flow = epanet_results['pipes'][pipe_id]['flow']
        
        difference = abs(hardy_flow - epanet_flow)
        relative_error = difference / epanet_flow * 100
        
        comparison['flows'][pipe_id] = {
            'hardy_cross': hardy_flow,
            'epanet': epanet_flow,
            'difference': difference,
            'relative_error': relative_error
        }
    
    # Comparaison des pressions
    for node_id in hardy_results['pressures']:
        hardy_pressure = hardy_results['pressures'][node_id]
        epanet_pressure = epanet_results['nodes'][node_id]['pressure']
        
        difference = abs(hardy_pressure - epanet_pressure)
        relative_error = difference / epanet_pressure * 100
        
        comparison['pressures'][node_id] = {
            'hardy_cross': hardy_pressure,
            'epanet': epanet_pressure,
            'difference': difference,
            'relative_error': relative_error
        }
    
    return comparison
```

#### **Rapport de Comparaison**
```markdown
# Rapport de Comparaison Hardy-Cross vs EPANET

## Comparaison des Débits

| Conduite | Hardy-Cross (m³/s) | EPANET (m³/s) | Différence (m³/s) | Erreur Relative (%) |
|----------|-------------------|---------------|------------------|-------------------|
| C1       | 0.0464            | 0.0464        | 0.0000           | 0.00%             |
| C2       | 0.0264            | 0.0264        | 0.0000           | 0.00%             |
| C3       | 0.0236            | 0.0236        | 0.0000           | 0.00%             |

## Comparaison des Pressions

| Nœud | Hardy-Cross (m) | EPANET (m) | Différence (m) | Erreur Relative (%) |
|------|-----------------|------------|----------------|-------------------|
| N1   | 45.2            | 45.2       | 0.0            | 0.00%             |
| N2   | 38.7            | 38.7       | 0.0            | 0.00%             |
| N3   | 32.1            | 32.1       | 0.0            | 0.00%             |

## Statistiques de Convergence

### Hardy-Cross
- **Itérations** : 6
- **Tolérance finale** : 1.2e-6
- **Temps de calcul** : 0.045 s

### EPANET
- **Itérations** : 8
- **Erreur relative** : 0.0001
- **Temps de calcul** : 0.012 s

## Conclusion
Les résultats Hardy-Cross et EPANET sont en parfait accord avec des écarts relatifs inférieurs à 0.01%, validant la précision des calculs LCPI.
```

## 📊 **PHASE 3 : POST-CALCUL**

### **3.1 Analyse des Résultats**

#### **Objectif**
Analyser les pressions et vitesses dans le réseau pour vérifier la conformité.

#### **Critères de Vérification**
```python
def analyze_network_results(results):
    """
    Analyse des résultats du réseau
    """
    analysis = {
        "pressures": {
            "min": float('inf'),
            "max": 0,
            "average": 0,
            "nodes_low_pressure": [],
            "nodes_high_pressure": []
        },
        "velocities": {
            "min": float('inf'),
            "max": 0,
            "average": 0,
            "pipes_low_velocity": [],
            "pipes_high_velocity": []
        },
        "compliance": {
            "pressure_ok": True,
            "velocity_ok": True,
            "issues": []
        }
    }
    
    # Analyse des pressions
    pressures = []
    for node_id, node_data in results['nodes'].items():
        pressure = node_data['pressure']
        pressures.append(pressure)
        
        if pressure < 20:  # Pression minimale
            analysis['pressures']['nodes_low_pressure'].append(node_id)
            analysis['compliance']['pressure_ok'] = False
            analysis['compliance']['issues'].append(f"Pression insuffisante au nœud {node_id}: {pressure} m")
        
        if pressure > 80:  # Pression maximale
            analysis['pressures']['nodes_high_pressure'].append(node_id)
            analysis['compliance']['pressure_ok'] = False
            analysis['compliance']['issues'].append(f"Pression excessive au nœud {node_id}: {pressure} m")
    
    analysis['pressures']['min'] = min(pressures)
    analysis['pressures']['max'] = max(pressures)
    analysis['pressures']['average'] = sum(pressures) / len(pressures)
    
    # Analyse des vitesses
    velocities = []
    for pipe_id, pipe_data in results['pipes'].items():
        velocity = pipe_data['velocity']
        velocities.append(velocity)
        
        if velocity < 0.6:  # Vitesse minimale
            analysis['velocities']['pipes_low_velocity'].append(pipe_id)
            analysis['compliance']['velocity_ok'] = False
            analysis['compliance']['issues'].append(f"Vitesse insuffisante dans la conduite {pipe_id}: {velocity} m/s")
        
        if velocity > 2.5:  # Vitesse maximale
            analysis['velocities']['pipes_high_velocity'].append(pipe_id)
            analysis['compliance']['velocity_ok'] = False
            analysis['compliance']['issues'].append(f"Vitesse excessive dans la conduite {p