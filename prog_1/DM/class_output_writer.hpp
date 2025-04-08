#include "class_mesh_1d.hpp"
#include "class_field.hpp"
#include <string>
#include <fstream>
#include <iostream>  // pour std::cerr
#pragma once


template <typename T>
class output_writer{
    protected:
        mesh_1d<T> const& mesh_; // aggregation
        std::string radical_name_;
        
    public:
        output_writer(mesh_1d<T> const& msh, std::string filename ):mesh_(msh) , radical_name_(filename ) { } ;
        inline const mesh_1d<T>& mesh() const {return mesh_; };
        void write_solution ( field <T> solution , std::string loop_counter );
        
};


// ======== DEFINITION ======= //

template<typename T>
void output_writer<T>::write_solution( field<T> solution,std::string loop_counter) {
    std::string nom_fichier = radical_name_ + "_" + loop_counter + ".txt";
    std::ofstream fichier(nom_fichier);

    if (!fichier) {
        std::cerr << " Problème d'bouerture du fichier " << nom_fichier << std::endl;
        
    }

    const std::vector<T>& x = mesh_.cells_centers();
    const std::vector<T>& u = solution();

    if (x.size() != u.size()) {
        std::cerr << "Les deux tableaux n'ont pas la même taille" << std::endl;
        
    }

    for (size_t i = 0; i < x.size(); ++i) {
        fichier << x[i] << " " << u[i] << "\n";
    }

    fichier.close();
}