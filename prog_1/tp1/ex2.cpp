#include <iostream>

using namespace std;

int factorial(int n){
    int res = 1;

    while(n>1){
        res*=n-1;
        n-=1;
    }
    return res;
}

int main(){
    
    int res = factorial(10);
    cout << res << endl;
}