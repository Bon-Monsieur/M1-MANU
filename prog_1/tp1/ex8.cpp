#include <iostream>
using namespace std;

double scalar_product(double* v1,double* v2,int n){

    double sum = 0;

    for (int i=0;i<n;i++){
        sum+=v1[i]*v2[i];
    }
    return sum;
}


int main(){

    int n;
    cin >> n;
    double* v1 = new double[n]{1,5,7};
    double* v2 = new double[n]{2,2,1};

    for (int i=0;i<n;i++){
        v1[i]=i;
        v2[i]=i;
    }

    double ps = scalar_product(v1,v2,n);
    cout << "Le produit scalaire vaut " << ps << endl;

    delete [] v1;
    delete [] v2;
    return 0;
}