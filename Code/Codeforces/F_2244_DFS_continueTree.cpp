// https://codeforces.com/contest/2244/problem/F
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<vector<int>>v(n+1);
    for(int i=2;i<=n;i++){
        int x;cin>>x;
        v[x].push_back(i);
    }
    vector<int>a(n);
    for(auto &i:a)cin>>i;

    vector<pair<int, int>>line;
    auto dfs = [&](auto &self, int u) -> tuple<int ,int, int>{
        if(v[u].empty()){
            return {a[u-1], a[u-1], 1};
        }
        int mx = 0, mn = 1e9, sz = 0;
        vector<int>mns;
        for(auto i:v[u]){
            auto [c_mn, c_mx, c_sz] = self(self, i);
            if(c_mx == -1)return {-1, -1, -1};
            mx = max(c_mx, mx);
            mn = min(c_mn, mn);
            sz += c_sz;
            mns.push_back(c_mn);
        }
        if(sz < mx-mn+1)return {-1, -1, -1};
        int cnt = 0;
        for(int i=1;i<mns.size();i++){
            if(mns[i-1] > mns[i])cnt++;
        }
        if(mns.back() > mns.front()) cnt++;
        if(cnt > 1)return {-1, -1, -1};
        return {mn, mx, sz};
    };

    auto [mn, mx, cnt] = dfs(dfs, 1);
    if(mn == -1 || mx == -1 || cnt == -1){
        cout<<"NO\n";
        return;
    }
    cout<<"YES\n";
    return;

}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}