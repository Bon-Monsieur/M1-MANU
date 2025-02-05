#include <iostream>
#include "class_point.hpp"
using namespace std;


double  point::icord(int ii) const {
    if (ii<0 || ii>=Ndim){
        throw("le parametre doit etre compris entre 0 et Ndim");
    }
    else{
        return coord[ii];
    }
}


void point::zero(){ // Set to zero mehtod
    for (int ii=0;ii<Ndim;ii++){
        coord[ii]=0.0;
    }
}


void point::set(int i, const double& a){
    if (i<0 || i>=Ndim){
        throw("le parametre doit etre compris entre 0 et Ndim");
    }
    else{
        this->coord[i] = a;
    }
}


point::point(double xx){ // Constructor assign one value for each coordinate
    for (int ii=0;ii<Ndim;ii++){
        coord[ii]=xx;
    }
}

point::point(double coo[Ndim]){ // Constructor à partir des coo d'un autre point 
    for (int ii=0;ii<Ndim;ii++){
        coord[ii]=coo[ii];
    }
}


point::point(){   // Constructor with no value
    this->zero();
}


point::point(const point& p){  // Constructor copy
    for (int ii=0;ii<Ndim;ii++){
        this->coord[ii]=p[ii];
    }
}


point::~point() {   // Destructor
}

const double point::operator[](int i) const{        // getter p[i]
    if (i<0 || i>=Ndim){
        throw("le parametre doit etre compris entre 0 et Ndim");
    }
    else{
        return this->coord[i];
    }
}


double& point::operator[]( int i ){  // renvoie  l'adresse memoire de la ieme coord
    return this->coord[i];
}


const point& point::operator=(const point& p){  // Overloading operator = to an easier assignment 
    if (this != &p){
        for (int ii=0;ii<Ndim;ii++){
            this->coord[ii]=p[ii];
        }
    }
    return *this;
}


const point operator-(const point& p) { // Point temporaire. On ne créer pas de nouveau point
                                        // avec -P, on se sert juste de sa valeur
    point temp1 = p;
    point temp2;
    for (int ii=0;ii<point::getNdim();ii++){
        temp2[ii] = -temp1[ii];
    }
    return temp2;
}

const point operator+(const point& p) {// Point temporaire. On ne créer pas de nouveau point
                                        // avec +P, on se sert juste de sa valeur
    point temp1 = p;
    point temp2;
    for (int ii=0;ii<point::getNdim();ii++){
        temp2[ii] = abs(temp1[ii]);
    }
    return temp2;
}


const point operator+(const point& p, const point& q){
    point temp;
    for (int ii=0;ii<point::getNdim();ii++){
        temp[ii] = p[ii]+q[ii];
    }
    return temp;
}

const point operator-(const point& p, const point& q){
    point temp;
    for (int ii=0;ii<point::getNdim();ii++){
        temp[ii] = p[ii]-q[ii];
    }
    return temp;
}


const point& point::operator+=(const point& p){ // Ici on modifie le point de base, donc on 
                                                //renvoie le pointeur
    *this = *this + p;
    return *this;
}

const point& point::operator-=(const point& p){ // Ici on modifie le point de base, donc on 
                                                //renvoie le pointeur
    *this = *this - p;
    return *this;
}
