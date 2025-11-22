// mixed_unroll_simd.c
// Compile: gcc -O3 -march=native -mavx2 -mfma dot_product-9.c -o 9.exe

#pragma GCC target("avx2,fma")
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <immintrin.h>

#define N 10000000
#define CHUNK 40

int main(void) {
    static int A[N], B[N];
    long long sum = 0;
    srand(0);
    for (int i=0;i<N;i++){ A[i]=rand()%100; B[i]=rand()%100; }

    clock_t t0 = clock();

    int i = 0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {
        int base = i;
        // --- 24 integer elements: 3 x 8-lane integer SIMD ---
        for (int block = 0; block < 3; ++block) {
            int idx = base + block*8;
            __m256i va = _mm256_loadu_si256((__m256i const*)&A[idx]);
            __m256i vb = _mm256_loadu_si256((__m256i const*)&B[idx]);
            __m256i prod = _mm256_mullo_epi32(va, vb);
            int tmp[8];
            _mm256_storeu_si256((__m256i*)tmp, prod);
            sum += (long long)tmp[0] + tmp[1] + tmp[2] + tmp[3]
                 + (long long)tmp[4] + tmp[5] + tmp[6] + tmp[7];
        }
        // --- 16 float elements: 2 x 8-lane float SIMD (int->float multiply -> float->int conv) ---
        for (int block = 0; block < 2; ++block) {
            int idx = base + 24 + block*8;
            __m256i ai = _mm256_loadu_si256((__m256i const*)&A[idx]);
            __m256i bi = _mm256_loadu_si256((__m256i const*)&B[idx]);
            __m256 af = _mm256_cvtepi32_ps(ai);
            __m256 bf = _mm256_cvtepi32_ps(bi);
            __m256 prodf = _mm256_mul_ps(af, bf);      // or _mm256_fmadd_ps(af,bf,zero)
            __m256i prod_i = _mm256_cvttps_epi32(prodf); // float->int (trunc)
            int tmp[8];
            _mm256_storeu_si256((__m256i*)tmp, prod_i);
            sum += (long long)tmp[0] + tmp[1] + tmp[2] + tmp[3]
                 + (long long)tmp[4] + tmp[5] + tmp[6] + tmp[7];
        }
    }

    // tail - follow same CHUNK rule
    for (; i < N; ++i) {
        int pos = i % CHUNK;
        if (pos < 24) sum += (long long)A[i] * B[i];
        else {
            float af = (float)A[i];
            float bf = (float)B[i];
            sum += (long long)(af * bf);
        }
    }

    clock_t t1 = clock();
    printf("Dot product (mixed-unroll-SIMD) = %lld\n", sum);
    printf("Time (mixed-unroll-SIMD) = %.6f sec\n", (double)(t1 - t0)/CLOCKS_PER_SEC);
    return 0;
}
