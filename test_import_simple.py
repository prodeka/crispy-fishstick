#!/usr/bin/env python3
"""
Test simple d'import des modules
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_import_database():
    """Test l'import du module database"""
    try:
        from lcpi.aep.core.database import AEPDatabase
        print("✅ Import AEPDatabase réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur import AEPDatabase: {e}")
        return False

def test_import_import_automatique():
    """Test l'import du module import_automatique"""
    try:
        from lcpi.aep.core.import_automatique import AEPImportAutomatique
        print("✅ Import AEPImportAutomatique réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur import AEPImportAutomatique: {e}")
        return False

def test_import_validation_donnees():
    """Test l'import du module validation_donnees"""
    try:
        from lcpi.aep.core.validation_donnees import AEPDataValidator
        print("✅ Import AEPDataValidator réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur import AEPDataValidator: {e}")
        return False

def test_import_recalcul_automatique():
    """Test l'import du module recalcul_automatique"""
    try:
        from lcpi.aep.core.recalcul_automatique import AEPRecalculEngine
        print("✅ Import AEPRecalculEngine réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur import AEPRecalculEngine: {e}")
        return False

if __name__ == "__main__":
    print("=== Test d'import des modules ===")
    
    success = True
    success &= test_import_database()
    success &= test_import_import_automatique()
    success &= test_import_validation_donnees()
    success &= test_import_recalcul_automatique()
    
    if success:
        print("\n✅ Tous les imports sont réussis")
    else:
        print("\n❌ Certains imports ont échoué")
