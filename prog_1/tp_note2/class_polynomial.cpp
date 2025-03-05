#include "class_polynomial.hpp"
#include <iostream>
#include <cmath>
using namespace std;


polynomial::polynomial(size_t n, double* tab){
    this->degree_ = n;
    this->coefficients_ = new double[n+1];
    for (auto ii=0;ii<=n;ii++){
        coefficients_[ii] = tab[ii];
    }
}


polynomial::polynomial(size_t n){
    this->degree_ = n;
    this->coefficients_ = new double[n+1];
    for (auto ii=0;ii<=n;ii++){
        coefficients_[ii] = 0;
    }
}


size_t polynomial::degree() const{
    return degree_;
}


double* polynomial::coefficients() const{
    return coefficients_;
}


const double polynomial::operator[](int i) const{    // read only p[i]
    return this->coefficients_[i];
}


double& polynomial::operator[]( int i ){  // renvoie  l'adresse memoire de la ieme coord
    return this->coefficients_[i];
}

polynomial::polynomial(const polynomial& p){ // Copy constructor
    this->degree_=p.degree_;
    this->coefficients_  = new double[degree_+1];
    for (auto ii=0;ii<=degree_;ii++){
        this->coefficients_[ii] = p[ii];
    }
}

const polynomial& polynomial::operator=(const polynomial& p){
    if (this != &p){
        this->degree_=p.degree_;
        delete[] this->coefficients_;    
        this->coefficients_ = new double[degree_+1];
        for (auto ii=0;ii<=degree_;ii++){
            this->coefficients_[ii] = p[ii];
        }
    }
    return *this;
}

const double polynomial::operator()(double x){ // Evaluation du polynome
    double sum = 0;
    for (int ii=0;ii<=degree();ii++){
        sum+=coefficients_[ii]*pow(x,ii);
    }
    return sum;
}


const polynomial& polynomial::operator+=(const polynomial& p){
    double* ctemp2 = new double[max(degree(),p.degree_)];
    double* ctemp1 = new double[degree()];
    for (auto ii=0;ii<=degree();ii++){
        ctemp1[ii]=coefficients()[ii];
    }
    this->degree_=max(p.degree_,degree());
    for (auto ii=0;ii<=degree();ii++){
        ctemp2[ii]=ctemp1[ii]+p[ii];
    }
    this->coefficients_ = ctemp2;
    return *this;
}



const polynomial operator+(const polynomial& p, const polynomial& q){
    polynomial temp(p);
    temp+=q;
    return temp;
}

const polynomial operator*(const double lambda, const polynomial& p){
    polynomial temp(p);
    for (auto ii=0;ii<=p.degree();ii++){
        temp[ii]*=lambda;
    }
    return temp;
}


const polynomial operator*(const polynomial& p,const double lambda){
    polynomial temp(p);
    for (auto ii=0;ii<=p.degree();ii++){
        temp[ii]*=lambda;
    }
    return temp;
}
