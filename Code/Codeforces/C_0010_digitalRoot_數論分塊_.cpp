/*
1 <= A, B, C <=N
ans = [d(AB) = d(C)組數] - [AB = C組數]
- 數位根(digit root) d(X) mod 9 = X mod 9 (%9 ==0 視為9, digit root = 1~9)
- d(AB) = d(C) => cnt[A] * cnt[B] * cnt[C]
- AB = C 組數 => N/i總和(1<= i <=N, i = Ai, N/i = Bi)

數論分塊: (未套用優化 O(n) => O(sqrt(n)))
i = 1~10, 10/[4~5]整數部分都為2；10/[6~10]整數部分都為2
- 分塊 n/L, R = n / (n/L), 分塊個數為 R-L+1
    - 10/4, R = 10 / (2) = 5, 分塊個數為 5-4+1 = 2
    - 10/6, R = 10 / (1) = 10, 分塊個數為 10-6+1 =5 
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int ans = 0;
    vector<int>cnt(10, 0);
    for(int i=1;i<=n;i++){  // O(n)
        cnt[(i-1)%9+1]++;
    }
    for(int i=1;i<=9;i++){  // O(9*9) = O(1)
        for(int j=1;j<=9;j++){
            ans += cnt[i] * cnt[j] * cnt[(i*j-1)%9+1];
        }
    }
    for(int i=1;i<=n;i++){
        ans -= (n/i);
    }
    cout<<ans;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}