#!/usr/bin/env python3
"""
Générateur de Licences Amélioré pour LCPI-CLI
Utilise le même système de chiffrement que le validateur
"""

import argparse
import json
import os
import uuid
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- CONFIGURATION SECRÈTE (DOIT ÊTRE IDENTIQUE À CELLE DU VALIDATEUR) ---
MASTER_PASSWORD = b"MaPhraseSecretePourLCPI-CLI-2025!"
SALT = b'\x9a\x8b\x01\xe0\x9c\x8a\x1e\x9f\x1d\x0c\x0b\x9d\x8e\x1f\x9a\x8b'

def get_encryption_key():
    """Dérive la même clé de chiffrement que le validateur."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD))
    return key

def get_machine_fingerprint():
    """Récupère l'empreinte de la machine actuelle."""
    mac_address = uuid.getnode()
    return hex(mac_address)

def generate_license(user_name, license_type, days_valid, machine_fingerprint=None):
    """
    Génère une licence pour LCPI-CLI.
    
    Args:
        user_name (str): Nom de l'utilisateur
        license_type (str): Type de licence (standard, premium, enterprise)
        days_valid (int): Nombre de jours de validité
        machine_fingerprint (str): Empreinte de la machine (optionnel)
    
    Returns:
        bytes: Licence chiffrée
    """
    # Utiliser l'empreinte fournie ou celle de la machine actuelle
    if machine_fingerprint is None:
        machine_fingerprint = get_machine_fingerprint()
    
    # Calculer la date d'expiration
    expiration_date = datetime.now() + timedelta(days=days_valid)
    
    # Créer les données de licence
    license_data = {
        "user_name": user_name,
        "license_type": license_type,
        "fingerprint": machine_fingerprint,
        "expiration_date": expiration_date.isoformat(),
        "created_date": datetime.now().isoformat(),
        "days_valid": days_valid,
        "version": "2.0.0"
    }
    
    # Chiffrer la licence
    fernet = Fernet(get_encryption_key())
    encrypted_license = fernet.encrypt(json.dumps(license_data).encode('utf-8'))
    
    return encrypted_license

def main():
    parser = argparse.ArgumentParser(description="Générateur de licences pour LCPI-CLI")
    parser.add_argument("user_name", help="Nom de l'utilisateur")
    parser.add_argument("license_type", choices=["standard", "premium", "enterprise"], 
                       help="Type de licence")
    parser.add_argument("days_valid", type=int, help="Durée de validité en jours")
    parser.add_argument("--machine-fingerprint", help="Empreinte de la machine (optionnel)")
    parser.add_argument("--output", help="Fichier de sortie (optionnel)")
    
    args = parser.parse_args()
    
    print("🔐 Générateur de Licences LCPI-CLI")
    print("=" * 40)
    
    # Générer la licence
    try:
        encrypted_license = generate_license(
            user_name=args.user_name,
            license_type=args.license_type,
            days_valid=args.days_valid,
            machine_fingerprint=args.machine_fingerprint
        )
        
        # Déterminer le fichier de sortie
        if args.output:
            output_file = args.output
        else:
            output_dir = "licenses"
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"license_{args.user_name}_{args.license_type}.key")
        
        # Sauvegarder la licence
        with open(output_file, 'wb') as f:
            f.write(encrypted_license)
        
        print(f"✅ Licence générée avec succès : {output_file}")
        print(f"👤 Utilisateur : {args.user_name}")
        print(f"🏷️  Type : {args.license_type}")
        print(f"⏱️  Validité : {args.days_valid} jours")
        
        if args.machine_fingerprint:
            print(f"🖥️  Machine : {args.machine_fingerprint}")
        else:
            print(f"🖥️  Machine : {get_machine_fingerprint()}")
        
        print("\n📋 INSTRUCTIONS POUR L'UTILISATEUR :")
        print("1. Copiez le contenu du fichier de licence")
        print("2. Créez le dossier : ~/.lcpi/")
        print("3. Créez le fichier : ~/.lcpi/license.key")
        print("4. Collez-y le contenu de la licence")
        print("5. Relancez LCPI-CLI")
        
    except Exception as e:
        print(f"❌ ERREUR lors de la génération : {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 