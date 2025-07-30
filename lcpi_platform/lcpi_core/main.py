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
# pour que `from lcpi_cm ...` fonctionne.
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


# -----------------------------------------------------------------------------
# Logique de découverte et de chargement des plugins
# -----------------------------------------------------------------------------

# Liste des modules plugins à charger. Le format est 'nom_du_dossier.nom_du_fichier'.
PLUGIN_MODULES = [
    "lcpi_cm.main",
    "lcpi_bois.main",
    "lcpi_beton.main",
    "lcpi_hydrodrain.main",
]

print("--- Initialisation de LCPI-CLI ---")

for plugin_module_str in PLUGIN_MODULES:
    try:
        # Importe le module dynamiquement
        module = importlib.import_module(plugin_module_str)
        
        # Le nom du plugin est la première partie (ex: "lcpi_cm")
        plugin_name = plugin_module_str.split('.')[0].replace('lcpi_', '')
        
        # Cas spécial pour le nouveau nom de commande
        if plugin_name == "hydrodrain":
            command_name = "hydro"
        else:
            command_name = plugin_name

        # Récupère la fonction d'enregistrement et l'exécute
        register_func = getattr(module, "register")
        plugin_app = register_func()
        
        # Ajoute le groupe de commandes du plugin à l'application principale
        app.add_typer(plugin_app, name=command_name)
        
        print(f"[SUCCES] Plugin '{plugin_name}' charge.")
        
    except ImportError as e:
        plugin_name = plugin_module_str.split('.')[0].replace('lcpi_', '')
        print(f"[ECHEC] Plugin '{plugin_name}' non charge. Erreur : {e}")
    except AttributeError:
        plugin_name = plugin_module_str.split('.')[0].replace('lcpi_', '')
        print(f"[ECHEC] Plugin '{plugin_name}' mal configure. La fonction 'register' est manquante.")

print("----------------------------------")

# -----------------------------------------------------------------------------
# Exécution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app()