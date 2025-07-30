import os
import uuid
import platform
import json
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path

# Generate a key for Fernet encryption. In a real application, this key
# should be securely stored and not hardcoded. For this pedagogical example,
# we'll generate one if it doesn't exist, but it should be consistent.
# You should generate this once and keep it secret!
# Example: Fernet.generate_key().decode()
ENCRYPTION_KEY = os.environ.get("LCPI_LICENSE_ENCRYPTION_KEY", "YOUR_VERY_SECRET_KEY_HERE").encode()
if ENCRYPTION_KEY == b"YOUR_VERY_SECRET_KEY_HERE":
    print("WARNING: Using a default, insecure encryption key. Generate a strong key and set it as LCPI_LICENSE_ENCRYPTION_KEY environment variable.")
    # For a real application, generate a key once and store it securely.
    # For example, in a .env file or a secrets management system.
    # ENCRYPTION_KEY = Fernet.generate_key()

_fernet = Fernet(ENCRYPTION_KEY)

def _get_machine_fingerprint() -> str:
    """Generates a simple, non-cryptographic machine fingerprint."""
    # Using MAC address (uuid.getnode()) and hostname (platform.node())
    # Note: MAC address can change or be spoofed. Hostname can be changed.
    # For stronger binding, more complex methods involving CPU ID, disk serials,
    # or external services would be needed.
    mac_address = ':'.join(('%012x' % uuid.getnode())[i:i+2] for i in range(0, 12, 2))
    hostname = platform.node()
    return f"{mac_address}-{hostname}"

def generate_license_key(output_path: Path, days_valid: int = 365) -> None:
    """
    Generates an encrypted license key for the current machine and saves it.
    This function is for the developer/distributor to create licenses.
    """
    fingerprint = _get_machine_fingerprint()
    expiration_timestamp = int(time.time()) + (days_valid * 24 * 3600) # seconds from now

    license_data = {
        "fingerprint": fingerprint,
        "expiration": expiration_timestamp,
        "issued_at": int(time.time()),
        "type": "proprietary",
        "version": "1.0"
    }
    
    json_data = json.dumps(license_data).encode('utf-8')
    encrypted_data = _fernet.encrypt(json_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(encrypted_data)
    print(f"License key generated and saved to {output_path}")
    print(f"Fingerprint: {fingerprint}")
    print(f"Expires: {time.ctime(expiration_timestamp)}")

def validate_license_key(license_path: Path) -> bool:
    """
    Validates the license key found at license_path.
    Returns True if valid, False otherwise.
    """
    if not license_path.exists():
        print("License file not found.")
        return False

    try:
        with open(license_path, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = _fernet.decrypt(encrypted_data).decode('utf-8')
        license_data = json.loads(decrypted_data)

        current_fingerprint = _get_machine_fingerprint()
        if license_data.get("fingerprint") != current_fingerprint:
            print("License invalid: Fingerprint mismatch.")
            return False
        
        if license_data.get("expiration", 0) < time.time():
            print("License invalid: Expired.")
            return False
        
        print("License valid.")
        return True

    except InvalidToken:
        print("License invalid: Could not decrypt (corrupted or wrong key).")
        return False
    except json.JSONDecodeError:
        print("License invalid: Corrupted data.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during license validation: {e}")
        return False

# Example usage (for developer to generate a key)
if __name__ == "__main__":
    import time
    # This part is for you (the developer) to generate a license for a user.
    # You would run this on the target machine or provide the user with a tool
    # to generate their fingerprint, which you then use to create a license.
    
    # For demonstration, let's generate a key that expires in 30 days
    # and save it in a common location for the app to find.
    
    # In a real scenario, you'd distribute this 'generate_license_key'
    # function or a separate tool to your users, or have them send you their fingerprint.
    
    # Example: Generate a key for the current machine, valid for 30 days
    # license_file_for_user = Path.home() / ".lcpi_license"
    # generate_license_key(license_file_for_user, days_valid=30)
    
    # To test validation:
    # print(f"Validating license at {license_file_for_user}: {validate_license_key(license_file_for_user)}")
    pass
