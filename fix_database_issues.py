#!/usr/bin/env python3
"""
Script de correction des problèmes de base de données pour le test de fusion AEP.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def fix_database_issues():
    """Corrige les problèmes de base de données identifiés."""
    print("🔧 Correction des Problèmes de Base de Données")
    print("=" * 60)
    
    # 1. Créer le dossier de test s'il n'existe pas
    test_dir = Path("test_fusion_aep")
    test_dir.mkdir(exist_ok=True)
    print(f"✅ Dossier de test créé: {test_dir}")
    
    # 2. Créer le fichier lcpi.yml manquant
    lcpi_config = test_dir / "lcpi.yml"
    if not lcpi_config.exists():
        config_content = """# Configuration du projet test_fusion_aep
projet_metadata:
  nom: "Projet AEP Fusion Test"
  description: "Projet de test pour la fusion AEP avec ProjectManager"
  version: "1.0.0"
  auteur: "LCPI-CLI"
  date_creation: "2025-08-16"

plugins_actifs:
  - aep
  - cm
  - bois
  - beton
  - hydro

configurations:
  base_de_donnees:
    type: "sqlite"
    chemin: "database.db"
    auto_initialisation: true
  
  modules:
    aep:
      version: "2.1.0"
      fonctionnalites:
        - hardy_cross
        - epanet_integration
        - base_donnees_centralisee
        - workflow_complet
"""
        with open(lcpi_config, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Fichier lcpi.yml créé")
    
    # 3. Initialiser la base de données unifiée
    try:
        from lcpi.core.unified_database import UnifiedDatabase
        
        db_path = test_dir / "database.db"
        db = UnifiedDatabase(db_path)
        print("✅ Base de données unifiée initialisée")
        
        # 4. Créer un projet de test
        projet_id = db.ajouter_projet(
            "Projet AEP Fusion Test",
            "Projet de test pour la fusion AEP avec ProjectManager",
            {"module": "aep", "type": "test"},
            "aep"
        )
        print(f"✅ Projet créé avec ID: {projet_id}")
        
        # 5. Les tables AEP sont déjà créées lors de l'initialisation
        print("✅ Tables AEP disponibles")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        return False
    
    # 6. Vérifier que tout fonctionne
    try:
        from lcpi.aep.core.aep_project_wrapper import AEPProjectWrapper
        
        wrapper = AEPProjectWrapper(test_dir)
        status = wrapper.get_status()
        
        print("\n📊 Statut du Wrapper AEP:")
        print(f"   Wrapper disponible: {status['available']}")
        print(f"   ProjectManager disponible: {status['project_manager_available']}")
        print(f"   Base de données disponible: {status.get('database_available', False)}")
        
        if status['available'] and status['project_manager_available']:
            print("✅ Tous les composants sont disponibles")
            return True
        else:
            print("❌ Certains composants ne sont pas disponibles")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test du wrapper: {e}")
        return False

if __name__ == "__main__":
    try:
        success = fix_database_issues()
        if success:
            print("\n🎉 Correction terminée avec succès !")
            print("Vous pouvez maintenant relancer test_fusion_aep.py")
        else:
            print("\n❌ Correction échouée")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
