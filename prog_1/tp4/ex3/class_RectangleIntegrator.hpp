#include "class_AbstractIntegrator.hpp"




class RectangleIntegrator:public AbstractIntegrator{

public:
    double computeIntegral(int Nint){
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
        return sum;
    }
};

