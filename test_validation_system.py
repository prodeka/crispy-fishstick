#!/usr/bin/env python3
"""
Test du système de validation LCPI.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_validation_schemas():
    """Test des schémas de validation."""
    print("🧪 Test des schémas de validation...")
    
    try:
        from lcpi.validation.schemas import ValidationSchema
        
        # Test d'un schéma simple
        schema = ValidationSchema({
            "type": "object",
            "required": ["name", "value"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "value": {"type": "number", "minimum": 0}
            }
        })
        
        # Données valides
        valid_data = {"name": "test", "value": 42}
        result = schema.validate(valid_data)
        print(f"✅ Validation données valides: {result['valid']}")
        
        # Données invalides
        invalid_data = {"name": "", "value": -1}
        result = schema.validate(invalid_data)
        print(f"✅ Validation données invalides: {not result['valid']}")
        print(f"  - Erreurs: {len(result['errors'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur schémas: {e}")
        return False

def test_data_validator():
    """Test du validateur de données."""
    print("\n🧪 Test du validateur de données...")
    
    try:
        from lcpi.validation.validator import validator
        
        # Vérifier les schémas disponibles
        schemas = validator.list_schemas()
        print(f"✅ Schémas disponibles: {len(schemas)}")
        
        for schema_name in schemas:
            schema = validator.get_schema(schema_name)
            if schema:
                info = schema.get_schema_info()
                print(f"  - {schema_name}: {info.get('type', 'object')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur validateur: {e}")
        return False

def test_validation_errors():
    """Test de la gestion des erreurs."""
    print("\n🧪 Test de la gestion des erreurs...")
    
    try:
        from lcpi.validation.errors import ValidationError, ValidationWarning, ValidationResult
        
        # Test d'erreur
        error = ValidationError("Test d'erreur", {"field": "test"})
        print(f"✅ Erreur créée: {error}")
        
        # Test d'avertissement
        warning = ValidationWarning("Test d'avertissement", "warning")
        print(f"✅ Avertissement créé: {warning}")
        
        # Test de résultat
        result = ValidationResult(False, [error], [warning])
        print(f"✅ Résultat créé: {result}")
        print(f"  - Valide: {result.valid}")
        print(f"  - Erreurs: {len(result.errors)}")
        print(f"  - Avertissements: {len(result.warnings)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestion erreurs: {e}")
        return False

def test_validation_context():
    """Test du contexte de validation."""
    print("\n🧪 Test du contexte de validation...")
    
    try:
        from lcpi.validation.errors import ValidationContext
        
        context = ValidationContext()
        
        # Ajouter des erreurs et avertissements
        context.add_error("Erreur 1", "field1")
        context.add_warning("Avertissement 1", "warning", "field2")
        
        # Changer de contexte
        context.push_path("nested")
        context.add_error("Erreur 2")
        context.pop_path()
        
        # Récupérer le résultat
        result = context.get_result()
        print(f"✅ Contexte créé: {result}")
        print(f"  - Valide: {result.valid}")
        print(f"  - Erreurs: {len(result.errors)}")
        print(f"  - Avertissements: {len(result.warnings)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur contexte: {e}")
        return False

def test_validation_integration():
    """Test d'intégration du système de validation."""
    print("\n🧪 Test d'intégration...")
    
    try:
        from lcpi.validation.validator import validator
        
        # Créer des données de test
        test_data = {
            "network": {
                "name": "Test Network",
                "nodes": [
                    {"id": "N1", "type": "junction", "elevation": 100},
                    {"id": "N2", "type": "reservoir", "elevation": 120}
                ],
                "pipes": [
                    {"id": "P1", "from_node": "N1", "to_node": "N2", "length": 100, "diameter": 0.2}
                ]
            }
        }
        
        # Valider avec le schéma AEP
        result = validator.validate_data(test_data, "aep_basic", "test_data")
        
        print(f"✅ Validation intégration: {result['valid']}")
        print(f"  - Schéma: {result.get('schema')}")
        print(f"  - Erreurs: {len(result.get('errors', []))}")
        print(f"  - Avertissements: {len(result.get('warnings', []))}")
        
        # Générer le rapport
        report = validator.get_validation_report(result)
        print(f"  - Rapport généré: {len(report)} caractères")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test du système de validation LCPI")
    print("=" * 50)
    
    tests = [
        test_validation_schemas,
        test_data_validator,
        test_validation_errors,
        test_validation_context,
        test_validation_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 Résumé des tests:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
