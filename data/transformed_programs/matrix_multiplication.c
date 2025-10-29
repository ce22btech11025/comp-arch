#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 512

int main() {
    static int A[N][N], B[N][N], C[N][N];
    srand(0);

    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            A[i][j] = rand() % 10;
            B[i][j] = rand() % 10;
        }

    clock_t start = clock();

    for (int i = 0; i < N; i++)
        for (int k = 0; k < N; k++) {
int r = A[i][k];
            for (int j = 0; j < N; j++)
                C[i][j] += r * B[k][j];
        }

    clock_t end = clock();
    printf("Execution time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}
