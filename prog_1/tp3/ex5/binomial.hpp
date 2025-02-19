#include <iostream>
using namespace std;
#pragma once


template<int M>
class Binomial;




// ================



template<int M>
class Binomial{
    private:
        double coeff[M][M];

    public:
        Binomial();
        double operator()(int n,int k) const;

};

template<int M>
Binomial<M>::Binomial(){
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < M; j++) {
            coeff[i][j] = 0;
        }
    }
    coeff[0][0]=1;
    
    for (int i=1;i<M;i++){
        coeff[i][0] = 1;

        for (int j=1;j<M;j++){
            if (j<=i){
                 coeff[i][j] = coeff[i-1][j-1] + coeff[i-1][j];
            }
            else{
                coeff[i][j]=0;
            }
           
        }
    }
}


template<int M>
double Binomial<M>::operator()(int n,int k) const {
    return coeff[n][k];
}


template<int M>
std::ostream& operator <<(std::ostream& os, const Binomial<M>& triangle){  // Overloading operator << to print 
    for (int i=0;i<M;i++){
        for (int j=0;j<M;j++){
            cout << triangle(i,j) << " ";
        }
        cout << endl;
    }
    return os;
}