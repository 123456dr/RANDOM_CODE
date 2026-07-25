// https://cses.fi/problemset/task/1074
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>v(n, 0);
    for(auto &i:v)cin>>i;
    sort(v.begin(), v.end());
    int k = v[n/2];
    int ans = 0;
    for(auto i:v){
        ans += abs(k - i);
    }
    cout<<ans;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}