#include "class_point.hpp"
#include <iostream>

using namespace std;

ostream& operator <<(std ::ostream& os, const point& p){  // Overloading operator << to print 
    os << "["; 
    for (int ii=0;ii<point::getNdim()-1;ii++){
        os << p[ii] << ",";
    }
    os << p[point::getNdim()-1] << "]" << endl;
    return os;
}


int main(){

    double coo1[point::getNdim()]={-1,-2,3};
    point P(coo1);
    point Q(2);
    point W;
    W = Q;
    W -=P;
    cout << W;
   
    return 0;
}