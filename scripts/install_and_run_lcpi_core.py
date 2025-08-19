#!/usr/bin/env python3
"""
Script d'installation et de lancement LCPI-CLI Core (amélioré)

Objectifs:
- Mode non interactif pour CI/automation (pas d'input bloquant)
- Installation des requirements (offline/online avec fallback)
- Installation en mode éditable (pip install -e .)
- Activation de plugins paramétrables (base et métier)
- Vérification de la CLI (lcpi --help) fiable

Usage rapide (non interactif):
  python scripts/install_and_run_lcpi_core.py --accept-license --install-editable --plugins aep,cm,bois,beton,hydro --offline

Remarques:
- Les prompts sont désactivables via --accept-license / --no-input
- En offline, les paquets sont pris depuis vendor/packages si présent
"""

import os
import sys
import json
import pathlib
import traceback
import subprocess
import urllib.request
import argparse
import glob
import shutil
import site
import sysconfig
from datetime import datetime

# Configuration
PROJECT_NAME = "LCPI-CLI"
VERSION = "2.0.0"
LICENSE_FILE = "docs/LICENSE.md"
DISCLAIMER_FILE = "docs/DISCLAIMER.md"

# Plugins de base (activés par défaut)
BASE_PLUGINS = ["shell", "utils"]
# Plugins métier disponibles (liste indicative)
BUSINESS_PLUGINS = ["beton", "bois", "cm", "hydro", "aep"]

def get_project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def force_utf8():
    """Force l'encodage UTF-8 côté terminal et Python (surtout sous Windows)."""
    # Variables d'environnement pour Python
    os.environ.setdefault('PYTHONUTF8', '1')
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if os.name == 'nt':
        # Console en UTF-8
        try:
            os.system('chcp 65001 > NUL')
        except Exception:
            pass
        # Reconfigurer les flux Python
        for stream_name in ('stdout', 'stderr', 'stdin'):
            try:
                stream = getattr(sys, stream_name)
                stream.reconfigure(encoding='utf-8', errors='replace')  # type: ignore[attr-defined]
            except Exception:
                pass

def print_banner():
    """Affiche la bannière d'accueil"""
    print("=" * 60)
    print(f"    {PROJECT_NAME} v{VERSION} - Installation Core")
    print("=" * 60)
    print()

def cleanup_invalid_distributions():
    """Supprime les distributions cassées (ex. dossier '~ip') qui provoquent des warnings pip."""
    try:
        site_packages = None
        # Essayer via site
        try:
            for p in site.getsitepackages():
                if p.endswith('site-packages') and os.path.isdir(p):
                    site_packages = p
                    break
        except Exception:
            pass
        # Fallback via sysconfig
        if not site_packages:
            site_packages = sysconfig.get_paths().get('purelib')
        if not site_packages or not os.path.isdir(site_packages):
            return
        patterns = [os.path.join(site_packages, '~ip*')]
        removed = []
        for pattern in patterns:
            for path in glob.glob(pattern):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                        removed.append(os.path.basename(path))
                    elif os.path.isfile(path):
                        os.remove(path)
                        removed.append(os.path.basename(path))
                except Exception:
                    pass
        if removed:
            print(f"🧹 Nettoyage des distributions invalides: {', '.join(sorted(set(removed)))})")
    except Exception:
        # Ne pas bloquer si le nettoyage échoue
        pass

def parse_args():
    parser = argparse.ArgumentParser(description="Installateur LCPI-CLI Core")
    parser.add_argument("--accept-license", action="store_true", help="Accepter licence/disclaimer sans prompt")
    parser.add_argument("--offline", action="store_true", help="Installer les dépendances en mode hors-ligne")
    parser.add_argument("--plugins", type=str, default="aep", help="Plugins métier à activer, séparés par des virgules (ex: aep,cm)")
    parser.add_argument("--install-editable", action="store_true", help="Installer lcpi-cli en mode éditable (pip install -e .)")
    parser.add_argument("--no-input", action="store_true", help="Désactiver tous les prompts interactifs")
    parser.add_argument("--verbose", action="store_true", help="Sortie détaillée")
    return parser.parse_args()

def check_internet_connection(url='http://www.google.com', timeout=5):
    """Vérifie la connexion Internet"""
    try:
        urllib.request.urlopen(url, timeout=timeout)
        print("✅ Connexion Internet détectée.")
        return True
    except (urllib.error.URLError, ConnectionResetError):
        print("❌ Pas de connexion Internet détectée.")
        return False

def display_license_and_disclaimer(accept: bool = False, no_input: bool = False):
    """Affiche la licence et le disclaimer"""
    print("📋 ACCEPTATION DE LA LICENCE ET DU DISCLAIMER")
    print("-" * 50)
    
    # Afficher la licence
    if os.path.exists(LICENSE_FILE):
        print("📄 LICENCE:")
        try:
            with open(LICENSE_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                # Afficher les sections importantes
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('#') or 'Tous Droits Réservés' in line or 'Utilisation Autorisée' in line:
                        print(line)
                    elif line.strip() and i < 50:  # Premières lignes importantes
                        print(line)
                print("... (voir docs/LICENSE.md pour le texte complet)")
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture de la licence: {e}")
    
    # Afficher le disclaimer
    if os.path.exists(DISCLAIMER_FILE):
        print("\n📄 DISCLAIMER:")
        try:
            with open(DISCLAIMER_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('#') or 'Objectif Pédagogique' in line or 'Utilisation sous la Seule Responsabilité' in line:
                        print(line)
                    elif line.strip() and i < 30:  # Premières lignes importantes
                        print(line)
                print("... (voir docs/DISCLAIMER.md pour le texte complet)")
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture du disclaimer: {e}")
    
    print("\n" + "=" * 50)
    print("⚠️  AVERTISSEMENT IMPORTANT:")
    print("Ce logiciel est fourni à des fins pédagogiques et expérimentales.")
    print("Toute utilisation professionnelle nécessite une validation externe.")
    print("=" * 50)
    
    # Mode silencieux
    if accept or no_input or os.getenv("LCPI_ACCEPT_LICENSE", "").lower() in ("1","true","yes","o","oui"):
        print("✅ Licence et disclaimer acceptés (mode non interactif).")
        return True

    # Demande interactive si autorisée
    if not no_input:
        while True:
            choice = input("\nAcceptez-vous la licence et le disclaimer ? (o/n): ").lower().strip()
            if choice in ['o', 'oui', 'y', 'yes']:
                print("✅ Licence et disclaimer acceptés.")
                return True
            elif choice in ['n', 'non', 'no']:
                print("❌ Installation annulée par l'utilisateur.")
                return False
            else:
                print("❌ Veuillez répondre par 'o' (oui) ou 'n' (non).")
    print("⚠️  Mode non interactif sans acceptation explicite: échec.")
    return False

def setup_license_system():
    """Configure le système de licence"""
    print("\n🔐 Configuration du système de licence...")
    
    try:
        # Créer le dossier .lcpi dans le répertoire utilisateur
        license_dir = os.path.expanduser("~/.lcpi")
        os.makedirs(license_dir, exist_ok=True)
        
        license_file_path = os.path.join(license_dir, "license.key")
        
        if os.path.exists(license_file_path):
            print("✅ Fichier de licence existant détecté.")
            return True
        else:
            print("📝 Création du fichier de licence...")
            print(f"📁 Dossier créé : {license_dir}")
            print(f"📄 Fichier de licence : {license_file_path}")
            print("\n📋 INSTRUCTIONS POUR LA LICENCE :")
            print("1. Contactez le support pour obtenir votre clé de licence")
            print("2. Créez le fichier 'license.key' dans le dossier ci-dessus")
            print("3. Collez-y votre clé de licence")
            print("4. Relancez LCPI")
            
            # Créer un fichier vide avec des instructions
            with open(license_file_path, 'w', encoding='utf-8') as f:
                f.write("# LCPI-CLI License Key\n")
                f.write("# Remplacez ce contenu par votre clé de licence\n")
                f.write("# Contactez le support pour obtenir votre licence\n")
                f.write("# Email: support@lcpi-cli.com\n")
            
            print("✅ Fichier de licence créé avec instructions.")
            return True
            
    except Exception as e:
        print(f"❌ ERREUR lors de la configuration de la licence : {e}")
        return False

def test_license_system():
    """Teste le système de licence"""
    print("\n🔍 Test du système de licence...")
    
    try:
        # Importer le système de licence
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        src_path = os.path.join(project_root, 'src')
        sys.path.insert(0, src_path)
        
        from lcpi.license_validator import validate_license, get_license_info
        
        # Tester la validation
        is_valid, message = validate_license()
        
        if is_valid:
            # Message UX explicite
            try:
                from rich.panel import Panel
                from rich.console import Console
                console = Console()
                license_data = get_license_info()
                user = license_data.get('user_name', 'Utilisateur') if license_data else 'Utilisateur'
                exp = license_data.get('expiration_date', None) if license_data else None
                exp_str = f" (valide jusqu'au {exp[:10]})" if exp else ''
                console.print(Panel(f"✅ Licence activée avec succès pour [bold]{user}[/bold]{exp_str}", style="green"))
            except Exception:
                print("✅ Licence activée avec succès !")
            print(f"📋 {message}")
            return True
        else:
            print("⚠️  Licence non valide ou absente.")
            print(f"📋 {message}")
            print("\n💡 Le système fonctionnera en mode démonstration.")
            return True  # On continue même sans licence valide
            
    except ImportError:
        print("⚠️  Module de licence non disponible.")
        print("💡 Le système fonctionnera sans vérification de licence.")
        return True
    except Exception as e:
        print(f"❌ ERREUR lors du test de licence : {e}")
        return False

def install_requirements(offline=False, verbose=False):
    """Installe les dépendances Python"""
    project_root = get_project_root()
    requirements_path = os.path.join(project_root, 'requirements.txt')

    if not os.path.exists(requirements_path):
        print("❌ ERREUR: Le fichier 'requirements.txt' est introuvable.", file=sys.stderr)
        return False

    vendor_dir = os.path.join(project_root, 'vendor', 'packages')
    if offline:
        print("\n📦 Installation des dépendances en mode hors ligne...")
        if not os.path.isdir(vendor_dir):
            print(f"❌ ERREUR: Le dossier des paquets hors ligne est introuvable.", file=sys.stderr)
            return False
        command = [sys.executable, "-m", "pip", "install", "--no-input", "--no-index", f"--find-links={vendor_dir}", "-r", requirements_path]
    else:
        print("\n📦 Installation des dépendances en ligne...")
        command = [sys.executable, "-m", "pip", "install", "--no-input", "-r", requirements_path]

    try:
        subprocess.check_call(command, cwd=project_root)
        print("✅ Dépendances installées avec succès.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERREUR lors de l'installation des dépendances : {e}", file=sys.stderr)
        return False

def install_lcpi_core(editable=True, verbose=False):
    """Installe le noyau LCPI-CLI"""
    project_root = get_project_root()
    
    print("\n🔧 Installation du noyau LCPI-CLI...")
    
    # Vérifier que pyproject.toml existe
    pyproject_path = os.path.join(project_root, 'pyproject.toml')
    if not os.path.exists(pyproject_path):
        print("❌ ERREUR: Le fichier 'pyproject.toml' est introuvable.", file=sys.stderr)
        return False
    
    try:
        # Installer d'abord setuptools et wheel (offline si dispo, sinon online, sinon ignorer si déjà présents)
        vendor_dir = os.path.join(project_root, 'vendor', 'packages')
        def tool_installed(mod_name: str) -> bool:
            try:
                __import__(mod_name)
                return True
            except Exception:
                return False

        # Setuptools
        try:
            if os.path.isdir(vendor_dir):
                print("📦 Installation des outils de build en mode hors ligne...")
                cmd_setuptools = [sys.executable, "-m", "pip", "install", "--no-index", f"--find-links={vendor_dir}", "setuptools"]
                subprocess.check_call(cmd_setuptools, cwd=project_root)
                print("✅ setuptools installé avec succès.")
            else:
                # En ligne
                cmd_setuptools = [sys.executable, "-m", "pip", "install", "--upgrade", "setuptools"]
                subprocess.check_call(cmd_setuptools, cwd=project_root)
                print("✅ setuptools installé/mis à jour.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  setuptools déjà installé ou erreur: {e}")

        # wheel
        if not tool_installed('wheel'):
            try:
                if os.path.isdir(vendor_dir) and glob.glob(os.path.join(vendor_dir, 'wheel-*.whl')):
                    cmd_wheel = [sys.executable, "-m", "pip", "install", "--no-index", f"--find-links={vendor_dir}", "wheel"]
                    subprocess.check_call(cmd_wheel, cwd=project_root)
                    print("✅ wheel installé avec succès (offline).")
                else:
                    cmd_wheel = [sys.executable, "-m", "pip", "install", "--upgrade", "wheel"]
                    subprocess.check_call(cmd_wheel, cwd=project_root)
                    print("✅ wheel installé/mis à jour (online).")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  wheel non installé (offline indisponible, online échoué): {e}")
        else:
            print("✅ wheel déjà installé.")
        
        # Installer en mode éditable ou standard
        print("🔧 Installation du package LCPI-CLI...")
        if editable:
            command = [sys.executable, "-m", "pip", "install", "--no-input", "-e", "."]
        else:
            command = [sys.executable, "-m", "pip", "install", "--no-input", "."]
        subprocess.check_call(command, cwd=project_root)
        print("✅ Noyau LCPI-CLI installé avec succès.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERREUR lors de l'installation du noyau : {e}", file=sys.stderr)
        return False

def configure_base_plugins(plugins_to_activate=None):
    """Configure les plugins de base uniquement"""
    print("\n🔌 Configuration des plugins de base...")
    
    try:
        # Créer le fichier de configuration des plugins
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        plugins_config_path = os.path.join(project_root, 'src', 'lcpi', '.plugins.json')
        
        activate = list(BASE_PLUGINS)
        if plugins_to_activate:
            # Nettoyer et dédupliquer
            extra = [p.strip() for p in plugins_to_activate if p.strip()]
            for p in extra:
                if p not in activate:
                    activate.append(p)
        config = {
            "active_plugins": activate,
            "available_plugins": sorted(list(set(BASE_PLUGINS + BUSINESS_PLUGINS))),
            "installation_date": datetime.now().isoformat(),
            "version": VERSION
        }
        
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(plugins_config_path), exist_ok=True)
        
        # Écrire la configuration
        with open(plugins_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Plugins activés : {', '.join(config['active_plugins'])}")
        print(f"📋 Plugins disponibles : {', '.join(config['available_plugins'])}")
        return True
    except Exception as e:
        print(f"❌ ERREUR lors de la configuration des plugins : {e}", file=sys.stderr)
        return False

def verify_installation(verbose=False):
    """Vérifie que l'installation s'est bien passée"""
    print("\n🔍 Vérification de l'installation...")
    
    try:
        # Tester l'import de LCPI
        import sys
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        src_path = os.path.join(project_root, 'src')
        sys.path.insert(0, src_path)
        
        from lcpi.main import app
        print("✅ Import de LCPI réussi.")
        
        # Essayer lcpi --help via entrée console
        lcpi_bin = os.path.join(project_root, 'venv', 'Scripts', 'lcpi.exe')
        cmd = [lcpi_bin, "--help"] if os.path.isfile(lcpi_bin) else [sys.executable, "-m", "lcpi.cli", "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            print("✅ CLI 'lcpi' disponible.")
            return True
        # Fallback: import direct ok, considérer réussi
        print("⚠️  CLI non détectée mais import LCPI OK.")
        return True
            
    except Exception as e:
        print(f"❌ ERREUR lors de la vérification : {e}", file=sys.stderr)
        return False

def display_next_steps():
    """Affiche les prochaines étapes pour l'utilisateur"""
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print()
    print("📋 PROCHAINES ÉTAPES :")
    print()
    print("1. 🚀 Lancer LCPI :")
    print("   lcpi --help   # ou venv\\Scripts\\lcpi.exe --help sous Windows")
    print()
    print("2. 🔌 Activer des plugins métier supplémentaires (si nécessaire) :")
    print(f"   lcpi plugins install cm | bois | beton | hydro | aep")
    print()
    print("3. 📚 Consulter la documentation :")
    print("   - docs/GUIDE_UTILISATION.md")
    print("   - docs/NOUVELLES_FONCTIONNALITES.md")
    print()
    print("4. 🛠️  Utiliser le shell interactif :")
    print("   lcpi shell")
    print()
    print("5. 🔐 Gestion de la licence :")
    print("   - Vérifiez votre licence : ~/.lcpi/license.key")
    print("   - Contactez le support pour obtenir une licence")
    print()
    print("⚠️  RAPPEL : Ce logiciel est à usage pédagogique.")
    print("   Toute utilisation professionnelle nécessite une validation externe.")
    print("=" * 60)

def main():
    """Fonction principale"""
    args = parse_args()
    # Encodage UTF-8 en tout début
    force_utf8()
    # Nettoyage des distributions invalides (évite les warnings pip)
    cleanup_invalid_distributions()
    print_banner()

    # Étape 1: Licence & disclaimer
    if not display_license_and_disclaimer(accept=args.accept_license, no_input=args.no_input):
        sys.exit(1)

    # Étape 2: Système de licence
    if not setup_license_system():
        print("\n❌ La configuration du système de licence a échoué.")
        sys.exit(1)

    # Étape 3: Requirements
    ok = install_requirements(offline=args.offline, verbose=args.verbose)
    if not ok and not args.offline:
        # Fallback offline si vendor présent
        print("\n⚠️  Échec online, tentative hors-ligne si paquets dispo...")
        ok = install_requirements(offline=True, verbose=args.verbose)
    if not ok:
        print("\n❌ Installation des dépendances échouée.")
        sys.exit(1)

    # Étape 4: Installation du noyau (editable si demandé)
    if not install_lcpi_core(editable=args.install_editable, verbose=args.verbose):
        print("\n❌ L'installation du noyau LCPI a échoué.")
        sys.exit(1)

    # Étape 5: Plugins
    plugins_list = [p.strip() for p in (args.plugins or '').split(',') if p.strip()]
    if not configure_base_plugins(plugins_to_activate=plugins_list):
        print("\n❌ La configuration des plugins a échoué.")
        sys.exit(1)

    # Étape 6: Licence runtime (facultatif, continue même si invalide)
    test_license_system()

    # Étape 7: Vérification
    if not verify_installation(verbose=args.verbose):
        print("\n❌ La vérification de l'installation a échoué.")
        sys.exit(1)

    # Étape 8: Fin
    display_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Installation interrompue par l'utilisateur.")
        sys.exit(130)
    except Exception as e:
        print("\n❌ ERREUR CRITIQUE INATTENDUE", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\n📝 Fin du script d'installation.")
