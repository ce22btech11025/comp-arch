#include <math.h>
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
    }

    clock_t start = clock();

    for (int i = 0; i < N; i++)
        C[i] = A[i] + B[i];

    clock_t end = clock();
    printf("Execution time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}
