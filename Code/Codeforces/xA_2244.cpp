#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    string s;cin>>s;
    int mx = 0;
    int cnt = 0;
    for(auto i:s){
        if(i == '#')cnt++;
        else{
            mx = max(cnt, mx);
            cnt = 0;
        }
    }
    mx = max(cnt, mx);
    cout<<(mx+1)/2<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}