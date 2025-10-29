#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 1024
#define K 5

int main() {
    static int signal[N], kernel[K], output[N];
    clock_t start, end;
    double cpu_time_used;

    for (int i = 0; i < N; i++)
        signal[i] = i % 256;
    for (int i = 0; i < K; i++)
        kernel[i] = 1;

    start = clock();

    for (int i = 0; i < N; i++) {
        int sum = 0;
        int *sig_ptr = &signal[i];
        int *ker_ptr = kernel;
        for (int j = 0; j < K && (i - j) >= 0; j++)
            sum += sig_ptr[-j] * ker_ptr[j];
        output[i] = sum;
    }

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Optimized Convolution completed in %f seconds\n", cpu_time_used);
    printf("Sample output: %d\n", output[N/2]);
    return 0;
}
