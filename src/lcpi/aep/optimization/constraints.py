"""
Gestionnaire de contraintes pour l'optimisation des réseaux AEP.
"""

from typing import Dict, List
from .models import ContraintesBudget, ContraintesTechniques
from .individual import Individu

class ConstraintManager:
    """
    Gère la vérification des contraintes techniques et budgétaires.
    """
    
    def __init__(self, contraintes_budget: ContraintesBudget, contraintes_techniques: ContraintesTechniques):
        self.contraintes_budget = contraintes_budget
        self.contraintes_techniques = contraintes_techniques
    
    def verifier_contraintes(self, individu: Individu, reseau_data: Dict) -> bool:
        """Vérifie toutes les contraintes pour un individu."""
        return (
            self._verifier_contraintes_budget(individu) and
            self._verifier_contraintes_techniques(individu, reseau_data)
        )
    
    def _verifier_contraintes_budget(self, individu: Individu) -> bool:
        """Vérifie les contraintes budgétaires."""
        # Contrainte sur le coût total
        if individu.cout_total > self.contraintes_budget.cout_max_fcfa:
            return False
        
        # Contrainte sur le coût par mètre (si spécifiée)
        if self.contraintes_budget.cout_par_metre_max is not None:
            # Calculer la longueur totale du réseau
            longueur_totale = 0
            if hasattr(individu, 'longueurs') and individu.longueurs:
                longueur_totale = sum(individu.longueurs)
            
            if longueur_totale > 0:
                cout_par_metre = individu.cout_total / longueur_totale
                if cout_par_metre > self.contraintes_budget.cout_par_metre_max:
                    return False
        
        return True
    
    def _verifier_contraintes_techniques(self, individu: Individu, reseau_data: Dict) -> bool:
        """Vérifie les contraintes techniques."""
        if 'conduites' not in reseau_data:
            return True  # Pas de données de réseau, on suppose OK
        
        for i, diametre in enumerate(individu.diametres):
            if i >= len(reseau_data['conduites']):
                continue
                
            conduite = reseau_data['conduites'][i]
            debit = conduite.get('debit_m3_s', 0.1)
            
            # Calculer la vitesse
            section = 3.14159 * (diametre / 1000) ** 2 / 4
            vitesse = debit / section if section > 0 else 0
            
            # Vérifier les contraintes de vitesse
            if vitesse < self.contraintes_techniques.vitesse_min_m_s:
                return False
            if vitesse > self.contraintes_techniques.vitesse_max_m_s:
                return False
        
        return True
    
    def calculer_penalites(self, individu: Individu, reseau_data: Dict) -> float:
        """Calcule les pénalités pour violation des contraintes."""
        penalites = 0.0
        
        # Pénalité pour dépassement budgétaire
        if individu.cout_total > self.contraintes_budget.cout_max_fcfa:
            penalites += (individu.cout_total - self.contraintes_budget.cout_max_fcfa) * 0.1
        
        # Pénalités techniques
        if 'conduites' in reseau_data:
            for i, diametre in enumerate(individu.diametres):
                if i >= len(reseau_data['conduites']):
                    continue
                    
                conduite = reseau_data['conduites'][i]
                debit = conduite.get('debit_m3_s', 0.1)
                
                # Calculer la vitesse
                section = 3.14159 * (diametre / 1000) ** 2 / 4
                vitesse = debit / section if section > 0 else 0
                
                # Pénalités de vitesse
                if vitesse < self.contraintes_techniques.vitesse_min_m_s:
                    penalites += (self.contraintes_techniques.vitesse_min_m_s - vitesse) * 100
                if vitesse > self.contraintes_techniques.vitesse_max_m_s:
                    penalites += (vitesse - self.contraintes_techniques.vitesse_max_m_s) * 100
        
        return penalites
