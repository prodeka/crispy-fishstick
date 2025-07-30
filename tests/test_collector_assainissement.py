#!/usr/bin/env python3
"""
Tests unitaires pour le module collecteur d'assainissement.
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

from lcpi.hydrodrain.calculs.assainissement_gravitaire import (
    Troncon, Reseau, dimensionner_reseau_eaux_usees, dimensionner_reseau_eaux_pluviales,
    calculer_debit_propre_eaux_usees, calculer_debit_amont, agreger_donnees_amont,
    run_calcul_rationnelle, calculer_tc_surface, calculer_intensite_pluie,
    dimensionner_section, dimensionner_circulaire, dimensionner_rectangulaire,
    dimensionner_trapezoidal, creer_reseau_depuis_json, exporter_resultats_json
)

class TestCollecteurAssainissement:
    """Tests pour le module collecteur d'assainissement."""
    
    def test_1_creation_troncon_simple(self):
        """Test 1: Création d'un tronçon simple (niveau: facile)"""
        troncon = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[]
        )
        
        assert troncon.id == "T1"
        assert troncon.type_section == "circulaire"
        assert troncon.longueur_troncon_m == 100.0
        assert troncon.pente_troncon == 0.005
        assert troncon.ks_manning_strickler == 70.0
        assert troncon.amont_ids == []
        assert troncon.statut == "En attente"
    
    def test_2_creation_reseau_vide(self):
        """Test 2: Création d'un réseau vide (niveau: facile)"""
        reseau = Reseau()
        
        assert len(reseau.troncons) == 0
        assert isinstance(reseau.troncons, dict)
    
    def test_3_ajout_troncon_au_reseau(self):
        """Test 3: Ajout d'un tronçon au réseau (niveau: facile)"""
        reseau = Reseau()
        troncon = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[]
        )
        
        reseau.ajouter_troncon(troncon)
        
        assert len(reseau.troncons) == 1
        assert "T1" in reseau.troncons
        assert reseau.troncons["T1"] == troncon
    
    def test_4_tri_topologique_simple(self):
        """Test 4: Tri topologique d'un réseau simple (niveau: moyen)"""
        reseau = Reseau()
        
        # Tronçon amont
        troncon1 = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[]
        )
        
        # Tronçon aval
        troncon2 = Troncon(
            id="T2",
            type_section="circulaire",
            longueur_troncon_m=150.0,
            pente_troncon=0.004,
            ks_manning_strickler=70.0,
            amont_ids=["T1"]
        )
        
        reseau.ajouter_troncon(troncon1)
        reseau.ajouter_troncon(troncon2)
        
        troncons_tries = reseau.trier_topologiquement()
        
        assert len(troncons_tries) == 2
        assert troncons_tries[0].id == "T1"  # Amont en premier
        assert troncons_tries[1].id == "T2"  # Aval en second
    
    def test_5_calcul_debit_propre_eaux_usees(self):
        """Test 5: Calcul du débit propre pour eaux usées (niveau: moyen)"""
        troncon = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[],
            population=100,
            dotation_l_jour_hab=150.0,
            coefficient_pointe=2.5
        )
        
        debit_propre = calculer_debit_propre_eaux_usees(troncon)
        
        # Calcul attendu: (150 * 2.5 * 100) / (1000 * 86400) = 0.000434
        assert abs(debit_propre - 0.000434) < 0.000001
    
    def test_6_calcul_debit_amont(self):
        """Test 6: Calcul du débit amont (niveau: moyen)"""
        reseau = Reseau()
        
        # Tronçon amont avec débit calculé
        troncon1 = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[]
        )
        troncon1.q_max_m3s = 0.001
        
        # Tronçon aval
        troncon2 = Troncon(
            id="T2",
            type_section="circulaire",
            longueur_troncon_m=150.0,
            pente_troncon=0.004,
            ks_manning_strickler=70.0,
            amont_ids=["T1"]
        )
        
        reseau.ajouter_troncon(troncon1)
        reseau.ajouter_troncon(troncon2)
        
        debit_amont = calculer_debit_amont(troncon2, reseau)
        
        assert debit_amont == 0.001
    
    def test_7_dimensionnement_circulaire_simple(self):
        """Test 7: Dimensionnement d'une section circulaire simple (niveau: moyen)"""
        resultat = dimensionner_circulaire(
            debit_m3s=0.01,  # 10 L/s
            pente=0.005,
            ks=70.0
        )
        
        assert resultat["statut"] == "OK"
        assert resultat["type_section"] == "circulaire"
        assert "diametre_mm" in resultat
        assert "vitesse_ms" in resultat
        assert resultat["vitesse_ms"] > 0
    
    def test_8_calcul_tc_surface_kirpich(self):
        """Test 8: Calcul du temps de concentration selon Kirpich (niveau: moyen)"""
        troncon = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[],
            longueur_parcours_m=80.0,
            pente_parcours_m_m=0.02
        )
        
        tc = calculer_tc_surface(troncon)
        
        # Vérification que le temps de concentration est raisonnable
        assert tc > 0
        assert tc < 60  # Moins d'une heure
    
    def test_9_calcul_intensite_pluie_talbot(self):
        """Test 9: Calcul de l'intensité de pluie selon Talbot (niveau: moyen)"""
        params_pluie = {
            "type": "talbot",
            "a": 120,
            "b": 20
        }
        
        intensite = calculer_intensite_pluie(30.0, params_pluie)  # 30 minutes
        
        # Calcul attendu: 120 / (20 + 30) = 2.4 mm/h
        assert abs(intensite - 2.4) < 0.01
    
    def test_10_reseau_eaux_usees_complet(self):
        """Test 10: Dimensionnement complet d'un réseau d'eaux usées (niveau: complexe)"""
        reseau = Reseau()
        
        # Tronçon amont
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
        
        # Tronçon aval
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
        
        resultats = dimensionner_reseau_eaux_usees(reseau)
        
        assert resultats["statut"] == "OK"
        assert len(resultats["troncons"]) == 2
        
        # Vérification du premier tronçon
        troncon1_resultat = resultats["troncons"][0]
        assert troncon1_resultat["id"] == "T1"
        assert troncon1_resultat["q_max_m3s"] > 0
        assert troncon1_resultat["resultat_dimensionnement"]["statut"] == "OK"
        
        # Vérification du second tronçon (débit cumulé)
        troncon2_resultat = resultats["troncons"][1]
        assert troncon2_resultat["id"] == "T2"
        assert troncon2_resultat["q_max_m3s"] > troncon1_resultat["q_max_m3s"]  # Débit cumulé
    
    def test_11_reseau_eaux_pluviales_complet(self):
        """Test 11: Dimensionnement complet d'un réseau d'eaux pluviales (niveau: complexe)"""
        reseau = Reseau()
        
        # Tronçon amont
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
        
        # Tronçon aval
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
        
        params_pluie = {
            "type": "talbot",
            "a": 120,
            "b": 20
        }
        
        resultats = dimensionner_reseau_eaux_pluviales(reseau, params_pluie)
        
        assert resultats["statut"] == "OK"
        assert len(resultats["troncons"]) == 2
        
        # Vérification que les calculs itératifs ont fonctionné
        for troncon_resultat in resultats["troncons"]:
            assert troncon_resultat["q_max_m3s"] > 0
            assert troncon_resultat["tc_final_min"] > 0
            assert troncon_resultat["resultat_dimensionnement"]["statut"] == "OK"
    
    def test_12_erreur_cycle_reseau(self):
        """Test 12: Détection d'un cycle dans le réseau (niveau: complexe)"""
        reseau = Reseau()
        
        # Création d'un cycle: T1 -> T2 -> T3 -> T1
        troncon1 = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=["T3"]  # Cycle
        )
        
        troncon2 = Troncon(
            id="T2",
            type_section="circulaire",
            longueur_troncon_m=150.0,
            pente_troncon=0.004,
            ks_manning_strickler=70.0,
            amont_ids=["T1"]
        )
        
        troncon3 = Troncon(
            id="T3",
            type_section="circulaire",
            longueur_troncon_m=200.0,
            pente_troncon=0.003,
            ks_manning_strickler=70.0,
            amont_ids=["T2"]
        )
        
        reseau.ajouter_troncon(troncon1)
        reseau.ajouter_troncon(troncon2)
        reseau.ajouter_troncon(troncon3)
        
        # Le tri topologique doit lever une exception
        with pytest.raises(ValueError, match="Le réseau contient des cycles"):
            reseau.trier_topologiquement()
    
    def test_13_export_import_json(self):
        """Test 13: Export et import JSON (niveau: moyen)"""
        # Créer un réseau de test
        reseau = Reseau()
        troncon = Troncon(
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
        reseau.ajouter_troncon(troncon)
        
        # Export vers fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_path = f.name
        
        try:
            exporter_resultats_json(reseau, export_path)
            
            # Import du fichier
            reseau_importe = creer_reseau_depuis_json(export_path)
            
            assert len(reseau_importe.troncons) == 1
            assert "T1" in reseau_importe.troncons
            
            troncon_importe = reseau_importe.troncons["T1"]
            assert troncon_importe.id == "T1"
            assert troncon_importe.type_section == "circulaire"
            assert troncon_importe.longueur_troncon_m == 100.0
            
        finally:
            # Nettoyage
            if os.path.exists(export_path):
                os.unlink(export_path)
    
    def test_14_dimensionnement_sections_alternatives(self):
        """Test 14: Dimensionnement des sections rectangulaire et trapézoïdale (niveau: moyen)"""
        # Test section rectangulaire
        resultat_rect = dimensionner_rectangulaire(
            debit_m3s=0.05,  # 50 L/s
            pente=0.005,
            ks=70.0
        )
        
        assert resultat_rect["statut"] == "OK"
        assert resultat_rect["type_section"] == "rectangulaire"
        assert "largeur_m" in resultat_rect
        assert "hauteur_m" in resultat_rect
        
        # Test section trapézoïdale
        resultat_trap = dimensionner_trapezoidal(
            debit_m3s=0.1,  # 100 L/s
            pente=0.005,
            ks=70.0
        )
        
        assert resultat_trap["statut"] == "OK"
        assert resultat_trap["type_section"] == "trapezoidal"
        assert "largeur_base_m" in resultat_trap
        assert "hauteur_m" in resultat_trap
        assert "fruit" in resultat_trap
    
    def test_15_calcul_intensite_pluie_montana(self):
        """Test 15: Calcul de l'intensité de pluie selon Montana (niveau: moyen)"""
        params_pluie = {
            "type": "montana",
            "a": 120,
            "b": 0.5
        }
        
        intensite = calculer_intensite_pluie(30.0, params_pluie)  # 30 minutes
        
        # Calcul attendu: 120 * (30^(-0.5)) = 120 / sqrt(30) ≈ 21.9 mm/h
        assert abs(intensite - 21.9) < 0.1
    
    def test_16_erreur_type_section_inconnu(self):
        """Test 16: Gestion d'erreur pour type de section inconnu (niveau: facile)"""
        troncon = Troncon(
            id="T1",
            type_section="ovale",  # Type non supporté
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[],
            population=50,
            dotation_l_jour_hab=150.0,
            coefficient_pointe=2.5
        )
        troncon.q_max_m3s = 0.01
        
        resultat = dimensionner_section(troncon)
        
        assert resultat["statut"] == "Erreur"
        assert "Type de section 'ovale' non supporté" in resultat["message"]
    
    def test_17_erreur_debit_trop_eleve(self):
        """Test 17: Gestion d'erreur pour débit trop élevé (niveau: moyen)"""
        resultat = dimensionner_circulaire(
            debit_m3s=1000.0,  # Débit énorme
            pente=0.005,
            ks=70.0
        )
        
        assert resultat["statut"] == "Erreur"
        assert "Débit trop élevé" in resultat["message"]
    
    def test_18_agregation_donnees_amont(self):
        """Test 18: Agrégation des données amont pour eaux pluviales (niveau: complexe)"""
        reseau = Reseau()
        
        # Tronçon amont
        troncon1 = Troncon(
            id="T1",
            type_section="circulaire",
            longueur_troncon_m=100.0,
            pente_troncon=0.005,
            ks_manning_strickler=70.0,
            amont_ids=[],
            surface_propre_ha=2.0,
            coefficient_ruissellement=0.8,
            longueur_parcours_m=80.0,
            pente_parcours_m_m=0.02
        )
        troncon1.surface_cumulee_ha = 2.0
        troncon1.coefficient_moyen = 0.8
        troncon1.tc_final_min = 15.0
        
        # Tronçon aval
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
        
        agreger_donnees_amont(troncon2, reseau)
        
        # Vérification de l'agrégation
        assert troncon2.surface_cumulee_ha == 5.0  # 2.0 + 3.0
        assert abs(troncon2.coefficient_moyen - 0.74) < 0.01  # (0.8*2 + 0.7*3) / 5
        assert troncon2.tc_final_min is None  # Pas encore calculé
    
    def test_19_convergence_calcul_rationnelle(self):
        """Test 19: Test de convergence du calcul rationnel (niveau: complexe)"""
        reseau = Reseau()
        
        troncon = Troncon(
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
        reseau.ajouter_troncon(troncon)
        
        params_pluie = {
            "type": "talbot",
            "a": 120,
            "b": 20
        }
        
        resultat = run_calcul_rationnelle(troncon, params_pluie)
        
        assert resultat["statut"] == "OK"
        assert resultat["debit_projet"] > 0
        assert resultat["tc_final"] > 0
        assert resultat["iterations"] > 0
        assert resultat["iterations"] <= 20  # Maximum d'itérations
    
    def test_20_reseau_complexe_multiple_troncons(self):
        """Test 20: Réseau complexe avec plusieurs tronçons (niveau: très complexe)"""
        reseau = Reseau()
        
        # Créer un réseau en étoile: T1 -> T2, T1 -> T3, T2 -> T4, T3 -> T4
        troncons = [
            Troncon(id="T1", type_section="circulaire", longueur_troncon_m=100.0, 
                   pente_troncon=0.005, ks_manning_strickler=70.0, amont_ids=[],
                   population=50, dotation_l_jour_hab=150.0, coefficient_pointe=2.5),
            Troncon(id="T2", type_section="circulaire", longueur_troncon_m=150.0, 
                   pente_troncon=0.004, ks_manning_strickler=70.0, amont_ids=["T1"],
                   population=75, dotation_l_jour_hab=150.0, coefficient_pointe=2.5),
            Troncon(id="T3", type_section="circulaire", longueur_troncon_m=120.0, 
                   pente_troncon=0.004, ks_manning_strickler=70.0, amont_ids=["T1"],
                   population=60, dotation_l_jour_hab=150.0, coefficient_pointe=2.5),
            Troncon(id="T4", type_section="circulaire", longueur_troncon_m=200.0, 
                   pente_troncon=0.003, ks_manning_strickler=70.0, amont_ids=["T2", "T3"],
                   population=100, dotation_l_jour_hab=150.0, coefficient_pointe=2.5)
        ]
        
        for troncon in troncons:
            reseau.ajouter_troncon(troncon)
        
        resultats = dimensionner_reseau_eaux_usees(reseau)
        
        assert resultats["statut"] == "OK"
        assert len(resultats["troncons"]) == 4
        
        # Vérifier l'ordre de calcul (T1, puis T2 et T3, puis T4)
        troncons_resultats = {t["id"]: t for t in resultats["troncons"]}
        
        # T1 doit avoir le plus petit débit
        assert troncons_resultats["T1"]["q_max_m3s"] < troncons_resultats["T2"]["q_max_m3s"]
        assert troncons_resultats["T1"]["q_max_m3s"] < troncons_resultats["T3"]["q_max_m3s"]
        
        # T4 doit avoir le plus grand débit (cumul de T2 et T3)
        assert troncons_resultats["T4"]["q_max_m3s"] > troncons_resultats["T2"]["q_max_m3s"]
        assert troncons_resultats["T4"]["q_max_m3s"] > troncons_resultats["T3"]["q_max_m3s"]
        
        # Vérifier que tous les tronçons ont été dimensionnés
        for troncon_resultat in resultats["troncons"]:
            assert troncon_resultat["resultat_dimensionnement"]["statut"] == "OK"
            assert troncon_resultat["q_max_m3s"] > 0 