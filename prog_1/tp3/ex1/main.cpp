#include "test.hpp"




int main() {

    int x1 = 5;
    cout << square(x1) << endl;
    cout << typeid(square(x1)).name() << endl;
    double x2 = 5.;
    cout << square(x2) << endl;
    cout << typeid(square(x2)).name() << endl;

    return 0;

}