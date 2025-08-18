from __future__ import annotations

from typing import List, Dict, Tuple


def compute_pareto(points: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """Retourne les points non-dominés (minimisation CAPEX et OPEX)."""
    pareto: List[Dict[str, float]] = []
    for p in points:
        dominated = False
        for q in points:
            if q is p:
                continue
            if (q.get("CAPEX", float("inf")) <= p.get("CAPEX", float("inf")) and
                q.get("OPEX", float("inf")) <= p.get("OPEX", float("inf")) and
                (q.get("CAPEX") < p.get("CAPEX") or q.get("OPEX") < p.get("OPEX"))):
                dominated = True
                break
        if not dominated:
            pareto.append(p)
    return pareto


def knee_point(pareto: List[Dict[str, float]]) -> Dict[str, float] | None:
    """Sélectionne un knee-point approximatif (plus grande distance à la ligne extrêmes)."""
    if not pareto:
        return None
    pts = sorted(pareto, key=lambda d: d["CAPEX"])  # croissant CAPEX
    min_c, min_o = min(d["CAPEX"] for d in pts), min(d["OPEX"] for d in pts)
    max_c, max_o = max(d["CAPEX"] for d in pts), max(d["OPEX"] for d in pts)
    if max_c == min_c or max_o == min_o:
        return pts[0]
    # normaliser et mesurer distance à la ligne reliant extrêmes
    import math
    A = (0.0, 0.0)
    B = (1.0, 1.0)
    def norm(p: Dict[str, float]) -> Tuple[float, float]:
        return (
            (p["CAPEX"] - min_c) / (max_c - min_c),
            (p["OPEX"] - min_o) / (max_o - min_o),
        )
    def dist_to_line(pt: Tuple[float, float]) -> float:
        x0, y0 = pt
        # distance point->ligne AB (A=(0,0), B=(1,1))
        return abs((B[1]-A[1])*x0 - (B[0]-A[0])*y0) / (2**0.5)
    best = max(pts, key=lambda d: dist_to_line(norm(d)))
    return best


