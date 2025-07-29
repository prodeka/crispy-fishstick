# Projet de Dimensionnement Multi-Matériaux (Hydro, Béton Armé, Bois)

## Description
Ce projet est une application CLI (Command Line Interface) robuste et interactive conçue pour assister les ingénieurs et les techniciens dans le dimensionnement et la vérification d'éléments structurels et hydrauliques. Il intègre des modules spécialisés pour le calcul des réseaux d'assainissement pluvial, le dimensionnement des éléments en béton armé (poteaux, radiers) et la vérification des sections en bois, en se basant sur les normes et méthodes de calcul pertinentes (Eurocode, BAEL, méthodes hydrologiques).

L'objectif principal est de fournir un outil fiable et pédagogique pour :
-   Calculer les débits de pointe et dimensionner les sections de canaux (circulaires, trapézoïdales, rectangulaires) pour les réseaux d'assainissement.
-   Dimensionner et vérifier les poteaux et radiers en béton armé sous diverses sollicitations.
-   Vérifier la résistance et la déformation des sections en bois (flexion, traction).
-   Générer des rapports de calcul détaillés et des plans de ferraillage (pour le béton armé).

## Fonctionnalités Clés
-   **Module Assainissement :**
    -   Calcul du temps de concentration (Kirpich, Californienne).
    -   Calcul de l'intensité de pluie (Montana, Talbot, Kiefer-Chu).
    -   Dimensionnement hydraulique des sections (circulaires, trapézoïdales, rectangulaires) selon Manning-Strickler.
    -   Gestion des données pluviométriques personnalisées.
    -   Génération de rapports PDF pour les simulations uniques et comparatives.
-   **Module Béton Armé :**
    -   Définition interactive des matériaux (béton, acier).
    -   Dimensionnement de poteaux rectangulaires en flexion composée ou compression centrée (BAEL 91).
    -   Calcul par lots de poteaux à partir de fichiers CSV.
    -   Analyse et prédimensionnement de radiers par la méthode des bandes.
    -   Génération de plans de ferraillage visuels.
-   **Module Bois :**
    -   Vérification de sections en bois en flexion et traction axiale selon l'Eurocode 5.
    -   Prise en compte des classes de service et durées de charge.
    -   Chargement des propriétés des classes de bois depuis un fichier CSV.
-   **Interface Utilisateur Interactive :** Menus clairs et invites pour une saisie guidée des données.
-   **Mode Verbeux :** Affichage détaillé des étapes de calcul pour une meilleure compréhension.
-   **Rapports Détaillés :** Génération automatique de rapports PDF et d'exports CSV des résultats.

## Installation

### Prérequis
-   Python 3.8+
-   `pip` (gestionnaire de paquets Python)

### Étapes d'installation
1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/prodeka/PROJET_DIMENTIONEMENT.git
    cd PROJET_DIMENTIONEMENT
    ```

2.  **Créer et activer un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    # Sur Windows:
    .\venv\Scripts\activate
    # Sur macOS/Linux:
    source venv/bin/activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
    Ou, si vous utilisez les scripts fournis :
    ```bash
    # Sur Windows:
    scripts\install.bat
    # Sur macOS/Linux:
    scripts/install.sh
    ```

## Utilisation

### Lancer l'application
Après l'installation, vous pouvez lancer l'application via le script principal :
```bash
# Sur Windows:
scripts\install_and_run.bat
# Sur macOS/Linux:
scripts/install_and_run.sh
```
Ou directement :
```bash
python src/nanostruct/main_app.py
```

### Options de ligne de commande
-   Pour activer le mode verbeux (affichage détaillé des calculs) :
    ```bash
    python src/nanostruct/main_app.py --verbose
    # ou
    python src/nanostruct/main_app.py -v
    ```

### Navigation dans l'application
L'application vous guidera à travers des menus interactifs pour choisir le module de dimensionnement (Assainissement, Béton Armé, Bois) et les options de calcul.

## Structure du Projet
```
PROJET_DIMENTIONEMENT/
├───.git/
├───.gitignore
├───PROJET_DIMENTIONEMENT.code-workspace
├───README.md
├───requirements.txt
├───build/
├───config/
│   └───pluviometrie_user.json  # Données pluviométriques personnalisées
├───data/
│   ├───ASS1.csv                # Exemples de données pour l'assainissement
│   ├───ASS2.csv
│   ├───classes_bois.csv        # Propriétés des classes de bois
│   ├───poteaux_a_calculer.csv  # Exemples de données pour le calcul par lots de poteaux
│   ├───poutres_a_calculer.csv
│   ├───profils_ipe.csv         # Profils IPE pour l'acier
│   └───psi_coeffs.csv          # Coefficients Psi pour les combinaisons de charges
├───dist/
├───docs/
├───output/
│   ├───rapports_assainissement/ # Rapports PDF générés pour l'assainissement
│   └───rapports_beton_arme/     # Rapports PDF et images générés pour le béton armé
├───scripts/
│   ├───install_and_run.bat      # Script d'installation et de lancement (Windows)
│   ├───install_and_run.sh       # Script d'installation et de lancement (Linux/macOS)
│   ├───install.bat              # Script d'installation des dépendances (Windows)
│   └───install.sh               # Script d'installation des dépendances (Linux/macOS)
├───src/
│   └───nanostruct/
│       ├───main_app.py          # Point d'entrée principal de l'application
│       ├───modules/
│       │   ├───assainissement/  # Module de calcul pour l'assainissement
│       │   │   ├───config/
│       │   │   ├───core/
│       │   │   ├───CSV/
│       │   │   ├───formulas.py
│       │   │   ├───main.py
│       │   │   ├───modules/
│       │   │   ├───plotting.py
│       │   │   ├───reporting.py
│       │   │   └───utils/
│       │   ├───beton_arme/      # Module de calcul pour le béton armé
│       │   │   ├───ba_entry.py  # Point d'entrée du module BA
│       │   │   ├───core/
│       │   │   ├───data/
│       │   │   ├───examples/
│       │   │   ├───reports/
│       │   │   └───tests/
│       │   └───bois/            # Module de calcul pour le bois
│       │       ├───main.py
│       │       ├───calculs/
│       │       └───db/
│       ├───ui/                  # Fonctions d'interface utilisateur (menus, saisie)
│       └───utils/               # Utilitaires généraux (settings, helpers)
├───tests/
├───utils/
└───vendor/
└───venv/                      # Environnement virtuel Python
```

## Contribution
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, veuillez suivre les étapes suivantes :
1.  Fork le dépôt.
2.  Créez une nouvelle branche (`git checkout -b feature/AmazingFeature`).
3.  Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`).
4.  Poussez vers la branche (`git push origin feature/AmazingFeature`).
5.  Ouvrez une Pull Request.

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
