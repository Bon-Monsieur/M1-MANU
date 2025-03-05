#include <iostream>
#include <cmath>
#include <iomanip> 
using namespace std;

// f(x)
double f(double x){
    return exp(x) + pow(x,3) - 5;
}
// f'(x)
double f_prime(double x){
    return exp(x) + 3*pow(x,2);
}


int main(){
    double x0 = 0;
    double* resultat = new double[100];
    resultat[0]=x0;

    for (auto ii=1;ii<100;ii++){
        resultat[ii] = resultat[ii-1]- f(resultat[ii-1])/f_prime(resultat[ii-1]);
        cout << setprecision(9) <<"i=" << ii << "  x_i=" << resultat[ii] << "  f(x_i)="<<f(resultat[ii]) << endl;
    }
    cout << setprecision(9) << "x_100=" << resultat[99];

    delete[] resultat;
    return 0;
}