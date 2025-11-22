#!/usr/bin/env python3
import math
import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def generate_c_code(int_percent, float_percent):
    """
    Generates C code for standard i-j-k matrix multiplication using CHUNK=40.
    For each (i,j), k-loop is chunked into:
       - INT_OPS integer MACs
       - FLOAT_OPS float MACs
    """
    if int_percent + float_percent != 100:
        raise ValueError("Percentages must sum to 100.")

    N = 120                # CHANGED FROM 100 → 120
    CHUNK = 40

    # ratio reduction
    g = gcd(int_percent, float_percent)
    ri = int_percent // g
    rf = float_percent // g
    total = ri + rf

    INT_OPS = (ri * CHUNK) // total
    FLOAT_OPS = CHUNK - INT_OPS

    ratio_str = f"{int_percent}%% Int / {float_percent}%% Float"
    filename = f"matmul_{int_percent}_{float_percent}.c"

    c_template = f"""#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N {N}
#define CHUNK {CHUNK}
#define INT_OPS {INT_OPS}
#define FLOAT_OPS {FLOAT_OPS}

int main() {{
    static int A[N][N], B[N][N], C[N][N];

    srand(0);

    // Initialize matrices with random numbers 4100-4200
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {{
            A[i][j] = 4100 + rand() % 101;
            B[i][j] = 4100 + rand() % 101;
            C[i][j] = 0;
        }}

    clock_t t0 = clock();

    // i-j-k with chunked mixed INT/FLOAT k-loop
    for (int i = 0; i < N; i++) {{
        for (int j = 0; j < N; j++) {{

            for (int k = 0; k < N; k += CHUNK) {{
                int base = k;

                // integer part (NO IF inside loop)
                for (int t = 0; t < INT_OPS; t++) {{
                    int kk = base + t;
                    C[i][j] += A[i][kk] * B[kk][j];
                }}

                // float part (NO IF inside loop)
                for (int t = INT_OPS; t < CHUNK; t++) {{
                    int kk = base + t;
                    C[i][j] += (int)((float)A[i][kk] * (float)B[kk][j]);
                }}
            }}

        }}
    }}

    clock_t t1 = clock();

    printf("Matrix Multiplication ({ratio_str}) completed in %.6f sec\\n",
           (double)(t1 - t0) / CLOCKS_PER_SEC);
    
    return 0;
}}
"""
    return c_template, filename


def main():
    if len(sys.argv) == 3:
        ip = int(sys.argv[1])
        fp = int(sys.argv[2])
    else:
        print("Matrix Multiplication Generator (CHUNK=40 mixed ops)")
        ip = int(input("Enter Integer percentage: "))
        fp = int(input("Enter Float percentage: "))

    code, filename = generate_c_code(ip, fp)
    with open(filename, "w") as f:
        f.write(code)
    print("Generated:", filename)


if __name__ == "__main__":
    main()
