// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int v, e;
    while(cin>>v>>e && !(!v && !e)){
        vector<vector<int>>val(v+1);
        for(int i=0;i<e;i++){
            int a, b;cin>>a>>b;
            val[a].push_back(b);
            val[b].push_back(a);
        }
        for(auto &i:val){
            sort(i.begin(), i.end());
            //for(auto j:i)cout<<j<<" ";cout<<endl;
        }
        vector<int>vis(v+1, 0);
        queue<int>qu;
        auto bfs = [&]() -> void{
            while(!qu.empty()){
                int x = qu.front();
                qu.pop();
                if(vis[x] == 0)cout<<x<<" ", vis[x] = 1;
                else continue;
                for(auto i:val[x]){
                    if(vis[i] == 0)qu.push(i);
                }
            }
            return;
        };
        qu.push(1);
        bfs();
        cout<<endl;
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}