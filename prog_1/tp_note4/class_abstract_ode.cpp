#include "class_abstract_ode.hpp"

abstract_odeSolver::abstract_odeSolver(double t0, double x0, double tend, pfn pf){
    t0_ = t0;
    x0_ = x0;
    tend_ = tend;
    pf_ = pf;
}

double abstract_odeSolver::get_t0() const{
    return t0_;
}

double abstract_odeSolver::get_x0() const{
    return x0_;
}

double abstract_odeSolver::get_tend() const{
    return tend_;
}
pfn abstract_odeSolver::get_pf() const{
    return pf_;
}




