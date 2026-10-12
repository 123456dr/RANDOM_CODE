// https://cses.fi/problemset/task/1141
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int l = 0;
    int n;cin>>n;
    vector<pair<int, int>>v(n);
    for(int i=0;i<n;i++)cin>>v[i].first, v[i].second = i;
    set<int>num;
    int ans = 0;
    for(int i=0;i<n;i++){
        if(num.find(v[i].first) != num.end()){
            ans = max(ans, i - 1 - l);
            l = v[i].second + 1;
            
        }
        else{

        }
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}