import typer
import sys
import os
import importlib
import subprocess
import json
from .reporter import generate_pdf_report

# -----------------------------------------------------------------------------
# Configuration des chemins pour le développement
# -----------------------------------------------------------------------------
# On s'assure que le dossier `lcpi_platform` est dans le path
# pour que `from lcpi.cm ...` fonctionne.
platform_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if platform_path not in sys.path:
    sys.path.insert(0, platform_path)

# -----------------------------------------------------------------------------
# Application principale Typer
# -----------------------------------------------------------------------------
app = typer.Typer(
    name="lcpi",
    help="LCPI-CLI: Plateforme de Calcul Polyvalent pour l'Ingénierie.",
    rich_markup_mode="markdown"
)

# --- Commandes du noyau (placeholders) ---
@app.command()
def init(nom_projet: str = typer.Argument("nouveau_projet_lcpi")):
    """Initialise une nouvelle structure de projet LCPI."""
    print(f"PLACEHOLDER: Création du projet '{nom_projet}'...")

@app.command()
def plugins(action: str = typer.Argument(..., help="Action à effectuer : list, install, uninstall, search, update.")):
    """Gère le cycle de vie des plugins."""
    print(f"PLACEHOLDER: Action '{action}' sur les plugins...")

@app.command()
def config(action: str, cle: str = typer.Argument(None), valeur: str = typer.Argument(None)):
    """Gère la configuration de LCPI (get|set|list)."""
    print(f"PLACEHOLDER: Action '{action}' sur la configuration...")

@app.command()
def doctor():
    """Vérifie l'installation et les dépendances de LCPI-CLI."""
    print("PLACEHOLDER: Vérification du système (dépendances, compatibilité plugins)...")

@app.command()
def report(project_dir: str = typer.Argument(".")):
    """Analyse tous les éléments d'un projet et génère un rapport."""
    print(f"--- Lancement de l'analyse du projet dans : {project_dir} ---")
    
    all_results = []
    plugin_element_dirs = {
        "cm": "lcpi_platform/lcpi_cm/elements",
        "bois": "lcpi_platform/lcpi_bois/elements",
    }

    for plugin, elements_dir in plugin_element_dirs.items():
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_elements_path = os.path.join(base_path, elements_dir)
        
        if not os.path.isdir(full_elements_path):
            continue

        print(f"\nScanning plugin '{plugin}' dans {full_elements_path}...")
        for filename in os.listdir(full_elements_path):
            if filename.endswith(".yml"):
                filepath = os.path.join(full_elements_path, filename)
                print(f"  -> Analyse de l'élément : {filepath}")
                
                command = [
                    sys.executable, "-m", "lcpi_platform.lcpi_core.main",
                    plugin, "calc" if plugin != "bois" else "check",
                    filepath,
                    "--json"
                ]
                
                result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
                
                if result.returncode == 0 and result.stdout:
                    try:
                        # Trouve le début du JSON (la première accolade)
                        json_start_index = result.stdout.find('{')
                        if json_start_index != -1:
                            json_output = result.stdout[json_start_index:]
                            data = json.loads(json_output)
                            all_results.append({
                                "element_id": os.path.basename(filepath),
                                "plugin": plugin,
                                "resultats": data
                            })
                            print(f"     [SUCCES] Calcul terminé et résultats parsés.")
                        else:
                            raise json.JSONDecodeError("Marqueur JSON '{' non trouvé.", result.stdout, 0)
                            
                    except json.JSONDecodeError as e:
                        print(f"     [ERREUR] Impossible de parser la sortie JSON: {e}")
                        all_results.append({"element": filepath, "error": "JSONDecodeError", "output": result.stdout})
                else:
                    print(f"     [ERREUR] Le calcul a échoué.")
                    all_results.append({"element": filepath, "error": result.stderr, "output": result.stdout})
    
    print("\n--- Fin de l'analyse ---")
    print(f"{len(all_results)} éléments analysés.")
    
    # Générer le rapport PDF
    if all_results:
        generate_pdf_report(all_results, "rapport_lcpi.pdf")


# --- Logique de découverte et de chargement des plugins (VERSION CORRIGÉE) ---
print("--- Initialisation de LCPI-CLI ---")

try:
    # Le point (.) est crucial. Il signifie "depuis le même paquet que moi".
    from .cm.main import register as register_cm
    app.add_typer(register_cm(), name="cm")
    print("[SUCCES] Plugin 'cm' chargé.")
except ImportError as e:
    print(f"[ECHEC] Plugin 'cm' non chargé. Erreur : {e}")

try:
    from .bois.main import register as register_bois
    app.add_typer(register_bois(), name="bois")
    print("[SUCCES] Plugin 'bois' chargé.")
except ImportError as e:
    print(f"[ECHEC] Plugin 'bois' non chargé. Erreur : {e}")
    
try:
    from .beton.main import register as register_beton
    app.add_typer(register_beton(), name="beton")
    print("[SUCCES] Plugin 'beton' chargé.")
except ImportError as e:
    print(f"[ECHEC] Plugin 'beton' non chargé. Erreur : {e}")

try:
    from .hydrodrain.main import register as register_hydrodrain
    app.add_typer(register_hydrodrain(), name="hydro")
    print("[SUCCES] Plugin 'hydro' chargé.")
except ImportError as e:
    print(f"[ECHEC] Plugin 'hydro' non chargé. Erreur : {e}")

print("----------------------------------")

# --- Mode shell interactif ---
def run_interactive_shell():
    print("Bienvenue dans le shell interactif LCPI-CLI !")
    print("Tapez 'exit' ou 'quit' pour sortir.")
    while True:
        try:
            cmd = input('> ').strip()
            if cmd in ('exit', 'quit'):
                print('Sortie du shell interactif.')
                break
            if not cmd:
                continue
            # Exécute la commande comme si elle était passée à Typer
            args = cmd.split()
            app(args)
        except (EOFError, KeyboardInterrupt):
            print('\nSortie du shell interactif.')
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_interactive_shell()
    else:
        app()
