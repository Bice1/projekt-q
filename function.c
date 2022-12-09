#include <stdio.h>
#include<math.h>
#include<string.h>
#include <stdlib.h>

void c_g_force(double *gravconst_mata_in, double *All_r_interaction_lisa_in, double *All_modr3a_in, int indexplanet, int n, double *f){
    int idx = 0;
    for(int i=0; i<n-1; ++i){
        if (i == indexplanet){
            continue;
        }
        else{
            f[i] = gravconst_mata_in[i]*All_r_interaction_lisa_in[idx]/All_modr3a_in[i];
            idx += 1;
        }
    }
}
