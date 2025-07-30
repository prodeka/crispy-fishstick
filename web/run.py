#!/usr/bin/env python3
"""
Script de demarrage pour l'application Nanostruct Web
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifie que toutes les dependances sont installees"""
    try:
        import flask
        import flask_cors
        print("Dependances Flask installees")
        return True
    except ImportError as e:
        print(f"Dependance manquante: {e}")
        return False

def install_dependencies():
    """Installe les dependances si necessaire"""
    print("Installation des dependances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, cwd=Path(__file__).parent)
        print("Dependances installees avec succes")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation: {e}")
        return False

def main():
    """Fonction principale"""
    print("Demarrage de Nanostruct Web...")
    
    # Verifier les dependances
    if not check_dependencies():
        print("Installation automatique des dependances...")
        if not install_dependencies():
            print("Impossible d'installer les dependances")
            sys.exit(1)
    
    # Verifier que le fichier app.py existe
    app_file = Path(__file__).parent / "app.py"
    if not app_file.exists():
        print("Fichier app.py introuvable")
        sys.exit(1)
    
    # Lancer l'application
    print("Lancement du serveur web...")
    print("L'application sera accessible a l'adresse: http://localhost:5000")
    print("Mode developpement active")
    print("Appuyez sur Ctrl+C pour arreter le serveur")
    print("-" * 50)
    
    try:
        # Changer vers le repertoire de l'application
        os.chdir(Path(__file__).parent)
        
        # Lancer Flask
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nArret du serveur")
    except Exception as e:
        print(f"Erreur lors du demarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()