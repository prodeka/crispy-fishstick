import unittest
import os
import json
from cryptography.fernet import Fernet
import hashlib

# Fonctions miroir de generate_license.py pour les tests
def generate_key(secret_phrase):
    return hashlib.sha256(secret_phrase.encode()).digest()

def encrypt_license(data, key):
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_license(encrypted_data, key):
    f = Fernet(key)
    return json.loads(f.decrypt(encrypted_data).decode())

class TestLicenseSystem(unittest.TestCase):

    def setUp(self):
        self.secret = "ma_phrase_secrete_de_test"
        self.key = generate_key(self.secret)
        self.license_dir = "test_licenses"
        os.makedirs(self.license_dir, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.license_dir):
            os.remove(os.path.join(self.license_dir, f))
        os.rmdir(self.license_dir)

    def test_license_creation_and_decryption(self):
        license_data = {
            "id_machine": "machine_test_123",
            "nom_client": "Client Test",
            "type_licence": "premium",
            "duree_jours": 365
        }

        encrypted_license = encrypt_license(license_data, self.key)
        
        file_path = os.path.join(self.license_dir, "test_license.lic")
        with open(file_path, "wb") as f:
            f.write(encrypted_license)

        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "rb") as f:
            read_encrypted_license = f.read()

        decrypted_data = decrypt_license(read_encrypted_license, self.key)

        self.assertEqual(license_data, decrypted_data)

if __name__ == '__main__':
    unittest.main()
