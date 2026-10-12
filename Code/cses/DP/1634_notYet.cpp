#include <bits/stdc++.h>
using namespace std;
#define int long long 

void solve(){
    int n;cin>>n;
    int tar;cin>>tar;
    vector<int>v(n+1, 1e7);
    vector<int>coin(n);
    v[0] = 1;
    for(auto &i:coin)cin>>i, v[i] = 1;
    for(int i=1;i<=n;i++){
        for(int j=0;j<n;j++){
            if(i - coin[j] == 0)
                v[i] = min(v[i], v[i - coin[j]] + 1);
        }
    }
    if(v[tar] == 1e7)cout<<-1;
    else cout<<v[tar];
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}