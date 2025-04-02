#include "class_AbstractIntegrator.hpp"
#include <iostream>
#pragma once



class TrapezoidalIntegrator: public AbstractIntegrator{
using AbstractIntegrator::AbstractIntegrator;

public:
    void computeIntegral(int Nint) const{
        double a = lowbd();
        double b = upbd();
        pfn f = getIntegrand();
        double h = (b-a)/Nint;
        double sum = 0;
        for (auto i=0;i<=Nint;i++){
            double xi = a+(b-a)/Nint*i;
            double xi_p1 = a+(b-a)/Nint*(i+1);
            double f_xi = f(xi);
            double f_xi_p1 = f(xi_p1);
            sum+=(f_xi+f_xi_p1)*h/2;
        }
        std::cout <<"integrale trapeze=" << sum << std::endl;
    }

};