#include <stdio.h>
#include <time.h>

#define N 200000000   /* Adjust if too slow */

double now_sec() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main() {

    volatile int xi = 1;       /* integer dependency chain */
    volatile float xf = 1.0f;  /* float dependency chain */

    double t0, t1;

    /* ------------------------------
       Test 1: INT ONLY (ALU load)
       ------------------------------ */
    xi = 1;
    t0 = now_sec();
    for (long i = 0; i < N; i++) {
        xi = xi * 3 + 1;   /* heavy dependent integer chain */
    }
    t1 = now_sec();
    double t_int = t1 - t0;
    printf("INT only time      = %.6f sec, result xi=%d\n", t_int, xi);


    /* ------------------------------
       Test 2: FLOAT ONLY (FPU load)
       ------------------------------ */
    xf = 1.0f;
    t0 = now_sec();
    for (long i = 0; i < N; i++) {
        xf = xf * 1.000001f;   /* heavy dependent float chain */
    }
    t1 = now_sec();
    double t_float = t1 - t0;
    printf("FLOAT only time    = %.6f sec, result xf=%f\n", t_float, xf);


    /* ------------------------------
       Test 3: MIXED INT + FLOAT
       (perfect test of concurrency)
       ------------------------------ */
    xi = 1;
    xf = 1.0f;

    t0 = now_sec();
    for (long i = 0; i < N; i++) {
        xi = xi * 3 + 1;          /* ALU chain */
        xf = xf * 1.000001f;      /* FPU chain */
    }
    t1 = now_sec();

    double t_mix = t1 - t0;
    printf("MIXED time         = %.6f sec, xi=%d, xf=%f\n", t_mix, xi, xf);


    /* ---------------------------------
       Interpretation
       --------------------------------- */

    printf("\n--- Concurrency Analysis ---\n");

    printf("Expected serial time: %.6f sec\n", t_int + t_float);

    if (t_mix < (t_int + t_float) * 0.8) {
        printf(">>> ALU and FPU executed in parallel (VALID concurrency).\n");
    } else {
        printf(">>> No strong evidence of ALU–FPU overlap.\n");
    }

    return 0;
}
