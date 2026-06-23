// https://codeforces.com/problemset/problem/71/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;cin>>s;
    int sz = s.length();
    if(sz<=10){
        cout<<s;
    }
    else{
        cout<<s[0]<<sz-2<<s[sz-1];
    }
    return;
}


signed main(){
    int t;cin>>t;
    while(t--){
        solve();
        cout<<"\n";
    }
    return 0;
}