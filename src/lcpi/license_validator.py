"""
Validateur de Licences pour LCPI-CLI
Module de vérification et validation des clés de licence
"""

import uuid
import json
import base64
import os
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- CONFIGURATION SECRÈTE (DOIT ÊTRE IDENTIQUE À CELLE DU GÉNÉRATEUR) ---
MASTER_PASSWORD = b"MaPhraseSecretePourLCPI-CLI-2025!"
SALT = b'\x9a\x8b\x01\xe0\x9c\x8a\x1e\x9f\x1d\x0c\x0b\x9d\x8e\x1f\x9a\x8b'
LICENSE_FILE_PATH = os.path.expanduser("~/.lcpi/license.key")

def get_encryption_key():
    """Dérive la même clé de chiffrement que le générateur."""
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

def validate_license():
    """
    Vérifie la validité de la licence.
    Retourne (True, "Message de succès") ou (False, "Message d'erreur").
    """
    # 1. Le fichier de licence existe-t-il ?
    if not os.path.exists(LICENSE_FILE_PATH):
        return (False, f"Fichier de licence introuvable.\n\nVeuillez créer le fichier : {LICENSE_FILE_PATH}\n\nInstructions :\n1. Créez le dossier : {os.path.dirname(LICENSE_FILE_PATH)}\n2. Créez le fichier 'license.key' dans ce dossier\n3. Collez-y votre clé de licence")

    # 2. Lire et déchiffrer la clé
    try:
        with open(LICENSE_FILE_PATH, 'rb') as f:
            encrypted_license = f.read().strip()
        
        if not encrypted_license:
            return (False, "Le fichier de licence est vide. Veuillez y coller votre clé de licence.")
        
        fernet = Fernet(get_encryption_key())
        # Tenter de déchiffrer (échoue si la clé est invalide ou a été modifiée)
        decrypted_license_json = fernet.decrypt(encrypted_license)
        license_data = json.loads(decrypted_license_json)

    except (InvalidToken, ValueError) as e:
        return (False, f"La clé de licence est invalide ou corrompue.\n\nErreur : {str(e)}\n\nVeuillez vérifier que vous avez copié la clé complète sans espaces supplémentaires.")
    except Exception as e:
        return (False, f"Une erreur est survenue lors de la lecture de la licence : {e}")

    # 3. Vérifier l'empreinte machine
    current_fingerprint = get_machine_fingerprint()
    license_fingerprint = license_data.get("fingerprint")
    if current_fingerprint != license_fingerprint:
        return (False, f"La licence n'est pas valide pour cette machine.\n\nEmpreinte actuelle : {current_fingerprint}\nEmpreinte de la licence : {license_fingerprint}\n\nCette licence a été générée pour une autre machine.")

    # 4. Vérifier la date d'expiration
    expiration_date = datetime.fromisoformat(license_data.get("expiration_date"))
    if datetime.now() > expiration_date:
        return (False, f"La licence a expiré le {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}.\n\nVeuillez contacter le support pour renouveler votre licence.")

    # 5. Vérifier le type de licence
    license_type = license_data.get("license_type", "standard")
    
    # Si toutes les vérifications passent
    user_name = license_data.get("user_name", "Utilisateur")
    days_remaining = (expiration_date - datetime.now()).days
    
    success_message = f"✅ Licence valide pour {user_name}\n"
    success_message += f"📅 Valide jusqu'au : {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
    success_message += f"⏱️  Jours restants : {days_remaining}\n"
    success_message += f"🏷️  Type : {license_type}"
    
    return (True, success_message)

def get_license_info():
    """
    Récupère les informations de la licence sans validation stricte.
    Utile pour afficher les détails de la licence.
    """
    if not os.path.exists(LICENSE_FILE_PATH):
        return None
    
    try:
        with open(LICENSE_FILE_PATH, 'rb') as f:
            encrypted_license = f.read().strip()
        
        if not encrypted_license:
            return None
        
        fernet = Fernet(get_encryption_key())
        decrypted_license_json = fernet.decrypt(encrypted_license)
        license_data = json.loads(decrypted_license_json)
        
        return license_data
    except:
        return None

def is_license_expired():
    """Vérifie si la licence est expirée."""
    license_data = get_license_info()
    if not license_data:
        return True
    
    expiration_date = datetime.fromisoformat(license_data.get("expiration_date"))
    return datetime.now() > expiration_date

def get_days_remaining():
    """Retourne le nombre de jours restants de la licence."""
    license_data = get_license_info()
    if not license_data:
        return 0
    
    expiration_date = datetime.fromisoformat(license_data.get("expiration_date"))
    days_remaining = (expiration_date - datetime.now()).days
    return max(0, days_remaining)

def get_license_type():
    """Retourne le type de licence."""
    license_data = get_license_info()
    if not license_data:
        return "none"
    
    return license_data.get("license_type", "standard")

def check_license_and_exit():
    """
    Vérifie la licence et arrête le programme si elle est invalide.
    Cette fonction est appelée au démarrage de l'application.
    """
    is_valid, message = validate_license()
    if not is_valid:
        print("\n" + "="*70)
        print("🚫 ERREUR DE LICENCE - LCPI-CLI")
        print("="*70)
        print(f"\n❌ {message}")
        print("\n" + "="*70)
        print("📞 Veuillez contacter le support pour obtenir une clé de licence valide.")
        print("🌐 Email : support@lcpi-cli.com")
        print("📱 Téléphone : +33 1 23 45 67 89")
        print("="*70)
        
        # Arrêter le programme avec un code d'erreur
        import sys
        sys.exit(1)
    else:
        # Optionnel: Afficher un message de succès silencieux
        # print(f"✅ {message}")
        pass 