import psutil
import subprocess
import time
from pathlib import Path

class PowerProfiler:
    """
    Estimates power and CPU usage while running a binary.
    (Requires psutil, works best on Linux.)
    """

    def __init__(self, log_dir="data/results/power_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def profile(self, binary_path: str, duration_limit: float = 10.0):
        """
        Run the binary and record CPU% and approximate power usage.
        """
        log_path = self.log_dir / f"{Path(binary_path).stem}_power.csv"

        proc = subprocess.Popen([binary_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        start_time = time.time()
        records = []

        while proc.poll() is None:
            cpu = psutil.cpu_percent(interval=0.2)
            power_est = cpu * 0.01 * psutil.cpu_freq().max  # heuristic
            records.append((time.time() - start_time, cpu, power_est))
            if time.time() - start_time > duration_limit:
                proc.terminate()
                break

        # Save to CSV
        with open(log_path, "w") as f:
            f.write("time_s,cpu_percent,power_est(W)\n")
            for t, cpu, pw in records:
                f.write(f"{t:.3f},{cpu:.2f},{pw:.2f}\n")

        print(f"[PowerProfiler] Saved: {log_path}")
        return log_path
