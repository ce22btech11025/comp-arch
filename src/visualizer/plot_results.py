import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

class PlotResults:
    """
    Handles generation of runtime comparison plots.
    """

    def __init__(self, results_csv="data/results/benchmarks/benchmark_results.csv", output_dir="data/results/plots"):
        self.results_csv = Path(results_csv)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self):
        if not self.results_csv.exists():
            raise FileNotFoundError(f"Benchmark results not found at {self.results_csv}")
        return pd.read_csv(self.results_csv)

    def plot_comparison(self):
        """
        Creates a bar chart comparing integer vs floating versions of each program.
        Assumes binaries are named like matrix_multiplication_int / matrix_multiplication_fp.
        """
        df = self.load_data()

        # Normalize names like "matrix_multiplication_fp" -> "matrix_multiplication"
        df['base'] = df['binary'].apply(lambda x: x.replace('_fp', '').replace('_int', ''))

        # Pivot to side-by-side comparison
        pivot = df.pivot(index='base', columns='binary', values='avg_time_s')

        # Bar chart
        pivot.plot(kind='bar', figsize=(10, 6))
        plt.title("Execution Time Comparison: Integer (ALU) vs Floating-Point (FPU)")
        plt.ylabel("Average Time (seconds)")
        plt.xlabel("Program")
        plt.grid(True, axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()

        plot_path = self.output_dir / "alu_vs_fpu_runtime_comparison.png"
        plt.savefig(plot_path)
        plt.close()
        print(f"[Visualizer] ✅ Plot saved at {plot_path}")
        return plot_path
