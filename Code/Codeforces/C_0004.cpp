#include<bits/stdc++.h>
using namespace std;
#define int long long

map<string, int>mp;

void solve(){
    string s;cin>>s;
    cout<<(mp[s] >= 1 ? s+to_string(mp[s]) : "OK")<<"\n";
    mp[s]++;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int t;cin>>t;
    while(t--)solve();
    return 0;
}