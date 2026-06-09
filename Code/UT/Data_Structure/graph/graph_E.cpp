// Code/UT/Data_Structure/graph/graph_E.pdf
/*
思路:
- 儲存每條邊的過路費
- DSU 互斥集
- 小到大排序過路費，從最小的開始走訪，如果當前路線連接的兩節點老大不同則走訪之並更新老大，累加該條路過路費
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long


struct edges{
    int x;
    int y;
    int p;
};

vector<int>parent;
vector<edges>v;

int findParent(int x){
    if(x == parent[x]){
        return x;
    }
    return findParent(parent[x]);
}


int solve(){
    int ans = 0;
    int sz = v.size();
    for(int i=0;i<sz;i++){
        int father1 = findParent(v[i].x), father2 = findParent(v[i].y);
        if(father1 != father2){
            ans += v[i].p;
            parent[father1] = father2;
        }
    }
    return ans;
}


bool cmp(edges a, edges b){
    return a.p<b.p;
}

signed main(){

    int n, e;
    while(cin>>n>>e){
        parent.clear();
        parent.resize(n+1);
        v.clear();
        v.resize(e);

        for(int i=0;i<e;i++){
            cin>>v[i].x>>v[i].y>>v[i].p;
        }
        sort(v.begin(), v.end(), cmp);

        int id=0;
        for(auto &i:parent)i=id++;

        cout<<solve()<<endl;
        
    }
    return 0;
}