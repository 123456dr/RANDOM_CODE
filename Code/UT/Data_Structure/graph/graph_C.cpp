// Code/UT/Data_Structure/graph/graph_C.pdf
/*
深度優先加剪枝，遍歷各條路徑並更新最小值
- DFS 時有任意一項累加超過 100% 則剪枝
- 已記錄至少一組解答時，若當前 DFS se 累加高於已記錄結果之 se 則剪枝
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long

int ansSt = 100, ansSe = 100;
int isAns = 0;
void dfs(vector<int>&vis, vector<vector<pair<int,pair<int,int>>>> &v, int from, int to, int st, int se){
    if(st>=100 || se>=100)return;
    for(auto i:v[from]){
        if(i.second.first + st >ansSt || i.second.first + st ==100 || i.second.second + se >=100 )continue;
        else if(vis[i.first]==0){
            if(i.first == to){
                if(i.second.first + st == ansSt && i.second.second + se <ansSe)ansSe = i.second.second+se;
                if(i.second.first + st < ansSt)ansSt = i.second.first+st, ansSe = i.second.second + se;
                isAns = 1;
                continue;
            }
            vis[i.first] = 1;
            dfs(vis, v, i.first, to, st+i.second.first, se+i.second.second);
            vis[i.first] = 0;
        }
    }
}

signed main(){

    int n,e;
    while(cin>>n>>e && !(!n && !e)){
        ansSe =100, ansSt =100, isAns = 0;
        vector<vector<pair<int,pair<int,int>>>>v(n+1);
        vector<int>vis(n+1, 0);
        int src, dst;cin>>src>>dst;
        int x, y, st, se;
        while(e--){
            cin>>x>>y>>st>>se;
            v[x].push_back({y,{st,se}});
            v[y].push_back({x,{st,se}});
        }

        dfs(vis, v, src, dst, 0, 0);
        if(isAns){
            cout<<100-ansSt<<"% "<<100-ansSe<<"%"<<endl;
        }
        else{
            cout<<"Passed out\n";
        }
    }

    return 0;
}