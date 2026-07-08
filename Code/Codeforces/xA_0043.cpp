// https://codeforces.com/problemset/problem/43/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    map<string, int>mp;
    pair<int, string>mx = {0,""};
    while(n--){
        string x;cin>>x;
        mp[x]++;
        if (mp[x] > mx.first) {
            mx = {mp[x], x};
        }
    }
    cout<<mx.second<<'\n';
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}