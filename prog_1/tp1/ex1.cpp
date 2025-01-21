#include <iostream>
using namespace std;


int power(int x, size_t a){
    int res = x;
    for (int i=0;i<a;i++){
        res*=x;
    }
    return res;
}


int main(){

    int x = 3; int a = 5;
    
    int res = power(x,a);
    
    cout << res << endl;

}

