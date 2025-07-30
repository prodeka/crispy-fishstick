#!/usr/bin/env python3
"""
Script de test pour le module collecteur d'assainissement.
"""

import sys
import os
import json

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_reseau_eaux_usees():
    """Test du dimensionnement d'un réseau d'eaux usées."""
    print("=== Test Réseau d'Eaux Usées ===")
    
    try:
        from lcpi.hydrodrain.calculs.assainissement_gravitaire import (
            Troncon, Reseau, dimensionner_reseau_eaux_usees
        )
        
        # Créer un réseau simple
        reseau = Reseau()
        
        # Tronçon 1 (amont)
        troncon1 = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[],
            population=50,
            dotation_l_jour_hab=150.0,
            coefficient_pointe=2.5
        )
        
        # Tronçon 2 (aval)
        troncon2 = Troncon(
            id="T2",
            type_section="circulaire",
            longueur_troncon_m=150.0,
            pente_troncon=0.004,
            ks_manning_strickler=70.0,
            amont_ids=["T1"],
            population=75,
            dotation_l_jour_hab=150.0,
            coefficient_pointe=2.5
        )
        
        reseau.ajouter_troncon(troncon1)
        reseau.ajouter_troncon(troncon2)
        
        # Dimensionner le réseau
        resultats = dimensionner_reseau_eaux_usees(reseau)
        
        print("Résultats du dimensionnement:")
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
        
        return resultats["statut"] == "OK"
        
    except Exception as e:
        print(f"Erreur lors du test eaux usées: {e}")
        return False

def test_reseau_eaux_pluviales():
    """Test du dimensionnement d'un réseau d'eaux pluviales."""
    print("\n=== Test Réseau d'Eaux Pluviales ===")
    
    try:
        from lcpi.hydrodrain.calculs.assainissement_gravitaire import (
            Troncon, Reseau, dimensionner_reseau_eaux_pluviales
        )
        
        # Créer un réseau simple
        reseau = Reseau()
        
        # Tronçon 1 (amont)
        troncon1 = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[],
            surface_propre_ha=2.5,
            coefficient_ruissellement=0.8,
            longueur_parcours_m=80.0,
            pente_parcours_m_m=0.02
        )
        
        # Tronçon 2 (aval)
        troncon2 = Troncon(
            id="T2",
            type_section="circulaire",
            longueur_troncon_m=150.0,
            pente_troncon=0.004,
            ks_manning_strickler=70.0,
            amont_ids=["T1"],
            surface_propre_ha=3.0,
            coefficient_ruissellement=0.7,
            longueur_parcours_m=120.0,
            pente_parcours_m_m=0.015
        )
        
        reseau.ajouter_troncon(troncon1)
        reseau.ajouter_troncon(troncon2)
        
        # Paramètres de pluie (formule Talbot)
        params_pluie = {
            "type": "talbot",
            "a": 120,
            "b": 20
        }
        
        # Dimensionner le réseau
        resultats = dimensionner_reseau_eaux_pluviales(reseau, params_pluie)
        
        print("Résultats du dimensionnement:")
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
        
        return resultats["statut"] == "OK"
        
    except Exception as e:
        print(f"Erreur lors du test eaux pluviales: {e}")
        return False

def test_reservoir():
    """Test du dimensionnement de réservoirs."""
    print("\n=== Test Réservoirs d'Eau Potable ===")
    
    try:
        from lcpi.hydrodrain.calculs.reservoir_aep import (
            dimensionner_reservoir_equilibrage,
            dimensionner_reservoir_incendie,
            dimensionner_reservoir_complet
        )
        
        # Test réservoir d'équilibrage
        resultat_equilibrage = dimensionner_reservoir_equilibrage(
            demande_journaliere_m3=100.0,
            coefficient_pointe_jour=1.3,
            coefficient_pointe_horaire=1.7,
            nombre_jours_stockage=1
        )
        
        print("Réservoir d'équilibrage:")
        print(json.dumps(resultat_equilibrage, indent=2, ensure_ascii=False))
        
        # Test réservoir d'incendie
        resultat_incendie = dimensionner_reservoir_incendie(
            population=1000,
            surface_zone_ha=50.0,
            type_zone="urbain"
        )
        
        print("\nRéservoir d'incendie:")
        print(json.dumps(resultat_incendie, indent=2, ensure_ascii=False))
        
        # Test réservoir complet
        resultat_complet = dimensionner_reservoir_complet(
            population=1000,
            dotation_l_jour_hab=150.0,
            coefficient_pointe_jour=1.3,
            coefficient_pointe_horaire=1.7,
            nombre_jours_securite=1,
            type_zone_incendie="urbain"
        )
        
        print("\nRéservoir complet:")
        print(json.dumps(resultat_complet, indent=2, ensure_ascii=False))
        
        return (resultat_equilibrage["statut"] == "OK" and 
                resultat_incendie["statut"] == "OK" and 
                resultat_complet["statut"] == "OK")
        
    except Exception as e:
        print(f"Erreur lors du test réservoirs: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("Démarrage des tests du module collecteur d'assainissement...")
    
    # Tests
    test1_ok = test_reseau_eaux_usees()
    test2_ok = test_reseau_eaux_pluviales()
    test3_ok = test_reservoir()
    
    # Résumé
    print("\n=== RÉSUMÉ DES TESTS ===")
    print(f"Réseau eaux usées: {'✓ OK' if test1_ok else '✗ ÉCHEC'}")
    print(f"Réseau eaux pluviales: {'✓ OK' if test2_ok else '✗ ÉCHEC'}")
    print(f"Réservoirs: {'✓ OK' if test3_ok else '✗ ÉCHEC'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n🎉 Tous les tests sont passés avec succès!")
        return 0
    else:
        print("\n❌ Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 