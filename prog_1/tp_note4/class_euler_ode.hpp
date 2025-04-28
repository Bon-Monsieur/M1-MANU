#include "class_abstract_ode.hpp"
#pragma once

typedef double (*pfn) (double,double);

class euler_ode_solver:public abstract_odeSolver{
using abstract_odeSolver::abstract_odeSolver;
public:
    double* solve_equation(std::size_t N) const override ;
    euler_ode_solver(double t0, double x0, double tend, pfn pf);
};