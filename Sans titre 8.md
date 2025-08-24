**Prochaine action (potentielle, moins critique que les diamètres et la vitesse) :**

Pour que l'optimisation multi-objectif fonctionne pleinement et que l'OPEX/NPV soit un critère d'optimisation, il faudrait modifier la méthode `_extract_results` dans `src/lcpi/aep/core/epanet_wrapper.py` pour extraire également les débits et hauteurs des pompes à partir des résultats de simulation EPANET.

