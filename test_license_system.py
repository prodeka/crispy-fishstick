#!/usr/bin/env python3
"""
Script de test pour le système de licence LCPI-CLI
Teste la génération, la validation et l'activation des licences
"""

import os
import sys
import pathlib
import tempfile
import shutil
from datetime import datetime, timedelta

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

def test_license_generation():
    """Test de la génération de licence."""
    print("🔐 Test de génération de licence")
    print("=" * 50)
    
    try:
        from generate_license import generate_license_key, get_machine_fingerprint
        
        # Obtenir l'empreinte de la machine
        fingerprint = get_machine_fingerprint()
        print(f"🔧 Empreinte machine : {fingerprint}")
        
        # Générer une licence de test
        license_key = generate_license_key("TestUser", 30, "standard")
        
        print("✅ Génération de licence réussie")
        return license_key
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return None

def test_license_validation(license_key):
    """Test de la validation de licence."""
    print("\n🔍 Test de validation de licence")
    print("=" * 50)
    
    if not license_key:
        print("❌ Pas de clé de licence à tester")
        return False
    
    try:
        from src.lcpi.license_validator import validate_license, get_license_info
        
        # Créer un dossier temporaire pour le test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le dossier .lcpi
            lcpi_dir = pathlib.Path(temp_dir) / ".lcpi"
            lcpi_dir.mkdir()
            
            # Créer le fichier de licence
            license_file = lcpi_dir / "license.key"
            with open(license_file, 'w') as f:
                f.write(license_key)
            
            print(f"📁 Fichier de licence créé : {license_file}")
            
            # Sauvegarder le chemin original
            original_path = os.path.expanduser("~/.lcpi/license.key")
            
            # Temporairement changer le chemin de licence pour le test
            import src.lcpi.license_validator as lv
            lv.LICENSE_FILE_PATH = str(license_file)
            
            # Tester la validation
            is_valid, message = validate_license()
            
            print(f"📋 Résultat de validation : {is_valid}")
            print(f"💬 Message : {message}")
            
            if is_valid:
                # Tester la récupération d'informations
                license_info = get_license_info()
                if license_info:
                    print(f"👤 Utilisateur : {license_info.get('user_name')}")
                    print(f"🏷️  Type : {license_info.get('license_type')}")
                    print(f"📅 Expiration : {license_info.get('expiration_date')}")
                
                print("✅ Validation de licence réussie")
                return True
            else:
                print("❌ Validation de licence échouée")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de la validation : {e}")
        return False

def test_license_activation():
    """Test de l'activation de licence."""
    print("\n🎯 Test d'activation de licence")
    print("=" * 50)
    
    try:
        # Créer le dossier .lcpi dans le répertoire utilisateur
        lcpi_dir = pathlib.Path.home() / ".lcpi"
        lcpi_dir.mkdir(exist_ok=True)
        
        license_file = lcpi_dir / "license.key"
        
        if license_file.exists():
            print(f"📁 Fichier de licence existant : {license_file}")
            
            # Lire le contenu
            with open(license_file, 'r') as f:
                content = f.read().strip()
            
            if content:
                print("✅ Fichier de licence non vide")
                
                # Tester la validation
                from src.lcpi.license_validator import validate_license
                is_valid, message = validate_license()
                
                print(f"📋 Validation : {is_valid}")
                if is_valid:
                    print("✅ Licence activée avec succès")
                    return True
                else:
                    print(f"❌ Licence invalide : {message}")
                    return False
            else:
                print("❌ Fichier de licence vide")
                return False
        else:
            print(f"📁 Aucun fichier de licence trouvé : {license_file}")
            print("💡 Pour activer une licence :")
            print("   1. Créez le fichier : ~/.lcpi/license.key")
            print("   2. Collez-y votre clé de licence")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'activation : {e}")
        return False

def test_license_expiration():
    """Test de l'expiration de licence."""
    print("\n⏰ Test d'expiration de licence")
    print("=" * 50)
    
    try:
        from src.lcpi.license_validator import is_license_expired, get_days_remaining, get_license_type
        
        is_expired = is_license_expired()
        days_remaining = get_days_remaining()
        license_type = get_license_type()
        
        print(f"📅 Licence expirée : {is_expired}")
        print(f"⏱️  Jours restants : {days_remaining}")
        print(f"🏷️  Type de licence : {license_type}")
        
        if is_expired:
            print("⚠️  Licence expirée - renouvellement nécessaire")
        else:
            print("✅ Licence encore valide")
            
        return not is_expired
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'expiration : {e}")
        return False

def show_license_instructions():
    """Affiche les instructions d'utilisation du système de licence."""
    print("\n📖 Instructions d'utilisation du système de licence")
    print("=" * 60)
    
    print("🔐 POUR LE DÉVELOPPEUR (Génération de licences) :")
    print("   1. Exécutez : python generate_license.py")
    print("   2. Suivez les instructions pour générer une licence")
    print("   3. Envoyez la clé à l'utilisateur")
    print()
    
    print("👤 POUR L'UTILISATEUR (Activation de licence) :")
    print("   1. Créez le dossier : ~/.lcpi/")
    print("   2. Créez le fichier : ~/.lcpi/license.key")
    print("   3. Collez-y votre clé de licence")
    print("   4. Relancez LCPI-CLI")
    print()
    
    print("🔍 VÉRIFICATION :")
    print("   - LCPI-CLI vérifie automatiquement la licence au démarrage")
    print("   - Si la licence est invalide, le programme s'arrête")
    print("   - Les erreurs de licence affichent des messages clairs")
    print()
    
    print("🛡️  SÉCURITÉ :")
    print("   - Licences liées à l'empreinte matérielle de la machine")
    print("   - Chiffrement robuste avec cryptography")
    print("   - Vérification de l'expiration automatique")
    print("   - Protection contre la modification des clés")

def main():
    """Fonction principale de test."""
    print("🧪 TESTS DU SYSTÈME DE LICENCE LCPI-CLI")
    print("=" * 60)
    
    # Test 1 : Génération de licence
    license_key = test_license_generation()
    
    # Test 2 : Validation de licence
    if license_key:
        test_license_validation(license_key)
    
    # Test 3 : Activation de licence
    test_license_activation()
    
    # Test 4 : Expiration de licence
    test_license_expiration()
    
    # Instructions
    show_license_instructions()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés")
    print("=" * 60)

if __name__ == "__main__":
    main() 