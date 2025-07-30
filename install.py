#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path

DOCS = [
    ("Politique de Confidentialité", "PRIVACY.md"),
    ("Clause de Non-Responsabilité", "DISCLAIMER.md"),
    ("Licence Propriétaire", "LICENSE.md"),
]

def show_doc(title, filename):
    print("\n" + "="*80)
    print(f"*** {title} ***")
    print("="*80)
    if not os.path.exists(filename):
        print(f"[ERREUR] Fichier manquant : {filename}")
        sys.exit(1)
    with open(filename, encoding="utf-8") as f:
        content = f.read()
    # Affichage paginé si long
    if len(content.splitlines()) > 30:
        pager = os.environ.get("PAGER", "less" if platform.system() != "Windows" else "more")
        try:
            proc = subprocess.Popen(pager, stdin=subprocess.PIPE, shell=True)
            proc.communicate(input=content.encode("utf-8"))
        except Exception:
            print(content)
    else:
        print(content)
    print("="*80)
    while True:
        resp = input(f"Acceptez-vous ce document ? (oui/non): ").strip().lower()
        if resp in ("oui", "o", "yes", "y"):
            return True
        elif resp in ("non", "n"):
            print("Installation annulée.")
            sys.exit(1)
        else:
            print("Veuillez répondre par 'oui' ou 'non'.")

def check_license():
    home = Path.home()
    license_file = home / ".lcpi" / "license.key"
    if not license_file.exists():
        print(f"\n[ERREUR] Aucune clé de licence trouvée dans {license_file}")
        print("Veuillez générer ou coller votre clé de licence avant de poursuivre.")
        sys.exit(1)
    # Validation réelle de la licence
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from lcpi.license_validator import validate_license
        is_valid, message = validate_license()
        if not is_valid:
            print(f"\n[ERREUR] Licence invalide :\n{message}")
            sys.exit(1)
        else:
            print(f"\n[OK] Licence valide :\n{message}")
    except Exception as e:
        print(f"\n[ERREUR] Impossible de valider la licence : {e}")
        sys.exit(1)

def main():
    print("=== Installation de LCPI-CLI ===")
    for title, filename in DOCS:
        show_doc(title, filename)
    check_license()
    print("\nInstallation des dépendances Python...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("[ERREUR] L'installation des dépendances a échoué.")
        sys.exit(1)
    print("\n✅ Installation terminée avec succès !")

if __name__ == "__main__":
    main()