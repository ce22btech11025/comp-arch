// mixed_90_10.c
// g2cc -O3 -march=native -mtune=native -funroll-loops -ffast-math \
//     -funsafe-math-optimizations -ftree-vectorize -fopt-info-vec-optimized \
//     -falign-loops=32 dot_product-4.c -o 1.exe
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000
#define CHUNK 40  // 36 int (90%) + 4 float (10%)

int main(void) {
    static int A[N], B[N];
    long long sum_int = 0;
    long long sum_float_conv = 0;
    srand(0);

    for (int i = 0; i < N; ++i) { 
        A[i] = rand()%100; 
        B[i] = rand()%100; 
    }

    clock_t t0 = clock();
    int i = 0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {
        int base = i;
        // 36 integer exact multiplications (ALU)
        for (int k = 0; k < 36; ++k) {
            int idx = base + k;
            sum_int += (long long)A[idx] * B[idx];
        }
        // 4 float conversions (FPU)
        for (int k = 36; k < CHUNK; ++k) {
            int idx = base + k;
            float af = (float)A[idx];
            float bf = (float)B[idx];
            sum_float_conv += (long long)(af * bf);
        }
    }
    for (; i < N; ++i) {
        int pos = i % CHUNK;
        if (pos < 36) sum_int += (long long)A[i] * B[i];
        else {
            float af = (float)A[i];
            float bf = (float)B[i];
            sum_float_conv += (long long)(af * bf);
        }
    }
    long long sum = sum_int + sum_float_conv;
    clock_t t1 = clock();

    printf("Dot product (90%% ALU / 10%% FPU) = %lld\n", sum);
    printf("Time (90/10) = %.6f sec\n", (double)(t1 - t0) / CLOCKS_PER_SEC);
    return 0;
}
