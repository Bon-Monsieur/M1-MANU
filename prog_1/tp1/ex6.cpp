#include <iostream>
#include <cmath>

using namespace std;



void CalculateRealAndImaginary(double r, double theta, double* pReal, double* pImaginary) {
    *pReal = r * cos(theta);        
    *pImaginary = r * sin(theta);   
}



int main() {
    double theta = M_PI / 3;
    double r = 1;

    double pReal = 0;
    double pImaginary = 0;

    double* pointReal = &pReal;  
    double* pointImag = &pImaginary;

    
    CalculateRealAndImaginary(r, theta, pointReal, pointImag);

    
    cout << "Real part: " << pReal << " Imaginary part: " << pImaginary << endl;

    return 0;
}
