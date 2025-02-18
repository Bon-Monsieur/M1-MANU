#pragma once
#include <iostream>


class Integral{
    private:
        double a;
        double b;
        double (*p_func)(double);
    public:
        // Constructor 
        Integral(double a, double b, double (*f)(double));

        //  Getters
        double lowbd(){ return a;}
        double upbd(){ return b;}

        // Common methods
        void change_bounds(double a, double b);
        double trapezoidal(int n) const;
        double rectangular(int n) const;
};