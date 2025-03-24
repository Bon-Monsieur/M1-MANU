#include <iostream>
#include "class_matrix.hpp"

template<int M, int N, typename T>
std::ostream& operator<<(std::ostream& os, const Matrix<M, N, T>& mat) {
    for (int i = 0; i < M; i++) {
        os << "  [ ";
        for (int j = 0; j < N; j++) {
            os << mat[i][j] << " ";  // Accès aux éléments
        }
        os << "]\n";
    }
    return os;
}


int main() {

    double xx[2][2]={{1. , 2.} ,{3. , 4.}};
    Matrix<2,2,double> N1(xx);
    double yy[2][2]={{5. , 6.} ,{7. , 8.}};
    Matrix<2,2,double> N2(yy);
    
    std::cout << N2*N1;



    return 0;
}