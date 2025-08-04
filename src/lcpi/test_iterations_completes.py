#!/usr/bin/env python3
"""
Test complet des calculs itératifs avec affichage des itérations
Démontre Hardy-Cross et calcul rationnel d'assainissement
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_hardy_cross_iterations():
    """Test Hardy-Cross avec affichage des itérations"""
    print("🔄 TEST HARDY-CROSS - AFFICHAGE DES ITÉRATIONS")
    print("=" * 60)
    
    from lcpi.aep.calculations.hardy_cross import hardy_cross_network
    
    # Réseau avec 2 mailles
    reseau = {
        'mailles': [
            ['C1', 'C2', 'C3'],  # Maille 1
            ['C2', 'C4', 'C5']   # Maille 2
        ],
        'conduites': {
            'C1': {'resistance_K': 100.0, 'debit_Q': 0.05},
            'C2': {'resistance_K': 150.0, 'debit_Q': 0.03},
            'C3': {'resistance_K': 80.0, 'debit_Q': 0.02},
            'C4': {'resistance_K': 120.0, 'debit_Q': 0.04},
            'C5': {'resistance_K': 90.0, 'debit_Q': 0.01}
        }
    }
    
    print("📊 Réseau maillé avec 2 mailles et 5 conduites")
    print("🔧 Formule: Hazen-Williams")
    print("🎯 Tolérance: 1e-6")
    print()
    
    resultats = hardy_cross_network(
        reseau, 
        tolerance=1e-6, 
        max_iterations=50, 
        formule="hazen_williams",
        afficher_iterations=True
    )
    
    print("\n📈 RÉSULTATS FINAUX:")
    print(f"✅ Convergence: {'Oui' if resultats['convergence'] else 'Non'}")
    print(f"📊 Itérations: {resultats['iterations']}")
    print(f"🎯 Erreur finale: {resultats['erreur_finale']:.2e}")
    
    print("\n💧 Débits finaux par conduite:")
    for id_conduite, conduite in resultats['conduites_finales'].items():
        debit_ls = conduite['debit_Q'] * 1000
        print(f"  {id_conduite}: {debit_ls:+.2f} l/s")
    
    print("\n" + "=" * 60)

def test_calcul_rationnel_iterations():
    """Test calcul rationnel avec affichage des itérations"""
    print("🔄 TEST CALCUL RATIONNEL - AFFICHAGE DES ITÉRATIONS")
    print("=" * 60)
    
    from lcpi.hydrodrain.calculs.assainissement_gravitaire import (
        Troncon, Reseau, run_calcul_rationnelle
    )
    
    # Créer un réseau simple
    reseau = Reseau()
    
    # Tronçon d'exemple
    troncon = Troncon(
        id="T1",
        type_section="circulaire",
        longueur_troncon_m=100.0,
        pente_troncon=0.01,
        ks_manning_strickler=100.0,
        amont_ids=[],
        surface_propre_ha=2.5,
        coefficient_ruissellement=0.8,
        longueur_parcours_m=150.0,
        pente_parcours_m_m=0.02,
        surface_cumulee_ha=2.5,
        coefficient_moyen=0.8
    )
    
    reseau.ajouter_troncon(troncon)
    
    # Paramètres de pluie (formule Talbot)
    params_pluie = {
        "type": "talbot",
        "a": 120,  # mm/h
        "b": 20    # minutes
    }
    
    print("📊 Tronçon d'assainissement pluvial")
    print(f"🔧 Surface: {troncon.surface_cumulee_ha} ha")
    print(f"📏 Longueur: {troncon.longueur_parcours_m} m")
    print(f"📐 Pente: {troncon.pente_parcours_m_m*100:.1f}%")
    print(f"🌧️  Formule pluie: {params_pluie['type']}")
    print()
    
    resultat = run_calcul_rationnelle(troncon, params_pluie, afficher_iterations=True)
    
    print("\n📈 RÉSULTATS FINAUX:")
    if resultat["statut"] == "OK":
        print(f"✅ Statut: {resultat['statut']}")
        print(f"💧 Débit projet: {resultat['debit_projet']:.3f} m³/s")
        print(f"⏱️  Temps de concentration final: {resultat['tc_final']:.2f} min")
        print(f"🔄 Itérations: {resultat['iterations']}")
    else:
        print(f"❌ Erreur: {resultat['message']}")
    
    print("\n" + "=" * 60)

def test_comparaison_formules():
    """Test de comparaison des formules Hardy-Cross"""
    print("🔧 COMPARAISON DES FORMULES HARDY-CROSS")
    print("=" * 60)
    
    from lcpi.aep.calculations.hardy_cross import hardy_cross_network
    
    # Réseau simple
    reseau = {
        'mailles': [['C1', 'C2', 'C3']],
        'conduites': {
            'C1': {'resistance_K': 100.0, 'debit_Q': 0.05},
            'C2': {'resistance_K': 150.0, 'debit_Q': 0.03},
            'C3': {'resistance_K': 80.0, 'debit_Q': 0.02}
        }
    }
    
    formules = ["hazen_williams", "manning", "darcy_weisbach"]
    
    for formule in formules:
        print(f"\n📊 Test avec formule: {formule}")
        resultats = hardy_cross_network(
            reseau, 
            tolerance=1e-6, 
            max_iterations=20,
            formule=formule,
            afficher_iterations=False
        )
        
        print(f"  ✅ Convergence: {'Oui' if resultats['convergence'] else 'Non'}")
        print(f"  📊 Itérations: {resultats['iterations']}")
        print(f"  🎯 Erreur finale: {resultats['erreur_finale']:.2e}")
        
        # Afficher un débit final pour comparaison
        debit_c1 = resultats['conduites_finales']['C1']['debit_Q'] * 1000
        print(f"  💧 Débit C1 final: {debit_c1:+.2f} l/s")
    
    print("\n" + "=" * 60)

def test_historique_iterations():
    """Test de l'historique des itérations"""
    print("📈 HISTORIQUE DES ITÉRATIONS")
    print("=" * 60)
    
    from lcpi.aep.calculations.hardy_cross import hardy_cross_network
    
    reseau = {
        'mailles': [['C1', 'C2', 'C3']],
        'conduites': {
            'C1': {'resistance_K': 100.0, 'debit_Q': 0.05},
            'C2': {'resistance_K': 150.0, 'debit_Q': 0.03},
            'C3': {'resistance_K': 80.0, 'debit_Q': 0.02}
        }
    }
    
    resultats = hardy_cross_network(
        reseau, 
        tolerance=1e-6, 
        max_iterations=10,
        afficher_iterations=False
    )
    
    if 'historique_iterations' in resultats:
        print(f"✅ Historique disponible: {len(resultats['historique_iterations'])} itérations")
        
        print("\n📊 Évolution des corrections:")
        for hist in resultats['historique_iterations']:
            print(f"  Itération {hist['iteration']:2d}: max_correction = {hist['max_correction']:.2e}")
        
        print("\n📊 Évolution des débits C1:")
        for hist in resultats['historique_iterations']:
            debit_c1 = hist['debits']['C1'] * 1000
            print(f"  Itération {hist['iteration']:2d}: Q = {debit_c1:+.2f} l/s")
    else:
        print("❌ Historique non disponible")
    
    print("\n" + "=" * 60)

def main():
    """Fonction principale"""
    print("🧪 TESTS COMPLETS - CALCULS ITÉRATIFS")
    print("Affichage détaillé des itérations pour tous les algorithmes")
    print("=" * 80)
    
    try:
        # Tests des calculs itératifs
        test_hardy_cross_iterations()
        test_calcul_rationnel_iterations()
        test_comparaison_formules()
        test_historique_iterations()
        
        print("🎉 Tous les tests terminés avec succès!")
        print("\n📋 RÉSUMÉ:")
        print("✅ Hardy-Cross: Méthode itérative pour réseaux maillés")
        print("✅ Calcul rationnel: Méthode itérative pour assainissement")
        print("✅ Affichage des itérations: Détails de convergence")
        print("✅ Historique: Suivi de l'évolution des calculs")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 