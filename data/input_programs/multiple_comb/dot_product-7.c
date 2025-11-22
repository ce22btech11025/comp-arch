// int_unroll_scalar.c
// Compile: gcc -O3 dot_product-7.c -o 7.exe

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

int main(void) {
    static int A[N], B[N];
    long long s0=0,s1=0,s2=0,s3=0;
    srand(0);
    for (int i=0;i<N;i++){ A[i]=rand()%100; B[i]=rand()%100; }

    clock_t t0 = clock();
    int i=0;
    for (; i+7 < N; i += 8) {
        s0 += (long long)A[i]   * B[i];
        s1 += (long long)A[i+1] * B[i+1];
        s2 += (long long)A[i+2] * B[i+2];
        s3 += (long long)A[i+3] * B[i+3];
        s0 += (long long)A[i+4] * B[i+4];
        s1 += (long long)A[i+5] * B[i+5];
        s2 += (long long)A[i+6] * B[i+6];
        s3 += (long long)A[i+7] * B[i+7];
    }
    for (; i < N; ++i) s0 += (long long)A[i] * B[i];
    long long sum = s0 + s1 + s2 + s3;
    clock_t t1 = clock();
    printf("Dot product (int-unroll) = %lld\n", sum);
    printf("Time (int-unroll) = %.6f sec\n", (double)(t1 - t0)/CLOCKS_PER_SEC);
    return 0;
}
