"""
Mappings YAML ↔ CSV pour LCPI-CLI
Définit les conversions spécifiques pour chaque module
"""

from typing import Dict, List, Any, Optional
import yaml
import csv

class CSVMappings:
    """Mappings pour la conversion YAML ↔ CSV par module."""
    
    @staticmethod
    def yaml_to_csv_cm(yaml_data: Any) -> List[Dict[str, Any]]:
        """Conversion YAML → CSV pour Construction Métallique."""
        if isinstance(yaml_data, list):
            return [CSVMappings._yaml_to_csv_cm_single(item) for item in yaml_data]
        else:
            return [CSVMappings._yaml_to_csv_cm_single(yaml_data)]
    
    @staticmethod
    def _yaml_to_csv_cm_single(yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'un élément YAML → CSV pour CM."""
        csv_row = {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'section': yaml_data.get('section', ''),
            'longueur': yaml_data.get('longueur', ''),
            'charge_permanente': yaml_data.get('charge_permanente', ''),
            'charge_exploitation': yaml_data.get('charge_exploitation', ''),
            'acier': yaml_data.get('acier', ''),
            'statut': yaml_data.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if yaml_data.get('type') == 'poteau':
            csv_row.update({
                'effort_normal': yaml_data.get('effort_normal', ''),
                'moment_flexion': yaml_data.get('moment_flexion', ''),
                'longueur_flambement': yaml_data.get('longueur_flambement', '')
            })
        elif yaml_data.get('type') == 'poutre':
            csv_row.update({
                'moment_flexion': yaml_data.get('moment_flexion', ''),
                'effort_tranchant': yaml_data.get('effort_tranchant', ''),
                'flèche_max': yaml_data.get('flèche_max', '')
            })
        elif yaml_data.get('type') == 'assemblage':
            csv_row.update({
                'nombre_boulons': yaml_data.get('nombre_boulons', ''),
                'diametre_boulon': yaml_data.get('diametre_boulon', ''),
                'effort_cisaillement': yaml_data.get('effort_cisaillement', ''),
                'longueur_soudure': yaml_data.get('longueur_soudure', ''),
                'epaisseur_soudure': yaml_data.get('epaisseur_soudure', '')
            })
        
        return csv_row
    
    @staticmethod
    def csv_to_yaml_cm(csv_data: List[Dict[str, Any]]) -> Any:
        """Conversion CSV → YAML pour Construction Métallique."""
        if len(csv_data) == 1:
            return CSVMappings._csv_to_yaml_cm_single(csv_data[0])
        else:
            return [CSVMappings._csv_to_yaml_cm_single(row) for row in csv_data]
    
    @staticmethod
    def _csv_to_yaml_cm_single(csv_row: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'une ligne CSV → YAML pour CM."""
        yaml_data = {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'section': csv_row.get('section', ''),
            'longueur': float(csv_row.get('longueur', 0)) if csv_row.get('longueur') else None,
            'charge_permanente': float(csv_row.get('charge_permanente', 0)) if csv_row.get('charge_permanente') else None,
            'charge_exploitation': float(csv_row.get('charge_exploitation', 0)) if csv_row.get('charge_exploitation') else None,
            'acier': csv_row.get('acier', ''),
            'statut': csv_row.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if csv_row.get('type') == 'poteau':
            yaml_data.update({
                'effort_normal': float(csv_row.get('effort_normal', 0)) if csv_row.get('effort_normal') else None,
                'moment_flexion': float(csv_row.get('moment_flexion', 0)) if csv_row.get('moment_flexion') else None,
                'longueur_flambement': float(csv_row.get('longueur_flambement', 0)) if csv_row.get('longueur_flambement') else None
            })
        elif csv_row.get('type') == 'poutre':
            yaml_data.update({
                'moment_flexion': float(csv_row.get('moment_flexion', 0)) if csv_row.get('moment_flexion') else None,
                'effort_tranchant': float(csv_row.get('effort_tranchant', 0)) if csv_row.get('effort_tranchant') else None,
                'flèche_max': float(csv_row.get('flèche_max', 0)) if csv_row.get('flèche_max') else None
            })
        elif csv_row.get('type') == 'assemblage':
            yaml_data.update({
                'nombre_boulons': int(csv_row.get('nombre_boulons', 0)) if csv_row.get('nombre_boulons') else None,
                'diametre_boulon': csv_row.get('diametre_boulon', ''),
                'effort_cisaillement': float(csv_row.get('effort_cisaillement', 0)) if csv_row.get('effort_cisaillement') else None,
                'longueur_soudure': float(csv_row.get('longueur_soudure', 0)) if csv_row.get('longueur_soudure') else None,
                'epaisseur_soudure': float(csv_row.get('epaisseur_soudure', 0)) if csv_row.get('epaisseur_soudure') else None
            })
        
        return yaml_data
    
    @staticmethod
    def yaml_to_csv_bois(yaml_data: Any) -> List[Dict[str, Any]]:
        """Conversion YAML → CSV pour Construction Bois."""
        if isinstance(yaml_data, list):
            return [CSVMappings._yaml_to_csv_bois_single(item) for item in yaml_data]
        else:
            return [CSVMappings._yaml_to_csv_bois_single(yaml_data)]
    
    @staticmethod
    def _yaml_to_csv_bois_single(yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'un élément YAML → CSV pour Bois."""
        csv_row = {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'section': yaml_data.get('section', ''),
            'longueur': yaml_data.get('longueur', ''),
            'essence': yaml_data.get('essence', ''),
            'classe': yaml_data.get('classe', ''),
            'charge_permanente': yaml_data.get('charge_permanente', ''),
            'charge_exploitation': yaml_data.get('charge_exploitation', ''),
            'statut': yaml_data.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if yaml_data.get('type') == 'poteau':
            csv_row.update({
                'effort_normal': yaml_data.get('effort_normal', ''),
                'moment_flexion': yaml_data.get('moment_flexion', ''),
                'longueur_flambement': yaml_data.get('longueur_flambement', '')
            })
        elif yaml_data.get('type') == 'poutre':
            csv_row.update({
                'moment_flexion': yaml_data.get('moment_flexion', ''),
                'effort_tranchant': yaml_data.get('effort_tranchant', ''),
                'flèche_max': yaml_data.get('flèche_max', ''),
                'effort_cisaillement': yaml_data.get('effort_cisaillement', '')
            })
        elif yaml_data.get('type') == 'assemblage':
            csv_row.update({
                'nombre_pointes': yaml_data.get('nombre_pointes', ''),
                'diametre_pointe': yaml_data.get('diametre_pointe', ''),
                'effort_cisaillement': yaml_data.get('effort_cisaillement', ''),
                'longueur_embrevement': yaml_data.get('longueur_embrevement', ''),
                'largeur_embrevement': yaml_data.get('largeur_embrevement', ''),
                'effort_traction': yaml_data.get('effort_traction', '')
            })
        
        return csv_row
    
    @staticmethod
    def csv_to_yaml_bois(csv_data: List[Dict[str, Any]]) -> Any:
        """Conversion CSV → YAML pour Construction Bois."""
        if len(csv_data) == 1:
            return CSVMappings._csv_to_yaml_bois_single(csv_data[0])
        else:
            return [CSVMappings._csv_to_yaml_bois_single(row) for row in csv_data]
    
    @staticmethod
    def _csv_to_yaml_bois_single(csv_row: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'une ligne CSV → YAML pour Bois."""
        yaml_data = {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'section': csv_row.get('section', ''),
            'longueur': float(csv_row.get('longueur', 0)) if csv_row.get('longueur') else None,
            'essence': csv_row.get('essence', ''),
            'classe': csv_row.get('classe', ''),
            'charge_permanente': float(csv_row.get('charge_permanente', 0)) if csv_row.get('charge_permanente') else None,
            'charge_exploitation': float(csv_row.get('charge_exploitation', 0)) if csv_row.get('charge_exploitation') else None,
            'statut': csv_row.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if csv_row.get('type') == 'poteau':
            yaml_data.update({
                'effort_normal': float(csv_row.get('effort_normal', 0)) if csv_row.get('effort_normal') else None,
                'moment_flexion': float(csv_row.get('moment_flexion', 0)) if csv_row.get('moment_flexion') else None,
                'longueur_flambement': float(csv_row.get('longueur_flambement', 0)) if csv_row.get('longueur_flambement') else None
            })
        elif csv_row.get('type') == 'poutre':
            yaml_data.update({
                'moment_flexion': float(csv_row.get('moment_flexion', 0)) if csv_row.get('moment_flexion') else None,
                'effort_tranchant': float(csv_row.get('effort_tranchant', 0)) if csv_row.get('effort_tranchant') else None,
                'flèche_max': float(csv_row.get('flèche_max', 0)) if csv_row.get('flèche_max') else None,
                'effort_cisaillement': float(csv_row.get('effort_cisaillement', 0)) if csv_row.get('effort_cisaillement') else None
            })
        elif csv_row.get('type') == 'assemblage':
            yaml_data.update({
                'nombre_pointes': int(csv_row.get('nombre_pointes', 0)) if csv_row.get('nombre_pointes') else None,
                'diametre_pointe': float(csv_row.get('diametre_pointe', 0)) if csv_row.get('diametre_pointe') else None,
                'effort_cisaillement': float(csv_row.get('effort_cisaillement', 0)) if csv_row.get('effort_cisaillement') else None,
                'longueur_embrevement': float(csv_row.get('longueur_embrevement', 0)) if csv_row.get('longueur_embrevement') else None,
                'largeur_embrevement': float(csv_row.get('largeur_embrevement', 0)) if csv_row.get('largeur_embrevement') else None,
                'effort_traction': float(csv_row.get('effort_traction', 0)) if csv_row.get('effort_traction') else None
            })
        
        return yaml_data
    
    @staticmethod
    def yaml_to_csv_beton(yaml_data: Any) -> List[Dict[str, Any]]:
        """Conversion YAML → CSV pour Béton Armé."""
        if isinstance(yaml_data, list):
            return [CSVMappings._yaml_to_csv_beton_single(item) for item in yaml_data]
        else:
            return [CSVMappings._yaml_to_csv_beton_single(yaml_data)]
    
    @staticmethod
    def _yaml_to_csv_beton_single(yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'un élément YAML → CSV pour Béton."""
        csv_row = {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'section': yaml_data.get('section', ''),
            'hauteur': yaml_data.get('hauteur', ''),
            'beton': yaml_data.get('beton', ''),
            'acier': yaml_data.get('acier', ''),
            'charge_permanente': yaml_data.get('charge_permanente', ''),
            'charge_exploitation': yaml_data.get('charge_exploitation', ''),
            'statut': yaml_data.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if yaml_data.get('type') == 'poteau':
            csv_row.update({
                'effort_normal': yaml_data.get('effort_normal', ''),
                'moment_flexion': yaml_data.get('moment_flexion', ''),
                'longueur_flambement': yaml_data.get('longueur_flambement', ''),
                'armatures_longitudinales': yaml_data.get('armatures_longitudinales', ''),
                'armatures_transversales': yaml_data.get('armatures_transversales', '')
            })
        elif yaml_data.get('type') == 'radier':
            csv_row.update({
                'epaisseur': yaml_data.get('epaisseur', ''),
                'largeur': yaml_data.get('largeur', ''),
                'longueur': yaml_data.get('longueur', ''),
                'charge_totale': yaml_data.get('charge_totale', ''),
                'armatures_inferieures': yaml_data.get('armatures_inferieures', ''),
                'armatures_superieures': yaml_data.get('armatures_superieures', '')
            })
        
        return csv_row
    
    @staticmethod
    def csv_to_yaml_beton(csv_data: List[Dict[str, Any]]) -> Any:
        """Conversion CSV → YAML pour Béton Armé."""
        if len(csv_data) == 1:
            return CSVMappings._csv_to_yaml_beton_single(csv_data[0])
        else:
            return [CSVMappings._csv_to_yaml_beton_single(row) for row in csv_data]
    
    @staticmethod
    def _csv_to_yaml_beton_single(csv_row: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'une ligne CSV → YAML pour Béton."""
        yaml_data = {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'section': csv_row.get('section', ''),
            'hauteur': float(csv_row.get('hauteur', 0)) if csv_row.get('hauteur') else None,
            'beton': csv_row.get('beton', ''),
            'acier': csv_row.get('acier', ''),
            'charge_permanente': float(csv_row.get('charge_permanente', 0)) if csv_row.get('charge_permanente') else None,
            'charge_exploitation': float(csv_row.get('charge_exploitation', 0)) if csv_row.get('charge_exploitation') else None,
            'statut': csv_row.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if csv_row.get('type') == 'poteau':
            yaml_data.update({
                'effort_normal': float(csv_row.get('effort_normal', 0)) if csv_row.get('effort_normal') else None,
                'moment_flexion': float(csv_row.get('moment_flexion', 0)) if csv_row.get('moment_flexion') else None,
                'longueur_flambement': float(csv_row.get('longueur_flambement', 0)) if csv_row.get('longueur_flambement') else None,
                'armatures_longitudinales': csv_row.get('armatures_longitudinales', ''),
                'armatures_transversales': csv_row.get('armatures_transversales', '')
            })
        elif csv_row.get('type') == 'radier':
            yaml_data.update({
                'epaisseur': float(csv_row.get('epaisseur', 0)) if csv_row.get('epaisseur') else None,
                'largeur': float(csv_row.get('largeur', 0)) if csv_row.get('largeur') else None,
                'longueur': float(csv_row.get('longueur', 0)) if csv_row.get('longueur') else None,
                'charge_totale': float(csv_row.get('charge_totale', 0)) if csv_row.get('charge_totale') else None,
                'armatures_inferieures': csv_row.get('armatures_inferieures', ''),
                'armatures_superieures': csv_row.get('armatures_superieures', '')
            })
        
        return yaml_data
    
    @staticmethod
    def yaml_to_csv_hydro(yaml_data: Any) -> List[Dict[str, Any]]:
        """Conversion YAML → CSV pour Hydraulique."""
        if isinstance(yaml_data, list):
            return [CSVMappings._yaml_to_csv_hydro_single(item) for item in yaml_data]
        else:
            return [CSVMappings._yaml_to_csv_hydro_single(yaml_data)]
    
    @staticmethod
    def _yaml_to_csv_hydro_single(yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'un élément YAML → CSV pour Hydraulique."""
        csv_row = {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'debit': yaml_data.get('debit', ''),
            'matiere': yaml_data.get('matiere', ''),
            'statut': yaml_data.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if yaml_data.get('type') == 'canal':
            csv_row.update({
                'largeur': yaml_data.get('largeur', ''),
                'hauteur': yaml_data.get('hauteur', ''),
                'pente': yaml_data.get('pente', ''),
                'rugosite': yaml_data.get('rugosite', '')
            })
        elif yaml_data.get('type') == 'reservoir':
            csv_row.update({
                'volume': yaml_data.get('volume', ''),
                'hauteur': yaml_data.get('hauteur', ''),
                'diametre': yaml_data.get('diametre', ''),
                'forme': yaml_data.get('forme', '')
            })
        elif yaml_data.get('type') == 'troncon':
            csv_row.update({
                'diametre': yaml_data.get('diametre', ''),
                'longueur': yaml_data.get('longueur', ''),
                'pente': yaml_data.get('pente', ''),
                'rugosite': yaml_data.get('rugosite', '')
            })
        elif yaml_data.get('type') == 'tuyau':
            csv_row.update({
                'diametre': yaml_data.get('diametre', ''),
                'longueur': yaml_data.get('longueur', ''),
                'type_fluide': yaml_data.get('type_fluide', ''),
                'pression': yaml_data.get('pression', '')
            })
        
        return csv_row
    
    @staticmethod
    def csv_to_yaml_hydro(csv_data: List[Dict[str, Any]]) -> Any:
        """Conversion CSV → YAML pour Hydraulique."""
        if len(csv_data) == 1:
            return CSVMappings._csv_to_yaml_hydro_single(csv_data[0])
        else:
            return [CSVMappings._csv_to_yaml_hydro_single(row) for row in csv_data]
    
    @staticmethod
    def _csv_to_yaml_hydro_single(csv_row: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion d'une ligne CSV → YAML pour Hydraulique."""
        yaml_data = {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'debit': float(csv_row.get('debit', 0)) if csv_row.get('debit') else None,
            'matiere': csv_row.get('matiere', ''),
            'statut': csv_row.get('statut', '')
        }
        
        # Ajouter des champs spécifiques selon le type
        if csv_row.get('type') == 'canal':
            yaml_data.update({
                'largeur': float(csv_row.get('largeur', 0)) if csv_row.get('largeur') else None,
                'hauteur': float(csv_row.get('hauteur', 0)) if csv_row.get('hauteur') else None,
                'pente': float(csv_row.get('pente', 0)) if csv_row.get('pente') else None,
                'rugosite': float(csv_row.get('rugosite', 0)) if csv_row.get('rugosite') else None
            })
        elif csv_row.get('type') == 'reservoir':
            yaml_data.update({
                'volume': float(csv_row.get('volume', 0)) if csv_row.get('volume') else None,
                'hauteur': float(csv_row.get('hauteur', 0)) if csv_row.get('hauteur') else None,
                'diametre': float(csv_row.get('diametre', 0)) if csv_row.get('diametre') else None,
                'forme': csv_row.get('forme', '')
            })
        elif csv_row.get('type') == 'troncon':
            yaml_data.update({
                'diametre': float(csv_row.get('diametre', 0)) if csv_row.get('diametre') else None,
                'longueur': float(csv_row.get('longueur', 0)) if csv_row.get('longueur') else None,
                'pente': float(csv_row.get('pente', 0)) if csv_row.get('pente') else None,
                'rugosite': float(csv_row.get('rugosite', 0)) if csv_row.get('rugosite') else None
            })
        elif csv_row.get('type') == 'tuyau':
            yaml_data.update({
                'diametre': float(csv_row.get('diametre', 0)) if csv_row.get('diametre') else None,
                'longueur': float(csv_row.get('longueur', 0)) if csv_row.get('longueur') else None,
                'type_fluide': csv_row.get('type_fluide', ''),
                'pression': float(csv_row.get('pression', 0)) if csv_row.get('pression') else None
            })
        
        return yaml_data 