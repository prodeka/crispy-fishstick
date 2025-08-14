#!/usr/bin/env python3
"""
Script pour convertir un fichier .inp EPANET en YAML LCPI et le simuler

Usage:
    python scripts/convert_inp_to_yaml.py chemin/vers/fichier.inp
"""

import sys
import os
import yaml
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.epanet_wrapper import EpanetSimulator

def parse_inp_file(inp_file_path: str):
    """
    Parse un fichier .inp EPANET et extrait les données
    
    Args:
        inp_file_path: Chemin vers le fichier .inp
        
    Returns:
        Dict contenant les données du réseau
    """
    
    print(f"📁 Lecture du fichier .inp: {inp_file_path}")
    
    network_data = {
        "network": {
            "nodes": {},
            "pipes": {}
        },
        "metadata": {
            "source": "EPANET .inp file",
            "original_file": inp_file_path
        }
    }
    
    try:
        with open(inp_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Ignorer les commentaires et lignes vides
            if not line or line.startswith(';') or line.startswith('['):
                continue
            
            # Détecter les sections
            if line.upper() == '[JUNCTIONS]':
                current_section = 'junctions'
                continue
            elif line.upper() == '[RESERVOIRS]':
                current_section = 'reservoirs'
                continue
            elif line.upper() == '[TANKS]':
                current_section = 'tanks'
                continue
            elif line.upper() == '[PIPES]':
                current_section = 'pipes'
                continue
            elif line.upper() == '[PUMPS]':
                current_section = 'pumps'
                continue
            elif line.upper() == '[VALVES]':
                current_section = 'valves'
                continue
            
            # Parser les données selon la section
            if current_section == 'junctions':
                parts = line.split()
                if len(parts) >= 3:
                    node_id = parts[0]
                    network_data["network"]["nodes"][node_id] = {
                        "type": "junction",
                        "elevation": float(parts[1]),
                        "demand": float(parts[2]) if len(parts) > 2 else 0.0
                    }
            
            elif current_section == 'reservoirs':
                parts = line.split()
                if len(parts) >= 2:
                    node_id = parts[0]
                    network_data["network"]["nodes"][node_id] = {
                        "type": "reservoir",
                        "elevation": float(parts[1]),
                        "demand": 0.0
                    }
            
            elif current_section == 'tanks':
                parts = line.split()
                if len(parts) >= 4:
                    node_id = parts[0]
                    network_data["network"]["nodes"][node_id] = {
                        "type": "tank",
                        "elevation": float(parts[1]),
                        "initial_level": float(parts[2]),
                        "minimum_level": float(parts[3]),
                        "maximum_level": float(parts[4]) if len(parts) > 4 else float(parts[2]) + 10,
                        "demand": 0.0
                    }
            
            elif current_section == 'pipes':
                parts = line.split()
                if len(parts) >= 6:
                    pipe_id = parts[0]
                    network_data["network"]["pipes"][pipe_id] = {
                        "from_node": parts[1],
                        "to_node": parts[2],
                        "length": float(parts[3]),
                        "diameter": float(parts[4]),
                        "roughness": float(parts[5])
                    }
            
            elif current_section == 'pumps':
                parts = line.split()
                if len(parts) >= 3:
                    pump_id = parts[0]
                    network_data["network"]["pipes"][pump_id] = {
                        "from_node": parts[1],
                        "to_node": parts[2],
                        "type": "pump",
                        "pump_curve": parts[3] if len(parts) > 3 else "HEAD"
                    }
            
            elif current_section == 'valves':
                parts = line.split()
                if len(parts) >= 4:
                    valve_id = parts[0]
                    network_data["network"]["pipes"][valve_id] = {
                        "from_node": parts[1],
                        "to_node": parts[2],
                        "type": "valve",
                        "valve_type": parts[3],
                        "setting": float(parts[4]) if len(parts) > 4 else 0.0
                    }
        
        print(f"✅ Fichier .inp parsé avec succès")
        print(f"   • Nœuds: {len(network_data['network']['nodes'])}")
        print(f"   • Conduites: {len(network_data['network']['pipes'])}")
        
        return network_data
        
    except Exception as e:
        print(f"❌ ERREUR lors du parsing: {e}")
        return None

def save_yaml_file(network_data, output_path: str):
    """
    Sauvegarde les données réseau au format YAML
    
    Args:
        network_data: Données du réseau
        output_path: Chemin de sortie
    """
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(network_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"✅ Fichier YAML sauvegardé: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERREUR lors de la sauvegarde: {e}")
        return False

def simulate_with_lcpi(network_data):
    """
    Simule le réseau avec LCPI AEP
    
    Args:
        network_data: Données du réseau
    """
    
    print("\n🚀 SIMULATION AVEC LCPI AEP")
    print("=" * 40)
    
    try:
        from lcpi.aep.core.epanet_integration import run_epanet_with_diagnostics
        
        # Lancer la simulation avec diagnostics
        results = run_epanet_with_diagnostics(network_data)
        
        if results['success']:
            print("✅ Simulation LCPI AEP réussie")
            
            # Afficher un résumé des résultats
            if 'epanet_results' in results:
                epanet_results = results['epanet_results']
                print(f"\n📊 RÉSULTATS:")
                print(f"   • Nœuds simulés: {len(epanet_results.get('nodes', {}))}")
                print(f"   • Conduites simulées: {len(epanet_results.get('pipes', {}))}")
                
                # Afficher quelques résultats
                if epanet_results.get('nodes'):
                    print(f"\n💧 PRESSIONS (échantillon):")
                    for i, (node_id, node_data) in enumerate(list(epanet_results['nodes'].items())[:3]):
                        pressure = node_data.get('pressure', 'N/A')
                        print(f"   {node_id}: {pressure:.2f} m" if pressure != 'N/A' else f"   {node_id}: {pressure}")
                
                if epanet_results.get('pipes'):
                    print(f"\n🌊 DÉBITS (échantillon):")
                    for i, (pipe_id, pipe_data) in enumerate(list(epanet_results['pipes'].items())[:3]):
                        flow = pipe_data.get('flow', 'N/A')
                        print(f"   {pipe_id}: {flow:.3f} m³/s" if flow != 'N/A' else f"   {pipe_id}: {flow}")
            
        else:
            print("❌ Échec de la simulation LCPI AEP")
            if 'errors' in results:
                for error in results['errors']:
                    print(f"   • {error}")
        
        return results['success']
        
    except Exception as e:
        print(f"❌ ERREUR lors de la simulation: {e}")
        return False

def main():
    """Fonction principale"""
    
    if len(sys.argv) != 2:
        print("Usage: python scripts/convert_inp_to_yaml.py <chemin_vers_fichier.inp>")
        print("\nExemples:")
        print("  python scripts/convert_inp_to_yaml.py examples/mon_reseau.inp")
        print("  python scripts/convert_inp_to_yaml.py C:/Users/moi/reseau.inp")
        return
    
    inp_file_path = sys.argv[1]
    
    # Vérifier que le fichier existe
    if not os.path.exists(inp_file_path):
        print(f"❌ ERREUR: Fichier {inp_file_path} introuvable")
        return
    
    # Parser le fichier .inp
    network_data = parse_inp_file(inp_file_path)
    if not network_data:
        print("❌ Échec du parsing du fichier .inp")
        return
    
    # Générer le nom du fichier YAML
    inp_path = Path(inp_file_path)
    yaml_path = inp_path.with_suffix('.yml')
    
    # Sauvegarder en YAML
    if not save_yaml_file(network_data, str(yaml_path)):
        print("❌ Échec de la sauvegarde YAML")
        return
    
    # Simuler avec LCPI AEP
    success = simulate_with_lcpi(network_data)
    
    if success:
        print(f"\n🎉 Conversion et simulation terminées avec succès!")
        print(f"📁 Fichier YAML créé: {yaml_path}")
        print(f"📁 Fichier .inp original: {inp_file_path}")
    else:
        print(f"\n❌ Échec de la simulation")
        print(f"📁 Fichier YAML créé: {yaml_path} (vous pouvez le corriger manuellement)")

if __name__ == "__main__":
    main() 