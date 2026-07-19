// https://cses.fi/problemset/task/1069
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;cin>>s;
    int sz = s.length();
    int mx = 0;
    int cnt = 1;
    for(int i=1;i<sz;i++){
        if(s[i - 1] == s[i])cnt++;
        else mx = max(mx, cnt), cnt = 1;
    }
    mx = max(cnt, mx);
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