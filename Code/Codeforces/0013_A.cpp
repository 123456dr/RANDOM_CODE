// https://codeforces.com/contest/13/problem/A

/* 進位制轉換 % /
while (num > 0) {
    int remainder = num % N; // 取出最低位
    num /= N;                // 降階消去最低位
} 
// 依序取得的餘數即為從低到高的位數
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n;
    while(cin>>n){
        int N = n;
        int sum = 0;
        for(int i=2;i<N;i++){
            n = N;
            while(n>0){
                sum += n%i;
                n/=i;
            }
        }
        cout<<sum/gcd(sum, N-2)<<"/"<<(N-2)/gcd(sum, N-2)<<endl;

    }

    return 0;
}