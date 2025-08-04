
**Directives **`

implenter a ameliorer les fonctioinaliter hydrolique et aep avec les fonctio dispo dans le dossier amelioration

1.  **Transparence Mathématique :** Pour chaque valeur calculée, affichez explicitement la formule mathématique utilisée, suivie du calcul étape par étape, et enfin, le résultat calculé.
    *   **Exemple :**
        ```
        ### Calcul du Volume d'Incendie

        **Formule utilisée :**
        $V = D \times T$

        Où :
        *   $V$ = Volume d'incendie (en litres)
        *   $D$ = Débit d'eau (en litres/minute)
        *   $T$ = Temps de couverture (en minutes)

        **Exemple de Calcul :**
        Si le débit d'eau ($D$) est de 500 litres/minute et le temps de couverture ($T$) est de 30 minutes, alors :
        $V = 500 \text{ litres/minute} \times 30 \text{ minutes}$
        $V = 15000 \text{ litres}$

        **Résultat :** Le volume d'incendie est de 15 000 litres.
        ```

2.  **Approche Pédagogique :** Expliquez le but de chaque calcul, la signification des variables impliquées et les implications des résultats. Imaginez que vous enseignez le sujet à quelqu'un.

3.  **Formatage Markdown :** Toute la sortie doit être méticuleusement formatée en utilisant Markdown. Utilisez les titres, sous-titres, listes, blocs de code pour les formules et tableaux, le cas échéant, pour améliorer la lisibilité et la structure.

4.  **Intégration des Dépendances Externes (Pandoc) :**
    *   **Dépendance :** Assurez-vous que `pandoc` est répertorié comme une dépendance requise pour le programme.
    *   **Fonctionnalité :** Implémentez un mécanisme interne pour utiliser `pandoc` afin de convertir la sortie Markdown générée (contenant du LaTeX pour les expressions mathématiques) en différents formats de document tels que `.docx`, `.pdf`, `.html`, etc. [2, 3, 5, 6]
    *   **Option Utilisateur :** Offrez à l'utilisateur la possibilité de sélectionner le format de sortie souhaité (par exemple, "Exporter en DOCX", "Exporter en PDF"). [5, 6]

5.  **Fonctionnalités Internes (LCPI - Hypothétique) :**
    *   **Utilisation de LCPI :** Intégrez et utilisez les fonctionnalités avancées d'une bibliothèque de programme interne, appelée "LCPI", pour améliorer la génération de rapports. Cela pourrait inclure :
        *   **Récupération Dynamique de Données :** Extraction automatique de données pertinentes pour les calculs (par exemple, coefficients standard, propriétés des matériaux) si LCPI peut accéder à de telles bases de données.
        *   **Analyse de Scénarios :** Le cas échéant, permettre à LCPI d'exécuter plusieurs scénarios basés sur des paramètres définis par l'utilisateur et de présenter des résultats comparatifs dans le rapport.
        *   **Vérifications de Validation :** Utiliser les capacités de LCPI pour effectuer des vérifications de validation internes sur les résultats calculés (par exemple, par rapport aux normes de l'industrie ou aux limites de sécurité) et signaler toute divergence.

7. appliquer cette logique a tout les modules de calcul lcpi-cli que ce soit en mode cli ou repl

6.  **Saisie Utilisateur pour le Volume d'Incendie :**
    *   Le système doit explicitement demander à l'utilisateur deux paramètres clés pour calculer le "Volume d'Incendie" :
        *   **Débit :** Demandez à l'utilisateur de saisir le débit d'eau (par exemple, en litres par minute, en gallons par minute). [9, 10, 11]
        *   **Temps de Couverture :** Demandez à l'utilisateur de saisir la durée pendant laquelle le débit est appliqué (par exemple, en minutes, en heures). [9, 10, 11]
    *   Assurez-vous que le calcul du "Volume d'Incendie" est effectué et présenté conformément à la directive "Transparence Mathématique". [7, 8, 10, 11]

8. Pour le cas des calcul itterative afficher les resultats de chaque itteration et elle doit etre integrer comme sortie aussi. pour savoir quelle sont les calcule itterative parcours tout le projet

**Objectif Global :** L'objectif ultime est de générer une note de calcul complète, détaillée et pédagogiquement solide, facilement convertible en formats de documents professionnels, facilitant une compréhension claire et le transfert de connaissances.