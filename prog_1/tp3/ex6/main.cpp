#include <iostream>
#include "exPade.hpp"


int main(){

    double x = 1;
    const int N = 8;

    cout <<  "Pade:  approximation de exp(" << x << ") = "<< exPade<N>(x) << endl;
    return 0;
}