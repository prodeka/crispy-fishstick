#!/usr/bin/env python3
"""
Script d'installation LCPI-CLI avec choix entre portable et système
Permet d'installer LCPI soit en mode portable soit en mode système
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Affiche la bannière d'accueil"""
    print("=" * 60)
    print("    LCPI-CLI - Installation avec choix")
    print("=" * 60)
    print()

def get_installation_choice():
    """Demande à l'utilisateur son choix d'installation"""
    print("📋 CHOIX D'INSTALLATION :")
    print()
    print("1. 🚀 Installation système (recommandée)")
    print("   ✅ lcpi disponible depuis n'importe quel répertoire")
    print("   ✅ Installation complète avec plugins")
    print("   ✅ Mise à jour facile")
    print("   ❌ Nécessite Python installé")
    print()
    print("2. 📦 Version portable (exécutable autonome)")
    print("   ✅ Exécutable autonome (pas besoin de Python)")
    print("   ✅ Distribution facile")
    print("   ✅ Fonctionne sur n'importe quel PC Windows")
    print("   ❌ Plus volumineux")
    print("   ❌ Démarrage plus lent")
    print()
    print("3. 🔄 Les deux (recommandé pour développeurs)")
    print("   ✅ Installation système + exécutable portable")
    print("   ✅ Flexibilité maximale")
    print("   ❌ Plus d'espace disque")
    print()
    
    while True:
        choice = input("Choisissez votre option (1/2/3) : ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("❌ Veuillez choisir 1, 2 ou 3.")

def install_system():
    """Installation système avec pip"""
    print("\n🚀 Installation système en cours...")
    
    try:
        # Vérifier que pip est disponible
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        
        # Installer en mode éditable
        project_root = Path(__file__).parent
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=project_root, check=True)
        
        print("✅ Installation système réussie !")
        print("🎉 Vous pouvez maintenant utiliser 'lcpi' depuis n'importe où.")
        
        # Tester l'installation
        try:
            result = subprocess.run(["lcpi", "--help"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Test de l'installation réussi !")
                return True
            else:
                print("⚠️  Installation réussie mais test échoué.")
                return True
        except Exception as e:
            print(f"⚠️  Test échoué : {e}")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation système : {e}")
        return False

def build_portable():
    """Construction de l'exécutable portable"""
    print("\n📦 Construction de l'exécutable portable...")
    
    try:
        # Utiliser le script de build existant
        build_script = Path(__file__).parent / "build_portable.py"
        if build_script.exists():
            subprocess.run([sys.executable, str(build_script)], check=True)
            print("✅ Construction portable réussie !")
            return True
        else:
            print("❌ Script de build non trouvé.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la construction portable : {e}")
        return False

def create_launcher_scripts():
    """Crée des scripts de lancement"""
    print("\n🚀 Création des scripts de lancement...")
    
    project_root = Path(__file__).parent
    
    # Script pour l'installation système
    system_launcher = project_root / "lcpi_system.bat"
    with open(system_launcher, 'w') as f:
        f.write("@echo off\n")
        f.write("REM Lanceur pour installation système\n")
        f.write("lcpi %*\n")
    
    # Script pour la version portable
    portable_launcher = project_root / "lcpi_portable.bat"
    portable_exe = project_root / "dist" / "lcpi" / "lcpi.exe"
    if portable_exe.exists():
        with open(portable_launcher, 'w') as f:
            f.write("@echo off\n")
            f.write("REM Lanceur pour version portable\n")
            f.write(f'"{portable_exe}" %*\n')
    
    print("✅ Scripts de lancement créés !")

def display_usage_instructions(choice):
    """Affiche les instructions d'utilisation"""
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION TERMINÉE !")
    print("=" * 60)
    print()
    
    if choice == '1':
        print("📋 UTILISATION (Installation système) :")
        print()
        print("🚀 Lancer LCPI depuis n'importe où :")
        print("   lcpi --help")
        print("   lcpi plugins install beton")
        print("   lcpi shell")
        print()
        print("📁 Ou utiliser le script de lancement :")
        print("   lcpi_system.bat --help")
        
    elif choice == '2':
        print("📋 UTILISATION (Version portable) :")
        print()
        print("🚀 Lancer LCPI :")
        print("   dist\\lcpi\\lcpi.exe --help")
        print("   lcpi_portable.bat --help")
        print()
        print("📁 Ou naviguer dans dist\\lcpi et double-cliquer sur lcpi.exe")
        
    elif choice == '3':
        print("📋 UTILISATION (Les deux versions) :")
        print()
        print("🚀 Installation système (recommandée) :")
        print("   lcpi --help")
        print("   lcpi_system.bat --help")
        print()
        print("📦 Version portable :")
        print("   dist\\lcpi\\lcpi.exe --help")
        print("   lcpi_portable.bat --help")
    
    print()
    print("📚 Documentation :")
    print("   - docs/GUIDE_UTILISATION.md")
    print("   - docs/NOUVELLES_FONCTIONNALITES.md")
    print()
    print("🔧 Support :")
    print("   - Email: support@lcpi-cli.com")
    print("   - GitHub: https://github.com/lcpi-cli")
    print("=" * 60)

def main():
    """Fonction principale"""
    print_banner()
    
    # Demander le choix d'installation
    choice = get_installation_choice()
    
    success = True
    
    if choice == '1':
        # Installation système uniquement
        success = install_system()
        
    elif choice == '2':
        # Version portable uniquement
        success = build_portable()
        
    elif choice == '3':
        # Les deux
        success_system = install_system()
        success_portable = build_portable()
        success = success_system and success_portable
    
    if success:
        # Créer les scripts de lancement
        create_launcher_scripts()
        
        # Afficher les instructions
        display_usage_instructions(choice)
    else:
        print("\n❌ L'installation a échoué.")
        print("💡 Vérifiez que Python et pip sont installés correctement.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Installation interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
    finally:
        print("\n📝 Fin du script d'installation.")
        input("Appuyez sur Entrée pour quitter...")
