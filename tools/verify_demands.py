#!/usr/bin/env python3
"""
Script de test pour vérifier la gestion des demandes dans le fichier INP temporaire.
"""

import tempfile
import os
from pathlib import Path

def verify_demands_in_temp_file():
    """Vérifie le contenu du fichier temporaire le plus récent."""
    
    # Chercher le fichier temporaire le plus récent
    temp_dir = Path(tempfile.gettempdir())
    demand_files = list(temp_dir.glob("*.demand_filled.inp"))
    
    if not demand_files:
        print("❌ Aucun fichier temporaire .demand_filled.inp trouvé")
        return
    
    # Prendre le plus récent
    latest_file = max(demand_files, key=lambda x: x.stat().st_mtime)
    print(f"🔍 Vérification du fichier : {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Analyser les sections
        junctions_demands = []
        demands_section = []
        in_junctions = False
        in_demands = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('[JUNCTIONS]'):
                in_junctions = True
                in_demands = False
                continue
            elif line.startswith('[DEMANDS]'):
                in_junctions = False
                in_demands = True
                continue
            elif line.startswith('['):
                in_junctions = False
                in_demands = False
                continue
            
            if in_junctions and line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        demand = float(parts[2])
                        if demand > 0:
                            junctions_demands.append((parts[0], demand))
                    except ValueError:
                        pass
            
            elif in_demands and line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        demand = float(parts[1])
                        demands_section.append((parts[0], demand))
                    except ValueError:
                        pass
        
        # Résultats
        print(f"\n📊 ANALYSE DES DEMANDES :")
        print(f"   [JUNCTIONS] avec demande > 0 : {len(junctions_demands)}")
        print(f"   [DEMANDS] : {len(demands_section)}")
        
        if junctions_demands:
            print(f"\n⚠️  PROBLÈME : Demandes > 0 trouvées dans [JUNCTIONS] :")
            for node, demand in junctions_demands[:5]:  # Afficher les 5 premiers
                print(f"      {node}: {demand}")
            if len(junctions_demands) > 5:
                print(f"      ... et {len(junctions_demands) - 5} autres")
        else:
            print(f"\n✅ SUCCÈS : Aucune demande > 0 dans [JUNCTIONS]")
        
        if demands_section:
            total_demand = sum(demand for _, demand in demands_section)
            print(f"\n📈 Section [DEMANDS] :")
            print(f"   Total : {total_demand:.4f}")
            print(f"   Moyenne : {total_demand/len(demands_section):.4f}")
        
        # Vérification finale
        if not junctions_demands and demands_section:
            print(f"\n🎉 CORRECTION RÉUSSIE : Double comptage évité !")
        else:
            print(f"\n❌ PROBLÈME PERSISTANT : Double comptage possible")
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")

if __name__ == "__main__":
    verify_demands_in_temp_file()
