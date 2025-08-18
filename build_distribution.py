#!/usr/bin/env python3
"""
Script de lancement principal pour la création de distribution LCPI-CLI
Redirige vers le script dans le dossier scripts/
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Lance le script de distribution depuis le dossier scripts"""
    
    # Chemin vers le script de distribution
    script_path = Path(__file__).parent / "scripts" / "create_distribution.py"
    
    if not script_path.exists():
        print("❌ Script de distribution non trouvé :")
        print(f"   {script_path}")
        print("\n📁 Vérifiez que le fichier existe dans le dossier scripts/")
        return 1
    
    print("🚀 Lancement du script de distribution...")
    print(f"📂 Script : {script_path}")
    print()
    
    # Lancer le script de distribution
    try:
        result = subprocess.run([sys.executable, str(script_path)], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n❌ Interruption par l'utilisateur")
        return 1

if __name__ == "__main__":
    sys.exit(main())
