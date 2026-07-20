// https://codeforces.com/problemset/problem/1398/C
/*
pref[r] - pref[l-1] = r - (l - 1)
=> pref[r] - r = pref[l-1] - (l - 1)
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>pref(n+1, 0);
    vector<int>v(n+1, 0);
    string s;cin>>s;
    for(int i=0;i<n;i++){
        pref[i+1] = pref[i] + (s[i] - '0');
        v[i+1] = pref[i+1] - (i+1);
    }
    map<int, int>mp;
    for(int i=0;i<=n;i++){
        mp[v[i]]++;
    }
    int ans = 0;
    for(auto k:mp){
        int i = k.second;
        ans += (i *(i-1))/2;
    }
    cout<<ans<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}