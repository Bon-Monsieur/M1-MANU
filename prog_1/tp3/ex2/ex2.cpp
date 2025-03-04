#include <iostream>

using namespace std;

template <typename T>
T sumArray(int N, T* tab){
    T res = 0;
    for (auto ii=0;ii<N;ii++){
        res += tab[ii];
    }
    return res;
}


int main(){
    int N = 10;
    int tab[N];
    for (int ii=0;ii<N;ii++){
        tab[ii] = ii+1;
    }
    int res1 = sumArray(N,tab);
    cout << res1 << endl;
    cout << typeid(res1).name() << endl;

    double tab2[N];
    for (auto ii=0;ii<N;ii++){
        tab2[ii] = ii+1;
    }
    double res2 = sumArray(N,tab);
    cout << res2 << endl;
    cout << typeid(res2).name() << endl;
    return 0;
}