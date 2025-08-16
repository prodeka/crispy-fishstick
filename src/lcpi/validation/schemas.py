"""
Schémas de validation pour LCPI.
Définit les structures de validation des données.
"""

from typing import Dict, Any, List, Optional, Union
import re

class ValidationSchema:
    """Schéma de validation pour les données LCPI."""
    
    def __init__(self, schema_definition: Dict[str, Any]):
        self.definition = schema_definition
        self._compile_schema()
    
    def _compile_schema(self):
        """Compile le schéma pour la validation."""
        # Pour l'instant, on utilise une validation simple
        # Dans une version future, on pourrait utiliser jsonschema ou pydantic
        pass
    
    def validate(self, data: Any) -> Dict[str, Any]:
        """Valide des données selon le schéma."""
        errors = []
        warnings = []
        
        try:
            self._validate_object(data, self.definition, "", errors, warnings)
        except Exception as e:
            errors.append(f"Erreur de validation: {e}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _validate_object(self, data: Any, schema: Dict[str, Any], path: str, errors: List[str], warnings: List[str]):
        """Valide un objet selon le schéma."""
        # Vérifier le type
        expected_type = schema.get("type")
        if expected_type:
            if not self._check_type(data, expected_type):
                errors.append(f"{path}: Type attendu '{expected_type}', reçu '{type(data).__name__}'")
                return
        
        # Vérifier les propriétés requises
        required = schema.get("required", [])
        if isinstance(data, dict):
            for prop in required:
                if prop not in data:
                    errors.append(f"{path}: Propriété requise '{prop}' manquante")
        
        # Vérifier les propriétés
        properties = schema.get("properties", {})
        if isinstance(data, dict):
            for prop_name, prop_schema in properties.items():
                if prop_name in data:
                    prop_path = f"{path}.{prop_name}" if path else prop_name
                    self._validate_property(data[prop_name], prop_schema, prop_path, errors, warnings)
        
        # Vérifier les contraintes
        self._validate_constraints(data, schema, path, errors, warnings)
    
    def _validate_property(self, value: Any, schema: Dict[str, Any], path: str, errors: List[str], warnings: List[str]):
        """Valide une propriété selon son schéma."""
        if isinstance(schema, dict):
            self._validate_object(value, schema, path, errors, warnings)
        else:
            # Validation simple pour les types de base
            if not self._check_type(value, schema):
                errors.append(f"{path}: Type invalide")
    
    def _check_type(self, data: Any, expected_type: str) -> bool:
        """Vérifie le type d'une donnée."""
        if expected_type == "string":
            return isinstance(data, str)
        elif expected_type == "number":
            return isinstance(data, (int, float))
        elif expected_type == "integer":
            return isinstance(data, int)
        elif expected_type == "boolean":
            return isinstance(data, bool)
        elif expected_type == "array":
            return isinstance(data, list)
        elif expected_type == "object":
            return isinstance(data, dict)
        elif expected_type == "null":
            return data is None
        return True
    
    def _validate_constraints(self, data: Any, schema: Dict[str, Any], path: str, errors: List[str], warnings: List[str]):
        """Valide les contraintes d'un schéma."""
        # Contraintes sur les chaînes
        if isinstance(data, str):
            min_length = schema.get("minLength")
            if min_length is not None and len(data) < min_length:
                errors.append(f"{path}: Longueur minimale {min_length}, reçu {len(data)}")
            
            max_length = schema.get("maxLength")
            if max_length is not None and len(data) > max_length:
                errors.append(f"{path}: Longueur maximale {max_length}, reçu {len(data)}")
            
            pattern = schema.get("pattern")
            if pattern and not re.match(pattern, data):
                errors.append(f"{path}: Format invalide, doit correspondre à {pattern}")
            
            enum = schema.get("enum")
            if enum and data not in enum:
                errors.append(f"{path}: Valeur '{data}' non autorisée. Valeurs acceptées: {enum}")
        
        # Contraintes sur les nombres
        elif isinstance(data, (int, float)):
            minimum = schema.get("minimum")
            if minimum is not None and data < minimum:
                errors.append(f"{path}: Valeur minimale {minimum}, reçu {data}")
            
            maximum = schema.get("maximum")
            if maximum is not None and data > maximum:
                errors.append(f"{path}: Valeur maximale {maximum}, reçu {data}")
            
            exclusive_minimum = schema.get("exclusiveMinimum")
            if exclusive_minimum is not None and data <= exclusive_minimum:
                errors.append(f"{path}: Valeur strictement supérieure à {exclusive_minimum}, reçu {data}")
            
            exclusive_maximum = schema.get("exclusiveMaximum")
            if exclusive_maximum is not None and data >= exclusive_maximum:
                errors.append(f"{path}: Valeur strictement inférieure à {exclusive_maximum}, reçu {data}")
        
        # Contraintes sur les tableaux
        elif isinstance(data, list):
            min_items = schema.get("minItems")
            if min_items is not None and len(data) < min_items:
                errors.append(f"{path}: Nombre minimum d'éléments {min_items}, reçu {len(data)}")
            
            max_items = schema.get("maxItems")
            if max_items is not None and len(data) > max_items:
                errors.append(f"{path}: Nombre maximum d'éléments {max_items}, reçu {len(data)}")
            
            unique_items = schema.get("uniqueItems")
            if unique_items and len(data) != len(set(data)):
                errors.append(f"{path}: Les éléments doivent être uniques")
            
            # Valider les éléments du tableau
            items_schema = schema.get("items")
            if items_schema:
                for i, item in enumerate(data):
                    item_path = f"{path}[{i}]"
                    self._validate_property(item, items_schema, item_path, errors, warnings)
        
        # Contraintes sur les objets
        elif isinstance(data, dict):
            min_properties = schema.get("minProperties")
            if min_properties is not None and len(data) < min_properties:
                errors.append(f"{path}: Nombre minimum de propriétés {min_properties}, reçu {len(data)}")
            
            max_properties = schema.get("maxProperties")
            if max_properties is not None and len(data) > max_properties:
                errors.append(f"{path}: Nombre maximum de propriétés {max_properties}, reçu {len(data)}")
            
            # Vérifier les propriétés supplémentaires
            additional_properties = schema.get("additionalProperties", True)
            if additional_properties is False:
                allowed_props = set(schema.get("properties", {}).keys())
                extra_props = set(data.keys()) - allowed_props
                if extra_props:
                    errors.append(f"{path}: Propriétés non autorisées: {extra_props}")
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Retourne des informations sur le schéma."""
        return {
            "type": self.definition.get("type"),
            "required": self.definition.get("required", []),
            "properties": list(self.definition.get("properties", {}).keys()),
            "description": self.definition.get("description", ""),
            "title": self.definition.get("title", "")
        }
    
    def is_valid(self, data: Any) -> bool:
        """Vérifie rapidement si des données sont valides."""
        result = self.validate(data)
        return result["valid"]
    
    def get_errors(self, data: Any) -> List[str]:
        """Récupère uniquement les erreurs de validation."""
        result = self.validate(data)
        return result.get("errors", [])
    
    def get_warnings(self, data: Any) -> List[str]:
        """Récupère uniquement les avertissements de validation."""
        result = self.validate(data)
        return result.get("warnings", [])
