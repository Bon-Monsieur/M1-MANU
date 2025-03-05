#include <iostream>
#include <cmath>
#include "sparse_polynomial.hpp"


sparse_polynomial::sparse_polynomial(){ // Initialise au polynome nul
    this->coefs = new pair<double,int>[1];
    pair<double,int> a (0.,0);
    coefs[0] = a;
    this->taille=1;
}


sparse_polynomial::sparse_polynomial(pair<double,int>* tab, size_t n){ // constructor par copy
    this->coefs = new pair<double,int>[n];
    for (auto ii=0;ii<n;ii++){
        coefs[ii] = tab[ii];
    }
    this->taille = n;
}



const double sparse_polynomial::operator()(double x){ // Evaluation du polynome
    double sum = 0;
    for (auto ii=0;ii<taille;ii++){
        sum += (coefs[ii]).first*pow(x,(coefs[ii]).second);
    }
    return sum;
}

// S'il existe bien un coef a_k devant le monome de degre k alors on le renvoie, sinon on renvoie 0
const double sparse_polynomial::operator[](int k) const{
    double res = 0;
    for (auto ii=0;ii<taille;ii++){
        if (coefs[ii].second == k){
            res = coefs[ii].first;
            return res;
        }
    }
    return res;
} 