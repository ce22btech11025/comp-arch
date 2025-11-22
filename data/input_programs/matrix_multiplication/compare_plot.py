import numpy as np
import matplotlib.pyplot as plt
import glob

N = 120

# Load baseline
baseline = np.loadtxt("baseline_output.txt", skiprows=1)
baseline = baseline.reshape(N, N)

files = sorted(glob.glob("out_*.txt"))   # all experiment output files

rmse_vals = []
times = []
names = []

for f in files:
    # read file
    with open(f, "r") as fp:
        first = fp.readline().strip().split()
        time_val = float(first[1])
        mat = np.loadtxt(f, skiprows=1).reshape(N, N)

    rmse = np.sqrt(np.mean((mat - baseline)**2))

    names.append(f.replace("out_", "").replace(".txt", ""))
    rmse_vals.append(rmse)
    times.append(time_val)

    print(f"{f}: RMSE={rmse}, Time={time_val}")

# Plot RMSE
plt.figure()
plt.bar(names, rmse_vals)
plt.ylabel("RMSE")
plt.title("RMSE Comparison")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("rmse_plot.png")

# Plot Times
plt.figure()
plt.bar(names, times)
plt.ylabel("Time (sec)")
plt.title("Execution Time Comparison")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("time_plot.png")

print("Plots saved: rmse_plot.png  and  time_plot.png")
