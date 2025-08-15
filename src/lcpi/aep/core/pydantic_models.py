"""
Modèles Pydantic pour la validation des données AEP.
Assure une validation robuste et des messages d'erreur clairs.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, List, Optional, Union, Any
from enum import Enum

class NoeudRole(str, Enum):
    """Rôles possibles pour un nœud."""
    RESERVOIR = "reservoir"
    CONSOMMATION = "consommation"
    JONCTION = "jonction"

class TypeReseau(str, Enum):
    """Types de réseau possibles."""
    MAILLE = "maillé"
    RAMIFIE = "ramifié"

class CoefficientFrottement(str, Enum):
    """Types de coefficients de frottement."""
    HAZEN_WILLIAMS = "hazen_williams"
    DARCY_WEISBACH = "darcy_weisbach"

class NoeudUnified(BaseModel):
    """Modèle pour un nœud du réseau."""
    role: NoeudRole = Field(..., description="Rôle du nœud")
    cote_m: float = Field(..., gt=0, description="Cote en mètres")
    demande_m3_s: float = Field(0.0, ge=0, description="Demande en m³/s")
    pression_min_mce: int = Field(20, gt=0, le=100, description="Pression minimale en mCE")
    pression_max_mce: int = Field(80, gt=0, le=200, description="Pression maximale en mCE")
    profil_consommation: Optional[str] = Field("residential", description="Profil de consommation")
    
    @field_validator('pression_max_mce')
    @classmethod
    def pression_max_superieure_min(cls, v, info):
        """Vérifie que la pression max est supérieure à la pression min."""
        if info.data and 'pression_min_mce' in info.data and v <= info.data['pression_min_mce']:
            raise ValueError('Pression max doit être > pression min')
        return v
    
    @field_validator('demande_m3_s')
    @classmethod
    def demande_positive_pour_consommation(cls, v, info):
        """Vérifie que les nœuds de consommation ont une demande positive."""
        if info.data and info.data.get('role') == NoeudRole.CONSOMMATION and v <= 0:
            raise ValueError('Les nœuds de consommation doivent avoir une demande > 0')
        return v

class ConduiteUnified(BaseModel):
    """Modèle pour une conduite du réseau."""
    noeud_amont: str = Field(..., description="Nœud amont")
    noeud_aval: str = Field(..., description="Nœud aval")
    longueur_m: float = Field(..., gt=0, description="Longueur en mètres")
    diametre_m: float = Field(..., gt=0, description="Diamètre en mètres")
    rugosite: float = Field(..., gt=0, description="Rugosité")
    materiau: str = Field(..., description="Matériau de la conduite")
    statut: str = Field("existant", description="Statut de la conduite")
    coefficient_frottement: CoefficientFrottement = Field(
        CoefficientFrottement.HAZEN_WILLIAMS, 
        description="Type de coefficient de frottement"
    )
    
    @field_validator('diametre_m')
    @classmethod
    def diametre_raisonnable(cls, v):
        """Vérifie que le diamètre est dans une plage raisonnable."""
        if v < 0.01 or v > 5.0:
            raise ValueError('Diamètre doit être entre 0.01 et 5.0 mètres')
        return v
    
    @field_validator('longueur_m')
    @classmethod
    def longueur_raisonnable(cls, v):
        """Vérifie que la longueur est raisonnable."""
        if v < 1.0 or v > 10000.0:
            raise ValueError('Longueur doit être entre 1 et 10000 mètres')
        return v

class HardyCrossConfig(BaseModel):
    """Configuration pour l'algorithme Hardy-Cross."""
    tolerance: float = Field(1e-6, gt=0, description="Tolérance de convergence")
    max_iterations: int = Field(200, gt=0, le=1000, description="Nombre max d'itérations")
    methode: CoefficientFrottement = Field(
        CoefficientFrottement.HAZEN_WILLIAMS, 
        description="Méthode de calcul"
    )
    convergence_criteria: str = Field("debit", pattern="^(debit|pression)$", description="Critère de convergence")

class EpanetConfig(BaseModel):
    """Configuration pour EPANET."""
    duration_h: int = Field(24, gt=0, le=168, description="Durée de simulation en heures")
    timestep_min: int = Field(60, gt=0, le=1440, description="Pas de temps en minutes")
    start_time: str = Field("00:00", pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", description="Heure de début")
    quality_type: str = Field("none", pattern="^(none|chemical|age|trace)$", description="Type d'analyse qualité")
    save_hydraulics: bool = Field(True, description="Sauvegarder les résultats hydrauliques")
    save_quality: bool = Field(False, description="Sauvegarder les résultats qualité")
    save_energy: bool = Field(True, description="Sauvegarder les résultats énergétiques")

class PostTraitementConfig(BaseModel):
    """Configuration pour le post-traitement."""
    verifications: Dict[str, Any] = Field(default_factory=dict, description="Paramètres de vérification")
    coup_belier: Dict[str, Any] = Field(default_factory=dict, description="Paramètres coup de bélier")
    optimisation: Dict[str, Any] = Field(default_factory=dict, description="Paramètres d'optimisation")

class ReseauCompletConfig(BaseModel):
    """Configuration complète d'un réseau."""
    nom: str = Field(..., min_length=1, description="Nom du réseau")
    type: TypeReseau = Field(..., description="Type de réseau")
    noeuds: Dict[str, NoeudUnified] = Field(..., description="Nœuds du réseau")
    conduites: Dict[str, ConduiteUnified] = Field(..., description="Conduites du réseau")
    boucles: Optional[Dict[str, List[str]]] = Field(None, description="Boucles du réseau")
    hardy_cross: Optional[HardyCrossConfig] = Field(None, description="Configuration Hardy-Cross")
    epanet: Optional[EpanetConfig] = Field(None, description="Configuration EPANET")
    post_traitement: Optional[PostTraitementConfig] = Field(None, description="Configuration post-traitement")
    
    @model_validator(mode='after')
    def valider_connectivite(self):
        """Valide la connectivité du réseau."""
        noeuds = self.noeuds
        conduites = self.conduites
        
        # Vérifier que tous les nœuds référencés dans les conduites existent
        noeuds_conduites = set()
        for conduite in conduites.values():
            noeuds_conduites.add(conduite.noeud_amont)
            noeuds_conduites.add(conduite.noeud_aval)
        
        noeuds_inexistants = noeuds_conduites - set(noeuds.keys())
        if noeuds_inexistants:
            raise ValueError(f"Nœuds référencés dans les conduites mais non définis: {noeuds_inexistants}")
        
        # Vérifier qu'il y a au moins un réservoir
        reservoirs = [n for n in noeuds.values() if n.role == NoeudRole.RESERVOIR]
        if not reservoirs:
            raise ValueError("Le réseau doit contenir au moins un réservoir")
        
        return self
    
    model_config = {
        "extra": "forbid",  # Interdire les champs non définis
        "validate_assignment": True  # Valider lors de l'assignation
    }

class OptimisationConfig(BaseModel):
    """Configuration pour l'optimisation."""
    criteres: Dict[str, Any] = Field(..., description="Critères d'optimisation")
    contraintes: Dict[str, Any] = Field(..., description="Contraintes")
    algorithmes: Dict[str, Any] = Field(..., description="Paramètres des algorithmes")
    diametres_candidats: Dict[str, Any] = Field(..., description="Diamètres candidats")

class AnalyseSensibiliteConfig(BaseModel):
    """Configuration pour l'analyse de sensibilité."""
    parametres: Dict[str, Any] = Field(..., description="Paramètres à analyser")
    sorties: Dict[str, bool] = Field(..., description="Sorties à analyser")
    methodes: List[str] = Field(..., description="Méthodes d'analyse")

class ConfigurationComplete(BaseModel):
    """Configuration complète pour une analyse AEP."""
    reseau_complet: ReseauCompletConfig
    optimisation: Optional[OptimisationConfig] = None
    analyse_sensibilite: Optional[AnalyseSensibiliteConfig] = None
    
    model_config = {
        "extra": "forbid"
    }

# Fonctions utilitaires pour la validation
def valider_fichier_yaml(contenu: Dict[str, Any]) -> ConfigurationComplete:
    """Valide un fichier YAML et retourne une configuration complète."""
    try:
        return ConfigurationComplete(**contenu)
    except Exception as e:
        raise ValueError(f"Erreur de validation YAML: {e}")

def valider_reseau_seul(contenu: Dict[str, Any]) -> ReseauCompletConfig:
    """Valide seulement la section réseau d'un fichier YAML."""
    try:
        return ReseauCompletConfig(**contenu)
    except Exception as e:
        raise ValueError(f"Erreur de validation réseau: {e}")

def exporter_vers_dict(config: ConfigurationComplete) -> Dict[str, Any]:
    """Exporte une configuration vers un dictionnaire."""
    return config.model_dump(exclude_none=True)
