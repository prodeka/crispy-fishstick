# tools/test_optimization_streaming.py
import sys
from pathlib import Path

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lcpi.aep.optimizer.controllers import OptimizationController

def main():
    """Test de l'optimisation avec streaming des flux"""
    print("🧪 Test de l'optimisation avec streaming des flux")
    
    # Chemin vers un fichier INP de test
    test_inp = Path("examples/bismark-Administrator.inp")
    if not test_inp.exists():
        print(f"❌ Fichier de test introuvable: {test_inp}")
        print("Création d'un fichier INP simple pour le test...")
        create_simple_inp(test_inp)
    
    # Configuration avec streaming activé
    algo_params = {
        "stream_flows": True,
        "generations": 5,  # Réduit pour le test
        "population": 10,  # Réduit pour le test
        "epanet_backend": "wntr"
    }
    
    constraints = {
        "pressure_min_m": 10.0,
        "velocity_min_m_s": 0.3,
        "velocity_max_m_s": 5.0,
    }
    
    print(f"📁 Fichier d'entrée: {test_inp}")
    print(f"⚙️  Paramètres: {algo_params}")
    
    # Créer le contrôleur
    controller = OptimizationController()
    
    # Lancer l'optimisation
    print("🚀 Lancement de l'optimisation...")
    result = controller.run_optimization(
        input_path=test_inp,
        method="genetic",
        solver="epanet",
        constraints=constraints,
        algo_params=algo_params,
        verbose=True,
        num_proposals=1
    )
    
    # Afficher les résultats
    print("\n📊 Résultats:")
    print(f"✅ Succès: {result.get('success', False)}")
    
    # Vérifier les artefacts de flux
    artifacts = result.get("meta", {}).get("artifacts", {}).get("flows", {})
    if artifacts:
        print("📈 Artefacts de flux générés:")
        for key, value in artifacts.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    print(f"  - {key}.{subkey}: {subvalue}")
            else:
                print(f"  - {key}: {value}")
    else:
        print("⚠️  Aucun artefact de flux trouvé")
    
    # Afficher les propositions
    proposals = result.get("proposals", [])
    if proposals:
        print(f"\n🏆 Meilleure proposition:")
        best = proposals[0]
        print(f"  - Coût: {best.get('CAPEX', 'N/A')} FCFA")
        print(f"  - Contraintes OK: {best.get('constraints_ok', 'N/A')}")
        print(f"  - Diamètres: {list(best.get('diameters_mm', {}).values())}")
    
    print("\n✅ Test terminé!")

def create_simple_inp(inp_path: Path):
    """Créer un fichier INP simple pour le test"""
    inp_content = """[TITLE]
Test Network for Flow Streaming

[JUNCTIONS]
J1         10.0    100.0   ;
J2         10.0    100.0   ;
J3         10.0    100.0   ;

[RESERVOIRS]
R1         50.0    0.0     ;

[PIPES]
P1         R1      J1      1000.0  315.0   100.0   ;
P2         J1      J2      800.0   315.0   100.0   ;
P3         J2      J3      600.0   315.0   100.0   ;

[DEMANDS]
J1         0.1     ;
J2         0.05    ;
J3         0.05    ;

[PATTERNS]
P1         1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     1.0     ;

[CONTROLS]
LINK P1 OPEN AT TIME 0

[OPTIONS]
UNITS           LPS
HEADLOSS        H-W
QUALITY         NONE
VISCOSITY       1.0
DIFFUSIVITY     1.0
SPECIFIC GRAVITY 1.0
TRIALS          40
ACCURACY        0.01
CHECKFREQ       2
MAXCHECK        10
DAMPLIMIT       0
UNBALANCED      STOP 10
PATTERN         1
DEMAND MULTIPLIER 1.0
EMITTER EXPONENT 0.5
QUALITY TOLERANCE 0.01
MAP             NONE

[REPORT]
STATUS          YES
SUMMARY         YES
PAGESIZE        0
FILE            NONE
PRESSURE        1
PRECISION       2
NODES           ALL
LINKS           ALL

[END]
"""
    inp_path.parent.mkdir(parents=True, exist_ok=True)
    with open(inp_path, 'w') as f:
        f.write(inp_content)
    print(f"✅ Fichier INP créé: {inp_path}")

if __name__ == "__main__":
    main()
