import subprocess
import re

# --------------------------------------
# USER INPUT: LIST OF .c FILES
# --------------------------------------
files = [
    "test1.c",
    "test2.c",
    "test3.c",
    "test4.c",
    "test5.c",
    "test6.c",
]

COMPILER = "gcc"
FLAGS = ["-O3"]


# --------------------------------------
# Function to determine exe name
# --------------------------------------
def get_exe_name(cfile):
    # match patterns like vector_add_50_50.c → 50.exe
    match = re.match(r"test.*(\d)\.c", cfile)
    if match:
        return f"{match.group(1)}.exe"

    # fallback
    return cfile.replace(".c", ".exe")


# --------------------------------------
# COMPILE & RUN (NO TXT FILES)
# --------------------------------------
for cfile in files:

    exe = get_exe_name(cfile)

    print(f"\n==> Compiling {cfile} → {exe}")

    cmd = [COMPILER] + FLAGS + [cfile, "-o", exe]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"❌ Compilation failed for {cfile}")
        print(result.stderr)
        continue

    print(f"✔ Compilation successful")

    # Run the executable
    print(f"==> Running {exe}")
    run = subprocess.run([exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print the output directly (NO txt file creation)
    print(run.stdout)
