#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};
    
    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;
}

// g++ -c -std=c++20 helloworld.cpp   -> Créer le fichier -o dit "objet"
// g++ helloworld.o -o helloworld     -> Exécute le programme 
