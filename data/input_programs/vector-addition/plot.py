import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# ---------------------------------------
# Locate all vec_*.txt files
# ---------------------------------------
files = sorted(glob.glob("vec_*.txt"))

if not files:
    raise FileNotFoundError("No vec_*.txt files found in folder!")

print("Found files:", files)

# ---------------------------------------
# Determine baseline file (vec_100_0.txt)
# ---------------------------------------
baseline_file = None
for f in files:
    if "100_0" in f:
        baseline_file = f
        break

if baseline_file is None:
    raise FileNotFoundError("Baseline vec_100_0.txt not found!")

print(f"\nUsing baseline: {baseline_file}")

# ---------------------------------------
# Load baseline vector
# ---------------------------------------
with open(baseline_file, "r") as fp:
    baseline_time = float(fp.readline().split()[1])
baseline = np.loadtxt(baseline_file, skiprows=1)

print(f"Baseline entries: {len(baseline)}")

# ---------------------------------------
# Evaluate all files
# ---------------------------------------
rmse_list = []
time_list = []
name_list = []

for f in files:
    print(f"\nProcessing {f}")

    # Read execution time
    with open(f, "r") as fp:
        first_line = fp.readline().split()
        time_val = float(first_line[1])

    # Load vector data
    vec = np.loadtxt(f, skiprows=1)

    # Compute RMSE
    rmse = np.sqrt(np.mean((vec - baseline) ** 2))

    rmse_list.append(rmse)
    time_list.append(time_val)
    name_list.append(f.replace(".txt", ""))

    print(f"RMSE = {rmse:.6f}, Time = {time_val:.6f}")

# ---------------------------------------
# Plot RMSE
# ---------------------------------------
plt.figure(figsize=(10, 5))
plt.bar(name_list, rmse_list)
plt.ylabel("RMSE")
plt.xlabel("File")
plt.title("RMSE Comparison (Vector Outputs)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("rmse_plot.png")

print("\nSaved: rmse_plot.png")

# ---------------------------------------
# Plot Time
# ---------------------------------------
plt.figure(figsize=(10, 5))
plt.bar(name_list, time_list)
plt.ylabel("Execution Time (sec)")
plt.xlabel("File")
plt.title("Execution Time Comparison (Vector Outputs)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("time_plot.png")

print("Saved: time_plot.png")

print("\nAnalysis complete!")
