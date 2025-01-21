#include <iostream>

using namespace std;

double expTaylor(double x, int N){
    double res = 1; // Variable de la somme 
    double temp = 1;
    for (int i=1;i<N;i++){ // Boucle pour calculer x**k/fact(k) rapidement 
            temp*=x/i;
            res += temp;
    }

    return res;
}


int main(){

    double x = 2;
    int N = 100;

    cout << expTaylor(x,N) << endl;

    return 0;

}