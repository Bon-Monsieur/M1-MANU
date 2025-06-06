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
T flux_stage(T const& u){
    return u*(1.0 - u);
}
template<typename T>
T Derivee_flux_stage(T const& u){
    return 1.0-2.0*u;
}



int main(){

    mesh_1d<double> mesh(-5.0, 5.0, 100);
    mesh.print();

    // Il faut definir la fonction de flux et sa derivee pour la classe field afin d'avoir une flexibilite quant au choix de la fonction de flux
    double (*flux)(double const&) = flux_stage<double>;
    double (*fp)(double const&) = Derivee_flux_stage<double>;

    field<double> field(1,mesh,flux,fp);  // 0 = gauss_pulse ; 1 = stage_test pour l'initialisation

    output_writer<double> out_stream(mesh, "stage");
    out_stream.write_solution(field, "initial");

    time_loop<double> loop(mesh, 1); 
    loop.run(field);            
    out_stream.write_solution(field, "final");

    return 0;
}