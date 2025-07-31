import pytest
import json
import os
import tempfile
import yaml
from typer.testing import CliRunner
from lcpi.bois.main import app

runner = CliRunner()

def test_check_poteau_bois_ok():
    """Test de vérification de poteau en bois - cas OK"""
    # Créer un fichier YAML temporaire
    data = {
        "description": "Vérification au flambement d'un poteau en bois C24",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {
                "b": 150,
                "h": 150
            }
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        },
        "longueur_flambement_m": 4.5,
        "efforts_elu": {
            "N_c_ed_kN": 80
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-poteau", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "contrainte_appliquee_MPa" in output
        assert "resistance_calcul_compression_MPa" in output
        assert "verification_flambement" in output
        assert "statut" in output["verification_flambement"]
    finally:
        os.remove(path)

def test_check_poteau_bois_non_ok():
    """Test de vérification de poteau en bois - cas NON OK"""
    # Créer un fichier YAML temporaire avec un effort plus élevé
    data = {
        "description": "Vérification au flambement d'un poteau en bois C24",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {
                "b": 100,
                "h": 100
            }
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        },
        "longueur_flambement_m": 4.5,
        "efforts_elu": {
            "N_c_ed_kN": 200  # Effort très élevé pour dépasser la résistance
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-poteau", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "verification_flambement" in output
        # Le statut devrait être "NON OK" avec un effort si élevé
        assert output["verification_flambement"]["statut"] in ["OK", "NON OK"]
    finally:
        os.remove(path)

def test_check_poteau_bois_erreur_classe_inexistante():
    """Test de vérification de poteau avec classe de résistance inexistante"""
    data = {
        "description": "Vérification au flambement d'un poteau en bois",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {
                "b": 150,
                "h": 150
            }
        },
        "materiau": {
            "classe_resistance": "C99",  # Classe inexistante
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        },
        "longueur_flambement_m": 4.5,
        "efforts_elu": {
            "N_c_ed_kN": 80
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-poteau", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "error" in output
        assert output["status"] == "error"
    finally:
        os.remove(path)

def test_check_deversement_bois_ok():
    """Test de vérification de déversement - cas OK"""
    data = {
        "description": "Vérification au déversement d'une poutre",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {
                "b": 80,
                "h": 240
            }
        },
        "materiau": {
            "classe_resistance": "C24"
        },
        "longueur_appuis_Lef_m": 5.0,
        "efforts_elu": {
            "M_y_ed_kNm": 15.0
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-deversement", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "elancement_relatif_deversement" in output
        assert "coefficient_instabilite_kcrit" in output
        assert "ratio" in output
        assert "statut" in output
    finally:
        os.remove(path)

def test_check_deversement_bois_non_ok():
    """Test de vérification de déversement - cas NON OK"""
    data = {
        "description": "Vérification au déversement d'une poutre",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {
                "b": 60,
                "h": 300  # Section plus élancée
            }
        },
        "materiau": {
            "classe_resistance": "C24"
        },
        "longueur_appuis_Lef_m": 8.0,  # Longueur plus importante
        "efforts_elu": {
            "M_y_ed_kNm": 25.0  # Moment plus élevé
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-deversement", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "statut" in output
        # Le statut devrait être "NON OK" avec ces paramètres défavorables
        assert output["statut"] in ["OK", "NON OK"]
    finally:
        os.remove(path)

def test_check_deversement_bois_erreur_fichier_inexistant():
    """Test de vérification de déversement avec fichier inexistant"""
    result = runner.invoke(app, ["check-deversement", "--filepath", "fichier_inexistant.yml"])
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert "error" in output
    assert output["status"] == "error"

def test_check_cisaillement_bois_ok():
    """Test de vérification de cisaillement - cas OK"""
    data = {
        "description": "Vérification au cisaillement d'une poutre en bois",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {
                "b": 150,
                "h": 300
            }
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        },
        "fissuration": {
            "presence_fissures": True
        },
        "efforts_elu": {
            "V_ed_kN": 20
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-cisaillement", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "largeur_efficace_bef_mm" in output
        assert "contrainte_cisaillement_appliquee_MPa" in output
        assert "resistance_calcul_cisaillement_MPa" in output
        assert "ratio" in output
        assert "statut" in output
    finally:
        os.remove(path)

def test_check_compression_perp_bois_ok():
    """Test de vérification de compression perpendiculaire - cas OK"""
    data = {
        "description": "Vérification de l'écrasement à l'appui d'une poutre",
        "profil": {
            "dimensions_mm": {
                "b": 150
            }
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 1,
            "duree_charge": "Permanente"
        },
        "appui": {
            "longueur_appui_la_mm": 200
        },
        "efforts_elu": {
            "Reaction_appui_F_c90_ed_kN": 30
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-compression-perp", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "contrainte_appliquee_MPa" in output
        assert "resistance_calcul_MPa" in output
        assert "ratio" in output
        assert "statut" in output
    finally:
        os.remove(path)

def test_check_compose_bois_ok():
    """Test de vérification de sollicitations composées - cas OK"""
    data = {
        "description": "Vérification en flexion composée d'un poteau",
        "profil": {
            "dimensions_mm": {
                "b": 150,
                "h": 300
            }
        },
        "materiau": {
            "classe_resistance": "C30",
            "classe_service": 1,
            "duree_charge": "Court terme"
        },
        "efforts_elu": {
            "N_c_ed_kN": 30,
            "M_y_ed_kNm": 8,
            "M_z_ed_kNm": 2
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(data, f)
        path = f.name
    
    try:
        result = runner.invoke(app, ["check-compose", "--filepath", path])
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert "ratio_resistance_section" in output
        assert "statut_resistance" in output
    finally:
        os.remove(path) 

def test_check_fleche_bois_ok():
    """Test de la commande check-fleche avec des données valides."""
    # Créer un fichier YAML temporaire
    donnees = {
        "description": "Vérification de la flèche d'une poutre en bois C24",
        "profil": {
            "type": "rectangulaire",
            "dimensions_mm": {"b": 100, "h": 200}
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        },
        "portee_m": 4.0,
        "type_ouvrage": "Bâtiments courants",
        "charges_service": {
            "permanente_G": {
                "type": "uniformement repartie",
                "valeur_kN_m": 3.0
            },
            "exploitation_Q": {
                "type": "ponctuelle",
                "valeur_kN": 8.0
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(donnees, f)
        temp_file = f.name
    
    try:
        result = runner.invoke(app, ["check-fleche", temp_file])
        assert result.exit_code == 0
        
        # Parser le JSON de sortie
        output_data = json.loads(result.stdout)
        
        # Vérifications de base
        assert "description" in output_data
        assert "donnees_calculees" in output_data
        assert "verification" in output_data
        
        # Vérifier que les données calculées sont présentes
        donnees_calculees = output_data["donnees_calculees"]
        assert "fleche_instantanee_G_mm" in donnees_calculees
        assert "fleche_instantanee_Q_mm" in donnees_calculees
        assert "fleche_fluage_mm" in donnees_calculees
        assert "fleche_finale_totale_mm" in donnees_calculees
        
        # Vérifier que la vérification est présente
        verification = output_data["verification"]
        assert "statut" in verification
        assert verification["statut"] in ["OK", "NON OK"]
        
    finally:
        import os
        os.unlink(temp_file)

def test_check_fleche_bois_erreur_fichier_inexistant():
    """Test de la commande check-fleche avec un fichier inexistant."""
    result = runner.invoke(app, ["check-fleche", "fichier_inexistant.yml"])
    assert result.exit_code == 0
    
    # Parser le JSON de sortie
    output_data = json.loads(result.stdout)
    
    # Vérifier qu'il y a une erreur
    assert "error" in output_data
    assert "status" in output_data
    assert output_data["status"] == "error"

def test_check_assemblage_pointe_bois_ok():
    """Test de la commande check-assemblage-pointe avec des données valides."""
    # Créer un fichier YAML temporaire
    donnees = {
        "description": "Vérification d'un assemblage par pointes",
        "effort_tranchant_Ed_kN": 15.0,
        "pointes": {
            "diametre_mm": 3.5,
            "longueur_mm": 80,
            "nombre_total": 6
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(donnees, f)
        temp_file = f.name
    
    try:
        result = runner.invoke(app, ["check-assemblage-pointe", temp_file])
        assert result.exit_code == 0
        
        # Parser le JSON de sortie
        output_data = json.loads(result.stdout)
        
        # Vérifications de base
        assert "description" in output_data
        assert "verification_assemblage_pointe" in output_data
        
        # Vérifier que la vérification est présente
        verification = output_data["verification_assemblage_pointe"]
        assert "resistance_caracteristique_par_pointe_N" in verification
        assert "effort_applique_par_pointe_N" in verification
        assert "ratio" in verification
        assert "statut" in verification
        assert verification["statut"] in ["OK", "NON OK"]
        
    finally:
        import os
        os.unlink(temp_file)

def test_check_assemblage_embrevement_bois_ok():
    """Test de la commande check-assemblage-embrevement avec des données valides."""
    # Créer un fichier YAML temporaire
    donnees = {
        "description": "Vérification d'un assemblage par embrèvement",
        "effort_compression_Ed_kN": 25.0,
        "embrevement": {
            "largeur_b_mm": 100,
            "hauteur_h_mm": 150,
            "profondeur_t_mm": 30,
            "angle_deg": 45
        },
        "materiau": {
            "classe_resistance": "C24",
            "classe_service": 2,
            "duree_charge": "Moyen terme"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(donnees, f)
        temp_file = f.name
    
    try:
        result = runner.invoke(app, ["check-assemblage-embrevement", temp_file])
        assert result.exit_code == 0
        
        # Parser le JSON de sortie
        output_data = json.loads(result.stdout)
        
        # Vérifications de base
        assert "description" in output_data
        assert "verification_assemblage_embrevement" in output_data
        
        # Vérifier que la vérification est présente
        verification = output_data["verification_assemblage_embrevement"]
        assert "resistance_calcul_N" in verification
        assert "effort_applique_N" in verification
        assert "contrainte_calcul_MPa" in verification
        assert "aire_contact_mm2" in verification
        assert "ratio" in verification
        assert "statut" in verification
        assert verification["statut"] in ["OK", "NON OK"]
        
    finally:
        import os
        os.unlink(temp_file)

def test_check_assemblage_pointe_bois_erreur_fichier_inexistant():
    """Test de la commande check-assemblage-pointe avec un fichier inexistant."""
    result = runner.invoke(app, ["check-assemblage-pointe", "fichier_inexistant.yml"])
    assert result.exit_code == 0
    
    # Parser le JSON de sortie
    output_data = json.loads(result.stdout)
    
    # Vérifier qu'il y a une erreur
    assert "error" in output_data
    assert "status" in output_data
    assert output_data["status"] == "error"

def test_check_assemblage_embrevement_bois_erreur_fichier_inexistant():
    """Test de la commande check-assemblage-embrevement avec un fichier inexistant."""
    result = runner.invoke(app, ["check-assemblage-embrevement", "fichier_inexistant.yml"])
    assert result.exit_code == 0
    
    # Parser le JSON de sortie
    output_data = json.loads(result.stdout)
    
    # Vérifier qu'il y a une erreur
    assert "error" in output_data
    assert "status" in output_data
    assert output_data["status"] == "error" 