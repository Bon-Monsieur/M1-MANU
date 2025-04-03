#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include <iostream>
#include <cmath>

void plot_vector(std::vector<double> const& vec){
    for (size_t ii = 0; ii < vec.size(); ii++){
        std::cout << vec[ii] << " ";
    }
    std::cout << std::endl;
}






int main(){

    mesh_1d<double> mesh(0.0, 10., 10);
    mesh.print();
    
    field<double> field(0,mesh);
    
    

    return 0;
}