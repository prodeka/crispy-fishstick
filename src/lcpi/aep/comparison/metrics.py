"""
Métriques de comparaison pour les variantes de réseaux AEP.
"""

import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class MetriqueComparaison:
    """Représente une métrique de comparaison entre variantes."""
    nom: str
    valeur_variante1: float
    valeur_variante2: float
    difference_absolue: float
    difference_relative: float
    meilleure_variante: str
    amelioration_pct: float

class ComparisonMetrics:
    """
    Calcule les métriques de comparaison entre variantes de réseau.
    """
    
    def __init__(self):
        self.metriques = []
    
    def comparer_variantes(self, variante1: Dict, variante2: Dict, nom_variante1: str = "base", nom_variante2: str = "optimisee") -> Dict:
        """
        Compare deux variantes de réseau et calcule les métriques.
        
        Args:
            variante1: Données de la première variante
            variante2: Données de la deuxième variante
            nom_variante1: Nom de la première variante
            nom_variante2: Nom de la deuxième variante
        """
        print(f"📊 Comparaison des variantes: {nom_variante1} vs {nom_variante2}")
        
        # Métriques de coût
        cout1 = variante1.get('cout_total_fcfa', 0)
        cout2 = variante2.get('cout_total_fcfa', 0)
        self._ajouter_metrique("cout_total_fcfa", cout1, cout2, nom_variante1, nom_variante2, inverser=True)
        
        # Métriques de performance
        perf1 = variante1.get('performance_hydraulique', 0)
        perf2 = variante2.get('performance_hydraulique', 0)
        self._ajouter_metrique("performance_hydraulique", perf1, perf2, nom_variante1, nom_variante2)
        
        # Métriques d'énergie
        energie1 = variante1.get('energie_totale', 0)
        energie2 = variante2.get('energie_totale', 0)
        self._ajouter_metrique("energie_totale", energie1, energie2, nom_variante1, nom_variante2, inverser=True)
        
        # Métriques de robustesse
        robustesse1 = variante1.get('robustesse', {}).get('score_global', 0)
        robustesse2 = variante2.get('robustesse', {}).get('score_global', 0)
        self._ajouter_metrique("robustesse", robustesse1, robustesse2, nom_variante1, nom_variante2)
        
        return self._generer_resultats_comparaison(nom_variante1, nom_variante2)
    
    def _ajouter_metrique(self, nom: str, val1: float, val2: float, nom1: str, nom2: str, inverser: bool = False) -> None:
        """Ajoute une métrique de comparaison."""
        if val1 == 0 and val2 == 0:
            return
        
        # Déterminer quelle variante est meilleure
        if inverser:
            # Pour les métriques où "moins c'est mieux" (coût, énergie)
            if val1 < val2:
                meilleure = nom1
                amelioration = ((val1 - val2) / val2) * 100 if val2 != 0 else 0
            else:
                meilleure = nom2
                amelioration = ((val2 - val1) / val1) * 100 if val1 != 0 else 0
        else:
            # Pour les métriques où "plus c'est mieux" (performance, robustesse)
            if val1 > val2:
                meilleure = nom1
                amelioration = ((val1 - val2) / val2) * 100 if val2 != 0 else 0
            else:
                meilleure = nom2
                amelioration = ((val2 - val1) / val1) * 100 if val1 != 0 else 0
        
        difference_abs = abs(val2 - val1)
        difference_rel = (difference_abs / val1) * 100 if val1 != 0 else 0
        
        metrique = MetriqueComparaison(
            nom=nom,
            valeur_variante1=val1,
            valeur_variante2=val2,
            difference_absolue=difference_abs,
            difference_relative=difference_rel,
            meilleure_variante=meilleure,
            amelioration_pct=abs(amelioration)
        )
        
        self.metriques.append(metrique)
    
    def calculer_score_global(self, poids: Dict[str, float] = None) -> float:
        """Calcule un score global de comparaison."""
        if not self.metriques:
            return 0.0
        
        # Poids par défaut si non spécifiés
        if poids is None:
            poids = {
                'cout_total_fcfa': 0.4,
                'performance_hydraulique': 0.3,
                'energie_totale': 0.2,
                'robustesse': 0.1
            }
        
        score_total = 0.0
        poids_total = 0.0
        
        for metrique in self.metriques:
            if metrique.nom in poids:
                # Normaliser la différence relative (0-1)
                diff_norm = min(metrique.difference_relative / 100, 1.0)
                score_total += poids[metrique.nom] * diff_norm
                poids_total += poids[metrique.nom]
        
        return score_total / poids_total if poids_total > 0 else 0.0
    
    def identifier_avantages_principaux(self, variante: str) -> List[str]:
        """Identifie les avantages principaux d'une variante."""
        avantages = []
        
        for metrique in self.metriques:
            if metrique.meilleure_variante == variante:
                avantages.append(f"{metrique.nom}: +{metrique.amelioration_pct:.1f}%")
        
        return avantages
    
    def generer_recommandation(self) -> Dict:
        """Génère une recommandation basée sur la comparaison."""
        if not self.metriques:
            return {"recommandation": "Aucune comparaison disponible"}
        
        # Compter les victoires par variante
        victoires = {}
        for metrique in self.metriques:
            variante = metrique.meilleure_variante
            victoires[variante] = victoires.get(variante, 0) + 1
        
        # Identifier la variante gagnante
        variante_gagnante = max(victoires, key=victoires.get)
        nb_victoires = victoires[variante_gagnante]
        total_metriques = len(self.metriques)
        
        # Calculer le score global
        score_global = self.calculer_score_global()
        
        # Générer la justification
        avantages = self.identifier_avantages_principaux(variante_gagnante)
        justification = f"La variante '{variante_gagnante}' remporte {nb_victoires}/{total_metriques} métriques. "
        justification += f"Avantages: {', '.join(avantages)}"
        
        return {
            "recommandation": variante_gagnante,
            "justification": justification,
            "score_global": score_global,
            "victoires": victoires,
            "avantages_principaux": avantages
        }
    
    def _generer_resultats_comparaison(self, nom_variante1: str, nom_variante2: str) -> Dict:
        """Génère le contrat de sortie JSON canonique pour la comparaison."""
        score_global = self.calculer_score_global()
        recommandation = self.generer_recommandation()
        
        return {
            "comparaison": {
                "variantes_comparees": [nom_variante1, nom_variante2],
                "metriques": [
                    {
                        "nom": m.nom,
                        "valeur_variante1": m.valeur_variante1,
                        "valeur_variante2": m.valeur_variante2,
                        "difference_absolue": m.difference_absolue,
                        "difference_relative": m.difference_relative,
                        "meilleure_variante": m.meilleure_variante,
                        "amelioration_pct": m.amelioration_pct
                    }
                    for m in self.metriques
                ],
                "score_global": score_global,
                "recommandation": recommandation["recommandation"],
                "justification": recommandation["justification"],
                "victoires": recommandation["victoires"]
            }
        }
