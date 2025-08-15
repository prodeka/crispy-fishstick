"""
Tests pour les modèles Pydantic.
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.pydantic_models import (
    NoeudUnified, ConduiteUnified, ReseauCompletConfig,
    HardyCrossConfig, EpanetConfig, valider_fichier_yaml,
    valider_reseau_seul, NoeudRole, TypeReseau, CoefficientFrottement
)

class TestNoeudUnified:
    """Tests pour le modèle NoeudUnified."""
    
    def test_noeud_valide(self):
        """Test d'un nœud valide."""
        noeud = NoeudUnified(
            role=NoeudRole.CONSOMMATION,
            cote_m=150.0,
            demande_m3_s=0.02,
            pression_min_mce=20,
            pression_max_mce=80
        )
        
        assert noeud.role == NoeudRole.CONSOMMATION
        assert noeud.cote_m == 150.0
        assert noeud.demande_m3_s == 0.02
        assert noeud.pression_min_mce == 20
        assert noeud.pression_max_mce == 80
    
    def test_noeud_reservoir(self):
        """Test d'un nœud réservoir."""
        noeud = NoeudUnified(
            role=NoeudRole.RESERVOIR,
            cote_m=200.0,
            demande_m3_s=0.0,  # Réservoir n'a pas de demande
            pression_min_mce=20,
            pression_max_mce=80
        )
        
        assert noeud.role == NoeudRole.RESERVOIR
        assert noeud.demande_m3_s == 0.0
    
    def test_pression_max_inferieure_min(self):
        """Test d'erreur quand pression max < pression min."""
        with pytest.raises(ValueError, match="Pression max doit être > pression min"):
            NoeudUnified(
                role=NoeudRole.CONSOMMATION,
                cote_m=150.0,
                demande_m3_s=0.02,
                pression_min_mce=80,
                pression_max_mce=20  # Erreur !
            )
    
    def test_consommation_sans_demande(self):
        """Test d'erreur quand nœud de consommation n'a pas de demande."""
        with pytest.raises(ValueError, match="Les nœuds de consommation doivent avoir une demande > 0"):
            NoeudUnified(
                role=NoeudRole.CONSOMMATION,
                cote_m=150.0,
                demande_m3_s=0.0,  # Erreur !
                pression_min_mce=20,
                pression_max_mce=80
            )

class TestConduiteUnified:
    """Tests pour le modèle ConduiteUnified."""
    
    def test_conduite_valide(self):
        """Test d'une conduite valide."""
        conduite = ConduiteUnified(
            noeud_amont="N1",
            noeud_aval="N2",
            longueur_m=500.0,
            diametre_m=0.2,
            rugosite=100.0,
            materiau="acier"
        )
        
        assert conduite.noeud_amont == "N1"
        assert conduite.noeud_aval == "N2"
        assert conduite.longueur_m == 500.0
        assert conduite.diametre_m == 0.2
        assert conduite.rugosite == 100.0
        assert conduite.materiau == "acier"
        assert conduite.coefficient_frottement == CoefficientFrottement.HAZEN_WILLIAMS
    
    def test_diametre_trop_petit(self):
        """Test d'erreur quand diamètre trop petit."""
        with pytest.raises(ValueError, match="Diamètre doit être entre 0.01 et 5.0 mètres"):
            ConduiteUnified(
                noeud_amont="N1",
                noeud_aval="N2",
                longueur_m=500.0,
                diametre_m=0.005,  # Trop petit !
                rugosite=100.0,
                materiau="acier"
            )
    
    def test_longueur_trop_courte(self):
        """Test d'erreur quand longueur trop courte."""
        with pytest.raises(ValueError, match="Longueur doit être entre 1 et 10000 mètres"):
            ConduiteUnified(
                noeud_amont="N1",
                noeud_aval="N2",
                longueur_m=0.5,  # Trop court !
                diametre_m=0.2,
                rugosite=100.0,
                materiau="acier"
            )

class TestReseauCompletConfig:
    """Tests pour le modèle ReseauCompletConfig."""
    
    def test_reseau_valide(self):
        """Test d'un réseau valide."""
        reseau = ReseauCompletConfig(
            nom="Réseau Test",
            type=TypeReseau.MAILLE,
            noeuds={
                "N1": NoeudUnified(
                    role=NoeudRole.RESERVOIR,
                    cote_m=200.0,
                    demande_m3_s=0.0,
                    pression_min_mce=20,
                    pression_max_mce=80
                ),
                "N2": NoeudUnified(
                    role=NoeudRole.CONSOMMATION,
                    cote_m=150.0,
                    demande_m3_s=0.02,
                    pression_min_mce=20,
                    pression_max_mce=80
                )
            },
            conduites={
                "C1": ConduiteUnified(
                    noeud_amont="N1",
                    noeud_aval="N2",
                    longueur_m=500.0,
                    diametre_m=0.2,
                    rugosite=100.0,
                    materiau="acier"
                )
            }
        )
        
        assert reseau.nom == "Réseau Test"
        assert reseau.type == TypeReseau.MAILLE
        assert len(reseau.noeuds) == 2
        assert len(reseau.conduites) == 1
    
    def test_reseau_sans_reservoir(self):
        """Test d'erreur quand réseau n'a pas de réservoir."""
        with pytest.raises(ValueError, match="Le réseau doit contenir au moins un réservoir"):
            ReseauCompletConfig(
                nom="Réseau Test",
                type=TypeReseau.MAILLE,
                noeuds={
                    "N1": NoeudUnified(
                        role=NoeudRole.CONSOMMATION,  # Pas de réservoir !
                        cote_m=150.0,
                        demande_m3_s=0.02,
                        pression_min_mce=20,
                        pression_max_mce=80
                    )
                },
                conduites={}
            )
    
    def test_conduite_noeud_inexistant(self):
        """Test d'erreur quand conduite référence un nœud inexistant."""
        with pytest.raises(ValueError, match="Nœuds référencés dans les conduites mais non définis"):
            ReseauCompletConfig(
                nom="Réseau Test",
                type=TypeReseau.MAILLE,
                noeuds={
                    "N1": NoeudUnified(
                        role=NoeudRole.RESERVOIR,
                        cote_m=200.0,
                        demande_m3_s=0.0,
                        pression_min_mce=20,
                        pression_max_mce=80
                    )
                },
                conduites={
                    "C1": ConduiteUnified(
                        noeud_amont="N1",
                        noeud_aval="N3",  # Nœud inexistant !
                        longueur_m=500.0,
                        diametre_m=0.2,
                        rugosite=100.0,
                        materiau="acier"
                    )
                }
            )

class TestHardyCrossConfig:
    """Tests pour le modèle HardyCrossConfig."""
    
    def test_config_valide(self):
        """Test d'une configuration Hardy-Cross valide."""
        config = HardyCrossConfig(
            tolerance=1e-6,
            max_iterations=200,
            methode=CoefficientFrottement.HAZEN_WILLIAMS,
            convergence_criteria="debit"
        )
        
        assert config.tolerance == 1e-6
        assert config.max_iterations == 200
        assert config.methode == CoefficientFrottement.HAZEN_WILLIAMS
        assert config.convergence_criteria == "debit"
    
    def test_tolerance_negative(self):
        """Test d'erreur quand tolérance négative."""
        with pytest.raises(ValueError):
            HardyCrossConfig(
                tolerance=-1e-6,  # Négatif !
                max_iterations=200,
                methode=CoefficientFrottement.HAZEN_WILLIAMS,
                convergence_criteria="debit"
            )

class TestEpanetConfig:
    """Tests pour le modèle EpanetConfig."""
    
    def test_config_valide(self):
        """Test d'une configuration EPANET valide."""
        config = EpanetConfig(
            duration_h=24,
            timestep_min=60,
            start_time="00:00",
            quality_type="none",
            save_hydraulics=True,
            save_quality=False,
            save_energy=True
        )
        
        assert config.duration_h == 24
        assert config.timestep_min == 60
        assert config.start_time == "00:00"
        assert config.quality_type == "none"
        assert config.save_hydraulics is True
        assert config.save_quality is False
        assert config.save_energy is True
    
    def test_heure_invalide(self):
        """Test d'erreur quand heure de début invalide."""
        with pytest.raises(ValueError):
            EpanetConfig(
                duration_h=24,
                timestep_min=60,
                start_time="25:00",  # Heure invalide !
                quality_type="none"
            )

class TestValidationFunctions:
    """Tests pour les fonctions de validation."""
    
    def test_valider_reseau_seul(self):
        """Test de validation d'un réseau seul."""
        data = {
            "nom": "Réseau Test",
            "type": "maillé",
            "noeuds": {
                "N1": {
                    "role": "reservoir",
                    "cote_m": 200.0,
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                },
                "N2": {
                    "role": "consommation",
                    "cote_m": 150.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {
                "C1": {
                    "noeud_amont": "N1",
                    "noeud_aval": "N2",
                    "longueur_m": 500.0,
                    "diametre_m": 0.2,
                    "rugosite": 100.0,
                    "materiau": "acier"
                }
            }
        }
        
        reseau = valider_reseau_seul(data)
        assert isinstance(reseau, ReseauCompletConfig)
        assert reseau.nom == "Réseau Test"
    
    def test_valider_reseau_invalide(self):
        """Test d'erreur de validation d'un réseau invalide."""
        data = {
            "nom": "Réseau Test",
            "type": "maillé",
            "noeuds": {
                "N1": {
                    "role": "consommation",  # Pas de réservoir !
                    "cote_m": 150.0,
                    "demande_m3_s": 0.02,
                    "pression_min_mce": 20,
                    "pression_max_mce": 80
                }
            },
            "conduites": {}
        }
        
        with pytest.raises(ValueError, match="Le réseau doit contenir au moins un réservoir"):
            valider_reseau_seul(data)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
