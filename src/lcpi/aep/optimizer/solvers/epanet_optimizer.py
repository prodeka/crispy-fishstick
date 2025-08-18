from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from ..io import NetworkModel, convert_to_solver_network_data
from ...core.solvers.factory import SolverFactory
import tempfile


class EPANETOptimizer:
    """Wrapper EPANET pour optimisation (Jalon 2 - version minimale).

    Utilise la factory existante pour obtenir un solveur EPANET et exécuter
    des simulations à partir d'un modèle réseau et d'une hauteur de réservoir.
    """

    def __init__(self):
        self.solver = SolverFactory.get_solver("epanet")

    def simulate_with_tank_height(
        self,
        network_model: NetworkModel,
        H_tank: float,
        diameters: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        # Convertir NetworkModel -> format EPANET solver (noeuds/conduites)
        network_dict = convert_to_solver_network_data(network_model, H_tank, diameters)
        # Générer un .inp via le solveur EPANET, puis exécuter la simulation
        try:
            inp_path = self.solver.generate_inp_file(network_dict)
            # Optionnel: ajuster précisément [TANKS]/[PIPES] si diameters fournis
            tweaked_path = self._tweak_inp_file(inp_path, H_tank, diameters or {})
            result = self.solver.run_epanet_simulation(tweaked_path)
            return result
        except AttributeError:
            # Fallback si les méthodes n'existent pas: exécuter run_simulation
            return self.solver.run_simulation(network_dict)

    def _tweak_inp_file(self, inp_path: str, H_tank: float, diameters: Dict[str, int]) -> str:
        """Ajuste le fichier .inp généré pour refléter H_tank et DN.

        - Met à jour la colonne Diameter dans [PIPES] pour les IDs présents
        - Met à jour InitLevel (ou Level) dans [TANKS] pour refléter H_tank relatif
        """
        try:
            original = Path(inp_path).read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            return inp_path

        out_lines: list[str] = []
        section = None
        for line in original:
            raw = line.rstrip("\n")
            stripped = raw.strip()
            if not stripped or stripped.startswith(";"):
                out_lines.append(raw)
                continue
            if stripped.startswith("[") and stripped.endswith("]"):
                section = stripped.upper()
                out_lines.append(raw)
                continue
            if section == "[PIPES]":
                parts = stripped.split()
                if len(parts) >= 5:
                    pid = parts[0]
                    if pid in diameters:
                        # Diameter (5th token) in mm -> EPANET expects mm or inch? We assume mm here
                        parts[4] = str(diameters[pid])
                        raw = ("\t").join(parts)
                out_lines.append(raw)
                continue
            if section == "[TANKS]":
                parts = stripped.split()
                if len(parts) >= 6:
                    # EPANET TANKS columns: ID Elevation InitLevel MinLevel MaxLevel Diameter ...
                    try:
                        elevation = float(parts[1])
                        init_level = max(0.0, float(H_tank) - elevation)
                        parts[2] = f"{init_level:.3f}"
                        raw = ("\t").join(parts)
                    except Exception:
                        pass
                out_lines.append(raw)
                continue
            out_lines.append(raw)

        tmp = tempfile.NamedTemporaryFile(suffix=".inp", delete=False)
        tmp.close()
        Path(tmp.name).write_text("\n".join(out_lines), encoding="utf-8")
        return tmp.name


