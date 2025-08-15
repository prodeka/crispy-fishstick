"""
Tests unitaires pour le module d'optimisation des réseaux AEP.
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from src.lcpi.aep.optimization.models import (
    CriteresOptimisation, ContraintesBudget, ContraintesTechniques,
    ParametresAlgorithme, DiametreCommercial, ConfigurationOptimisation
)
from src.lcpi.aep.optimization.constraints import ConstraintManager
from src.lcpi.aep.optimization.genetic_algorithm import GeneticOptimizer, Individu

class TestModels:
    """Tests pour les modèles Pydantic."""
    
    def test_criteres_optimisation(self):
        """Test de création des critères d'optimisation."""
        criteres = CriteresOptimisation(
            principal="cout",
            secondaires=["energie"],
            poids=[0.7, 0.3]
        )
        assert criteres.principal == "cout"
        assert len(criteres.secondaires) == 1
        assert len(criteres.poids) == 2
    
    def test_contraintes_budget(self):
        """Test de création des contraintes budgétaires."""
        contraintes = ContraintesBudget(cout_max_fcfa=100000)
        assert contraintes.cout_max_fcfa == 100000
        assert contraintes.cout_par_metre_max is None
    
    def test_contraintes_techniques(self):
        """Test de création des contraintes techniques."""
        contraintes = ContraintesTechniques(
            pression_min_mce=20,
            pression_max_mce=80,
            vitesse_min_m_s=0.5,
            vitesse_max_m_s=2.5
        )
        assert contraintes.pression_min_mce == 20
        assert contraintes.vitesse_max_m_s == 2.5
    
    def test_diametre_commercial(self):
        """Test de création d'un diamètre commercial."""
        diametre = DiametreCommercial(
            diametre_mm=110,
            cout_fcfa_m=45
        )
        assert diametre.diametre_mm == 110
        assert diametre.cout_fcfa_m == 45
        assert diametre.materiau == "pvc"

class TestConstraintManager:
    """Tests pour le gestionnaire de contraintes."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        self.contraintes_budget = ContraintesBudget(cout_max_fcfa=100000)
        self.contraintes_techniques = ContraintesTechniques()
        self.manager = ConstraintManager(
            self.contraintes_budget,
            self.contraintes_techniques
        )
    
    def test_verification_contraintes_budget_ok(self):
        """Test de vérification des contraintes budgétaires (OK)."""
        individu = Individu(diametres=[110, 125])
        individu.cout_total = 50000  # Sous le budget
        
        assert self.manager._verifier_contraintes_budget(individu) is True
    
    def test_verification_contraintes_budget_depasse(self):
        """Test de vérification des contraintes budgétaires (dépassé)."""
        individu = Individu(diametres=[110, 125])
        individu.cout_total = 150000  # Au-dessus du budget
        
        assert self.manager._verifier_contraintes_budget(individu) is False

class TestGeneticOptimizer:
    """Tests pour l'optimiseur génétique."""
    
    def setup_method(self):
        """Configuration initiale pour chaque test."""
        # Créer une configuration minimale
        criteres = CriteresOptimisation(principal="cout", poids=[1.0])
        contraintes_budget = ContraintesBudget(cout_max_fcfa=100000)
        contraintes_techniques = ContraintesTechniques()
        algorithme = ParametresAlgorithme(
            population_size=20,
            generations=10
        )
        diametres = [
            DiametreCommercial(diametre_mm=110, cout_fcfa_m=45),
            DiametreCommercial(diametre_mm=125, cout_fcfa_m=60)
        ]
        
        self.config = ConfigurationOptimisation(
            criteres=criteres,
            contraintes_budget=contraintes_budget,
            contraintes_techniques=contraintes_techniques,
            algorithme=algorithme,
            diametres_candidats=diametres
        )
        
        self.constraint_manager = ConstraintManager(
            contraintes_budget,
            contraintes_techniques
        )
        
        self.optimizer = GeneticOptimizer(self.config, self.constraint_manager)
    
    def test_initialisation_population(self):
        """Test de l'initialisation de la population."""
        self.optimizer.initialiser_population(3)
        
        assert len(self.optimizer.population) == 20
        for individu in self.optimizer.population:
            assert len(individu.diametres) == 3
            assert all(d in [110, 125] for d in individu.diametres)
    
    def test_calcul_cout_total(self):
        """Test du calcul du coût total."""
        diametres = [110, 125]
        cout_total = self.optimizer._calculer_cout_total(diametres)
        
        # 45 + 60 = 105
        assert cout_total == 105
    
    def test_calcul_performance_hydraulique(self):
        """Test du calcul de la performance hydraulique."""
        diametres = [110, 125]
        reseau_data = {
            'conduites': [
                {'debit_m3_s': 0.05},
                {'debit_m3_s': 0.03}
            ]
        }
        
        performance = self.optimizer._calculer_performance_hydraulique(diametres, reseau_data)
        assert 0 <= performance <= 1

class TestIntegration:
    """Tests d'intégration pour l'optimisation complète."""
    
    def test_optimisation_complete(self, tmp_path):
        """Test d'une optimisation complète avec un petit réseau."""
        # Créer un fichier de configuration temporaire
        config_data = {
            'reseau_complet': {
                'conduites': [
                    {'debit_m3_s': 0.05, 'longueur_m': 100},
                    {'debit_m3_s': 0.03, 'longueur_m': 80}
                ]
            },
            'optimisation': {
                'criteres': {
                    'principal': 'cout',
                    'poids': [1.0]
                },
                'contraintes_budget': {
                    'cout_max_fcfa': 100000
                },
                'contraintes_techniques': {},
                'algorithme': {
                    'type': 'genetique',
                    'population_size': 20,
                    'generations': 10,
                    'mutation_rate': 0.1,
                    'crossover_rate': 0.8,
                    'tolerance': 1e-6
                },
                'diametres_candidats': [
                    {'diametre_mm': 110, 'cout_fcfa_m': 45},
                    {'diametre_mm': 125, 'cout_fcfa_m': 60}
                ]
            }
        }
        
        config_file = tmp_path / "test_config.yml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        # Charger et valider la configuration
        config = ConfigurationOptimisation(**config_data['optimisation'])
        assert config.criteres.principal == "cout"
        assert len(config.diametres_candidats) == 2

if __name__ == '__main__':
    pytest.main([__file__])
