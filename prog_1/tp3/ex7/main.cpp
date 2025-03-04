#include "class_vector.hpp"

int main(){
    const int n = 4;
    int tab[n]={1,1,3,3};
    double tab2[n]={2,2,4,4};
    Vector<n,int> v1(tab);
    Vector<n,double> v2(tab2);
    v1*=3 ;
    std::cout << v1;
    std::cout << v2;
    //std::cout << v1*v2 << std::endl;

    std::cout << v2.norm2() << std::endl;
    return 0;
}