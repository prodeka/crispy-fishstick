#!/usr/bin/env python3
"""
Générateur de Licences pour LCPI-CLI
Outil de génération de clés de licence chiffrées et sécurisées
"""

import uuid
import json
import base64
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- CONFIGURATION SECRÈTE DU DÉVELOPPEUR ---
# ATTENTION : Gardez cette "master_password" secrète.
# Elle est utilisée pour dériver la clé de chiffrement. Changez-la pour votre propre projet.
MASTER_PASSWORD = b"MaPhraseSecretePourLCPI-CLI-2025!"
SALT = b'\x9a\x8b\x01\xe0\x9c\x8a\x1e\x9f\x1d\x0c\x0b\x9d\x8e\x1f\x9a\x8b'  # Sel statique

def get_encryption_key():
    """Dérive une clé de chiffrement stable à partir du mot de passe maître."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD))
    return key

def get_machine_fingerprint():
    """
    Génère un identifiant unique pour la machine basé sur l'adresse MAC.
    Retourne une chaîne de caractères.
    """
    # uuid.getnode() retourne l'adresse MAC sous forme d'un entier de 48 bits.
    # C'est une méthode simple et assez fiable pour lier la licence à une machine.
    mac_address = uuid.getnode()
    return hex(mac_address)

def generate_license_key(user_name: str, days_valid: int, license_type: str = "standard"):
    """
    Génère une clé de licence chiffrée pour un utilisateur et une durée données.
    
    Args:
        user_name: Nom de l'utilisateur
        days_valid: Nombre de jours de validité
        license_type: Type de licence (standard, premium, enterprise)
    """
    fingerprint = get_machine_fingerprint()
    expiration_date = datetime.now() + timedelta(days=days_valid)

    license_data = {
        "user_name": user_name,
        "fingerprint": fingerprint,
        "expiration_date": expiration_date.isoformat(),
        "generated_at": datetime.now().isoformat(),
        "license_type": license_type,
        "version": "1.0"
    }

    # Sérialiser les données en JSON
    license_json = json.dumps(license_data, indent=2).encode('utf-8')

    # Chiffrer les données
    fernet = Fernet(get_encryption_key())
    encrypted_license = fernet.encrypt(license_json)

    print("\n" + "="*60)
    print("  🎫 GÉNÉRATION DE LA CLÉ DE LICENCE RÉUSSIE")
    print("="*60)
    print(f"👤 Utilisateur : {user_name}")
    print(f"🔧 Empreinte machine : {fingerprint}")
    print(f"📅 Valide jusqu'au : {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏷️  Type de licence : {license_type}")
    print(f"⏱️  Durée : {days_valid} jours")
    
    print("\n" + "="*60)
    print("🔑 CLÉ DE LICENCE À FOURNIR À L'UTILISATEUR")
    print("="*60)
    print(encrypted_license.decode('utf-8'))
    print("="*60)
    
    # Sauvegarder dans un fichier pour le développeur
    license_file = f"license_{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(license_file, 'w') as f:
        f.write(f"Licence générée pour : {user_name}\n")
        f.write(f"Type : {license_type}\n")
        f.write(f"Valide jusqu'au : {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Empreinte machine : {fingerprint}\n")
        f.write("\n" + "="*60 + "\n")
        f.write("CLÉ DE LICENCE :\n")
        f.write("="*60 + "\n")
        f.write(encrypted_license.decode('utf-8'))
        f.write("\n" + "="*60 + "\n")
    
    print(f"\n💾 Licence sauvegardée dans : {license_file}")
    
    return encrypted_license.decode('utf-8')

def show_activation_instructions():
    """Affiche les instructions d'activation pour l'utilisateur."""
    print("\n" + "="*60)
    print("📋 INSTRUCTIONS D'ACTIVATION POUR L'UTILISATEUR")
    print("="*60)
    print("1. Créez un dossier caché nommé '.lcpi' dans votre répertoire personnel :")
    print("   • Windows : C:\\Users\\VotreNom\\.lcpi")
    print("   • Linux/macOS : /home/votrenom/.lcpi")
    print()
    print("2. Dans ce dossier, créez un fichier nommé 'license.key'")
    print()
    print("3. Copiez-collez la clé de licence ci-dessus dans ce fichier")
    print("   (seulement la clé, sans espaces supplémentaires)")
    print()
    print("4. Sauvegardez le fichier")
    print()
    print("5. Relancez LCPI-CLI - la licence sera automatiquement validée")
    print("="*60)

def main():
    """Point d'entrée principal pour le développeur."""
    print("🔐 Outil de Génération de Licence pour LCPI-CLI")
    print("="*60)
    
    # Demander au développeur l'empreinte de la machine de l'utilisateur
    print("\n⚠️  IMPORTANT : Exécutez ce script sur la machine de l'utilisateur final")
    print("pour capturer automatiquement la bonne empreinte matérielle.")
    
    confirm = input("\nAvez-vous bien exécuté ce script sur la machine de l'utilisateur final ? (o/n) : ")
    if confirm.lower() != 'o':
        print("❌ Opération annulée. Veuillez relancer sur la machine cible.")
        return
    
    print("\n" + "="*60)
    print("📝 INFORMATIONS DE LA LICENCE")
    print("="*60)
    
    user_name = input("👤 Nom de l'utilisateur : ")
    days_valid = int(input("⏱️  Nombre de jours de validité (ex: 365) : "))
    
    print("\n🏷️  Type de licence :")
    print("1. Standard (fonctionnalités de base)")
    print("2. Premium (fonctionnalités avancées)")
    print("3. Enterprise (toutes les fonctionnalités)")
    
    license_type_choice = input("Choisissez le type (1/2/3) [1] : ").strip()
    
    license_types = {
        "1": "standard",
        "2": "premium", 
        "3": "enterprise"
    }
    
    license_type = license_types.get(license_type_choice, "standard")
    
    # Générer la licence
    license_key = generate_license_key(user_name, days_valid, license_type)
    
    # Afficher les instructions d'activation
    show_activation_instructions()
    
    print(f"\n✅ Licence générée avec succès pour {user_name} !")

if __name__ == "__main__":
    main() 