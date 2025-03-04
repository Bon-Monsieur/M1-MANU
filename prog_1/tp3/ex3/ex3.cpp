#include <iostream>
#include <cmath>

using namespace std;


template<typename T>
T coefLag(int i, T x_in, T* vx, const int n){   // Calcule les coefficients L_i(x_in)
    T res = 1;
    for(int jj=0;jj<n+1;jj++){
        if (jj!=i){
            res *= (x_in-vx[jj])/(vx[i]-vx[jj]);
        }
        
    }
    return res;
}


template <typename T> 
T lagrange(T* vx, T* vy, T x_in, const int n){ // Evalue Pn au point x_in
    T Pn = 0;
    for(int ii=0;ii<n+1;ii++){
        Pn += vy[ii]*coefLag(ii,x_in,vx,n);
    }
    return Pn;
}



int main(){
    const int n = 3;
    double xi[n+1];
    for (int ii=0;ii<n+1;ii++){  // Initialisation des x_i
        xi[ii] = 1+ii/4.0;
    } 

    double yi[n+1];
    for (int ii=0;ii<n+1;ii++){ // Initialisation des y_i
        yi[ii] = exp(xi[ii]);
    } 
    double res = lagrange(xi,yi,(double)1.4,n);
    cout << res << endl;
    cout << typeid(res).name() << endl;

    return 0;
}