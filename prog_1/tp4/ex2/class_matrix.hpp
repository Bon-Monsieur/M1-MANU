#include "class_vector.hpp"
#include <iostream>
#pragma once



template<int N,int M,typename T>
class Matrix : public Vector<M,Vector<N,T>>{
    public:
        Matrix();
        Matrix(T xx);
        Matrix(T tab[N][M] );
        T& operator()( int i , int j ) ;
        /*const T& operator()( int i , int j ) ;
        const T& operator()( int i , int j ) const ;*/
        
        getCoord(){return this->coord;}
        
        friend Matrix<M, N, T> transpose(const Matrix<N, M, T>& mat) {
            Matrix<M, N, T> result;
        
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    result(j, i) = mat(i, j);
                }
            }
        
            return result;
        }

        friend Matrix operator+(const Matrix<N,M,T>& M1,const Matrix<N,M,T>& M2){
            Matrix<N,M,T> temp;
            for (int ii=0;ii<M;ii++){
                temp[ii] = M1[ii] + M2[ii];  // use Vector's operator+ 
            }
            return temp;
        }

        friend Matrix operator-(const Matrix<N,M,T>& M1,const Matrix<N,M,T>& M2){
            Matrix<N,M,T> temp;
            for (int ii=0;ii<M;ii++){
                temp[ii] = M1[ii] - M2[ii];  // use Vector's operator+ 
            }
            return temp;
        }
        
        friend const Matrix<N, N, T> operator+(const Matrix<N, N, T>& mat, const T& lambda){
            Matrix<N,M,T> temp;
            Vector<N,T> col;
            for (int ii=0;ii<M;ii++){
                col.zero();
                col[ii] = lambda;
                temp[ii] = mat[ii] + col;  // use Vector's operator+ 
            }
            return temp;
        }
        
        
        friend const Matrix<N, N, T> operator+( const T& lambda,const Matrix<N, N, T>& mat){
            Matrix<N,M,T> temp;
            Vector<N,T> col;
            for (int ii=0;ii<M;ii++){
                col.zero();
                col[ii] = lambda;
                temp[ii] = mat[ii] + col;  // use Vector's operator+ 
            }
            return temp;
        }

        
        friend const Matrix<N, M, T> operator*(const Matrix<N, M, T>& mat, const T& lambda){
            Matrix<N,M,T> temp;
            for (int ii=0;ii<M;ii++){
                temp[ii] = mat[ii]*lambda; // use Vector's operator+ 
            }
            return temp;
        }
        
        friend const Matrix<N, M, T> operator*(const T& lambda,const Matrix<N, M, T>& mat){
            Matrix<N,M,T> temp;
            for (int ii=0;ii<M;ii++){
                temp[ii] = mat[ii]*lambda; // use Vector's operator+ 
            }
            return temp;
        }

        const Matrix& operator*=(const T& lambda);

        friend const Vector<N,T> operator*(const Matrix<N, M, T>& mat,const Vector<N,T>& v){
            Vector<N,T> temp;
            for (int ii=0;ii<M;ii++){
                temp[ii] = mat[ii]*v; // use Vector's product (scalar product)
            }
            return temp;
        }

        
        template<int P>
        friend Matrix<N, P, T> operator*(const Matrix<N, M, T>& mat1, const Matrix<M, P, T>& mat2) {
            Matrix<N, P, T> result;
        
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < P; j++) {
                    result(i, j) = 0;  // Initialisation à zéro
                    for (int k = 0; k < M; k++) {
                        result(i, j) += mat1(i, k) * mat2(k, j);
                    }
                }
            }
        
            return result;
        }
        
        
        
};

template<int N,int M,typename T>
Matrix<N,M,T>::Matrix() : Vector<M, Vector<N, T>>(){
    for (int ii = 0; ii < M; ii++) {
        this->coord[ii] = Vector<N,T>(); // Initialisation des colonnes à 0
    }
}

template<int N,int M,typename T>
Matrix<N,M,T>::Matrix(T xx) : Vector<M, Vector<N, T>>(xx){
}

template<int N,int M,typename T>
Matrix<N,M,T>::Matrix(T tab[N][M]){     // Constructor par copie
    for (int ii=0;ii<M;ii++){
        this->coord[ii] = Vector<N,T>(tab[ii]);
    }
}
/*
template<int N,int M,typename T>
const T& Matrix<N,M,T>::operator()(int i,int j) {  //Getter
    return this->coord[i][j];
}

template<int N,int M,typename T>
const T& Matrix<N,M,T>::operator()(int i,int j) const {  //Getter
    return this->coord[i][j];
}
*/


template<int N,int M,typename T>
T& Matrix<N,M,T>::operator()(int i,int j) {  //Getter
    return this->coord[i][j];
}


template<int N,int M,typename T>
const Matrix<N,M,T>& Matrix<N,M,T>::operator*=(const T& lambda){
    for (int ii=0;ii<M;ii++){
        this->coord[ii] = this->coord[ii]*lambda; 
    }
    return (*this);
}