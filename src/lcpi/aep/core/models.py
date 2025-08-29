"""
Modèles Pydantic pour le module AEP.
Définit les structures de données pour la validation et la sérialisation.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum

# =============================================================================
# ENUMS ET CONSTANTES
# =============================================================================

class TypeConsommation(str, Enum):
    """Types de consommation d'eau."""
    BRANCHEMENT_PRIVE = "branchement_prive"
    BORNE_FONTAINE = "borne_fontaine"
    INDUSTRIEL = "industriel"
    COMMERCIAL = "commercial"
    PUBLIC = "public"

class MethodeProjection(str, Enum):
    """Méthodes de projection démographique."""
    MALTHUS = "malthus"
    ARITHMETIQUE = "arithmetique"
    GEOMETRIQUE = "geometrique"
    LOGISTIQUE = "logistique"

class MethodeCalcul(str, Enum):
    """Méthodes de calcul hydraulique."""
    DARCY_WEISBACH = "darcy_weisbach"
    HAZEN_WILLIAMS = "hazen_williams"
    MANNING = "manning"

class TypeReservoir(str, Enum):
    """Types de réservoir."""
    CYLINDRIQUE = "cylindrique"
    PARALLELEPIPEDIQUE = "parallelepipedique"
    SPHERIQUE = "spherique"

class TypeAdduction(str, Enum):
    """Types d'adduction."""
    CONTINUE = "continue"
    DISCONTINUE = "discontinue"

# =============================================================================
# MODÈLES DE BASE
# =============================================================================

class PopulationData(BaseModel):
    """Données de base pour les calculs démographiques."""
    population_base: int = Field(..., gt=0, description="Population de base")
    taux_croissance: float = Field(default=0.037, ge=0, le=0.1, description="Taux de croissance annuel")
    annees_projection: int = Field(default=20, ge=1, le=100, description="Nombre d'années de projection")
    methode: MethodeProjection = Field(default=MethodeProjection.MALTHUS, description="Méthode de projection")
    
    class Config:
        schema_extra = {
            "example": {
                "population_base": 1000,
                "taux_croissance": 0.037,
                "annees_projection": 20,
                "methode": "malthus"
            }
        }

class DemandeData(BaseModel):
    """Données pour le calcul de la demande en eau."""
    population: int = Field(..., gt=0, description="Population")
    dotation_l_hab_j: float = Field(default=150, ge=50, le=300, description="Dotation en L/hab/j")
    coefficient_pointe: float = Field(default=1.5, ge=1.0, le=3.0, description="Coefficient de pointe")
    type_consommation: TypeConsommation = Field(default=TypeConsommation.BRANCHEMENT_PRIVE, description="Type de consommation")
    
    class Config:
        schema_extra = {
            "example": {
                "population": 1000,
                "dotation_l_hab_j": 150,
                "coefficient_pointe": 1.5,
                "type_consommation": "branchement_prive"
            }
        }

class NetworkData(BaseModel):
    """Données pour le dimensionnement de réseau."""
    debit_m3s: float = Field(..., gt=0, description="Débit en m³/s")
    longueur_m: float = Field(default=1000, gt=0, description="Longueur en mètres")
    materiau: str = Field(default="fonte", description="Matériau de la conduite")
    perte_charge_max_m: float = Field(default=10.0, gt=0, description="Perte de charge maximale en m")
    methode: MethodeCalcul = Field(default=MethodeCalcul.DARCY_WEISBACH, description="Méthode de calcul")
    
    class Config:
        schema_extra = {
            "example": {
                "debit_m3s": 0.1,
                "longueur_m": 1000,
                "materiau": "fonte",
                "perte_charge_max_m": 10.0,
                "methode": "darcy_weisbach"
            }
        }

class ReservoirData(BaseModel):
    """Données pour le dimensionnement de réservoir."""
    volume_journalier_m3: float = Field(..., gt=0, description="Volume journalier en m³")
    type_adduction: TypeAdduction = Field(default=TypeAdduction.CONTINUE, description="Type d'adduction")
    forme_reservoir: TypeReservoir = Field(default=TypeReservoir.CYLINDRIQUE, description="Forme du réservoir")
    type_zone: str = Field(default="ville_francaise_peu_importante", description="Type de zone")
    
    class Config:
        schema_extra = {
            "example": {
                "volume_journalier_m3": 1000,
                "type_adduction": "continue",
                "forme_reservoir": "cylindrique",
                "type_zone": "ville_francaise_peu_importante"
            }
        }

class PumpingData(BaseModel):
    """Données pour le dimensionnement de pompage."""
    debit_m3h: float = Field(..., gt=0, description="Débit en m³/h")
    hmt_m: float = Field(..., gt=0, description="Hauteur manométrique totale en m")
    type_pompe: str = Field(default="centrifuge", description="Type de pompe")
    rendement_pompe: float = Field(default=0.75, ge=0.1, le=0.95, description="Rendement de la pompe")
    
    class Config:
        schema_extra = {
            "example": {
                "debit_m3h": 100,
                "hmt_m": 50,
                "type_pompe": "centrifuge",
                "rendement_pompe": 0.75
            }
        }

# =============================================================================
# MODÈLES DE RÉSULTATS
# =============================================================================

class PopulationResult(BaseModel):
    """Résultats d'une projection démographique."""
    population_initiale: int
    population_finale: int
    taux_croissance: float
    methode_utilisee: str
    projections_annuelles: List[Dict[str, Union[int, float]]]
    statistiques: Dict[str, float]
    
    class Config:
        schema_extra = {
            "example": {
                "population_initiale": 1000,
                "population_finale": 2100,
                "taux_croissance": 0.037,
                "methode_utilisee": "malthus",
                "projections_annuelles": [
                    {"annee": 0, "population": 1000, "accroissement": 0},
                    {"annee": 1, "population": 1037, "accroissement": 37}
                ],
                "statistiques": {"accroissement_total": 1100, "accroissement_moyen": 55}
            }
        }

class DemandeResult(BaseModel):
    """Résultats du calcul de demande en eau."""
    population: int
    dotation_l_hab_j: float
    demande_moyenne_m3j: float
    demande_pointe_m3j: float
    demande_pointe_m3s: float
    coefficient_pointe: float
    type_consommation: str
    
    class Config:
        schema_extra = {
            "example": {
                "population": 1000,
                "dotation_l_hab_j": 150,
                "demande_moyenne_m3j": 150.0,
                "demande_pointe_m3j": 225.0,
                "demande_pointe_m3s": 0.0026,
                "coefficient_pointe": 1.5,
                "type_consommation": "branchement_prive"
            }
        }

class NetworkResult(BaseModel):
    """Résultats du dimensionnement de réseau."""
    debit_m3s: float
    diametre_m: float
    vitesse_ms: float
    perte_charge_m: float
    materiau: str
    methode_calcul: str
    parametres_calcul: Dict[str, Any]
    
    class Config:
        schema_extra = {
            "example": {
                "debit_m3s": 0.1,
                "diametre_m": 0.25,
                "vitesse_ms": 2.04,
                "perte_charge_m": 8.5,
                "materiau": "fonte",
                "methode_calcul": "darcy_weisbach",
                "parametres_calcul": {"lambda": 0.02, "longueur": 1000}
            }
        }

class ReservoirResult(BaseModel):
    """Résultats du dimensionnement de réservoir."""
    volume_journalier_m3: float
    volume_utile_m3: float
    volume_total_m3: float
    hauteur_m: float
    diametre_m: Optional[float]
    surface_m2: float
    type_adduction: str
    forme_reservoir: str
    
    class Config:
        schema_extra = {
            "example": {
                "volume_journalier_m3": 1000,
                "volume_utile_m3": 1200,
                "volume_total_m3": 1500,
                "hauteur_m": 4.5,
                "diametre_m": 20.6,
                "surface_m2": 333.3,
                "type_adduction": "continue",
                "forme_reservoir": "cylindrique"
            }
        }

class PumpingResult(BaseModel):
    """Résultats du dimensionnement de pompage."""
    debit_m3h: float
    hmt_m: float
    puissance_hydraulique_kw: float
    puissance_electrique_kw: float
    puissance_groupe_kva: float
    energie_journaliere_kwh: float
    cout_journalier_fcfa: float
    type_pompe: str
    rendement_pompe: float
    
    class Config:
        schema_extra = {
            "example": {
                "debit_m3h": 100,
                "hmt_m": 50,
                "puissance_hydraulique_kw": 13.6,
                "puissance_electrique_kw": 18.1,
                "puissance_groupe_kva": 21.7,
                "energie_journaliere_kwh": 434.4,
                "cout_journalier_fcfa": 6516.0,
                "type_pompe": "centrifuge",
                "rendement_pompe": 0.75
            }
        }

# =============================================================================
# MODÈLES POUR L'ANALYSE DE SCÉNARIOS
# =============================================================================

class ScenarioOverride(BaseModel):
    """Override de paramètres pour un scénario spécifique."""
    nom: str
    description: str
    parametres: Dict[str, Any]
    priorite: int = Field(default=1, ge=1, le=10, description="Priorité du scénario (1-10)")
    
    class Config:
        schema_extra = {
            "example": {
                "nom": "scenario_optimiste",
                "description": "Croissance démographique optimiste avec augmentation des dotations",
                "parametres": {
                    "taux_croissance": 0.045,
                    "dotation_l_hab_j": 180,
                    "coefficient_pointe": 1.8
                },
                "priorite": 3
            }
        }

class ScenarioAnalysis(BaseModel):
    """Configuration pour l'analyse de scénarios multiples."""
    scenarios: List[ScenarioOverride]
    criteres_comparaison: List[str] = Field(
        default=["cout_total", "performance_hydraulique", "energie_consommee"],
        description="Critères de comparaison entre scénarios"
    )
    format_sortie: str = Field(default="tableau", description="Format de sortie (tableau/graphique)")
    
    class Config:
        schema_extra = {
            "example": {
                "scenarios": [
                    {
                        "nom": "scenario_base",
                        "description": "Scénario de référence",
                        "parametres": {},
                        "priorite": 5
                    },
                    {
                        "nom": "scenario_optimiste",
                        "description": "Croissance optimiste",
                        "parametres": {"taux_croissance": 0.045},
                        "priorite": 3
                    }
                ],
                "criteres_comparaison": ["cout_total", "performance_hydraulique"],
                "format_sortie": "tableau"
            }
        }

class ScenarioResult(BaseModel):
    """Résultat d'un scénario individuel."""
    nom_scenario: str
    description: str
    parametres_appliques: Dict[str, Any]
    resultats: Dict[str, Any]
    metriques: Dict[str, float]
    statut: str = Field(default="succes", description="Statut de l'exécution")
    temps_calcul: float = Field(description="Temps de calcul en secondes")
    erreurs: List[str] = Field(default_factory=list, description="Erreurs éventuelles")
    
    class Config:
        schema_extra = {
            "example": {
                "nom_scenario": "scenario_base",
                "description": "Scénario de référence",
                "parametres_appliques": {"taux_croissance": 0.037},
                "resultats": {"population_finale": 1500, "demande_totale": 225.0},
                "metriques": {"cout_total": 450000.0, "performance_hydraulique": 0.85},
                "statut": "succes",
                "temps_calcul": 2.5,
                "erreurs": []
            }
        }

class ScenarioComparison(BaseModel):
    """Résultats comparatifs de tous les scénarios."""
    nom_analyse: str
    date_analyse: datetime
    scenarios_analyses: List[ScenarioResult]
    tableau_comparatif: Dict[str, List[Any]]
    graphiques: Dict[str, str] = Field(default_factory=dict, description="Chemins vers les graphiques générés")
    recommandations: List[str] = Field(default_factory=list, description="Recommandations basées sur l'analyse")
    
    class Config:
        schema_extra = {
            "example": {
                "nom_analyse": "Analyse_scenarios_projet_AEP",
                "date_analyse": "2025-08-16T10:00:00",
                "scenarios_analyses": [],
                "tableau_comparatif": {
                    "scenarios": ["Base", "Optimiste", "Pessimiste"],
                    "cout_total": [450000, 520000, 380000],
                    "performance": [0.85, 0.88, 0.82]
                },
                "graphiques": {
                    "comparaison_couts": "graphs/couts_comparaison.png",
                    "evolution_performance": "graphs/performance_evolution.png"
                },
                "recommandations": [
                    "Le scénario optimiste offre le meilleur rapport qualité-prix",
                    "Considérer une approche hybride entre base et optimiste"
                ]
            }
        }

# =============================================================================
# MODÈLES POUR L'OPTIMISATION
# =============================================================================

class DiametreCommercial(BaseModel):
    """Diamètre commercial disponible."""
    diametre_mm: int = Field(..., gt=0, description="Diamètre en millimètres")
    cout_fcfa_m: float = Field(..., gt=0, description="Coût par mètre en FCFA")
    disponibilite: float = Field(default=1.0, ge=0, le=1, description="Disponibilité du diamètre")
    
    class Config:
        schema_extra = {
            "example": {
                "diametre_mm": 110,
                "cout_fcfa_m": 45,
                "disponibilite": 0.95
            }
        }

class CriteresOptimisation(BaseModel):
    """Critères d'optimisation."""
    principal: str = Field(default="cout", description="Critère principal")
    secondaires: List[str] = Field(default_factory=list, description="Critères secondaires")
    poids: List[float] = Field(default_factory=list, description="Poids des critères")
    
    @validator('poids')
    def poids_sum_to_one(cls, v):
        if v and abs(sum(v) - 1.0) > 0.01:
            raise ValueError("La somme des poids doit être égale à 1.0")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "principal": "cout",
                "secondaires": ["energie", "performance"],
                "poids": [0.6, 0.25, 0.15]
            }
        }

class ContraintesBudget(BaseModel):
    """Contraintes budgétaires."""
    cout_max_fcfa: float = Field(default=500000, gt=0, description="Coût maximum en FCFA")
    cout_par_metre_max: float = Field(default=500, gt=0, description="Coût maximum par mètre")
    
    class Config:
        schema_extra = {
            "example": {
                "cout_max_fcfa": 500000,
                "cout_par_metre_max": 500
            }
        }

class ContraintesTechniques(BaseModel):
    """Contraintes techniques."""
    pression_min_mce: float = Field(default=20.0, gt=0, description="Pression minimale en mCE")
    pression_max_mce: float = Field(default=80.0, gt=0, description="Pression maximale en mCE")
    vitesse_min_m_s: float = Field(default=0.5, gt=0, description="Vitesse minimale en m/s")
    vitesse_max_m_s: float = Field(default=2.5, gt=0, description="Vitesse maximale en m/s")
    
    class Config:
        schema_extra = {
            "example": {
                "pression_min_mce": 20.0,
                "pression_max_mce": 80.0,
                "vitesse_min_m_s": 0.5,
                "vitesse_max_m_s": 2.5
            }
        }

class ParametresAlgorithme(BaseModel):
    """Paramètres de l'algorithme d'optimisation."""
    type: str = Field(default="genetique", description="Type d'algorithme")
    population_size: int = Field(default=100, ge=20, le=1000, description="Taille de la population")
    generations: int = Field(default=50, ge=10, le=500, description="Nombre de générations")
    mutation_rate: float = Field(default=0.1, ge=0.01, le=0.5, description="Taux de mutation")
    crossover_rate: float = Field(default=0.8, ge=0.5, le=0.95, description="Taux de croisement")
    tolerance: float = Field(default=1e-6, ge=1e-8, le=1e-3, description="Tolérance de convergence")
    
    class Config:
        schema_extra = {
            "example": {
                "type": "genetique",
                "population_size": 100,
                "generations": 50,
                "mutation_rate": 0.1,
                "crossover_rate": 0.8,
                "tolerance": 1e-6
            }
        }

class ConfigurationOptimisation(BaseModel):
    """Configuration complète pour l'optimisation."""
    criteres: CriteresOptimisation
    contraintes_budget: ContraintesBudget
    contraintes_techniques: ContraintesTechniques
    algorithme: ParametresAlgorithme
    diametres_candidats: List[DiametreCommercial]
    
    class Config:
        schema_extra = {
            "example": {
                "criteres": {
                    "principal": "cout",
                    "secondaires": ["energie", "performance"],
                    "poids": [0.6, 0.25, 0.15]
                },
                "contraintes_budget": {
                    "cout_max_fcfa": 100000,
                    "cout_par_metre_max": 150
                },
                "contraintes_techniques": {
                    "pression_min_mce": 20.0,
                    "pression_max_mce": 80.0,
                    "vitesse_min_m_s": 0.5,
                    "vitesse_max_m_s": 2.5
                },
                "algorithme": {
                    "type": "genetique",
                    "population_size": 100,
                    "generations": 50,
                    "mutation_rate": 0.1,
                    "crossover_rate": 0.8,
                    "tolerance": 1e-6
                },
                "diametres_candidats": [
                    {"diametre_mm": 90, "cout_fcfa_m": 35, "disponibilite": 0.95},
                    {"diametre_mm": 110, "cout_fcfa_m": 45, "disponibilite": 0.95}
                ]
            }
        }

# =============================================================================
# MODÈLES POUR LA JOURNALISATION
# =============================================================================

class TransparenceMathematique(BaseModel):
    """Informations de transparence mathématique."""
    formule_utilisee: str
    parametres: Dict[str, float]
    etapes_calcul: List[str]
    references: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "formule_utilisee": "P = ρgQH",
                "parametres": {"ρ": 1000, "g": 9.81, "Q": 0.1, "H": 50},
                "etapes_calcul": ["Calcul puissance hydraulique", "Application formule P = ρgQH"],
                "references": ["Manuel hydraulique", "Norme EN 805"]
            }
        }

class LogEntryModel(BaseModel):
    """Modèle pour les entrées de journalisation."""
    id: str
    timestamp: datetime
    titre_calcul: str
    commande_executee: str
    donnees_resultat: Dict[str, Any]
    projet_dir: str
    parametres_entree: Dict[str, Any]
    transparence_mathematique: List[TransparenceMathematique]
    version_algorithme: str
    hash_donnees_entree: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": "20250816_100000",
                "timestamp": "2025-08-16T10:00:00",
                "titre_calcul": "Dimensionnement réseau unifié",
                "commande_executee": "lcpi aep network-unified 0.1 --longueur 1000",
                "donnees_resultat": {"diametre": 0.25, "vitesse": 2.04},
                "projet_dir": "/path/to/project",
                "parametres_entree": {"debit": 0.1, "longueur": 1000},
                "transparence_mathematique": [],
                "version_algorithme": "2.1.0",
                "hash_donnees_entree": "abc123..."
            }
        }

