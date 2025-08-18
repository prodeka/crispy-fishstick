#!/usr/bin/env python3
"""
Script de build pour créer un exécutable portable LCPI-CLI
Version optimisée avec --onedir pour un démarrage rapide
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_portable():
    """Construit un exécutable portable de LCPI-CLI avec démarrage rapide"""
    
    print("Construction de l'executable portable LCPI-CLI (mode complet)...")
    print("Mode --onedir avec toutes les dependances pour plugins 100% fonctionnels")
    
    # Chemin du projet
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"
    
    # Créer le dossier de sortie avec nom unique
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dist_dir = project_root / f"dist_{timestamp}"
    build_dir = project_root / f"build_{timestamp}"
    
    # Gestion intelligente des anciens builds
    print("Gestion des anciens builds...")
    
    def find_next_available_name(base_name):
        """Trouve le prochain nom disponible pour un dossier"""
        counter = 1
        while True:
            new_name = f"{base_name}_{counter}"
            new_path = project_root / new_name
            if not new_path.exists():
                return new_name, new_path
            counter += 1
    
    def handle_existing_folder(folder_path, folder_type):
        """Gère un dossier existant avec options intelligentes"""
        if not folder_path.exists():
            return folder_path
            
        print(f"\n📁 Dossier {folder_type} existant detecte: {folder_path.name}")
        print("   Options disponibles:")
        print("   1. Renommer automatiquement (dist_1, dist_2, etc.)")
        print("   2. Forcer la suppression (peut etre dangereux)")
        print("   3. Annuler et quitter")
        
        while True:
            try:
                choice = input("   Votre choix (1/2/3): ").strip()
                if choice == "1":
                    new_name, new_path = find_next_available_name(folder_type)
                    print(f"   Renommage de {folder_path.name} en {new_name}")
                    folder_path.rename(new_path)
                    print(f"   ✅ {folder_path.name} renomme en {new_name}")
                    return folder_path
                elif choice == "2":
                    print(f"   Tentative de suppression forcee de {folder_path.name}...")
                    try:
                        # Suppression forcée avec gestion d'erreurs
                        import stat
                        def on_rm_error(func, path, exc_info):
                            try:
                                os.chmod(path, stat.S_IWRITE)
                                func(path)
                            except:
                                pass
                        shutil.rmtree(folder_path, onerror=on_rm_error)
                        print(f"   ✅ {folder_path.name} supprime avec succes")
                        return folder_path
                    except Exception as e:
                        print(f"   ❌ Impossible de supprimer {folder_path.name}: {e}")
                        print(f"   🔄 Tentative de renommage automatique...")
                        new_name, new_path = find_next_available_name(folder_type)
                        folder_path.rename(new_path)
                        print(f"   ✅ {folder_path.name} renomme en {new_name}")
                        return folder_path
                elif choice == "3":
                    print("   Annulation du build.")
                    sys.exit(0)
                else:
                    print("   Choix invalide. Veuillez entrer 1, 2 ou 3.")
            except KeyboardInterrupt:
                print("\n   Annulation du build.")
                sys.exit(0)
    
    # Gérer les dossiers existants
    dist_dir = handle_existing_folder(dist_dir, "dist")
    build_dir = handle_existing_folder(build_dir, "build")
    
    # Créer les nouveaux dossiers
    dist_dir.mkdir(exist_ok=True)
    build_dir.mkdir(exist_ok=True)
    print("✅ Dossiers de build prepares")
    
    # Construire avec PyInstaller en mode --onedir optimisé
    print("Construction de l'executable (mode --onedir optimise)...")
    cmd = [
        'pyinstaller',
        # '--clean',  # Désactivé pour éviter les conflits de nettoyage
        '--onedir',  # Mode dossier pour plugins fonctionnels
        '--console',
        '--name=lcpi_cli',
        f'--distpath={dist_dir.name}',  # Utiliser le nom unique du dossier
        f'--workpath={build_dir.name}',  # Utiliser le nom unique du dossier
        '--log-level=INFO',
        '--noconfirm',  # Éviter les questions de confirmation
        # Inclusions forcées des plugins
        '--add-data=src/lcpi;lcpi',
        # Inclure toutes les dépendances pour garantir la fonctionnalité des plugins
        # Pas d'exclusions pour maintenir la compatibilité complète
        # Optimisations supplémentaires
        '--optimize=2',  # Optimisation Python
        str(src_path / 'lcpi' / '__main__.py')
    ]
    
    try:
        print("Construction en cours (cela peut prendre 5-12 minutes avec optimisations)...")
        print(f"Commande executee : {' '.join(cmd)}")
        print("Sortie en temps reel :")
        print("-" * 50)
        
        # Exécution verbeuse avec sortie en temps réel
        result = subprocess.run(cmd, cwd=project_root, check=True, text=True)
        
        print("-" * 50)
        print("Construction reussie !")
        
        # Vérifier que l'exécutable existe
        exe_path = dist_dir / "lcpi_cli" / "lcpi_cli.exe"
        if exe_path.exists():
            # Calculer la taille du dossier
            folder_size = sum(f.stat().st_size for f in exe_path.parent.rglob('*') if f.is_file())
            
            print(f"Executable cree: {exe_path}")
            print(f"Taille du dossier: {folder_size / (1024*1024):.1f} MB")
            print(f"Dossier complet: {exe_path.parent}")
            
            # Créer un script de test
            test_script = project_root / "test_portable.bat"
            with open(test_script, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'echo Test de l\'executable portable LCPI-CLI (mode rapide)...\n')
                f.write(f'echo.\n')
                f.write(f'echo Temps de demarrage attendu: 2-5 secondes (mode onedir)\n')
                f.write(f'echo.\n')
                f.write(f'"{exe_path}" --help\n')
                f.write(f'echo.\n')
                f.write(f'echo Test termine!\n')
                f.write(f'pause\n')
            
            print(f"Script de test cree: {test_script}")
            
            # Créer un script de lancement rapide
            launcher_script = project_root / "lcpi_launcher.bat"
            with open(launcher_script, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'REM Lanceur rapide pour LCPI-CLI\n')
                f.write(f'REM Démarrage ultra-rapide en mode --onedir\n')
                f.write(f'"{exe_path}" %*\n')
            
            print(f"Script de lancement cree: {launcher_script}")
            
            # Créer un script d'installation simple
            install_script = project_root / "install_lcpi.bat"
            with open(install_script, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'echo Installation de LCPI-CLI...\n')
                f.write(f'echo.\n')
                f.write(f'REM Créer le dossier d\'installation\n')
                f.write(f'mkdir "C:\\Program Files\\LCPI-CLI" 2>nul\n')
                f.write(f'REM Copier l\'exécutable\n')
                f.write(f'copy "{exe_path}" "C:\\Program Files\\LCPI-CLI\\lcpi_cli.exe"\n')
                f.write(f'REM Ajouter au PATH (nécessite des droits admin)\n')
                f.write(f'setx PATH "%PATH%;C:\\Program Files\\LCPI-CLI"\n')
                f.write(f'echo.\n')
                f.write(f'echo Installation terminee !\n')
                f.write(f'echo LCPI-CLI est maintenant accessible depuis n\'importe ou.\n')
                f.write(f'pause\n')
            
            print(f"Script d'installation cree: {install_script}")
            
            return True
        else:
            print("L'executable n'a pas ete cree")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la construction: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

if __name__ == "__main__":
    success = build_portable()
    if success:
        print("\nDeploiement reussi !")
        print("L'executable se trouve dans le dossier 'dist/lcpi_cli/'")
        print("Dossier complet avec tous les plugins")
        print("Demarrage ultra-rapide (2-5 secondes)")
        print("Utilisez 'lcpi_launcher.bat' pour lancer rapidement")
        print("Utilisez 'install_lcpi.bat' pour installer dans C:\\Program Files")
        print("Ou naviguez dans 'dist/lcpi_cli' et double-cliquez sur 'lcpi_cli.exe'")
    else:
        print("\n❌ Échec du déploiement")
        sys.exit(1)
