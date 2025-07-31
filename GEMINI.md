# Journal de Bord du Projet LCPI-CLI

Ce document retrace les étapes clés de la transition du projet `nanostruct` vers la nouvelle plateforme modulaire `LCPI-CLI`.

---

## **Phase 1 : Création de la Nouvelle Fondation LCPI - TERMINÉE**

**Date :** 30/07/2025

**Objectif atteint :**
- Création de la branche de développement `lpci_developpement`.
- Mise en place de l'arborescence du projet `lcpi_platform`.
- Création des squelettes pour le noyau (`lcpi-core`) et les plugins (`lcpi-cm`, `lcpi-bois`, `lcpi-beton`, `lcpi-assainissement`).
- Migration des utilitaires communs de `nanostruct` vers `lcpi-core`.
- Création du point d'entrée initial pour le noyau.

**Statut :** La fondation est prête. La prochaine étape est la migration de la logique de calcul métier dans les plugins respectifs.
---

## **Phase 4 : Remplissage des Plugins - TERMINÉE**

**Date :** 30/07/2025

**Objectifs :**
- Migrer la logique de calcul de `nanostruct` vers les nouvelles fonctions "pures" des plugins LCPI.
- Rendre les commandes `calc` et `check` réellement fonctionnelles.
- Nettoyer les dépendances vers l'ancien code.

**Avancement :**
- **Plugin `cm` (Construction Métallique) :**
    - [x] La logique de calcul pour le dimensionnement des poutres en acier a été migrée avec succès.
    - [x] La commande `lcpi cm calc` est maintenant fonctionnelle et lit les fichiers de définition YAML.
- **Plugin `bois` :**
    - [x] La logique de vérification pour les poutres en bois (Eurocode 5) a été migrée avec succès dans la fonction `_verifier_poutre_bois_logic`.
    - [x] La commande `lcpi bois check` est maintenant fonctionnelle et lit les fichiers de définition YAML.
- **Plugin `beton` :**
    - [x] La logique de calcul pour les poteaux en béton a été migrée.
    - [x] La commande `lcpi beton calc` est maintenant fonctionnelle pour les poteaux.
- **Plugin `assainissement` :**
    - [x] La logique de calcul pour le dimensionnement des réseaux a été migrée.
    - [x] La commande `lcpi assainissement calc` est maintenant fonctionnelle.

**Statut :** Tous les plugins ont été migrés avec succès. La transition est terminée.
---

## **Chantier 2 : Amélioration du Moteur de Rapport**

**Date :** 30/07/2025

**Objectifs :**
- Créer un moteur de rapport capable d'analyser tous les éléments d'un projet.
- Formater la sortie des calculs en JSON pour une communication inter-processus fiable.
- Générer un rapport de synthèse unique (HTML ou PDF).

**Avancement :**
- **Moteur de scan initial :**
    - [x] Une commande `lcpi report` a été ajoutée au noyau.
    - [x] La commande scanne les dossiers de plugins (`cm`, `bois`), trouve les fichiers `.yml`, et exécute les commandes `calc`/`check` correspondantes.
    - [x] La gestion des erreurs d'encodage de la sortie des sous-processus a été implémentée avec succès.
- **Communication Structurée :**
    - [x] Les plugins `cm` et `bois` ont été mis à jour pour accepter une option `--json` et retourner des résultats au format JSON.
    - [x] La commande `report` a été mise à jour pour utiliser cette option et parser la sortie JSON en un dictionnaire de résultats structurés.
- **Génération de Rapport :**
    - [x] Un nouveau module `reporter.py` a été créé dans le noyau.
    - [x] La commande `report` génère maintenant un rapport `rapport_lcpi.pdf` simple contenant les résultats de l'analyse.

**Statut :** Le Chantier 2 est terminé. Le moteur de rapport est fonctionnel.
---

## **Chantier 3 : Développement des Fonctionnalités Existantes**

**Date :** 30/07/2025

**Objectifs :**
- Intégrer les logiques de calcul existantes (radiers, etc.) dans les plugins correspondants.
- Assurer une couverture de test pour les nouvelles commandes.
- Continuer à améliorer la sortie et les rapports.

**Avancement :**
- **Plugin `beton` (Radiers) :**
    - [x] Une commande `calc-radier` a été ajoutée au plugin `beton`.
    - [x] La logique de calcul des moments par la méthode des bandes a été migrée et est fonctionnelle.
---

## **Chantier 4 : Finalisation du Mode Interactif**

**Date :** 30/07/2025

**Objectifs :**
- Remplacer les anciens fichiers `main.py` des plugins par des versions finales.
- Implémenter une commande `interactive` pour chaque plugin majeur.
- Préparer la refonte du plugin `assainissement`.

**Avancement :**
- **Plugin `cm` :**
    - [x] Le mode `interactive` est terminé et fonctionnel.
- **Plugin `bois` :**
    - [x] Le mode `interactive` est terminé et fonctionnel.
- **Plugin `beton` :**
    - [x] Le mode `interactive` a été ajouté avec un menu pour Poteau/Radier.
    - [x] La logique pour le calcul de Poteau est connectée.
- **Plugin `assainissement` :**
    ## **Chantier 5 : Lanceur du Noyau et Autonomie des Plugins**

**Date :** 31/07/2025

**Objectifs :**
- Créer un script unique qui gère l'installation et le lancement du noyau LCPI.
- Rendre le chargement des plugins entièrement dépendant des commandes de l'utilisateur (`lcpi plugins install`).
- Simplifier le premier contact avec l'application.

**Avancement :**
- **Nouveau Lanceur :**
    - [x] Le script `scripts/install.py` a été renommé en `scripts/install_and_run_lcpi_core.py`.
    - [x] Ce script gère désormais l'installation des dépendances (en ligne et hors ligne) puis lance directement le noyau de l'application.
- **Démarrage du Noyau Seul :**
    - [x] Le lanceur utilise une variable d'environnement (`LCPI_CORE_ONLY_LAUNCH=1`) pour démarrer l'application sans charger les plugins.
    - [x] `src/lcpi/main.py` a été modifié pour ne pas appeler `print_plugin_status()` si cette variable est détectée.
    - [x] L'utilisateur est maintenant accueilli par le noyau LCPI pur et doit utiliser `lcpi plugins install <nom>` pour activer les fonctionnalités.

**Statut :** Le Chantier 5 est terminé. L'expérience de démarrage est plus propre et la gestion des plugins est désormais entièrement sous le contrôle de l'utilisateur.