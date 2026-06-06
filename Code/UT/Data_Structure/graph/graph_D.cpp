// Code/UT/Data_Structure/graph/graph_D.pdf

#include <bits/stdc++.h>
using namespace std;
#define int long long

int cnt = 0;
int n, e;
int ans = 0;

int findParent(int x, vector<int> &parent){
    if(parent[x] == x) return x;
    return parent[x] = findParent(parent[x], parent);
}

int solve(vector<int> &parent, vector<pair<int, pair<int, int>>> &v){
    int id = 0;
    while(cnt < n-1 && id<e){
        int root1, root2;
        root1 = findParent(v[id].second.first, parent);
        root2 = findParent(v[id].second.second, parent);
        if(root1 != root2){
            parent[root1] = root2;
            ans += v[id].first;
            cnt++;
        }
        id++;
    }
    return 0;
}

signed main(){
    int t;cin>>t;
    while(t--){
        cnt = 0;
        ans = 0;
        cin>>n>>e;
        vector<pair<int, pair<int, int>>>v;
        vector<int>parent(n+1);
        for(int i=0;i<e;i++){
            int x, y, w;
            cin>>x>>y>>w;
            v.push_back({w, {x, y}});
        }
        for(int i=0;i<n;i++){
            parent[i+1] = i+1;
        }
        sort(v.begin(), v.end());
        solve(parent, v);
        cout<<ans << endl;

    }

    return 0;
}