
## **Améliorations possibles**

### **1. Architecture et évolutivité**

- **Centraliser la définition des paramètres**
    
    - Actuellement, les méthodes `analyser_sensibilite_dotation`, `analyser_sensibilite_croissance_demographique` et `analyser_sensibilite_fuites` ont encore des paramètres codés en dur.
        
    - Idée : utiliser `self.parametres_standard` comme source unique pour tous les calculs → moins d’erreurs, plus simple à maintenir.
        
- **Généraliser l’analyse de sensibilité**
    
    - Créer une méthode générique `analyser_parametre()` qui prend en entrée :
        
        - une fonction de calcul métier
            
        - un paramètre `SensitivityParameter`
            
        - la valeur de base
            
    - Cela évite de réécrire le même pattern de boucle, calcul des impacts, etc.
        
- **Séparer logique métier / génération de rapport**
    
    - Les méthodes `_generer_rapport_*` pourraient être déplacées dans une classe `AEPSensitivityReport` pour isoler la présentation des calculs.
        

---

### **2. Qualité du code**

- **Validation des entrées**
    
    - Vérifier que `population`, `dotation`, `rendement` soient > 0.
        
    - Lever des exceptions claires (`ValueError`) si les valeurs sont incohérentes.
        
- **Utiliser NumPy/Pandas**
    
    - Pour éviter des boucles `for` manuelles et rendre le calcul plus rapide si beaucoup de variations.
        
    - Exemple : calculer directement toutes les variations et impacts en vecteur.
        
- **Réduire la redondance**
    
    - Les méthodes d’analyse ont beaucoup de code répétitif (calcul min, max, moyenne, classification) → extraire ça dans une fonction commune.
        

---

### **3. Fonctionnalités supplémentaires**

- **Graphiques intégrés**
    
    - Générer automatiquement des graphiques de sensibilité (`matplotlib`) → plus visuel.
        
    - Exemple : courbe Variation (%) vs Impact (%).
        
- **Export multi-format complet**
    
    - Actuellement : JSON, Markdown, HTML → ajouter CSV pour exploitation dans Excel.
        
- **Poids relatif des paramètres**
    
    - Calculer un indicateur d’importance relative pour voir quels paramètres influencent le plus les besoins.
        
- **Mode batch**
    
    - Pouvoir lancer l’analyse sur une série de scénarios (différents villages, différents horizons) d’un coup.
        
- **Config externe**
    
    - Lire `self.parametres_standard` depuis un fichier `parametres.json` pour éviter de modifier le code en cas de changement.
        

---

### **4. Lisibilité et documentation**

- **Docstrings enrichis**
    
    - Ajouter des exemples d’utilisation dans les docstrings.
        
    - Expliquer le lien métier : pourquoi la variation de dotation impacte X ou Y.
        
- **Commentaires de formule**
    
    - Chaque calcul métier devrait avoir une référence à la formule ou norme utilisée (OMS, normes nationales).
        
- **Typage strict**
    
    - Tes annotations sont bonnes, mais tu peux activer `mypy` pour vérifier.
        

---

### **5. Robustesse**

- **Tests unitaires**
    
    - Écrire des tests avec `pytest` pour vérifier que :
        
        - Les variations sont bien calculées.
            
        - Les classes d’impact sont correctes.
            
        - Aucun crash si on met 0 ou valeurs extrêmes.
            
- **Tolérance flottants**
    
    - Utiliser `math.isclose` pour éviter les erreurs d’arrondi dans les comparaisons.
        
- **Gestion des grands nombres**
    
    - Si population > 1 million ou horizon > 50 ans, vérifier que les calculs ne débordent pas ou restent cohérents.
        

---
- Une **méthode générique** `analyser_parametre()` pour éviter la répétition
    
- Gestion **multi-paramètres**
    
- Export JSON/Markdown/HTML
    
- Génération automatique **de graphiques avec matplotlib**
    
- Lecture des paramètres depuis un **dictionnaire central**

"""
Analyse de sensibilité AEP - version améliorée
"""

import math
import json
from dataclasses import dataclass
from typing import Dict, List, Callable
import matplotlib.pyplot as plt
import os

@dataclass
class SensitivityParameter:
    nom: str
    valeur_base: float
    variation_pct: float
    pas: float
    unite: str
    description: str

@dataclass
class SensitivityResult:
    parametre: str
    variations: List[float]
    impacts: List[float]
    impact_max: float
    impact_min: float
    impact_moyen: float
    classe_impact: str

class AEPSensitivityAnalyzer:
    def __init__(self):
        # Définition centralisée des paramètres
        self.parametres_standard: Dict[str, SensitivityParameter] = {
            "dotation": SensitivityParameter("dotation", 60.0, 10.0, 2.0, "L/j/hab", "Dotation en eau par habitant"),
            "croissance_demographique": SensitivityParameter("croissance_demographique", 0.025, 30.0, 0.005, "%/an", "Taux de croissance démographique"),
            "fuites": SensitivityParameter("fuites", 0.05, 20.0, 0.01, "%", "Taux de fuites du réseau")
        }

    def analyser_parametre(
        self,
        param: SensitivityParameter,
        calc_impact: Callable[[float], float]
    ) -> SensitivityResult:
        variations = []
        impacts = []
        pas = param.pas
        nb_points = int(param.variation_pct / pas)

        for i in range(-nb_points, nb_points + 1):
            valeur_variee = param.valeur_base * (1 + i * pas / 100)
            variations.append(valeur_variee)
            impacts.append(calc_impact(valeur_variee))

        impact_max = max(impacts)
        impact_min = min(impacts)
        impact_moyen = sum(impacts) / len(impacts)

        if abs(impact_max) > 25:
            classe = "élevé"
        elif abs(impact_max) > 10:
            classe = "moyen"
        else:
            classe = "faible"

        return SensitivityResult(
            parametre=param.nom,
            variations=variations,
            impacts=impacts,
            impact_max=impact_max,
            impact_min=impact_min,
            impact_moyen=impact_moyen,
            classe_impact=classe
        )

    def analyser_sensibilite_globale(self, population: int, annees: int = 10, rendement: float = 0.95) -> Dict[str, SensitivityResult]:
        resultats = {}

        # Dotation
        def impact_dotation(valeur):
            besoin_base = population * self.parametres_standard["dotation"].valeur_base / 1000
            besoin_var = population * valeur / 1000
            return ((besoin_var - besoin_base) / besoin_base) * 100

        resultats["dotation"] = self.analyser_parametre(self.parametres_standard["dotation"], impact_dotation)

        # Croissance démographique
        def impact_croissance(valeur):
            pop_base = population * (1 + self.parametres_standard["croissance_demographique"].valeur_base) ** annees
            pop_var = population * (1 + valeur) ** annees
            return ((pop_var - pop_base) / pop_base) * 100

        resultats["croissance_demographique"] = self.analyser_parametre(self.parametres_standard["croissance_demographique"], impact_croissance)

        # Fuites
        def impact_fuites(valeur):
            demande_nette = population * self.parametres_standard["dotation"].valeur_base / 1000
            prod_base = demande_nette / rendement
            prod_var = demande_nette / valeur
            return ((prod_var - prod_base) / prod_base) * 100

        resultats["fuites"] = self.analyser_parametre(self.parametres_standard["fuites"], impact_fuites)

        return resultats

    def generer_rapport_json(self, resultats: Dict[str, SensitivityResult], fichier: str = "rapport.json"):
        rapport = {nom: {
            "variations": res.variations,
            "impacts": res.impacts,
            "impact_max": res.impact_max,
            "impact_min": res.impact_min,
            "impact_moyen": res.impact_moyen,
            "classe_impact": res.classe_impact
        } for nom, res in resultats.items()}
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2)
        print(f"Rapport JSON généré: {fichier}")

    def generer_graphiques(self, resultats: Dict[str, SensitivityResult], dossier: str = "graph_sensibilite"):
        os.makedirs(dossier, exist_ok=True)
        for nom, res in resultats.items():
            plt.figure()
            plt.plot(res.variations, res.impacts, marker='o')
            plt.title(f"Sensibilité : {nom}")
            plt.xlabel(f"{nom} ({self.parametres_standard[nom].unite})")
            plt.ylabel("Impact (%)")
            plt.grid(True)
            plt.savefig(os.path.join(dossier, f"{nom}.png"))
            plt.close()
        print(f"Graphiques générés dans le dossier: {dossier}")

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    analyzer = AEPSensitivityAnalyzer()
    res_globale = analyzer.analyser_sensibilite_globale(population=1000)
    analyzer.generer_rapport_json(res_globale)
    analyzer.generer_graphiques(res_globale)
