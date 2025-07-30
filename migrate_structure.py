import os
import shutil

# Définir les chemins source et destination
OLD_PLATFORM_PATH = "lcpi_platform"
NEW_SRC_PATH = "src"

# Dictionnaire de correspondance pour les plugins
PLUGIN_MAPPING = {
    "lcpi_core": "lcpi",
    "lcpi_cm": "lcpi/cm",
    "lcpi_bois": "lcpi/bois",
    "lcpi_beton": "lcpi/beton",
    "lcpi_hydrodrain": "lcpi/hydrodrain"
}

def move_files(source_dir, dest_dir):
    """Déplace tous les fichiers et dossiers d'un répertoire source vers un répertoire de destination."""
    if not os.path.exists(source_dir):
        print(f"AVERTISSEMENT: Le dossier source n'existe pas: {source_dir}")
        return

    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        print(f"Déplacement de {source_item} vers {dest_item}")
        shutil.move(source_item, dest_item)

if __name__ == "__main__":
    print("### DÉBUT DE LA MIGRATION DE LA STRUCTURE DU PROJET ###")

    # Déplacer le noyau
    core_source = os.path.join(OLD_PLATFORM_PATH, "lcpi_core", "src", "lcpi_core")
    core_dest = os.path.join(NEW_SRC_PATH, "lcpi")
    if os.path.exists(os.path.join(core_source, "main.py")):
        shutil.move(os.path.join(core_source, "main.py"), os.path.join(core_dest, "main.py"))
    if os.path.exists(os.path.join(core_source, "utils")):
        move_files(os.path.join(core_source, "utils"), os.path.join(core_dest, "utils"))

    # Déplacer les plugins
    for old_plugin, new_plugin_path in PLUGIN_MAPPING.items():
        if old_plugin == "lcpi_core":
            continue
        plugin_source = os.path.join(OLD_PLATFORM_PATH, old_plugin, "src", old_plugin)
        plugin_dest = os.path.join(NEW_SRC_PATH, new_plugin_path)
        move_files(plugin_source, plugin_dest)

    print("### MIGRATION DE LA STRUCTURE TERMINÉE ###")
