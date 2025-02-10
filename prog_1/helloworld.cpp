#include <iostream>
#include <vector>
#include <string>

using namespace std;


void Fibonnaci(size_t n, double* res){
    if (n<=0){
        throw("n doit être strictement positif");
    }
    if (n==1){
        res[0]=0;
    }
    if (n==2){
        res[1]=1;
    }
    else{
        double u1 = 0;
        double u2 = 1;
        res[0]=0;
        res[1]=1;
        double temp;
        for (size_t ii=2;ii<n;ii++){
            temp = u2;
            u2 = u2 + u1;
            u1 = temp;
            res[ii]=u2;
        }
    }
}


void afficherTableau(double* tab, int n){
    cout << "["; 
    for (int ii=0;ii<n-1;ii++){
        cout << tab[ii] << ",";
    }
    cout << tab[n-1] << "]" << endl;
}


int main()
{
    int n = 30;
    double* res = new double[n];
    Fibonnaci(n,res);
    afficherTableau(res,n);

    return 0;
}

// g++ -c -std=c++20 helloworld.cpp   -> Créer le fichier -o dit "objet"
// g++ helloworld.o -o helloworld     -> Exécute le programme 
