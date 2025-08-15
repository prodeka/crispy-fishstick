"""
Gestion dynamique des constantes et références locales AEP

Ce module permet d'ajouter et gérer dynamiquement les constantes,
dotations et références locales selon les besoins des ingénieurs.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml
from datetime import datetime
from enum import Enum

class StatutElement(Enum):
    """Statuts possibles pour les éléments"""
    PROPOSE = "propose"
    VALIDE = "valide"
    DEPRECIE = "deprecie"

class TypeUtilisateur(Enum):
    """Types d'utilisateurs"""
    UTILISATEUR = "utilisateur"
    VALIDATEUR = "validateur"
    ADMIN = "admin"

class ModeImport(Enum):
    """Modes d'import"""
    REMPLACER = "remplacer"
    FUSION = "fusion"
    METTRE_A_JOUR = "mettre_a_jour"

@dataclass
class ReferenceLocale:
    """Référence locale pour les constantes AEP"""
    nom: str
    valeur: Union[float, int, str]
    unite: str
    source: str
    description: str
    date_creation: str
    validateur: str
    statut: str  # "propose", "valide", "deprecie"
    version: int = 1
    historique: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.historique is None:
            self.historique = []

@dataclass
class DotationLocale:
    """Dotation locale en eau"""
    nom: str
    valeur: float
    unite: str
    type_zone: str
    source: str
    description: str
    conditions: Dict[str, Any]
    date_creation: str
    statut: str
    version: int = 1
    historique: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.historique is None:
            self.historique = []

@dataclass
class CoefficientLocal:
    """Coefficient local"""
    nom: str
    valeur: float
    unite: str
    type_calcul: str
    source: str
    description: str
    conditions: Dict[str, Any]
    date_creation: str
    statut: str
    version: int = 1
    historique: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.historique is None:
            self.historique = []

class AEPDynamicConstantsManager:
    """Gestionnaire des constantes dynamiques AEP"""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".lcpi", "aep", "constants")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Fichiers de configuration
        self.references_file = self.config_dir / "references_locales.json"
        self.dotations_file = self.config_dir / "dotations_locales.json"
        self.coefficients_file = self.config_dir / "coefficients_locaux.json"
        
        # Charger les données existantes
        self.references_locales = self._charger_references()
        self.dotations_locales = self._charger_dotations()
        self.coefficients_locaux = self._charger_coefficients()
        
        # Unités valides
        self.unites_valides = {
            "longueur": ["m", "cm", "mm", "km"],
            "volume": ["m³", "L", "ml", "cm³"],
            "debit": ["m³/h", "L/s", "m³/s"],
            "pression": ["bar", "Pa", "kPa", "mCE"],
            "puissance": ["W", "kW", "MW"],
            "temps": ["s", "min", "h", "j"],
            "sans_unite": ["", "-", "adimensionnel"]
        }
        
        # Types de valeurs valides
        self.types_valeurs_valides = {
            "numerique": [int, float],
            "texte": [str],
            "booleen": [bool]
        }
    
    def _normaliser_nom(self, nom: str) -> str:
        """
        Normalise un nom pour éviter les doublons dus à la casse
        
        Args:
            nom: Nom à normaliser
            
        Returns:
            Nom normalisé
        """
        # Supprimer les espaces en début et fin
        nom = nom.strip()
        # Remplacer les espaces multiples par un seul
        nom = re.sub(r'\s+', ' ', nom)
        # Convertir en minuscules pour la comparaison
        return nom.lower()
    
    def _valider_unite(self, unite: str, type_mesure: str = None) -> bool:
        """
        Valide une unité de mesure
        
        Args:
            unite: Unité à valider
            type_mesure: Type de mesure (optionnel)
            
        Returns:
            True si l'unité est valide
        """
        if type_mesure and type_mesure in self.unites_valides:
            return unite in self.unites_valides[type_mesure]
        
        # Vérifier dans toutes les catégories
        for categories in self.unites_valides.values():
            if unite in categories:
                return True
        
        return False
    
    def _valider_valeur(self, valeur: Any, type_attendu: str = "numerique") -> bool:
        """
        Valide une valeur selon son type attendu
        
        Args:
            valeur: Valeur à valider
            type_attendu: Type attendu
            
        Returns:
            True si la valeur est valide
        """
        if type_attendu not in self.types_valeurs_valides:
            return False
        
        types_valides = self.types_valeurs_valides[type_attendu]
        
        # Vérifier le type
        if not any(isinstance(valeur, t) for t in types_valides):
            return False
        
        # Validations spécifiques
        if type_attendu == "numerique":
            # Vérifier que la valeur n'est pas négative (sauf si c'est explicitement autorisé)
            if isinstance(valeur, (int, float)) and valeur < 0:
                return False
        
        return True
    
    def _ajouter_entree_historique(self, element, action: str, utilisateur: str, details: str = ""):
        """
        Ajoute une entrée dans l'historique d'un élément
        
        Args:
            element: Élément à modifier
            action: Action effectuée
            utilisateur: Utilisateur qui a effectué l'action
            details: Détails supplémentaires
        """
        entree = {
            "date": datetime.now().isoformat(),
            "action": action,
            "utilisateur": utilisateur,
            "details": details,
            "version_precedente": element.version
        }
        element.historique.append(entree)
        element.version += 1
    
    def _charger_references(self) -> Dict[str, ReferenceLocale]:
        """Charge les références locales depuis le fichier"""
        if self.references_file.exists():
            try:
                with open(self.references_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {k: ReferenceLocale(**v) for k, v in data.items()}
            except Exception as e:
                print(f"Erreur lors du chargement des références: {e}")
                return {}
        return {}
    
    def _charger_dotations(self) -> Dict[str, DotationLocale]:
        """Charge les dotations locales depuis le fichier"""
        if self.dotations_file.exists():
            try:
                with open(self.dotations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {k: DotationLocale(**v) for k, v in data.items()}
            except Exception as e:
                print(f"Erreur lors du chargement des dotations: {e}")
                return {}
        return {}
    
    def _charger_coefficients(self) -> Dict[str, CoefficientLocal]:
        """Charge les coefficients locaux depuis le fichier"""
        if self.coefficients_file.exists():
            try:
                with open(self.coefficients_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {k: CoefficientLocal(**v) for k, v in data.items()}
            except Exception as e:
                print(f"Erreur lors du chargement des coefficients: {e}")
                return {}
        return {}
    
    def _sauvegarder_references(self):
        """Sauvegarde les références locales dans le fichier"""
        try:
            with open(self.references_file, 'w', encoding='utf-8') as f:
                json.dump({k: asdict(v) for k, v in self.references_locales.items()}, 
                          f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des références: {e}")
    
    def _sauvegarder_dotations(self):
        """Sauvegarde les dotations locales dans le fichier"""
        try:
            with open(self.dotations_file, 'w', encoding='utf-8') as f:
                json.dump({k: asdict(v) for k, v in self.dotations_locales.items()}, 
                          f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des dotations: {e}")
    
    def _sauvegarder_coefficients(self):
        """Sauvegarde les coefficients locaux dans le fichier"""
        try:
            with open(self.coefficients_file, 'w', encoding='utf-8') as f:
                json.dump({k: asdict(v) for k, v in self.coefficients_locaux.items()}, 
                          f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des coefficients: {e}")
    
    def ajouter_reference_locale(
        self,
        nom: str,
        valeur: Union[float, int, str],
        unite: str,
        source: str,
        description: str,
        validateur: str = "utilisateur",
        type_valeur: str = "numerique"
    ) -> bool:
        """
        Ajoute une nouvelle référence locale avec validation
        
        Args:
            nom: Nom de la référence
            valeur: Valeur de la référence
            unite: Unité de mesure
            source: Source de la référence
            description: Description détaillée
            validateur: Nom du validateur
            type_valeur: Type de valeur attendu
            
        Returns:
            True si ajouté avec succès, False sinon
        """
        # Normaliser le nom
        nom_normalise = self._normaliser_nom(nom)
        
        # Vérifier si la référence existe déjà (insensible à la casse)
        for nom_existant in self.references_locales.keys():
            if self._normaliser_nom(nom_existant) == nom_normalise:
                print(f"La référence '{nom}' existe déjà (insensible à la casse)")
                return False
        
        # Valider la valeur
        if not self._valider_valeur(valeur, type_valeur):
            print(f"Valeur invalide pour le type '{type_valeur}': {valeur}")
            return False
        
        # Valider l'unité
        if not self._valider_unite(unite):
            print(f"Unité non reconnue: {unite}")
            return False
        
        # Créer la référence
        reference = ReferenceLocale(
            nom=nom,
            valeur=valeur,
            unite=unite,
            source=source,
            description=description,
            date_creation=datetime.now().isoformat(),
            validateur=validateur,
            statut=StatutElement.PROPOSE.value
        )
        
        # Ajouter l'entrée d'historique
        self._ajouter_entree_historique(
            reference, 
            "creation", 
            validateur, 
            f"Création de la référence '{nom}'"
        )
        
        self.references_locales[nom] = reference
        self._sauvegarder_references()
        return True
    
    def ajouter_dotation_locale(
        self,
        nom: str,
        valeur: float,
        unite: str,
        type_zone: str,
        source: str,
        description: str,
        conditions: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Ajoute une nouvelle dotation locale
        
        Args:
            nom: Nom de la dotation
            valeur: Valeur de la dotation
            unite: Unité de mesure
            type_zone: Type de zone concernée
            source: Source de la dotation
            description: Description détaillée
            conditions: Conditions d'application
            
        Returns:
            True si ajouté avec succès, False sinon
        """
        from datetime import datetime
        
        if nom in self.dotations_locales:
            print(f"La dotation '{nom}' existe déjà")
            return False
        
        if conditions is None:
            conditions = {}
        
        dotation = DotationLocale(
            nom=nom,
            valeur=valeur,
            unite=unite,
            type_zone=type_zone,
            source=source,
            description=description,
            conditions=conditions,
            date_creation=datetime.now().isoformat(),
            statut="propose"
        )
        
        self.dotations_locales[nom] = dotation
        self._sauvegarder_dotations()
        return True
    
    def ajouter_coefficient_local(
        self,
        nom: str,
        valeur: float,
        unite: str,
        type_calcul: str,
        source: str,
        description: str,
        conditions: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Ajoute un nouveau coefficient local
        
        Args:
            nom: Nom du coefficient
            valeur: Valeur du coefficient
            unite: Unité de mesure
            type_calcul: Type de calcul concerné
            source: Source du coefficient
            description: Description détaillée
            conditions: Conditions d'application
            
        Returns:
            True si ajouté avec succès, False sinon
        """
        from datetime import datetime
        
        if nom in self.coefficients_locaux:
            print(f"Le coefficient '{nom}' existe déjà")
            return False
        
        if conditions is None:
            conditions = {}
        
        coefficient = CoefficientLocal(
            nom=nom,
            valeur=valeur,
            unite=unite,
            type_calcul=type_calcul,
            source=source,
            description=description,
            conditions=conditions,
            date_creation=datetime.now().isoformat(),
            statut="propose"
        )
        
        self.coefficients_locaux[nom] = coefficient
        self._sauvegarder_coefficients()
        return True
    
    def valider_reference(self, nom: str, validateur: str) -> bool:
        """Valide une référence locale"""
        if nom in self.references_locales:
            reference = self.references_locales[nom]
            reference.statut = StatutElement.VALIDE.value
            reference.validateur = validateur
            
            # Ajouter l'entrée d'historique
            self._ajouter_entree_historique(
                reference, 
                "validation", 
                validateur, 
                f"Validation de la référence '{nom}'"
            )
            
            self._sauvegarder_references()
            return True
        return False
    
    def valider_dotation(self, nom: str) -> bool:
        """Valide une dotation locale"""
        if nom in self.dotations_locales:
            self.dotations_locales[nom].statut = "valide"
            self._sauvegarder_dotations()
            return True
        return False
    
    def valider_coefficient(self, nom: str) -> bool:
        """Valide un coefficient local"""
        if nom in self.coefficients_locaux:
            self.coefficients_locaux[nom].statut = "valide"
            self._sauvegarder_coefficients()
            return True
        return False
    
    def deprecie_reference(self, nom: str) -> bool:
        """Marque une référence comme dépréciée"""
        if nom in self.references_locales:
            self.references_locales[nom].statut = "deprecie"
            self._sauvegarder_references()
            return True
        return False
    
    def deprecie_dotation(self, nom: str) -> bool:
        """Marque une dotation comme dépréciée"""
        if nom in self.dotations_locales:
            self.dotations_locales[nom].statut = "deprecie"
            self._sauvegarder_dotations()
            return True
        return False
    
    def deprecie_coefficient(self, nom: str) -> bool:
        """Marque un coefficient comme déprécié"""
        if nom in self.coefficients_locaux:
            self.coefficients_locaux[nom].statut = "deprecie"
            self._sauvegarder_coefficients()
            return True
        return False
    
    def obtenir_references_valides(self) -> Dict[str, ReferenceLocale]:
        """Obtient toutes les références validées"""
        return {k: v for k, v in self.references_locales.items() if v.statut == "valide"}
    
    def obtenir_dotations_validees(self) -> Dict[str, DotationLocale]:
        """Obtient toutes les dotations validées"""
        return {k: v for k, v in self.dotations_locales.items() if v.statut == "valide"}
    
    def obtenir_coefficients_valides(self) -> Dict[str, CoefficientLocal]:
        """Obtient tous les coefficients validés"""
        return {k: v for k, v in self.coefficients_locaux.items() if v.statut == "valide"}
    
    def rechercher_references(self, terme: str) -> List[ReferenceLocale]:
        """Recherche des références par terme"""
        resultats = []
        terme_lower = terme.lower()
        
        for ref in self.references_locales.values():
            if (terme_lower in ref.nom.lower() or 
                terme_lower in ref.description.lower() or
                terme_lower in ref.source.lower()):
                resultats.append(ref)
        
        return resultats
    
    def rechercher_dotations(self, terme: str) -> List[DotationLocale]:
        """Recherche des dotations par terme"""
        resultats = []
        terme_lower = terme.lower()
        
        for dotation in self.dotations_locales.values():
            if (terme_lower in dotation.nom.lower() or 
                terme_lower in dotation.description.lower() or
                terme_lower in dotation.type_zone.lower()):
                resultats.append(dotation)
        
        return resultats
    
    def rechercher_coefficients(self, terme: str) -> List[CoefficientLocal]:
        """Recherche des coefficients par terme"""
        resultats = []
        terme_lower = terme.lower()
        
        for coeff in self.coefficients_locaux.values():
            if (terme_lower in coeff.nom.lower() or 
                terme_lower in coeff.description.lower() or
                terme_lower in coeff.type_calcul.lower()):
                resultats.append(coeff)
        
        return resultats
    
    def exporter_configuration(self, format_sortie: str = "json") -> str:
        """
        Exporte la configuration complète
        
        Args:
            format_sortie: Format de sortie (json, yaml)
            
        Returns:
            Configuration formatée
        """
        config = {
            "references_locales": {k: asdict(v) for k, v in self.references_locales.items()},
            "dotations_locales": {k: asdict(v) for k, v in self.dotations_locales.items()},
            "coefficients_locaux": {k: asdict(v) for k, v in self.coefficients_locaux.items()}
        }
        
        if format_sortie == "json":
            return json.dumps(config, indent=2, ensure_ascii=False)
        elif format_sortie == "yaml":
            return yaml.dump(config, default_flow_style=False, allow_unicode=True)
        else:
            raise ValueError(f"Format de sortie non supporté: {format_sortie}")
    
    def importer_configuration(
        self, 
        fichier_config: str, 
        mode: ModeImport = ModeImport.REMPLACER,
        utilisateur: str = "import"
    ) -> bool:
        """
        Importe une configuration depuis un fichier avec gestion des conflits
        
        Args:
            fichier_config: Chemin vers le fichier de configuration
            mode: Mode d'import (remplacer, fusion, mettre_a_jour)
            utilisateur: Utilisateur effectuant l'import
            
        Returns:
            True si importé avec succès, False sinon
        """
        try:
            with open(fichier_config, 'r', encoding='utf-8') as f:
                if fichier_config.endswith('.json'):
                    config = json.load(f)
                elif fichier_config.endswith('.yaml') or fichier_config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    print("Format de fichier non supporté")
                    return False
            
            conflits = []
            
            # Importer les références
            if "references_locales" in config:
                for k, v in config["references_locales"].items():
                    if k in self.references_locales:
                        if mode == ModeImport.REMPLACER:
                            # Remplacer complètement
                            self.references_locales[k] = ReferenceLocale(**v)
                            self._ajouter_entree_historique(
                                self.references_locales[k], 
                                "remplacement_import", 
                                utilisateur, 
                                f"Remplacement par import de '{k}'"
                            )
                        elif mode == ModeImport.FUSION:
                            # Fusionner les données
                            conflits.append(f"Conflit de fusion pour référence '{k}'")
                            continue
                        elif mode == ModeImport.METTRE_A_JOUR:
                            # Mettre à jour seulement si plus récent
                            if v.get("version", 0) > self.references_locales[k].version:
                                self.references_locales[k] = ReferenceLocale(**v)
                                self._ajouter_entree_historique(
                                    self.references_locales[k], 
                                    "mise_a_jour_import", 
                                    utilisateur, 
                                    f"Mise à jour par import de '{k}'"
                                )
                    else:
                        # Nouvel élément
                        self.references_locales[k] = ReferenceLocale(**v)
                        self._ajouter_entree_historique(
                            self.references_locales[k], 
                            "creation_import", 
                            utilisateur, 
                            f"Création par import de '{k}'"
                        )
            
            # Importer les dotations (même logique)
            if "dotations_locales" in config:
                for k, v in config["dotations_locales"].items():
                    if k in self.dotations_locales:
                        if mode == ModeImport.REMPLACER:
                            self.dotations_locales[k] = DotationLocale(**v)
                        elif mode == ModeImport.FUSION:
                            conflits.append(f"Conflit de fusion pour dotation '{k}'")
                            continue
                        elif mode == ModeImport.METTRE_A_JOUR:
                            if v.get("version", 0) > self.dotations_locales[k].version:
                                self.dotations_locales[k] = DotationLocale(**v)
                    else:
                        self.dotations_locales[k] = DotationLocale(**v)
            
            # Importer les coefficients (même logique)
            if "coefficients_locaux" in config:
                for k, v in config["coefficients_locaux"].items():
                    if k in self.coefficients_locaux:
                        if mode == ModeImport.REMPLACER:
                            self.coefficients_locaux[k] = CoefficientLocal(**v)
                        elif mode == ModeImport.FUSION:
                            conflits.append(f"Conflit de fusion pour coefficient '{k}'")
                            continue
                        elif mode == ModeImport.METTRE_A_JOUR:
                            if v.get("version", 0) > self.coefficients_locaux[k].version:
                                self.coefficients_locaux[k] = CoefficientLocal(**v)
                    else:
                        self.coefficients_locaux[k] = CoefficientLocal(**v)
            
            # Afficher les conflits
            if conflits:
                print("Conflits détectés lors de l'import:")
                for conflit in conflits:
                    print(f"  - {conflit}")
            
            # Sauvegarder
            self._sauvegarder_references()
            self._sauvegarder_dotations()
            self._sauvegarder_coefficients()
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'import: {e}")
            return False
    
    def generer_rapport_statut(self) -> Dict[str, Any]:
        """Génère un rapport de statut des constantes locales"""
        return {
            "references_locales": {
                "total": len(self.references_locales),
                "validees": len(self.obtenir_references_valides()),
                "proposees": len([r for r in self.references_locales.values() if r.statut == StatutElement.PROPOSE.value]),
                "depreciees": len([r for r in self.references_locales.values() if r.statut == StatutElement.DEPRECIE.value])
            },
            "dotations_locales": {
                "total": len(self.dotations_locales),
                "validees": len(self.obtenir_dotations_validees()),
                "proposees": len([d for d in self.dotations_locales.values() if d.statut == StatutElement.PROPOSE.value]),
                "depreciees": len([d for d in self.dotations_locales.values() if d.statut == StatutElement.DEPRECIE.value])
            },
            "coefficients_locaux": {
                "total": len(self.coefficients_locaux),
                "valides": len(self.obtenir_coefficients_valides()),
                "proposes": len([c for c in self.coefficients_locaux.values() if c.statut == StatutElement.PROPOSE.value]),
                "deprecies": len([c for c in self.coefficients_locaux.values() if c.statut == StatutElement.DEPRECIE.value])
            }
        }
    
    def obtenir_historique_element(self, nom: str, type_element: str = "reference") -> List[Dict[str, Any]]:
        """
        Obtient l'historique complet d'un élément
        
        Args:
            nom: Nom de l'élément
            type_element: Type d'élément ("reference", "dotation", "coefficient")
            
        Returns:
            Liste des entrées d'historique
        """
        if type_element == "reference" and nom in self.references_locales:
            return self.references_locales[nom].historique
        elif type_element == "dotation" and nom in self.dotations_locales:
            return self.dotations_locales[nom].historique
        elif type_element == "coefficient" and nom in self.coefficients_locaux:
            return self.coefficients_locaux[nom].historique
        else:
            return []
    
    def obtenir_statistiques_utilisateur(self, utilisateur: str) -> Dict[str, Any]:
        """
        Obtient les statistiques d'un utilisateur
        
        Args:
            utilisateur: Nom de l'utilisateur
            
        Returns:
            Statistiques de l'utilisateur
        """
        stats = {
            "references_crees": 0,
            "references_validees": 0,
            "dotations_crees": 0,
            "dotations_validees": 0,
            "coefficients_crees": 0,
            "coefficients_valides": 0,
            "actions_total": 0
        }
        
        # Compter les créations
        for ref in self.references_locales.values():
            if ref.validateur == utilisateur:
                stats["references_crees"] += 1
                if ref.statut == StatutElement.VALIDE.value:
                    stats["references_validees"] += 1
        
        for dot in self.dotations_locales.values():
            if dot.statut == StatutElement.VALIDE.value:
                stats["dotations_validees"] += 1
        
        for coeff in self.coefficients_locaux.values():
            if coeff.statut == StatutElement.VALIDE.value:
                stats["coefficients_valides"] += 1
        
        # Compter les actions dans l'historique
        for ref in self.references_locales.values():
            for entree in ref.historique:
                if entree["utilisateur"] == utilisateur:
                    stats["actions_total"] += 1
        
        return stats
    
    def rechercher_par_utilisateur(self, utilisateur: str) -> Dict[str, List]:
        """
        Recherche tous les éléments créés ou modifiés par un utilisateur
        
        Args:
            utilisateur: Nom de l'utilisateur
            
        Returns:
            Dictionnaire avec les éléments trouvés
        """
        resultats = {
            "references": [],
            "dotations": [],
            "coefficients": []
        }
        
        # Rechercher dans les références
        for ref in self.references_locales.values():
            if ref.validateur == utilisateur:
                resultats["references"].append(ref)
        
        # Rechercher dans l'historique
        for ref in self.references_locales.values():
            for entree in ref.historique:
                if entree["utilisateur"] == utilisateur:
                    resultats["references"].append(ref)
                    break
        
        return resultats
    
    def exporter_historique_complet(self, format_sortie: str = "json") -> str:
        """
        Exporte l'historique complet de tous les éléments
        
        Args:
            format_sortie: Format de sortie (json, yaml)
            
        Returns:
            Historique formaté
        """
        historique = {
            "date_export": datetime.now().isoformat(),
            "references": {
                nom: {
                    "element": asdict(ref),
                    "historique": ref.historique
                }
                for nom, ref in self.references_locales.items()
            },
            "dotations": {
                nom: {
                    "element": asdict(dot),
                    "historique": dot.historique
                }
                for nom, dot in self.dotations_locales.items()
            },
            "coefficients": {
                nom: {
                    "element": asdict(coeff),
                    "historique": coeff.historique
                }
                for nom, coeff in self.coefficients_locaux.items()
            }
        }
        
        if format_sortie == "json":
            return json.dumps(historique, indent=2, ensure_ascii=False)
        elif format_sortie == "yaml":
            return yaml.dump(historique, default_flow_style=False, allow_unicode=True)
        else:
            raise ValueError(f"Format de sortie non supporté: {format_sortie}")
    
    def nettoyer_historique(self, jours_max: int = 365) -> int:
        """
        Nettoie l'historique ancien pour économiser l'espace
        
        Args:
            jours_max: Nombre maximum de jours à conserver
            
        Returns:
            Nombre d'entrées supprimées
        """
        date_limite = datetime.now().timestamp() - (jours_max * 24 * 3600)
        suppressions = 0
        
        for ref in self.references_locales.values():
            historique_nettoye = []
            for entree in ref.historique:
                try:
                    date_entree = datetime.fromisoformat(entree["date"]).timestamp()
                    if date_entree > date_limite:
                        historique_nettoye.append(entree)
                    else:
                        suppressions += 1
                except:
                    historique_nettoye.append(entree)  # Garder si erreur de parsing
            ref.historique = historique_nettoye
        
        # Même logique pour dotations et coefficients
        for dot in self.dotations_locales.values():
            historique_nettoye = []
            for entree in dot.historique:
                try:
                    date_entree = datetime.fromisoformat(entree["date"]).timestamp()
                    if date_entree > date_limite:
                        historique_nettoye.append(entree)
                    else:
                        suppressions += 1
                except:
                    historique_nettoye.append(entree)
            dot.historique = historique_nettoye
        
        for coeff in self.coefficients_locaux.values():
            historique_nettoye = []
            for entree in coeff.historique:
                try:
                    date_entree = datetime.fromisoformat(entree["date"]).timestamp()
                    if date_entree > date_limite:
                        historique_nettoye.append(entree)
                    else:
                        suppressions += 1
                except:
                    historique_nettoye.append(entree)
            coeff.historique = historique_nettoye
        
        # Sauvegarder les modifications
        self._sauvegarder_references()
        self._sauvegarder_dotations()
        self._sauvegarder_coefficients()
        
        return suppressions
