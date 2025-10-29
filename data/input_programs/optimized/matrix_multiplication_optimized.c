#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 256
#define BLOCK 32

int main() {
    static int A[N][N], B[N][N], C[N][N];
    clock_t start, end;
    double cpu_time_used;

    // Initialize matrices
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            A[i][j] = i + j;
            B[i][j] = i - j;
            C[i][j] = 0;
        }

    start = clock();

    // Blocked matrix multiplication for better cache use
    for (int i = 0; i < N; i += BLOCK)
        for (int j = 0; j < N; j += BLOCK)
            for (int k = 0; k < N; k += BLOCK)
                for (int ii = i; ii < i + BLOCK && ii < N; ii++)
                    for (int jj = j; jj < j + BLOCK && jj < N; jj++) {
                        int sum = C[ii][jj];
                        for (int kk = k; kk < k + BLOCK && kk < N; kk++)
                            sum += A[ii][kk] * B[kk][jj];
                        C[ii][jj] = sum;
                    }

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Optimized Matrix Multiplication completed in %f seconds\n", cpu_time_used);
    printf("Sample result: %d\n", C[N/2][N/2]);
    return 0;
}
