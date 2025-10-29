#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 200000

void merge(float arr[], int l, int m, int r) {
float n1 = m - l + 1;
float n2 = r - m;
float *L = (int *)malloc(n1 * sizeof(int));
float *R = (int *)malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

void mergeSort(float arr[], int l, int r) {
    if (l < r) {
int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int main() {
    static int arr[N];
    srand(0);
    for (int i = 0; i < N; i++) arr[i] = rand();

    clock_t start = clock();
    mergeSort(arr, 0, N - 1);
    clock_t end = clock();

    printf("Execution time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}
