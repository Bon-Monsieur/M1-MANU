#include "class_integral.hpp"
#include <cmath>
using namespace std;
#define M_PI 3.14159265358979323846

double square(double x){
    return x*x;
}

double mycos(double x){
    return cos(x);
}


int main(){
    
    double a = 0.;
    double b = 5.;
    double (*f)(double x); // déclaration pointeur de fonction
    f = &square; 
    Integral integral_1(a,b,f);

    int N = 100;
    double result_1 = integral_1.rectangular(N);
    cout << "Integral["<<a<<"," << b <<"] of f=x^2 using rectangular rule with n="<< N <<" is : " << result_1 << endl ;
    cout << "Wolfram value: 41.667" << endl;

    double result_2 = integral_1.trapezoidal(N);
    cout << "Integral["<<a<<"," << b <<"] of f=x^2 using trapezoidal rule with n="<< N <<" is : " << result_2 << endl ;
    cout << "Wolfram value: 41.667" << endl;

    
    // Nouvel objet pour changer f:
    
    double c=0.;
    double d=M_PI*2;
    f = &mycos;
    Integral integral_2(c,d,f);

    double result_3 = integral_2.rectangular(N);
    cout << "Integral["<<c<<"," << d <<"] of f=x^2 using rectangular rule with n="<< N <<" is : " << result_3 << endl ;
    cout << "Wolfram value: 0" << endl;

    double result_4 = integral_2.trapezoidal(N);
    cout << "Integral["<<c<<"," << d <<"] of f=x^2 using trapezoidal rule with n="<< N <<" is : " << result_4 << endl ;
    cout << "Wolfram value: 0" << endl;
    
    
    
    return 0;
}