// unrolled_80_20.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

int main() {
    static int A[N], B[N], C[N];
    srand(0);

    for (int i = 0; i < N; i++) {
        A[i] = rand() % 100;
        B[i] = rand() % 100;
        C[i] = 0;
    }

    const int CHUNK = 40;

    clock_t start = clock();

    int i = 0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {
        for (int k = 0; k < 32; k++)
            C[i + k] += A[i + k] * B[i + k];

        for (int k = 32; k < 40; k++)
            C[i + k] += (int)((float)A[i + k] * (float)B[i + k]);
    }

    for (; i < N; i++) {
        if ((i % CHUNK) < 32) C[i] += A[i] * B[i];
        else C[i] += (int)((float)A[i] * (float)B[i]);
    }

    clock_t end = clock();
    printf("Time = %.6f sec\n", (double)(end - start) / CLOCKS_PER_SEC);

    return 0;
}
