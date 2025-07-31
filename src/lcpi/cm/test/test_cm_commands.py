import os
import tempfile
import json
import pytest
from typer.testing import CliRunner
from lcpi.cm.main import app

runner = CliRunner()

def write_yaml(data):
    fd, path = tempfile.mkstemp(suffix='.yml')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        import yaml
        yaml.dump(data, f, allow_unicode=True)
    return path

# --- Tests check-poteau ---
def test_check_poteau_ok():
    data = {
        'description': "Poteau IPE 200",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'longueurs_flambement': {'Lf_y_m': 3.0, 'Lf_z_m': 3.0},
        'efforts': {'N_ed_kN': 150}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-poteau", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["contrainte_appliquee_MPa"] > 0
    assert output["verification_flambement_plan_faible (axe z)"]["statut"] in ("OK", "NON OK")
    os.remove(path)

def test_check_poteau_non_ok():
    data = {
        'description': "Poteau IPE 200 surchargé",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'longueurs_flambement': {'Lf_y_m': 10.0, 'Lf_z_m': 10.0},
        'efforts': {'N_ed_kN': 2000}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-poteau", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["verification_flambement_plan_faible (axe z)"]["statut"] == "NON OK"
    os.remove(path)

# --- Tests check-deversement ---
def test_check_deversement_ok():
    data = {
        'description': "Poutre flexion simple",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'My_ed_kNm': 50}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-deversement", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["statut"] in ("OK", "NON OK")
    os.remove(path)

def test_check_deversement_non_ok():
    data = {
        'description': "Poutre flexion surchargée",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'My_ed_kNm': 10000}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-deversement", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["statut"] == "NON OK"
    os.remove(path)

# --- Tests check-tendu ---
def test_check_tendu_ok():
    data = {
        'description': "Tirant acier",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'N_ed_kN': 50}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-tendu", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["statut"] == "OK"
    os.remove(path)

def test_check_tendu_non_ok():
    data = {
        'description': "Tirant acier surchargé",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'N_ed_kN': 10000}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-tendu", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["statut"] == "NON OK"
    os.remove(path)

# --- Tests check-compose ---
def test_check_compose_flexion_composee():
    data = {
        'description': "Flexion composée",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'N_ed_kN': 100, 'My_ed_kNm': 50}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-compose", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["type_verification"] == "Flexion composée (N+My)"
    os.remove(path)

def test_check_compose_flexion_deviee():
    data = {
        'description': "Flexion déviée",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'My_ed_kNm': 50, 'Mz_ed_kNm': 30}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-compose", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["type_verification"] == "Flexion déviée (My+Mz)"
    os.remove(path)

# --- Tests pour vérifier la gestion des erreurs et warnings ---
def test_check_poteau_erreur_profil_inexistant():
    data = {
        'description': "Poteau avec profil inexistant",
        'profil': {'nom': 'PROFIL_INEXISTANT'},
        'materiau': {'nuance': 'S235'},
        'longueurs_flambement': {'Lf_y_m': 3.0, 'Lf_z_m': 3.0},
        'efforts': {'N_ed_kN': 150}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-poteau", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "error" in output
    assert output["status"] == "error"
    os.remove(path)

def test_check_deversement_avec_warning():
    data = {
        'description': "Poutre flexion simple",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'efforts': {'My_ed_kNm': 50}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-deversement", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "warning" in output
    assert output["statut"] in ("OK", "NON OK")
    os.remove(path)

# --- Tests pour check-fleche ---
def test_check_fleche_charge_uniforme():
    data = {
        'description': "Poutre IPE 240 sur appuis simples",
        'profil': {'nom': 'IPE 240'},
        'materiau': {'nuance': 'S235'},
        'portee_m': 6.0,
        'charges_service': {
            'permanente_G': {
                'type': 'uniformement repartie',
                'valeur_kN_m': 5.0
            },
            'exploitation_Q': {
                'type': 'uniformement repartie',
                'valeur_kN_m': 10.0
            }
        }
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-fleche", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "donnees_calculees" in output
    assert "verification" in output
    assert output["verification"]["statut"] in ("OK", "NON OK")
    os.remove(path)

def test_check_fleche_charge_ponctuelle():
    data = {
        'description': "Poutre IPE 200 avec charge ponctuelle",
        'profil': {'nom': 'IPE 200'},
        'materiau': {'nuance': 'S235'},
        'portee_m': 4.0,
        'charges_service': {
            'exploitation_Q': {
                'type': 'ponctuelle',
                'valeur_kN': 20.0,
                'position_m': 2.0
            }
        }
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-fleche", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "donnees_calculees" in output
    assert "verification" in output
    os.remove(path)

# --- Tests pour check-assemblage-boulon ---
def test_check_assemblage_boulon():
    data = {
        'description': "Assemblage par platine d'extrémité",
        'effort_tranchant_Ed_kN': 120.0,
        'platine': {
            'epaisseur_mm': 10,
            'nuance_acier': 'S235'
        },
        'boulons': {
            'classe_qualite': '8.8',
            'diametre_mm': 20,
            'nombre_total': 4,
            'plan_cisaillement_dans_filetage': True
        },
        'geometrie': {
            'p1': 50,
            'e1': 80,
            'e2': 80
        }
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-assemblage-boulon", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "warning" in output
    assert "verification_cisaillement_boulon" in output
    assert "verification_pression_diametrale" in output
    os.remove(path)

# --- Tests pour check-assemblage-soude ---
def test_check_assemblage_soude():
    data = {
        'description': "Cordon de soudure d'angle",
        'longueur_efficace_mm': 150,
        'epaisseur_gorge_a_mm': 5,
        'materiau_base': {
            'nuance': 'S235'
        },
        'effort_applique_kN_par_mm': 0.8
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["check-assemblage-soude", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "warning" in output
    assert "resistance_calcul_soudure_N_par_mm" in output
    assert "ratio" in output
    assert "statut" in output
    os.remove(path)

# --- Tests pour optimize-section ---
def test_optimize_section_poteau():
    data = {
        'description': "Optimisation poteau",
        'profil': {'nom': 'IPE 200'},  # Sera remplacé par l'optimisation
        'materiau': {'nuance': 'S235'},
        'longueurs_flambement': {'Lf_y_m': 3.0, 'Lf_z_m': 3.0},
        'efforts': {'N_ed_kN': 150}
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["optimize-section", "--check", "poteau", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "statut_optimisation" in output
    os.remove(path)

def test_optimize_section_fleche():
    data = {
        'description': "Optimisation flèche",
        'profil': {'nom': 'IPE 200'},  # Sera remplacé par l'optimisation
        'materiau': {'nuance': 'S235'},
        'portee_m': 6.0,
        'charges_service': {
            'permanente_G': {
                'type': 'uniformement repartie',
                'valeur_kN_m': 5.0
            },
            'exploitation_Q': {
                'type': 'uniformement repartie',
                'valeur_kN_m': 10.0
            }
        }
    }
    path = write_yaml(data)
    result = runner.invoke(app, ["optimize-section", "--check", "fleche", "--filepath", path])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "statut_optimisation" in output
    os.remove(path)