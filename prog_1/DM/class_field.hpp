#include "class_mesh_1d.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#pragma once

template<typename T>
class residual;

template<typename T>
class field{
    protected:
        std::vector<T> values_; // composition
        size_t n_cells_{0};
        T (*flux)(T const&); // pointer to flux function
        T (*fp)(T const&); // pointer to derivative function

    public:
        field (int test_label , mesh_1d<T> const& msh, T (*flux)(T const&), T(*fp)(T const&)) ; 
        inline T (*flux_() const)(T const&) { return flux; }
        inline T (*fp_() const)(T const&) { return fp; }
        inline const size_t n_cells () const { return n_cells_ ; };
        inline const std::vector<T>& operator()() const { return values_; };
        
        inline double operator()( size_t ii ) const { return values_[ ii ] ; };
        field<T>& operator+=(residual<T> res );

};

// ============ POSSIBLES U0 ============ //
double gauss_pulse(double xx){
    return exp(-pow((xx-5.) ,2));
}

// =========== DEFINITION ============ //

template<typename T>
field<T>::field(int test_label, mesh_1d<T> const& msh, T (*flux)(T const&),T (*fp)(T const&)){
    this->n_cells_ = msh.n_cells();
    this->values_.resize(n_cells_);
    this->flux = flux; 
    this->fp = fp;  
    
    switch(test_label){     // 0 = gauss_pulse ; 1 = test
        case 0: 
            for (size_t ii = 0; ii < n_cells_; ii++){
                this->values_[ii] = gauss_pulse(msh.xc(ii));
            }
            break;
    }
}

template<typename T>
field<T>& field<T>::operator+=(residual<T> res ){
    for (size_t ii = 0; ii < n_cells_; ++ii) {
        this->values_[ii] = this->values_[ii]+res(ii);
    }
    return *this;
}

