// https://codeforces.com/problemset/problem/158/A
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, k;cin>>n>>k;
    vector<int>v(n);
    for(auto &i:v)cin>>i;
    int ans = 0;
    for(auto i:v)if(i >= v[k-1] && i>0)ans++;
    cout<<ans;
    return;
}


signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}