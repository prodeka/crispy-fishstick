"""
Algorithme génétique pour l'optimisation des diamètres de conduites.
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from .models import ConfigurationOptimisation, DiametreCommercial
from .constraints import ConstraintManager
from .individual import Individu

class GeneticOptimizer:
    """
    Optimiseur génétique pour la sélection des diamètres de conduites.
    """
    
    def __init__(self, config: ConfigurationOptimisation, constraint_manager: ConstraintManager):
        self.config = config
        self.constraint_manager = constraint_manager
        self.population: List[Individu] = []
        self.best_solution: Optional[Individu] = None
        self.history: List[Dict] = []
        
    def initialiser_population(self, nb_conduites: int) -> None:
        """Initialise la population avec des solutions aléatoires."""
        self.population = []
        
        for _ in range(self.config.algorithme.population_size):
            # Générer des diamètres aléatoires
            diametres = []
            for _ in range(nb_conduites):
                diametre = random.choice(self.config.diametres_candidats).diametre_mm
                diametres.append(diametre)
            
            individu = Individu(diametres=diametres)
            self.population.append(individu)
    
    def evaluer_fitness(self, individu: Individu, reseau_data: Dict) -> float:
        """Évalue la fitness d'un individu selon les critères définis."""
        # Calculer les métriques
        cout_total = self._calculer_cout_total(individu.diametres)
        energie_totale = self._calculer_energie_totale(individu.diametres, reseau_data)
        performance = self._calculer_performance_hydraulique(individu.diametres, reseau_data)
        
        # Stocker les métriques
        individu.cout_total = cout_total
        individu.energie_totale = energie_totale
        individu.performance_hydraulique = performance
        
        # Vérifier les contraintes
        if not self.constraint_manager.verifier_contraintes(individu, reseau_data):
            return 0.0  # Solution invalide
        
        # Calculer la fitness pondérée
        fitness = 0.0
        if self.config.criteres.principal == "cout":
            fitness += self.config.criteres.poids[0] * (1.0 / (1.0 + cout_total / 100000))
        elif self.config.criteres.principal == "energie":
            fitness += self.config.criteres.poids[0] * (1.0 / (1.0 + energie_totale / 10000))
        elif self.config.criteres.principal == "performance":
            fitness += self.config.criteres.poids[0] * performance
        
        # Ajouter les critères secondaires
        for i, critere in enumerate(self.config.criteres.secondaires):
            if critere == "cout":
                fitness += self.config.criteres.poids[i + 1] * (1.0 / (1.0 + cout_total / 100000))
            elif critere == "energie":
                fitness += self.config.criteres.poids[i + 1] * (1.0 / (1.0 + energie_totale / 10000))
            elif critere == "performance":
                fitness += self.config.criteres.poids[i + 1] * performance
        
        return fitness
    
    def _calculer_cout_total(self, diametres: List[int]) -> float:
        """Calcule le coût total des diamètres sélectionnés."""
        cout_total = 0.0
        for diametre in diametres:
            # Trouver le diamètre commercial correspondant
            for candidat in self.config.diametres_candidats:
                if candidat.diametre_mm == diametre:
                    cout_total += candidat.cout_fcfa_m
                    break
        return cout_total
    
    def _calculer_energie_totale(self, diametres: List[int], reseau_data: Dict) -> float:
        """Calcule l'énergie totale consommée (approximation)."""
        # Approximation basée sur les pertes de charge
        energie_totale = 0.0
        for i, diametre in enumerate(diametres):
            # Utiliser les données du réseau pour calculer les pertes
            if 'conduites' in reseau_data and i < len(reseau_data['conduites']):
                conduite = reseau_data['conduites'][i]
                longueur = conduite.get('longueur_m', 100)
                debit = conduite.get('debit_m3_s', 0.1)
                
                # Formule simplifiée pour les pertes de charge
                perte = self._calculer_pertes_charge(diametre, debit, longueur)
                energie_totale += perte * debit * 9.81  # Puissance en W
        
        return energie_totale
    
    def _calculer_performance_hydraulique(self, diametres: List[int], reseau_data: Dict) -> float:
        """Calcule la performance hydraulique globale."""
        performances = []
        
        for i, diametre in enumerate(diametres):
            if 'conduites' in reseau_data and i < len(reseau_data['conduites']):
                conduite = reseau_data['conduites'][i]
                debit = conduite.get('debit_m3_s', 0.1)
                
                # Calculer la vitesse
                section = np.pi * (diametre / 1000) ** 2 / 4
                vitesse = debit / section
                
                # Évaluer la performance (0-1)
                if 0.5 <= vitesse <= 2.0:
                    perf = 1.0
                elif 0.3 <= vitesse <= 2.5:
                    perf = 0.8
                else:
                    perf = 0.3
                
                performances.append(perf)
        
        return np.mean(performances) if performances else 0.0
    
    def _calculer_pertes_charge(self, diametre_mm: int, debit_m3_s: float, longueur_m: float) -> float:
        """Calcule les pertes de charge selon Hazen-Williams."""
        diametre_m = diametre_mm / 1000
        c = 120  # Coefficient de Hazen-Williams pour PVC
        
        # Formule de Hazen-Williams
        perte = 10.67 * (debit_m3_s / c) ** 1.852 / (diametre_m ** 4.87)
        return perte * longueur_m
    
    def selection_tournoi(self, k: int = 3) -> Individu:
        """Sélection par tournoi de k individus."""
        participants = random.sample(self.population, k)
        return max(participants, key=lambda x: x.fitness)
    
    def croisement(self, parent1: Individu, parent2: Individu) -> Tuple[Individu, Individu]:
        """Croisement de deux parents pour créer deux enfants."""
        if random.random() > self.config.algorithme.crossover_rate:
            return parent1, parent2
        
        # Croisement à un point
        point = random.randint(1, len(parent1.diametres) - 1)
        
        enfant1 = Individu(
            diametres=parent1.diametres[:point] + parent2.diametres[point:]
        )
        enfant2 = Individu(
            diametres=parent2.diametres[:point] + parent1.diametres[point:]
        )
        
        return enfant1, enfant2
    
    def mutation(self, individu: Individu) -> None:
        """Applique une mutation à un individu."""
        if random.random() < self.config.algorithme.mutation_rate:
            # Mutation aléatoire d'un diamètre
            idx = random.randint(0, len(individu.diametres) - 1)
            nouveau_diametre = random.choice(self.config.diametres_candidats).diametre_mm
            individu.diametres[idx] = nouveau_diametre
    
    def optimiser(self, reseau_data: Dict, nb_conduites: int) -> Dict:
        """Exécute l'optimisation génétique."""
        print(f"🚀 Démarrage de l'optimisation génétique...")
        print(f"   Population: {self.config.algorithme.population_size}")
        print(f"   Générations: {self.config.algorithme.generations}")
        print(f"   Conduites à optimiser: {nb_conduites}")
        
        # Initialiser la population
        self.initialiser_population(nb_conduites)
        
        # Boucle principale
        for generation in range(self.config.algorithme.generations):
            # Évaluer la fitness de tous les individus
            for individu in self.population:
                individu.fitness = self.evaluer_fitness(individu, reseau_data)
            
            # Trier par fitness
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            
            # Sauvegarder le meilleur
            if self.best_solution is None or self.population[0].fitness > self.best_solution.fitness:
                self.best_solution = Individu(
                    diametres=self.population[0].diametres.copy(),
                    fitness=self.population[0].fitness,
                    cout_total=self.population[0].cout_total,
                    energie_totale=self.population[0].energie_totale,
                    performance_hydraulique=self.population[0].performance_hydraulique
                )
            
            # Enregistrer l'historique
            self.history.append({
                'generation': generation,
                'meilleur_fitness': self.population[0].fitness,
                'moyenne_fitness': np.mean([ind.fitness for ind in self.population]),
                'meilleur_cout': self.population[0].cout_total,
                'meilleur_performance': self.population[0].performance_hydraulique
            })
            
            # Affichage de progression
            if generation % 10 == 0:
                print(f"   Génération {generation:3d}: Fitness={self.population[0].fitness:.4f}, "
                      f"Cout={self.population[0].cout_total:.0f}€, "
                      f"Perf={self.population[0].performance_hydraulique:.3f}")
            
            # Créer la nouvelle génération
            nouvelle_population = []
            
            # Élitisme: garder les meilleurs
            nb_elites = max(1, self.config.algorithme.population_size // 10)
            nouvelle_population.extend(self.population[:nb_elites])
            
            # Générer le reste de la population
            while len(nouvelle_population) < self.config.algorithme.population_size:
                # Sélection
                parent1 = self.selection_tournoi()
                parent2 = self.selection_tournoi()
                
                # Croisement
                enfant1, enfant2 = self.croisement(parent1, parent2)
                
                # Mutation
                self.mutation(enfant1)
                self.mutation(enfant2)
                
                nouvelle_population.extend([enfant1, enfant2])
            
            # Tronquer si nécessaire
            self.population = nouvelle_population[:self.config.algorithme.population_size]
        
        # Résultats finaux
        print(f"✅ Optimisation terminée!")
        print(f"   Meilleure solution trouvée:")
        print(f"   - Diamètres: {self.best_solution.diametres}")
        print(f"   - Coût total: {self.best_solution.cout_total:.0f}€")
        print(f"   - Performance: {self.best_solution.performance_hydraulique:.3f}")
        print(f"   - Fitness finale: {self.best_solution.fitness:.4f}")
        
        return self._generer_resultats()
    
    def _generer_resultats(self) -> Dict:
        """Génère le contrat de sortie JSON canonique."""
        return {
            "optimisation": {
                "algorithme": self.config.algorithme.type,
                "convergence": {
                    "iterations": self.config.algorithme.generations,
                    "fitness_finale": self.best_solution.fitness,
                    "temps_calcul_s": 0.0  # À implémenter avec time.time()
                },
                "meilleure_solution": {
                    "diametres": {f"C{i+1}": d for i, d in enumerate(self.best_solution.diametres)},
                    "performance": {
                        "cout_total_fcfa": self.best_solution.cout_total,
                        "energie_totale_kwh": self.best_solution.energie_totale / 3600,  # Conversion W→kWh
                        "performance_hydraulique": self.best_solution.performance_hydraulique
                    }
                },
                "historique": self.history
            }
        }
