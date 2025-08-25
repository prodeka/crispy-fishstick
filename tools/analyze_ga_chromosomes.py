import re
import sys
from pathlib import Path
from collections import defaultdict


LOG_DEFAULT = Path("test_validation/logs/ga_chromosomes.log")

LINE_RE = re.compile(
    r"generation=(?P<gen>\d+)\s+ind=(?P<ind>\d+)\s+genes=(?P<genes>\d+)\s+invalid_indices=(?P<inv>\d+)" 
)


def analyze_log(path: Path, top_k: int = 10):
    total = 0
    invalid = 0
    per_gen_total = defaultdict(int)
    per_gen_invalid = defaultdict(int)

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = LINE_RE.search(line)
            if not m:
                continue
            gen = int(m.group("gen"))
            inv = int(m.group("inv"))
            total += 1
            per_gen_total[gen] += 1
            if inv > 0:
                invalid += 1
                per_gen_invalid[gen] += 1

    ratio = (invalid / total * 100.0) if total else 0.0
    # Sort generations by invalid count desc, then by gen id
    gen_stats = [
        (gen, per_gen_invalid.get(gen, 0), per_gen_total.get(gen, 0))
        for gen in sorted(per_gen_total.keys())
    ]
    top_gens = sorted(gen_stats, key=lambda x: (-x[1], x[0]))[:top_k]

    return {
        "total": total,
        "invalid": invalid,
        "ratio_pct": ratio,
        "top_generations": top_gens,
    }


def main():
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_DEFAULT
    if not log_path.exists():
        print(f"Log introuvable: {log_path}")
        sys.exit(1)
    res = analyze_log(log_path)
    print(f"Fichier: {log_path}")
    print(f"Lignes analysées: {res['total']}")
    print(f"Lignes avec invalid_indices>0: {res['invalid']}")
    print(f"Ratio: {res['ratio_pct']:.2f}%")
    print("Generations les plus touchées (gen, invalid, total):")
    for gen, inv, tot in res["top_generations"]:
        pct = (inv / tot * 100.0) if tot else 0.0
        print(f"  gen={gen}: invalid={inv}/{tot} ({pct:.2f}%)")


if __name__ == "__main__":
    main()


