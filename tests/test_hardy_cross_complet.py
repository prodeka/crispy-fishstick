#!/usr/bin/env python3
"""
Test complet pour la méthode Hardy-Cross
Inclut des exemples de réseaux maillés et affichage des itérations
"""

import json
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.calculations.hardy_cross import (
    hardy_cross_network,
    calculate_resistance_coefficient,
    validate_hardy_cross_data,
    export_hardy_cross_results
)

def creer_reseau_exemple_simple():
    """Crée un réseau maillé simple pour test"""
    return {
        "mailles": [
            ["C1", "C2", "C3"],  # Maille 1
            ["C2", "C4", "C5"]   # Maille 2
        ],
        "conduites": {
            "C1": {"resistance_K": 100.0, "debit_Q": 0.05},
            "C2": {"resistance_K": 150.0, "debit_Q": 0.03},
            "C3": {"resistance_K": 80.0, "debit_Q": 0.02},
            "C4": {"resistance_K": 120.0, "debit_Q": 0.04},
            "C5": {"resistance_K": 90.0, "debit_Q": 0.01}
        }
    }

def creer_reseau_exemple_complexe():
    """Crée un réseau maillé plus complexe pour test"""
    return {
        "mailles": [
            ["C1", "C2", "C3", "C4"],
            ["C4", "C5", "C6", "C7"],
            ["C2", "C5", "C8", "C9"],
            ["C3", "C6", "C10", "C11"]
        ],
        "conduites": {
            "C1": {"resistance_K": 50.0, "debit_Q": 0.10},
            "C2": {"resistance_K": 75.0, "debit_Q": 0.08},
            "C3": {"resistance_K": 60.0, "debit_Q": 0.06},
            "C4": {"resistance_K": 40.0, "debit_Q": 0.04},
            "C5": {"resistance_K": 65.0, "debit_Q": 0.07},
            "C6": {"resistance_K": 55.0, "debit_Q": 0.05},
            "C7": {"resistance_K": 45.0, "debit_Q": 0.03},
            "C8": {"resistance_K": 70.0, "debit_Q": 0.09},
            "C9": {"resistance_K": 35.0, "debit_Q": 0.02},
            "C10": {"resistance_K": 80.0, "debit_Q": 0.12},
            "C11": {"resistance_K": 30.0, "debit_Q": 0.01}
        }
    }

def test_calcul_coefficient_resistance():
    """Test du calcul du coefficient de résistance"""
    print("🔧 Test: Calcul du coefficient de résistance")
    print("-" * 50)
    
    # Test avec différentes formules
    longueur = 100.0  # m
    diametre = 0.2    # m
    coefficient = 100.0  # C pour Hazen-Williams
    
    formules = ["hazen_williams", "manning", "darcy_weisbach"]
    
    for formule in formules:
        try:
            K = calculate_resistance_coefficient(longueur, diametre, coefficient, formule)
            print(f"✅ {formule}: K = {K:.2f}")
        except Exception as e:
            print(f"❌ {formule}: {e}")
    
    print()

def test_reseau_simple():
    """Test avec un réseau simple"""
    print("🔄 Test: Réseau simple (2 mailles)")
    print("-" * 50)
    
    reseau = creer_reseau_exemple_simple()
    
    # Valider les données
    try:
        validate_hardy_cross_data(reseau)
        print("✅ Validation des données: OK")
    except Exception as e:
        print(f"❌ Validation des données: {e}")
        return
    
    # Afficher les données initiales
    print("\n📊 Données initiales:")
    for id_conduite, conduite in reseau['conduites'].items():
        debit_ls = conduite['debit_Q'] * 1000
        print(f"  {id_conduite}: K={conduite['resistance_K']:.1f}, Q={debit_ls:.2f} l/s")
    
    # Calculer avec affichage des itérations
    print("\n🔄 Calcul Hardy-Cross avec affichage des itérations:")
    resultats = hardy_cross_network(
        reseau, 
        tolerance=1e-6, 
        max_iterations=50, 
        formule="hazen_williams",
        afficher_iterations=True
    )
    
    # Afficher les résultats finaux
    print("\n📊 Résultats finaux:")
    print(f"  Convergence: {'✅' if resultats['convergence'] else '❌'}")
    print(f"  Itérations: {resultats['iterations']}")
    print(f"  Erreur finale: {resultats['erreur_finale']:.2e}")
    
    print("\n💧 Débits finaux par conduite:")
    for id_conduite, conduite in resultats['conduites_finales'].items():
        debit_ls = conduite['debit_Q'] * 1000
        print(f"  {id_conduite}: {debit_ls:+.2f} l/s")
    
    print()

def test_reseau_complexe():
    """Test avec un réseau complexe"""
    print("🔄 Test: Réseau complexe (4 mailles)")
    print("-" * 50)
    
    reseau = creer_reseau_exemple_complexe()
    
    # Calculer sans affichage détaillé
    resultats = hardy_cross_network(
        reseau, 
        tolerance=1e-6, 
        max_iterations=100, 
        formule="hazen_williams",
        afficher_iterations=False
    )
    
    # Afficher les résultats
    print(f"✅ Convergence: {'Oui' if resultats['convergence'] else 'Non'}")
    print(f"📊 Itérations: {resultats['iterations']}")
    print(f"🎯 Erreur finale: {resultats['erreur_finale']:.2e}")
    
    print("\n💧 Débits finaux (top 5):")
    debits_tries = sorted(
        resultats['conduites_finales'].items(), 
        key=lambda x: abs(x[1]['debit_Q']), 
        reverse=True
    )
    
    for i, (id_conduite, conduite) in enumerate(debits_tries[:5]):
        debit_ls = conduite['debit_Q'] * 1000
        print(f"  {id_conduite}: {debit_ls:+.2f} l/s")
    
    print()

def test_differentes_formules():
    """Test avec différentes formules de perte de charge"""
    print("🔧 Test: Comparaison des formules")
    print("-" * 50)
    
    reseau = creer_reseau_exemple_simple()
    formules = ["hazen_williams", "manning", "darcy_weisbach"]
    
    for formule in formules:
        print(f"\n📊 Formule: {formule}")
        resultats = hardy_cross_network(
            reseau, 
            tolerance=1e-6, 
            max_iterations=50, 
            formule=formule,
            afficher_iterations=False
        )
        
        print(f"  Convergence: {'✅' if resultats['convergence'] else '❌'}")
        print(f"  Itérations: {resultats['iterations']}")
        print(f"  Erreur finale: {resultats['erreur_finale']:.2e}")
    
    print()

def test_export_resultats():
    """Test d'export des résultats"""
    print("💾 Test: Export des résultats")
    print("-" * 50)
    
    reseau = creer_reseau_exemple_simple()
    resultats = hardy_cross_network(reseau, tolerance=1e-6)
    
    # Export JSON
    try:
        export_hardy_cross_results(resultats, "resultats_hardy_cross.json", "json")
        print("✅ Export JSON: OK")
    except Exception as e:
        print(f"❌ Export JSON: {e}")
    
    # Export CSV
    try:
        export_hardy_cross_results(resultats, "resultats_hardy_cross.csv", "csv")
        print("✅ Export CSV: OK")
    except Exception as e:
        print(f"❌ Export CSV: {e}")
    
    print()

def test_historique_iterations():
    """Test de l'historique des itérations"""
    print("📈 Test: Historique des itérations")
    print("-" * 50)
    
    reseau = creer_reseau_exemple_simple()
    resultats = hardy_cross_network(
        reseau, 
        tolerance=1e-6, 
        max_iterations=20,
        afficher_iterations=False
    )
    
    if 'historique_iterations' in resultats:
        print(f"✅ Historique disponible: {len(resultats['historique_iterations'])} itérations")
        
        # Afficher les 3 premières itérations
        print("\n📊 Détails des 3 premières itérations:")
        for i, hist in enumerate(resultats['historique_iterations'][:3]):
            print(f"  Itération {hist['iteration']}: max_correction = {hist['max_correction']:.2e}")
            for j, correction in enumerate(hist['corrections_par_maille']):
                print(f"    Maille {j+1}: ΔQ = {correction:+.2e} m³/s")
    else:
        print("❌ Historique non disponible")
    
    print()

def main():
    """Fonction principale de test"""
    print("🧪 TESTS COMPLETS - MÉTHODE HARDY-CROSS")
    print("=" * 60)
    
    try:
        # Tests individuels
        test_calcul_coefficient_resistance()
        test_reseau_simple()
        test_reseau_complexe()
        test_differentes_formules()
        test_export_resultats()
        test_historique_iterations()
        
        print("🎉 Tous les tests terminés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 