#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    int i = 5;
    bool m = 0<=i && i<=6;
    cout << !m; 
    return 0;
}

// g++ -c -std=c++20 helloworld.cpp   -> Créer le fichier -o dit "objet"
// g++ helloworld.o -o helloworld     -> Exécute le programme 
