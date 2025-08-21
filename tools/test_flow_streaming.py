# tools/test_flow_streaming.py
import time, random
from pathlib import Path
from src.lcpi.aep.utils.flows_inspector import FlowEventConsumer

def main():
    out = Path("results/test_stream")
    out.mkdir(parents=True, exist_ok=True)
    consumer = FlowEventConsumer(outdir=out, stem="demo", sim_name="teststream", save_plot=True)
    # simulate events for 60 steps:
    for i in range(60):
        # fake flows dict with 3 pipes
        flows = {"P1": random.uniform(-0.2,0.3), "P2": random.uniform(-0.1,0.2), "P3": random.uniform(-0.05,0.05)}
        evt = "simulation"
        data = {"time_s": float(i), "flows": flows}
        consumer(evt, data)
        time.sleep(0.02)
    consumer.finalize()
    print("stream test done, artifacts in", out)

if __name__ == "__main__":
    main()
