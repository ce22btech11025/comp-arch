#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000
#define INT_OPS 0
#define FLOAT_OPS 40
#define CHUNK 40

int main() {
    static int A[N], B[N];
    static int C[N];
    clock_t t0, t1;

    srand(0);
    for (int i = 0; i < N; i++) {
        A[i] = 17000000 + rand() % 83000001;
        B[i] = 17000000 + rand() % 83000001;
    }

    t0 = clock();

    // --- Mixed Vector Addition (0% Int / 100% Float) ---
    int i = 0;
    for (; i < N; i += 5) {
        C[i] = A[i] + B[i];
        C[i+1] = A[i+1] + B[i+1];
        C[i+2] = A[i+2] + B[i+2];
        C[i+3] = A[i+3] + B[i+3];
        C[i+4] = A[i+4] + B[i+4];
    }

    // Tail handling for leftover elements
    for (; i < N; ++i) {
        C[i] = A[i] + B[i];
    }
    t1 = clock();

    printf("Time taken: %.6f sec\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    return 0;
}
    // char fname[128];
    // sprintf(fname, "vec_0_100.txt");

    // FILE *fp = fopen(fname, "w");

    // fprintf(fp, "time %.6f\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    // for (int i = 0; i < N; i++) {
    //     fprintf(fp, "%d\n", C[i]);
    // }

    // fclose(fp);

    // printf("%s", fname);

    
