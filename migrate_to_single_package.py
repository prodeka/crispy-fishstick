import os
import shutil

print("### DÉBUT DE LA MIGRATION VERS UN PAQUET UNIQUE ###")

# Définition des chemins
BASE_DIR = os.getcwd()
OLD_PLATFORM_PATH = os.path.join(BASE_DIR, "lcpi_platform")
NEW_SRC_PATH = os.path.join(BASE_DIR, "src")
NEW_PACKAGE_PATH = os.path.join(NEW_SRC_PATH, "lcpi")

# Dictionnaire de correspondance: ancien dossier -> nouveau sous-dossier dans src/lcpi/
MODULE_MAP = {
    "lcpi_core": "", # Les fichiers du noyau vont à la racine de src/lcpi/
    "lcpi_cm": "cm",
    "lcpi_bois": "bois",
    "lcpi_beton": "beton",
    "lcpi_hydrodrain": "hydrodrain"
}

# Création de la structure de base
print("\n1. Création de la nouvelle arborescence de dossiers...")
os.makedirs(NEW_PACKAGE_PATH, exist_ok=True)
with open(os.path.join(NEW_PACKAGE_PATH, "__init__.py"), "w") as f: pass

for new_subdir in MODULE_MAP.values():
    if new_subdir:
        path = os.path.join(NEW_PACKAGE_PATH, new_subdir)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "__init__.py"), "w") as f: pass

# Migration des fichiers
print("\n2. Migration des fichiers de code source...")
for old_dir, new_subdir in MODULE_MAP.items():
    source_path = os.path.join(OLD_PLATFORM_PATH, old_dir)
    dest_path = os.path.join(NEW_PACKAGE_PATH, new_subdir)
    
    print(f"   -> Copie de {source_path} vers {dest_path}")
    if not os.path.isdir(source_path):
        print(f"      AVERTISSEMENT: Le dossier source n'existe pas, ignoré : {source_path}")
        continue

    for item in os.listdir(source_path):
        s_item = os.path.join(source_path, item)
        d_item = os.path.join(dest_path, item)
        # On ne copie que les fichiers python et les dossiers de code
        if item.endswith(".py") or item in ["utils", "core", "calculs", "core_legacy", "data", "elements", "radiers"]:
            if os.path.isdir(s_item):
                shutil.copytree(s_item, d_item, dirs_exist_ok=True)
            else:
                shutil.copy2(s_item, d_item)

print("\n### MIGRATION DES FICHIERS TERMINÉE ###")
print("La nouvelle structure est prête dans le dossier 'src/'.")