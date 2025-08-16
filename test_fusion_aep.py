#!/usr/bin/env python3
"""
Script de test pour la fusion AEP avec le ProjectManager centralisé.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.core.aep_project_wrapper import AEPProjectWrapper
from lcpi.reporting.utils.pdf_generator import get_weasyprint_status

def test_fusion_aep():
    """Test complet de la fusion AEP."""
    print("🔧 Test de la Fusion AEP avec ProjectManager Centralisé")
    print("=" * 60)
    
    # Test 1: Statut WeasyPrint
    print("\n📋 1. Diagnostic WeasyPrint:")
    weasyprint_status = get_weasyprint_status()
    print(f"   Disponible: {weasyprint_status['available']}")
    if weasyprint_status['error']:
        print(f"   Erreur: {weasyprint_status['error']}")
        print(f"   Suggestions: {', '.join(weasyprint_status['suggestions'])}")
    
    # Test 2: Création du wrapper AEP
    print("\n📋 2. Création du Wrapper AEP:")
    project_dir = "test_fusion_aep"
    wrapper = AEPProjectWrapper(project_dir)
    status = wrapper.get_status()
    print(f"   Wrapper disponible: {status['available']}")
    print(f"   ProjectManager disponible: {status['project_manager_available']}")
    print(f"   Dossier projet: {status['project_dir']}")
    
    # Test 3: Création du projet AEP
    print("\n📋 3. Création du Projet AEP:")
    projet_id = wrapper.create_aep_project(
        "Projet AEP Fusion Test",
        "Projet de test pour la fusion AEP avec ProjectManager"
    )
    print(f"   Projet créé avec ID: {projet_id}")
    
    # Test 4: Ajout d'un réseau
    print("\n📋 4. Création du Réseau:")
    reseau_id = wrapper.add_network(
        "Réseau Principal",
        "distribution",
        {
            "type": "gravitaire",
            "pression_nominale": 3.0,
            "debit_max": 50.0
        }
    )
    print(f"   Réseau créé avec ID: {reseau_id}")
    
    # Test 5: Ajout de nœuds
    print("\n📋 5. Création des Nœuds:")
    noeud1_id = wrapper.add_node(
        reseau_id, "Réservoir Principal", "reservoir",
        elevation=150.0, pression_min=2.5, pression_max=4.0
    )
    noeud2_id = wrapper.add_node(
        reseau_id, "Point de Consommation 1", "consommation",
        elevation=120.0, demande=15.0, pression_min=1.5
    )
    noeud3_id = wrapper.add_node(
        reseau_id, "Point de Consommation 2", "consommation",
        elevation=110.0, demande=20.0, pression_min=1.5
    )
    print(f"   Nœuds créés: {noeud1_id}, {noeud2_id}, {noeud3_id}")
    
    # Test 6: Ajout de tronçons
    print("\n📋 6. Création des Tronçons:")
    troncon1_id = wrapper.add_pipe(
        reseau_id, "Tronçon 1", "Réservoir Principal", "Point de Consommation 1",
        longueur=200.0, diametre=150.0, rugosite=0.001, type_materiau="PEHD"
    )
    troncon2_id = wrapper.add_pipe(
        reseau_id, "Tronçon 2", "Point de Consommation 1", "Point de Consommation 2",
        longueur=150.0, diametre=100.0, rugosite=0.001, type_materiau="PEHD"
    )
    print(f"   Tronçons créés: {troncon1_id}, {troncon2_id}")
    
    # Test 7: Ajout de calculs
    print("\n📋 7. Ajout de Calculs:")
    calcul1_id = wrapper.add_calculation(
        "hardy_cross",
        {
            "pression_reservoir": 3.0,
            "debit_total": 35.0,
            "pertes_charge": 0.8
        },
        metadata={
            "algorithme": "hardy_cross_v2",
            "tolerance": 0.001,
            "iterations_max": 100
        }
    )
    calcul2_id = wrapper.add_calculation(
        "optimisation_diametres",
        {
            "couts_materiaux": 15000.0,
            "couts_excavation": 8000.0,
            "diametres_optimaux": [150, 100]
        },
        metadata={
            "algorithme": "genetic_algorithm",
            "population": 100,
            "generations": 50
        }
    )
    print(f"   Calculs ajoutés: {calcul1_id}, {calcul2_id}")
    
    # Test 8: Ajout de relevés terrain
    print("\n📋 8. Ajout de Relevés Terrain:")
    releve1_id = wrapper.add_field_survey(
        "pression", "Point 1", {"pression": 2.8, "debit": 15.0},
        coordonnees_gps="48.8566,2.3522", altitude=120.0, operateur="Technicien A"
    )
    releve2_id = wrapper.add_field_survey(
        "debit", "Point 2", {"pression": 1.8, "debit": 20.0},
        coordonnees_gps="48.8567,2.3523", altitude=110.0, operateur="Technicien B"
    )
    print(f"   Relevés ajoutés: {releve1_id}, {releve2_id}")
    
    # Test 9: Récupération du réseau complet
    print("\n📋 9. Récupération du Réseau Complet:")
    reseau_complet = wrapper.get_network_complete(reseau_id)
    if reseau_complet:
        print(f"   Réseau: {reseau_complet['nom_reseau']} ({reseau_complet['type_reseau']})")
        print(f"   Nœuds: {len(reseau_complet['noeuds'])}")
        print(f"   Tronçons: {len(reseau_complet['troncons'])}")
        print(f"   Hash: {reseau_complet['hash_reseau'][:16]}...")
    else:
        print("   ❌ Erreur lors de la récupération du réseau")
    
    # Test 10: Historique du projet
    print("\n📋 10. Historique du Projet:")
    historique = wrapper.get_project_history(20)
    print(f"   Nombre d'éléments: {len(historique)}")
    if historique:
        print(f"   Dernier calcul: {historique[0]['commande']}")
        print(f"   Module source: {historique[0]['module_source']}")
    
    # Test 11: Informations du projet
    print("\n📋 11. Informations du Projet:")
    project_info = wrapper.get_project_info()
    print(f"   Nom: {project_info.get('nom_projet', 'N/A')}")
    print(f"   Version: {project_info.get('version', 'N/A')}")
    print(f"   Auteur: {project_info.get('auteur', 'N/A')}")
    print(f"   Description: {project_info.get('description', 'N/A')}")
    
    print("\n✅ Test de fusion AEP terminé avec succès !")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        test_fusion_aep()
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
