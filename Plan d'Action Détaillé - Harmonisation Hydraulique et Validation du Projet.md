**Plan d'Action Détaillé : Harmonisation Hydraulique et Validation du Projet**

**Priorité 1 : Harmonisation des Modèles et Coefficients Hydrauliques**

C'est la cause la plus probable de l'écart de coût majeur. Il faut que les deux solveurs utilisent les mêmes règles physiques.

- **Action Concrète 1.1 : Modifier le Fichier INP pour Utiliser Hazen-Williams (H-W)**
    - **Localisation :** Ouvrez le fichier `bismark-Administrator.inp` (ou le fichier INP que vous utilisez pour les tests).
    - **Modification :** Dans la section `[OPTIONS]`, changez la ligne `Headloss C-M` en `Headloss H-W`.
- **Action Concrète 1.2 : Convertir les Coefficients de Rugosité C-M en H-W**
    - **Problème :** Le fichier INP contient des coefficients de rugosité pour Chezy-Manning (156.4, 108.4, 94.4). Vous avez besoin des coefficients équivalents pour Hazen-Williams (coefficient 'C').
    - **Recherche Documentaire :** Recherchez des formules ou des tables de conversion pour passer des coefficients de Chezy-Manning aux coefficients de Hazen-Williams. La relation dépend du diamètre de la conduite. Une formule courante relie C (Hazen-Williams) et n (Manning) : `C ≈ (1/n) * R^(1/6)`, où R est le rayon hydraulique (approximativement D/4 pour une conduite circulaire pleine). La relation avec Chezy (C_chezy) est `C_chezy = (1/n) * R^(1/6) * g^(1/2)`, où g est l'accélération de la gravité. Il existe des abaques ou des formules approchées.
    - **Action Concrète :**
        - Identifiez le matériau correspondant à chaque coefficient de rugosité Chezy dans votre INP (par exemple, 156.4 pour PVC, 108.4 pour Fonte, etc.).
        - Trouvez une méthode de conversion fiable C-M -> H-W (recherche documentaire).
        - Calculez ou trouvez les coefficients Hazen-Williams ('C') correspondants pour chaque matériau et pour les diamètres pertinents de votre réseau.
        - Modifiez le fichier INP : dans la section `[PIPES]`, remplacez les coefficients de rugosité Chezy-Manning par les coefficients Hazen-Williams calculés. Assurez-vous que les entêtes de colonne dans `[PIPES]` correspondent également au modèle de perte de charge choisi (`C` si H-W, `N` si Manning, `K` si D-W).
- **Action Concrète 1.3 : Vérifier le Modèle Utilisé par LCPI**
    - **Localisation :** Examinez le code de votre solveur LCPI Hardy-Cross (`src/lcpi/aep/core/solvers/lcpi_solver.py` ou les modules qu'il utilise pour les calculs hydrauliques).
    - **Vérification :** Quel modèle de perte de charge (H-W, D-W) votre code utilise-t-il pour calculer les pertes de charge dans les conduites ? Quel paramètre de rugosité utilise-t-il (C, ε, n) ?
- **Action Concrète 1.4 : Assurer la Cohérence LCPI**
    - Si LCPI utilise Hazen-Williams, assurez-vous qu'il lit et utilise correctement les coefficients 'C' que vous avez mis dans le fichier INP.
    - Si LCPI utilise Darcy-Weisbach, vous devrez convertir les coefficients C-M en coefficients de rugosité absolue (ε) pour D-W et modifier l'INP en conséquence.
- **Action Concrète 1.5 : Relancer les Tests Harmonisé**
    - **Commande :** Exécutez à nouveau votre script de comparaison (`tools/compare_solvers.py`) ou les tests avec contraintes harmonisées sur le fichier INP modifié (avec `Headloss H-W` et les coefficients 'C' convertis).
    - **Analyse :** Comparez les résultats de coût, faisabilité et distribution des diamètres. L'écart devrait se réduire significativement.

**Priorité 2 : Validation de l'Implémentation LCPI Hardy-Cross et de la Structure du Projet**

Vous avez eu des messages indiquant que le fichier Hardy-Cross était "manquant". C'est préoccupant.

- **Action Concrète 2.1 : Localiser et Vérifier le Fichier Hardy-Cross**
    - **Localisation :** Où se trouve le code principal de votre algorithme Hardy-Cross (`_run_hardy_cross` ou équivalent) ? Est-il bien dans un fichier accessible depuis `src/lcpi/aep/core/solvers/lcpi_solver.py` ?
    - **Vérification :** Assurez-vous que le fichier existe, qu'il n'y a pas de faute de frappe dans le nom du fichier ou dans les imports y faisant référence.
- **Action Concrète 2.2 : Créer des Tests Unitaires Spécifiques au Solveur LCPI Hardy-Cross**
    - **Action :** Écrivez un script Python simple qui crée manuellement un très petit réseau maillé (par exemple, 3 nœuds, 3 conduites formant une boucle, 1 réservoir).
    - **Action :** Appelez directement la méthode `run_simulation` (ou l'équivalent) de votre `LcpiHardyCrossSolver` avec les données de ce petit réseau.
    - **Validation :** Vérifiez que le solveur s'exécute sans erreur, qu'il converge, et que les résultats hydrauliques (débits dans la boucle, pressions aux nœuds) sont cohérents et correspondent à ce que vous attendez pour un tel réseau simple (vous pouvez le vérifier manuellement ou avec une simulation EPANET sur le même petit réseau).
    - **Transparence :** Vérifiez que la trace de convergence (si implémentée) est correctement générée et accessible.
- **Recherche Documentaire :** Recherchez des exemples d'implémentations simples de l'algorithme Hardy-Cross ou des problèmes de réseaux hydrauliques de base avec solutions connues pour valider vos calculs.
- **Action Concrète 2.3 : Vérifier la Gestion des Éléments (Tanks)**
    - Votre investigation a détecté 3 TANKS dans le réseau INP. Un solveur Hardy-Cross "pur" gère les boucles de conduites. Les réservoirs sont des points de pression fixe qui peuvent influencer les boucles.
    - **Vérification :** Comment votre solveur LCPI Hardy-Cross gère-t-il les réservoirs ? Sont-ils correctement intégrés dans la formulation du problème (points avec élévation et pression connue) ?
    - **Test :** Créez un petit réseau simple avec un réservoir et une ou deux conduites et vérifiez que LCPI calcule correctement les débits et pressions.

**Priorité 3 : Affinage de l'Optimisation et de la Validation**

Une fois l'harmonisation hydraulique et la base du solveur validées, concentrez-vous sur l'algorithme génétique et les métriques.

- **Action Concrète 3.1 : Affiner la Fonction d'Évaluation de l'AG**
    - **Localisation :** Examinez `src/lcpi/aep/optimizer/genetic_algorithm.py` et `src/lcpi/aep/optimizer/scoring.py` ou `constraints_handler.py`.
    - **Vérification :** Comment la fitness est-elle calculée ? Comment les violations de contraintes sont-elles pénalisées ?
    - **Amélioration :** Implémentez un schéma de pénalité qui décourage _fortement_ les solutions non faisables. Par exemple, une pénalité qui augmente rapidement à mesure que la violation de contrainte s'aggrave, ou un système de rang basé sur la faisabilité avant le coût.
- **Recherche Documentaire :** Recherchez des méthodes courantes pour gérer les contraintes dans les algorithmes génétiques pour l'optimisation de réseaux hydrauliques (pénalités statiques, dynamiques, méthodes de réparation, etc.).
- **Action Concrète 3.2 : Assurer que les Métriques Hydrauliques sont Collectées et Affichées**
    - **Problème :** Le rapport a signalé que les métriques de pression/vitesse sont N/A.
    - **Vérification :** Après une simulation réussie avec votre solveur LCPI, les résultats de pression et vitesse sont-ils correctement structurés et inclus dans le dictionnaire de retour ? Le pipeline de traitement des résultats de l'AG collecte-t-il ces métriques ?
    - **Correction :** Modifiez le code pour vous assurer que les statistiques hydrauliques sont toujours calculées et affichées pour toutes les solutions simulées (même non faisables, pour analyse).
- **Action Concrète 3.3 : Améliorer la Journalisation Détaillée**
    - **Action :** Ajoutez des instructions de journalisation (`logging.info(...)` ou `print(...)` si le logging n'est pas configuré) dans des endroits clés de votre code :
        - Début/fin de la simulation Hardy-Cross.
        - Début/fin de l'évaluation d'un individu dans l'AG.
        - Calcul du coût d'une conduite (longueur, diamètre, matériau, prix unitaire utilisé).
        - Vérification des contraintes pour un nœud/conduite (pression calculée vs min/max, vitesse calculée vs min/max, montant de la violation).
    - **Objectif :** Permettre une traçabilité complète du processus pour identifier l'origine des éventuels problèmes restants.

**Recherche Documentaire Générale pour la Conformité et la Robustesse :**

- **Normes de Conception de Réseaux AEP :** Recherchez les normes nationales ou internationales pour la conception de réseaux d'eau potable (pression minimale/maximale typique, vitesses minimales pour éviter les dépôts, vitesses maximales pour limiter l'érosion et les pertes de charge). Cela vous aidera à choisir des contraintes hydrauliques réalistes.
- **Optimisation de Réseaux AEP :** Recherchez des articles scientifiques ou des ressources sur l'optimisation de réseaux d'eau potable, en particulier l'utilisation d'algorithmes génétiques et la gestion des contraintes.
- **Modèles de Pertes de Charge :** Approfondissez votre compréhension des modèles Hazen-Williams, Darcy-Weisbach et Chezy-Manning, et des contextes dans lesquels ils sont typiquement utilisés.

Ce plan est ambitieux mais il couvre tous les points nécessaires pour valider et rendre robuste votre module d'optimisation. Commencer par l'harmonisation des modèles hydrauliques (Priorité 1) est la première étape logique, car elle garantit que les deux solveurs travaillent sur le même problème fondamental.