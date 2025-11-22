import pandas as pd
from pathlib import Path

class SummaryReport:
    """
    Generates textual summary reports comparing integer vs floating-point versions.
    """

    def __init__(self, results_csv="data/results/benchmarks/benchmark_results.csv", output_file="data/results/summary_report.txt"):
        self.results_csv = Path(results_csv)
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def generate(self):
        if not self.results_csv.exists():
            raise FileNotFoundError(f"No benchmark results found: {self.results_csv}")

        df = pd.read_csv(self.results_csv)
        df['base'] = df['binary'].apply(lambda x: x.replace('_fp', '').replace('_int', ''))

        grouped = df.groupby('base')
        summary_lines = ["ALU vs FPU Performance Summary\n", "-" * 40 + "\n"]

        for prog, group in grouped:
            int_time = group[group['binary'].str.contains('_int')]['avg_time_s'].mean()
            fp_time = group[group['binary'].str.contains('_fp')]['avg_time_s'].mean()

            if pd.isna(int_time) or pd.isna(fp_time):
                continue

            speedup = (int_time - fp_time) / int_time * 100
            summary_lines.append(f"{prog:<25}  ALU: {int_time:.6f}s  |  FPU: {fp_time:.6f}s  |  Δ: {speedup:+.2f}%\n")

        with open("summary.txt", "w", encoding="utf-8") as f:
            f.writelines(summary_lines)

        print(f"[Visualizer] Summary written to {self.output_file}")
        return self.output_file
