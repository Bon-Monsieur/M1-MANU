#include <iostream>
#include <cmath>
#include <iomanip> 
using namespace std;


double f(double x){
    return exp(x) + pow(x,3) - 5;
}

double f_prime(double x){
    return exp(x) + 3*pow(x,2);
}


int main(){
    double x0 = 0;
    double eps = powf(10,-7);
    cout << "eps=" << eps<< endl;

    double x_prev = x0;
    double x_next;
    double temp = x_prev; // variable temporaire permet de stocker la bonne valeur de x_prev pour verifier la condition

    x_next = x_prev - f(x_prev)/f_prime(x_prev); // Premiere itération pour pouvoir tester la condition du while
    int ii=1;
    
    while(abs(temp - x_next)>=eps){
        if (ii==1){
            x_prev = x_next;
        }
        x_next = x_prev - f(x_prev)/f_prime(x_prev);
        temp = x_prev;
        x_prev = x_next;
        
        ii++;
        cout << setprecision(9) <<"i=" << ii << "  x_i=" << x_next << "  f(x_i)=" << f(x_next) << endl;
    }
    
    return 0;
}