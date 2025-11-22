// float_dot_normal.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

int main(void) {
    static float A[N], B[N];
    double sum = 0.0;

    srand(0);

    for (int i = 0; i < N; i++) {
        A[i] = (float)(rand() % 100);
        B[i] = (float)(rand() % 100);
    }

    clock_t t0 = clock();

    for (int i = 0; i < N; i++)
        sum += (double)(A[i] * B[i]);

    clock_t t1 = clock();

    printf("Dot product (float-normal) = %.0f\n", sum);
    printf("Time (float-normal) = %.6f sec\n",
           (double)(t1 - t0) / CLOCKS_PER_SEC);

    return 0;
}
