#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include "class_time_loop.hpp"
#include "class_output_writer.hpp"
#include "class_residual.hpp"
#include <iostream>
#include <cmath>
#include <algorithm>

void plot_vector(std::vector<double> const& vec){
    for (size_t ii = 0; ii < vec.size(); ii++){
        std::cout << vec[ii] << " ";
    }
    std::cout << std::endl;
}

// =========== Differents choix possible pour F(u) ============ //


template<typename T>
T flux_Burgers(T const& u){
    return 1.0/2.0*u*u;
}

template<typename T>
T Derivee_flux_Burgers(T const& u){
    return u;
}


template<typename T>
T test(T const& u){
    return std::exp(-u);
}
template<typename T>
T test2(T const& u){
    return -std::exp(-u);
}



int main(){

    mesh_1d<double> mesh(0.0, 10., 1500);
    mesh.print();
    double (*flux)(double const&) = test<double>;
    double (*fp)(double const&) = test2<double>;

    field<double> field(0,mesh,flux,fp);  // 0 = gauss_pulse ; 1 = sin(2*pi*x)

    output_writer<double> out_stream(mesh, "GAUSS_PULSE");
    out_stream.write_solution(field, "initial");

    time_loop<double> loop(mesh, 2); 
    loop.run(field); // Applique la methode FV sur uh
    out_stream.write_solution(field, "final");

    return 0;
}