#include "class_polynomial.hpp"
#include <iostream>

using namespace std;

ostream& operator<<(ostream& os, const polynomial& v){  // Overloading operator << to print 
    size_t dim = v.polynomial::degree();
    os << "["; 
    for (auto ii=0;ii<dim;ii++){
        os << v.coefficients()[ii] << ",";
    }
    os << v.coefficients()[dim] << "]" << endl;
    return os;
}

int main(){
    const size_t deg = 4;
    double a[] = {1., 2., 3., 4., 5.};

    // test of Q2)
    polynomial p2(deg, a);
    cout << "p2(x)=" << p2 << endl<< endl;
    polynomial pn(deg);
    cout << "pn(x)=" << pn << endl << endl;
    // test of Q4)
    cout << "p2 degree= " << p2.degree() << endl<< endl;

    // test of Q5)
    cout << "p2[2]= " << p2[2] << endl<< endl;
    p2[3] = 100;
    cout << "p2[3]=" << p2[3] << endl<< endl;

    // test of Q6)
    polynomial p3(deg);
    p3 = p2;
    cout << "p3(x)=" << p3 << endl<< endl;

    // test of Q7)
    cout << "p1(1)= " << p2(1) << endl << endl; 

    // test of 8)
    polynomial p4(3);
    cout << "p4(x)= " << p4 << endl << endl; 
    p4 += p2;
    cout << "p4(x)= " << p4 << endl << endl; 
    
    // test of 9)
    polynomial p5 = p2 + p3;
    cout << "p5(x)= " << p5 << endl << endl; 

    // test of 10)
    polynomial p6(2.*p3);
    cout << "p6(x)= " << p6 << endl << endl; 

    return 0;
}
