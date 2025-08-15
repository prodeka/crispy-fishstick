"""
Classe Individu pour l'algorithme génétique.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Individu:
    """Représente un individu dans l'algorithme génétique."""
    diametres: List[int]
    fitness: float = 0.0
    cout_total: float = 0.0
    energie_totale: float = 0.0
    performance_hydraulique: float = 0.0
    
    def __post_init__(self):
        """Validation post-initialisation."""
        if not self.diametres:
            raise ValueError("Un individu doit avoir au moins un diamètre")
    
    def __len__(self):
        """Retourne le nombre de diamètres."""
        return len(self.diametres)
    
    def __getitem__(self, index):
        """Accès aux diamètres par index."""
        return self.diametres[index]
    
    def __setitem__(self, index, value):
        """Modification d'un diamètre par index."""
        self.diametres[index] = value
    
    def copy(self):
        """Retourne une copie de l'individu."""
        return Individu(
            diametres=self.diametres.copy(),
            fitness=self.fitness,
            cout_total=self.cout_total,
            energie_totale=self.energie_totale,
            performance_hydraulique=self.performance_hydraulique
        )
