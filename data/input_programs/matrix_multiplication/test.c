#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 120

int main() {
    static int A[N][N], B[N][N], C[N][N];

    srand(0);

    // initialize matrices
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            A[i][j] = 4100 + rand() % 101;
            B[i][j] = 4100 + rand() % 101;
            C[i][j] = 0;
        }

    clock_t t0 = clock();

    // matrix multiplication (golden reference)
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                C[i][j] += A[i][k] * B[k][j];

    clock_t t1 = clock();

    double time_sec = (double)(t1 - t0) / CLOCKS_PER_SEC;

    // write output to txt file
    FILE *fp = fopen("baseline_output.txt", "w");
    if (!fp) return 1;

    fprintf(fp, "time %.6f\n", time_sec);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++)
            fprintf(fp, "%d ", C[i][j]);
        fprintf(fp, "\n");
    }

    fclose(fp);

    printf("Baseline matrix saved to baseline_output.txt\n");

    return 0;
}
