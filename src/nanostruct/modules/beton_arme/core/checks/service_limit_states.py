# PROJET_DIMENTIONEMENT/BA/core/checks/service_limit_states.py
# Fonctions pour les vérifications à l'État Limite de Service (ELS)

from nanostruct.utils.ui_helpers import v_print

def check_concrete_compression_stress(Nser_kN, section, beton):
    """
    Vérifie la contrainte de compression dans le béton à l'ELS.
    Règle : σ_bc <= 0.6 * f_c28
    
    Args:
        Nser_kN (float): Effort normal de service (en kN).
        section (object): Objet section avec les attributs b et h (en m).
        beton (object): Objet béton avec l'attribut fc28 (en MPa).
    
    Returns:
        dict: Dictionnaire avec le statut et les valeurs de la vérification.
    """
    Nser_MN = Nser_kN / 1000
    area_m2 = section.b * section.h
    
    # Contrainte agissante en MPa (1 MPa = 1 MN/m²)
    sigma_bc_acting = Nser_MN / area_m2 if area_m2 > 0 else 0
    
    # Contrainte limite
    sigma_bc_limit = 0.6 * beton.fc28
    
    v_print("Contrainte béton (ELS)", "σ_bc = Nser / B", f"{Nser_MN:.3f} / {area_m2:.3f}", sigma_bc_acting, "MPa")
    v_print("Contrainte limite béton", "σ_lim = 0.6 * fc28", f"0.6 * {beton.fc28}", sigma_bc_limit, "MPa")
    
    if sigma_bc_acting <= sigma_bc_limit:
        return {"status": "OK", "message": "Contrainte de compression du béton vérifiée."}
    else:
        return {"status": "NON CONFORME", "message": "Contrainte de compression du béton dépassée. Augmenter la section."}

def check_soil_bearing_pressure(total_p_ser_kN, radier_dims):
    """
    Vérifie la contrainte sous le radier à l'ELS pour limiter les tassements.
    
    Args:
        total_p_ser_kN (float): Somme des charges de service des poteaux (en kN).
        radier_dims (tuple): Dimensions du radier (A, B) en mètres.
    
    Returns:
        float: La contrainte de service sous le radier (en kPa).
    """
    A, B = radier_dims
    surface = A * B
    
    sigma_sol_ser = total_p_ser_kN / surface if surface > 0 else 0
    
    v_print("Contrainte au sol (ELS)", "σ_ser = ΣP_ser / S", f"{total_p_ser_kN:.1f} / {surface:.2f}", sigma_sol_ser, "kPa")
    
    return sigma_sol_ser