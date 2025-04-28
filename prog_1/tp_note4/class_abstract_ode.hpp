#include <iostream>
#pragma once
typedef double (*pfn) (double,double);

class abstract_odeSolver{
protected:
    double t0_;
    double x0_;
    double tend_;
    pfn pf_;
public:
    abstract_odeSolver(double t0, double x0, double tend, pfn pf);

    double get_t0() const;
    double get_x0() const;
    double get_tend() const;
    pfn get_pf() const;

    virtual double* solve_equation(std::size_t N) const = 0;
};