#pragma once
#include <iostream>

class dynamic_vector{
    private:
        size_t Ndim;
        double* coord;

    public:

        // Getters
        const size_t getDim() const { return this->Ndim; }  // Return la dimension du vecteur
        const double* getCoord() const {return this->coord;}

        // Constructors
        dynamic_vector();
        dynamic_vector(size_t N, double xx=0.0);  
        dynamic_vector(size_t N, double* xx); 
        dynamic_vector(const dynamic_vector& v);  // Constructor par copy

        // Destructor
        ~dynamic_vector() { delete[] coord; }  // ✅ Libérer la mémoire

        void set(int i, const double& a);

        
        const dynamic_vector& operator=(const dynamic_vector& v);
        const dynamic_vector& operator=(const double& xx);

        double operator[]( int ii ) const;
        double& operator[] ( int ii );

        friend const dynamic_vector operator*(const dynamic_vector& p, const double& lambda);
        friend const dynamic_vector operator*(const double& lambda, const dynamic_vector& p );

        const dynamic_vector& operator+(const dynamic_vector& v1, const dynamic_vector& v2);
};