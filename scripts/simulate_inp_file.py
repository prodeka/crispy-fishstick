#!/usr/bin/env python3
"""
Script pour simuler un fichier .inp EPANET avec LCPI AEP

Usage:
    python scripts/simulate_inp_file.py chemin/vers/fichier.inp
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.epanet_wrapper import EpanetSimulator

def simulate_inp_file(inp_file_path: str):
    """
    Simule un fichier .inp EPANET avec LCPI AEP
    
    Args:
        inp_file_path: Chemin vers le fichier .inp
    """
    
    print(f"🚀 SIMULATION FICHIER .INP: {inp_file_path}")
    print("=" * 60)
    
    # Vérifier que le fichier existe
    if not os.path.exists(inp_file_path):
        print(f"❌ ERREUR: Fichier {inp_file_path} introuvable")
        return False
    
    try:
        # Créer l'instance EPANET
        print("🔧 Initialisation EPANET...")
        epanet = EpanetSimulator()
        
        # Ouvrir le fichier .inp
        print(f"📁 Ouverture du fichier: {inp_file_path}")
        if not epanet.open_project(inp_file_path):
            print("❌ ERREUR: Impossible d'ouvrir le fichier .inp")
            return False
        
        print("✅ Fichier .inp ouvert avec succès")
        
        # Lancer la simulation hydraulique
        print("⚡ Lancement de la simulation hydraulique...")
        if not epanet.solve_hydraulics():
            print("❌ ERREUR: Échec de la simulation hydraulique")
            return False
        
        print("✅ Simulation hydraulique réussie")
        
        # Extraire les résultats
        print("📊 Extraction des résultats...")
        results = extract_epanet_results(epanet)
        
        # Afficher un résumé
        print("\n📋 RÉSUMÉ DES RÉSULTATS")
        print("=" * 40)
        print(f"   • Nombre de nœuds: {results['node_count']}")
        print(f"   • Nombre de conduites: {results['pipe_count']}")
        print(f"   • Nombre de réservoirs: {results['reservoir_count']}")
        print(f"   • Nombre de tanks: {results['tank_count']}")
        
        if 'statistics' in results:
            stats = results['statistics']
            print(f"   • Itérations: {stats.get('iterations', 'N/A')}")
            print(f"   • Erreur relative: {stats.get('relative_error', 'N/A')}")
            print(f"   • Erreur max tête: {stats.get('max_head_error', 'N/A')}")
        
        # Afficher quelques résultats de nœuds
        if results['nodes']:
            print(f"\n💧 RÉSULTATS NŒUDS (échantillon):")
            print("-" * 40)
            for i, (node_id, node_data) in enumerate(list(results['nodes'].items())[:5]):
                print(f"   {node_id}: Pression={node_data.get('pressure', 'N/A'):.2f} m")
        
        # Afficher quelques résultats de conduites
        if results['pipes']:
            print(f"\n🌊 RÉSULTATS CONDUITES (échantillon):")
            print("-" * 40)
            for i, (pipe_id, pipe_data) in enumerate(list(results['pipes'].items())[:5]):
                print(f"   {pipe_id}: Débit={pipe_data.get('flow', 'N/A'):.3f} m³/s")
        
        # Fermer le projet
        epanet.close_project()
        print("\n✅ Simulation terminée avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

def extract_epanet_results(epanet):
    """
    Extrait les résultats d'une simulation EPANET
    
    Args:
        epanet: Instance EpanetSimulator
        
    Returns:
        Dict contenant les résultats
    """
    results = {
        "nodes": {},
        "pipes": {},
        "statistics": {}
    }
    
    try:
        # Statistiques de simulation
        results["statistics"] = {
            "iterations": epanet.getstatistic(0),  # EN_ITERATIONS
            "relative_error": epanet.getstatistic(1),  # EN_RELATIVEERROR
            "max_head_error": epanet.getstatistic(2),  # EN_MAXHEADERROR
            "max_flow_change": epanet.getstatistic(3),  # EN_MAXFLOWCHANGE
            "mass_balance": epanet.getstatistic(4)  # EN_MASSBALANCE
        }
        
        # Résultats des nœuds
        node_count = epanet.getcount(0)  # EN_NODECOUNT
        results["node_count"] = node_count
        
        for i in range(1, node_count + 1):
            node_id = epanet.getnodeid(i)
            results["nodes"][node_id] = {
                "pressure": epanet.getnodevalue(i, 0),  # EN_PRESSURE
                "head": epanet.getnodevalue(i, 1),  # EN_HEAD
                "demand": epanet.getnodevalue(i, 2),  # EN_DEMAND
                "quality": epanet.getnodevalue(i, 3)  # EN_QUALITY
            }
        
        # Résultats des conduites
        pipe_count = epanet.getcount(1)  # EN_LINKCOUNT
        results["pipe_count"] = pipe_count
        
        for i in range(1, pipe_count + 1):
            link_id = epanet.getlinkid(i)
            results["pipes"][link_id] = {
                "flow": epanet.getlinkvalue(i, 0),  # EN_FLOW
                "velocity": epanet.getlinkvalue(i, 1),  # EN_VELOCITY
                "headloss": epanet.getlinkvalue(i, 2),  # EN_HEADLOSS
                "quality": epanet.getlinkvalue(i, 3),  # EN_QUALITY
                "status": epanet.getlinkvalue(i, 4)  # EN_STATUS
            }
        
        # Compter les types de nœuds
        reservoir_count = 0
        tank_count = 0
        
        for i in range(1, node_count + 1):
            node_type = epanet.getnodetype(i)
            if node_type == 0:  # EN_RESERVOIR
                reservoir_count += 1
            elif node_type == 1:  # EN_TANK
                tank_count += 1
        
        results["reservoir_count"] = reservoir_count
        results["tank_count"] = tank_count
        
    except Exception as e:
        print(f"⚠️  Avertissement lors de l'extraction des résultats: {e}")
    
    return results

def main():
    """Fonction principale"""
    
    if len(sys.argv) != 2:
        print("Usage: python scripts/simulate_inp_file.py <chemin_vers_fichier.inp>")
        print("\nExemples:")
        print("  python scripts/simulate_inp_file.py examples/mon_reseau.inp")
        print("  python scripts/simulate_inp_file.py C:/Users/moi/reseau.inp")
        return
    
    inp_file_path = sys.argv[1]
    
    # Simuler le fichier
    success = simulate_inp_file(inp_file_path)
    
    if success:
        print("\n🎉 Simulation terminée avec succès!")
    else:
        print("\n❌ Échec de la simulation")
        sys.exit(1)

if __name__ == "__main__":
    main() 