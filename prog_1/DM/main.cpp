#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include "class_time_loop.hpp"
#include "class_output_writer.hpp"
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

    mesh_1d<double> mesh(0.0, 10., 40);
    mesh.print();
    
    field<double> field(0,mesh);
    //time_loop<double> time_loop(mesh, 1.0);
    output_writer<double> out_stream(mesh, "solution");
    
    out_stream.write_solution(field, "0");

    return 0;
}