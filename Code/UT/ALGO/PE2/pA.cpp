// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int v, e, type;
    while(cin>>v>>e>>type && !(!v && !e && !type)){
        deque<int>dq;
        vector<vector<int>>val(v+1);
        vector<int>vis(v+1, 0);

        while(e--){
            int x, y;cin>>x>>y;
            val[x].push_back(y);
            val[y].push_back(x);
        }
        for(auto &i:val){
            sort(i.begin(), i.end());
        }

        auto bfs = [&]() -> void{
            while(!dq.empty()){
                int tmp = dq.front();
                dq.pop_front();
                if(vis[tmp] == 0){
                    cout<<tmp<<" ";
                    vis[tmp] = 1;
                    for(auto i:val[tmp])dq.push_back(i);
                }
            }
            return;
        };

        auto dfs = [&](auto &self) -> void{
            while(!dq.empty()){
                int tmp = dq.back();
                dq.pop_back();
                if(vis[tmp] == 0){
                    cout<<tmp<<" ";
                    vis[tmp] = 1;
                    for(auto i:val[tmp])if(vis[i] == 0)dq.push_back(i);
                }
            }
            return;
        };

        dq.push_back(1);
        if(type == 0){
            bfs();
        }
        else dfs(dfs);
        cout<<endl;
    }
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}