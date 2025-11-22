import subprocess
import re

# --------------------------
# USER FILE LIST (EDIT HERE)
# --------------------------
files = [
    "matmul_0_100.c",
    "matmul_50_50.c",
    "matmul_60_40.c",
    "matmul_75_25.c",
    "matmul_80_20.c",
    "matmul_90_10.c",
    "matmul_95_5.c",
    "matmul_100_0.c",
    "test.c"
]

COMPILER = "gcc"
FLAGS = ["-O3"]


def get_exe_name(filename):
    """Extract exe name from filename pattern."""
    if filename == "test.c":
        return "baseline.exe"

    match = re.match(r"matmul_(\d+)_\d+\.c", filename)
    if match:
        return f"{match.group(1)}.exe"

    return filename.replace(".c", ".exe")


def compile_and_run(cfile):
    exe = get_exe_name(cfile)
    txt = exe.replace(".exe", ".txt")

    print(f"\n==> Compiling {cfile} as {exe}")

    cmd = [COMPILER, "-O3", cfile, "-o", exe]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"❌ Compilation failed for {cfile}")
        print(result.stderr)
        return

    print(f"✔ Compilation successful → {exe}")

    print(f"Running {exe} ...")
    run = subprocess.run([exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    with open(txt, "w") as f:
        f.write(run.stdout)

    print(f"✔ Output saved → {txt}")


# --------------------------
# MAIN LOOP
# --------------------------
for cfile in files:
    compile_and_run(cfile)
