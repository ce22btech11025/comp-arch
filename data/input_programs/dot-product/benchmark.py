# benchmark_full_final.py
# - Raw logs for all runs
# - Averages for each exe
# - CSV summary (exe, avg_time, avg_dot)
# - Plots comparing normal vs native

import subprocess
import re
import os
import csv
import matplotlib.pyplot as plt

executables = [
    "1-normal.exe","2-normal.exe","5-normal.exe","6-normal.exe","7-normal.exe","8-normal.exe","9-normal.exe","10-normal.exe","11-normal.exe",
    "1-native.exe","2-native.exe","5-native.exe","6-native.exe","7-native.exe","8-native.exe","9-native.exe","10-native.exe","11-native.exe"
]

RUNS = 15

dot_regex  = re.compile(r"Dot product\b.*=\s*([0-9]+)", re.IGNORECASE)
time_regex = re.compile(r"Time\b.*=\s*([0-9]+\.[0-9]+)", re.IGNORECASE)

LOGFILE = "benchmark_log.txt"
CSVFILE = "results.csv"

def run_and_capture(exe):
    proc = subprocess.run(exe, capture_output=True, text=True, shell=True)
    return proc.stdout

print("=================================================")
print(f" Running each EXE {RUNS} times")
print(" Raw logs to benchmark_log.txt")
print(" Summary to results.csv")
print("=================================================\n")

# Clean old files
with open(LOGFILE, "w", encoding="utf-8") as f:
    f.write("====== GLOBAL BENCHMARK LOG ======\n\n")

with open(CSVFILE, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["exe_name", "avg_time", "avg_dot"])

results = {}

# ====================================================
# Run All Executables
# ====================================================
for exe in executables:

    if not os.path.exists(exe):
        print(f"Skipping {exe} (not found)\n")
        with open(LOGFILE, "a", encoding="utf-8") as logf:
            logf.write(f"--- {exe} NOT FOUND ---\n\n")
        continue

    print(f"--- Running {exe} ---")
    all_times = []
    all_dots = []

    # Write header inside log
    with open(LOGFILE, "a", encoding="utf-8") as logf:
        logf.write(f"EXECUTABLE: {exe}\n")

        for i in range(1, RUNS + 1):
            print(f"Run {i}...")
            out = run_and_capture(exe)

            # Raw log
            logf.write(f"\n----- Run {i} -----\n")
            logf.write(out + "\n")

            # Extract dot
            dot_match = dot_regex.search(out)
            if dot_match:
                all_dots.append(int(dot_match.group(1)))
            else:
                for line in out.splitlines():
                    if "dot" in line.lower():
                        m = re.search(r"([0-9]{2,})", line)
                        if m:
                            all_dots.append(int(m.group(1)))
                            break

            # Extract time
            time_match = time_regex.search(out)
            if time_match:
                all_times.append(float(time_match.group(1)))
            else:
                m = re.search(r"([0-9]+\.[0-9]+)", out)
                if m:
                    all_times.append(float(m.group(1)))

            print(out, end="")

    avg_time = sum(all_times) / len(all_times) if all_times else 0.0
    avg_dot  = sum(all_dots)  / len(all_dots)  if all_dots  else 0.0

    print(f"Averages for {exe}:")
    print(f"  Average time = {avg_time:.6f} sec")
    print(f"  Average dot  = {avg_dot:.3f}")
    print("--------------------------------------------\n")

    # Append summary into log
    with open(LOGFILE, "a", encoding="utf-8") as logf:
        logf.write("\n===== SUMMARY =====\n")
        logf.write(f"Runs attempted: {RUNS}\n")
        logf.write(f"Successful time entries: {len(all_times)}\n")
        logf.write(f"Successful dot entries:  {len(all_dots)}\n")
        logf.write(f"Average time: {avg_time:.6f} sec\n")
        logf.write(f"Average dot product: {avg_dot:.3f}\n")

    # Save into CSV
    with open(CSVFILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([exe, avg_time, avg_dot])

    results[exe] = (avg_time, avg_dot)

print("DONE! Raw logs + CSV generation complete.\n")


# ====================================================
# PLOTS (clean version, readable x-axis labels)
# ====================================================

sources = [
    "1int-normal.c",
    "2float-normal.c",
    "5int50float50.c",
    "6int60float40.c",
    "7int75float25.c",
    "8int80float20.c",
    "9int90float10.c",
    "10int95float5.c",
    "11int100float0.c"
]

normal_times = []
native_times = []
normal_dots = []
native_dots = []

for src in sources:
    prefix = src.split("int")[0].split("float")[0].strip()  # extract '1', '2', '5', ...
    n = f"{prefix}-normal.exe"
    v = f"{prefix}-native.exe"

    if n in results and v in results:
        normal_times.append(results[n][0])
        native_times.append(results[v][0])
        normal_dots.append(results[n][1])
        native_dots.append(results[v][1])
    else:
        normal_times.append(0)
        native_times.append(0)
        normal_dots.append(0)
        native_dots.append(0)


# --------- Plot 1: Time ----------
plt.figure(figsize=(12,6))
plt.plot(sources, normal_times, marker='o', label="Normal EXE")
plt.plot(sources, native_times, marker='o', label="Native EXE")
plt.title("Execution Time Comparison")
plt.xlabel("Source C File")
plt.ylabel("Time (seconds)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig("time_plot.png", dpi=300)
plt.close()


# --------- Plot 2: Dot Product ----------
plt.figure(figsize=(12,6))
plt.plot(sources, normal_dots, marker='o', label="Normal EXE")
plt.plot(sources, native_dots, marker='o', label="Native EXE")
plt.title("Dot Product Value Comparison")
plt.xlabel("Source C File")
plt.ylabel("Dot Product")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig("dot_plot.png", dpi=300)
plt.close()

print("Graphs saved: time_plot.png, dot_plot.png")
