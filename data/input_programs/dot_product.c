#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

int main() {
    static int A[N], B[N];
    long long sum = 0;
    srand(0);

    for (int i = 0; i < N; i++) {
        A[i] = rand() % 100;
        B[i] = rand() % 100;
    }

    clock_t start = clock();

    for (int i = 0; i < N; i++)
        sum += (long long)A[i] * B[i];

    clock_t end = clock();
    printf("Dot product: %lld\n", sum);
    printf("Execution time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}
