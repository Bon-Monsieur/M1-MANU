#include <iostream>
#include <cmath>
#include <iomanip>      // std::setprecision


using namespace std;

// Question 1
double expTaylor(double x, int N){
    double res = 1; // Variable de la somme 
    double temp = x;
    int m = 0;
    while (temp>0.25){
        temp/=2;
        m++;
    }
    temp = 1;
    for (int i=1;i<=N;i++){ // Boucle pour calculer x**k/fact(k) rapidement 
        temp*=(x/pow(2,m))/i;
        res += temp;
    }


    return pow(res,pow(2,m));
}


int main(){

    double x = 15;
    int N = 10;

    cout << setprecision(11)<< "Taylor:  approximation de exp(" << x << ") = "<< expTaylor(x,N) << endl;
    cout << exp(x) << endl;
    return 0;

}