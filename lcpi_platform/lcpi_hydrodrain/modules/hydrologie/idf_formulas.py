# modules/hydrologie/idf_formulas.py
from ...utils.ui import print_colored


def _calculer_intensite_montana(tc_min, params):
    """Calcule l'intensité avec la formule de Montana : i = a * tc^b."""
    a = params["a"]
    b = params["b"]
    return a * (tc_min**b)


def _calculer_intensite_talbot(tc_min, params):
    """Calcule l'intensité avec la formule de Talbot : i = a / (b + tc)."""
    a = params["a"]
    b = params["b"]
    if (b + tc_min) == 0:
        return float("inf")
    return a / (b + tc_min)


def _calculer_intensite_kiefer_chu(tc_min, params):
    """Calcule l'intensité avec la formule de Kiefer-Chu : i = a / ((tc + b)^c)."""
    a = params["a"]
    b = params["b"]
    c = params["c"]
    if (tc_min + b) <= 0:
        return float("inf")
    return a / ((tc_min + b) ** c)


def calculer_intensite_pluie(tc_min: float, idf_params: dict, verbose=False) -> float:
    """
    Dispatcher qui appelle la bonne formule IDF en fonction des paramètres.
    'idf_params' est le dictionnaire complet, incluant la clé 'formula'.
    """
    formula = idf_params.get("formula", "montana").lower()

    if formula == "montana":
        intensite = _calculer_intensite_montana(tc_min, idf_params)
    elif formula == "talbot":
        intensite = _calculer_intensite_talbot(tc_min, idf_params)
    elif formula == "kiefer-chu":
        intensite = _calculer_intensite_kiefer_chu(tc_min, idf_params)
    else:
        raise ValueError(f"Formule IDF non reconnue : {formula}")

    if verbose:
        print_colored(
            f"\n   -> Calcul de l'intensité (i) via {formula.capitalize()}:", "yellow"
        )
        print(f"      Avec Tc={tc_min:.2f} min et paramètres {idf_params}")
        print(f"      Résultat : i = {intensite:.2f} mm/h")

    return intensite
