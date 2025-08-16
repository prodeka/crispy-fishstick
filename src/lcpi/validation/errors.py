"""
Gestion des erreurs de validation pour LCPI.
Définit les types d'erreurs et d'avertissements.
"""

from typing import List, Dict, Any, Optional

class ValidationError(Exception):
    """Erreur de validation des données."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        return f"ValidationError: {self.message}"
    
    def get_details(self) -> Dict[str, Any]:
        """Retourne les détails de l'erreur."""
        return self.details

class ValidationWarning:
    """Avertissement de validation."""
    
    def __init__(self, message: str, level: str = "warning", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.level = level  # warning, info, suggestion
        self.details = details or {}
    
    def __str__(self):
        return f"ValidationWarning[{self.level}]: {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'avertissement en dictionnaire."""
        return {
            "message": self.message,
            "level": self.level,
            "details": self.details
        }

class ValidationResult:
    """Résultat d'une validation."""
    
    def __init__(self, valid: bool, errors: List[ValidationError] = None, warnings: List[ValidationWarning] = None):
        self.valid = valid
        self.errors = errors or []
        self.warnings = warnings or []
    
    def add_error(self, error: ValidationError):
        """Ajoute une erreur."""
        self.errors.append(error)
        self.valid = False
    
    def add_warning(self, warning: ValidationWarning):
        """Ajoute un avertissement."""
        self.warnings.append(warning)
    
    def has_errors(self) -> bool:
        """Vérifie s'il y a des erreurs."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Vérifie s'il y a des avertissements."""
        return len(self.warnings) > 0
    
    def get_error_messages(self) -> List[str]:
        """Récupère les messages d'erreur."""
        return [str(error) for error in self.errors]
    
    def get_warning_messages(self) -> List[str]:
        """Récupère les messages d'avertissement."""
        return [str(warning) for warning in self.warnings]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le résultat en dictionnaire."""
        return {
            "valid": self.valid,
            "errors": [str(error) for error in self.errors],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "error_count": len(self.errors),
            "warning_count": len(self.warnings)
        }
    
    def __bool__(self):
        """Permet d'utiliser le résultat comme un booléen."""
        return self.valid

class ValidationContext:
    """Contexte de validation pour gérer les erreurs et avertissements."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.current_path = ""
        self.schema_name = ""
    
    def add_error(self, message: str, path: str = None, details: Optional[Dict[str, Any]] = None):
        """Ajoute une erreur de validation."""
        error_path = path or self.current_path
        error = ValidationError(f"{error_path}: {message}" if error_path else message, details)
        self.errors.append(error)
    
    def add_warning(self, message: str, level: str = "warning", path: str = None, details: Optional[Dict[str, Any]] = None):
        """Ajoute un avertissement de validation."""
        warning_path = path or self.current_path
        warning_message = f"{warning_path}: {message}" if warning_path else message
        warning = ValidationWarning(warning_message, level, details)
        self.warnings.append(warning)
    
    def set_path(self, path: str):
        """Définit le chemin actuel pour les erreurs."""
        self.current_path = path
    
    def push_path(self, component: str):
        """Ajoute un composant au chemin actuel."""
        if self.current_path:
            self.current_path = f"{self.current_path}.{component}"
        else:
            self.current_path = component
    
    def pop_path(self):
        """Retire le dernier composant du chemin."""
        if "." in self.current_path:
            self.current_path = ".".join(self.current_path.split(".")[:-1])
        else:
            self.current_path = ""
    
    def get_result(self) -> ValidationResult:
        """Retourne le résultat de validation."""
        return ValidationResult(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings
        )
    
    def clear(self):
        """Vide le contexte de validation."""
        self.errors.clear()
        self.warnings.clear()
        self.current_path = ""
