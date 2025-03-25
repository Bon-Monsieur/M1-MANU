#include <iostream>
#include <cmath>
#pragma once 


template<typename T>
class complex_number
{
  private:
   T real_; // real part
   T imaginary_;

  public:
   complex_number();
   complex_number(T x, T y);
   complex_number(complex_number const& cc); // copy constructor

   T real() const { return real_; };
   T imaginary() const { return imaginary_; };
   
   T modulus() const;
   T argument() const;
   complex_number compute_power(size_t n) const;

   const complex_number& operator=(const complex_number& cc);

   template<typename S> // Pour éviter le masquage
   friend const complex_number<S> operator+(const complex_number<S>& z1, const complex_number<S>& z2);

   template<typename S > // Pour éviter le masquage
   friend std::ostream& operator<<(std::ostream& os, const complex_number<S>& z);
};


// ========   DEFINITION DES FONCTIONS ======== //


// Set real and imaginary parts to zero
template<typename T>
complex_number<T>::complex_number()
{
    real_ = 0.0;
    imaginary_ = 0.0;
}

// Constructor that sets complex number z=x+iy
template<typename T>
complex_number<T>::complex_number(T x, T y)
{
    real_ = x;
    imaginary_ = y;
}
template<typename T>
complex_number<T>::complex_number(complex_number const& cc):real_(cc.real()), imaginary_(cc.imaginary()){}


// Method for computing the modulus of a complex number
template<typename T>
T complex_number<T>::modulus() const
{
    return std::sqrt(std::pow(real_, 2) + imaginary_ * imaginary_);
}

// Method for computing the argument of a complex number
template<typename T>
T complex_number<T>::argument() const
{
    return atan2(imaginary_, real_);
}

// Method for raising complex number to the power n
// using De Moivre’s theorem - first complex
// number must be converted to polar form
template<typename T>
complex_number<T> complex_number<T>::compute_power(size_t n) const
{
    T modulus       = this->modulus();
    T argument      = this->argument();
    T mod_of_result = pow(modulus, n);
    T arg_of_result = argument * n;
    T real_part     = mod_of_result * std::cos(arg_of_result);
    T imag_part     = mod_of_result * std::sin(arg_of_result);
    complex_number z(real_part, imag_part);
    return z;
}


template<typename T>
const complex_number<T>& complex_number<T>::operator=(const complex_number<T>& cc){
    real_ = cc.real();
    imaginary_ = cc.imaginary();
    return *this;
}

template<typename T>
const complex_number<T> operator+( const complex_number<T>& z1, const complex_number<T>& z2){
    complex_number<T> temp(z1.real()+z2.real(),z1.imaginary()+z2.imaginary());
    return temp;
}

template<typename T>
std::ostream& operator<<(std::ostream& os, const complex_number<T>& z){
    os << z.real() << "+" << z.imaginary() << "i" << std::endl;
    return os;
}