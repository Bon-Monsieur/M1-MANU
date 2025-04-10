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
        T operator()( size_t ii ) const { return values_[ ii ] ; } ;

        void assemble_from_field( field <T> const& uh);     
        
        template <typename S>
        friend residual<S> operator*(S lambda, residual<S> const& res );

};


// ============ DEFINITION ============ //

template <typename T>
T flux_Burgers(T const& u)
{
    return 0.5*u*u;
}


template <typename T, typename Func>
T flux_LF(T const& ul , T const& ur , T max_vel, Func flux )
{
    return 0.5*( flux ( ul ) + flux (ur )) - 0.5/max_vel*(ur-ul );
}


template<typename T>
void residual<T>::assemble_from_field(field <T> const& uh){
    values_.resize(uh().size()); 

    for (size_t ii = 1; ii < uh().size()-1; ++ii) {
        values_[ii] = -uh()(ii);
    }
}