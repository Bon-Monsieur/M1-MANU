#include "class_RectangleIntegrator.hpp"
#include "class_TrapezoidalIntegrator.hpp"
#include <iostream>
#include <cmath>



double carre(double x){
    return x*x;
}


int main(){

    pfn pcarre=carre;
    AbstractIntegrator *integrator = new RectangleIntegrator(0.,1,pcarre);
    integrator->computeIntegral(1000);
    delete integrator;
    /*
    RectangleIntegrator rec(0.,1.,pcarre);
    rec.computeIntegral(500);

    TrapezoidalIntegrator trap(0.,1.,pcarre);
    trap.computeIntegral(500);
    */
    

    return 0;
}