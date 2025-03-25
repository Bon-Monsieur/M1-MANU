#include "class_complex_number_T.hpp"
#include <iostream>
#include <cmath>




int main() {
    complex_number<double> z1(1.0, 1.0);
    complex_number<int> cc(1, 1);
    std::cout << typeid(z1).name() << std::endl;  // z1 est un nombre_complex de type double
    std::cout << typeid(cc).name() << std::endl; // cc est un nombre_complex de type int
    
    complex_number<double> z2=z1;
    std::cout << "z2=" << z2;
    complex_number<double> z3;
    std::cout << "z3=" << z3;
    z3 = z2+z1;
    std::cout << "z3=" << z3;
    std::cout << z3.modulus() << std::endl;
    

    return 0;
}