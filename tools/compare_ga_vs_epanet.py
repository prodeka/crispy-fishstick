import re
from pathlib import Path
from typing import List, Dict, Tuple


LOGS_DIR = Path("test_validation/logs")
GA_LOG = LOGS_DIR / "ga_chromosomes.log"
EPANET_LOG = LOGS_DIR / "epanet_sim_debug.log"

# Formats attendus dans les logs (simples, sans constructions conditionnelles PCRE)
RE_PIPE_IDS = re.compile(r"^\s*pipe_ids\[(?P<idx>\d+)\]=(.*?)(?P<id>[^\s]+)\s*$")
RE_GA_SAMPLE = re.compile(r"^\s*pipe\[(?P<id>[^\]]+)\]: idx=(?P<idx>-?\d+) diam=(?P<diam>\d+)mm\s*$")
RE_EPANET_DIAM = re.compile(r"^\s*diam\[(?P<id>[^\]]+)\]=(.*?)(?P<diam>\d+)\s*$")


def parse_ga_samples(path: Path) -> Tuple[List[str], Dict[str, int]]:
    pipe_ids_sample: List[str] = []
    ga_diams: Dict[str, int] = {}
    if not path.exists():
        return pipe_ids_sample, ga_diams
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        in_pid_block = False
        for line in f:
            s = line.strip()
            if s.startswith("pipe_ids_sample:"):
                in_pid_block = True
                continue
            # collect from declared block
            if in_pid_block:
                m = RE_PIPE_IDS.match(line)
                if m:
                    pipe_ids_sample.append(m.group("id").strip())
                    continue
                else:
                    in_pid_block = False
            # also collect any pipe_ids[...] line globally (fallback)
            m_any = RE_PIPE_IDS.match(line)
            if m_any and len(pipe_ids_sample) < 10:
                pipe_ids_sample.append(m_any.group("id").strip())
            # collect GA diam sample lines
            m2 = RE_GA_SAMPLE.match(line)
            if m2 and len(ga_diams) < 20:
                pid = m2.group("id").strip()
                ga_diams[pid] = int(m2.group("diam"))
    # truncate pipe_ids_sample to at most 10
    pipe_ids_sample = pipe_ids_sample[:10]
    return pipe_ids_sample, ga_diams


def parse_epanet_samples(path: Path) -> Dict[str, int]:
    ep_diams: Dict[str, int] = {}
    if not path.exists():
        return ep_diams
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = RE_EPANET_DIAM.match(line)
            if m:
                ep_diams[m.group("id").strip()] = int(m.group("diam"))
    return ep_diams


def read_controller_info() -> Dict[str, object]:
    info = {}
    f = LOGS_DIR / "pipe_ids_controller.json"
    if f.exists():
        try:
            import json
            data = json.loads(f.read_text(encoding="utf-8"))
            info["controller_count"] = int(data.get("count", 0))
            smp = data.get("sample", [])
            info["controller_sample"] = list(smp[:10])
        except Exception:
            pass
    return info


def parse_ga_pipe_ids_received_len(path: Path) -> int:
    if not path.exists():
        return -1
    last_len = -1
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.endswith("pipe_ids_received_len=0"):
                last_len = 0
            elif "pipe_ids_received_len=" in line:
                try:
                    val = int(line.split("pipe_ids_received_len=")[-1].split()[0])
                    last_len = val
                except Exception:
                    continue
    return last_len


def find_latest(pattern: str) -> Path | None:
    if not LOGS_DIR.exists():
        return None
    cands = sorted(LOGS_DIR.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0] if cands else None


def compare():
    # Auto-détecter les logs par-processus récents si disponibles
    ga_log_path = find_latest("ga_chromosomes_*.log") or GA_LOG
    ep_log_path = find_latest("epanet_sim_debug_*.log") or EPANET_LOG
    print(f"Using GA log: {ga_log_path}")
    print(f"Using EPANET log: {ep_log_path}")

    pipe_ids_sample, ga_diams = parse_ga_samples(ga_log_path)
    ep_diams = parse_epanet_samples(ep_log_path)
    # Controller info
    ctrl = read_controller_info()
    if ctrl:
        print(f"Controller pipe_ids: count={ctrl.get('controller_count')} sample={ctrl.get('controller_sample')}")
    # GA received len
    recv_len = parse_ga_pipe_ids_received_len(ga_log_path)
    if recv_len >= 0:
        print(f"GA pipe_ids_received_len: {recv_len}")
    print(f"GA pipe_ids_sample count: {len(pipe_ids_sample)}")
    print(f"GA sample diam count: {len(ga_diams)}  | EPANET diam entries: {len(ep_diams)}")
    if not pipe_ids_sample:
        print("No pipe_ids_sample found in GA log. Run GA again to populate.")
        return 1
    # Compare only over sampled IDs that appear in EPANET log
    checked = 0
    mismatches = []
    missing_in_epanet = []
    for pid in pipe_ids_sample:
        if pid in ep_diams and pid in ga_diams:
            checked += 1
            if ep_diams[pid] != ga_diams[pid]:
                mismatches.append((pid, ga_diams[pid], ep_diams[pid]))
        else:
            if pid not in ep_diams:
                missing_in_epanet.append(pid)
    print(f"Checked IDs: {checked}")
    if mismatches:
        print("MISMATCHES (pipe_id, ga_diam, epanet_diam):")
        for pid, gd, ed in mismatches[:20]:
            print(f"  {pid}: GA={gd} EPANET={ed}")
    else:
        print("No mismatches on the sampled IDs found in both logs.")
    if missing_in_epanet:
        print(f"IDs missing in EPANET log: {len(missing_in_epanet)} (showing up to 20)")
        for pid in missing_in_epanet[:20]:
            print(f"  {pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(compare())


