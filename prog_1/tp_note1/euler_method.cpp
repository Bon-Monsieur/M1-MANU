#include "euler_method.hpp"
#include <iostream>

using namespace std;

double euler_method( double t_ini, double i_sol, double t_end, double (*sfn)(double t, double x), size_t N){
    double h = (t_end - t_ini)/N;
    
    double x_k = i_sol;
    double t_k;
    for (int kk=1;kk<=N;kk++){
        t_k = t_ini + kk*h;
        x_k = x_k + h*(sfn(t_k,x_k));
    }
    return x_k; // Renvoie toujours le dernier itéré
}