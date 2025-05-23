#include "class_AbstractIntegrator.hpp"
#include <iostream>
#pragma once


class RectangleIntegrator:public AbstractIntegrator{
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
            double f_xi = (f)(xi);
            sum+=f_xi*h;
        }
        std::cout <<"integrale rectangle=" << sum << std::endl;
    }
};

