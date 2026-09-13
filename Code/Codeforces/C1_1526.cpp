// https://codeforces.com/problemset/problem/1526/C1
#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>val(n);for(auto &i:val)cin>>i;
    vector<int>v(n+1, -1);
    v[0] = 0;
    for(int i=0;i<n;i++){
        for(int j=i+1;j>0;j--){
            if(v[j-1] != -1 && v[j-1] + val[i] >= 0){
                v[j] = max(v[j], v[j-1] + val[i]);
            }
        }
    }

    for(int i=n;i>=0;i--){
        if(v[i] != -1){
            cout<<i;
            return;
        }
    }
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}