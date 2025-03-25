#include "class_complex_number.hpp"
#include <cmath>

// Set real and imaginary parts to zero
complex_number::complex_number()
{
    real_      = 0.0;
    imaginary_ = 0.0;
}

// Constructor that sets complex number z=x+iy
complex_number::complex_number(double x, double y)
{
    real_      = x;
    imaginary_ = y;
}

complex_number::complex_number(complex_number const& cc):real_(cc.real()), imaginary_(cc.imaginary()){}

// Method for computing the modulus of a complex number
double complex_number::modulus() const
{
    return sqrt(pow(real_, 2) + imaginary_ * imaginary_);
}
//
// Method for computing the argument of a complex number
double complex_number::argument() const
{
    return atan2(imaginary_, real_);
}
//
// Method for raising complex number to the power n
// using De Moivre’s theorem - first complex
// number must be converted to polar form

complex_number complex_number::compute_power(size_t n) const
{
    double modulus       = this->modulus();
    double argument      = this->argument();
    double mod_of_result = pow(modulus, n);
    double arg_of_result = argument * n;
    double real_part     = mod_of_result * std::cos(arg_of_result);
    double imag_part     = mod_of_result * std::sin(arg_of_result);
    complex_number z(real_part, imag_part);
    return z;
}

