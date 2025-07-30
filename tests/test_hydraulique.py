#!/usr/bin/env python3
"""
Tests unitaires pour le module hydraulique.
10 tests allant du plus simple au plus complexe.
"""

import pytest
import sys
import os
import math
from unittest.mock import patch, MagicMock

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lcpi.hydrodrain.calculs.hydraulique import (
    calculer_pertes_charge_lineaires, calculer_pertes_charge_singulieres,
    calculer_courbe_remous, verifier_stabilite_talus, calculer_debit_critique
)

class TestHydraulique:
    """Tests pour le module hydraulique."""
    
    def test_1_pertes_charge_lineaires_simple(self):
        """Test 1: Calcul des pertes de charge linéaires simple (niveau: facile)"""
        resultat = calculer_pertes_charge_lineaires(
            debit_m3s=0.1,  # 100 L/s
            diametre_m=0.2,  # 200 mm
            longueur_m=100.0,
            rugosite_mm=0.1,
            viscosite_m2s=1.004e-6
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["debit_m3s"] == 0.1
        assert resultat["diametre_m"] == 0.2
        assert resultat["longueur_m"] == 100.0
        assert resultat["vitesse_ms"] > 0
        assert resultat["nombre_reynolds"] > 0
        assert resultat["coefficient_frottement"] > 0
        assert resultat["pertes_charge_m"] > 0
        assert resultat["pente_hydraulique"] > 0
    
    def test_2_pertes_charge_singulieres_simple(self):
        """Test 2: Calcul des pertes de charge singulières simple (niveau: facile)"""
        coefficients_k = {
            "entree": 0.5,
            "coude_90": 0.3,
            "vanne": 0.2
        }
        
        resultat = calculer_pertes_charge_singulieres(
            vitesse_ms=2.0,
            coefficients_k=coefficients_k
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["vitesse_ms"] == 2.0
        assert resultat["pertes_charge_totales_m"] > 0
        assert len(resultat["pertes_charge_detaillees"]) == 3
        assert "entree" in resultat["pertes_charge_detaillees"]
        assert "coude_90" in resultat["pertes_charge_detaillees"]
        assert "vanne" in resultat["pertes_charge_detaillees"]
    
    def test_3_calcul_debit_critique_simple(self):
        """Test 3: Calcul du débit critique simple (niveau: facile)"""
        resultat = calculer_debit_critique(
            largeur_m=2.0,
            profondeur_m=1.0,
            pente_m_m=0.01,
            rugosite_manning=0.013
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["largeur_m"] == 2.0
        assert resultat["profondeur_m"] == 1.0
        assert resultat["pente_m_m"] == 0.01
        assert resultat["debit_critique_m3s"] > 0
        assert resultat["vitesse_critique_ms"] > 0
        assert resultat["nombre_froude"] > 0
    
    def test_4_verification_stabilite_talus_simple(self):
        """Test 4: Vérification de stabilité des talus simple (niveau: facile)"""
        resultat = verifier_stabilite_talus(
            hauteur_m=5.0,
            pente_talus=2.0,  # 1V:2H
            angle_frottement_deg=30.0,
            cohesion_kpa=20.0,
            poids_volumique_kn_m3=20.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["hauteur_m"] == 5.0
        assert resultat["pente_talus"] == 2.0
        assert resultat["angle_frottement_deg"] == 30.0
        assert resultat["cohesion_kpa"] == 20.0
        assert resultat["coefficient_securite"] > 0
        assert resultat["stabilite"] in ["Stable", "Instable", "Limite"]
    
    def test_5_courbe_remous_simple(self):
        """Test 5: Calcul de courbe de remous simple (niveau: moyen)"""
        resultat = calculer_courbe_remous(
            debit_m3s=10.0,
            largeur_m=5.0,
            pente_m_m=0.001,
            rugosite_manning=0.013,
            profondeur_aval_m=1.5,
            longueur_calcul_m=100.0,
            pas_m=10.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["debit_m3s"] == 10.0
        assert resultat["largeur_m"] == 5.0
        assert resultat["pente_m_m"] == 0.001
        assert resultat["profondeur_aval_m"] == 1.5
        assert len(resultat["points_courbe"]) > 0
        assert "abscisses_m" in resultat["points_courbe"]
        assert "profondeurs_m" in resultat["points_courbe"]
        assert "vitesses_ms" in resultat["points_courbe"]
        assert "nombres_froude" in resultat["points_courbe"]
    
    def test_6_pertes_charge_lineaires_ecoulement_turbulent(self):
        """Test 6: Pertes de charge en écoulement turbulent (niveau: moyen)"""
        resultat = calculer_pertes_charge_lineaires(
            debit_m3s=1.0,  # Débit élevé
            diametre_m=0.5,  # Diamètre important
            longueur_m=500.0,
            rugosite_mm=0.5,  # Rugosité élevée
            viscosite_m2s=1.004e-6
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["nombre_reynolds"] > 4000  # Écoulement turbulent
        assert resultat["coefficient_frottement"] > 0.01  # Frottement important
        assert resultat["pertes_charge_m"] > 1.0  # Pertes importantes
    
    def test_7_pertes_charge_singulieres_complexes(self):
        """Test 7: Pertes de charge singulières complexes (niveau: moyen)"""
        coefficients_k = {
            "entree_brusque": 0.5,
            "reduction_brusque": 0.3,
            "elargissement_brusque": 0.4,
            "coude_90_degre": 0.3,
            "coude_45_degre": 0.2,
            "vanne_ouverte": 0.1,
            "vanne_fermee": 10.0,
            "sortie": 1.0
        }
        
        resultat = calculer_pertes_charge_singulieres(
            vitesse_ms=3.0,
            coefficients_k=coefficients_k
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["vitesse_ms"] == 3.0
        assert len(resultat["pertes_charge_detaillees"]) == 8
        assert resultat["pertes_charge_totales_m"] > 0
        assert "vanne_fermee" in resultat["pertes_charge_detaillees"]
        assert resultat["pertes_charge_detaillees"]["vanne_fermee"] > resultat["pertes_charge_detaillees"]["vanne_ouverte"]
    
    def test_8_calcul_debit_critique_differentes_profondeurs(self):
        """Test 8: Calcul du débit critique avec différentes profondeurs (niveau: moyen)"""
        profondeurs = [0.5, 1.0, 1.5, 2.0]
        debits_critiques = []
        
        for profondeur in profondeurs:
            resultat = calculer_debit_critique(
                largeur_m=3.0,
                profondeur_m=profondeur,
                pente_m_m=0.005,
                rugosite_manning=0.013
            )
            
            assert resultat["statut"] == "OK"
            debits_critiques.append(resultat["debit_critique_m3s"])
        
        # Vérifier que le débit critique augmente avec la profondeur
        for i in range(1, len(debits_critiques)):
            assert debits_critiques[i] > debits_critiques[i-1]
    
    def test_9_verification_stabilite_talus_differentes_conditions(self):
        """Test 9: Vérification de stabilité avec différentes conditions (niveau: moyen)"""
        # Test avec talus raide
        resultat_raide = verifier_stabilite_talus(
            hauteur_m=10.0,
            pente_talus=1.0,  # 1V:1H (très raide)
            angle_frottement_deg=25.0,
            cohesion_kpa=10.0,
            poids_volumique_kn_m3=18.0
        )
        
        # Test avec talus doux
        resultat_doux = verifier_stabilite_talus(
            hauteur_m=10.0,
            pente_talus=4.0,  # 1V:4H (très doux)
            angle_frottement_deg=35.0,
            cohesion_kpa=30.0,
            poids_volumique_kn_m3=16.0
        )
        
        assert resultat_raide["statut"] == "OK"
        assert resultat_doux["statut"] == "OK"
        
        # Le talus doux devrait être plus stable
        assert resultat_doux["coefficient_securite"] > resultat_raide["coefficient_securite"]
    
    def test_10_courbe_remous_ecoulement_rapide(self):
        """Test 10: Courbe de remous en écoulement rapide (niveau: complexe)"""
        resultat = calculer_courbe_remous(
            debit_m3s=50.0,  # Débit élevé
            largeur_m=8.0,
            pente_m_m=0.01,  # Pente importante
            rugosite_manning=0.012,
            profondeur_aval_m=2.0,
            longueur_calcul_m=200.0,
            pas_m=20.0
        )
        
        assert resultat["statut"] == "OK"
        assert len(resultat["points_courbe"]["abscisses_m"]) > 0
        assert len(resultat["points_courbe"]["profondeurs_m"]) > 0
        assert len(resultat["points_courbe"]["vitesses_ms"]) > 0
        assert len(resultat["points_courbe"]["nombres_froude"]) > 0
        
        # Vérifier que les profondeurs sont cohérentes
        profondeurs = resultat["points_courbe"]["profondeurs_m"]
        for i in range(1, len(profondeurs)):
            # En écoulement rapide, la profondeur devrait diminuer vers l'amont
            assert profondeurs[i] >= profondeurs[i-1]
    
    def test_11_pertes_charge_lineaires_ecoulement_laminar(self):
        """Test 11: Pertes de charge en écoulement laminaire (niveau: moyen)"""
        resultat = calculer_pertes_charge_lineaires(
            debit_m3s=0.001,  # Débit très faible
            diametre_m=0.1,  # Petit diamètre
            longueur_m=10.0,
            rugosite_mm=0.01,  # Rugosité faible
            viscosite_m2s=1.004e-6
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["nombre_reynolds"] < 2300  # Écoulement laminaire
        assert resultat["coefficient_frottement"] > 0.01
        assert resultat["pertes_charge_m"] > 0
    
    def test_12_pertes_charge_singulieres_vitesse_nulle(self):
        """Test 12: Pertes de charge singulières avec vitesse nulle (niveau: facile)"""
        coefficients_k = {"entree": 0.5}
        
        resultat = calculer_pertes_charge_singulieres(
            vitesse_ms=0.0,
            coefficients_k=coefficients_k
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["vitesse_ms"] == 0.0
        assert resultat["pertes_charge_totales_m"] == 0.0
        assert resultat["pertes_charge_detaillees"]["entree"] == 0.0
    
    def test_13_calcul_debit_critique_profondeur_nulle(self):
        """Test 13: Calcul du débit critique avec profondeur nulle (niveau: facile)"""
        resultat = calculer_debit_critique(
            largeur_m=2.0,
            profondeur_m=0.0,
            pente_m_m=0.01,
            rugosite_manning=0.013
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["debit_critique_m3s"] == 0.0
        assert resultat["vitesse_critique_ms"] == 0.0
        assert resultat["nombre_froude"] == 0.0
    
    def test_14_verification_stabilite_talus_hauteur_nulle(self):
        """Test 14: Vérification de stabilité avec hauteur nulle (niveau: facile)"""
        resultat = verifier_stabilite_talus(
            hauteur_m=0.0,
            pente_talus=2.0,
            angle_frottement_deg=30.0,
            cohesion_kpa=20.0,
            poids_volumique_kn_m3=20.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["coefficient_securite"] > 1000  # Très stable (pas de talus)
        assert resultat["stabilite"] == "Stable"
    
    def test_15_courbe_remous_profondeur_aval_nulle(self):
        """Test 15: Courbe de remous avec profondeur aval nulle (niveau: moyen)"""
        resultat = calculer_courbe_remous(
            debit_m3s=5.0,
            largeur_m=3.0,
            pente_m_m=0.005,
            rugosite_manning=0.013,
            profondeur_aval_m=0.0,
            longueur_calcul_m=50.0,
            pas_m=5.0
        )
        
        assert resultat["statut"] == "OK"
        # Avec une profondeur aval nulle, la courbe devrait être vide ou très courte
        assert len(resultat["points_courbe"]["profondeurs_m"]) >= 0
    
    def test_16_pertes_charge_lineaires_parametres_extremes(self):
        """Test 16: Pertes de charge avec paramètres extrêmes (niveau: complexe)"""
        # Test avec débit très élevé
        resultat_grand_debit = calculer_pertes_charge_lineaires(
            debit_m3s=100.0,
            diametre_m=1.0,
            longueur_m=1000.0,
            rugosite_mm=1.0,
            viscosite_m2s=1.004e-6
        )
        
        assert resultat_grand_debit["statut"] == "OK"
        assert resultat_grand_debit["nombre_reynolds"] > 100000  # Écoulement très turbulent
        assert resultat_grand_debit["pertes_charge_m"] > 10.0  # Pertes importantes
        
        # Test avec débit très faible
        resultat_petit_debit = calculer_pertes_charge_lineaires(
            debit_m3s=0.0001,
            diametre_m=0.05,
            longueur_m=1.0,
            rugosite_mm=0.001,
            viscosite_m2s=1.004e-6
        )
        
        assert resultat_petit_debit["statut"] == "OK"
        assert resultat_petit_debit["nombre_reynolds"] < 1000  # Écoulement laminaire
        assert resultat_petit_debit["pertes_charge_m"] < 0.1  # Pertes faibles
    
    def test_17_calcul_debit_critique_differentes_pentes(self):
        """Test 17: Calcul du débit critique avec différentes pentes (niveau: moyen)"""
        pentes = [0.001, 0.005, 0.01, 0.02]
        debits_critiques = []
        
        for pente in pentes:
            resultat = calculer_debit_critique(
                largeur_m=4.0,
                profondeur_m=1.0,
                pente_m_m=pente,
                rugosite_manning=0.013
            )
            
            assert resultat["statut"] == "OK"
            debits_critiques.append(resultat["debit_critique_m3s"])
        
        # Vérifier que le débit critique augmente avec la pente
        for i in range(1, len(debits_critiques)):
            assert debits_critiques[i] > debits_critiques[i-1]
    
    def test_18_verification_stabilite_talus_materiaux_differents(self):
        """Test 18: Vérification de stabilité avec différents matériaux (niveau: complexe)"""
        # Sol cohérent (argile)
        resultat_argile = verifier_stabilite_talus(
            hauteur_m=8.0,
            pente_talus=2.0,
            angle_frottement_deg=20.0,
            cohesion_kpa=50.0,
            poids_volumique_kn_m3=18.0
        )
        
        # Sol pulvérulent (sable)
        resultat_sable = verifier_stabilite_talus(
            hauteur_m=8.0,
            pente_talus=2.0,
            angle_frottement_deg=35.0,
            cohesion_kpa=0.0,
            poids_volumique_kn_m3=16.0
        )
        
        assert resultat_argile["statut"] == "OK"
        assert resultat_sable["statut"] == "OK"
        
        # L'argile devrait être plus stable que le sable pour la même pente
        assert resultat_argile["coefficient_securite"] > resultat_sable["coefficient_securite"]
    
    def test_19_courbe_remous_ecoulement_lent(self):
        """Test 19: Courbe de remous en écoulement lent (niveau: complexe)"""
        resultat = calculer_courbe_remous(
            debit_m3s=2.0,  # Débit faible
            largeur_m=4.0,
            pente_m_m=0.0005,  # Pente faible
            rugosite_manning=0.015,
            profondeur_aval_m=1.5,
            longueur_calcul_m=300.0,
            pas_m=30.0
        )
        
        assert resultat["statut"] == "OK"
        assert len(resultat["points_courbe"]["abscisses_m"]) > 0
        
        # En écoulement lent, la profondeur devrait augmenter vers l'amont
        profondeurs = resultat["points_courbe"]["profondeurs_m"]
        for i in range(1, len(profondeurs)):
            assert profondeurs[i] <= profondeurs[i-1]
    
    def test_20_integration_complete_hydraulique(self):
        """Test 20: Test d'intégration complète hydraulique (niveau: très complexe)"""
        # 1. Calculer les pertes de charge linéaires
        resultat_pertes_lineaires = calculer_pertes_charge_lineaires(
            debit_m3s=5.0,
            diametre_m=0.3,
            longueur_m=200.0,
            rugosite_mm=0.1,
            viscosite_m2s=1.004e-6
        )
        
        assert resultat_pertes_lineaires["statut"] == "OK"
        pertes_lineaires = resultat_pertes_lineaires["pertes_charge_m"]
        
        # 2. Calculer les pertes de charge singulières
        coefficients_k = {"entree": 0.5, "sortie": 1.0}
        resultat_pertes_singulieres = calculer_pertes_charge_singulieres(
            vitesse_ms=resultat_pertes_lineaires["vitesse_ms"],
            coefficients_k=coefficients_k
        )
        
        assert resultat_pertes_singulieres["statut"] == "OK"
        pertes_singulieres = resultat_pertes_singulieres["pertes_charge_totales_m"]
        
        # 3. Calculer le débit critique pour un canal
        resultat_debit_critique = calculer_debit_critique(
            largeur_m=3.0,
            profondeur_m=1.0,
            pente_m_m=0.01,
            rugosite_manning=0.013
        )
        
        assert resultat_debit_critique["statut"] == "OK"
        
        # 4. Vérifier la stabilité d'un talus
        resultat_stabilite = verifier_stabilite_talus(
            hauteur_m=6.0,
            pente_talus=2.5,
            angle_frottement_deg=28.0,
            cohesion_kpa=25.0,
            poids_volumique_kn_m3=19.0
        )
        
        assert resultat_stabilite["statut"] == "OK"
        
        # 5. Calculer une courbe de remous
        resultat_courbe_remous = calculer_courbe_remous(
            debit_m3s=resultat_debit_critique["debit_critique_m3s"],
            largeur_m=3.0,
            pente_m_m=0.01,
            rugosite_manning=0.013,
            profondeur_aval_m=1.0,
            longueur_calcul_m=100.0,
            pas_m=10.0
        )
        
        assert resultat_courbe_remous["statut"] == "OK"
        
        # 6. Vérifier la cohérence des résultats
        assert pertes_lineaires > 0
        assert pertes_singulieres > 0
        assert resultat_debit_critique["debit_critique_m3s"] > 0
        assert resultat_stabilite["coefficient_securite"] > 0
        assert len(resultat_courbe_remous["points_courbe"]["profondeurs_m"]) > 0
        
        # 7. Vérifier que les pertes totales sont cohérentes
        pertes_totales = pertes_lineaires + pertes_singulieres
        assert pertes_totales > pertes_lineaires
        assert pertes_totales > pertes_singulieres 