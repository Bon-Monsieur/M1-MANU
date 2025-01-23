#include <iostream>
#include <cmath>
using namespace std;


double rectangular(double a, double b,double (*pFun)(double x),int N){
    // nb de pt = N+1
    // i 0 à N compris
    double h = (b-a)/N;
    double sum = 0;
    for (auto i=0;i<=N;i++){
        double xi = a+(b-a)/N*i;
        double f_xi = (*pFun)(xi);
        sum+=f_xi*h;
    }


    return sum;
}

double trapezoidal(double a, double b,double (*pFun)(double x),int N){
    // nb de pt = N+1
    // i 0 à N compris
    double h = (b-a)/N;
    double sum = 0;
    for (auto i=0;i<=N;i++){
        double xi = a+(b-a)/N*i;
        double xi_p1 = a+(b-a)/N*(i+1);
        double f_xi = (*pFun)(xi);
        double f_xi_p1 = (*pFun)(xi_p1);
        sum+=(f_xi+f_xi_p1)*h/2;
    }


    return sum;
}

double square(double x){
    return x*x;
}



int main(){
    int n = 1000;
    double result_1 = rectangular(0. , 5. ,square, n);
    cout << "Integral of f=square using rectangular rule with n="<< n <<" is : " << result_1 << endl ;
    cout << "Wolfram value: 41.667" << endl;

    double result_2 = trapezoidal(0. , 5. , square, n);
    cout << "Integral of f=square using trapezoidal rule with n="<< n <<" is : " << result_2 << endl ;
    cout << "Wolfram value: 41.667" << endl;

    double result_3 = trapezoidal(0. , 5. , sqrt, n);
    cout << "Integral of f=square using rectangular rule with n="<< n <<" is : " << result_3 << endl ;
    cout << "Wolfram value: 7.436" << endl;

    return 0;
}