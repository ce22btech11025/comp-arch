# import math

# def gcd(a, b):
#     """Computes the greatest common divisor of a and b."""
#     while b:
#         a, b = b, a % b
#     return a

# def generate_c_code(int_percent, float_percent):
#     """
#     Generates C code for vector addition with a specified int/float ratio.
#     """
#     if int_percent + float_percent != 100:
#         raise ValueError("Percentages must sum to 100.")

#     common_divisor = gcd(int_percent, float_percent)

#     ratio_int = int_percent // common_divisor
#     ratio_float = float_percent // common_divisor

#     CHUNK_SIZE = 40

#     unit = ratio_int + ratio_float
#     scale = CHUNK_SIZE // unit
#     INT_OPS = ratio_int * scale
#     FLOAT_OPS = ratio_float * scale
#     REM = CHUNK_SIZE - (INT_OPS + FLOAT_OPS)
#     INT_OPS += REM

#     # FIXED: escape % for C string → %%
#     ratio_str = f"{int_percent}%% Int / {float_percent}%% Float"

#     filename = f"vector_add_{int_percent}_{float_percent}.c"

#     alu_loop = ""
#     if INT_OPS > 0:
#         alu_loop = f"""
#         // {INT_OPS} integer operation(s)
#         for (int k = 0; k < INT_OPS; ++k) {{
#             int idx = base + k;
#             C[idx] = A[idx] + B[idx];
#         }}"""

#     fpu_loop = ""
#     if FLOAT_OPS > 0:
#         fpu_loop = f"""
#         // {FLOAT_OPS} float operation(s)
#         for (int k = INT_OPS; k < (INT_OPS + FLOAT_OPS); ++k) {{
#             int idx = base + k;
#             C[idx] = (int)((float)A[idx] + (float)B[idx]);
#         }}"""

#     loop_content = f"""
#     // --- Mixed Vector Addition ({ratio_str}) ---
#     int i = 0;
#     for (; i + CHUNK - 1 < N; i += CHUNK) {{
#         int base = i;
# {alu_loop}
# {fpu_loop}
#     }}"""

#     tail_content = f"""
#     // Tail handling for leftover elements
#     for (; i < N; ++i) {{
#         int pos = i % CHUNK;
#         if (pos < INT_OPS) {{
#             C[i] = A[i] + B[i];
#         }} else {{
#             C[i] = (int)((float)A[i] + (float)B[i]);
#         }}
#     }}"""

#     c_template = f"""#include <stdio.h>
# #include <stdlib.h>
# #include <time.h>

# #define N 10000000
# #define RATIO "{ratio_str}"
# #define INT_OPS {INT_OPS}
# #define FLOAT_OPS {FLOAT_OPS}
# #define CHUNK {CHUNK_SIZE}

# int main() {{
#     static int A[N], B[N];
#     static int C[N];
#     clock_t t0, t1;

#     srand(0);
#     for (int i = 0; i < N; i++) {{
#         A[i] = 17000000 + rand() % 83000001;
#         B[i] = 17000000 + rand() % 83000001;
#     }}

#     t0 = clock();
# {loop_content}
# {tail_content}
#     t1 = clock();

#     printf("Vector Addition (%s) Time = %.6f sec\\n",
#         RATIO, (double)(t1 - t0) / CLOCKS_PER_SEC);
#         // -------------------------------------------
#     // SAVE OUTPUT VECTOR AND TIME FOR PYTHON RMSE
#     // -------------------------------------------

#     char fname[64];
#     sprintf(fname, "vec_%s.txt", RATIO);  // convert "50% Int / 50% Float" → "vec_50% Int / 50% Float.txt"

#     // Replace spaces and % for safe filenames
#     for (int x = 0; fname[x]; x++) {
#         if (fname[x] == ' ') fname[x] = '_';
#         if (fname[x] == '%') fname[x] = 'p';
#         if (fname[x] == '/') fname[x] = '-';
#     }

#     FILE *fp = fopen(fname, "w");

#     fprintf(fp, "time %.6f\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

#     for (int i = 0; i < N; i++) {
#         fprintf(fp, "%d\n", C[i]);
#     }

#     fclose(fp);

#     printf("Vector output saved to %s\n", fname);

#     return 0;
# }}
# """

#     return c_template, filename


# if __name__ == "__main__":
#     print("Welcome to the C Code Vector Addition Generator!")
#     print("This script will generate a C file for a given Integer/Float ratio (X/Y).")

#     while True:
#         try:
#             int_p = int(input("Enter Integer percentage (X%): "))
#             float_p = int(input("Enter Float percentage (Y%): "))

#             if int_p + float_p != 100:
#                 print("Error: The percentages must sum to 100.")
#                 continue

#             code, filename = generate_c_code(int_p, float_p)

#             with open(filename, "w") as f:
#                 f.write(code)

#             print(f"\nC file generated: {filename}\n")

#             choice = input("Generate another ratio? (y/n): ")
#             if choice.lower() != 'y':
#                 break

#         except ValueError as e:
#             print(f"Invalid input: {e}. Please enter whole numbers.")
#         except Exception as e:
#             print(f"Unexpected error: {e}")
import math

def gcd(a, b):
    """Computes the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def generate_c_code(int_percent, float_percent):
    """
    Generates C code for vector addition with a specified int/float ratio.
    """
    if int_percent + float_percent != 100:
        raise ValueError("Percentages must sum to 100.")

    common_divisor = gcd(int_percent, float_percent)

    ratio_int = int_percent // common_divisor
    ratio_float = float_percent // common_divisor

    CHUNK_SIZE = 40

    unit = ratio_int + ratio_float
    scale = CHUNK_SIZE // unit
    INT_OPS = ratio_int * scale
    FLOAT_OPS = ratio_float * scale
    REM = CHUNK_SIZE - (INT_OPS + FLOAT_OPS)
    INT_OPS += REM

    # Escape % for C printf and filenames
    ratio_str = f"{int_percent}% Int / {float_percent}% Float"

    # Safe filename version
    safe_ratio = ratio_str.replace("%", "p").replace(" ", "_").replace("/", "-")

    filename = f"vector_add_{int_percent}_{float_percent}.c"

    # Escape braces in f-strings
    alu_loop = ""
    if INT_OPS > 0:
        alu_loop = f"""
        // {INT_OPS} integer operation(s)
        for (int k = 0; k < INT_OPS; ++k) {{
            int idx = base + k;
            C[idx] = A[idx] + B[idx];
        }}"""

    fpu_loop = ""
    if FLOAT_OPS > 0:
        fpu_loop = f"""
        // {FLOAT_OPS} float operation(s)
        for (int k = INT_OPS; k < (INT_OPS + FLOAT_OPS); ++k) {{
            int idx = base + k;
            C[idx] = (int)((float)A[idx] + (float)B[idx]);
        }}"""

    loop_content = f"""
    // --- Mixed Vector Addition ({ratio_str}) ---
    int i = 0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {{
        int base = i;
{alu_loop}
{fpu_loop}
    }}"""

    tail_content = f"""
    // Tail handling for leftover elements
    for (; i < N; ++i) {{
        int pos = i % CHUNK;
        if (pos < INT_OPS) {{
            C[i] = A[i] + B[i];
        }} else {{
            C[i] = (int)((float)A[i] + (float)B[i]);
        }}
    }}"""

    # C code template (all % and braces fixed)
    c_template = f"""#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000
#define INT_OPS {INT_OPS}
#define FLOAT_OPS {FLOAT_OPS}
#define CHUNK {CHUNK_SIZE}

int main() {{
    static int A[N], B[N];
    static int C[N];
    clock_t t0, t1;

    srand(0);
    for (int i = 0; i < N; i++) {{
        A[i] = 17000000 + rand() % 83000001;
        B[i] = 17000000 + rand() % 83000001;
    }}

    t0 = clock();
{loop_content}
{tail_content}
    t1 = clock();

    printf("Vector Addition ({ratio_str}) Time = %.6f sec\\n",
        (double)(t1 - t0) / CLOCKS_PER_SEC);

    char fname[128];
    sprintf(fname, "vec_{int_percent}_{float_percent}.txt");

    FILE *fp = fopen(fname, "w");

    fprintf(fp, "time %.6f\\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    for (int i = 0; i < N; i++) {{
        fprintf(fp, "%d\\n", C[i]);
    }}

    fclose(fp);

    printf("%s", fname);

    return 0;
}}
"""

    return c_template, filename


# ---------------- MAIN PROGRAM ---------------- #

if __name__ == "__main__":
    print("Welcome to the C Code Vector Addition Generator!")
    print("This script will generate a C file for a given Integer/Float ratio (X/Y).")

    while True:
        try:
            int_p = int(input("Enter Integer percentage (X%): "))
            float_p = int(input("Enter Float percentage (Y%): "))

            if int_p + float_p != 100:
                print("Error: The percentages must sum to 100.")
                continue

            code, filename = generate_c_code(int_p, float_p)

            with open(filename, "w") as f:
                f.write(code)

            print(f"\nC file generated: {filename}\n")

            choice = input("Generate another ratio? (y/n): ")
            if choice.lower() != 'y':
                break

        except ValueError as e:
            print(f"Invalid input: {e}. Please enter whole numbers.")
        except Exception as e:
            print(f"Unexpected error: {e}")
