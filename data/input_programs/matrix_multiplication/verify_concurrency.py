import subprocess
import re
import statistics
import os

# -----------------------------
# Executable Names
# -----------------------------
EXEC_INT   = "matmul_100_0.exe"     # 100% integer ops
EXEC_FLOAT = "matmul_0_100.exe"     # 100% float ops
EXEC_MIX   = "matmul_80_20.exe"     # 80% ALU + 20% FPU

RUNS = 5
time_regex = re.compile(r"([0-9]+\.[0-9]+) sec", re.IGNORECASE)


def run_get_time(exe):
    """Run executable and extract time from printf output."""
    if not os.path.exists(exe):
        print(f"[ERROR] Executable not found: {exe}")
        return None

    out = subprocess.run(exe, capture_output=True, text=True, shell=True).stdout
    m = time_regex.search(out)

    if not m:
        print(f"[ERROR] No time found in output of {exe}")
        print("Output was:")
        print(out)
        return None

    return float(m.group(1))


def avg_time(exe):
    times = []
    for r in range(RUNS):
        print(f"Running {exe} [{r+1}/{RUNS}]...")
        t = run_get_time(exe)
        if t:
            times.append(t)

    if not times:
        return None

    return sum(times) / len(times)


print("\n==============================")
print(" MATRIX MUL ALU/FPU CONCURRENCY TEST ")
print("==============================\n")

print("\n--- Measuring INT-only (100/0) ---")
t_int = avg_time(EXEC_INT)
print(f"INT-only average = {t_int:.6f} sec\n")

print("--- Measuring FLOAT-only (0/100) ---")
t_float = avg_time(EXEC_FLOAT)
print(f"FLOAT-only average = {t_float:.6f} sec\n")

print("--- Measuring MIXED (80/20) ---")
t_mix = avg_time(EXEC_MIX)
print(f"MIXED 80/20 average = {t_mix:.6f} sec\n")

# -------------------------------------------------
# Concurrency Analysis
# -------------------------------------------------
print("============== ANALYSIS ==============")

serial = t_int + t_float
parallel = max(t_int, t_float)

print(f"Expected serial time     : {serial:.6f} sec")
print(f"Expected parallel time   : {parallel:.6f} sec")
print(f"Measured mixed time      : {t_mix:.6f} sec\n")

if t_mix <= parallel * 1.20:
    print(">>> RESULT: ALU + FPU executed concurrently ✔")
    print("Mixed time close to max(INT, FLOAT)")
else:
    print(">>> RESULT: No strong concurrency ✖")
    print("Mixed time close to INT + FLOAT")

print("\nDone.\n")
