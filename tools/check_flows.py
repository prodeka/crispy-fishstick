#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_flows.py
------------
Vérifie la conservation des débits d'un fichier INP via WNTR/EpanetSimulator,
exporte CSV/JSON, trace l'évolution temporelle de sum(flows) et génère un petit rapport MD.

Usage:
    python tools/check_flows.py <network.inp> [--simulator {epanet,wntr}] [--outdir results] [--show]
    python tools/check_flows.py net.inp --simulator wntr --outdir results --links "P1,P2" --sample 10 --save-plot

Dépendances:
    pip install wntr pandas matplotlib numpy
    (Si vous voulez utiliser EPANET via WNTR, installez EPANET/wntr comme d'habitude)
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import logging
import math

try:
    import wntr
except Exception as e:
    wntr = None

try:
    import pandas as pd
except Exception:
    pd = None

try:
    import numpy as np
except Exception:
    np = None

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

logger = logging.getLogger("check_flows")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def run_simulation(inp_path: Path, simulator: str = "epanet"):
    if wntr is None:
        raise RuntimeError("La librairie wntr n'est pas installée (pip install wntr).")
    wn = wntr.network.WaterNetworkModel(str(inp_path))
    if simulator == "wntr":
        sim = wntr.sim.WNTRSimulator(wn)
        logger.info("Using WNTRSimulator")
    else:
        # try EpanetSimulator first (via wntr) and fallback to WNTRSimulator
        SimClass = getattr(wntr.sim, "EpanetSimulator", None) or getattr(wntr.sim, "EPANETSimulator", None)
        if SimClass is None:
            logger.warning("EpanetSimulator not available in wntr; falling back to WNTRSimulator")
            sim = wntr.sim.WNTRSimulator(wn)
        else:
            logger.info("Using EpanetSimulator (via WNTR)")
            sim = SimClass(wn)
    results = sim.run_sim()
    return wn, results


def compute_sum_flows(results, selected_links: list | None = None):
    # results.link["flowrate"] is a DataFrame indexed by timestamps with one column per link
    flows_df = results.link.get("flowrate")
    if flows_df is None:
        raise RuntimeError("No flowrate results in simulation output.")
    # Keep only selected links if provided
    if selected_links:
        missing = [l for l in selected_links if l not in flows_df.columns]
        if missing:
            logger.warning(f"Some requested links not present in results: {missing}")
        cols = [c for c in selected_links if c in flows_df.columns]
        if not cols:
            raise RuntimeError("No valid links selected.")
        flows_df = flows_df[cols]
    # Sum signed flows per time step (conservation check)
    total_signed = flows_df.sum(axis=1)  # signed sum
    # Also compute absolute sum magnitude
    total_abs = flows_df.abs().sum(axis=1)
    return flows_df, total_signed, total_abs


def summarize_flows(flows_df, total_signed):
    stats = {}
    stats["n_timesteps"] = int(len(total_signed))
    stats["mean_total_signed"] = float(total_signed.mean())
    stats["max_total_signed"] = float(total_signed.max())
    stats["min_total_signed"] = float(total_signed.min())
    stats["std_total_signed"] = float(total_signed.std())
    # per-link stats
    link_stats = []
    for col in flows_df.columns:
        s = flows_df[col]
        link_stats.append({
            "link": col,
            "min": float(s.min()),
            "max": float(s.max()),
            "mean": float(s.mean()),
            "abs_mean": float(s.abs().mean()),
            "pct_negative": float((s < 0).sum()) / max(1, len(s)) * 100.0,
        })
    stats["link_count"] = int(len(link_stats))
    return stats, link_stats


def save_outputs(inp_path: Path, sim_name: str, total_signed, total_abs, flows_df, stats, link_stats, outdir: Path, write_full_series: bool = True):
    outdir.mkdir(parents=True, exist_ok=True)
    stem = inp_path.stem
    csv_file = outdir / f"{stem}_sumflows_{sim_name}.csv"
    json_file = outdir / f"{stem}_sumflows_{sim_name}.json"

    # CSV: time, sum_signed, sum_abs
    df_out = pd.DataFrame({
        "time": list(map(lambda t: float(t.total_seconds()) if hasattr(t, "total_seconds") else float(t), total_signed.index)),
        "sum_signed_m3s": total_signed.values,
        "sum_abs_m3s": total_abs.values
    })
    df_out.to_csv(csv_file, index=False)

    # JSON: metadata + series (optional)
    json_payload = {
        "inp_file": str(inp_path),
        "simulator": sim_name,
        "statistics": stats,
        "link_stats_sample": link_stats[:50]  # don't dump too many by default
    }
    if write_full_series:
        json_payload["series"] = df_out.to_dict(orient="records")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2, ensure_ascii=False)

    logger.info(f"CSV écrit: {csv_file}")
    logger.info(f"JSON écrit: {json_file}")
    return csv_file, json_file


def plot_sum_flows(total_signed, total_abs, outdir: Path, stem: str, sample_rate: int = 1, save_png: bool = True, show_plot: bool = False):
    if plt is None or np is None:
        logger.warning("Matplotlib ou numpy non installé. Ignorer le tracé.")
        return None
    # Downsample for plotting if sample_rate > 1
    if sample_rate > 1:
        ts = total_signed.iloc[::sample_rate]
        ta = total_abs.iloc[::sample_rate]
    else:
        ts = total_signed
        ta = total_abs

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(ts.index.total_seconds() if hasattr(ts.index[0], "total_seconds") else ts.index, ts.values, label="sum_signed (m³/s)")
    ax.plot(ta.index.total_seconds() if hasattr(ta.index[0], "total_seconds") else ta.index, ta.values, label="sum_abs (m³/s)", alpha=0.6)
    ax.axhline(0.0, color="k", linestyle="--", linewidth=0.7)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Flow (m³/s)")
    ax.set_title(f"Sum(flows) - {stem}")
    ax.legend(loc="best")
    ax.grid(True, linestyle=":", linewidth=0.6)
    plt.tight_layout()

    png_file = outdir / f"{stem}_sumflows_plot.png"
    if save_png:
        fig.savefig(png_file, dpi=150)
        logger.info(f"Plot sauvegardé: {png_file}")
    if show_plot:
        plt.show()
    plt.close(fig)
    return png_file


def generate_markdown_report(outdir: Path, stem: str, stats: dict, flow_warning: bool, csv_file: Path, json_file: Path, png_file: Path | None):
    md_file = outdir / f"{stem}_sumflows_report.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# Rapport conservation des débits - {stem}\n\n")
        f.write("## Résumé statistique\n\n")
        f.write("| Clé | Valeur |\n")
        f.write("|---|---|\n")
        for k, v in stats.items():
            if k == "link_count":
                f.write(f"| {k} | {v} |\n")
            elif isinstance(v, (int, float)):
                f.write(f"| {k} | {v:.6f} |\n")
            else:
                f.write(f"| {k} | {v} |\n")
        f.write("\n")
        f.write(f"- CSV: `{csv_file.name}`\n")
        f.write(f"- JSON: `{json_file.name}`\n")
        if png_file:
            f.write(f"- Plot: `{png_file.name}`\n")
        f.write("\n")
        if flow_warning:
            f.write("> **⚠️ Alerte**: conservation des débits violée (|sum| > epsilon). Vérifiez les orientations / demandes dynamiques / valves.\n")
    logger.info(f"Rapport Markdown écrit: {md_file}")
    return md_file


def parse_args():
    p = argparse.ArgumentParser(description="Check flow conservation with WNTR/EPANET and export CSV/JSON + plot")
    p.add_argument("inp", help="Chemin vers le fichier .inp")
    p.add_argument("--simulator", choices=("epanet", "wntr"), default="epanet", help="Backend simulator (default: epanet via WNTR)")
    p.add_argument("--outdir", default=None, help="Dossier de sortie (default: <inp>/results)")
    p.add_argument("--links", default=None, help="Liste CSV des link IDs à inclure (par défaut toutes les conduites)")
    p.add_argument("--sample", type=int, default=1, help="Downsample factor for plot (1=no downsample)")
    p.add_argument("--epsilon", type=float, default=1e-3, help="Threshold for flow conservation breach (m3/s)")
    p.add_argument("--show", action="store_true", help="Montrer le plot à l'écran (plt.show())")
    p.add_argument("--save-plot", action="store_true", help="Sauvegarder le plot en PNG")
    p.add_argument("--no-json-series", action="store_true", help="Ne pas écrire la série complète dans le JSON (allège la taille)")
    return p.parse_args()


def main():
    args = parse_args()
    inp = Path(args.inp)
    if not inp.exists():
        logger.error("Fichier INP introuvable: %s", inp)
        sys.exit(2)
    outdir = Path(args.outdir) if args.outdir else inp.resolve().parent / "results"
    links = None
    if args.links:
        links = [s.strip() for s in args.links.split(",") if s.strip()]

    try:
        wn, results = run_simulation(inp, simulator=args.simulator)
    except Exception as e:
        logger.error("Erreur simulation: %s", e)
        sys.exit(3)

    try:
        flows_df, total_signed, total_abs = compute_sum_flows(results, selected_links=links)
    except Exception as e:
        logger.error("Erreur calcul flows: %s", e)
        sys.exit(4)

    stats, link_stats = summarize_flows(flows_df, total_signed)

    # flow conservation check (signed sum near zero)
    mean_abs = abs(stats["mean_total_signed"])
    flow_warning = abs(stats["mean_total_signed"]) > args.epsilon or abs(stats["max_total_signed"]) > 1.0
    if flow_warning:
        logger.warning("FLOW_CONSERVATION_BREACH: total flow not ~0 (mean=%g)", stats["mean_total_signed"])

    csv_file, json_file = save_outputs(inp, args.simulator, total_signed, total_abs, flows_df, stats, link_stats, outdir, write_full_series=not args.no_json_series)

    png_file = None
    if args.save_plot or args.show:
        png_file = plot_sum_flows(total_signed, total_abs, outdir, inp.stem, sample_rate=max(1, args.sample), save_png=args.save_plot, show_plot=args.show)

    md_file = generate_markdown_report(outdir, inp.stem, stats, flow_warning, csv_file, json_file, png_file)

    logger.info("Terminé. Résultats dans %s", outdir.resolve())


if __name__ == "__main__":
    main()
