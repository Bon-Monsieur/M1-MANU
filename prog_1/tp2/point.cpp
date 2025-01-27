#include <iostream>

using namespace std;


class point
{
private:
    double x;
    double y;
public:

    double X() const{ return x; }
    double Y() const{ return y; }

    void zero();
    void set(int i, const double& a);

    point(double x,double y);
    point(const point& p);
    point();

    ~point();

    const point& operator=(const point& p);

};





void point::zero(){ // Set to zero mehtod
    x = 0;
    y = 0;
}

void point::set(int i, const double& a){
    switch(i){
        case 1: 
            x = a;
            break;

        case 2:
            y = a;
            break;
        default:
            throw invalid_argument("first argument must be 1 or 2");      
    }
}

point::point(double x, double y){ // Constructor
    this->x=x;
    this->y=y;
}

point::point(const point& p){ // Constructor à partir d'un autre point 
    this->x = p.X();
    this->y = p.Y();
}

point::point(){
    this->zero();
}

point::~point() {   // Destructor
}


ostream& operator <<(std ::ostream& os, const point& p){  // Overloading operator << to print 
    os << "(x,y)=" <<  '(' << p.X() << ',' << p.Y() << ')' <<  endl;
    return os;
}

const point& point::operator =(const point& p){
    if (this != &p){
        this->x = p.x;
        this->y = p.y;
    }
    return *this;
}


int main(){

    /* 
    point P(3.,5.);
    point Q(P);
    cout <<"P" << P;
    cout << "Q" << Q;
    */
    
    point P,W,Q(1. ,2.);
    P=W=Q;

    cout << "P" << P;
    cout << "W" << W;
    cout << "Q" << Q;

 
    

    return 0;
}