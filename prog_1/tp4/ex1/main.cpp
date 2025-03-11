#include "class_colorPoint.hpp"
#include <iostream>

std::ostream& operator<<(std::ostream& os, const colorPoint& p){  // Overloading operator << to print 
    os << "["; 
    for (int ii=0;ii<point::getNdim()-1;ii++){
        os << p[ii] << ",";
    }
    os << p[point::getNdim()-1] << "] color=" << p.Color() << std::endl;
    return os;
}


int main(){

    colorPoint p(3,2,1);
    std::cout << p;
    colorPoint q,w;
    q = p;
    std::cout << w; 
    

    

    return 0;
}