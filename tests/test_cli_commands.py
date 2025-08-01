"""
Tests pour vérifier l'affichage automatique des paramètres d'entrée des commandes CLI.
"""

import pytest
import sys
import os
import subprocess
from unittest.mock import patch, MagicMock
from io import StringIO

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestCLICommandsParameterDisplay:
    """Tests pour vérifier l'affichage des paramètres d'entrée des commandes CLI."""
    
    def run_lcpi_command(self, command_args):
        """Exécute une commande lcpi et retourne la sortie."""
        try:
            result = subprocess.run(
                ["python", "-m", "lcpi"] + command_args,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.join(os.path.dirname(__file__), '..')
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Timeout", 1
        except Exception as e:
            return "", str(e), 1
    
    def test_cm_check_poteau_no_args(self):
        """Test de la commande cm check-poteau sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-poteau"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Poteau (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
        assert "Chemin vers le fichier YAML de définition du poteau" in stdout
        assert "lcpi cm check-poteau --filepath poteau_exemple.yml" in stdout
    
    def test_cm_check_deversement_no_args(self):
        """Test de la commande cm check-deversement sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-deversement"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Déversement (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
        assert "Chemin vers le fichier YAML de définition de la poutre" in stdout
    
    def test_cm_check_tendu_no_args(self):
        """Test de la commande cm check-tendu sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-tendu"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Élément Tendu (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_cm_check_compose_no_args(self):
        """Test de la commande cm check-compose sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-compose"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Sollicitations Composées (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_cm_check_fleche_no_args(self):
        """Test de la commande cm check-fleche sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-fleche"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Flèche (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_cm_check_assemblage_boulon_no_args(self):
        """Test de la commande cm check-assemblage-boulon sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-assemblage-boulon"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Assemblage Boulonné (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_cm_check_assemblage_soude_no_args(self):
        """Test de la commande cm check-assemblage-soude sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "check-assemblage-soude"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Assemblage Soudé (Construction Métallique)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_cm_optimize_section_no_args(self):
        """Test de la commande cm optimize-section sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["cm", "optimize-section"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Optimisation de Section (Construction Métallique)" in stdout
        assert "--check (-c)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_poteau_no_args(self):
        """Test de la commande bois check-poteau sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-poteau"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Poteau (Bois)" in stdout
        assert "--filepath (-f)" in stdout
        assert "Vérifie un poteau en bois en compression avec flambement selon Eurocode 5" in stdout
    
    def test_bois_check_deversement_no_args(self):
        """Test de la commande bois check-deversement sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-deversement"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Déversement (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_cisaillement_no_args(self):
        """Test de la commande bois check-cisaillement sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-cisaillement"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Cisaillement (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_compression_perp_no_args(self):
        """Test de la commande bois check-compression-perp sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-compression-perp"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Compression Perpendiculaire (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_compose_no_args(self):
        """Test de la commande bois check-compose sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-compose"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Sollicitations Composées (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_no_args(self):
        """Test de la commande bois check sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Traitement par Lot (Bois)" in stdout
        assert "--filepath (-f)" in stdout
        assert "--batch-file (-b)" in stdout
        assert "--output-file" in stdout
    
    def test_bois_check_fleche_no_args(self):
        """Test de la commande bois check-fleche sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-fleche"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Flèche (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_assemblage_pointe_no_args(self):
        """Test de la commande bois check-assemblage-pointe sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-assemblage-pointe"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Assemblage à Pointes (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_bois_check_assemblage_embrevement_no_args(self):
        """Test de la commande bois check-assemblage-embrevement sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["bois", "check-assemblage-embrevement"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification Assemblage par Embrevement (Bois)" in stdout
        assert "--filepath (-f)" in stdout
    
    def test_beton_calc_poteau_no_args(self):
        """Test de la commande beton calc-poteau sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["beton", "calc-poteau"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Calcul Poteau (Béton)" in stdout
        assert "--filepath (-f)" in stdout
        assert "--batch-file (-b)" in stdout
        assert "Calcule un ou plusieurs poteaux en béton selon BAEL 91 / Eurocode 2" in stdout
    
    def test_beton_calc_radier_no_args(self):
        """Test de la commande beton calc-radier sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["beton", "calc-radier"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Calcul Radier (Béton)" in stdout
        assert "--filepath (-f)" in stdout
        assert "Calcule un radier en béton selon BAEL 91 / Eurocode 2" in stdout
    
    def test_hydro_plomberie_dimensionner_no_args(self):
        """Test de la commande hydro plomberie dimensionner sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "plomberie", "dimensionner"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Dimensionnement Plomberie" in stdout
        assert "--nb-appareils (-n)" in stdout
        assert "--debits-base (-d)" in stdout
        assert "--v-max" in stdout
    
    def test_hydro_reservoir_equilibrage_no_args(self):
        """Test de la commande hydro reservoir equilibrage sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "reservoir", "equilibrage"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Dimensionnement Réservoir d'Équilibrage" in stdout
        assert "--demande-journaliere (-d)" in stdout
        assert "--cp-jour" in stdout
        assert "--cp-horaire" in stdout
        assert "--jours-stockage" in stdout
    
    def test_hydro_reservoir_incendie_no_args(self):
        """Test de la commande hydro reservoir incendie sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "reservoir", "incendie"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Dimensionnement Réservoir d'Incendie" in stdout
        assert "--population (-p)" in stdout
        assert "--type-zone (-t)" in stdout
    
    def test_hydro_reservoir_complet_no_args(self):
        """Test de la commande hydro reservoir complet sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "reservoir", "complet"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Dimensionnement Réservoir Complet" in stdout
        assert "--population (-p)" in stdout
        assert "--dotation (-d)" in stdout
        assert "--cp-jour" in stdout
        assert "--cp-horaire" in stdout
        assert "--jours-securite" in stdout
        assert "--type-zone (-t)" in stdout
    
    def test_hydro_reservoir_verifier_pression_no_args(self):
        """Test de la commande hydro reservoir verifier-pression sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "reservoir", "verifier-pression"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Vérification de la Pression" in stdout
        assert "--cote-reservoir (-c)" in stdout
        assert "--cote-terrain (-t)" in stdout
        assert "--pertes-charge (-p)" in stdout
        assert "--pression-min" in stdout
    
    def test_hydro_util_prevoir_population_no_args(self):
        """Test de la commande hydro util prevoir-population sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "util", "prevoir-population"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Prévision de Population" in stdout
        assert "--method (-m)" in stdout
        assert "--annee (-a)" in stdout
    
    def test_hydro_util_estimer_demande_eau_no_args(self):
        """Test de la commande hydro util estimer-demande-eau sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "util", "estimer-demande-eau"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Estimation Demande en Eau" in stdout
        assert "--pop (-p)" in stdout
        assert "--dota (-d)" in stdout
    
    def test_hydro_util_diagramme_ombro_no_args(self):
        """Test de la commande hydro util diagramme-ombro sans arguments."""
        stdout, stderr, returncode = self.run_lcpi_command(["hydro", "util", "diagramme-ombro"])
        
        assert returncode == 0
        assert "Paramètres d'entrée - Génération Diagramme Ombrothermique" in stdout
        assert "--filepath (-f)" in stdout
        assert "--output (-o)" in stdout


class TestCLICommandsWithArgs:
    """Tests pour vérifier que les commandes fonctionnent toujours avec des arguments."""
    
    def run_lcpi_command(self, command_args):
        """Exécute une commande lcpi et retourne la sortie."""
        try:
            result = subprocess.run(
                ["python", "-m", "lcpi"] + command_args,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.join(os.path.dirname(__file__), '..')
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Timeout", 1
        except Exception as e:
            return "", str(e), 1
    
    def test_hydro_plomberie_dimensionner_with_args(self):
        """Test de la commande hydro plomberie dimensionner avec arguments."""
        stdout, stderr, returncode = self.run_lcpi_command([
            "hydro", "plomberie", "dimensionner", 
            "--nb-appareils", "5", 
            "--debits-base", "2.5"
        ])
        
        # La commande devrait fonctionner (même si elle peut échouer sur les calculs)
        # L'important est qu'elle ne retourne pas l'affichage des paramètres
        assert "Paramètres d'entrée - Dimensionnement Plomberie" not in stdout
    
    def test_hydro_reservoir_equilibrage_with_args(self):
        """Test de la commande hydro reservoir equilibrage avec arguments."""
        stdout, stderr, returncode = self.run_lcpi_command([
            "hydro", "reservoir", "equilibrage", 
            "--demande-journaliere", "1000"
        ])
        
        # La commande devrait fonctionner
        assert "Paramètres d'entrée - Dimensionnement Réservoir d'Équilibrage" not in stdout
    
    def test_hydro_reservoir_incendie_with_args(self):
        """Test de la commande hydro reservoir incendie avec arguments."""
        stdout, stderr, returncode = self.run_lcpi_command([
            "hydro", "reservoir", "incendie", 
            "--population", "5000"
        ])
        
        # La commande devrait fonctionner
        assert "Paramètres d'entrée - Dimensionnement Réservoir d'Incendie" not in stdout


if __name__ == "__main__":
    pytest.main([__file__]) 