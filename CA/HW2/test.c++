#include <iostream>

using namespace std;


int main(){
	int s0, s1, s2, ans;
	cin >> s0 >> s1 >> s2;

	switch (s1) {
		case 0 :
			cout << s0 + s2 << '\n';
			break;
		case 1 :	
			cout << s0 - s2 << '\n';
			break;
		case 2 : 
			cout << s0 * s2 << '\n';
			break;
		case 3 :
			cout << s0 / s2 << '\n';
			break;
		case 4 :
			ans = (s1 <= s2) ? s1 : s2;
			cout << ans << '\n';
			break;
		case 5 :
			ans = 1;
			while (s2 >= 0) {
				ans *= s0;
				s2 --;
			}
			cout << s2 << '\n';
			break;
		case 6 :
			ans = 1;
			while (s0 >0 ) {
				ans *= s0;
				s0 --;
			}
			cout << ans << '\n';
			break;
	}
}
