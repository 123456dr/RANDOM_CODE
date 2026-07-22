// https://cses.fi/problemset/task/1091
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m;cin>>n>>m;
    multiset<int>mst;
    while(n--){int x;cin>>x;mst.insert(x);}
    while(m--){
        int x;cin>>x;
        auto tar = mst.upper_bound(x);
        if(tar != mst.begin()){
            tar--;
            cout<<*tar<<'\n';
            mst.erase(tar);
        }
        else cout<<-1<<'\n';
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