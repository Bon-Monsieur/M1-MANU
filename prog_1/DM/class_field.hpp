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

    public:
        field (int test_label , mesh_1d<T> const& msh);
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
field<T>::field(int test_label, mesh_1d<T> const& msh){
    this->n_cells_ = msh.n_cells();
    this->values_.resize(n_cells_);
    
    switch(test_label){
        case 0: // Gauss_pulse
            for (size_t ii = 0; ii < n_cells_; ii++){
                this->values_[ii] = gauss_pulse(msh.xc(ii));
            }
            break;
    }

    
}


