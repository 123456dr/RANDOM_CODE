// Code/UT/Data_Structure/graph/graph_B.pdf
#include <bits/stdc++.h>
using namespace std;
#define int long long

int v, e, t;
vector<vector<int>>vt;


void dfs(int x, vector<int>&vis){
    if(vis[x] == 1)return;
    vis[x] = 1;
    cout<<x<<" ";
    for(auto i:vt[x]){
        if(vis[i] == 0)dfs(i, vis);
    }
}


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
        vector<int>vis(v+1,0);
        for(int i=1;i<=v;i++){
            if(vis[i] == 0){
                dfs(i, vis);
            }
            
        }
    }
    return 0;
}
/*
1 2 4 
2 3 
3 2 
4 1 
*/
bool cmp(int a, int b){
    return a>b;
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
        if(t==1)for(auto &i:vt){
            sort(i.begin(), i.end(),cmp);
        }
        else{
            for(auto &i:vt){
            sort(i.begin(), i.end());
        }
        }
        solve();
        cout<<endl;
    }

    return 0;
}