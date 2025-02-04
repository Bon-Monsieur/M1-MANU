#include <iostream>

using namespace std;


class point
{
private:
    double x;
    double y;
public:
    // get coordinates
    double X() const{ return x; }
    double Y() const{ return y; }

    // setters
    void zero();
    void set(int i, const double& a);

    // Constructors
    point(double x,double y);
    point(const point& p);
    point();

    // Destructor
    ~point();

    const point& operator=(const point& p);  //Definir un point à partir d'un autre
    const point& operator=(double xx);       // Definir seulement la première coordonnée d'un point

    operator double() const;

    friend const point operator-(const point& p); // Donne -la valeur du point donné en entrée
    friend const point operator+(const point& p); // Donne valeur absolue du point donné en entrée

    
    const point& operator+=(const point& p);
    const point& operator-=(const point& p); 
    const point& operator+=(double xx); // Incrémente uniquement la coordonée x
    const point& operator-=(double xx); // Décémente uniquement la coordonée x

    friend const point operator+(const point& p, const point& q); // Sum of two point
    friend const point operator-(const point& p, const point& q); // Subtract

    friend const point operator+(const point& p, double xx); // point + double (x coordinate only)
    friend const point operator+(double xx, const point& p); // double + point (x coordinate only)

    friend const point operator-(const point& p, double xx); // point - double (x coordinate only)
    friend const point operator-(double xx,const point& p); // point - double (x coordinate only)

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

point::point(double x, double y){ // Constructor with 2 values
    this->x=x;
    this->y=y;
}

point::point(const point& p){ // Constructor à partir d'un autre point 
    this->x = p.X();
    this->y = p.Y();
}

point::point(){   // Constructor with no value
    this->zero();
}

point::~point() {   // Destructor
}


ostream& operator <<(std ::ostream& os, const point& p){  // Overloading operator << to print 
    os << "(x,y)=" <<  '(' << p.X() << ',' << p.Y() << ')' <<  endl;
    return os;
}

const point& point::operator =(const point& p){  // Overloading operator = to an easier assignment 
    if (this != &p){
        this->x = p.x;
        this->y = p.y;
    }
    return *this;
}


const point& point::operator=(double xx){ 
    this->x = xx;
    return *this;
}

// read the x-coordinate of a point object P
point::operator double() const {
    return this->x;
}


const point operator-(const point& p) { // Point temporaire. On ne créer pas de nouveau point
                                        // avec -P, on se sert juste de sa valeur
    point temp(-p.x,-p.y);
    return temp;
}

const point operator+(const point& p) {// Point temporaire. On ne créer pas de nouveau point
                                        // avec +P, on se sert juste de sa valeur
    point temp(abs(p.x),abs(p.y));
    return temp;
}


const point& point::operator+=(const point& p){ // Ici on modifie le point de base, donc on 
                                                //renvoie le pointeur
    this->x = this->x + p.x;
    this->y = this->y + p.y;
    return *this;
}

const point& point::operator-=(const point& p){ // Ici on modifie le point de base, donc on 
                                                //renvoie le pointeur
    this->x = this->x - p.x;
    this->y = this->y - p.y;
    return *this;
}

const point& point::operator+=(double xx){ // Ici on modifie le point de base, donc on 
                                           //renvoie le pointeur
    this->x += xx;
    return *this;
} // add real number to the current point

const point& point::operator-=(double xx){
    this->x -= xx;
    return *this;
} // subtract real number to the current point


const point operator+(const point& p, const point& q){
    point temp(p.x+q.x,p.y+q.y);
    return temp;
}

const point operator-(const point& p, const point& q){
    point temp(p.x-q.x,p.y-q.y);
    return temp;
}


const point operator+(const point& p, double xx){
    point temp(p.x+xx,p.y);
    return temp;
}


const point operator+(double xx, const point& p){
    point temp(p.x+xx,p.y);
    return temp;
}


const point operator-(const point& p, double xx){
    point temp(p.x-xx,p.y);
    return temp;
}


const point operator-(double xx, const point& p){
    point temp = -p + xx;
    return temp;
}


int main(){

    
    
    point P(1,2);
    point Q(3,4);
    point W;
    
    W = P - 1.;
    cout << "W" << W;
   
    
    return 0;
}