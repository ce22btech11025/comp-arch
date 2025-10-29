import subprocess
import time
import csv
from pathlib import Path

class BenchmarkRunner:
    """
    Executes compiled binaries and records performance metrics.
    """

    def __init__(self, results_dir="data/results/benchmarks"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def run(self, binary_path: str, input_args=None, repeat=3):
        """
        Execute binary multiple times and compute average runtime.
        """
        input_args = input_args or []
        times = []

        for i in range(repeat):
            start = time.perf_counter()
            result = subprocess.run([binary_path] + input_args,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            end = time.perf_counter()
            times.append(end - start)

        avg_time = sum(times) / len(times)
        print(f"[Benchmark] {Path(binary_path).name}: {avg_time:.6f}s avg over {repeat} runs")

        # Save results
        self._save_result(binary_path, avg_time, repeat)
        return avg_time

    def _save_result(self, binary_path, avg_time, repeat):
        csv_path = self.results_dir / "benchmark_results.csv"
        file_exists = csv_path.exists()

        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["binary", "avg_time_s", "repetitions"])
            writer.writerow([Path(binary_path).name, f"{avg_time:.6f}", repeat])
