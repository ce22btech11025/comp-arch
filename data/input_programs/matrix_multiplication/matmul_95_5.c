#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 120
#define CHUNK 40
#define INT_OPS 38
#define FLOAT_OPS 2

int main() {
    static int A[N][N], B[N][N], C[N][N];

    srand(0);

    // Initialize matrices with random numbers 4100-4200
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            A[i][j] = 4100 + rand() % 101;
            B[i][j] = 4100 + rand() % 101;
            C[i][j] = 0;
        }

    clock_t t0 = clock();

    // i-j-k with chunked mixed INT/FLOAT k-loop
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {

            for (int k = 0; k < N; k += CHUNK) {
                int base = k;

                // integer part (NO IF inside loop)
                for (int t = 0; t < INT_OPS; t++) {
                    int kk = base + t;
                    C[i][j] += A[i][kk] * B[kk][j];
                }

                // float part (NO IF inside loop)
                for (int t = INT_OPS; t < CHUNK; t++) {
                    int kk = base + t;
                    C[i][j] += (int)((float)A[i][kk] * (float)B[kk][j]);
                }
            }

        }
    }

    clock_t t1 = clock();

    printf("Matrix Multiplication (95%% Int / 5%% Float) completed in %.6f sec\n",
           (double)(t1 - t0) / CLOCKS_PER_SEC);
    // write output to txt
    char fname[64];
    sprintf(fname, "out_%s.txt", "int95float5");   // change name per file

    FILE *fp = fopen(fname, "w");
    fprintf(fp, "time %.6f\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++)
            fprintf(fp, "%d ", C[i][j]);
        fprintf(fp, "\n");
    }
    fclose(fp);

    return 0;
}
