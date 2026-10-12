// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;
    while(cin>>n && n){
    map<string, vector<string>> mp;
    map<string, int>val;
    for(int i=0;i<n;i++){
        string x;int y;
        cin>>x>>y;
        val[x] = y;
    }
    set<string>nroot;
    for(int i=0;i<n-1;i++){
        string x, y;
        cin>>x>>y;
        mp[x].push_back(y);
        nroot.insert(y);
    }
    string rot;
    for(auto i:val){
        if(nroot.find(i.first) == nroot.end()){
            rot = i.first;
            break;
        }
    }

    auto dfs = [&](auto &self, string r) -> pair<int, int>{
        int rskip = 0;
        int rtake = val[r];
        for(auto i:mp[r]){
            auto [cskip, ctake] = self(self, i);
            rskip += max(cskip, ctake);
            rtake += cskip;
        }
        return {rskip, rtake};

    };
    auto [a, b] = dfs(dfs, rot);
    cout<<max(a, b)<<endl;
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}