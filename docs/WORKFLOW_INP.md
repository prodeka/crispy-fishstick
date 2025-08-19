# Workflow : Du Fichier EPANET (.inp) au Rapport Complet

Ce document décrit le processus complet pour prendre un fichier de réseau EPANET (`.inp`), effectuer un dimensionnement optimisé et générer un rapport d'analyse complet avec l'outil `lcpi-cli`.

## Prérequis

- `lcpi-cli` est installé et fonctionnel.
- Vous disposez d'un fichier `.inp` décrivant votre réseau hydraulique.

---

## Étape 1 : Initialisation du Projet

Chaque analyse doit se faire dans le contexte d'un projet LCPI. Cette étape crée l'arborescence de dossiers nécessaire pour organiser vos données et les résultats.

1.  **Créez un dossier** pour votre projet et naviguez à l'intérieur :
    ```bash
    mkdir mon_projet_aep
    cd mon_projet_aep
    ```

2.  **Initialisez le projet** avec le template `complet` :
    ```bash
    lcpi init . --template complet
    ```
    *Note : Le `.` indique que le projet est initialisé dans le dossier courant.*

---

## Étape 2 : Conversion du Fichier .inp

Le moteur de calcul de LCPI utilise un format de fichier YAML. Vous devez donc convertir votre fichier `.inp`.

1.  **Copiez votre fichier `.inp`** dans le dossier `data` de votre projet.
    - `mon_projet_aep/data/mon_reseau.inp`

2.  **Exécutez la commande de conversion** :
    ```bash
    lcpi aep convert-inp data/mon_reseau.inp --output data/mon_reseau.yml
    ```
    - Cette commande va lire `mon_reseau.inp`, le convertir en format YAML et sauvegarder le résultat dans `mon_reseau.yml`.

---

## Étape 3 : Dimensionnement et Optimisation

Une fois le fichier de configuration `.yml` créé, vous pouvez lancer le dimensionnement. La commande `network-optimize-unified` utilise un algorithme génétique pour trouver les meilleurs diamètres de conduites en fonction de contraintes (coût, pression, vitesse).

1.  **(Optionnel mais recommandé) Modifiez le fichier de configuration** `data/mon_reseau.yml` pour y ajouter la section `optimisation`. Cette section est cruciale pour piloter le calcul.

    Exemple de section à ajouter dans le fichier `mon_reseau.yml` :
    ```yaml
    optimisation:
      criteres:
        principal: "cout" # "cout", "energie", ou "performance"
      contraintes_budget:
        cout_max_fcfa: 50000000
      contraintes_techniques:
        pression_min_m: 15.0
        vitesse_max_ms: 2.0
      diametres_candidats: [100, 150, 200, 250, 300] # En mm
      algorithme:
        generations: 50
        population_size: 100
    ```

2.  **Lancez l'optimisation du réseau** :
    ```bash
    lcpi aep network-optimize-unified data/mon_reseau.yml --output output/resultats_optimisation.json --verbose
    ```
    - `--output` : Sauvegarde les résultats détaillés de l'optimisation (meilleure solution, statistiques) dans un fichier JSON.
    - `--verbose` : Affiche des informations détaillées pendant le processus.

---

## Étape 4 : Analyse Complète et Rapports Intermédiaires

Pour une analyse plus poussée, la commande `workflow-complete` enchaîne plusieurs étapes : diagnostic, simulation Hardy-Cross, simulation EPANET, et comparaison des résultats.

1.  **Exécutez le workflow complet** sur votre fichier de configuration :
    ```bash
    lcpi aep workflow-complete data/mon_reseau.yml --reports --compare --output output/workflow_results
    ```
    - `--reports` : Génère des rapports détaillés pour chaque étape.
    - `--compare` : Active la comparaison entre les solveurs Hardy-Cross et EPANET.
    - `--output` : Spécifie le dossier où sauvegarder les résultats.

---

## Étape 5 : Génération du Rapport Final

La commande `lcpi report` est la dernière étape. Elle scanne l'ensemble du projet, collecte tous les résultats des calculs (optimisation, simulations, etc.) et les compile dans un rapport PDF ou HTML unique et synthétique.

1.  **Depuis la racine de votre projet** (`mon_projet_aep`), lancez la commande :
    ```bash
    lcpi report . --output rapport_final.html --format html
    ```
    - `.` : Indique à LCPI de scanner le projet courant.
    - `--output` : Nom du fichier de rapport final.
    - `--format`: Spécifie le format de sortie (`html` ou `pdf`).

Vous obtiendrez alors un fichier `rapport_final.html` contenant l'ensemble des analyses effectuées.
