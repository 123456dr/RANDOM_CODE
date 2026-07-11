// https://codeforces.com/problemset/problem/189/A
/*
經典 dp 走石階問題
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, a, b, c;
    cin>>n>>a>>b>>c;
    vector<int>dp(n+1, 0);
    dp[0] = 1;
    for(int i=1;i<=n;i++){
        dp[i] = max({(i-a>=0 && dp[i-a]>0 ? dp[i-a]+1 : 0), (i-b>=0 && dp[i-b]>0 ? dp[i-b]+1 : 0), (i-c>=0 && dp[i-c]>0 ? dp[i-c]+1 : 0)});
    }
    cout<<dp[n]-1;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}