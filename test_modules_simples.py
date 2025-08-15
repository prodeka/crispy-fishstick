#!/usr/bin/env python3
"""
Test simple pour vérifier les modules créés
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_database():
    """Test du module database"""
    try:
        from lcpi.aep.core.database import AEPDatabase
        print("✅ Module database importé avec succès")
        
        # Test d'initialisation
        db = AEPDatabase(":memory:")  # Base en mémoire pour les tests
        print("✅ Base de données initialisée")
        
        # Test d'ajout de projet
        projet_id = db.ajouter_projet("Test Projet", "Description test")
        print(f"✅ Projet ajouté avec ID: {projet_id}")
        
        # Test d'obtention des projets
        projets = db.obtenir_projets()
        print(f"✅ {len(projets)} projet(s) récupéré(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le module database: {e}")
        return False

def test_import_automatique():
    """Test du module import_automatique"""
    try:
        from lcpi.aep.core.import_automatique import AEPImportAutomatique
        from lcpi.aep.core.database import AEPDatabase
        print("✅ Module import_automatique importé avec succès")
        
        # Test d'initialisation
        db = AEPDatabase(":memory:")
        importateur = AEPImportAutomatique(db)
        print("✅ Importateur initialisé")
        
        # Test des types supportés
        types = importateur.obtenir_types_import_supportes()
        print(f"✅ Types d'import supportés: {types}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le module import_automatique: {e}")
        return False

def test_validation_donnees():
    """Test du module validation_donnees"""
    try:
        from lcpi.aep.core.validation_donnees import AEPDataValidator, ValidationResult
        from lcpi.aep.core.database import AEPDatabase
        print("✅ Module validation_donnees importé avec succès")
        
        # Test d'initialisation
        db = AEPDatabase(":memory:")
        validateur = AEPDataValidator(db)
        print("✅ Validateur initialisé")
        
        # Test de validation de coordonnées GPS
        resultat = validateur.valider_coordonnees_gps("12.345,67.890")
        print(f"✅ Validation GPS: {resultat.valide}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le module validation_donnees: {e}")
        return False

def test_recalcul_automatique():
    """Test du module recalcul_automatique"""
    try:
        from lcpi.aep.core.recalcul_automatique import AEPRecalculEngine, TypeRecalcul
        from lcpi.aep.core.database import AEPDatabase
        print("✅ Module recalcul_automatique importé avec succès")
        
        # Test d'initialisation
        db = AEPDatabase(":memory:")
        moteur = AEPRecalculEngine(db)
        print("✅ Moteur de recalcul initialisé")
        
        # Test d'ajout de tâche
        task_id = moteur.ajouter_tache_recalcul(
            TypeRecalcul.POPULATION, 
            1, 
            {"population_base": 1000, "taux_croissance": 0.025, "annees": 5}
        )
        print(f"✅ Tâche de recalcul ajoutée: {task_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le module recalcul_automatique: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test des modules créés\n")
    
    tests = [
        ("Database", test_database),
        ("Import Automatique", test_import_automatique),
        ("Validation Données", test_validation_donnees),
        ("Recalcul Automatique", test_recalcul_automatique)
    ]
    
    resultats = []
    for nom, test_func in tests:
        print(f"\n--- Test {nom} ---")
        try:
            resultat = test_func()
            resultats.append((nom, resultat))
        except Exception as e:
            print(f"❌ Erreur lors du test {nom}: {e}")
            resultats.append((nom, False))
    
    # Résumé
    print(f"\n{'='*50}")
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    
    succes = 0
    for nom, resultat in resultats:
        status = "✅ SUCCÈS" if resultat else "❌ ÉCHEC"
        print(f"{nom:25} {status}")
        if resultat:
            succes += 1
    
    print(f"\nTotal: {succes}/{len(resultats)} tests réussis")
    
    if succes == len(resultats):
        print("🎉 Tous les modules fonctionnent correctement!")
        return 0
    else:
        print("⚠️ Certains modules ont des problèmes")
        return 1

if __name__ == "__main__":
    exit(main())
