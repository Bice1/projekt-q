#include <stdio.h>
#include<math.h>
#include<string.h>
#include <stdlib.h>
const double daysec = 24.0*60*60;
const double G = 6.67e-11;
int a = 8;
int dt = 1;
int tsimu = 20;

void Compute_force_G_on_a(double* gravconst_mata, double All_r_interaction_lisa[][a-1], double All_modr3a[][a-1],int indexplanet, double* fx_a, double*fy_a, double*fz_a,int a){

    for (int i=0 ; i<a-1; ++i){
        if (i == indexplanet) {
            continue;
        }
        else{
            fx_a[i] = gravconst_mata[i]*All_r_interaction_lisa[i][0]/All_modr3a[i][0];
            fy_a[i] = gravconst_mata[i]*All_r_interaction_lisa[i][1]/All_modr3a[i][1];
            fz_a[i] = gravconst_mata[i]*All_r_interaction_lisa[i][2]/All_modr3a[i][2];

        }
    }

}

double sum(double *fx){
    double somme = 0.0;
    for (int i=0 ; i<sizeof(fx); ++i){
        somme += fx[i];
    }
    return somme;
}

int simu(float dtincr, int tsimu, int a){
    

    double * Mass_list = malloc(100*sizeof(double));
    double * ap_v_y = malloc(100*sizeof(double));
    double * ap_v_z = malloc(100*sizeof(double));
    double * orbit_diameter = malloc(100*sizeof(double));
    double * All_x = malloc(10000000*sizeof(double));
    double * All_y = malloc(10000000*sizeof(double));
    double * All_z = malloc(10000000*sizeof(double));
    double * All_vx = malloc(10000000*sizeof(double));
    double * All_vy = malloc(10000000*sizeof(double));
    double * All_vz = malloc(10000000*sizeof(double));
    double * All_save_x = malloc(10000000*sizeof(double));
    double * All_save_y = malloc(10000000*sizeof(double));
    double * All_save_z = malloc(10000000*sizeof(double));
    double fx[a-1];
    double fy[a-1];
    double fz[a-1];
    double ** Gravconst_mat = malloc(1000*sizeof(double));
    for (int i= 0 ; i<a-1 ;++i){
        for (int j = 0 ; j < a-1 ; ++j){
            if (i == j){
                continue;
            }
            else
            {
                Gravconst_mat[i][j] = Mass_list[i]*Mass_list[j]*G;
            }
        }
    }
    
    


    double * planetes = malloc(10000 * sizeof (double));
    double All_r_interaction_list[a-1][a-1];
    double All_modr3[a-1][a-1];
    for (int i = 0; i<a-1 ; ++i){
        All_x[i] = orbit_diameter[i];
        All_y[i] = 0;
        All_z[i] = 0;
        All_vx[i] = 0;
        All_vy[i] = ap_v_y[i];
        All_vz[i] = ap_v_z[i];
    }
    for(int i=0 ; i<a-1; ++i){
        All_save_x[i] = All_x[i];
        All_save_x[i] = All_x[i];
        All_save_x[i] = All_x[i];
    }
    double t= 0.0;
    double dt = dtincr*daysec;


    while (t<tsimu*365*daysec){
        for(int i = 0; i <a-1; ++i){
            for (int j = i+1 ; j < a-1; ++j){
                double rx = All_x[j]-All_x[i];
                double ry = All_y[j]-All_y[i];
                double rz = All_z[j]-All_z[i];
                All_r_interaction_list[j][i]= -rx;
                All_r_interaction_list[j][i]= -ry;
                All_r_interaction_list[j][i]= -rz;
                All_modr3[i][j]=pow((pow(rx,2)+pow(ry,2)+pow(rz,2)),1.5);
                All_modr3[j][i]=All_modr3[i][j];
            }
        }
        for(int i = 0; i<a-1; ++i){
            Compute_force_G_on_a(Gravconst_mat[i], All_r_interaction_list,All_modr3, i, fx, fy, fz, a);
            All_vx[i] += sum(fx)*dt/Mass_list[i];
            All_vy[i] += sum(fy)*dt/Mass_list[i];
            All_vz[i] += sum(fz)*dt/Mass_list[i];
            All_x[i]+=All_vx[i]*dt;
            All_y[i]+=All_vy[i]*dt;
            All_z[i]+=All_vz[i]*dt;
            All_save_x[i] = All_x[i];
            All_save_y[i] = All_y[i];
            All_save_z[i] = All_z[i];
        }
    t += dt;
    }

    free(Mass_list);
    free(ap_v_y);
    free(ap_v_z);
    free(orbit_diameter);
    free(All_x);
    free(All_y);
    free(All_z);
    free(All_vx);
    free(All_vy);
    free(All_vz);
    free(All_save_x);
    free(All_save_y);
    free(All_save_z);
    free(fx);
    free(fy);
    free(fz);
    free(Gravconst_mat);

    FILE *f=fopen("All_save_x.csv","w");
    for (int i=0; i<sizeof(All_save_x); i++)
    {
        fprintf(f,"%f\n", All_save_x[i]);
    }
    fclose(f);

    FILE *g=fopen("All_save_y.csv","w");
    for (int i=0; i<sizeof(All_save_y); i++)
    {
        fprintf(g,"%f\n", All_save_y[i]);
    }
    fclose(g);

    FILE *h=fopen("All_save_z.csv","w");
    for (int i=0; i<sizeof(All_save_z); i++)
    {
        fprintf(h,"%f\n", All_save_z[i]);
    }
    fclose(h);
    return 0;
}
int main(){
    simu(1,20,8,);
    return 0;
}