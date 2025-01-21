#include <iostream>
using namespace std;

// Exo 1
int power(int x, size_t a){
    int res = x;
    for (int i=0;i<a;i++){
        res*=x;
    }
    return res;
}

// Exo 2
int factorial(int n){
    int res = 1;

    while(n>1){
        res*=n-1;
        n-=1;
    }
    return res;
}

int main(){

    int x = 3; int a = 5;
    
    int res1 = power(x,a);
    int res2 = factorial(10);
    cout << res1 << endl;
    cout << res2 << endl;
}

