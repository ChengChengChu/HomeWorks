#include <iostream>

using namespace std;

int T(int n){
    if (n == 0) return 0;
    else if (n == 1) return 1;
    else {
        return 2 * T(n - 1) + T(n - 2);
    }
}

int main(){
    for (int i = 0; i < 16; i ++)
        cout << T(i) << '\n';
}
