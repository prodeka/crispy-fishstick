from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .io import NetworkModel, sha256_of_file


class NetworkValidator:
    """Validations d'intégrité et de contenu minimal (MVP)."""

    def check_integrity(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {"ok": False, "errors": ["fichier introuvable"], "path": str(path)}
        try:
            checksum = sha256_of_file(path)
        except Exception as e:
            return {"ok": False, "errors": [f"lecture impossible: {e}"], "path": str(path)}
        return {"ok": True, "checksum": checksum, "path": str(path)}

    def validate_model(self, model: NetworkModel) -> Dict[str, Any]:
        errors = []
        if not model.nodes:
            errors.append("aucun noeud trouvé")
        if not model.links:
            errors.append("aucun lien trouvé")
        if not model.tanks:
            errors.append("aucun réservoir/tank défini")
        return {"ok": len(errors) == 0, "errors": errors}


def check_inp_feasibility(inp_path: Path, simulate: bool = True, timestep_min: int = 5) -> Dict[str, Any]:
    """
    Vérifie rapidement la faisabilité physique d'un .inp.
    Retourne {ok, errors, warnings, simulator_info}.
    """
    result: Dict[str, Any] = {"ok": True, "errors": [], "warnings": [], "simulator_info": None}
    try:
        import wntr  # type: ignore
    except Exception as e:
        result["warnings"].append(f"WNTR indisponible: {e}")
        simulate = False

    try:
        from pathlib import Path as _P
        if not _P(inp_path).exists():
            result["ok"] = False
            result["errors"].append(f"Fichier introuvable: {inp_path}")
            return result
        if simulate:
            wn = wntr.network.WaterNetworkModel(str(inp_path))  # type: ignore
            # checks basiques sur diam/longueur
            for pipe_id in getattr(wn, 'pipe_name_list', []):
                p = wn.get_link(pipe_id)
                if getattr(p, 'length', 1.0) <= 0:
                    result["ok"] = False
                    result["errors"].append(f"Longueur invalide: {pipe_id}")
                if getattr(p, 'diameter', 0.0) <= 0:
                    result["ok"] = False
                    result["errors"].append(f"Diamètre invalide: {pipe_id}")
            if not result["ok"]:
                return result
            sim = wntr.sim.EpanetSimulator(wn)  # type: ignore
            res = sim.run_sim()
            press_df = res.node['pressure'] if isinstance(res.node, dict) else getattr(res.node, 'pressure', None)
            if press_df is not None:
                try:
                    last_row = press_df.iloc[-1]
                    vals = list(last_row.to_dict().values())
                    bad = [v for v in vals if v is None or v != v]
                    if bad:
                        result["ok"] = False
                        result["errors"].append("Pressions NaN/None détectées")
                    else:
                        result["simulator_info"] = {
                            "n_nodes": int(len(vals)),
                            "min_pressure": float(min(vals)) if vals else 0.0,
                            "max_pressure": float(max(vals)) if vals else 0.0,
                        }
                except Exception:
                    pass
    except Exception as e:
        result["ok"] = False
        result["errors"].append(f"Lecture/Simulation échouée: {e}")
    return result


