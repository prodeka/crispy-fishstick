---
tags:
  - concept/hydraulique
  - méthode/calcul
  - aep
---

# Méthode de Hardy-Cross

La méthode de Hardy-Cross est un **processus itératif historique** utilisé pour calculer la distribution des débits dans un réseau maillé d'eau potable, en s'assurant que les lois de Kirchhoff hydrauliques (loi des nœuds et loi des mailles) sont respectées.

## Rôle et Utilité
Aujourd'hui, cette méthode est principalement un **outil pédagogique exceptionnel** pour comprendre les mécanismes fondamentaux d'équilibrage des flux et des pertes de charge dans une boucle. Elle force l'ingénieur à :
1.  Poser des hypothèses logiques sur le sens des écoulements.
2.  Vérifier la continuité des débits à chaque nœud (Loi des Nœuds).
3.  Calculer itérativement une correction de débit (`ΔQ`) pour chaque maille jusqu'à ce que la somme des pertes de charge soit proche de zéro (Loi des Mailles).

En pratique, ces calculs sont désormais entièrement automatisés par les solveurs hydrauliques comme celui de [[Outil - EPA SWMM]].

## Approfondissement
Pour une explication détaillée du processus de calcul, des formules et un exemple d'application, se référer à la ressource principale :
➡️ **[[Guide détailler sur la méthode de Hardy-Cross]]**

## Connexions & Réflexions
- Cette méthode est la base conceptuelle des solveurs modernes qui permettent le [[Processus Itératif de Dimensionnement AEP]].
- Comprendre Hardy-Cross aide à diagnostiquer des problèmes dans les modèles numériques, comme les instabilités (`System ill-conditioned`).

## Source(s)
- [[CONV - Débriefing Projet AEP Fidokpui & Dikame]]
- 