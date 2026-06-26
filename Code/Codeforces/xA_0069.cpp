#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t;cin>>t;
    int a=0, b=0, c=0;
    while(t--){
        int x, y, z;
        cin>>x>>y>>z;
        a+=x, b+=y, c+=z;
    }
    if(!a && !b &&!c)cout<<"YES";
    else cout<<"NO";
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}