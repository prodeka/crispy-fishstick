#!/usr/bin/env python3
"""
Script de démarrage pour l'application Nanostruct Web Avancée
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    try:
        import flask
        import flask_cors
        import pandas
        print("✅ Dépendances Flask et pandas installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        return False

def install_dependencies():
    """Installe les dépendances si nécessaire"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, cwd=Path(__file__).parent)
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Démarrage de Nanostruct Web Avancée...")
    print("📋 Version 2.0 - Fonctionnalités avancées")
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("📦 Installation automatique des dépendances...")
        if not install_dependencies():
            print("❌ Impossible d'installer les dépendances")
            sys.exit(1)
    
    # Vérifier que le fichier app_advanced.py existe
    app_file = Path(__file__).parent / "app_advanced.py"
    if not app_file.exists():
        print("❌ Fichier app_advanced.py introuvable")
        sys.exit(1)
    
    # Lancer l'application
    print("🌐 Lancement du serveur web avancé...")
    print("📱 L'application sera accessible à l'adresse: http://localhost:5001")
    print("🔧 Mode développement activé")
    print("⚡ Fonctionnalités avancées activées")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("-" * 60)
    
    try:
        # Changer vers le répertoire de l'application
        os.chdir(Path(__file__).parent)
        
        # Lancer Flask avec la version avancée
        subprocess.run([sys.executable, "app_advanced.py"])
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur avancé")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 