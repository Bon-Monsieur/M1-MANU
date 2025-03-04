#include <iostream>
#include <cassert>
#include <cmath>
#pragma once

template<int Ndim, typename T>
class Vector {
protected:
    T coord[Ndim];

public:
    void zero();
    Vector();
    Vector(T tab[Ndim]);
    T norm2();

    // Surcharge de l'opérateur []
    T& operator[](int i);
    const T& operator[](int i) const;

    // Opérateurs de multiplication par un scalaire
    friend Vector operator*(const Vector<Ndim,T>& p, const T& lambda) {
        Vector temp;
        for (int ii = 0; ii < Ndim; ii++)
            temp[ii] = p[ii] * lambda;
        return temp;
    }

    friend Vector operator*(const T& lambda, const Vector<Ndim,T>& p) {
        Vector temp;
        for (int ii = 0; ii < Ndim; ii++)
            temp[ii] = p[ii] * lambda;
        return temp;
    }

    friend T operator*(const Vector<Ndim,T>& v1, const Vector<Ndim,T>& v2) {
        T sum{0};
        for (int ii = 0; ii < Ndim; ii++)
            sum+= v1[ii] * v2[ii];
        return sum;
    }

    // Surcharge de l'opérateur << pour l'affichage
    friend std::ostream& operator<<(std::ostream& os, const Vector& v) {
        os << "(";
        for (int ii = 0; ii < Ndim; ii++) {
            os << v[ii];
            if (ii < Ndim - 1) os << ", ";
        }
        os << ")" << std::endl;
        return os;
    }



    const Vector& operator*=(const T& lambda );
};

// Implémentation des méthodes

template<int Ndim, typename T>
void Vector<Ndim, T>::zero() {
    for (int ii = 0; ii < Ndim; ii++) {
        coord[ii] = 0;
    }
}

template<int Ndim, typename T>
Vector<Ndim, T>::Vector() {
    this->zero();
}

template<int Ndim, typename T>
Vector<Ndim,T>::Vector(T tab[Ndim]){
    for (int ii = 0; ii < Ndim; ii++) {
        coord[ii] = tab[ii];
    }
}

template<int Ndim, typename T>
T& Vector<Ndim, T>::operator[](int i) {
    assert(i >= 0 && i < Ndim && "Index out of bounds");
    return coord[i];
}

template<int Ndim, typename T>
const T& Vector<Ndim, T>::operator[](int i) const {
    assert(i >= 0 && i < Ndim && "Index out of bounds");
    return coord[i];
}

template<int Ndim,typename T>
const Vector<Ndim,T>& Vector<Ndim,T>::operator*=(const T& lambda ){
    for (int ii = 0; ii < Ndim; ii++) {
        coord[ii] *= lambda;
    }
    return *this;
}

template<int Ndim,typename T>
T Vector<Ndim,T>::norm2(){
    return std::sqrt(*this*(*this));
}