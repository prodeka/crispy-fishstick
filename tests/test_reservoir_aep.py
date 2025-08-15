#!/usr/bin/env python3
"""
Tests unitaires pour le module réservoir d'eau potable.
10 tests allant du plus simple au plus complexe.
"""

import pytest
import sys
import os
import json
import tempfile
from unittest.mock import patch, MagicMock

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lcpi.hydrodrain.calculs.reservoir_aep import (
    dimensionner_reservoir_equilibrage, dimensionner_reservoir_incendie,
    calculer_volume_reservoir_optimal, verifier_pression_reservoir,
    calculer_renouvellement_eau_reservoir, dimensionner_reservoir_complet
)

class TestReservoirAEP:
    """Tests pour le module réservoir d'eau potable."""
    
    def test_1_dimensionnement_equilibrage_simple(self):
        """Test 1: Dimensionnement d'équilibrage simple (niveau: facile)"""
        resultat = dimensionner_reservoir_equilibrage(
            demande_journaliere_m3=100.0,
            coefficient_pointe_jour=1.3,
            coefficient_pointe_horaire=1.7,
            nombre_jours_stockage=1
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["debit_moyen_m3_h"] == 4.17  # 100/24
        assert resultat["debit_pointe_jour_m3_h"] == 5.42  # 4.17 * 1.3
        assert resultat["debit_pointe_horaire_m3_h"] == 7.08  # 4.17 * 1.7
        assert resultat["volume_equilibrage_m3"] == 15.0  # 100 * 0.15
        assert resultat["volume_securite_m3"] == 100.0  # 100 * 1
        assert resultat["volume_total_m3"] == 115.0  # 15 + 100
    
    def test_2_reservoir_incendie_urbain(self):
        """Test 2: Réservoir d'incendie zone urbaine (niveau: facile)"""
        resultat = dimensionner_reservoir_incendie(
            population=1000,
            surface_zone_ha=50.0,
            type_zone="urbain"
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["type_zone"] == "urbain"
        assert resultat["debit_incendie_l_min"] == 120
        assert resultat["duree_incendie_min"] == 60
        assert resultat["volume_incendie_m3"] == 7.2  # (120 * 60) / 1000
        assert resultat["volume_domestique_m3"] > 0
        assert resultat["volume_total_m3"] > 7.2
    
    def test_3_reservoir_incendie_rural(self):
        """Test 3: Réservoir d'incendie zone rurale (niveau: facile)"""
        resultat = dimensionner_reservoir_incendie(
            population=500,
            surface_zone_ha=25.0,
            type_zone="rural"
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["type_zone"] == "rural"
        assert resultat["debit_incendie_l_min"] == 60
        assert resultat["duree_incendie_min"] == 45
        assert resultat["volume_incendie_m3"] == 2.7  # (60 * 45) / 1000
    
    def test_4_reservoir_incendie_industriel(self):
        """Test 4: Réservoir d'incendie zone industrielle (niveau: facile)"""
        resultat = dimensionner_reservoir_incendie(
            population=2000,
            surface_zone_ha=100.0,
            type_zone="industriel"
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["type_zone"] == "industriel"
        assert resultat["debit_incendie_l_min"] == 200
        assert resultat["duree_incendie_min"] == 90
        assert resultat["volume_incendie_m3"] == 18.0  # (200 * 90) / 1000
    
    def test_5_erreur_type_zone_inconnu(self):
        """Test 5: Gestion d'erreur pour type de zone inconnu (niveau: facile)"""
        resultat = dimensionner_reservoir_incendie(
            population=1000,
            surface_zone_ha=50.0,
            type_zone="inconnu"
        )
        
        assert resultat["statut"] == "Erreur"
        assert "Type de zone 'inconnu' non reconnu" in resultat["message"]
    
    def test_6_verification_pression_simple(self):
        """Test 6: Vérification de pression simple (niveau: moyen)"""
        resultat = verifier_pression_reservoir(
            cote_reservoir_m=150.0,
            cote_terrain_m=100.0,
            pertes_charge_m=5.0,
            pression_minimale_m=15.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["pression_disponible_m"] == 45.0  # 150 - 100 - 5 = 45
        assert resultat["pression_minimale_m"] == 15.0
        assert resultat["marge_securite_m"] == 30.0  # 45 - 15 = 30
        assert resultat["conforme"] == True
        assert resultat["niveau_securite"] == "Excellent"  # 30 > 10
    
    def test_7_verification_pression_insuffisante(self):
        """Test 7: Vérification de pression insuffisante (niveau: moyen)"""
        resultat = verifier_pression_reservoir(
            cote_reservoir_m=110.0,
            cote_terrain_m=100.0,
            pertes_charge_m=5.0,
            pression_minimale_m=15.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["pression_disponible_m"] == 5.0  # 110 - 100 - 5
        assert resultat["conforme"] == False
        assert resultat["niveau_securite"] == "Insuffisant"
    
    def test_8_calcul_renouvellement_eau(self):
        """Test 8: Calcul du renouvellement de l'eau (niveau: moyen)"""
        resultat = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=100.0,
            debit_circulation_m3_h=10.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["temps_renouvellement_h"] == 10.0  # 100 / 10
        assert resultat["temps_renouvellement_jours"] == 0.4  # 10 / 24 = 0.416... arrondi à 0.4
        assert resultat["qualite_renouvellement"] == "Excellent"
        assert "satisfaisant" in resultat["recommandation"]
    
    def test_9_calcul_renouvellement_problematique(self):
        """Test 9: Calcul du renouvellement problématique (niveau: moyen)"""
        resultat = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=1000.0,
            debit_circulation_m3_h=5.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["temps_renouvellement_h"] == 200.0  # 1000 / 5
        assert resultat["qualite_renouvellement"] == "Problématique"
        assert "Augmenter la circulation" in resultat["recommandation"]
    
    def test_10_erreur_debit_circulation_negatif(self):
        """Test 10: Gestion d'erreur pour débit de circulation négatif (niveau: facile)"""
        resultat = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=100.0,
            debit_circulation_m3_h=-5.0
        )
        
        assert resultat["statut"] == "Erreur"
        assert "Le débit de circulation doit être positif" in resultat["message"]
    
    def test_11_calcul_volume_optimal_simple(self):
        """Test 11: Calcul du volume optimal simple (niveau: moyen)"""
        # Demande constante
        demandes_horaires = [4.17] * 24  # Demande constante
        production_horaire = 4.17  # Production constante
        
        resultat = calculer_volume_reservoir_optimal(
            demandes_horaires_m3=demandes_horaires,
            production_horaire_m3=production_horaire
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["volume_stockage_m3"] == 0.0  # Pas de stockage nécessaire
        assert resultat["surplus_max_m3"] == 0.0
        assert resultat["deficit_max_m3"] == 0.0
    
    def test_12_calcul_volume_optimal_variable(self):
        """Test 12: Calcul du volume optimal avec demande variable (niveau: moyen)"""
        # Demande variable (pointe le matin et le soir)
        demandes_horaires = [2.0] * 6 + [6.0] * 6 + [2.0] * 6 + [6.0] * 6
        production_horaire = 4.0  # Production constante
        
        resultat = calculer_volume_reservoir_optimal(
            demandes_horaires_m3=demandes_horaires,
            production_horaire_m3=production_horaire
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["volume_stockage_m3"] > 0  # Stockage nécessaire
        assert resultat["surplus_max_m3"] > 0
        # Le déficit peut être 0 si la production couvre toujours la demande
        assert resultat["deficit_max_m3"] >= 0
        assert len(resultat["courbes_cumulees"]["production"]) == 24
        assert len(resultat["courbes_cumulees"]["demande"]) == 24
        assert len(resultat["courbes_cumulees"]["differences"]) == 24
    
    def test_13_erreur_demandes_horaires_incorrectes(self):
        """Test 13: Gestion d'erreur pour demandes horaires incorrectes (niveau: facile)"""
        demandes_horaires = [4.17] * 12  # Seulement 12 heures au lieu de 24
        
        resultat = calculer_volume_reservoir_optimal(
            demandes_horaires_m3=demandes_horaires,
            production_horaire_m3=4.17
        )
        
        assert resultat["statut"] == "Erreur"
        assert "La liste doit contenir 24 valeurs" in resultat["message"]
    
    def test_14_reservoir_complet_simple(self):
        """Test 14: Dimensionnement d'un réservoir complet simple (niveau: complexe)"""
        resultat = dimensionner_reservoir_complet(
            population=1000,
            dotation_l_jour_hab=150.0,
            coefficient_pointe_jour=1.3,
            coefficient_pointe_horaire=1.7,
            nombre_jours_securite=1,
            type_zone_incendie="urbain"
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["population"] == 1000
        assert resultat["demande_journaliere_m3"] == 150.0  # (1000 * 150) / 1000
        assert resultat["volume_equilibrage_m3"] > 0
        assert resultat["volume_incendie_m3"] > 0
        assert resultat["volume_total_m3"] > 0
        assert resultat["hauteur_eau_m"] == 4.0
        assert resultat["surface_m2"] > 0
        assert resultat["diametre_m"] > 0
        assert "details_equilibrage" in resultat
        assert "details_incendie" in resultat
    
    def test_15_reservoir_complet_grande_population(self):
        """Test 15: Réservoir complet pour grande population (niveau: complexe)"""
        resultat = dimensionner_reservoir_complet(
            population=10000,
            dotation_l_jour_hab=200.0,
            coefficient_pointe_jour=1.5,
            coefficient_pointe_horaire=2.0,
            nombre_jours_securite=2,
            type_zone_incendie="industriel"
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["demande_journaliere_m3"] == 2000.0  # (10000 * 200) / 1000
        assert resultat["volume_total_m3"] > 2000  # Plus que la demande journalière
        assert resultat["surface_m2"] > 500  # Surface importante
        assert resultat["diametre_m"] > 25  # Diamètre important
    
    def test_16_verification_pression_niveaux_securite(self):
        """Test 16: Vérification des différents niveaux de sécurité (niveau: moyen)"""
        # Test niveau "Limite" (marge = 0, conforme = True)
        resultat_limite = verifier_pression_reservoir(
            cote_reservoir_m=120.0,
            cote_terrain_m=100.0,
            pertes_charge_m=5.0,
            pression_minimale_m=15.0
        )
        # Pression disponible = 120 - 100 - 5 = 15, marge = 15 - 15 = 0
        # Niveau = "Limite" car marge <= 5 et conforme = True
        assert resultat_limite["niveau_securite"] == "Limite"
        
        # Test niveau "Bon" (marge > 5 et <= 10)
        resultat_bon = verifier_pression_reservoir(
            cote_reservoir_m=126.0,
            cote_terrain_m=100.0,
            pertes_charge_m=5.0,
            pression_minimale_m=15.0
        )
        # Pression disponible = 126 - 100 - 5 = 21, marge = 21 - 15 = 6
        # Niveau = "Bon" car marge > 5 et <= 10
        assert resultat_bon["niveau_securite"] == "Bon"
        
        # Test niveau "Insuffisant"
        resultat_insuffisant = verifier_pression_reservoir(
            cote_reservoir_m=110.0,
            cote_terrain_m=100.0,
            pertes_charge_m=5.0,
            pression_minimale_m=15.0
        )
        assert resultat_insuffisant["niveau_securite"] == "Insuffisant"
    
    def test_17_calcul_renouvellement_differentes_qualites(self):
        """Test 17: Calcul du renouvellement avec différentes qualités (niveau: moyen)"""
        # Test qualité "Bon"
        resultat_bon = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=100.0,
            debit_circulation_m3_h=3.0
        )
        assert resultat_bon["qualite_renouvellement"] == "Bon"
        
        # Test qualité "Acceptable"
        resultat_acceptable = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=100.0,
            debit_circulation_m3_h=2.0
        )
        assert resultat_acceptable["qualite_renouvellement"] == "Acceptable"
        
        # Test qualité "Problématique"
        resultat_problematique = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=100.0,
            debit_circulation_m3_h=1.0
        )
        assert resultat_problematique["qualite_renouvellement"] == "Problématique"
    
    def test_18_calcul_volume_optimal_pointe_extreme(self):
        """Test 18: Calcul du volume optimal avec pointe extrême (niveau: complexe)"""
        # Demande avec pointe extrême
        demandes_horaires = [2.0] * 23 + [20.0]  # Pointe extrême à la dernière heure
        production_horaire = 4.0  # Production constante
        
        resultat = calculer_volume_reservoir_optimal(
            demandes_horaires_m3=demandes_horaires,
            production_horaire_m3=production_horaire
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["volume_stockage_m3"] > 0
        
        # Vérifier que l'heure de pointe correspond à la logique de la fonction
        # Avec [2.0] * 23 + [20.0] et production = 4.0
        # Heure 1-23: demande = 2, production = 4, différence = +2
        # Heure 24: demande = 20, production = 96, différence = +30 (pas le maximum)
        # Le maximum est à l'heure 23 (index 22), donc heure_pointe = 22 + 1 = 23
        assert resultat["heure_pointe"] == 23  # Heure 23 (index 22 + 1)
        assert resultat["heure_creux"] == 1  # Heure 1 (index 0 + 1)
    
    def test_19_reservoir_complet_parametres_extremes(self):
        """Test 19: Réservoir complet avec paramètres extrêmes (niveau: complexe)"""
        resultat = dimensionner_reservoir_complet(
            population=50000,
            dotation_l_jour_hab=300.0,
            coefficient_pointe_jour=2.0,
            coefficient_pointe_horaire=3.0,
            nombre_jours_securite=3,
            type_zone_incendie="industriel"
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["demande_journaliere_m3"] == 15000.0  # (50000 * 300) / 1000
        assert resultat["volume_total_m3"] > 15000  # Stockage important
        assert resultat["surface_m2"] > 3000  # Très grande surface
        assert resultat["diametre_m"] > 60  # Très grand diamètre
    
    def test_20_integration_complete_reservoir(self):
        """Test 20: Test d'intégration complète du réservoir (niveau: très complexe)"""
        # 1. Dimensionner un réservoir complet
        resultat_complet = dimensionner_reservoir_complet(
            population=5000,
            dotation_l_jour_hab=150.0,
            coefficient_pointe_jour=1.3,
            coefficient_pointe_horaire=1.7,
            nombre_jours_securite=1,
            type_zone_incendie="urbain"
        )
        
        assert resultat_complet["statut"] == "OK"
        volume_total = resultat_complet["volume_total_m3"]
        
        # 2. Vérifier la pression disponible
        resultat_pression = verifier_pression_reservoir(
            cote_reservoir_m=200.0,
            cote_terrain_m=150.0,
            pertes_charge_m=10.0,
            pression_minimale_m=15.0
        )
        
        assert resultat_pression["statut"] == "OK"
        assert resultat_pression["conforme"] == True
        
        # 3. Calculer le renouvellement
        resultat_renouvellement = calculer_renouvellement_eau_reservoir(
            volume_reservoir_m3=volume_total,
            debit_circulation_m3_h=50.0
        )
        
        assert resultat_renouvellement["statut"] == "OK"
        assert resultat_renouvellement["temps_renouvellement_h"] > 0
        
        # 4. Vérifier la cohérence des résultats
        assert resultat_complet["volume_total_m3"] > resultat_complet["demande_journaliere_m3"]
        assert resultat_pression["pression_disponible_m"] > resultat_pression["pression_minimale_m"]
        assert resultat_renouvellement["temps_renouvellement_h"] < 72  # Moins de 3 jours 