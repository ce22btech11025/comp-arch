// int_simd.c
// Compile: gcc -O3 -march=native -mavx2 -mfma dot_product-5.c -o 5.exe

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <immintrin.h>

#define N 10000000

int main(void) {
    static int A[N], B[N];
    long long sum = 0;
    srand(0);

    for (int i = 0; i < N; ++i) { A[i] = rand()%100; B[i] = rand()%100; }

    clock_t t0 = clock();

    int i = 0;
    for (; i + 7 < N; i += 8) {
        __m256i va = _mm256_loadu_si256((__m256i const*)&A[i]);
        __m256i vb = _mm256_loadu_si256((__m256i const*)&B[i]);
        __m256i prod = _mm256_mullo_epi32(va, vb);
        int tmp[8];
        _mm256_storeu_si256((__m256i*)tmp, prod);
        sum += (long long)tmp[0] + tmp[1] + tmp[2] + tmp[3]
             + (long long)tmp[4] + tmp[5] + tmp[6] + tmp[7];
    }
    for (; i < N; ++i) sum += (long long)A[i] * B[i];

    clock_t t1 = clock();
    printf("Dot product (int-SIMD) = %lld\n", sum);
    printf("Time (int-SIMD) = %.6f sec\n", (double)(t1 - t0)/CLOCKS_PER_SEC);
    return 0;
}
