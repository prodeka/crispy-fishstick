#!/usr/bin/env python3
"""
Script de création de packages de distribution LCPI-CLI
Crée automatiquement tous les types de distribution
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def print_banner():
    """Affiche la bannière"""
    print("=" * 60)
    print("    LCPI-CLI - Création de distribution")
    print("=" * 60)
    print()

def get_distribution_choice():
    """Demande le type de distribution"""
    print("📦 TYPES DE DISTRIBUTION :")
    print()
    print("1. 📋 Package pip (installation système)")
    print("   ✅ Distribution via pip")
    print("   ✅ Installation facile")
    print("   ✅ Mise à jour automatique")
    print()
    print("2. 📁 Archive portable (exécutable autonome)")
    print("   ✅ Exécutable autonome")
    print("   ✅ Pas besoin de Python")
    print("   ✅ Distribution simple")
    print()
    print("3. 🔄 Distribution complète (recommandée)")
    print("   ✅ Package pip + archive portable")
    print("   ✅ Flexibilité maximale")
    print("   ✅ Couvre tous les cas d'usage")
    print()
    
    while True:
        choice = input("Choisissez le type de distribution (1/2/3) : ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("❌ Veuillez choisir 1, 2 ou 3.")

def create_pip_package():
    """Crée un package pip"""
    print("\n📋 Création du package pip...")
    print("🔧 Cette option crée un package pip pour installation système")
    print("✅ Résultat : 'lcpi' disponible depuis n'importe quel répertoire")
    print()
    
    try:
        print("🧹 Nettoyage des anciens builds...")
        # Nettoyer les anciens builds avec gestion d'erreurs
        for folder in ['build', 'dist']:
            if os.path.exists(folder):
                print(f"   Suppression de {folder}/")
                try:
                    shutil.rmtree(folder)
                except OSError as e:
                    print(f"   ⚠️  Impossible de supprimer {folder}/ : {e}")
                    print(f"   🔄 Tentative de suppression forcée...")
                    try:
                        # Tentative avec force=True (Windows)
                        import stat
                        def on_rm_error(func, path, exc_info):
                            # Changer les permissions et réessayer
                            os.chmod(path, stat.S_IWRITE)
                            os.unlink(path)
                        
                        shutil.rmtree(folder, onerror=on_rm_error)
                        print(f"   ✅ {folder}/ supprimé avec succès")
                    except Exception as e2:
                        print(f"   ❌ Échec de la suppression de {folder}/ : {e2}")
                        print(f"   ⚠️  Continuation sans nettoyage...")
        print("✅ Nettoyage terminé")
        
        print("\n🔨 Création du package pip...")
        print("   Commande : python -m build")
        print("📋 Sortie en temps réel :")
        print("-" * 50)
        
        # Créer le package avec build (sortie en temps réel)
        print("   🔄 Exécution de la commande...")
        process = subprocess.Popen(
            [sys.executable, "-m", "build"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Afficher la sortie en temps réel
        for line in process.stdout:
            print(f"   {line.rstrip()}")
        
        # Attendre la fin du processus
        return_code = process.wait()
        
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, "python -m build")
        
        print("-" * 50)
        print("✅ Package pip créé avec succès !")
        
        # Lister les fichiers créés
        print("\n📁 Fichiers créés dans dist/ :")
        dist_files = list(Path("dist").glob("*"))
        total_size = 0
        for file in dist_files:
            size = file.stat().st_size / (1024*1024)
            total_size += size
            print(f"   📦 {file.name} ({size:.1f} MB)")
        print(f"   📊 Taille totale : {total_size:.1f} MB")
        
        print("\n🎯 Utilisation pour l'utilisateur :")
        print("   pip install dist/lcpi-cli-*.whl")
        print("   lcpi --help")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création du package pip : {e}")
        print(f"📋 Sortie d'erreur : {e.stderr}")
        return False

def create_portable_archive():
    """Crée une archive portable"""
    print("\n📁 Création de l'archive portable...")
    print("🔧 Cette option crée un exécutable portable autonome")
    print("✅ Résultat : Exécutable qui fonctionne sans Python installé")
    print()
    
    try:
        print("🔨 Construction de l'exécutable portable...")
        # Construire l'exécutable portable
        build_script = Path(__file__).parent / "build_portable.py"
        if build_script.exists():
            print(f"   Utilisation du script : {build_script}")
            print("   ⏱️  Construction en cours (peut prendre 5-10 minutes)...")
            print("📋 Sortie en temps réel :")
            print("-" * 50)
            
            # Exécuter avec sortie en temps réel
            process = subprocess.Popen(
                [sys.executable, str(build_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Afficher la sortie en temps réel
            for line in process.stdout:
                print(f"   {line.rstrip()}")
            
            # Attendre la fin du processus
            return_code = process.wait()
            
            if return_code != 0:
                raise subprocess.CalledProcessError(return_code, str(build_script))
            
            print("-" * 50)
            print("✅ Construction de l'exécutable terminée !")
        else:
            print("❌ Script de build portable non trouvé.")
            print("   Vérifiez que build_portable.py existe dans le répertoire.")
            return False
        
        print("\n📦 Création de l'archive ZIP...")
        # Créer l'archive ZIP
        portable_dir = Path(__file__).parent.parent / "dist/lcpi"
        if not portable_dir.exists():
            print("❌ Dossier portable non trouvé.")
            print(f"   Dossier attendu : {portable_dir}")
            return False
        
        print(f"   Dossier source : {portable_dir}")
        
        # Nom de l'archive avec version et date
        version = "2.1.0"  # À récupérer depuis pyproject.toml
        date = datetime.now().strftime("%Y%m%d")
        archive_name = f"lcpi-cli-portable-v{version}-{date}.zip"
        
        print(f"   Archive de destination : {archive_name}")
        print("   📝 Compression en cours...")
        
        # Créer l'archive
        file_count = 0
        total_size = 0
        archive_path = Path(__file__).parent.parent / archive_name
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(portable_dir.parent)
                    zipf.write(file_path, arcname)
                    file_count += 1
                    total_size += file_path.stat().st_size
        
        # Afficher les informations
        archive_size = archive_path.stat().st_size / (1024*1024)
        print("✅ Archive portable créée avec succès !")
        print(f"📁 Archive : {archive_name}")
        print(f"📦 Taille de l'archive : {archive_size:.1f} MB")
        print(f"📊 Fichiers inclus : {file_count}")
        print(f"📊 Taille originale : {total_size / (1024*1024):.1f} MB")
        print(f"📊 Taux de compression : {((total_size - archive_size * 1024*1024) / total_size * 100):.1f}%")
        
        print("\n🎯 Utilisation pour l'utilisateur :")
        print("   1. Décompresser le ZIP")
        print("   2. Naviguer dans le dossier lcpi")
        print("   3. Double-cliquer sur lcpi.exe")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'archive portable : {e}")
        print(f"📋 Détails de l'erreur : {type(e).__name__}")
        return False

def create_complete_distribution():
    """Crée une distribution complète"""
    print("\n🔄 Création de la distribution complète...")
    
    success_pip = create_pip_package()
    success_portable = create_portable_archive()
    
    if success_pip and success_portable:
        # Créer un fichier README de distribution
        create_distribution_readme()
        print("✅ Distribution complète créée avec succès !")
        return True
    else:
        print("❌ Erreur lors de la création de la distribution complète.")
        return False

def create_distribution_readme():
    """Crée un README pour la distribution"""
    readme_content = """# LCPI-CLI Distribution

## 📦 Contenu de cette distribution

### Package pip (installation système)
- `lcpi-cli-*.whl` : Package pip pour installation système
- Installation : `pip install lcpi-cli-*.whl`
- Utilisation : `lcpi --help` (disponible partout)

### Archive portable (exécutable autonome)
- `lcpi-cli-portable-*.zip` : Exécutable portable
- Extraction : Décompresser le ZIP
- Utilisation : Double-cliquer sur `lcpi.exe`

## 🚀 Installation

### Option 1 : Installation système (recommandée)
```bash
pip install lcpi-cli-*.whl
lcpi --help
```

### Option 2 : Version portable
1. Décompresser `lcpi-cli-portable-*.zip`
2. Naviguer dans le dossier `lcpi`
3. Double-cliquer sur `lcpi.exe`

## 📚 Documentation
- Guide d'utilisation : docs/GUIDE_UTILISATION.md
- Nouvelles fonctionnalités : docs/NOUVELLES_FONCTIONNALITES.md

## 🔧 Support
- Email : support@lcpi-cli.com
- GitHub : https://github.com/lcpi-cli

---
*Distribution créée le {date}*
""".format(date=datetime.now().strftime("%d/%m/%Y à %H:%M"))

    readme_path = Path(__file__).parent.parent / "DISTRIBUTION_README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("📝 README de distribution créé : DISTRIBUTION_README.md")

def display_distribution_info(choice):
    """Affiche les informations de distribution"""
    print("\n" + "=" * 60)
    print("🎉 DISTRIBUTION CRÉÉE AVEC SUCCÈS !")
    print("=" * 60)
    print()
    
    if choice == '1':
        print("📋 DISTRIBUTION PIP :")
        print("📁 Fichiers à distribuer :")
        print("   - dist/lcpi-cli-*.whl")
        print("   - dist/lcpi-cli-*.tar.gz")
        print()
        print("📦 Installation pour l'utilisateur :")
        print("   pip install lcpi-cli-*.whl")
        print("   lcpi --help")
        
    elif choice == '2':
        print("📋 DISTRIBUTION PORTABLE :")
        print("📁 Fichier à distribuer :")
        print("   - lcpi-cli-portable-*.zip")
        print()
        print("📦 Utilisation pour l'utilisateur :")
        print("   1. Décompresser le ZIP")
        print("   2. Naviguer dans le dossier lcpi")
        print("   3. Double-cliquer sur lcpi.exe")
        
    elif choice == '3':
        print("📋 DISTRIBUTION COMPLÈTE :")
        print("📁 Fichiers à distribuer :")
        print("   - dist/lcpi-cli-*.whl (installation système)")
        print("   - lcpi-cli-portable-*.zip (version portable)")
        print("   - DISTRIBUTION_README.md (instructions)")
        print()
        print("📦 Options pour l'utilisateur :")
        print("   Option 1 : pip install lcpi-cli-*.whl")
        print("   Option 2 : Décompresser lcpi-cli-portable-*.zip")
    
    print()
    print("📤 MÉTHODES DE DISTRIBUTION :")
    print("   - Email (fichiers < 25 MB)")
    print("   - Google Drive / OneDrive")
    print("   - GitHub Releases")
    print("   - Serveur FTP")
    print("   - USB / Disque externe")
    print("=" * 60)

def main():
    """Fonction principale"""
    print_banner()
    
    # Demander le type de distribution
    choice = get_distribution_choice()
    
    success = False
    
    if choice == '1':
        success = create_pip_package()
    elif choice == '2':
        success = create_portable_archive()
    elif choice == '3':
        success = create_complete_distribution()
    
    if success:
        display_distribution_info(choice)
    else:
        print("\n❌ La création de la distribution a échoué.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Création de distribution interrompue.")
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
    finally:
        print("\n📝 Fin du script de distribution.")
        input("Appuyez sur Entrée pour quitter...")
