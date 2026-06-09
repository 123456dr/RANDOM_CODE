// Code/UT/Data_Structure/graph/graph_F.pdf
/*
- 建立二維陣列，記錄每個節點相連接的節點以及權重v
- Dijkstra priority queue: 
    - 一個distance陣列紀錄(t, i)起點到達i節點的最短距離x
    - 先丟入(0, s)代表起點到達起點的距離0
    - 接著pop直到佇列為空，每次pop出一組就遍歷(x, u)u的所有v[u]
        - 並且若[x+u到該節點的邊權重]>distance[v[u]]則跳過
        - 否則跟新最小值並丟入佇列(x+u到該節點邊權重也就是新最小值, 該節點)
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

int v, e, s;
vector<vector<pair<int, int>>> vt; //先權重再節點
vector<int> solve(){
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int,int>>> pq;
    vector<int>distance(v+1, 1e9);
    pq.push({0,s});
    while(!pq.empty()){
        int x, id;
        pair<int, int>temp = pq.top();
        pq.pop();
        x = temp.first, id = temp.second;
        if(distance[id] < x)continue;
        distance[id] = x;
        for(auto i:vt[id]){
            if(x+i.first < distance[i.second])distance[i.second] = x+i.first, pq.push({x+i.first,i.second});
        }
    }
    return distance;
}


signed main(){
    int t;cin>>t;
    while(t--){
        cin>>v>>e>>s;
        vt.clear();
        vt.resize(v+1);
        for(int i=0;i<e;i++){
            int x, y, w;
            cin>>x>>y>>w;
            vt[x].push_back(make_pair(w,y));
            vt[y].push_back({w,x});
        }
        for(auto &i:vt){
            sort(i.begin(), i.end());
        }
        auto ans = solve();

        int pass = 1;
        for(auto i:ans){
            if(pass){
                pass = 0;
            }
            else cout<<i<<" ";
        }
        cout<<endl;
    }
    return 0;
}