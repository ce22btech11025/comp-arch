#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000
#define INT_OPS 36
#define FLOAT_OPS 4
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

    // --- Mixed Vector Addition (90% Int / 10% Float) ---
    int i = 0;
    for (; i + CHUNK - 1 < N; i += CHUNK) {
        int base = i;

        // 36 integer operation(s)
        for (int k = 0; k < INT_OPS; ++k) {
            int idx = base + k;
            C[idx] = A[idx] + B[idx];
        }

        // 4 float operation(s)
        for (int k = INT_OPS; k < (INT_OPS + FLOAT_OPS); ++k) {
            int idx = base + k;
            C[idx] = (int)((float)A[idx] + (float)B[idx]);
        }
    }

    // Tail handling for leftover elements
    for (; i < N; ++i) {
        int pos = i % CHUNK;
        if (pos < INT_OPS) {
            C[i] = A[i] + B[i];
        } else {
            C[i] = (int)((float)A[i] + (float)B[i]);
        }
    }
    t1 = clock();

    printf("Vector Addition (90% Int / 10% Float) Time = %.6f sec\n",
        (double)(t1 - t0) / CLOCKS_PER_SEC);

    char fname[128];
    sprintf(fname, "vec_90_10.txt");

    FILE *fp = fopen(fname, "w");

    fprintf(fp, "time %.6f\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    for (int i = 0; i < N; i++) {
        fprintf(fp, "%d\n", C[i]);
    }

    fclose(fp);

    printf("%s", fname);

    return 0;
}
