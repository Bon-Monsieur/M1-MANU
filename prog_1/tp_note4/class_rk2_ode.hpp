#include "class_abstract_ode.hpp"
#pragma once


class rk2_odeSolver: public abstract_odeSolver{
    using abstract_odeSolver::abstract_odeSolver;
public: 
    double* solve_equation(std::size_t N) const override;
    rk2_odeSolver(double t0, double x0, double tend, pfn pf);
};