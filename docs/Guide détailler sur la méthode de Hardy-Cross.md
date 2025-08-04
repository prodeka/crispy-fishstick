[[Guide Préliminaire QGIS pour la Méthode de Hardy-Cross]]

## Méthode de Calcul (Méthode de Hardy Cross)

> [!abstract] Principe
> La méthode de Hardy Cross est une technique itérative utilisée pour calculer les débits dans les réseaux de conduites maillés (en boucle) où les débits ne peuvent pas être déterminés directement. Elle repose sur le principe que la somme algébrique des pertes de charge dans une boucle fermée doit être nulle et que le principe de continuité (conservation du débit) doit être respecté à chaque nœud.

### Étapes de la Méthode

1.  **Calcul des Coefficients de Résistance ($K_i$)**
    *   À partir des caractéristiques de chaque conduite $i$ (longueur $L_i$, diamètre $d_i$, coefficient de rugosité ou $C_{Hw}$), calculer le coefficient de résistance $K_i$ basé sur la formule de perte de charge utilisée (ex: Darcy-Weisbach $H_L = K Q^2$, Hazen-Williams $H_L = K Q^{1.852}$). La formule générale est $H_{Li} = K_i Q_i^n$.
> [!info] Coefficients $K_i$
> Pour Hazen-Williams ($n=1.852$):
> $$
> K_i = \frac{\beta L_i}{d_i^{4.871} C_{Hw}^{1.852}}
> $$
> (Voir la fiche sur les valeurs de $\beta$ selon les unités).
    
*   Tenir compte des pertes de charge singulières ($K_s$) si elles sont importantes, en les ajoutant aux $K_i$ correspondants ou en les traitant comme des éléments séparés dans la somme des pertes de charge.

2.  **Répartition Initiale des Débits ($Q_{si}$)**
    *   Attribuer arbitrairement des débits initiaux $Q_{si}$ (débits supposés) dans chaque conduite $i$ du réseau.
    *   Cette répartition initiale **doit impérativement respecter la loi des nœuds** : la somme algébrique des débits à chaque nœud doit être nulle.
> [!important] Principe de Continuité aux Nœuds
> $$
> \Sigma Q_{entrant} = \Sigma Q_{sortant}
> $$
> ou
> $$
> \Sigma Q = 0 \quad \text{(à chaque nœud)}
> $$

*  important dependaement des boucle (anti horaire ou horaire )attribuer les signe par rapport au sens découlement imposer par les boucle pour chaque boucle au troncons au troncons Par exemple si le sens choisi pour les boucle est horaire, tous les troncons suivant cette direction est positif, au cas contraire negatif. NB: cést normal que selon une boucle un troncons soit posif et negatif dans l'autre. Cette etape peut etre fait dans qgis en cree un champs comme indiquer, en selectionnant boucle boucle et a láide de la calculatrice appliquer le sens (positif)
petite astuce, apres la copie des donner du sens dans par boucle, renitialiser tout les valeur de sens par null pour ne pas etre troubler

dans le traitement excel ajouter quíl faut filtrer par un champs pour garantir que lors que copier coler on ne fait pas d'erreur


3.  **Définition des Débits Supposés**
    *   Les débits déterminés à l'étape 2 sont notés $Q_{si}$ pour chaque conduite $i$. Ils constituent la première estimation.

4.  **Calcul des Pertes de Charge par Maille**
    *   Pour chaque **maille** (boucle fermée) du réseau :
        *   Choisir un sens de parcours (ex: horaire).
        *   Calculer la perte de charge $\Delta H_i = K_i Q_{si}^n$ pour chaque conduite $i$ de la maille. Le signe de $\Delta H_i$ dépend du signe de $Q_{si}$ (qui dépend du sens du débit par rapport au sens de parcours).
        *   Calculer la somme algébrique des pertes de charge pour la maille :
            $$
            \Sigma \Delta H_i = \Sigma (K_i Q_{si}^n)
            $$
    *   Idéalement, $\Sigma \Delta H_i$ devrait être nulle. Comme les $Q_{si}$ sont des estimations, cette somme sera généralement non nulle $\Sigma (K_i Q_{si}^n) \neq 0$. Cela indique une erreur $\Delta Q$ sur les débits supposés.
    *   On admet que le débit réel $Q_{ri}$ est lié au débit supposé $Q_{si}$ par $Q_{ri} = Q_{si} + \Delta Q$, où $\Delta Q$ est la correction à apporter (supposée identique pour toutes les conduites d'une même maille lors d'une itération).

5.  **Calcul du Terme Dénominateur pour la Correction**
    *   Pour chaque maille, calculer la somme suivante, qui correspond (à un facteur $n$ près) à la dérivée de la somme des pertes de charge par rapport au débit. Cette somme est toujours **positive** :
        $$
        \Sigma (n K_i |Q_{si}|^{n-1})
        $$
    *   On calcule $n K_i |Q_{si}|^{n-1}$ pour chaque conduite de la maille et on somme ces valeurs positives.
> [!note] Calcul Pratique
> Cette somme est le dénominateur utilisé pour calculer la correction $\Delta Q$.

6.  **Calcul de la Correction de Débit ($\Delta Q$)**
    *   Pour chaque maille, estimer la correction $\Delta Q$ à appliquer aux débits supposés $Q_{si}$:
        $$
        \Delta Q = - \frac{\Sigma (K_i Q_{si}^n)}{\Sigma (n K_i |Q_{si}|^{n-1})}
        $$
    *   Le numérateur $\Sigma (K_i Q_{si}^n)$ est la somme algébrique calculée à l'étape 4 (avec les signes).
    *   Le dénominateur $\Sigma (n K_i |Q_{si}|^{n-1})$ est la somme des termes positifs calculée à l'étape 5.
    *   Le signe de $\Delta Q$ indique si les débits supposés dans le sens de parcours de la maille doivent être augmentés ($\Delta Q > 0$) ou diminués ($\Delta Q < 0$).

7.  **Correction des Débits et Itération**
    *   Corriger les débits dans chaque conduite $i$ de la maille en utilisant :
        $$
        Q_{nouveau} = Q_{ancien} + \Delta Q_{maille}
        $$
    *   Pour une conduite $j$ appartenant à deux mailles (A et B), la correction est la somme des corrections des deux mailles, en tenant compte des signes relatifs.
> [!warning] Conduites Communes à Deux Mailles
> $Q_{nouveau, j} = Q_{ancien, j} + \Delta Q_A - \Delta Q_B$ (si le débit $Q_{ancien, j}$ est compté positivement dans A et négativement dans B selon les sens de parcours choisis). Adapter les signes selon la convention.
 
*   Les $Q_{nouveau}$ deviennent les $Q_{ancien}$ (ou $Q_{si}$) pour l'itération suivante, en n'oubliant pas de les ramener en valeurs absolue
*   **Répéter** les étapes 4 à 7 pour toutes les mailles jusqu'à ce que les valeurs de $\Delta Q$ (ou les sommes $\Sigma \Delta H_i$) soient suffisamment proches de zéro pour toutes les mailles, indiquant que les débits ont convergé vers la solution réelle.

### Remarque

*   La convergence de la méthode de Hardy Cross est généralement assurée mais peut être lente pour les grands réseaux ou si les estimations initiales sont très éloignées de la réalité.
*   Le choix de l'exposant $n$ dépend de la formule de perte de charge utilisée ($n=2$ pour Darcy-Weisbach, $n=1.852$ pour Hazen-Williams).