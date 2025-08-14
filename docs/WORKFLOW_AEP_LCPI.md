# Workflow du Module AEP avec LCPI-CLI

Ce document décrit le processus complet pour réaliser une étude d'Alimentation en Eau Potable (AEP) en utilisant le module `aep` de `lcpi-cli`.

## 1. Objectif du Module AEP

Le module AEP de `lcpi` est conçu pour le dimensionnement et la vérification de réseaux de distribution d'eau potable. Il permet de calculer les pressions, débits, et vitesses de l'eau dans chaque tronçon d'un réseau, en se basant sur les caractéristiques des canalisations, les demandes aux nœuds et les apports des réservoirs ou pompes.

## 2. Le Fichier de Données d'Entrée (`.yml`)

Toute étude AEP commence par la création d'un fichier de configuration au format YAML. Ce fichier centralise l'ensemble des informations nécessaires au calcul.

La structure du fichier est la suivante :

```yaml
#-------------------------------------------------
# Fichier d'exemple pour un calcul AEP
#-------------------------------------------------

# Métadonnées du projet (optionnel)
projet:
  nom: "Projet d'AEP de la localité X"
  auteur: "Bureau d'Études Y"
  date: "2025-08-05"

# Définition des composants du réseau
reseau:
  # 1. Noeuds (Junctions)
  noeuds:
    - id: "N1"
      altitude: 100.0  # en mètres
      demande: 5.0     # en L/s (litres par seconde)
    - id: "N2"
      altitude: 95.0
      demande: 3.5
    - id: "N3"
      altitude: 98.0
      demande: 2.0

  # 2. Réservoirs (Tanks/Reservoirs)
  reservoirs:
    - id: "RES1"
      altitude_eau: 150.0 # Niveau de l'eau (charge) en mètres

  # 3. Canalisations (Pipes)
  canalisations:
    - id: "T1"
      noeud_depart: "RES1"
      noeud_arrivee: "N1"
      longueur: 500.0     # en mètres
      diametre: 150       # en millimètres
      rugosite: 0.1       # Coeff. de Hazen-Williams ou Manning (selon config)
    - id: "T2"
      noeud_depart: "N1"
      noeud_arrivee: "N2"
      longueur: 300.0
      diametre: 100
      rugosite: 0.1
    - id: "T3"
      noeud_depart: "N1"
      noeud_arrivee: "N3"
      longueur: 250.0
      diametre: 90
      rugosite: 0.1

# Paramètres de calcul (optionnel)
parametres:
  unites:
    debit: "LPS" # Litres Par Seconde
  formule_pertes_charge: "H-W" # Hazen-Williams (par défaut)
```

### Composants Clés :

*   **`noeuds`**: Points du réseau où l'eau est consommée. Chaque nœud a un identifiant unique (`id`), une altitude et une demande de base.
*   **`reservoirs`**: Sources d'eau du réseau. Ils sont définis par un `id` et le niveau de l'eau (`altitude_eau`) qui impose la charge au point de connexion.
*   **`canalisations`**: Les tuyaux qui relient les nœuds et les réservoirs. Ils sont caractérisés par leurs nœuds de départ et d'arrivée, leur longueur, leur diamètre et leur rugosité.

## 3. Exécution du Calcul via la Ligne de Commande

Une fois le fichier `.yml` préparé, le calcul est lancé via une simple commande `lcpi`.

La commande principale est `calc-reseau`.

```bash
lcpi aep calc-reseau /chemin/vers/votre/fichier_aep.yml
```

### Options Utiles :

*   **Sortie JSON** : Pour une utilisation programmatique (comme avec le futur plugin QGIS), il est crucial de récupérer les résultats dans un format structuré. L'option `--json` est prévue à cet effet.

    ```bash
    lcpi aep calc-reseau fichier_aep.yml --json
    ```

    Cette commande n'affichera rien dans la console mais produira un fichier JSON (ou un flux JSON) contenant tous les résultats.

*   **Génération de Rapport** : Pour obtenir un rapport PDF synthétique.

    ```bash
    lcpi aep calc-reseau fichier_aep.yml --report /chemin/vers/rapport.pdf
    ```

## 4. Analyse des Résultats

L'exécution de la commande produit un ensemble de résultats détaillés pour chaque composant du réseau.

### Exemple de Sortie (format lisible) :

```
========================================
      RÉSULTATS DU CALCUL DU RÉSEAU
========================================

NOEUDS
+------+----------+---------+-----------+
|  ID  | Altitude | Demande | Pression  |
|      |   (m)    |  (L/s)  |  (mCE)    |
+------+----------+---------+-----------+
|  N1  |  100.0   |   5.0   |   48.5    |
|  N2  |   95.0   |   3.5   |   52.1    |
|  N3  |   98.0   |   2.0   |   50.2    |
+------+----------+---------+-----------+

CANALISATIONS
+------+----------+---------+--------+----------+
|  ID  |  Débit   | Vitesse | Pertes |  Pertes  |
|      |  (L/s)   |  (m/s)  | Charge | Linéaires|
|      |          |         | (m)    |  (m/km)  |
+------+----------+---------+--------+----------+
|  T1  |   10.5   |   1.48  |  1.5   |   3.0    |
|  T2  |   6.2    |   1.25  |  1.4   |   4.67   |
|  T3  |   4.3    |   1.05  |  1.3   |   5.2    |
+------+----------+---------+--------+----------+
```

### Interprétation :

*   **Pression aux Nœuds**: La pression est exprimée en Mètres de Colonne d'Eau (mCE). C'est l'indicateur clé pour vérifier si la desserte est correcte (généralement, on vise une pression minimale en tout point).
*   **Débit dans les Canalisations**: Montre comment le débit se répartit dans le réseau pour satisfaire les demandes.
*   **Vitesse**: Permet de vérifier que la vitesse n'est ni trop faible (risque de sédimentation) ni trop élevée (risque d'érosion et de coup de bélier).
*   **Pertes de Charge**: Indique l'énergie "perdue" par frottement. Utile pour optimiser le diamètre des canalisations.

## 5. Intégration dans QGIS (Workflow Cible)

L'objectif final est d'intégrer ce processus dans QGIS pour un workflow visuel et interactif :

1.  **Modélisation dans QGIS** :
    *   Créer une couche de lignes (`canalisations`) et une couche de points (`noeuds`/`reservoirs`).
    *   Remplir leurs tables d'attributs avec les données requises (diamètre, longueur, altitude, demande, etc.).

2.  **Utilisation du Plugin LCPI** :
    *   Lancer le plugin depuis la barre d'outils de QGIS.
    *   Dans la boîte de dialogue du plugin, mapper les couches et les champs correspondants aux paramètres du calcul AEP.
    *   Cliquer sur "Exécuter".

3.  **Actions en Arrière-Plan** :
    *   Le plugin lit les données des couches QGIS.
    *   Il génère automatiquement le fichier `.yml` temporaire.
    *   Il exécute `lcpi aep calc-reseau ... --json`.
    *   Il récupère la sortie JSON.

4.  **Visualisation des Résultats** :
    *   Le plugin met à jour les tables d'attributs des couches existantes avec les résultats (pression, débit, vitesse).
    *   Il applique une symbologie thématique pour une analyse visuelle immédiate (ex: canalisations en rouge si la vitesse est trop élevée, nœuds en bleu si la pression est bonne).
