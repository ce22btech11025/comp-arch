// mixed_unroll_native.c
// Compile: gcc -O3 -march=native dot_product-8.c -o 8.exe

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000
#define CHUNK 40   // 24 int (60%) + 16 float (40%)

int main(void) {
    static int A[N], B[N];
    long long sum_int = 0;
    long long sum_float_conv = 0;
    srand(0);
    for (int i=0;i<N;i++){ 
        A[i]=rand()%100; 
        B[i]=rand()%100; 
    }

    clock_t t0 = clock();
    int i=0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {
        int base = i;
        // 24 integer exact multiplications
        for (int k = 0; k < 24; ++k) {
            int idx = base + k;
            sum_int += (long long)A[idx] * B[idx];
        }
        // 16 float-conversion multiplications
        for (int k = 24; k < CHUNK; ++k) {
            int idx = base + k;
            sum_float_conv += (long long)((float)A[idx] * (float)B[idx]);
        }
    }
    for (; i < N; ++i) {
        int pos = i % CHUNK;
        if (pos < 24) sum_int += (long long)A[i] * B[i];
        else          sum_float_conv += (long long)((float)A[i] * (float)B[i]);
    }
    long long sum = sum_int + sum_float_conv;
    clock_t t1 = clock();
    printf("Dot product (60%% ALU / 40%% FPU) = %lld\n", sum);
    printf("Time (60/40) = %.6f sec\n", (double)(t1 - t0) / CLOCKS_PER_SEC);
    return 0;
}
