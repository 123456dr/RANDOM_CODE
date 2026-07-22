// https://cses.fi/problemset/task/1643
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>pref(n+1, 0);
    int mx = -2e18, mn = 0;
    for(int i=1;i<=n;i++){
        int x;cin>>x;
        pref[i] = pref[i-1] + x;
        mx = max(pref[i] - mn, mx);
        mn = min(mn, pref[i]);
        //cout<<pref[i]<<" "<<mn<<'\n';
    }
    cout<<mx;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}