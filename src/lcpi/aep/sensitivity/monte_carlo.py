"""
Analyseur Monte-Carlo pour l'analyse de sensibilité des réseaux AEP.
"""

import random
import numpy as np
from typing import Dict, List, Tuple, Any, Callable
from dataclasses import dataclass
import time

@dataclass
class ParametreSensibilite:
    """Représente un paramètre pour l'analyse de sensibilité."""
    nom: str
    distribution: str  # "uniforme", "normale", "triangulaire"
    valeur_base: float
    min_val: float
    max_val: float
    moyenne: float = None
    ecart_type: float = None
    
    def generer_valeur(self) -> float:
        """Génère une valeur aléatoire selon la distribution."""
        if self.distribution == "uniforme":
            return random.uniform(self.min_val, self.max_val)
        elif self.distribution == "normale":
            if self.moyenne is None or self.ecart_type is None:
                self.moyenne = self.valeur_base
                self.ecart_type = (self.max_val - self.min_val) / 6
            return random.gauss(self.moyenne, self.ecart_type)
        elif self.distribution == "triangulaire":
            # Distribution triangulaire simplifiée
            u = random.random()
            if u < 0.5:
                return self.min_val + np.sqrt(2 * u) * (self.valeur_base - self.min_val)
            else:
                return self.valeur_base - np.sqrt(2 * (1 - u)) * (self.valeur_base - self.max_val)
        else:
            return self.valeur_base

class MonteCarloAnalyzer:
    """
    Analyseur Monte-Carlo pour évaluer la sensibilité des paramètres.
    """
    
    def __init__(self, parametres: List[ParametreSensibilite], iterations: int = 1000):
        self.parametres = parametres
        self.iterations = iterations
        self.resultats = []
        self.statistiques = {}
        self.temps_debut = None
        self.temps_fin = None
    
    def analyser_sensibilite(self, fonction_evaluation: Callable, **kwargs) -> Dict:
        """
        Exécute l'analyse Monte-Carlo.
        
        Args:
            fonction_evaluation: Fonction qui évalue le réseau avec des paramètres donnés
            **kwargs: Arguments supplémentaires pour la fonction d'évaluation
        """
        self.temps_debut = time.time()
        print(f"🔬 Démarrage de l'analyse Monte-Carlo...")
        print(f"   Paramètres: {len(self.parametres)}")
        print(f"   Itérations: {self.iterations}")
        
        self.resultats = []
        
        for i in range(self.iterations):
            # Générer des valeurs aléatoires pour tous les paramètres
            valeurs_parametres = {}
            for param in self.parametres:
                valeurs_parametres[param.nom] = param.generer_valeur()
            
            # Évaluer le réseau avec ces paramètres
            try:
                resultat = fonction_evaluation(**valeurs_parametres, **kwargs)
                resultat['iteration'] = i
                resultat['parametres'] = valeurs_parametres
                self.resultats.append(resultat)
            except Exception as e:
                print(f"⚠️  Erreur à l'itération {i}: {e}")
                continue
            
            # Affichage de progression
            if (i + 1) % 100 == 0:
                print(f"   Itération {i + 1}/{self.iterations}")
        
        self.temps_fin = time.time()
        
        # Calculer les statistiques
        self._calculer_statistiques()
        
        print(f"✅ Analyse Monte-Carlo terminée!")
        print(f"   Résultats valides: {len(self.resultats)}/{self.iterations}")
        print(f"   Temps total: {self.temps_fin - self.temps_debut:.2f} secondes")
        
        return self._generer_resultats()
    
    def _calculer_statistiques(self) -> None:
        """Calcule les statistiques sur les résultats."""
        if not self.resultats:
            return
        
        # Extraire les métriques principales
        metriques = ['cout_total', 'performance_hydraulique', 'energie_totale']
        
        for metrique in metriques:
            valeurs = [r.get(metrique, 0) for r in self.resultats if metrique in r]
            if valeurs:
                self.statistiques[metrique] = {
                    'moyenne': np.mean(valeurs),
                    'ecart_type': np.std(valeurs),
                    'min': np.min(valeurs),
                    'max': np.max(valeurs),
                    'median': np.median(valeurs),
                    'q25': np.percentile(valeurs, 25),
                    'q75': np.percentile(valeurs, 75)
                }
    
    def calculer_indices_sobol(self, metrique: str = 'cout_total') -> Dict:
        """
        Calcule les indices de Sobol pour identifier les paramètres les plus influents.
        Version simplifiée basée sur la variance.
        """
        if not self.resultats or metrique not in self.statistiques:
            return {}
        
        indices_sobol = {}
        
        for param in self.parametres:
            # Calculer la variance conditionnelle
            variance_totale = self.statistiques[metrique]['ecart_type'] ** 2
            
            if variance_totale == 0:
                indices_sobol[param.nom] = 0.0
                continue
            
            # Grouper les résultats par valeurs du paramètre
            groupes = {}
            for resultat in self.resultats:
                val_param = resultat['parametres'][param.nom]
                val_metrique = resultat.get(metrique, 0)
                
                # Créer des groupes de valeurs similaires
                groupe = round(val_param, 2)
                if groupe not in groupes:
                    groupes[groupe] = []
                groupes[groupe].append(val_metrique)
            
            # Calculer la variance entre groupes
            if len(groupes) > 1:
                moyennes_groupes = [np.mean(vals) for vals in groupes.values()]
                variance_entre_groupes = np.var(moyennes_groupes)
                indices_sobol[param.nom] = variance_entre_groupes / variance_totale
            else:
                indices_sobol[param.nom] = 0.0
        
        return indices_sobol
    
    def identifier_parametres_critiques(self, seuil: float = 0.1) -> List[Dict]:
        """Identifie les paramètres critiques selon les indices de Sobol."""
        indices_sobol = self.calculer_indices_sobol()
        
        parametres_critiques = []
        for nom, indice in indices_sobol.items():
            if indice > seuil:
                parametres_critiques.append({
                    'parametre': nom,
                    'indice_sobol': indice,
                    'impact': self._classifier_impact(indice)
                })
        
        # Trier par ordre décroissant d'impact
        parametres_critiques.sort(key=lambda x: x['indice_sobol'], reverse=True)
        return parametres_critiques
    
    def _classifier_impact(self, indice: float) -> str:
        """Classe l'impact d'un paramètre selon son indice de Sobol."""
        if indice > 0.5:
            return "très élevé"
        elif indice > 0.3:
            return "élevé"
        elif indice > 0.1:
            return "moyen"
        else:
            return "faible"
    
    def calculer_score_robustesse(self) -> float:
        """Calcule un score de robustesse global (0-1)."""
        if not self.statistiques:
            return 0.0
        
        scores = []
        for metrique, stats in self.statistiques.items():
            # Coefficient de variation (CV = écart_type / moyenne)
            if stats['moyenne'] != 0:
                cv = stats['ecart_type'] / abs(stats['moyenne'])
                # Score inversement proportionnel au CV
                score = max(0, 1 - cv)
                scores.append(score)
        
        return np.mean(scores) if scores else 0.0
    
    def identifier_zones_critiques(self) -> List[str]:
        """Identifie les zones critiques du réseau."""
        zones_critiques = []
        
        # Analyser les résultats pour identifier les problèmes récurrents
        if self.resultats:
            # Exemple: identifier les nœuds avec pression faible
            for resultat in self.resultats[:100]:  # Analyser un échantillon
                if 'pressions' in resultat:
                    for noeud, pression in resultat['pressions'].items():
                        if pression < 20:  # Pression < 20 mCE
                            zones_critiques.append(noeud)
        
        # Retourner les zones uniques
        return list(set(zones_critiques))
    
    def generer_rapport_detaille(self) -> Dict:
        """Génère un rapport détaillé de l'analyse."""
        indices_sobol = self.calculer_indices_sobol()
        parametres_critiques = self.identifier_parametres_critiques()
        score_robustesse = self.calculer_score_robustesse()
        zones_critiques = self.identifier_zones_critiques()
        
        return {
            "rapport_detaille": {
                "resume_execution": {
                    "iterations_demande": self.iterations,
                    "iterations_reussies": len(self.resultats),
                    "taux_reussite": len(self.resultats) / self.iterations * 100,
                    "temps_execution_s": self.temps_fin - self.temps_debut if self.temps_fin else 0
                },
                "analyse_parametres": {
                    "total_parametres": len(self.parametres),
                    "parametres_critiques": parametres_critiques,
                    "indices_sobol": indices_sobol
                },
                "evaluation_robustesse": {
                    "score_global": score_robustesse,
                    "zones_critiques": zones_critiques,
                    "recommandations": self._generer_recommandations(score_robustesse, parametres_critiques)
                }
            }
        }
    
    def _generer_recommandations(self, score_robustesse: float, parametres_critiques: List[Dict]) -> List[str]:
        """Génère des recommandations basées sur l'analyse."""
        recommandations = []
        
        if score_robustesse < 0.5:
            recommandations.append("Le réseau présente une faible robustesse. Considérer des marges de sécurité plus importantes.")
        
        if len(parametres_critiques) > 0:
            param_principal = parametres_critiques[0]
            recommandations.append(f"Le paramètre '{param_principal['parametre']}' a un impact {param_principal['impact']}. "
                                 f"Considérer une étude plus approfondie de ce paramètre.")
        
        if len(self.resultats) < self.iterations * 0.8:
            recommandations.append("Taux d'échec élevé dans les simulations. Vérifier la validité des paramètres d'entrée.")
        
        return recommandations
    
    def _generer_resultats(self) -> Dict:
        """Génère le contrat de sortie JSON canonique."""
        indices_sobol = self.calculer_indices_sobol()
        parametres_critiques = self.identifier_parametres_critiques()
        score_robustesse = self.calculer_score_robustesse()
        zones_critiques = self.identifier_zones_critiques()
        
        return {
            "analyse_sensibilite": {
                "methode": "monte_carlo",
                "iterations": self.iterations,
                "resultats_valides": len(self.resultats),
                "parametres_critiques": parametres_critiques,
              "indices_sobol": indices_sobol,
                "statistiques": self.statistiques,
                "robustesse": {
                    "score_global": score_robustesse,
                    "zones_critiques": zones_critiques
                },
                "temps_execution_s": self.temps_fin - self.temps_debut if self.temps_fin else 0
            }
        }
  