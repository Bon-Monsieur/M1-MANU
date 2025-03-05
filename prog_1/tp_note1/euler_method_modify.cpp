#include "euler_method_modify.hpp"
#include <iostream>

using namespace std;

void euler_method_modify( double t_ini, double i_sol, double t_end, double (*sfn)(double t, double x), size_t N,double* resultat){
    double h = (t_end - t_ini)/N;
    
    double x_k = i_sol;
    double x_kp; // x_k+1
    double t_k;
    resultat[0] = x_k;
    for (int kk=1;kk<=N;kk++){
        t_k = t_ini + kk*h;
        x_kp = x_k + h*(sfn(t_k,x_k)); 
        resultat[kk] = x_kp; // ajout de x_k au tableau
        x_k = x_kp;
    }
}