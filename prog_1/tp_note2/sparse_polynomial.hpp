#pragma once
#include <iostream>
#include <cmath>
using namespace std;

/*
je choisi de stocker les polynomes sous la forme d'un tableau contenant les coefs non-nuls et leur degre associe
par exemple le polynome 4+3*x**5+x**100 sera stocké sous la forme [(4,0),(3,5),(1,100)]
ce n'est pas la meilleure façon de faire, mais cela fonctionne
*/

class sparse_polynomial{
    private:
        pair<double,int>* coefs; // Tableau où l'on stocke que les coefs non-nuls avec le degré du monome associé
        size_t taille;
    public:
        sparse_polynomial(); // Constructor nul
        sparse_polynomial(pair<double,int>* tab,size_t nb); // Copy constructor

        const double operator()(double x);  // Evaluation du polynome
        const double operator[](int k) const; // Permet de lire le ieme coef (indique si c'est 0 ou non)
};