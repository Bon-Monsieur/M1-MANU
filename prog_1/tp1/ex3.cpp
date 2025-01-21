#include <iostream>

using namespace std;


int main(){

    int n = 5;
    int triangle[n][n];
    triangle[0][0]=1;
    
    for (int i=0;i<n;i++){
        triangle[i][0] = 1;

        for (int j=1;j<n;j++){
            triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j];
        }
    }

    for (int i=0;i<n;i++){
        for (int j=0;j<n;j++){
            cout << triangle[i][j] << " ";
        }

        cout << endl;
    }

    return 0;
}