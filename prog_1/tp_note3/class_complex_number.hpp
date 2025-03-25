#pragma once

#include <iostream>

class complex_number
{
  private:

   double real_; // real part
   double imaginary_;

  public:

   complex_number();
   complex_number(double x, double y);
   complex_number(complex_number const& cc);
   double real() const { return real_; };
   double imaginary() const { return imaginary_; };
   
   double modulus() const;
   double argument() const;
   complex_number compute_power(size_t n) const;
};
