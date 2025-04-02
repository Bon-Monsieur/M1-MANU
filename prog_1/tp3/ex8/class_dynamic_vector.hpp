#include <iostream>
#include <cassert>
#include <cmath>
#pragma once

template<typename T>
class DynamicVector {
protected:
    size_t Ndim;
    T* coord;

public:
    DynamicVector();
    DynamicVector(size_t N, T xx);
    DynamicVector(const DynamicVector<T>& other);
    ~DynamicVector();

    void zero();
    T norm2();

    T& operator[](int i);
    const T& operator[](int i) const;

    DynamicVector& operator*=(const T& lambda);

    friend DynamicVector operator*(const DynamicVector<T>& p, const T& lambda) {
        DynamicVector<T> temp(p);
        for (size_t ii = 0; ii < p.Ndim; ii++)
            temp[ii] *= lambda;
        return temp;
    }

    friend DynamicVector operator*(const T& lambda, const DynamicVector<T>& p) {
        return p * lambda;
    }

    friend T operator*(const DynamicVector<T>& v1, const DynamicVector<T>& v2) {
        assert(v1.Ndim == v2.Ndim && "Vectors must have the same dimension");
        T sum = 0;
        for (size_t ii = 0; ii < v1.Ndim; ii++)
            sum += v1[ii] * v2[ii];
        return sum;
    }

    friend std::ostream& operator<<(std::ostream& os, const DynamicVector<T>& v) {
        os << "(";
        for (size_t ii = 0; ii < v.Ndim; ii++) {
            os << v[ii];
            if (ii < v.Ndim - 1) os << ", ";
        }
        os << ")";
        return os;
    }
};

// Implémentation

template<typename T>
DynamicVector<T>::DynamicVector() : Ndim(0), coord(nullptr) {}

template<typename T>
DynamicVector<T>::DynamicVector(size_t N,T xx) : Ndim(N) {
    coord = new T[Ndim];
    for (size_t ii = 0; ii < Ndim; ii++) {
        coord[ii] = xx;
    }
}

template<typename T>
DynamicVector<T>::DynamicVector(const DynamicVector<T>& other) : Ndim(other.Ndim) {
    coord = new T[Ndim];
    for (size_t ii = 0; ii < Ndim; ii++) {
        coord[ii] = other.coord[ii];
    }
}

template<typename T>
DynamicVector<T>::~DynamicVector() {
    delete[] coord;
}

template<typename T>
void DynamicVector<T>::zero() {
    for (size_t ii = 0; ii < Ndim; ii++) {
        coord[ii] = 0;
    }
}

template<typename T>
T& DynamicVector<T>::operator[](int i) {
    assert(i >= 0 && i < Ndim && "Index out of bounds");
    return coord[i];
}

template<typename T>
const T& DynamicVector<T>::operator[](int i) const {
    assert(i >= 0 && i < Ndim && "Index out of bounds");
    return coord[i];
}

template<typename T>
DynamicVector<T>& DynamicVector<T>::operator*=(const T& lambda) {
    for (size_t ii = 0; ii < Ndim; ii++) {
        coord[ii] *= lambda;
    }
    return *this;
}

template<typename T>
T DynamicVector<T>::norm2() {
    return std::sqrt(*this * *this);
}
