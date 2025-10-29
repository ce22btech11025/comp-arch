#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 1000000

int main() {
    static int A[N], B[N];
    long long dot = 0;
    clock_t start, end;
    double cpu_time_used;

    for (int i = 0; i < N; i++) {
        A[i] = i % 100;
        B[i] = (N - i) % 100;
    }

    start = clock();
    long long temp1 = 0, temp2 = 0, temp3 = 0, temp4 = 0;
    int i;
    for (i = 0; i < N - 3; i += 4) {
        temp1 += A[i] * B[i];
        temp2 += A[i + 1] * B[i + 1];
        temp3 += A[i + 2] * B[i + 2];
        temp4 += A[i + 3] * B[i + 3];
    }
    for (; i < N; i++)
        dot += A[i] * B[i];
    dot += temp1 + temp2 + temp3 + temp4;

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Optimized Dot Product = %lld, computed in %f seconds\n", dot, cpu_time_used);
    return 0;
}
