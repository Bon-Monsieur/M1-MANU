#include "class_rk2_ode.hpp"



rk2_odeSolver::rk2_odeSolver(double t_init, double x_init, double t_end,pfn f):abstract_odeSolver(t_init,x_init,t_end,f) {}


double* rk2_odeSolver::solve_equation(std::size_t N) const{
    double* x = new double[N+1];
    double h = (get_tend()-get_t0())/N;
    x[0] = get_x0();
    for (std::size_t i=1;i<=N;i++){
        double t_k = get_t0() + h*(i-1);
        double F1 = (pf_)(t_k,x[i-1]);
        double F2 = (pf_)(t_k+h,x[i-1]+h*F1);
        x[i] = x[i-1] + 0.5*(F1+F2)*h;
    }
    return x;
}


