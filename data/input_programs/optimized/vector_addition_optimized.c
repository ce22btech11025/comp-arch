// #include <stdio.h>
// #include <stdlib.h>
// #include <time.h>

// #define N 1000000

// int main() {
//     static int A[N], B[N], C[N];
//     clock_t start, end;
//     double cpu_time_used;

//     for (int i = 0; i < N; i++) {
//         A[i] = i;
//         B[i] = N - i;
//     }

//     start = clock();
//     int i;
//     for (i = 0; i < N - 3; i += 4) {
//         C[i] = A[i] + B[i];
//         C[i + 1] = A[i + 1] + B[i + 1];
//         C[i + 2] = A[i + 2] + B[i + 2];
//         C[i + 3] = A[i + 3] + B[i + 3];
//         // C[i+4] = (int) A'[i+4] + B'[i+4];
//     }
//     for (; i < N; i++)
//         C[i] = A[i] + B[i];
//     end = clock();

//     cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
//     printf("Optimized Vector Addition completed in %f seconds\n", cpu_time_used);
//     printf("Sample result: %d\n", C[N/2]);
//     return 0;
// }
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 1000000

int main() {
    static int A[N], B[N], C[N];
    clock_t start, end;
    double cpu_time_used;

    for (int i = 0; i < N; i++) {
        A[i] = i;
        B[i] = N - i;
    }

    float fa[N];

    transform(A, A + N, fa, [](int x) { return static_cast<float>(x); });

    start = clock();
    int i;
    for (i = 0; i < N - 3; i += 4) {
        C[i] = A[i] + B[i];
        C[i + 1] = A[i + 1] + B[i + 1];
        C[i + 2] = A[i + 2] + B[i + 2];
        C[i + 3] = A[i + 3] + B[i + 3];
        // C[i+4] = (int) A'[i+4] + B'[i+4];
    }
    for (; i < N; i++)
        C[i] = A[i] + B[i];
    end = clock();

    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Optimized Vector Addition completed in %f seconds\n", cpu_time_used);
    printf("Sample result: %d\n", C[N/2]);
    return 0;
}
