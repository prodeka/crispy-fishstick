# tools/diagnose_results.py
import json
import sys
from pathlib import Path
from statistics import mean

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def fmt(n):
    try:
        return f"{float(n):,.3f}"
    except Exception:
        return str(n)

def main(p):
    p = Path(p)
    if not p.exists():
        print(f"Fichier introuvable: {p}")
        return 2
    data = load(p)
    meta = data.get("meta", {})
    props = data.get("proposals", []) or []
    hydraulics = data.get("hydraulics", {}) or {}
    metrics = data.get("metrics", {}) or {}

    print("=== Résumé quick-check ===")
    print("meta.best_cost:", meta.get("best_cost"))
    if props:
        print("proposals[0].CAPEX:", props[0].get("CAPEX"))
    print("meta.solver_calls:", meta.get("solver_calls"))
    print("meta.sim_time_seconds_total:", meta.get("sim_time_seconds_total"))
    print("meta.duration_seconds:", meta.get("duration_seconds"))

    # Best consistency
    best_meta = meta.get("best_cost")
    best_prop = (props[0].get("CAPEX") if props else None)
    if best_meta is None and best_prop is None:
        print("WARNING: Aucun best trouvé (meta/proposals).")
    elif best_meta is None and best_prop is not None:
        print("NOTE: meta.best_cost absent, fallback proposals[0].CAPEX =", best_prop)
    elif best_prop is None and best_meta is not None:
        print("NOTE: proposals vide mais meta.best_cost present =", best_meta)
    else:
        if float(best_meta) != float(best_prop):
            print("ERROR: mismatch best_cost: meta != proposals[0]")
            print("  meta.best_cost =", best_meta)
            print("  proposals[0].CAPEX =", best_prop)
        else:
            print("OK: best_cost cohérent.")

    # Flow conservation
    flows = hydraulics.get("flows_m3_s") or hydraulics.get("flows") or {}
    total_flow = 0.0
    try:
        if isinstance(flows, dict):
            total_flow = sum(float(v or 0.0) for v in flows.values())
        elif isinstance(flows, list):
            total_flow = sum(float(x.get("value", 0)) for x in flows)
    except Exception:
        pass
    print("Total flow (sum over links):", total_flow)
    if abs(total_flow) > 1e-3:
        print("WARNING: Flow conservation breach (abs(total) > 1e-3)")

    # Diameters uniformity
    diam_map = {}
    if props:
        diam_map = props[0].get("diameters_mm", {}) or {}
    unique_diams = set(diam_map.values()) if diam_map else set()
    print("Diameters: count_links =", len(diam_map), "unique =", sorted(unique_diams)[:10])
    if len(unique_diams) == 1 and len(diam_map) > 5:
        print("WARNING: All diameters identical -> check PriceDB or repair logic")

    # Constraints vs metrics
    violations = []
    for i, p in enumerate(props):
        ok = bool(p.get("constraints_ok", True))
        m = p.get("metrics", {}) or {}
        min_p = m.get("min_pressure_m") or p.get("min_pressure_m")
        max_v = m.get("max_velocity_m_s") or p.get("max_velocity_m_s")
        # if constraints defined in meta, show them
        if meta.get("constraints"):
            try:
                req_p = float(meta["constraints"].get("pressure_min_m", float('nan')))
                req_vmax = float(meta["constraints"].get("velocity_max_m_s", float('nan')))
            except Exception:
                req_p = req_vmax = None
        else:
            req_p = req_vmax = None
        if req_p and min_p is not None and float(min_p) < req_p:
            violations.append((i, "pressure", min_p, req_p))
        if req_vmax and max_v is not None and float(max_v) > req_vmax:
            violations.append((i, "velocity", max_v, req_vmax))
        if not ok:
            print(f"Proposal[{i}] constraints_ok = False (min_p={min_p}, max_v={max_v})")
    if violations:
        print("Found constraint violations (index, type, observed, required):")
        for v in violations:
            print(" ", v)

    # Simulation stats quick sanity
    print("\n--- Simulation stats ---")
    print("simulator:", meta.get("simulator_used") or hydraulics.get("simulator"))
    print("sim_time_seconds_total:", meta.get("sim_time_seconds_total") or metrics.get("sim_time_seconds"))
    print("solver_calls:", meta.get("solver_calls"))
    # PDF backend
    print("\n--- Export / PDF ---")
    print("pdf_backend:", meta.get("pdf_backend") or meta.get("report_backend"))
    print("pdf_status_message:", meta.get("pdf_status_message"))
    # final
    print("\n=== End quick-check ===")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: diagnose_results.py <result.json>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
