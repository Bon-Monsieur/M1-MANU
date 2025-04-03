#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include <iostream>
#include <vector>
#pragma once

template<typename T>
class residual;


template <typename T>
class time_loop{
    protected:
        size_t iteration_counter_ {0};
        T dt_ {0.};
        T physical_time_ {0.};
        T final_time_ {0.};
        bool last_iteration_ {false };
        double cfl_number_ = 0.5;
        residual<T> residual_ ; // class composition
        mesh_1d<T> const& mesh_; // class aggregation
        
    public:
        time_loop(mesh_1d<T> const& msh, T final_time ) : mesh_(msh) , final_time_ ( final_time ) , residual_(residual<T>(msh)) { };// constructor
        ~time_loop() { };                                                                                                      // destructor
        inline const T final_time () const { return final_time_ ; };
        void run( field <T>& uh);                                                                                // Applique la methode FV sur uh
        void compute_dt( field <T>& uh);                                                                         // Calcule le prochain dt                                         
    
};


// ============ DEFINITION ============ //


template<typename T>
void compute_dt( field <T>& uh){
    this->dt_ = cfl_number_ * mesh_.dx();
}