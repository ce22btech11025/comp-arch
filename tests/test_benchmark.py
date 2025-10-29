import unittest
import os
from pathlib import Path
from src.executor.compiler_runner import CompilerRunner
from src.executor.benchmark_runner import BenchmarkRunner

class TestBenchmark(unittest.TestCase):

    def setUp(self):
        # Prepare directories
        self.work_dir = Path("data/tests_temp")
        self.work_dir.mkdir(parents=True, exist_ok=True)

        # Minimal C program to benchmark
        self.source_file = self.work_dir / "hello.c"
        with open(self.source_file, "w") as f:
            f.write('#include <stdio.h>\nint main(){ for(int i=0;i<1000;i++); printf("done\\n"); return 0; }')

        # Compile binary
        self.compiler = CompilerRunner(output_dir=self.work_dir)
        self.binary_path = self.compiler.compile(str(self.source_file), output_name="hello_test")

    def tearDown(self):
        for file in self.work_dir.iterdir():
            file.unlink()
        self.work_dir.rmdir()

    def test_benchmark_runs_successfully(self):
        runner = BenchmarkRunner(results_dir=self.work_dir)
        avg_time = runner.run(self.binary_path, repeat=2)
        self.assertTrue(avg_time > 0)
        self.assertTrue((self.work_dir / "benchmark_results.csv").exists())

if __name__ == "__main__":
    unittest.main()
