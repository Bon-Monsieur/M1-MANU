#include <iostream>


using namespace std;


class dynamic_vector{
    private:
        size_t Ndim;
        double* coord;

    public:
        // Constructors
        dynamic_vector(size_t N, double xx=0.0);  
        dynamic_vector(size_t N, double* xx); 

        // Destructor
        ~dynamic_vector() { delete[] coord; }  // ✅ Libérer la mémoire

        // Getters
        const size_t getDim() const { return this->Ndim; }  // Return la dimension du vecteur
        const double* getCoord() const {return this->coord;}

        void set(int i, const double& a);
}; 

// Affichage vector 
ostream& operator <<(std ::ostream& os, const dynamic_vector& v){  // Overloading operator << to print 
    size_t dim = v.dynamic_vector::getDim();
    os << "["; 
    for (int ii=0;ii<dim-1;ii++){
        os << v.getCoord()[ii] << ",";
    }
    os << v.getCoord()[dim-1] << "]" << endl;
    return os;
}


dynamic_vector::dynamic_vector(size_t N, double xx){
    this->Ndim = N;
    this->coord = new double[Ndim];
    for (int ii=0;ii<Ndim;ii++){
        this->coord[ii] = xx;
    }
}


dynamic_vector::dynamic_vector(size_t N, double* xx){
    this->Ndim = N;
    this->coord = new double[Ndim];
    for (int ii=0;ii<Ndim;ii++){
        this->coord[ii] = xx[ii];
    }
}


void set(int i, const double& a){
    
}



int main(){

    size_t dim = 5;
    double* coo1 = new double[dim]{1,-2,3,-4,5};

    dynamic_vector v(dim,coo1);
    cout << "v" << v; 
    
    
    return 0;
}