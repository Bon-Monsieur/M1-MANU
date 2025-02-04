#include <iostream>
#include <cmath>

using namespace std;


pair<double,double> quadraticRoot (const double & a, const double & b, const double & c){
    double delta = pow(b,2) - 4*a*c;

    if (delta<0){
        throw invalid_argument("Delta is negative");
    }
    else{
        
        pair<double,double> res ((-b-sqrt(delta))/2/a , (-b+sqrt(delta))/2/a);
        return res;
    }
}


int main(){

    const double a=1,b=-3,c=2;
    pair<double,double> racines = quadraticRoot(a,b,c);
    double x1 = racines.first;
    double x2 = racines.second;

    cout << "x1=" << x1 << "  et x2=" << x2 << endl;

    return 0;
}