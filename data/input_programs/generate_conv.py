#!/usr/bin/env python3
import math
import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def generate_c_code(int_percent, float_percent):
    """
    Generates a C program for 1D convolution with INT/FLOAT mixed ops.
    Uses forward indexing: input[i + j] * kernel[j].
    Kernel size K=40, split into INT_OPS / FLOAT_OPS.
    """
    if int_percent + float_percent != 100:
        raise ValueError("Percentages must sum to 100.")

    common_divisor = gcd(int_percent, float_percent)
    ratio_int = int_percent // common_divisor
    ratio_float = float_percent // common_divisor

    CHUNK = 40
    K = 40
    total_ratio = ratio_int + ratio_float

    INT_OPS = (ratio_int * CHUNK) // total_ratio
    FLOAT_OPS = CHUNK - INT_OPS
    if INT_OPS == 0 and int_percent > 0:
        INT_OPS = 1
        FLOAT_OPS = CHUNK - INT_OPS

    ratio_str = f"{int_percent}%% Int / {float_percent}%% Float"
    filename = f"conv_{int_percent}_{float_percent}.c"

    c_template = f"""#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define INPUT_SIZE 1024
#define KERNEL_SIZE {K}
#define INT_OPS {INT_OPS}
#define FLOAT_OPS {FLOAT_OPS}

int main() {{
    static int input[INPUT_SIZE];
    static int kernel[KERNEL_SIZE];
    static int output[INPUT_SIZE - KERNEL_SIZE + 1];

    srand(0);
    for (int i = 0; i < INPUT_SIZE; i++) input[i] = rand() % 10;
    for (int i = 0; i < KERNEL_SIZE; i++) kernel[i] = rand() % 5;

    clock_t t0 = clock();

    for (int i = 0; i < INPUT_SIZE - KERNEL_SIZE + 1; i++) {{
        int sum = 0;

        int int_end = INT_OPS;
        if (int_end > KERNEL_SIZE) int_end = KERNEL_SIZE;

        /* Integer MACs */
        for (int j = 0; j < int_end; j++)
            sum += input[i + j] * kernel[j];

        /* Float MACs */
        for (int j = int_end; j < KERNEL_SIZE; j++)
            sum += (int)((float)input[i + j] * (float)kernel[j]);

        output[i] = sum;
    }}

    clock_t t1 = clock();

    printf("Convolution Mixed Ops ({ratio_str}) completed in %.6f sec\\n",
           (double)(t1 - t0) / CLOCKS_PER_SEC);

    return 0;
}}
"""
    return c_template, filename

def main():
    if len(sys.argv) == 3:
        int_p = int(sys.argv[1])
        float_p = int(sys.argv[2])
    else:
        print("Mixed INT/FLOAT Convolution C Code Generator (K=40, forward indexing)")
        int_p = int(input("Enter Integer percentage (%): ").strip())
        float_p = int(input("Enter Float percentage (%): ").strip())

    code, filename = generate_c_code(int_p, float_p)
    with open(filename, "w") as f:
        f.write(code)
    print(f"C file generated: {filename}")

if __name__ == '__main__':
    main()
