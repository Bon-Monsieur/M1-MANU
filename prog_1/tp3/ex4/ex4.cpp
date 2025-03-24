#include <iostream>
using namespace std;

template<int Ndim>
class point {
private:
    double coord[Ndim];

public:
    // Constructeurs
    point();
    point(double xx);
    point(double coo[Ndim]);
    point(const point& p);

    // Destructeur
    ~point();

    // Accès aux coordonnées
    double icord(int ii) const;
    static int getNdim() { return Ndim; }

    // Opérateurs
    const point& operator=(const point& p);
    const double operator[](int i) const;
    double& operator[](int i);
    const point& operator+=(const point& p);
    const point& operator-=(const point& p);

    // Opérateurs amis (sans template ici)
    template<int N>
    friend point<N> operator-(const point<N>& p);

    friend point operator+(const point& p) {
        point temp;
        for (int i = 0; i < Ndim; i++)
            temp[i] = abs(p[i]);
        return temp;
    }

    friend point operator+(const point& p, const point& q) {
        point temp;
        for (int i = 0; i < Ndim; i++)
            temp[i] = p[i] + q[i];
        return temp;
    }

    friend point operator-(const point& p, const point& q) {
        point temp;
        for (int i = 0; i < Ndim; i++)
            temp[i] = p[i] - q[i];
        return temp;
    }
};


template<int Ndim>
point<Ndim> operator-(const point<Ndim>& p){
    cout << "yo";
    point<Ndim> temp;
    for (int i = 0; i < Ndim; i++)
        temp[i] = -p[i];
    return temp;
    
}


// ====================================================


// Implémentation des méthodes
template<int Ndim>
point<Ndim>::point() {
    for (int i = 0; i < Ndim; i++)
        coord[i] = 0.0;
}

template<int Ndim>
point<Ndim>::point(double xx) {
    for (int i = 0; i < Ndim; i++)
        coord[i] = xx;
}

template<int Ndim>
point<Ndim>::point(double coo[]) {
    for (int i = 0; i < Ndim; i++)
        coord[i] = coo[i];
}

template<int Ndim>
point<Ndim>::point(const point& p) {
    for (int i = 0; i < Ndim; i++)
        coord[i] = p.coord[i];
}

template<int Ndim>
point<Ndim>::~point() {}

template<int Ndim>
double point<Ndim>::icord(int ii) const {
    if (ii < 0 || ii >= Ndim)
        throw("Index hors limites");
    return coord[ii];
}

template<int Ndim>
const double point<Ndim>::operator[](int i) const {
    if (i < 0 || i >= Ndim)
        throw("Index hors limites");
    return coord[i];
}

template<int Ndim>
double& point<Ndim>::operator[](int i) {
    return coord[i];
}

template<int Ndim>
const point<Ndim>& point<Ndim>::operator=(const point<Ndim>& p) {
    if (this != &p) {
        for (int i = 0; i < Ndim; i++)
            coord[i] = p[i];
    }
    return *this;
}

template<int Ndim>
const point<Ndim>& point<Ndim>::operator+=(const point<Ndim>& p) {
    for (int i = 0; i < Ndim; i++)
        coord[i] += p[i];
    return *this;
}

template<int Ndim>
const point<Ndim>& point<Ndim>::operator-=(const point<Ndim>& p) {
    for (int i = 0; i < Ndim; i++)
        coord[i] -= p[i];
    return *this;
}

template<int Ndim>
ostream& operator <<(std ::ostream& os, const point<Ndim>& p){  // Overloading operator << to print 
    os << "["; 
    for (int ii=0;ii<point<Ndim>::getNdim()-1;ii++){
        os << p[ii] << ",";
    }
    os << p[point<Ndim>::getNdim()-1] << "]" << endl;
    return os;
}

// Programme principal
int main() {
    double coo1[3] = {-1, -2, 3};
    point<2> p(2);
    point<3> q(coo1);
    point<3> w = -q;
    cout << w;
    point<3> z;
    z= w-q;
    cout << z;

    return 0;
}
