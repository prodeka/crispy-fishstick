import argparse
import json
import os
from cryptography.fernet import Fernet
import hashlib

def generate_key(secret_phrase):
    return hashlib.sha256(secret_phrase.encode()).digest()

def encrypt_license(data, key):
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def main():
    parser = argparse.ArgumentParser(description="Générateur de licences pour LCPI-CLI.")
    parser.add_argument("id_machine", help="Identifiant unique de la machine cliente.")
    parser.add_argument("nom_client", help="Nom du client.")
    parser.add_argument("type_licence", choices=["standard", "premium", "entreprise"], help="Type de licence.")
    parser.add_argument("duree_jours", type=int, help="Durée de validité de la licence en jours.")
    parser.add_argument("--secret", required=True, help="Phrase secrète pour le chiffrement.")
    args = parser.parse_args()

    key = generate_key(args.secret)
    
    license_data = {
        "id_machine": args.id_machine,
        "nom_client": args.nom_client,
        "type_licence": args.type_licence,
        "duree_jours": args.duree_jours
    }

    encrypted_license = encrypt_license(license_data, key)

    output_dir = "licenses"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"license_{args.nom_client}.lic")
    
    with open(file_path, "wb") as f:
        f.write(encrypted_license)

    print(f"Licence générée avec succès : {file_path}")

if __name__ == "__main__":
    main()
