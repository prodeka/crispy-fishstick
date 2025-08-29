#!/usr/bin/env python3
"""
Script de monitoring pour suivre l'avancement de l'optimisation EPANET.
Objectif : Surveiller les fichiers de résultats et l'état de l'optimisation.
"""

import time
import json
from pathlib import Path
from datetime import datetime, timedelta

def check_epanet_progress():
    """Vérifie l'avancement de l'optimisation EPANET."""
    
    print("🔍 MONITORING DE L'OPTIMISATION EPANET")
    print("=" * 50)
    
    # Fichiers à surveiller
    target_file = "test_epanet_optimise"
    start_time = datetime.now()
    
    print(f"🎯 Fichier cible: {target_file}")
    print(f"⏰ Début du monitoring: {start_time.strftime('%H:%M:%S')}")
    print("")
    
    while True:
        current_time = datetime.now()
        elapsed = current_time - start_time
        
        print(f"⏱️  Temps écoulé: {elapsed.strftime('%M:%S')}")
        
        # Vérifier si le fichier existe
        if Path(target_file).exists():
            print(f"✅ Fichier créé: {target_file}")
            
            try:
                # Analyser le contenu
                with open(target_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print("📊 ANALYSE DES RÉSULTATS EPANET")
                print("-" * 40)
                
                if "proposals" in data and data["proposals"]:
                    best = data["proposals"][0]
                    print(f"💰 Coût: {best.get('CAPEX', 'N/A'):,} FCFA")
                    print(f"✅ Faisable: {best.get('constraints_ok', 'N/A')}")
                    print(f"⚡ Temps d'exécution: {data.get('execution_time', 'N/A')}s")
                    print(f"🔧 Évaluations: {data.get('evaluations', 'N/A'):,}")
                    print(f"📈 Générations: {data.get('generations', 'N/A')}")
                    print(f"👥 Population: {data.get('population', 'N/A')}")
                else:
                    print("⚠️  Aucune proposition trouvée")
                
                print("")
                print("🎉 OPTIMISATION EPANET TERMINÉE !")
                break
                
            except Exception as e:
                print(f"❌ Erreur lecture: {e}")
                break
        
        else:
            print("⏳ Fichier en cours de création...")
            
            # Vérifier s'il y a des fichiers temporaires
            temp_files = list(Path(".").glob(f"{target_file}*"))
            if temp_files:
                print(f"📁 Fichiers temporaires détectés: {[f.name for f in temp_files]}")
            
            # Vérifier l'utilisation CPU/mémoire (approximatif)
            print("💻 Vérification système...")
            
            # Attendre avant la prochaine vérification
            print("🔄 Attente 30 secondes...")
            time.sleep(30)
            print("")
    
    print("=" * 50)
    print("🔍 MONITORING TERMINÉ")

def main():
    """Fonction principale."""
    try:
        check_epanet_progress()
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main()
