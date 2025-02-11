#include "euler_method_modify.hpp"
#include "euler_method.hpp"
#include <iostream>
#include <cmath>
using namespace std;


double f(double t, double x){
    return (1-exp(t))*x/(1+exp(t));
}

double x(double t){
    return 12*exp(t)/(pow((1+exp(t)),2));
}

// Affiche un tableau
void afficherTableau(double* tab, int n){
    cout << "["; 
    for (int ii=0;ii<n-1;ii++){
        cout << tab[ii] << ",";
    }
    cout << tab[n-1] << "]" << endl;
}

// Fonction qui affiche l'erreur numerique
double numerical_error(double t_ini,double t_end,size_t N,double* resultat, double x_0){
    double h = (t_end - t_ini)/N;
    double t_k;
    double sum = abs(x(t_ini) - x_0 );
    for (int kk=1;kk<N+1;kk++){
        t_k = t_ini + kk*h;
        sum += abs(x(t_k)-resultat[kk]); // resultat[kk] correspond donc à x_k
    }
    return sum;
}
    

int main(){
    size_t N = 100;
    double t_0 = 0;
    double T = 2;
    double x_0 = 3;
    double (*p_func)(double t,double x) = &f; 

    double* resultat = new double[N]; // Tableau qui stocke les N valeurs retournées par la méthode
    euler_method_modify(t_0,x_0,T,p_func,N,resultat); // modifie directement le tableau resultat avec la methode de euler_method_modify.cpp
    afficherTableau(resultat,N);
    double err = numerical_error(t_0,T,N,resultat,x_0);
    cout << "erreur numerique:" << err << endl;
    return 0;
}