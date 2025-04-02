#include <iostream>
#include <vector>
#pragma once

template <typename T>
class mesh_1d{
    protected:
        std::vector<T> vertices_coordinates_ ; // composition
        std::vector<T> cells_centers_ ; // composition
        size_t n_vertices_{0};
        size_t n_cells_{0};
        T dx_;

    public:
        mesh_1d(T x_left , T x_right , size_t n_cells );
        ~mesh_1d() { };
        inline const size_t n_vertices() const { return n_vertices_ ; };
        inline const size_t n_cells() const { return n_cells_ ; };
        inline const T dx() const { return dx_; };
        inline T xc( size_t ii ) const { return cells_centers_ [ ii ]; };
        void print();
    
};


// ============ DEFINITION ============ // 

template<typename T>
mesh_1d<T>::mesh_1d(T x_left,T x_right, size_t n_cells){
    
    this->n_cells_ = n_cells;
    this->n_vertices_ = n_cells + 1;
    this->dx_ = (x_right-x_left)/n_cells;

    this->vertices_coordinates_.resize(n_vertices_);
    this->cells_centers_.resize(n_cells_);

    for (size_t ii = 0; ii < n_vertices_; ii++){
        this->vertices_coordinates_[ii] = x_left + ii*dx_;
    }
    for (size_t ii = 0; ii < n_cells_; ii++){
        this->cells_centers_[ii] = x_left + (ii+0.5)*dx_;
    }
}

template<typename T>
void mesh_1d<T>::print(){
    std::cout << "Mesh define over [" << vertices_coordinates_[0] << ", " << vertices_coordinates_.back()<< "]" << std::endl;
    std::cout << "Number of vertices : " << n_vertices () << std::endl;
    std::cout << "Number of cells : " << n_cells() << std::endl;
    std::cout << "dx : " << dx() << std::endl;
}
