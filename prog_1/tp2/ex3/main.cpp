#include "class_dynamic_vector.hpp"
using namespace std;

// Affichage vector 
ostream& operator <<(std ::ostream& os, const dynamic_vector& v){  // Overloading operator << to print 
    size_t dim = v.dynamic_vector::getDim();
    os << "["; 
    for (auto ii=0;ii<dim-1;ii++){
        os << v.getCoord()[ii] << ",";
    }
    os << v.getCoord()[dim-1] << "]" << endl;
    return os;
}


int main(){

    size_t dim = 6;
    double* coo1 = new double[dim]{1,-2,3,-4,5,0};
    double* coo2 = new double[dim]{1,-2,3,-4,5,6};

    dynamic_vector v(dim,coo1);
    dynamic_vector v2(dim,coo2);
    double lambda  = 3;
    dynamic_vector a;
    a = v*lambda;
    cout << a;
    
    delete[] coo1;
    delete[] coo2;

    return 0;
}