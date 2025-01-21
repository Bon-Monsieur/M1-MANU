#include <iostream>
#include <cmath>
using namespace std;

double factorial(int n) {
    if (n == 0 || n == 1) return 1;
    double res = 1;
    for (int i = 2; i <= n; i++) {
        res *= i;
    }
    return res;
}

double coefBinom(double n,double k){ // Donne la valeur du coefficient binomial
    double res;
    res = factorial(n)/factorial(k)/factorial(n-k);
    //cout <<  res;
    return res;
}

double PN(double x, int N){ // Calcul de chaque polynôme PN
    double sum = 0;
    for (int n=0;n<=N;n++){
        sum+= coefBinom(N,n)/(factorial(n)*coefBinom(2*N,n))*pow(x,n);
    }
    return sum;
}

double expPade(double x,int N){
    int m = 0;
    double temp = x;
    
    // Calcul de m
    while (temp>0.25){
        temp/=2;
        m++;
    }  
    
    double res = PN(x/pow(2,m),N)/PN(-x/pow(2,m),N);
    return pow(res,pow(2,m));
}


int main(){

    double x = 0.14;
    int N = 5;

    cout <<"res "<< expPade(x,N) << endl;
    return 0;
}