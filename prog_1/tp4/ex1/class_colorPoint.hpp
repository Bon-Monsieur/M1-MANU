#include "class_point.hpp"
#pragma once

class colorPoint: public point{

protected:
    unsigned int color;

public:
    unsigned int Color() const {return color;}
    void zero();
    void setColor(unsigned int c){color = c;}

    colorPoint();
    colorPoint(double x, double y,unsigned int color);
    colorPoint(const colorPoint& p);

    const colorPoint& operator=(const colorPoint& p);
    friend const colorPoint operator+(const colorPoint& p, const colorPoint& q); // Sum of two point
    friend const colorPoint operator-(const colorPoint& p, const colorPoint& q); // Subtract
};


void colorPoint::zero(){
    this->point::zero();
    this->color = 0;
}

colorPoint::colorPoint():point(){
    this->color=0;
}

colorPoint::colorPoint(double x, double y, unsigned int color):point((double[]){x,y}){
    this->color=color;
}

colorPoint::colorPoint(const colorPoint& p):point(p){
    this->color = p.Color();
}

const colorPoint& colorPoint::operator=(const colorPoint& p){
    this->color = p.Color();
    this->point::operator=(p);
    return *this;
}   

const colorPoint operator-(const colorPoint& p, const colorPoint& q){
    colorPoint temp;
    
    return temp;
}