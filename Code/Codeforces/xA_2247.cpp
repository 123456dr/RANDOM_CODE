// https://codeforces.com/contest/2247/problem/A
/*
- 長度偶數個才可 n/2 個 -1 抵銷 n/2 個 1
- 每次可改變相鄰兩個數的符號變相等於可以改變任意兩個位置的數字的符號
所以每次可以 +2/-2 個 -1/1 數量，目標是要有 n/2 個 -1/1
所以只要 n/2 和 -1/1 的奇偶相同就一定可透過 +-2 改變得到
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int cnt = 0;
    int k = n >> 1;
    int N = n;
    while(n--){
        int x;cin>>x;
        if(x == -1)cnt++;
    }
    if(N & 1){cout<<"NO\n";return;}
    cout<<((cnt & 1) == (k & 1) ? "YES\n" : "NO\n");
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}