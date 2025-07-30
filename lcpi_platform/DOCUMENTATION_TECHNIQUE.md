# Documentation Technique LCPI Platform

## Architecture détaillée

### 1. Module Core (`lcpi_core/`)

#### 1.1 Point d'entrée principal (`main.py`)

**Responsabilités :**
- Gestion de l'application CLI principale
- Chargement dynamique des plugins
- Orchestration des commandes

**Architecture :**
```python
# Configuration des chemins
platform_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if platform_path not in sys.path:
    sys.path.insert(0, platform_path)

# Application Typer principale
app = typer.Typer(
    name="lcpi",
    help="LCPI-CLI: Plateforme de Calcul Polyvalent pour l'Ingénierie.",
    rich_markup_mode="markdown"
)
```

**Commande `report` :**
```python
@app.command()
def report(project_dir: str = typer.Argument(".")):
    """Analyse tous les éléments d'un projet et génère un rapport."""
    # Scan des dossiers d'éléments
    plugin_element_dirs = {
        "cm": "lcpi_platform/lcpi_cm/elements",
        "bois": "lcpi_platform/lcpi_bois/elements",
    }
    
    # Exécution des calculs via subprocess
    command = [
        sys.executable, "-m", "lcpi_platform.lcpi_core.main",
        plugin, "calc" if plugin != "bois" else "check",
        filepath, "--json"
    ]
```

**Chargement des plugins :**
```python
PLUGIN_MODULES = [
    "lcpi_cm.main",
    "lcpi_bois.main", 
    "lcpi_beton.main",
    "lcpi_hydrodrain.main",
]

for plugin_module_str in PLUGIN_MODULES:
    module = importlib.import_module(plugin_module_str)
    register_func = getattr(module, "register")
    plugin_app = register_func()
    app.add_typer(plugin_app, name=command_name)
```

#### 1.2 Calculs de base (`calculs.py`)

**Fonction principale :**
```python
def calculer_sollicitations_completes(
    longueur, charges_list, materiau, categorie_usage, verbose=True
):
    """
    Calcule toutes les combinaisons d'actions pour l'ELU et l'ELS.
    
    Args:
        longueur: Longueur de l'élément (m)
        charges_list: Liste des charges [{'type': 'repartie', 'valeur': 5.0, 'categorie': 'G'}]
        materiau: 'acier' ou 'bois'
        categorie_usage: Catégorie d'usage pour le bois
        verbose: Mode verbeux
    
    Returns:
        dict: Sollicitations maximales {M_Ed, V_Ed, p_ser}
    """
```

**Combinaisons d'actions :**

Pour l'acier :
```python
combinaisons_elu = [
    {"desc": "1.35G + 1.5Q", "p_Ed": gamma_G * G + gamma_Q * Q},
    {"desc": "1.35G + 1.5W", "p_Ed": gamma_G * G + gamma_Q * W},
    {"desc": "1.35G + 1.5S", "p_Ed": gamma_G * G + gamma_Q * S},
    # ...
]
```

Pour le bois :
```python
# Cas 1: Q en base
p_Ed1 = base_G + gamma_Q * Q + gamma_Q * psi0 * W + gamma_Q * psi0 * S
# Cas 2: W en base  
p_Ed2 = base_G + gamma_Q * W + gamma_Q * psi0 * Q + gamma_Q * psi0 * S
```

#### 1.3 Génération de rapports (`reporter.py`)

```python
def generate_pdf_report(results_list: list, output_filename: str):
    """Génère un rapport PDF simple à partir d'une liste de résultats."""
    doc = SimpleDocTemplate(output_filename)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("Rapport d'Analyse LCPI-CLI", styles['h1']))
    
    for result in results_list:
        element_id = result.get('element_id', 'Inconnu')
        plugin = result.get('plugin', 'Inconnu')
        
        story.append(Paragraph(f"Élément : {element_id} (Plugin: {plugin})", styles['h2']))
        # ...
```

### 2. Module Construction Métallique (`lcpi_cm/`)

#### 2.1 Interface principale (`main.py`)

**Structure des commandes :**
```python
app = typer.Typer(name="cm", help="Plugin pour la Construction Métallique")

@app.command(name="calc")
def run_calc_from_file(
    filepath: str = typer.Option(None, "--filepath"),
    batch_file: str = typer.Option(None, "--batch-file"),
    output_file: str = typer.Option("resultats_batch.csv", "--output-file"),
    as_json: bool = typer.Option(False, "--json")
):
```

**Logique de calcul :**
```python
def _calculer_poutre_acier_logic(data: dict) -> dict:
    longueur = data.get("longueur")
    charges_entrees = data.get("charges")
    nuance = data.get("nuance")
    fy = data.get("fy_MPa")
    E_module = data.get("E_MPa")
    
    # Calcul des sollicitations
    sollicitations = calculer_sollicitations_completes(
        longueur, charges_entrees, "acier", "A", verbose=False
    )
    
    # Dimensionnement du profil
    profil_recommande = trouver_profil_acier(
        sollicitations["M_Ed"], 
        sollicitations["V_Ed"], 
        longueur, 
        sollicitations["p_ser"],
        famille_profil=famille_profil,
        nuance=nuance,
        fy_MPa=fy,
        E_MPa=E_module
    )
    
    return {
        "profil_recommande": profil_recommande,
        "M_Ed": sollicitations["M_Ed"],
        "V_Ed": sollicitations["V_Ed"],
        "p_ser": sollicitations["p_ser"],
        "statut": "OK"
    }
```

#### 2.2 Calculs métalliques (`calculs.py`)

**Dimensionnement des profils :**
```python
def trouver_profil_acier(M_Ed, V_Ed, longueur, p_ser, famille_profil="IPE", 
                        nuance="S235", fy_MPa=235.0, E_MPa=210000.0, verbose=True):
    """
    Trouve le profil en acier le plus économique qui vérifie tous les critères.
    
    Args:
        M_Ed: Moment de flexion de calcul (kN.m)
        V_Ed: Effort tranchant de calcul (kN)
        longueur: Longueur de la poutre (m)
        p_ser: Charge de service (kN/m)
        famille_profil: Famille de profil ('IPE', 'HEA', etc.)
        nuance: Nuance d'acier
        fy_MPa: Limite élastique (MPa)
        E_MPa: Module d'Young (MPa)
    
    Returns:
        dict: Profil recommandé avec toutes les vérifications
    """
```

**Vérifications :**
- Résistance en flexion : `M_Ed ≤ M_Rd`
- Résistance en cisaillement : `V_Ed ≤ V_Rd`
- Déformation admissible : `δ ≤ L/300`
- Déversement : Vérification de la stabilité

### 3. Module Construction Bois (`lcpi_bois/`)

#### 3.1 Interface principale (`main.py`)

```python
@app.command(name="check")
def run_check_from_file(
    filepath: str = typer.Option(None, "--filepath"),
    as_json: bool = typer.Option(False, "--json")
):
    """Vérifie un élément en bois à partir d'un fichier YAML."""
```

#### 3.2 Calculs bois (`calculs.py`)

**Classes de bois :**
```python
CLASSES_BOIS = {
    "C14": {"fm_k": 14, "fv_k": 2.7, "E_mean": 7000, "G_mean": 440},
    "C16": {"fm_k": 16, "fv_k": 1.8, "E_mean": 8000, "G_mean": 500},
    "C18": {"fm_k": 18, "fv_k": 2.0, "E_mean": 9000, "G_mean": 560},
    "C20": {"fm_k": 20, "fv_k": 2.2, "E_mean": 9500, "G_mean": 590},
    "C22": {"fm_k": 22, "fv_k": 2.4, "E_mean": 10000, "G_mean": 630},
    "C24": {"fm_k": 24, "fv_k": 2.5, "E_mean": 11000, "G_mean": 690},
    "C27": {"fm_k": 27, "fv_k": 2.8, "E_mean": 11500, "G_mean": 720},
    "C30": {"fm_k": 30, "fv_k": 3.0, "E_mean": 12000, "G_mean": 750},
    "C35": {"fm_k": 35, "fv_k": 3.4, "E_mean": 13000, "G_mean": 810},
    "C40": {"fm_k": 40, "fv_k": 3.8, "E_mean": 14000, "G_mean": 870},
}
```

**Vérifications selon Eurocode 5 :**
```python
def verifier_element_bois(longueur, classe_bois, categorie_usage, charges_list):
    """
    Vérifie un élément en bois selon l'Eurocode 5.
    
    Vérifications :
    1. Résistance en flexion (ELU)
    2. Résistance en cisaillement (ELU) 
    3. Déformation (ELS)
    4. Stabilité au déversement
    """
```

### 4. Module Béton Armé (`lcpi_beton/`)

#### 4.1 Point d'entrée (`ba_entry.py`)

**Interface unifiée :**
```python
class BetonArmeCalculator:
    """Calculateur principal pour le béton armé."""
    
    def __init__(self):
        self.materials = Materials()
        self.sections = Sections()
    
    def calculer_poutre(self, data):
        """Calcul d'une poutre en béton armé."""
        
    def calculer_colonne(self, data):
        """Calcul d'une colonne en béton armé."""
        
    def calculer_radier(self, data):
        """Calcul d'un radier de fondation."""
```

#### 4.2 Core du module (`core/`)

**Analyse des structures (`analysis/`) :**
```python
# continuous_beam.py
class ContinuousBeam:
    """Analyse de poutres continues."""
    
    def __init__(self, spans, loads):
        self.spans = spans
        self.loads = loads
    
    def calculate_moments(self):
        """Calcule les moments de flexion."""
        
    def calculate_shear_forces(self):
        """Calcule les efforts tranchants."""
```

**Vérifications (`checks/`) :**
```python
# service_limit_states.py
class ServiceLimitStates:
    """Vérification des états limites de service."""
    
    def check_deflection(self, beam, load):
        """Vérifie la déformation."""
        
    def check_cracking(self, beam, load):
        """Vérifie la fissuration."""
```

**Dimensionnement (`design/`) :**
```python
# column_design.py
class ColumnDesign:
    """Dimensionnement des colonnes."""
    
    def design_reinforcement(self, column, loads):
        """Dimensionne les armatures."""
        
    def check_buckling(self, column):
        """Vérifie le flambement."""
```

### 5. Module Hydraulique (`lcpi_hydrodrain/`)

#### 5.1 Moteur de calcul (`core/engine.py`)

```python
class HydraulicEngine:
    """Moteur de calcul hydraulique principal."""
    
    def __init__(self):
        self.models = Models()
        self.formulas = SharedFormulas()
    
    def calculate_network(self, network_data):
        """Calcule un réseau d'assainissement."""
        
    def calculate_basin(self, basin_data):
        """Calcule un bassin versant."""
        
    def calculate_pumping(self, pump_data):
        """Calcule une station de pompage."""
```

#### 5.2 Calculs spécialisés (`calculs/`)

**Assainissement gravitaire (`assainissement_gravitaire.py`) :**
```python
def dimensionner_canalisation(debit, pente, rugosite, diametres_disponibles):
    """
    Dimensionne une canalisation d'assainissement.
    
    Args:
        debit: Débit de calcul (L/s)
        pente: Pente de la canalisation (%)
        rugosite: Coefficient de rugosité (mm)
        diametres_disponibles: Liste des diamètres disponibles (mm)
    
    Returns:
        dict: Diamètre recommandé et caractéristiques hydrauliques
    """
```

**Hydrologie (`hydrologie.py`) :**
```python
def calculer_debit_pluie(surface, intensite, coefficient_ruissellement):
    """
    Calcule le débit de pointe par la méthode rationnelle.
    
    Args:
        surface: Surface du bassin versant (ha)
        intensite: Intensité de pluie (mm/h)
        coefficient_ruissellement: Coefficient de ruissellement
    
    Returns:
        float: Débit de pointe (L/s)
    """
```

#### 5.3 Modèles hydrologiques (`modules/hydrologie/`)

**Méthode de Caquot (`caquot.py`) :**
```python
def methode_caquot(debit, pente, longueur, surface):
    """
    Applique la méthode de Caquot pour le dimensionnement.
    
    Cette méthode est utilisée pour les réseaux d'assainissement
    unitaires en France.
    """
```

**Formules IDF (`idf_formulas.py`) :**
```python
def formule_idf(duree, periode_retour, region):
    """
    Calcule l'intensité de pluie selon les formules IDF.
    
    Args:
        duree: Durée de la pluie (min)
        periode_retour: Période de retour (ans)
        region: Région climatique
    
    Returns:
        float: Intensité de pluie (mm/h)
    """
```

## Formats de données

### 1. YAML pour les éléments

**Construction Métallique :**
```yaml
longueur: 6.0
nuance: S235
fy_MPa: 235.0
E_MPa: 210000.0
famille_profil: IPE
charges:
  permanentes_G:
    - type: repartie
      valeur: 5.0
      description: "Poids propre + revêtements"
  exploitation_Q:
    - type: repartie
      valeur: 3.0
      description: "Charge d'exploitation"
    - type: ponctuelle
      valeur: 10.0
      position: 3.0
      description: "Charge ponctuelle"
```

**Construction Bois :**
```yaml
longueur: 4.0
classe_bois: C24
categorie_usage: A
section:
  largeur: 0.08
  hauteur: 0.20
charges:
  permanentes_G:
    - type: repartie
      valeur: 2.0
  exploitation_Q:
    - type: repartie
      valeur: 1.5
```

### 2. CSV pour le traitement par lot

**Format d'entrée :**
```csv
longueur_m,charge_G_kn_m,charge_Q_kn_m,nuance,fy_MPa,E_MPa,famille_profil
6.0,5.0,3.0,S235,235.0,210000.0,IPE
8.0,6.0,4.0,S355,355.0,210000.0,HEA
```

**Format de sortie :**
```csv
longueur_m,charge_G_kn_m,charge_Q_kn_m,nuance,profil_recommande,M_Ed,V_Ed,p_ser,statut
6.0,5.0,3.0,S235,IPE200,45.2,24.8,8.0,OK
8.0,6.0,4.0,S355,HEA200,67.8,32.4,10.0,OK
```

### 3. JSON pour l'intégration

**Format de sortie JSON :**
```json
{
  "statut": "OK",
  "profil_recommande": "IPE200",
  "M_Ed": 45.2,
  "V_Ed": 24.8,
  "p_ser": 8.0,
  "verifications": {
    "flexion": "OK",
    "cisaillement": "OK", 
    "deformation": "OK",
    "deversement": "OK"
  },
  "proprietes_profil": {
    "W_el": 194.0,
    "I": 1940.0,
    "A": 28.5
  }
}
```

## Système de plugins

### 1. Interface requise

Chaque plugin doit exposer une fonction `register()` :

```python
def register():
    """Enregistre le plugin dans l'application principale."""
    app = typer.Typer(name="nom_plugin", help="Description du plugin")
    
    @app.command()
    def calc(filepath: str):
        """Commande principale du plugin."""
        # Logique du plugin
        pass
    
    return app
```

### 2. Structure recommandée

```
lcpi_nouveau_module/
├── __init__.py
├── main.py          # Point d'entrée avec register()
├── calculs.py       # Logique de calcul
├── elements/        # Fichiers d'exemples
│   └── exemple.yml
└── pyproject.toml   # Métadonnées
```

### 3. Intégration automatique

Le système charge automatiquement tous les modules listés dans `PLUGIN_MODULES` :

```python
PLUGIN_MODULES = [
    "lcpi_cm.main",
    "lcpi_bois.main",
    "lcpi_beton.main", 
    "lcpi_hydrodrain.main",
    # Ajouter ici les nouveaux modules
]
```

## Tests et validation

### 1. Tests unitaires

```python
# test_calculs.py
def test_calculer_sollicitations_completes():
    """Test du calcul des sollicitations."""
    charges = [{'type': 'repartie', 'valeur': 5.0, 'categorie': 'G'}]
    result = calculer_sollicitations_completes(6.0, charges, "acier", "A")
    
    assert result["M_Ed"] == pytest.approx(22.5, rel=1e-2)
    assert result["V_Ed"] == pytest.approx(15.0, rel=1e-2)
```

### 2. Tests d'intégration

```python
# test_integration.py
def test_plugin_cm_integration():
    """Test d'intégration du plugin CM."""
    # Test avec un fichier YAML réel
    result = run_calc_from_file("elements/poutre_test.yml")
    assert result["statut"] == "OK"
```

### 3. Validation des résultats

**Comparaison avec des logiciels de référence :**
- Robot Structural Analysis
- SAP2000
- Autodesk Structural Bridge Design

**Validation par calculs manuels :**
- Vérification des formules
- Contrôle des unités
- Validation des hypothèses

## Performance et optimisation

### 1. Optimisations actuelles

- **Cache des calculs** : Mise en cache des résultats fréquents
- **Calculs vectorisés** : Utilisation de NumPy pour les calculs matriciels
- **Chargement lazy** : Chargement des données à la demande

### 2. Optimisations futures

- **Parallélisation** : Calculs en parallèle pour les gros projets
- **Base de données** : Stockage des résultats pour réutilisation
- **API asynchrone** : Interface web asynchrone

## Sécurité et robustesse

### 1. Validation des entrées

```python
def valider_donnees_entree(data):
    """Valide les données d'entrée."""
    required_fields = ['longueur', 'charges', 'nuance']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Champ requis manquant: {field}")
    
    if data['longueur'] <= 0:
        raise ValueError("La longueur doit être positive")
```

### 2. Gestion des erreurs

```python
try:
    result = calculer_poutre_acier_logic(data)
except ValueError as e:
    return {"statut": "Erreur", "message": str(e)}
except Exception as e:
    return {"statut": "Erreur", "message": f"Erreur inattendue: {e}"}
```

### 3. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculer_poutre_acier_logic(data):
    logger.info(f"Début du calcul pour {data}")
    # ...
    logger.info(f"Calcul terminé: {result}")
    return result
```

## Maintenance et évolution

### 1. Versioning

- **Version sémantique** : MAJOR.MINOR.PATCH
- **Changelog** : Documentation des changements
- **Compatibilité** : Maintien de la compatibilité ascendante

### 2. Documentation

- **Docstrings** : Documentation inline du code
- **README** : Documentation utilisateur
- **API docs** : Documentation technique

### 3. Tests automatisés

- **CI/CD** : Tests automatiques à chaque commit
- **Coverage** : Mesure de la couverture de code
- **Performance** : Tests de performance

Cette documentation technique fournit une vue d'ensemble complète de l'architecture et de l'implémentation de la plateforme LCPI. 