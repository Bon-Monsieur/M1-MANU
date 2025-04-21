#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include "class_residual.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#pragma once



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
void time_loop<T>::compute_dt(field <T>& uh){
    
    double maximum = 0.0;
    for (size_t ii = 0; ii < uh().size(); ++ii) {
        maximum = std::max(maximum, std::abs(uh.fp_()(uh(ii)))); // Selectionne le max des F'(uh)
    }
    this->dt_ = cfl_number_ * mesh_.dx() / maximum;   // A modifier en fonction du F 
}


template<typename T>
void time_loop<T>::run(field <T>& uh){
    
    while (physical_time_ < final_time_ && !last_iteration_){
        compute_dt(uh); // Calcul du dt
        if (physical_time_ + dt_ > final_time_){ 
            dt_ = final_time_ - physical_time_; 
            last_iteration_ = true; 
        }
        residual_.assemble_from_field(uh); // Calcul le residual par rapport a uh
        uh += (dt_*residual_);
        
        physical_time_ += dt_; // Incremente le temps physique
        iteration_counter_++;   // Incremente le compteur d'iteration
        
    }
    
}