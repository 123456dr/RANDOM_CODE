#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m, a, b;
    cin>>n>>m>>a>>b;
    if(b >= a * m){
        cout<<a * n;
        return;
    }
    int ans = 0;
    ans += (b * (n/m));
    if(n/m)n-= m*(n/m);
    ans = min(ans + n*a, ans + b);
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