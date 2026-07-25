// https://cses.fi/problemset/task/2216
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    map<int, int>mp;
    int n;cin>>n;
    int ans = 0;
    while(n--){
        int x;cin>>x;
        if(mp.find(x-1) == mp.end())ans++;//, cout<<x;
        mp[x] = 1;
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