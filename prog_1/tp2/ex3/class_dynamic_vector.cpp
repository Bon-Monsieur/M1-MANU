#include "class_dynamic_vector.hpp"
using namespace std;


dynamic_vector::dynamic_vector(){
    this->Ndim = 1;
    this->coord = new double[Ndim]{0};
}


dynamic_vector::dynamic_vector(size_t N, double xx){
    this->Ndim = N;
    this->coord = new double[Ndim];
    for (size_t ii=0;ii<Ndim;ii++){
        this->coord[ii] = xx;
    }
}


dynamic_vector::dynamic_vector(size_t N, double* xx){
    this->Ndim = N;
    this->coord = new double[N];
    for (size_t ii=0;ii<N;ii++){
        this->coord[ii] = xx[ii];
    }
}


dynamic_vector::dynamic_vector(const dynamic_vector& v){  // Copy constructor
    this->Ndim = v.getDim();
    for (int ii=0;ii<Ndim;ii++){
        this->coord[ii] = v.getCoord()[ii];
    } 
}

/*
void dynamic_vector::set(int i, const double& a){
    if (i<0 || i>=this->getDim()){
        throw("Le premier parametre doit être compris entre 0 et la dim du vecteur");
    }
    else{
        this->coord[i] = a;
    }
}
*/



double dynamic_vector::operator[](int ii) const {   // Renvoie
    if (ii<0 || ii>=this->getDim()){
        throw("Le premier parametre doit être compris entre 0 et la dim du vecteur");
    }
    else{
        return this->coord[ii];
    }
}


double& dynamic_vector::operator[](int ii){ // Renvoie l'adresse mémoire de coord[ii] qui peut être modifiée
    if (ii<0 || ii>=this->getDim()){
        throw("Le premier parametre doit être compris entre 0 et la dim du vecteur");
    }
    else{
        return this->coord[ii];
    }
}


const dynamic_vector& dynamic_vector::operator=(const dynamic_vector& v){
    if (this != &v){
        this->Ndim = v.getDim();
        delete[] this->coord;    // IL FALLAIT SUPPRIMER LES ANCIENNES COORDONNEES
        this->coord = new double[Ndim]; // PUTAIN
        for (int ii=0;ii<v.getDim();ii++){
            this->coord[ii] = v.getCoord()[ii];
        }
    }
    return *this;
}


const dynamic_vector operator*(const dynamic_vector& v, const double& lambda){
    size_t n = v.getDim();
    dynamic_vector temp(n,0.0);
    for (int ii=0;ii<n;ii++){
        temp[ii] = v[ii] * lambda;
    }
    return temp;
}