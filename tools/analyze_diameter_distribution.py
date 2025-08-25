import re
from pathlib import Path
from collections import Counter

LOGS = Path("test_validation/logs")

RE_GA = re.compile(r"send \d+ diams \| sample=\[(?P<sample>.*)\]")
RE_PAIR = re.compile(r"\('(?P<id>[^']+)',\s*(?P<d>\d+)\)")
RE_EP_SET = re.compile(r"set_diam: link=(?P<id>[^\s]+) req_mm=(?P<mm>\d+)")


def parse_ga(path: Path) -> Counter:
    c = Counter()
    if not path.exists():
        return c
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = RE_GA.search(line)
        if not m:
            continue
        sample = m.group("sample")
        for p in RE_PAIR.finditer(sample):
            d = int(p.group("d"))
            c[d] += 1
    return c


def parse_epanet(path: Path) -> Counter:
    c = Counter()
    if not path.exists():
        return c
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = RE_EP_SET.search(line)
        if m:
            c[int(m.group("mm"))] += 1
    return c


def main():
    ga = parse_ga(LOGS / "ga_to_solver_debug.log")
    ep = parse_epanet(LOGS / "epanet_mapping_debug.log")
    print("GA diameter frequencies (sampled):")
    for d, n in ga.most_common(10):
        print(f"  {d} mm: {n}")
    print("\nEPANET diameter frequencies (applied, sampled):")
    for d, n in ep.most_common(10):
        print(f"  {d} mm: {n}")


if __name__ == "__main__":
    main()


