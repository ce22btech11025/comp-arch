#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define INPUT_SIZE 1024
#define KERNEL_SIZE 5

int main() {
    static int input[INPUT_SIZE];
    static int kernel[KERNEL_SIZE];
    static int output[INPUT_SIZE - KERNEL_SIZE + 1];

    srand(0);
    for (int i = 0; i < INPUT_SIZE; i++) input[i] = rand() % 10;
    for (int i = 0; i < KERNEL_SIZE; i++) kernel[i] = rand() % 5;

    clock_t start = clock();
    for (int i = 0; i < INPUT_SIZE - KERNEL_SIZE + 1; i++) {
float sum = 0;
        for (int j = 0; j < KERNEL_SIZE; j++)
            sum += input[i + j] * kernel[j];
        output[i] = sum;
    }
    clock_t end = clock();

    printf("Execution time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}
