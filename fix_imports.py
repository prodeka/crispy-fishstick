import os
import glob

BASE_DIR = os.getcwd()
SRC_PATH = os.path.join(BASE_DIR, "src", "lcpi")

# Mapping from old import prefix to new import prefix
IMPORT_MAP = {
    "from lcpi_core": "from lcpi",
    "import lcpi_core": "import lcpi",
    "from lcpi_cm": "from lcpi.cm",
    "import lcpi_cm": "import lcpi.cm",
    "from lcpi_bois": "from lcpi.bois",
    "import lcpi_bois": "import lcpi.bois",
    "from lcpi_beton": "from lcpi.beton",
    "import lcpi_beton": "import lcpi.beton",
    "from lcpi_hydrodrain": "from lcpi.hydrodrain",
    "import lcpi_hydrodrain": "import lcpi.hydrodrain",
}

def fix_imports_in_file(file_path):
    """Fixes imports in a single Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"ERROR: Could not read file {file_path}: {e}")
            return 0

    original_content = content
    replacements_done = 0
    
    # Create a temporary variable for content modification
    modified_content = content

    for old_import, new_import in IMPORT_MAP.items():
        if old_import in modified_content:
            modified_content = modified_content.replace(old_import, new_import)
            
    # Check if content was actually changed before counting a replacement
    if original_content != modified_content:
        replacements_done = 1
        
    if replacements_done > 0:
        print(f"-> Fixing imports in {file_path}...")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"   Done.")
            return 1
        except Exception as e:
            print(f"ERROR: Could not write to file {file_path}: {e}")
            return 0
            
    return 0


def fix_all_imports():
    """Fixes all imports in the new package structure."""
    print("\n### DÉBUT DE LA CORRECTION DES IMPORTS ###")
    
    py_files = glob.glob(os.path.join(SRC_PATH, "**/*.py"), recursive=True)
    
    if not py_files:
        print("AVERTISSEMENT: Aucun fichier Python trouvé. La correction est terminée.")
        return

    files_modified = 0
    for file_path in py_files:
        files_modified += fix_imports_in_file(file_path)

    print(f"\n### CORRECTION DES IMPORTS TERMINÉE ###")
    print(f"{files_modified} fichier(s) ont été modifié(s).")
    print("Prochaine étape : réinstaller le projet.")


if __name__ == "__main__":
    fix_all_imports()