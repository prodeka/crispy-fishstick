# src/lcpi/aep/utils/flows_inspector.py
from __future__ import annotations
from pathlib import Path
from collections import deque
import json
import logging
import time
from typing import Optional, Dict, Any, Iterable

logger = logging.getLogger(__name__)

# lazy imports to avoid heavy deps if unused
def _import_pandas():
    try:
        import pandas as pd
        return pd
    except Exception:
        raise RuntimeError("pandas is required for flows_inspector (pip install pandas)")

def _import_wntr():
    try:
        import wntr
        return wntr
    except Exception:
        return None

def _import_matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except Exception:
        return None

def _times_to_seconds(index):
    # WNTR timestamps are pandas Timedelta or datetime; convert to seconds
    try:
        import pandas as pd
    except Exception:
        return [float(i) for i in index]
    # if TimedeltaIndex or DatetimeIndex -> convert to seconds from start
    try:
        if isinstance(index, pd.TimedeltaIndex):
            return [float(t.total_seconds()) for t in index]
        if isinstance(index, pd.DatetimeIndex):
            base = index[0]
            return [(t - base).total_seconds() for t in index]
    except Exception:
        pass
    # fallback
    return [float(i) for i in index]

# --- core analyzer (offline) ---
def analyze_and_dump(flows_df, outdir: Path, stem: str, sim_name: str, save_plot: bool=True, write_json_series: bool=True):
    """
    flows_df: pandas.DataFrame indexed by time with columns per link (m3/s signed)
    """
    pd = _import_pandas()
    outdir.mkdir(parents=True, exist_ok=True)
    # total signed and abs
    total_signed = flows_df.sum(axis=1)
    total_abs = flows_df.abs().sum(axis=1)

    # CSV
    csv_path = outdir / f"{stem}_sumflows_{sim_name}.csv"
    df_out = pd.DataFrame({
        "time_s": _times_to_seconds(total_signed.index),
        "sum_signed_m3s": total_signed.values,
        "sum_abs_m3s": total_abs.values,
    })
    df_out.to_csv(csv_path, index=False)

    # JSON
    json_path = outdir / f"{stem}_sumflows_{sim_name}.json"
    stats = {
        "n_timesteps": int(len(total_signed)),
        "mean_total_signed": float(total_signed.mean()),
        "max_total_signed": float(total_signed.max()),
        "min_total_signed": float(total_signed.min()),
        "std_total_signed": float(total_signed.std()),
        "link_count": int(len(flows_df.columns))
    }
    payload = {"simulator": sim_name, "inp_stem": stem, "statistics": stats}
    if write_json_series:
        payload["series"] = df_out.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # plot
    png_path = None
    plt = _import_matplotlib()
    if plt is not None and save_plot:
        try:
            fig, ax = plt.subplots(figsize=(9,3))
            t_sec = _times_to_seconds(total_signed.index)
            ax.plot(t_sec, total_signed.values, label="sum_signed")
            ax.plot(t_sec, total_abs.values, label="sum_abs", alpha=0.6)
            ax.axhline(0.0, color="k", linestyle="--", linewidth=0.6)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Flow (m³/s)")
            ax.set_title(f"sum(flows) - {stem}")
            ax.legend()
            ax.grid(True, linestyle=":", linewidth=0.5)
            plt.tight_layout()
            png_path = outdir / f"{stem}_sumflows_{sim_name}.png"
            fig.savefig(str(png_path), dpi=150)
            plt.close(fig)
            logger.info("flows_inspector: saved plot %s", png_path)
        except Exception as e:
            logger.exception("flows_inspector: plot failed: %s", e)
    else:
        logger.debug("flows_inspector: matplotlib not available -> skip plot")

    logger.info("flows_inspector: CSV %s JSON %s", csv_path, json_path)
    return {"csv": str(csv_path), "json": str(json_path), "png": str(png_path) if png_path else None, "statistics": stats}

# --- flexible inspector wrapper to accept various simulation outputs ---
def inspect_simulation_result(sim_out: Any, outdir: Path, stem: str = "network", sim_name: str = "sim", save_plot: bool = True, write_json_series: bool = True):
    """
    Acceptable sim_out:
      - wntr.sim.results.WNTRSimulatorResults object (typical wntr.run_sim)
      - dict with key 'flow_df' (pandas DataFrame) or 'flow_series' list or 'flows_time_series'
      - dict with 'flows_m3_s' mapping link->value (single snapshot) -> produce single-row CSV/JSON
    """
    pd = _import_pandas()
    # Case 1: WNTR results
    wntr = _import_wntr()
    if wntr is not None and sim_out is not None and getattr(sim_out, "link", None) is not None:
        try:
            flows_df = sim_out.link.get("flowrate")
            if flows_df is None:
                raise RuntimeError("WNTR results contains no link.flowrate")
            return analyze_and_dump(flows_df, outdir, stem, sim_name, save_plot=save_plot, write_json_series=write_json_series)
        except Exception as e:
            logger.debug("inspect_simulation_result: not wntr-like: %s", e)
    # Case 2: sim_out is dict containing 'flow_df' or 'flow_series'
    if isinstance(sim_out, dict):
        if "flow_df" in sim_out:
            flows_df = sim_out["flow_df"]
            return analyze_and_dump(flows_df, outdir, stem, sim_name, save_plot=save_plot, write_json_series=write_json_series)
        if "flow_series" in sim_out:
            # flow_series expected: list of { "time": t, "flows": {link:val,...} }
            rows = []
            for rec in sim_out["flow_series"]:
                t = rec.get("time", None)
                flows = rec.get("flows", {})
                row = {"time_s": float(t) if t is not None else None}
                row.update(flows)
                rows.append(row)
            df = pd.DataFrame(rows).set_index("time_s")
            return analyze_and_dump(df, outdir, stem, sim_name, save_plot=save_plot, write_json_series=write_json_series)
        if "flows_m3_s" in sim_out:
            # Single snapshot -> create 1-row dataframe
            flows = sim_out["flows_m3_s"]
            df = pd.DataFrame([flows])
            df.index = pd.Index([0.0])
            return analyze_and_dump(df, outdir, stem, sim_name, save_plot=save_plot, write_json_series=write_json_series)
    raise RuntimeError("Unsupported simulation output format for inspect_simulation_result")

# --- Event consumer for live plotting ---
class FlowEventConsumer:
    """
    Consumer that accepts progress events and builds a time series of total flow.
    - The simulate method must emit events with evt='simulation' and data containing either:
        - 'flows': dict link->value  (snapshot)
        - or 'total_flow': float (signed sum) OR
        - 'time_s': float to set explicit time
    - On finalize call, call .finalize() to flush CSV/JSON/PNG.
    """
    def __init__(self, outdir: Path, stem: str = "network", sim_name: str = "stream", save_plot: bool = True):
        self.outdir = Path(outdir)
        self.stem = stem
        self.sim_name = sim_name
        self.save_plot = save_plot
        self._times = []
        self._values = []
        self._count = 0
        self._last_time = 0.0
        self._start_ts = time.time()
        self._plt = _import_matplotlib()
        self._live_fig = None
        self._max_points = 10000  # avoid memory explosion

        # prepare live figure if matplotlib present
        if self._plt is not None:
            try:
                self._live_fig, self._ax = self._plt.subplots(figsize=(8,3))
                self._line_ts, = self._ax.plot([], [], label="sum_signed")
                self._ax.axhline(0.0, color="k", linestyle="--", linewidth=0.6)
                self._ax.set_xlabel("Time (s)")
                self._ax.set_ylabel("Flow (m³/s)")
                self._ax.set_title(f"Live sum(flows) - {stem}")
                self._ax.grid(True, linestyle=":", linewidth=0.4)
                self._plt.tight_layout()
                # non-blocking interactive mode
                try:
                    self._plt.ion()
                except Exception:
                    pass
            except Exception:
                self._live_fig = None

    def __call__(self, evt: str, data: Dict[str, Any]):
        """
        When called as callback, expects evt='simulation' or 'simulation_step'
        data can contain:
          - 'flows' : dict link->value
          - 'total_flow' : float
          - 'time_s' : float
          - 'step_index' : int
        """
        try:
            if not data:
                return
            # only interested in simulation snapshots
            if evt not in ("simulation", "simulation_step", "sim_step", "sim_snapshot"):
                return
            t = data.get("time_s", None)
            total = None
            if "total_flow" in data:
                total = float(data["total_flow"])
            elif "flows" in data and isinstance(data["flows"], dict):
                total = sum(float(v or 0.0) for v in data["flows"].values())
            elif "flows_snapshot" in data and isinstance(data["flows_snapshot"], dict):
                total = sum(float(v or 0.0) for v in data["flows_snapshot"].values())
            # fallback: compute from 'flows_series' if present (last)
            if total is None and "flows_series" in data and isinstance(data["flows_series"], list):
                last = data["flows_series"][-1]
                if isinstance(last, dict):
                    total = sum(float(v or 0.0) for v in last.values())
            if total is None:
                return

            if t is None:
                # approximate time elapsed since consumer creation
                t = time.time() - self._start_ts
            # Append
            self._times.append(float(t))
            self._values.append(float(total))
            self._count += 1
            # keep memory bounded
            if self._count > self._max_points:
                self._times.pop(0)
                self._values.pop(0)
                self._count -= 1
            # live update plot
            if self._plt is not None and self._live_fig is not None:
                try:
                    self._line_ts.set_data(self._times, self._values)
                    self._ax.relim()
                    self._ax.autoscale_view()
                    self._plt.pause(0.001)
                except Exception:
                    pass
        except Exception as e:
            logger.debug("FlowEventConsumer error: %s", e)

    def finalize(self):
        # write CSV/JSON/PNG
        try:
            import pandas as pd
            outdir = Path(self.outdir)
            outdir.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame({"time_s": self._times, "sum_signed_m3s": self._values})
            csv_file = outdir / f"{self.stem}_sumflows_{self.sim_name}_stream.csv"
            df.to_csv(csv_file, index=False)
            json_file = outdir / f"{self.stem}_sumflows_{self.sim_name}_stream.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump({"series": df.to_dict(orient="records")}, f, indent=2, ensure_ascii=False)
            png_file = None
            if self._plt is not None and self.save_plot:
                try:
                    fig = self._live_fig
                    png_file = outdir / f"{self.stem}_sumflows_{self.sim_name}_stream.png"
                    fig.savefig(str(png_file), dpi=150)
                except Exception:
                    png_file = None
            logger.info("FlowEventConsumer finalize: csv=%s json=%s png=%s", csv_file, json_file, png_file)
            return {"csv": str(csv_file), "json": str(json_file), "png": str(png_file) if png_file else None}
        except Exception as e:
            logger.exception("FlowEventConsumer finalize error: %s", e)
            return {}
