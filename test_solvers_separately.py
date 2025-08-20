#!/usr/bin/env python3
"""
Script de test pour exécuter les solveurs séparément
"""

import subprocess
import json
from pathlib import Path

def run_solver_test():
    """Exécute les solveurs séparément pour tester"""
    
    base_cmd = [
        "lcpi", "aep", "network-optimize-unified",
        "src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp",
        "--method", "genetic",
        "--pression-min", "12",
        "--vitesse-max", "2.0",
        "--output"
    ]
    
    solvers = ["epanet", "lcpi"]
    
    for solver in solvers:
        output_file = f"results/test_{solver}_separate.json"
        cmd = base_cmd + [output_file, "--solver", solver]
        
        print(f"🔄 Exécution de {solver}...")
        print(f"   Commande: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print(f"✅ {solver} terminé avec succès")
                
                # Vérifier le contenu
                if Path(output_file).exists():
                    with open(output_file, 'r') as f:
                        data = json.load(f)
                    solver_used = data.get('meta', {}).get('solver', 'unknown')
                    print(f"   Solveur utilisé: {solver_used}")
                    print(f"   CAPEX: {data.get('proposals', [{}])[0].get('CAPEX', 'N/A')}")
            else:
                print(f"❌ {solver} échoué")
                print(f"   Erreur: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"⏰ {solver} timeout")
        except Exception as e:
            print(f"❌ Erreur {solver}: {e}")

if __name__ == "__main__":
    run_solver_test()
