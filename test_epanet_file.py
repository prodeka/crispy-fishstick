#!/usr/bin/env python3
"""Test simple du fichier .inp EPANET"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.aep.epanet_wrapper import EpanetSimulator

def test_epanet_file():
    """Test le fichier .inp avec EPANET"""
    
    inp_file = "temp_validation.inp"
    
    if not os.path.exists(inp_file):
        print(f"❌ Fichier {inp_file} non trouvé")
        return False
    
    print(f"🔍 Test du fichier {inp_file}")
    print(f"📏 Taille du fichier : {os.path.getsize(inp_file)} octets")
    
    # Lire les premières lignes pour vérifier le format
    with open(inp_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📄 Nombre de lignes : {len(lines)}")
    
    # Vérifier les sections principales
    sections = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            sections.append((i+1, line))
    
    print("📋 Sections trouvées :")
    for line_num, section in sections:
        print(f"   Ligne {line_num}: {section}")
    
    # Test avec EPANET
    try:
        epanet = EpanetSimulator()
        print("✅ EPANET initialisé")
        
        # Essayer d'ouvrir le fichier
        print("🔧 Tentative d'ouverture du fichier...")
        success = epanet.open_project(inp_file)
        
        if success:
            print("✅ Fichier ouvert avec succès")
            
            # Essayer de résoudre l'hydraulique
            print("🔧 Tentative de résolution hydraulique...")
            solve_success = epanet.solve_hydraulics()
            
            if solve_success:
                print("✅ Résolution hydraulique réussie")
                
                # Récupérer les résultats
                summary = epanet.get_network_summary()
                print(f"📊 Résumé du réseau : {summary}")
                
                # Fermer le projet
                epanet.close_project()
                return True
            else:
                print("❌ Échec de la résolution hydraulique")
                return False
        else:
            print("❌ Impossible d'ouvrir le fichier")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False

if __name__ == "__main__":
    success = test_epanet_file()
    if success:
        print("\n🎉 Test réussi !")
    else:
        print("\n💥 Test échoué !") 