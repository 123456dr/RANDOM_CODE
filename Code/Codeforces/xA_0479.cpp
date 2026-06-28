#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int a, b, c;cin>>a>>b>>c;
    cout<<max({a+b*c, a*(b+c), a*b*c, (a+b)*c, a+b+c});
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}