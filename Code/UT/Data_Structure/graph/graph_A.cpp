#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int v, e, t;
    while(cin>>v>>e>>t && !(v==e && v==t &&v==0)){
        if(t == 0){
            vector<vector<int>> vt(v+1, vector<int>(v+1, 100));
            for(int i=0;i<=v;i++)vt[i][i] = 0;
            for(int i=0;i<e;i++){
                int x, y, w;
                cin>>x>>y>>w;
                vt[x][y] = w;
                vt[y][x] = w;
                // vt[i+1][i+1] = 0; 我是大天才 直接期末考RUN ERROR
            }
            for(int i=1;i<=v;i++){
                for(int j=1;j<=v;j++){
                    printf("%3lld ", vt[i][j]);
                }cout<<endl;
            }
        }
        else{
            vector<vector<pair<int,int>>> vt(v+1);
            for(int i=0;i<e;i++){
                int x, y, w;
                cin>>x>>y>>w;
                vt[x].push_back({y, w});
                vt[y].push_back({x, w});
            }
            for(int i=1;i<=v;i++){
                cout<<i<<" ";
                sort(vt[i].begin(), vt[i].end());
                for(auto j:vt[i]){
                    cout<<j.first<<" "<<j.second<<" ";
                }
                cout<<endl;
            }
        }
        cout<<endl;
    }

    return 0;
}