#include <iostream>
using namespace std;

// https://fr.wikibooks.org/wiki/Programmation_C-C%2B%2B/Pointeurs_et_r%C3%A9f%C3%A9rences_de_fonctions

double myFunction(double x ) {
    return x*x;
}

double myOtherFunction(double x ) {
    return x*x*x;
}


int main(){

    double x = 3;
    double (*p_function)(double x); // Déclaration d'un pointeur de fonction
    p_function = &myFunction; // Le pointeur pointe vers l'adresse de myFunction
    cout << "pointe vers myFunction = " << (*p_function)(x) << endl;
    // cout << "pointe vers myFunction = " << p_function(x) << endl;    fonctionne aussi si envie
    p_function = &myOtherFunction; // Maintenant le pointeur pointe vers l'adresse de myOtherFunction
    cout << "pointe vers myOtherFunction = " << (*p_function)(x) << endl; 
    // cout << "pointe vers myOtherFunction = " << (*p_function)(x) << endl; fonctionne aussi si envie
    return 0;
}