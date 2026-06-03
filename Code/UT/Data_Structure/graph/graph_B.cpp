// Code/UT/Data_Structure/graph/graph_B.pdf
#include <bits/stdc++.h>
using namespace std;
#define int long long

int v, e, t;
vector<vector<int>>vt;

int solve(){
    if(!t){ // BFS廣志
        queue<int>q;
        int vis[v+1] = {0};
        for(int i=1;i<=v;i++){
            if(vis[i] == 0)q.push(i),vis[i]=1;
            while(!q.empty()){
                int x = q.front();
                cout<< x<<" ";
                q.pop();
                for(auto j:vt[x]){
                    if(vis[j] == 0) q.push(j),vis[j]=1;
                }
            }
        }
    }
    else{ // DFS深度
        stack<int>q;
        int vis[v+1] = {0};
        for(int i=1;i<=v;i++){
            if(vis[i] == 0)q.push(i),vis[i]=1;
            while(!q.empty()){
                int x = q.top();
                cout<< x<<" ";
                q.pop();
                for(auto j:vt[x]){
                    if(vis[j] == 0) q.push(j),vis[j]=1;
                }
            }
        }
    }
    return 0;
}

signed main(){
    while(cin>>v>>e>>t &&!( !v && !e && !t)){
        vt.clear();
        vt.resize(v+1); // index-1
        for(int i=0;i<e;i++){
            int x, y;
            cin>>x>>y;
            vt[x].push_back(y);
            vt[y].push_back(x);
        }
        solve();
        cout<<endl;
    }

    return 0;
}