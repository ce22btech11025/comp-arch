// mixed_50_50.c
// 50% ALU (int * int) + 50% FPU (float * float)
// Scalar-only code, no SIMD intrinsics.
// gcc -O3 -march=native dot_product-10.c -o 10.exe

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000
#define CHUNK 40   // 20 int ops + 20 float ops

int main(void) {
    static int A[N], B[N];
    long long sum_int = 0;
    long long sum_float_conv = 0;

    srand(0);

    // Initialize data
    for (int i = 0; i < N; ++i) {
        A[i] = rand() % 100;
        B[i] = rand() % 100;
    }

    clock_t t0 = clock();

    int i = 0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {
        int base = i;

        // ---------------------------
        // 20 ALU-heavy integer ops
        // ---------------------------
        for (int k = 0; k < 20; ++k) {
            int idx = base + k;
            sum_int += (long long)A[idx] * B[idx];
        }

        // ---------------------------
        // 20 FPU-heavy float ops
        // ---------------------------
        for (int k = 20; k < CHUNK; ++k) {
            int idx = base + k;
            float af = (float)A[idx];
            float bf = (float)B[idx];
            sum_float_conv += (long long)(af * bf);  // truncation
        }
    }

    // Tail loop (same ratio)
    for (; i < N; ++i) {
        int pos = i % CHUNK;

        if (pos < 20) {
            sum_int += (long long)A[i] * B[i];
        } else {
            float af = (float)A[i];
            float bf = (float)B[i];
            sum_float_conv += (long long)(af * bf);
        }
    }

    long long sum = sum_int + sum_float_conv;

    clock_t t1 = clock();

    printf("Dot product (50%% ALU / 50%% FPU) = %lld\n", sum);
    printf("Time (50/50) = %.6f sec\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    return 0;
}
