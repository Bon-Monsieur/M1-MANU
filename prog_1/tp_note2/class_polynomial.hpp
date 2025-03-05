#include <iostream>

#pragma once

class polynomial{
    private:
        size_t degree_;
        double* coefficients_;
    public:
        // J'ai choisi de modifier le premier constructor pour la question 3)
        polynomial(size_t n, double* tab);
        polynomial(size_t n);
        polynomial(const polynomial& p); // copy constructor
        ~polynomial(){delete[] coefficients_; }; // destructor

        size_t degree() const;
        double* coefficients() const;

        const double operator[](int i) const; // read ieme coord
        double& operator[]( int i );  // Assign ieme coord

        const polynomial& operator=(const polynomial& p);

        const double operator()(double x); // Evaluation du polynome

        const polynomial& operator+=(const polynomial& p);
        
        friend const polynomial operator+(const polynomial& p, const polynomial& q);
        friend const polynomial operator*(const double lambda, const polynomial& p);
        friend const polynomial operator*( const polynomial& p,const double lambda);
        
};