# benchmark_full_fixed.py
# Run each exe RUNS times, save raw output, extract exact dot-product and exact time,
# compute average dot-product and average time, append summary to the .txt log.

import subprocess
import re
import os

# Put your executables here (same names as on disk)
executables = [
    "1.exe",
    "2.exe",
    "3.exe",
    "4.exe",
    "5.exe",
    "6.exe",
    "7.exe",
    "8.exe",
    "9.exe","10.exe", "11.exe", "12.exe"
    # "6.exe"
]

RUNS = 15

# Specific regex patterns
dot_regex  = re.compile(r"Dot product\b.*=\s*([0-9]+)", re.IGNORECASE)
time_regex = re.compile(r"Time\b.*=\s*([0-9]+\.[0-9]+)", re.IGNORECASE)

def run_and_capture(exe):
    """Run exe and return stdout (as a single string)."""
    # shell=True makes it work on Windows with .exe names
    proc = subprocess.run(exe, capture_output=True, text=True, shell=True)
    return proc.stdout

print("==============================================")
print(f" Running each EXE {RUNS} times")
print(" Saving RAW output + computing averages")
print("==============================================\n")

for exe in executables:
    if not os.path.exists(exe):
        print(f"Skipping {exe} (not found)\n")
        continue

    logname = exe.replace(".exe", ".txt")
    print(f"--- Running {exe} ---")
    all_times = []
    all_dots = []

    with open(logname, "w", encoding="utf-8") as logf:
        for i in range(1, RUNS + 1):
            print(f"Run {i}...")
            out = run_and_capture(exe)

            # Write raw output to file (preserve exactly)
            logf.write(f"===== Run {i} =====\n")
            logf.write(out + "\n")

            # Search for Dot product line (exact)
            dot_match = dot_regex.search(out)
            if dot_match:
                dot_val = int(dot_match.group(1))
                all_dots.append(dot_val)
            else:
                # fallback: try to find a line that starts with "Dot" loosely
                for line in out.splitlines():
                    if "dot" in line.lower():
                        m = re.search(r"([0-9]{2,})", line)   # only big integers
                        if m:
                            all_dots.append(int(m.group(1)))
                            break
                else:
                    print(f"  Warning: Dot product not found in run {i} output of {exe}")

            # Search for Time line (exact)
            time_match = time_regex.search(out)
            if time_match:
                t = float(time_match.group(1))
                all_times.append(t)
            else:
                # fallback: find any float-looking number (with decimal) in output
                fm = re.search(r"([0-9]+\.[0-9]+)", out)
                if fm:
                    all_times.append(float(fm.group(1)))
                else:
                    print(f"  Warning: Time not found in run {i} output of {exe}")

            # print the raw output on screen (as you requested)
            print(out, end="")

    # compute averages safely
    avg_time = sum(all_times) / len(all_times) if all_times else 0.0
    avg_dot  = sum(all_dots)  / len(all_dots)  if all_dots  else 0.0

    # print summary
    print(f"Averages for {exe}:")
    print(f"  Average time = {avg_time:.6f} sec (based on {len(all_times)} runs)")
    print(f"  Average dot  = {avg_dot:.3f} (based on {len(all_dots)} runs)")
    print("--------------------------------------------\n")

    # append summary to log file
    with open(logname, "a", encoding="utf-8") as logf:
        logf.write("\n===== SUMMARY =====\n")
        logf.write(f"Runs attempted: {RUNS}\n")
        logf.write(f"Successful time entries: {len(all_times)}\n")
        logf.write(f"Successful dot entries:  {len(all_dots)}\n")
        logf.write(f"Average time: {avg_time:.6f} sec\n")
        logf.write(f"Average dot_product: {avg_dot:.3f}\n")

print("DONE!")
