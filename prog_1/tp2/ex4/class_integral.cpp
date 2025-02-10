#include "class_integral.hpp"
using namespace std;

integral::integral(double a, double b, double  (*p_func)(double) ){
    this->a = a;
    this->b = b;
    this->p_func = p_func;
}


void integral::change_bounds(double a, double b){
    this->a = a;
    this->b = b;
}


double integral::trapezoidal(int n) const{
    double h = (b-a)/n;
    double sum = 0;
    for (auto i=0;i<=n;i++){
        double xi = a+(b-a)/n*i;
        double xi_p1 = a+(b-a)/n*(i+1);
        double f_xi = (p_func)(xi);
        double f_xi_p1 = (p_func)(xi_p1);
        sum+=(f_xi+f_xi_p1)*h/2;
    }
    return sum;
}


double integral::rectangular(int n) const {
    // nb de pt = N+1
    // i 0 à N compris
    double h = (b-a)/n;
    double sum = 0;
    for (auto i=0;i<=n;i++){
        double xi = a+(b-a)/n*i;
        double f_xi = (p_func)(xi);
        sum+=f_xi*h;
    }
}
