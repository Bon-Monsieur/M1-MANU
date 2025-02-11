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
    double x_prev = x0;
    double x_next;

    for (auto ii=1;ii<100;ii++){
        x_next = x_prev - f(x_prev)/f_prime(x_prev);
        x_prev = x_next;
        cout << setprecision(9) <<"i=" << ii << "  x_i=" << x_next << "  f(x_i)=" << f(x_next) <<endl;
    }
    cout << setprecision(9) << "x_100=" << x_next;
    
    return 0;
}