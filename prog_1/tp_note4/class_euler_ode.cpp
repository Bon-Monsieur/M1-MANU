#include "class_euler_ode.hpp"


double* euler_ode_solver::solve_equation(std::size_t N) const{
    double* x = new double[N+1];
    double h = (get_tend()-get_t0())/N;
    x[0] = get_x0();
    for (std::size_t i=1;i<=N;i++){
        double t_k = get_t0() + (i-1)*h;
        x[i] = x[i-1] + h*(pf_)(t_k,x[i-1]);
    }
    return x;
}

euler_ode_solver::euler_ode_solver(double t_init, double x_init, double t_end,pfn f):abstract_odeSolver(t_init,x_init,t_end,f) {}