"""
Gestion dynamique des constantes et références locales AEP

Ce module permet d'ajouter et gérer dynamiquement les constantes,
dotations et références locales selon les besoins des ingénieurs.
"""

import json
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml

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
        validateur: str = "utilisateur"
    ) -> bool:
        """
        Ajoute une nouvelle référence locale
        
        Args:
            nom: Nom de la référence
            valeur: Valeur de la référence
            unite: Unité de mesure
            source: Source de la référence
            description: Description détaillée
            validateur: Nom du validateur
            
        Returns:
            True si ajouté avec succès, False sinon
        """
        from datetime import datetime
        
        if nom in self.references_locales:
            print(f"La référence '{nom}' existe déjà")
            return False
        
        reference = ReferenceLocale(
            nom=nom,
            valeur=valeur,
            unite=unite,
            source=source,
            description=description,
            date_creation=datetime.now().isoformat(),
            validateur=validateur,
            statut="propose"
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
            self.references_locales[nom].statut = "valide"
            self.references_locales[nom].validateur = validateur
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
    
    def importer_configuration(self, fichier_config: str) -> bool:
        """
        Importe une configuration depuis un fichier
        
        Args:
            fichier_config: Chemin vers le fichier de configuration
            
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
            
            # Importer les références
            if "references_locales" in config:
                for k, v in config["references_locales"].items():
                    self.references_locales[k] = ReferenceLocale(**v)
            
            # Importer les dotations
            if "dotations_locales" in config:
                for k, v in config["dotations_locales"].items():
                    self.dotations_locales[k] = DotationLocale(**v)
            
            # Importer les coefficients
            if "coefficients_locaux" in config:
                for k, v in config["coefficients_locaux"].items():
                    self.coefficients_locaux[k] = CoefficientLocal(**v)
            
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
                "proposees": len([r for r in self.references_locales.values() if r.statut == "propose"]),
                "depreciees": len([r for r in self.references_locales.values() if r.statut == "deprecie"])
            },
            "dotations_locales": {
                "total": len(self.dotations_locales),
                "validees": len(self.obtenir_dotations_validees()),
                "proposees": len([d for d in self.dotations_locales.values() if d.statut == "propose"]),
                "depreciees": len([d for d in self.dotations_locales.values() if d.statut == "deprecie"])
            },
            "coefficients_locaux": {
                "total": len(self.coefficients_locaux),
                "valides": len(self.obtenir_coefficients_valides()),
                "proposes": len([c for c in self.coefficients_locaux.values() if c.statut == "propose"]),
                "deprecies": len([c for c in self.coefficients_locaux.values() if c.statut == "deprecie"])
            }
        }
