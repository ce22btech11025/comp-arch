// int_dot_normal.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

int main(void) {
    static int A[N], B[N];
    long long sum = 0;

    srand(0);

    for (int i = 0; i < N; i++) {
        A[i] = rand() % 100;
        B[i] = rand() % 100;
    }

    clock_t t0 = clock();

    for (int i = 0; i < N; i++)
        sum += (long long)A[i] * B[i];

    clock_t t1 = clock();

    printf("Dot product (int-normal) = %lld\n", sum);
    printf("Time (int-normal) = %.6f sec\n",
           (double)(t1 - t0) / CLOCKS_PER_SEC);

    return 0;
}
