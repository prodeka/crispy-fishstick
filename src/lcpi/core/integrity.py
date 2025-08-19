from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

KEY_DIR = Path.home() / ".lcpi"
PRIVATE_KEY_PATH = KEY_DIR / "signing_key.pem"
PUBLIC_KEY_PATH = KEY_DIR / "signing_key.pub"

def generate_keys(force: bool = False):
    """Génère une paire de clés ECDSA pour la signature."""
    KEY_DIR.mkdir(exist_ok=True)
    if PRIVATE_KEY_PATH.exists() and not force:
        print("Les clés de signature existent déjà.")
        return

    private_key = ec.generate_private_key(ec.SECP384R1())
    
    # Sauvegarder la clé privée
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    PRIVATE_KEY_PATH.write_bytes(pem)
    PRIVATE_KEY_PATH.chmod(0o600) # Accès restreint

    # Sauvegarder la clé publique
    public_key = private_key.public_key()
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    PUBLIC_KEY_PATH.write_bytes(pub_pem)
    print(f"Paire de clés générée dans {KEY_DIR}")

def _get_private_key() -> ec.EllipticCurvePrivateKey:
    if not PRIVATE_KEY_PATH.exists():
        raise FileNotFoundError("La clé privée n'existe pas. Exécutez `lcpi-admin generate-keys`.")
    return serialization.load_pem_private_key(
        PRIVATE_KEY_PATH.read_bytes(),
        password=None
    )

def _get_public_key() -> ec.EllipticCurvePublicKey:
    if not PUBLIC_KEY_PATH.exists():
        raise FileNotFoundError("La clé publique n'existe pas.")
    return serialization.load_pem_public_key(PUBLIC_KEY_PATH.read_bytes())

def _canonical_json(data: Dict[str, Any]) -> bytes:
    """Crée une représentation JSON canonique et stable pour le hachage."""
    # Exclure le bloc d'intégrité lui-même pour le calcul du hash
    data_copy = data.copy()
    data_copy.pop("integrity", None)
    return json.dumps(data_copy, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode('utf-8')

def sign_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ajoute un bloc d'intégrité avec un checksum et une signature."""
    private_key = _get_private_key()
    canonical_data = _canonical_json(data)
    
    # Calculer le checksum
    digest = hashes.Hash(hashes.SHA256())
    digest.update(canonical_data)
    checksum = digest.finalize().hex()

    # Signer le checksum
    signature = private_key.sign(
        checksum.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    ).hex()

    data["integrity"] = {
        "checksum_sha256": checksum,
        "signature_ecdsa": signature,
        "signer": "lcpi_default_key"
    }
    return data

def verify_signature(data: Dict[str, Any]) -> Dict[str, Any]:
    """Vérifie le checksum et la signature dans le bloc d'intégrité."""
    integrity_block = data.get("integrity")
    if not isinstance(integrity_block, dict):
        return {"valid": False, "reason": "Bloc d'intégrité manquant ou malformé."}

    # 1. Vérifier le checksum
    canonical_data = _canonical_json(data)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(canonical_data)
    expected_checksum = digest.finalize().hex()

    actual_checksum = integrity_block.get("checksum_sha256")
    if expected_checksum != actual_checksum:
        return {"valid": False, "reason": "Le checksum ne correspond pas. Le contenu a été altéré."}

    # 2. Vérifier la signature
    try:
        public_key = _get_public_key()
        signature = bytes.fromhex(integrity_block.get("signature_ecdsa", ""))
        public_key.verify(
            signature,
            expected_checksum.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
    except InvalidSignature:
        return {"valid": False, "reason": "La signature est invalide."}
    except (ValueError, FileNotFoundError) as e:
        return {"valid": False, "reason": f"Erreur lors de la vérification de la signature: {e}"}

    return {"valid": True, "reason": "Le contenu est intègre et la signature est valide."}
