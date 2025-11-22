// float_simd.c
// Compile: gcc -O3 -march=native -mavx2 -mfma dot_product-6.c -o 6.exe

#pragma GCC target("avx2,fma")
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <immintrin.h>

#define N 10000000

int main(void) {
    static float A[N], B[N];
    double sum = 0.0;
    srand(0);

    for (int i = 0; i < N; ++i) { A[i] = (float)(rand()%100); B[i] = (float)(rand()%100); }

    clock_t t0 = clock();

    int i = 0;
    __m256 vsum = _mm256_setzero_ps();
    for (; i + 7 < N; i += 8) {
        __m256 a = _mm256_loadu_ps(&A[i]);
        __m256 b = _mm256_loadu_ps(&B[i]);
        vsum = _mm256_fmadd_ps(a, b, vsum);
    }
    float tmp[8];
    _mm256_storeu_ps(tmp, vsum);
    for (int k = 0; k < 8; ++k) sum += tmp[k];
    for (; i < N; ++i) sum += (double)A[i] * (double)B[i];

    clock_t t1 = clock();
    printf("Dot product (float-SIMD ~) = %.0f\n", sum);
    printf("Time (float-SIMD) = %.6f sec\n", (double)(t1 - t0)/CLOCKS_PER_SEC);
    return 0;
}
