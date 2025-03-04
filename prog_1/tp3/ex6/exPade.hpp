#include <iostream>
#include <cmath>
#include "../ex5/binomial.hpp"
#pragma once 


template<int N=5,typename T>
T exPade(T x);

template<int N=5,typename T>
T PN(T x);

double factorial(int n);

// ===========================


template<int N,typename T>
T exPade(T x){
    int m = 0;
    T temp = x;
    
    // Calcul de m
    while (temp>0.25){
        temp/=2;
        m++;
    }  
    
    T res = PN<N,T>(x/pow(2,m))/PN<N,T>(-x/pow(2,m));
    return pow(res,pow(2,m));
}

template<int N,typename T>
T PN(T x){
    Binomial<2*N> B;
    T sum{0};
    for (int n=0;n<=N;n++){
        
        sum+= B(N,n)/(factorial(n)*B(2*N,n))*pow(x,n);
    }
    return sum;
}


double factorial(int n) {
    if (n == 0 || n == 1) return 1;
    double res = 1;
    for (int i = 2; i <= n; i++) {
        res *= i;
    }
    return res;
}