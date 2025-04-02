#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include <iostream>
#include <cmath>


double gauss_pulse(double xx)
{
return exp(-pow((xx-5.) ,2));
}


int main(){

    mesh_1d<double> mesh(0.0, 1.0, 10);
    mesh.print();

    return 0;
}