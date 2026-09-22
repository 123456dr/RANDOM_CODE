#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int v, e, t;
    while(cin>>v>>e>>t && !(!v && !e && !t)){
        if(t == 0){
            vector<vector<int>>arr(v, vector<int>(v, 100));
            for(int i=0;i<v;i++)arr[i][i]=0;
            while(e--){
                int x, y;
                cin>>x>>y>>arr[x-1][y-1];
                arr[y-1][x-1] = arr[x-1][y-1];
            }
            for(vector<int> i:arr){
                for(auto j:i)printf("%3d ",j);
                cout<<endl;
            }
        }
        else{
            vector<vector<pair<int,int>>>arr(v);
            while(e--){
                int x, y, d;
                cin>>x>>y>>d;
                arr[x-1].push_back({y, d});
                arr[y-1].push_back({x, d});
            }
            int ind = 1;
            for(vector<pair<int, int>> i:arr){
                sort(i.begin(), i.end());
                cout<<ind++<<" ";
                for(auto j:i)cout<<j.first<<" "<<j.second<<" ";
                cout<<endl;
            }
        }
        cout<<endl;
    }
}

signed main(){
    solve();
    return 0;
}