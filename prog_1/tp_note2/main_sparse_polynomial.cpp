#include "sparse_polynomial.hpp"
#include <iostream>
#include <cmath>


int main(){

    size_t n = 2;
    pair<double,int> f (1.,3);
    pair<double,int> s (2,2);
    pair<double,int> c[n]{f,s};

    sparse_polynomial p(c,n); 
    cout << p(3); 


    return 0;
}