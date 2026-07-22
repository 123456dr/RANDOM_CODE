// https://cses.fi/problemset/task/1619
/* 差分 */
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    map<int, int>diff;
    while(n--){
        int a, b;cin>>a>>b;
        diff[a] = 1;
        diff[b] = -1;
    }
    int mx = 0;
    int cnt = 0;
    for(auto i:diff){
        cnt += i.second;
        mx = max(cnt, mx);
    }
    cout<<mx;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}