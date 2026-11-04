// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int v, e;
    while(cin>>v>>e && !(!v && !e)){
        vector<vector<int>>val(v+1);
        for(int i=0;i<e;i++){
            int x, y;cin>>x>>y;
            val[x].push_back(y);
            val[y].push_back(x);
        }
        for(auto &i:val){
            sort(i.begin(), i.end());
        }
        vector<int>vis(v+1, 0);
        auto dfs = [&](auto &self, int id) -> void{
            //cout<<id<<" ";
            vis[id] = 1;
            for(auto i:val[id]){
                if(vis[i] == 0)self(self, i);
            }
            cout<<id<<" ";
        };
        dfs(dfs, 1);
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}