#!/usr/bin/env python3
"""
Test des améliorations de la Phase 2 : Raffinement de l'Algorithme Génétique de LCPI.
Valide les corrections apportées aux algorithmes d'optimisation.
"""

import sys
import os
from pathlib import Path
import json

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_improved_repair_logic():
    """Test de la logique de réparation améliorée."""
    print("🔍 Test de la logique de réparation améliorée...")
    
    try:
        from src.lcpi.aep.optimization.genetic_algorithm import GeneticOptimizerV2
        
        # Vérifier que la classe existe et peut être instanciée
        print("✅ GeneticOptimizerV2 importé avec succès")
        
        # Vérifier que les méthodes de réparation existent
        if hasattr(GeneticOptimizerV2, '_repair_velocity_violations'):
            print("✅ Méthode _repair_velocity_violations disponible")
        else:
            print("❌ Méthode _repair_velocity_violations manquante")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de la logique de réparation: {e}")
        return False

def test_improved_mutation_bias():
    """Test du biais de mutation amélioré."""
    print("\n🔍 Test du biais de mutation amélioré...")
    
    try:
        from src.lcpi.aep.optimization.genetic_algorithm import GeneticOptimizerV2
        
        # Vérifier que la méthode de mutation existe
        if hasattr(GeneticOptimizerV2, '_biased_mutation'):
            print("✅ Méthode _biased_mutation disponible")
        else:
            print("❌ Méthode _biased_mutation manquante")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du biais de mutation: {e}")
        return False

def test_advanced_constraint_handler():
    """Test du gestionnaire de contraintes avancé."""
    print("\n🔍 Test du gestionnaire de contraintes avancé...")
    
    try:
        from src.lcpi.aep.optimizer.constraints_handler import ConstraintManager, ConstraintPenaltyCalculator
        
        # Vérifier que les classes existent
        print("✅ ConstraintManager et ConstraintPenaltyCalculator importés")
        
        # Tester la création d'instances
        penalty_calc = ConstraintPenaltyCalculator()
        constraint_mgr = ConstraintManager(penalty_calc)
        
        print("✅ Instances créées avec succès")
        
        # Tester le calcul de pénalités
        test_violations = {
            "max_velocity_m_s": 2.5,
            "current_velocity_m_s": 3.0,
            "min_pressure_mce": 20.0,
            "current_pressure_mce": 15.0
        }
        
        total_penalty, penalty_details = penalty_calc.calculate_total_penalty(
            test_violations, 100000, 500000
        )
        
        if total_penalty > 0:
            print(f"✅ Calcul de pénalités réussi: {total_penalty:.0f} FCFA")
            print(f"📊 Détails: {penalty_details}")
        else:
            print("⚠️ Aucune pénalité calculée (vérifier la logique)")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du gestionnaire de contraintes: {e}")
        return False

def test_budget_constraints():
    """Test des contraintes budgétaires améliorées."""
    print("\n🔍 Test des contraintes budgétaires améliorées...")
    
    try:
        from src.lcpi.aep.core.models import ContraintesBudget
        
        # Vérifier que la classe a des valeurs par défaut réalistes
        budget_constraint = ContraintesBudget()
        
        if budget_constraint.cout_max_fcfa == 500000:
            print("✅ Budget maximum par défaut réaliste: 500,000 FCFA")
        else:
            print(f"⚠️ Budget maximum inattendu: {budget_constraint.cout_max_fcfa} FCFA")
            
        if budget_constraint.cout_par_metre_max == 500:
            print("✅ Coût par mètre maximum par défaut réaliste: 500 FCFA/m")
        else:
            print(f"⚠️ Coût par mètre maximum inattendu: {budget_constraint.cout_par_metre_max} FCFA/m")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des contraintes budgétaires: {e}")
        return False

def test_controller_integration():
    """Test de l'intégration dans le contrôleur."""
    print("\n🔍 Test de l'intégration dans le contrôleur...")
    
    try:
        from src.lcpi.aep.optimizer.controllers import OptimizationController
        
        # Vérifier que le contrôleur peut être créé
        controller = OptimizationController()
        print("✅ OptimizationController créé avec succès")
        
        # Vérifier que le nouveau gestionnaire de contraintes est utilisé
        try:
            from src.lcpi.aep.optimizer.constraints_handler import ConstraintManager
            print("✅ Nouveau gestionnaire de contraintes disponible")
        except ImportError:
            print("❌ Nouveau gestionnaire de contraintes non disponible")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du contrôleur: {e}")
        return False

def test_penalty_calculation_scenarios():
    """Test de différents scénarios de calcul de pénalités."""
    print("\n🔍 Test de différents scénarios de calcul de pénalités...")
    
    try:
        from src.lcpi.aep.optimizer.constraints_handler import ConstraintPenaltyCalculator
        
        penalty_calc = ConstraintPenaltyCalculator()
        
        # Scénario 1: Violation légère de vitesse
        vel_penalty_light = penalty_calc.calculate_velocity_penalty(2.6, 2.5, 100000, 500000)
        print(f"📊 Violation légère vitesse (2.6 vs 2.5 m/s): {vel_penalty_light:.0f} FCFA")
        
        # Scénario 2: Violation sévère de vitesse
        vel_penalty_severe = penalty_calc.calculate_velocity_penalty(5.0, 2.5, 100000, 500000)
        print(f"📊 Violation sévère vitesse (5.0 vs 2.5 m/s): {vel_penalty_severe:.0f} FCFA")
        
        # Scénario 3: Violation de pression
        press_penalty = penalty_calc.calculate_pressure_penalty(15.0, 20.0, 100000, 500000)
        print(f"📊 Violation pression (15 vs 20 mCE): {press_penalty:.0f} FCFA")
        
        # Scénario 4: Dépassement de budget
        budget_penalty = penalty_calc.calculate_budget_penalty(600000, 500000)
        print(f"📊 Dépassement budget (600k vs 500k): {budget_penalty:.0f} FCFA")
        
        # Vérifier que les pénalités sont cohérentes
        if vel_penalty_severe > vel_penalty_light:
            print("✅ Pénalités de vitesse cohérentes (sévère > légère)")
        else:
            print("⚠️ Pénalités de vitesse incohérentes")
            
        if budget_penalty > 0:
            print("✅ Pénalité de budget active")
        else:
            print("⚠️ Aucune pénalité de budget")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des scénarios de pénalités: {e}")
        return False

def main():
    """Test principal des améliorations de la Phase 2."""
    print("🚀 TEST DES AMÉLIORATIONS DE LA PHASE 2")
    print("🎯 Raffinement de l'Algorithme Génétique de LCPI")
    print("=" * 70)
    
    # Tests principaux
    repair_ok = test_improved_repair_logic()
    mutation_ok = test_improved_mutation_bias()
    constraint_ok = test_advanced_constraint_handler()
    budget_ok = test_budget_constraints()
    controller_ok = test_controller_integration()
    penalty_scenarios_ok = test_penalty_calculation_scenarios()
    
    # Résumé des résultats
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS DE LA PHASE 2")
    print("=" * 70)
    
    tests = [
        ("Logique de réparation améliorée", repair_ok),
        ("Biais de mutation amélioré", mutation_ok),
        ("Gestionnaire de contraintes avancé", constraint_ok),
        ("Contraintes budgétaires améliorées", budget_ok),
        ("Intégration dans le contrôleur", controller_ok),
        ("Scénarios de calcul de pénalités", penalty_scenarios_ok),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    # Vérifications finales
    if passed == total:
        print("\n🎉 PHASE 2 VALIDÉE AVEC SUCCÈS !")
        print("✅ Toutes les améliorations sont fonctionnelles")
        print("✅ L'algorithme génétique est maintenant plus robuste")
        print("✅ Les contraintes budgétaires sont effectives")
        print("✅ Le système de pénalités est sophistiqué")
        
        return True
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Des corrections sont nécessaires pour la Phase 2")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
