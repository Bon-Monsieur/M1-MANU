#include <iostream>
#include <cmath>

using namespace std;


pair<double,double> quadraticRoot (const double & a, const double & b, const double & c){
    double delta = pow(b,2) - 4*a*c;

    if (delta<0){
        throw invalid_argument( "Delta is negative");
    }
    else{

        pair<double,double> res ((-b-sqrt(delta))/2/a , (-b+sqrt(delta))/2/a);

        return res;
    }
}


int main(){

    const double a=2,b=6,c=1;

    cout << quadraticRoot(a,b,c).first << " " << quadraticRoot(a,b,c).second ;

    return 0;
}