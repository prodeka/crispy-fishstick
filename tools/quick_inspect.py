import json
import sys
from typing import Any, Dict, List, Union


def _to_float(value: Any) -> float:
    try:
        if isinstance(value, dict):
            # common shapes: {"value": x}, or {"flow": x}
            for key in ("value", "flow", "q", "v"):
                if key in value:
                    return float(value[key] or 0.0)
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def sum_flows(flows: Any) -> Union[float, None]:
    # flows can be dict{name->value}, list of numbers, list of dicts, or None
    if flows is None:
        return None
    if isinstance(flows, dict):
        try:
            return sum(_to_float(v) for v in flows.values())
        except Exception:
            return sum(_to_float(v) for v in flows.values())
    if isinstance(flows, list):
        return sum(_to_float(v) for v in flows)
    # unknown shape
    return None


def collect_diameters_mm(props: List[Dict[str, Any]]) -> List[Union[int, float]]:
    diameters: List[Union[int, float]] = []
    for p in props or []:
        dd = p.get("diameters_mm")
        if dd is None:
            continue
        if isinstance(dd, dict):
            diameters.extend([_to_float(v) for v in dd.values()])
        elif isinstance(dd, list):
            diameters.extend([_to_float(v) for v in dd])
    return diameters


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python tools/quick_inspect.py <results.json>")
        return 2
    path = sys.argv[1]
    d = json.load(open(path, encoding="utf-8"))

    meta: Dict[str, Any] = d.get("meta", {})
    props: List[Dict[str, Any]] = d.get("proposals", []) or []

    print("meta.best_cost:", meta.get("best_cost"))
    print("simulator:", meta.get("simulator_used") or meta.get("simulator"))
    print("solver_calls:", meta.get("solver_calls"))
    print("sim_time_s_total:", meta.get("sim_time_seconds_total"))

    hyd: Dict[str, Any] = d.get("hydraulics", {}) or {}
    flows = hyd.get("flows_m3_s")
    if flows is None:
        flows = hyd.get("flows")
    total = sum_flows(flows)
    print("total_flow:", total)

    ds = collect_diameters_mm(props)
    uniq = sorted({int(x) if float(x).is_integer() else float(x) for x in ds}) if ds else []
    print("Diameters count:", len(ds), "unique:", uniq)

    # quick cross-check on best proposal
    best = props[0] if props else {}
    print("best.CAPEX:", best.get("CAPEX"))
    print("best.constraints_ok:", best.get("constraints_ok"))

    pinfo = meta.get("price_db_info") or {}
    print("price_db.type:", pinfo.get("type"))
    print("price_db.source:", pinfo.get("source"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


