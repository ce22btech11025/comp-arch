import os
import subprocess
from pathlib import Path

class CompilerRunner:
    """
    Compiles C source files using GCC or Clang with given flags.
    """

    def __init__(self, compiler="gcc", output_dir="data/results/bin"):
        self.compiler = compiler
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compile(self, source_path: str, output_name: str = None, extra_flags=None):
        """
        Compile a C file and return path to the generated executable.
        """
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        if output_name is None:
            output_name = source.stem
        output_exe = self.output_dir / output_name

        cmd = [self.compiler, str(source), "-o", str(output_exe), "-O3", "-lm"]
        if extra_flags:
            cmd.extend(extra_flags)

        print(f"[Compiler] Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"[Compiler] ✅ Successfully built {output_exe}")
        except subprocess.CalledProcessError as e:
            print(f"[Compiler] ❌ Compilation failed for {source_path}")
            print("stderr:", e.stderr)
            raise

        return str(output_exe)
