import json
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python tools/check_opt_meta.py <path_to_output.json> [--no-surrogate]")
        return 2
    path = sys.argv[1]
    try:
        data = json.load(open(path, "r", encoding="utf-8"))
    except Exception as e:
        print(f"ERREUR: impossible de lire {path}: {e}")
        return 2
    m = data.get("meta", {}) or {}
    errs = []
    if float(m.get("solver_calls", 0) or 0) <= 0:
        errs.append("solver_calls <= 0 (vérifier cache / bypass)")
    if float(m.get("sim_time_seconds_total", 0) or 0) <= 0:
        errs.append("sim_time_seconds_total <= 0 (pas de simulations réelles détectées)")
    if float(m.get("duration_seconds", 0) or 0) <= 0:
        errs.append("duration_seconds <= 0 (run non mesuré)")
    if "--no-surrogate" in sys.argv and bool(m.get("surrogate_used", False)):
        errs.append("surrogate_used true malgré --no-surrogate")
    if errs:
        print("ERREURS:\n" + "\n".join(errs))
        return 1
    print("META OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


