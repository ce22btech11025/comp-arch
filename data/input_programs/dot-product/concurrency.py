import subprocess
import re
import os
import statistics

# ----------------------------------------------------------
# CONFIGURATION — UPDATE YOUR EXE NAMES HERE
# ----------------------------------------------------------
EXEC_INT   = "1-normal.exe"        # INT-only program
EXEC_FLOAT = "2-normal.exe"        # FLOAT-only program
EXEC_MIXED = "8-normal.exe"        # Mixed 80–20 program

RUNS = 5   # number of times each exe runs
# ----------------------------------------------------------

time_regex = re.compile(r"Time.*=\s*([0-9]+\.[0-9]+)", re.IGNORECASE)


def run_and_get_time(exe):
    """Run executable and extract execution time."""
    if not os.path.exists(exe):
        print(f"[ERROR] Executable not found: {exe}")
        return None

    out = subprocess.run(exe, shell=True, capture_output=True, text=True).stdout

    # extract time
    m = time_regex.search(out)
    if not m:
        print(f"[ERROR] No time found in output of {exe}")
        print("Output was:")
        print(out)
        return None

    return float(m.group(1))


def average_time(exe):
    """Run executable RUNS times and return average time."""
    times = []
    for r in range(RUNS):
        print(f"Running {exe} [{r+1}/{RUNS}]...")
        t = run_and_get_time(exe)
        if t is not None:
            times.append(t)

    if not times:
        return None

    return sum(times) / len(times)


print("\n=========================================")
print(" ALU + FPU CONCURRENCY VERIFICATION TOOL ")
print("==========================================\n")

# ------------------------------
# RUN ALL THREE EXECUTABLES
# ------------------------------

print("\n--- Measuring INT-only time ---")
t_int = average_time(EXEC_INT)
print(f"\nINT-only average time = {t_int:.6f} sec\n")

print("\n--- Measuring FLOAT-only time ---")
t_float = average_time(EXEC_FLOAT)
print(f"\nFLOAT-only average time = {t_float:.6f} sec\n")

print("\n--- Measuring MIXED (80–20) time ---")
t_mixed = average_time(EXEC_MIXED)
print(f"\nMIXED 80–20 average time = {t_mixed:.6f} sec\n")

# ------------------------------
# CONCURRENCY ANALYSIS
# ------------------------------
print("\n==========================================")
print("          FINAL CONCURRENCY RESULT         ")
print("==========================================")

serial_expected = t_int + t_float
parallel_expected = max(t_int, t_float)

print(f"Expected serial time:     {serial_expected:.6f} sec")
print(f"Expected parallel time:   {parallel_expected:.6f} sec")
print(f"Measured mixed time:      {t_mixed:.6f} sec\n")

if t_mixed <= parallel_expected * 1.20:
    print(">>> RESULT: ALU + FPU executed concurrently ✔")
else:
    print(">>> RESULT: NO strong concurrency detected ✖")

print("\nDone.\n")
