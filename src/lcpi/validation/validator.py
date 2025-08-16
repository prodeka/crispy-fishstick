"""
Validateur principal pour LCPI.
Gère la validation des données selon différents schémas.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import hashlib

from .schemas import ValidationSchema
from .errors import ValidationError, ValidationWarning

class DataValidator:
    """Validateur de données LCPI."""
    
    def __init__(self):
        self.schemas = {}
        self.validation_cache = {}
        self._load_builtin_schemas()
    
    def _load_builtin_schemas(self):
        """Charge les schémas de validation intégrés."""
        # Schéma AEP de base
        self.schemas["aep_basic"] = ValidationSchema({
            "type": "object",
            "required": ["network"],
            "properties": {
                "network": {
                    "type": "object",
                    "required": ["name", "nodes", "pipes"],
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "nodes": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": ["id", "type", "elevation"],
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string", "enum": ["junction", "reservoir", "tank"]},
                                    "elevation": {"type": "number", "minimum": 0}
                                }
                            }
                        },
                        "pipes": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": ["id", "from_node", "to_node", "length", "diameter"],
                                "properties": {
                                    "id": {"type": "string"},
                                    "from_node": {"type": "string"},
                                    "to_node": {"type": "string"},
                                    "length": {"type": "number", "minimum": 0.1},
                                    "diameter": {"type": "number", "minimum": 0.01}
                                }
                            }
                        }
                    }
                }
            }
        })
        
        # Schéma canal
        self.schemas["canal"] = ValidationSchema({
            "type": "object",
            "required": ["canal"],
            "properties": {
                "canal": {
                    "type": "object",
                    "required": ["nom", "geometrie", "hydraulique"],
                    "properties": {
                        "nom": {"type": "string", "minLength": 1},
                        "description": {"type": "string"},
                        "geometrie": {
                            "type": "object",
                            "required": ["type", "largeur_fond", "profondeur"],
                            "properties": {
                                "type": {"type": "string", "enum": ["trapezoidal", "rectangular", "triangular"]},
                                "largeur_fond": {"type": "number", "minimum": 0.1},
                                "pente_talus": {"type": "number", "minimum": 0.5},
                                "profondeur": {"type": "number", "minimum": 0.1}
                            }
                        },
                        "hydraulique": {
                            "type": "object",
                            "required": ["debit_design", "pente_longitudinale", "coefficient_rugosite"],
                            "properties": {
                                "debit_design": {"type": "number", "minimum": 0.001},
                                "pente_longitudinale": {"type": "number", "minimum": 0.0001, "maximum": 0.1},
                                "coefficient_rugosite": {"type": "number", "minimum": 0.01, "maximum": 0.1}
                            }
                        },
                        "securite": {
                            "type": "object",
                            "properties": {
                                "revanche": {"type": "number", "minimum": 0.1},
                                "vitesse_maximale": {"type": "number", "minimum": 0.5},
                                "vitesse_minimale": {"type": "number", "minimum": 0.1}
                            }
                        },
                        "construction": {
                            "type": "object",
                            "properties": {
                                "materiau": {"type": "string"},
                                "revetement": {"type": "string"},
                                "compactage": {"type": "string"}
                            }
                        },
                        "environnement": {
                            "type": "object",
                            "properties": {
                                "zone_climatique": {"type": "string"},
                                "exposition": {"type": "string"},
                                "protection_vegetation": {"type": "boolean"}
                            }
                        }
                    }
                }
            }
        })
        
        # Schéma béton
        self.schemas["beton"] = ValidationSchema({
            "type": "object",
            "required": ["element", "charges", "materiaux"],
            "properties": {
                "element": {
                    "type": "object",
                    "required": ["type", "dimensions"],
                    "properties": {
                        "type": {"type": "string", "enum": ["poteau", "poutre", "radier"]},
                        "dimensions": {
                            "type": "object",
                            "required": ["width", "height"],
                            "properties": {
                                "width": {"type": "number", "minimum": 0.1},
                                "height": {"type": "number", "minimum": 0.1}
                            }
                        }
                    }
                },
                "charges": {
                    "type": "object",
                    "required": ["permanentes", "variables"],
                    "properties": {
                        "permanentes": {"type": "number", "minimum": 0},
                        "variables": {"type": "number", "minimum": 0}
                    }
                },
                "materiaux": {
                    "type": "object",
                    "required": ["fc28", "fe"],
                    "properties": {
                        "fc28": {"type": "number", "minimum": 20, "maximum": 100},
                        "fe": {"type": "number", "minimum": 400, "maximum": 600}
                    }
                }
            }
        })
    
    def validate_file(self, file_path: Union[str, Path], schema_name: Optional[str] = None) -> Dict[str, Any]:
        """Valide un fichier selon un schéma."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ValidationError(f"Fichier non trouvé: {file_path}")
        
        # Détecter le type de fichier
        if file_path.suffix.lower() in ['.yml', '.yaml']:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValidationError(f"Type de fichier non supporté: {file_path.suffix}")
        
        # Détecter automatiquement le schéma si non spécifié
        if not schema_name:
            schema_name = self._detect_schema(data, file_path)
        
        return self.validate_data(data, schema_name, str(file_path))
    
    def _detect_schema(self, data: Dict[str, Any], file_path: Path) -> str:
        """Détecte automatiquement le schéma à utiliser."""
        # Détection par nom de fichier
        filename = file_path.name.lower()
        if "canal" in filename:
            return "canal"
        elif "beton" in filename or "concrete" in filename:
            return "beton"
        elif "aep" in filename or "network" in filename or "reseau" in filename:
            return "aep_basic"
        
        # Détection par structure des données
        if "network" in data:
            return "aep_basic"
        elif "geometry" in data and "flow" in data:
            return "canal"
        elif "element" in data and "materiaux" in data:
            return "beton"
        
        # Schéma par défaut
        return "aep_basic"
    
    def validate_data(self, data: Dict[str, Any], schema_name: str, source: str = "unknown") -> Dict[str, Any]:
        """Valide des données selon un schéma."""
        if schema_name not in self.schemas:
            raise ValidationError(f"Schéma inconnu: {schema_name}")
        
        schema = self.schemas[schema_name]
        
        # Calculer le hash des données pour le cache
        data_hash = self._calculate_data_hash(data)
        cache_key = f"{schema_name}_{data_hash}"
        
        # Vérifier le cache
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        # Valider les données
        try:
            validation_result = schema.validate(data)
            
            # Ajouter des métadonnées
            result = {
                "valid": validation_result["valid"],
                "errors": validation_result.get("errors", []),
                "warnings": validation_result.get("warnings", []),
                "schema": schema_name,
                "source": source,
                "timestamp": datetime.now().isoformat(),
                "data_hash": data_hash,
                "data_summary": self._generate_data_summary(data)
            }
            
            # Mettre en cache
            self.validation_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            raise ValidationError(f"Erreur lors de la validation: {e}")
    
    def _calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """Calcule le hash des données pour le cache."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _generate_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un résumé des données validées."""
        summary = {
            "keys": list(data.keys()),
            "size": len(str(data)),
            "depth": self._calculate_depth(data)
        }
        
        # Compter les éléments pour les structures communes
        if "network" in data:
            network = data["network"]
            if "nodes" in network:
                summary["node_count"] = len(network["nodes"])
            if "pipes" in network:
                summary["pipe_count"] = len(network["pipes"])
        
        return summary
    
    def _calculate_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calcule la profondeur maximale d'un objet."""
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._calculate_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._calculate_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth
    
    def get_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Génère un rapport de validation lisible."""
        report = []
        report.append("=" * 60)
        report.append("📋 RAPPORT DE VALIDATION LCPI")
        report.append("=" * 60)
        
        # Informations générales
        report.append(f"📁 Source: {validation_result.get('source', 'Inconnue')}")
        report.append(f"🔧 Schéma: {validation_result.get('schema', 'Inconnu')}")
        report.append(f"⏰ Timestamp: {validation_result.get('timestamp', 'Inconnu')}")
        report.append(f"🔍 Hash: {validation_result.get('data_hash', 'Inconnu')[:8]}...")
        
        # Résumé des données
        summary = validation_result.get('data_summary', {})
        if summary:
            report.append("\n📊 RÉSUMÉ DES DONNÉES:")
            for key, value in summary.items():
                report.append(f"  • {key}: {value}")
        
        # Statut de validation
        report.append(f"\n✅ STATUT: {'VALIDÉ' if validation_result.get('valid') else 'ERREURS DÉTECTÉES'}")
        
        # Erreurs
        errors = validation_result.get('errors', [])
        if errors:
            report.append(f"\n❌ ERREURS ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                report.append(f"  {i}. {error}")
        
        # Avertissements
        warnings = validation_result.get('warnings', [])
        if warnings:
            report.append(f"\n⚠️  AVERTISSEMENTS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                report.append(f"  {i}. {warning}")
        
        # Recommandations
        if validation_result.get('valid'):
            report.append("\n💡 RECOMMANDATIONS:")
            report.append("  • Les données sont valides et prêtes pour le calcul")
            report.append("  • Vérifiez les unités et les valeurs limites")
        else:
            report.append("\n🔧 CORRECTIONS NÉCESSAIRES:")
            report.append("  • Corrigez les erreurs listées ci-dessus")
            report.append("  • Vérifiez la structure des données")
            report.append("  • Consultez la documentation du schéma")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def add_schema(self, name: str, schema: ValidationSchema):
        """Ajoute un nouveau schéma de validation."""
        self.schemas[name] = schema
    
    def list_schemas(self) -> List[str]:
        """Liste les schémas disponibles."""
        return list(self.schemas.keys())
    
    def get_schema(self, name: str) -> Optional[ValidationSchema]:
        """Récupère un schéma par nom."""
        return self.schemas.get(name)
    
    def clear_cache(self):
        """Vide le cache de validation."""
        self.validation_cache.clear()

# Instance globale
validator = DataValidator()
