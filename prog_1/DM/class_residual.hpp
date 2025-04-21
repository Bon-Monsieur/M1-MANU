#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#pragma once

template <typename T>
class residual {
    protected:
        std::vector<T> values_; // composition
        mesh_1d<T> const& mesh_; // aggregation
    
    public:
        residual (mesh_1d<T> const& mesh):mesh_(mesh) { } ;
        const mesh_1d<T>& mesh() const { return mesh_; };
        inline const size_t n_cells () const { return mesh_.n_cells() ; };

        inline void clear () {values_.clear() ; } ;
        inline const std::vector<T>& operator()() const { return values_; };
        T operator()( size_t ii ) const { return values_[ ii ] ; } ;

        void assemble_from_field( field <T> const& uh);     
        
        template <typename S>
        friend residual<S> operator*(S lambda, residual<S> const& res) {
            residual<S> res_new(res.mesh());
            res_new.values_.resize(res.n_cells());

            for (size_t ii = 0; ii < res.n_cells(); ++ii) {
                res_new.values_[ii] = lambda * res(ii);
            }
            return res_new;
        }

};


// ============ DEFINITION ============ //

template <typename T>
T flux_Burgers(T const& u)
{
    return 0.5*u*u;
}


template <typename T, typename Func>
T flux_LF(T const ul , T const ur , T max_vel, Func flux )    // Fi+1/2
{
    return 0.5*( flux (ul) + flux (ur) - max_vel*(ur-ul));
}


template<typename T>
void residual<T>::assemble_from_field(field <T> const& uh){
    values_.resize(uh().size()); 
    double maximum = 0.0;
    for (size_t ii = 0; ii < uh().size(); ++ii) {
        maximum = std::max(maximum, std::abs(uh(ii))); // Selectionne le max des uh
    }

    T (*flux)(T const&) = flux_Burgers<T>;

    for (size_t ii = 0; ii < uh().size(); ++ii) {
        if (ii == 0) {
            values_[ii] = -1.0/ mesh_.dx() * (flux_LF<T>(uh(ii), uh(ii+1), maximum, flux) - flux_LF<T>(uh(ii), uh(ii), maximum, flux));
        } else if (ii == uh().size()-1) {
            values_[ii] = -1.0/ mesh_.dx() * (flux_LF<T>(uh(ii), uh(ii), maximum, flux) - flux_LF<T>(uh(ii-1), uh(ii), maximum, flux));
        } else
        values_[ii] = -1.0/ mesh_.dx() * (flux_LF<T>(uh(ii), uh(ii+1), maximum, flux) - flux_LF<T>(uh(ii-1), uh(ii), maximum, flux));
    }
}