//
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define mod  (1e9+7)

void solve(){
    int n;cin>>n;
    vector<int>v(n+1, 0);
    v[0] = 1;
    for(int i=1;i<=n;i++){
        for(int j=1;i-j>=0 && j<=6;j++){
            v[i] += v[i-j];
            v[i] %= (int)mod;
        }
    }
    cout<<v[n];
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}