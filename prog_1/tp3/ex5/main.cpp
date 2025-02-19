#include "binomial.hpp"


int main(){

    const int M = 11;
    Binomial<M> b1;
    cout << b1;
    cout << b1(9,5);

    return 0;
}