#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t;cin>>t;
    vector<int>v(5, 0);
    while(t--){
        int x;cin>>x;
        v[x]++;
    }
    v[1] = ((v[1] - v[3]) >= 0 ? v[1]-v[3] : 0);
    v[1] = (v[2] % 2 == 1 ? (v[1]-2 >= 0 ? v[1]-2 :0) : v[1]);
    int ans = v[4] + v[3] + v[2]/2 + v[2]%2 + v[1]/4 + (v[1]%4 ? 1 : 0);
    cout<<ans;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}