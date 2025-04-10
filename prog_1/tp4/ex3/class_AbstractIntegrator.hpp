#pragma once

typedef double (*pfn) (double);

class AbstractIntegrator {
private:
    double lower;
    double upper;
    pfn integrand ;
public:
    AbstractIntegrator (double a, double b, pfn f ); // constructor
    double lowbd() const; // accessor: get lower bound
    double upbd() const; // accessor: get upper bound
    void change_bounds(double a, double b); //change integral bounds to a, b
    virtual void computeIntegral(int Nint) const = 0; // pure ( = 0 ) virtual function

    pfn getIntegrand() const {return integrand;}
};

AbstractIntegrator::AbstractIntegrator (double a, double b, pfn f ) {
    lower = a;
    upper = b;
    integrand = f;
}

double AbstractIntegrator::lowbd() const {
    return lower;
}   

double AbstractIntegrator::upbd() const {
    return upper;
}



void AbstractIntegrator::change_bounds(double a, double b) {
    lower = a;
    upper = b;
}