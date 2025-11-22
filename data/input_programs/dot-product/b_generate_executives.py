import subprocess
import os

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

for src in sources:
    if not os.path.exists(src):
        print(f"Skipping {src} (file not found)")
        continue

    # extract number prefix (1,2,5,6,...)
    prefix = src.split("int")[0].split("float")[0]  # handles both patterns
    prefix = prefix.strip()  # just in case

    normal_exe = f"{prefix}-normal.exe"
    native_exe = f"{prefix}-native.exe"

    cmd_normal = f"gcc -O3 {src} -o {normal_exe}"
    cmd_native = f"gcc -O3 -march=native {src} -o {native_exe}"

    print(f"Compiling {src} to {normal_exe}")
    subprocess.run(cmd_normal, shell=True)

    print(f"Compiling {src} to {native_exe}")
    subprocess.run(cmd_native, shell=True)

print("processing complete")
