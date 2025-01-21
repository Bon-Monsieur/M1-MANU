#include <iostream>

using namespace std;

double factorial(int n) {
    if (n == 0 || n == 1) return 1;
    double res = 1;
    for (int i = 2; i <= n; i++) {
        res *= i;
    }
    return res;
}

int main(){
    
    double res = factorial(10);
    cout << res << endl;
}