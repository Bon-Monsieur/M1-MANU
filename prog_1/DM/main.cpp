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



int main(){

    mesh_1d<double> mesh(0.0, 15., 1500);
    mesh.print();
    
    field<double> field(0,mesh);  // u0 = gauss_pulse

    output_writer<double> out_stream(mesh, "GAUSS_PULSE");
    out_stream.write_solution(field, "initial");

    time_loop<double> loop(mesh, 4); 
    loop.run(field); // Applique la methode FV sur uh
    out_stream.write_solution(field, "final");

    return 0;
}